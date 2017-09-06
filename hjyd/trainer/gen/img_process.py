from PIL import Image
import numpy as np
import random


def rotate(img, angle):
    """ rotate the image """
    im2 = img.convert('RGBA')
    rot = im2.rotate(angle, expand=1)
    fff = Image.new('RGBA', rot.size, (255,) * 4)
    out = Image.composite(rot, fff, rot)
    return out.convert(img.mode)


def cut(img):
    """ cut the redundant white padding of the image """
    img_arr = np.asarray(img)
    row = [0, 0]  # the cut row range
    col = [0, 0]  # the cut column range
    # search for row
    for x in range(img_arr.shape[0]):
        count = 0
        for y in range(img_arr.shape[1]):
            if img_arr[x, y] == 255:
                count += 1

        if count != img_arr.shape[1]:
            if row[0] == 0:
                row[0] = x
            else:
                row[1] = x+1

    # search for column
    for y in range(img_arr.shape[1]):
        count = 0
        for x in range(img_arr.shape[0]):
            if img_arr[x, y] == 255:
                count += 1
        if count != img_arr.shape[0]:
            if col[0] == 0:
                col[0] = y
            else:
                col[1] = y+1

    return Image.fromarray(np.uint8(img_arr[row[0]: row[1], col[0]: col[1]]))

def grey_to_binary(im):
    im = im.convert("RGBA")
    datas = im.getdata()
    newData = list()
    for item in datas:
        if item[0] < 128 and item[1] < 128 and item[2] < 128:
            newData.append((255, 255, 255, 255))
        else:
            newData.append((0, 0, 0, 255))

    im.putdata(newData)
    return im

def distortion(im, w, h):
    img_arr = np.array(np.asarray(im))

    a,b = random.random() * 2 * np.pi, random.random() * 2 * np.pi
    for y in range(img_arr.shape[1]):
        cur = int(np.sin(min(a,b) + (y+1)/float(img_arr.shape[1])*abs(a-b)) * 5)
        cur = min(cur, h)
        cur = max(cur, -h)
        img_arr[:,y] = np.roll(img_arr[:,y], cur, axis=0)

    a,b = random.random() * 2 * np.pi - np.pi, random.random() * 2 * np.pi - np.pi
    for x in range(img_arr.shape[0]):
        cur = int(np.sin(min(a,b) + (x+1)/float(img_arr.shape[0])*abs(a-b)) * 5)
        cur = min(cur, w)
        cur = max(cur, -w)
        img_arr[x,:] = np.roll(img_arr[x,:], cur, axis=0)
    ret = Image.fromarray(np.uint8(img_arr))
    return ret

def rotate_and_cut(im, degree):
    im = rotate(im, degree)
    im = cut(im)
    im = grey_to_binary(im)
    return im

