import os
import sys
import random
from numpy import asarray
from PIL import Image
from urllib.request import urlopen
from staticmap import StaticMap, col_to_char


def main():
    sm = StaticMap()
    im = Image.open(urlopen(sm.get()))
    im = im.convert('RGB')
    w, h = im.size[0], im.size[1] - 22  # remove Google footer
    im = im.crop([0, 0, w, h])
    arr = asarray(im)
    char_array = [['' for i in range(w)] for j in range(h)]
    found_start = False
    known_markers = [(31, 60, 19), (44, 35, 17), (0, 0, 0)]
    for i in range(w):
        for j in range(h):
            _col = tuple(arr[j, i])
            _char = col_to_char(_col)
            if _col[0] < 60 and _col[1] < 60 and _col[2] < 60:
                print("Mark found!")
                if found_start:
                    _char = 'B'
                else:
                    _char = 'A'
                    found_start = True
            char_array[j][i] = _char

    with open(sm.name(), 'wb') as cmap:
        for line in char_array:
            for c in line:
                cmap.write(c.encode())
            cmap.write('\r\n'.encode())


main()
