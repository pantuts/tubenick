#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: pantuts
# Agreement: You can use, modify, or redistribute this tool under 
# the terms of GNU General Public License (GPLv3). This tool is for educational purposes only.
# Any damage you make will not affect the author.

from urllib.request import Request, urlopen, urlretrieve
from urllib.parse import unquote
from urllib.request import URLError
from xml.dom import minidom

import os
import random
import re
import string
import sys


class Youtuber(object):
    """
    Stupid as it is.
    Limitations: some videos has restrictions downloading manifest file.
    Reasons may be age, geolocation, and I don't know about the others.
    """

    def __init__(self, video_id):
        self.video_id = video_id
        self.video_info_url = 'http://www.youtube.com/get_video_info?video_id='
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) \
                Gecko/20100101 Firefox/16.0'
        }

    def requestor(self, video_info=False, manifest=False, url=None):
        if video_info:
            url = self.video_info_url + self.video_id + '&gl=US&hl=en' + \
            '&eurl=https://youtube.googleapis.com/v/' + self.video_id
        if manifest:
            url = url
        try:
            req = Request(url, headers=self.headers)
            res = urlopen(req)
            src = str(res.read().decode('utf-8'))
            return src
        except URLError as e:
            print('[-] URLERROR: ' + e.reason)
            return False

    def get_video_info_source(self):
        src = self.requestor(video_info=True)
        return src

    def get_title(self, src):
        title = re.findall(r'title=(.+?)&', src)
        title = title[0].replace('+', ' ') if title else \
            'RandomTitle-' + ''.join(random.choice(string.ascii_lowercase) for i in range(12))
        title = unquote(unquote(title.replace('+', ' ')))
        return title

    def get_manifest(self, src):
        manifest = re.findall(r'(https?.{0,10}manifest\.googlevideo\.com.+?)&', src) or []
        if not manifest:
            return False
        xmlsrc = self.requestor(manifest=True, url=unquote(unquote(manifest[0])))
        if not xmlsrc:
            return False
        fname = os.path.expanduser('~') + '/.tubenick-xmlsrc'
        with open(fname, 'a') as f:
            f.write(xmlsrc)
        return fname

    def get_videos_list(self, xmlsrc):
        try:
            xmldoc = minidom.parse(xmlsrc)
        except Exception as e:
            print('[-] ERROR: ' + e.reason)
            if os.path.exists(xmlsrc):
                os.remove(xmlsrc)
            return False

        vid_list = {}
        adaptation_set = xmldoc.getElementsByTagName('AdaptationSet')
        for adapset in adaptation_set:
            representation = adapset.getElementsByTagName('Representation')
            for rptn in representation:
                mime = adapset.attributes['mimeType'].value
                ext = mime.split('/')[-1]
                vid_format = rptn.attributes['id'].value
                vid_list.update({
                    vid_format: {}
                })
                vid_list[vid_format]['mime'] = mime
                vid_list[vid_format]['ext'] = ext

                if 'audio' in mime:
                    vid_list[vid_format]['resolution'] = 'audio'
                else:
                    width = rptn.attributes['width'].value
                    height = rptn.attributes['height'].value
                    vid_list[vid_format]['width'] = width
                    vid_list[vid_format]['height'] = height
                    vid_list[vid_format]['resolution'] = width + 'x' + height

                base_url = rptn.getElementsByTagName('BaseURL')
                for bu in base_url:
                    size = int(bu.attributes['yt:contentLength'].value) * 1e-6
                    vid_list[vid_format]['size'] = '{0:.2f}'.format(size) + 'MB'
                    vid_list[vid_format]['link'] = bu.firstChild.data

        os.remove(xmlsrc)
        return vid_list

    def query_videos(self, vid_list):
        print('fmt{:>15}{:>15}{:>15}'.format('res', 'mime', 'size'))
        for key, val in vid_list.items():
            print(key + "{:>15}".format(val['resolution']) + \
                "{:>15}".format(val['mime']) + "{:>15}".format(val['size']))

    def download(self, link, fname, fsize):
        try:
            def download_progress(counter, bsize, size):
                prog_percent = (counter * bsize * 100) / size
                sys.stdout.write('\r' + fname + ' [' + fsize + ']' + \
                    ' .......................... %2.f%%' % int(prog_percent))
                sys.stdout.flush()
            urlretrieve(link, fname, reporthook=download_progress)
        except Exception as e:
            print('[-] ERROR: ' + e.reason)
            return False
