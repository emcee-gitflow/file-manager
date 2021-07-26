#!/usr/bin/env python3

"""
Automate various bulk file actions; currently includes:
- Sequentially renaming all files in a directory.
- Creating youtube-dl download commands for one or more links.
"""
import os

# testing or development constants
TEST_PATH = 'Backgrounds/'
IGNORE = ('.DS_Store',)
TEST = True


class FileManager:
    """ Store a list of general files. """

    def __init__(self, files):
        self._files = list(files)

    @property
    def files(self):
        return self._files

    @files.setter
    def files(self, files):
        self._files = list(files)


class ImageManager(FileManager):
    """ Image specific file functionality. """
    pass


class VideoManager(FileManager):
    """ Video specific file functionality. """
    pass


def name_prompt() -> str:
    """ Prompt user for an alphanumeric string with dashes. """
    while True:
        name = input(
            'Enter a file name (letters, numbers, and "-" allowed): ').strip()
        if name.replace('-', '').isalnum():
            return name
        print('error: please use only letters, numbers, and dashes.')


def youtube_dl_links():
    """ Populate urls dictionary using video names as keys and their URL for
    the value; print corresponding youtube-dl command for each video.
    """
    urls = {}
    while True:
        item = input(
            'URLs: [a]dd, [v]iew, [d]elete, [r]ename, '
            '[p]rint youtube-dl commands; [b]ack: ').strip().lower()
        if item in ('a',):  # add
            urls[name_prompt()] = input('Enter url to video: ')
        elif item in ('v',):  # view
            for item in urls:
                print(f'{item}: {urls[item]}')
        elif item in ('d',):  # delete
            key = input('Video name: ')
            if key in urls:
                urls.pop(key)
        elif item in ('r',):  # rename
            urls[name_prompt()] = urls.pop(input('Video to change: '))
        elif item in ('p',):  # print youtube-dl commands
            for item in urls:
                print(f'youtube-dl -f best --output "{item}.%(ext)s" '
                      f'"{urls[item]}"')
        elif item in ('b',):  # back
            break
        else:
            continue


def list_files(path: str) -> list[str]:
    """ Given a path, return a list of filenames; exclude those in IGNORE. """
    _, _, filenames = next(os.walk(path))
    return [f for f in filenames if f not in IGNORE]


def split_name(file: str) -> list[str, str]:
    """ Split a filename into its name and extension. """
    return file.split('.')


def rename_files():
    """ Sequentially rename files present in TEST_PATH using a chosen prefix.
    Files are moved to the 'temp' directory; 'temp' directory is created
    if it does not already exist.
    """
    dst_dir = os.path.join(TEST_PATH, 'temp')
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    backgrounds = FileManager(list_files(TEST_PATH))
    prefix = input('Enter a prefix: ')

    num_files = str(len(backgrounds.files[-1]))
    zpad = int(len(num_files))

    for count, file in enumerate(backgrounds.files, 1):
        name, ext = split_name(file)
        src = os.path.join(TEST_PATH, file)
        dst = os.path.join(dst_dir, f'{prefix}_{str(count).zfill(zpad)}.{ext}')
        print(f"os.rename('{src}', '{dst}')" if TEST else os.rename(src, dst))


def main():
    """ CLI menu for testing. """
    while True:
        item = input(
            '[r]ename files, [m]ake video links; [q]uit: ').strip().lower()
        if item in ('r',):  # rename files
            rename_files()
        elif item in ('m',):  # make video links
            youtube_dl_links()
        elif item in ('q',):  # quit
            break
        else:
            continue


if __name__ == '__main__':
    main()
