from PIL import Image
import os
from img_process import grey_to_binary, distortion
import random
import math
from utils import str2vec
import numpy as np

candidates = ['3', '4', '5', '6', '7', '8', 'A', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'Q', 'R', 'T', 'U', 'W', 'X']

def load_templates(dir=os.path.join('.', 'templates')):
    """ load the letter template from ./templates """
    templates = []
    for i in range(24):
        template = [];
        path = os.path.join(dir, "%s" % candidates[i])
        for f in os.listdir(path):
            if f.endswith('.png'):
                image_path = os.path.join(path, f)
                template.append(Image.open(image_path).convert("L"))
        templates.append(template)
    return templates


def create_captcha(templates):

    temp_index = []
    index = []
    margin = []
    width = 0
    height = 0
    for i in range(4):
        temp_index.append(random.randint(0, 23))
        index.append(random.randint(0, len(templates[temp_index[i]])-1))
        margin.append(random.randint(2, 5))
        template = templates[temp_index[i]][index[i]]
        width += template.size[0] + margin[i]
        if template.size[1] > height:
            height = template.size[1]
    width -= margin[3]
    captcha = Image.new('RGBA', (96, 30), (0, 0, 0, 255))
    captcha_str = ""
    start_x = (96 - width) / 2
    for i in range(4):
        template = templates[temp_index[i]][index[i]]
        template = grey_to_binary(template)
        start_y = 30 - template.size[1] - (30 - height) / 2
        captcha.paste(template, (start_x, start_y), mask=template)
        start_x += template.size[0] + margin[i]
        captcha_str += candidates[temp_index[i]]

    captcha = distortion(captcha, (96-width)/2, (30-height)/2)
    return captcha, captcha_str


def gen_dataset(num, templates):
    # print("generating %d dataset..." % num)
    dataset = []
    labels = []
    for _ in range(num):
        captcha, captcha_str = create_captcha(templates)
        dataset.append(np.asarray(captcha.convert("L")).reshape([30 * 96]) / 255)
        labels.append(str2vec(captcha_str))

    return np.array(dataset), np.array(labels)
