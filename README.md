tubenick
===================

A stupid youtube video downloader.


Why?
-------

This is a revamp of my previous script at [sourceforge](http://sourceforge.net/projects/tubenickdownloa/).
So why did I do it again even there are plenty of great tools available? Simple, I'm getting rusty so practice is needed.

This script doesn't rely on any external libraries/modules  or api, it just uses **python3 standard library**.
Tested only on Gnu/Linux box.

>**Yeah**
 Honestly, you don't need this one. It's just only to show how to download videos from youtube with python. If you want something cool, try [youtube-dl](https://rg3.github.io/youtube-dl/).


Usage
--------

```
$ python tubenick.py -h

optional arguments:
  -h, --help   show this help message and exit
  -q           Query video formats.
  -f FORMAT    Specify format. [default: best]
  -u URL or -  Youtube url or - (STDIN)
```
Query video formats:
```
$ python tubenick.py -q -u https://www.youtube.com/watch?v=lww1rVA4wDI
```

Default download (highest resolution):
```
$ python tubenick.py -u https://www.youtube.com/watch?v=lww1rVA4wDI
```

Specify format to download:
```
$ python tubenick.py -f 244 -u https://www.youtube.com/watch?v=lww1rVA4wDI
```

Using stdin (I'm using my own script to extract playlist: [youParse.py](https://github.com/pantuts/youParse)):
```
$ ./youParse.py PLAYLIST | python tubenick.py -f 140 -u -

```

Limitation
--------------
Youtube has restrictions. And don't expect too much.

Agreement and Disclaimer
--------------------------------------
You can use, modify, or redistribute this tool under the terms of GNU General Public License (GPLv3).
This tool is for educational purposes only. Any damage you make will not affect the author.