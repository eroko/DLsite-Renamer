#!/usr/bin/env python
# coding=utf-8
# @Software: PyCharm

from PIL import Image
import os
import re


def make_ico_file(src_image_file, dist_ico_file, size_list=None):
    """
    :param src_image_file:
    :param dist_ico_file:
    :return:
    """
    default_size_list = [
        (256, 256),
        (128, 128),
        (64, 64),
        (48, 48),
        (32, 32),
        (24, 24),
        (16, 16)
    ]
    size_list = size_list or default_size_list
    image = Image.open(src_image_file)
    image = image.convert('RGBA')
    image.thumbnail([256, 256])
    width, height = image.size
    new_image = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
    if width == 256:
        upper = (256 - height) // 2
        new_image.paste(image, (0, upper))
    elif height == 256:
        left = (256 - width) // 2
        new_image.paste(image, (left, 0))
    else:
        print('error')
    # image_cropped = image.crop((0, 0, 256, 256))

    # new_image.save(r'.\test\re.png')
    new_image.save(dist_ico_file, sizes=size_list)


def listdirs(folder):
    return [
        d for d in (os.path.join(folder, d1) for d1 in os.listdir(folder))
        if os.path.isdir(d)
    ]


def listfiles(folder):
    return [
        d for d in (os.path.join(folder, d1) for d1 in os.listdir(folder))
        if os.path.isfile(d)
    ]


def find_getchu_cover(folder):
    pattern = r'c[0-9]+package\.jpg'
    f = listfiles(folder)

    for file in f:
        result = re.search(pattern, file)
        if result is not None:
            return result.group()


if __name__ == '__main__':
    base_dir = r'E:\BaiduNetdiskDownload\Sync'

    dirs = listdirs(base_dir)
    cover_path = ''

    for name in dirs:
        if os.path.exists(name + "\\cover.jpg"):
            cover_path = name + "\\cover.jpg"
        elif find_getchu_cover(name) is not None:
            cover_path = name + '\\' + find_getchu_cover(name)
        else:
            print("Cover Not Found")
            break
        make_ico_file(src_image_file=cover_path,
                      dist_ico_file=name + '\\fic.ico')

        desktop_ini = ["[.ShellClassInfo]\n\r", "IconResource=fic.ico,0\n\r", 'FolderType=Pictures']
        with open(name + '\\desktop.ini', 'w') as f:
            f.writelines(desktop_ini)
            f.close()
        print(name)
        os.system('attrib +s +h ' + '"' + name + '"' + '\\desktop.ini')
        os.system('attrib +r ' + '"' + name + '"')
