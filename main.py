from __future__ import unicode_literals
from genericpath import exists
import os
import time
import json
from tkinter import filedialog
from tkinter import *
import url_check
import config
import downloader


def main():

    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    root = Tk()
    root.withdraw()

    if not os.path.exists('data.json'):

        print("Choose default destination folder:")

        folder_selected = filedialog.askdirectory()
        while folder_selected == "":
            folder_selected = filedialog.askdirectory()

        with open('data.json', 'w') as f:
            data = {
                'path': f'{folder_selected}'
            }
            json.dump(data, f)

    mode = 'mp3'
    input_text = 'mp4'

    links = []
    q = ''

    while q != "e":

        ydl_opts = config.return_config(mode)

        DEFAULT_PATH = ydl_opts['DEFAULT_PATH']

        q = input(
            f"Insert links \n *-download given links\n l-clear links list\n c-clear default dir\n m-switch to {input_text}\n d-change default dir (current: {DEFAULT_PATH})\n e-exit\n{links}\n: ")

        if q == 'c':
            for i in os.listdir(DEFAULT_PATH):
                if i.endswith('.mp3') or i.endswith('.mp4'):
                    os.remove(f'{DEFAULT_PATH}/{i}')

        elif q == '*':
            if not links:
                print("List is empty!")
                time.sleep(1)
            else:
                downloader.download(links, ydl_opts)
            print("Done!")
            time.sleep(1)
            links.clear()

        elif q == 'e':
            quit()

        elif q == 'l':  # lowercase L
            links = []

        elif q == 'm':
            if mode == 'mp3':
                mode = 'mp4'
                input_text = 'mp3'
            else:
                mode = 'mp3'
                input_text = 'mp4'

        elif q == 'd':
            folder_selected = filedialog.askdirectory()

            with open('data.json', 'w') as f:
                data = {
                    'path': f'{folder_selected}'
                }
                json.dump(data, f)

        else:
            if url_check.check_url(q):
                links.append(q)
            else:
                print("Invalid URL!")
                time.sleep(1)

        os.system('cls')


if __name__ == "__main__":
    import argparse
    import sys
    import downloader

    if len(sys.argv) > 1:

        parser = argparse.ArgumentParser(description='yt_downloader')

        parser.add_argument(
            "-L", "--links", help="links seperated with a space", required=True, nargs="*")

        parser.add_argument('-M', '--mode', help='mp3 or mp4', required=True)

        parser.add_argument('-D', '--destination',
                            help='destination folder', required=True)

        args = parser.parse_args()

        links = args.links
        mode = args.mode
        destination = args.destination

        ydl_opts = config.return_config(mode, destination)

        downloader.download(links, ydl_opts)

    else:
        main()
