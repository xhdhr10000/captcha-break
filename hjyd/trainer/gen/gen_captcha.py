from PIL import Image
import os
from img_process import rotate_and_cut
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
        for j in range(4):
            image_path = os.path.join(dir, "%s" % candidates[i], "%s%d.png" % (candidates[i], j))
            template.append(Image.open(image_path).convert("L"))
        templates.append(template)
    return templates


def create_captcha(templates):

    captcha = Image.new('RGBA', (96, 30), (0, 0, 0, 255))
    captcha_str = ""
    for i in range(4):
        temp_index = random.randint(0, 23)
        index = random.randint(0, 3)
        captcha_str += candidates[temp_index]
        template = templates[temp_index][index]
        template = rotate_and_cut(template, random.randint(-20, 20))
        width_range = math.fabs(24 - template.size[0])
        height_range = math.fabs(30 - template.size[1])

        start_x_pos = i * 24 + random.randint(-width_range, width_range)
        start_y_pos = random.randint(0, height_range)

        captcha.paste(template, (start_x_pos, start_y_pos), mask=template)
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
