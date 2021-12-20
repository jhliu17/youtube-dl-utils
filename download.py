# Script for downloading cs61c videos

# Requirement: install youtube-dl (https://github.com/rg3/youtube-dl/)

import os
import re
import argparse

from vtt2srt import vtt_to_srt


def download_files(vid_root, url_file):
    with open(url_file, 'r') as uf:
        vid_key = uf.readlines()
        vid_list = list(map(lambda x: space.split(x.strip()), vid_key))

    for vid_prefix, vid_url in vid_list:
        print(f"Downloading {vid_prefix} at {vid_url}")

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
        else:
            print(f'Video {videos} already exist')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--input_file', '-i', type=str, help='Download url path of videos.')
    parser.add_argument('--video_root', '-s', default='video', type=str, help='Root path to save downloaded video.')
    parser.add_argument('--proxy_command', '-p', default='', type=str, help='Proxy setting to download video.')
    parser.add_argument('--vtt_to_str', '-c', default=False, action="store_true", help='Whether to conver vtt subtitle into str format.')

    args = parser.parse_args()
    vid_root = args.video_root
    url_file = args.input_file
    proxy_cmd = args.proxy_command

    space = re.compile(r'\s+')
    if not os.path.isdir(vid_root):
        os.mkdir(vid_root)

    print('\nStart downloading videos...\n')
    download_files(vid_root, url_file)

    if args.vtt_to_str:
        print('\nStart converting vtt files...\n')
        for root, dirs, files in os.walk(vid_root):
            for name in files:
                if name.endswith('.vtt'):
                    vtt_to_srt(os.path.join(root, name))

    print('\nDownload Finished!')
