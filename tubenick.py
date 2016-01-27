#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Name: tubenick.py
# Author: pantuts
# Description: Download videos from youtube.
# Use python3 and later.
# Agreement: You can use, modify, or redistribute this tool under 
# the terms of GNU General Public License (GPLv3). This tool is for educational purposes only.
# Any damage you make will not affect the author.

from tuber import Youtuber
from urllib.parse import unquote

import argparse
import re
import sys


def parser():
    parser = argparse.ArgumentParser(description='[A stupid youtube video downloader.]', \
        usage='python3 tubenick.py -q [-f format] [URL or - (STDIN)]')
    parser.add_argument('-q', dest="query", action="store_true", \
        default=False, help='Query video formats.')
    parser.add_argument('-f', metavar="FORMAT", \
        dest='format', default="best", type=str, help='Specify format. [default: best]')
    parser.add_argument('-u', metavar="URL or -", \
        dest='url', help='Youtube url or - (STDIN)')
    return parser.parse_args()


def check_url(url):
    split_url = url.split('/')
    tmp_id = split_url[-1]

    if 'v=' not in url or ('youtube.com' not in url and url != '-') or 'watch?v' not in tmp_id:
        print('[-] ERROR: Invalid link.')
        sys.exit(1)

    eq = tmp_id.index('=') + 1
    if '&' in tmp_id:
        tmp_split = tmp_id.split('&')[0]
        final_id = tmp_split[eq:]
    else:
        final_id = tmp_id[eq:]
    return final_id.strip()


def tube_it(id, fmt=None, query=False):
    tuber = Youtuber(id)
    src = tuber.get_video_info_source()
    if src and 'status=fail' not in src:
        title = tuber.get_title(src)
        xmlsrc = tuber.get_manifest(src)
        if xmlsrc:
            vid_list = tuber.get_videos_list(xmlsrc)
            if query:
                if vid_list:
                    print(title)
                    tuber.query_videos(vid_list)
                else:
                    print('[-] ERROR: Unable to get list of videos.')
            else:
                if fmt != 'best' and fmt not in [key for key, val in vid_list.items()]:
                    print('[-] ERROR: Format not found.')
                    return False
                elif fmt == 'best':
                    # max(list of tuples with (id, res, size))
                    fmt = max(list(filter(None, \
                        [(key, val['height'], float(val['size'].replace('MB', ''))) \
                        if 'video' in val['mime'] else None for key, val in vid_list.items()])), \
                        key=lambda k: k[1])[0]
                    link = vid_list[fmt]['link']
                else:
                    link = vid_list[fmt]['link']

                ext = vid_list[fmt]['ext']
                size = vid_list[fmt]['size']
                fname = title + '.' + ext
                tuber.download(link, fname, size)
        else:
            print('[-] ERROR: Unable to process dash manifest. ' + id)
    else:
        print('[-] ERROR: Unable to get video info source. ' + id)
        if src:
            err = re.findall(r'errorcode=([0-9]{3})', src)
            err = err[0] if err else '?'
            print('[-] YOUTUBE ERROR CODE: ' + err)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Switch with -h for help')
        sys.exit(0)

    try:
        args = parser()
        url = args.url if args.url is not '-' else list(sys.stdin.readlines())
        fmt = args.format
        query = args.query

        if type(url) is not str:
            for u in url:
                vid_id = check_url(u)
                if vid_id:
                    if query:
                        tube_it(vid_id, query=True)
                    else:
                        tube_it(vid_id, fmt=fmt)
        else:
            vid_id = check_url(url)
            if vid_id:
                if query:
                    tube_it(vid_id, query=True)
                else:
                    tube_it(vid_id, fmt=fmt)
    except KeyboardInterrupt:
        print()
        print(".------..------..------..------..------.")
        print("|H.--. ||O.--. ||O.--. ||H.--. ||A.--. |")
        print("| :/\: || :/\: || :/\: || :/\: || (\/) |")
        print("| (__) || :\/: || :\/: || (__) || :\/: |")
        print("| '--'H|| '--'O|| '--'O|| '--'H|| '--'A|")
        print("`------'`------'`------'`------'`------'")
