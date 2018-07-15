# -*- coding: utf-8 -*-

from PIL import Image, ImageEnhance
import pytesseract
import queue


def binarizing(img,threshold):
    """传入image对象进行灰度、二值处理"""
    img = img.convert("L") # 转灰度
    pixdata = img.load()
    w, h = img.size
    # 遍历所有像素，大于阈值的为黑色
    for y in range(h):
        for x in range(w):
            if pixdata[x, y] < threshold:
                pixdata[x, y] = 0
            else:
                pixdata[x, y] = 255
    return img

def vertical(img):
    """传入二值化后的图片进行垂直投影"""
    pixdata = img.load()
    w,h = img.size
    ver_list = []
    # 开始投影
    for x in range(w):
        black = 0
        for y in range(h):
            if pixdata[x,y] == 0:
                black += 1
        ver_list.append(black)
    # 判断边界
    l,r = 0,0
    flag = False
    cuts = []
    for i,count in enumerate(ver_list):
        # 阈值这里为0
        if flag is False and count > 0:
            l = i
            flag = True
        if flag and count == 0:
            r = i-1
            flag = False
            cuts.append((l,r))
    return cuts


def cfs(img):
    """传入二值化后的图片进行连通域分割"""
    pixdata = img.load()
    w,h = img.size
    visited = set()
    q = queue.Queue()
    offset = [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]
    cuts = []
    for x in range(w):
        for y in range(h):
            x_axis = []
            y_axis = []
            if pixdata[x,y] == 0 and (x,y) not in visited:
                q.put((x,y))
                visited.add((x,y))
            while not q.empty():
                x_p,y_p = q.get()
                for x_offset,y_offset in offset:
                    x_c,y_c = x_p+x_offset,y_p+y_offset
                    if (x_c,y_c) in visited:
                        continue
                    visited.add((x_c,y_c))
                    try:
                        if pixdata[x_c,y_c] == 0:
                            q.put((x_c,y_c))
                            x_axis.append(x_c)
                            y_axis.append(y_c)
                    except:
                        pass
            if x_axis:
                min_x,max_x = min(x_axis),max(x_axis)
                min_y,max_y = min(y_axis),max(y_axis)
                if max_x - min_x >  3:
                    # 宽度小于3的认为是噪点，根据需要修改
                    cuts.append((min_x,min_y,max_x,max_y))
    return cuts

if __name__=='__main__':

    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
    img = Image.open(r'./captcha0HBAA.jpg')
    binimg = binarizing(img, 127)
    cuts = cfs(binimg)
    if len(cuts)<4:
        num = 0
        max = cuts[num][2]-cuts[num][0]
        for i in cuts:
            temp = i[2]-i[0]
            if temp > max:
                num = i
                max = temp
        a = (cuts[num][0]+max//2+1, cuts[num][1], cuts[num][2], cuts[num][3])
        b = (cuts[num][0],cuts[num][1],cuts[num][0]+max//2,cuts[num][3])
        del cuts[num]
        cuts.insert(num, a)
        cuts.insert(num, b)
    str_img = ''
    for i, n in enumerate(cuts, 1):
        pic = binimg.crop(n)
        # pic.save('cut%s.jpg'%i)
        str_img += pytesseract.image_to_string(pic, lang='eng', config='-psm 10')
    print(str_img)


