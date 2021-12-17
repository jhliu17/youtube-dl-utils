# Script for downloading cs61c videos

# Requirement: install youtube-dl (https://github.com/rg3/youtube-dl/)

import os
import re

vid_root = 'video'
url_file = 'urls.txt'
proxy_cmd = 'socks5://127.0.0.1:1086'
space = re.compile(r'\s+')
if not os.path.isdir(vid_root):
    os.mkdir(vid_root)


with open(url_file, 'r') as uf:
    vid_key = uf.readlines()
    vid_list = list(map(lambda x: space.split(x.strip()), vid_key))

for vid_prefix, vid_url in vid_list:
    print("Start download the following videos:")
    print('%s-%s' % (vid_prefix, vid_url))

    file_path = os.path.join(vid_root, vid_prefix)
    if not os.path.isdir(file_path):
        os.mkdir(file_path)

    files = os.listdir(file_path)
    videos = list(filter(lambda x: x.endswith('.mkv') or x.endswith('.mp4'), files))

    if not videos:
        result = 1
        while result != 0:
            if proxy_cmd:
                result = os.system(' '.join(("youtube-dl -o", "\"%s\"" % (file_path + "/%(playlist_index)s-%(title)s.%(ext)s"), "--write-auto-sub", "--proxy", proxy_cmd, "\"%s\"" % vid_url)))
            else:
                result = os.system(' '.join(("youtube-dl -o", "\"%s\"" % (file_path + "/%(playlist_index)s-%(title)s.%(ext)s"), "--write-auto-sub", "\"%s\"" % vid_url)))
