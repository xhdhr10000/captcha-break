from PIL import Image
import numpy as np


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
    for y in range(img_arr.shape[1]):
        count = 0
        for x in range(img_arr.shape[0]):
            if img_arr[x, y] == 255:
                count += 1

        if count != img_arr.shape[0]:
            if row[0] == 0:
                row[0] = y
            else:
                row[1] = y+1

    # search for column
    for x in range(img_arr.shape[0]):
        count = 0
        for y in range(img_arr.shape[1]):
            if img_arr[x, y] == 255:
                count += 1
        if count != img_arr.shape[1]:
            if col[0] == 0:
                col[0] = x
            else:
                col[1] = x+1

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

def rotate_and_cut(im, degree):
    im = rotate(im, degree)
    im = cut(im)

    im = grey_to_binary(im)
    return im

