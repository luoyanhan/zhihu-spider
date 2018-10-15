# -*- coding: utf-8 -*-

from PIL import Image, ImageEnhance
import pytesseract
import tesserocr
import queue
from captcha.image import ImageCaptcha
import random
from claptcha import Claptcha
from itertools import groupby

number = ['0','1','2','3','4','5','6','7','8','9']
alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
ALPHABET = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

def get_random_text(char_set = number + alphabet + ALPHABET, char_num = 4):
    li = []
    for i in range(char_num):
        c = random.choice(char_set)
        li.append(c)
    return ''.join(li)

def Claptcha_get(char_text):
    c = Claptcha(char_text, 'C:\Windows\Fonts\ARIALUNI.TTF')
    captcha = c.write('./' + char_text + '.jpg')
    text, im = c.image
    return text, im

def Captcha_get(char_text):
    im = ImageCaptcha()
    im.write(char_text, './' + char_text + '.jpg')
    chptcha = im.generate(char_text)
    chptcha = Image.open(chptcha)
    return chptcha

def binarizing(img,threshold):
    img = img.convert('L')
    pixdata = img.load()
    w, h = img.size
    for i in range(h):
        for j in range(w):
            if pixdata[j, i] < threshold:
                pixdata[j, i] = 0
            else:
                pixdata[j, i] = 255
    return img

def depoint(img):
    pixdata = img.load()
    w, h = img.size
    for y in range(1, h-1):
        for x in range(1, w-1):
            count = 0
            if pixdata[x, y-1] > 245:
                count = count + 1
            if pixdata[x, y+1] > 245:
                count = count + 1
            if pixdata[x-1, y] > 245:
                count = count + 1
            if pixdata[x+1, y] > 245:
                count = count + 1
            if pixdata[x-1, y-1] > 245:
                count = count + 1
            if pixdata[x-1, y+1] > 245:
                count = count + 1
            if pixdata[x+1, y-1] > 245:
                count = count + 1
            if pixdata[x+1, y+1] > 245:
                count = count + 1
            if count > 4:
                pixdata[x, y] = 255
    return img

def vertical(img):
    pixdata = img.load()
    w, h = img.size
    ver_li = []
    for x in range(w):
        black = 0
        for y in range(h):
            if pixdata[x, y] == 0:
                black += 1
        ver_li.append(black)
    left = 0
    right = 0
    flag = False
    cuts = []
    for i, count in enumerate(ver_li):
        if not flag and count > 10:
            left = i
            flag = True
        if flag and count < 10:
            flag = False
            right = i - 1
            cuts.append((left, right))
    return cuts

def cfs(img):
    pixdata = img.load()
    w, h = img.size
    visited = set()
    offset = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    cuts = []
    q = queue.Queue()
    for x in range(w):
        for y in range(h):
            x_axis = []
            if pixdata[x, y] == 0 and (x, y) not in visited:
                q.put((x, y))
                visited.add((x, y))
            while not q.empty():
                x_p, y_p = q.get()
                for x_offset, y_offset in offset:
                    x_c, y_c = x_p + x_offset, y_p + y_offset
                    if (x_c, y_c) in visited:
                        continue
                    visited.add((x_c, y_c))
                    try:
                        if pixdata[x_c, y_c] == 0:
                            q.put((x_c, y_c))
                            x_axis.append(x_c)
                    except:
                        pass
            if len(x_axis) != 0:
                min_x = min(x_axis)
                max_x = max(x_axis)
                if max_x - min_x > 5:
                    cuts.append((min_x, max_x))
    return cuts


if __name__ == "__main__":
    im = Image.open('./ocr7.png')
    im = binarizing(im, 170)
    for i in range(3):
        im = depoint(im)
    cuts = cfs(im)
    print(cuts)
    w, h = im.size
    for i, c in enumerate(cuts, 1):
        im.crop((c[0], 0, c[1], h)).save('./'+str(i)+'.png')


