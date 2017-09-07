# coding=utf-8
from __future__ import print_function

import os
import sys

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
basedir = os.getcwd()
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.append('trainer')
sys.path.append('downloader')

from gen.gen_captcha import gen_dataset, load_templates, candidates
from gen.img_process import grey_to_binary
from model.nn import load_model_nn
from model.common import find_model_ckpt
import tensorflow as tf
from gen.utils import vec2str
import numpy as np
from PIL import Image
from downloader import download

def show_im(dataset):
    data = np.uint8(dataset[0]).reshape((30, 96)) * 255
    im = Image.fromarray(data)
    im.show()

def test_model(captcha):
    im = Image.open(os.path.join(basedir, 'downloader', 'captchas', captcha))
    im = im.convert('L')
    im.show()
    im = grey_to_binary(im)
    # templates = load_templates(os.path.join('trainer', 'templates'))

    model = load_model_nn()
    x = model['x']
    keep_prob = model['keep_prob']
    saver = model['saver']
    prediction = model['prediction']
    graph = model['graph']
    model_ckpt_path, _ = find_model_ckpt(os.path.join('trainer', '.checkpoint'))
    # print("Used the model:", model_ckpt_path)


    with tf.Session(graph=graph) as session:
        tf.global_variables_initializer().run()
        saver.restore(session, model_ckpt_path)

        # dataset, labels = gen_dataset(1, templates)  # generate one image
        dataset = []
        dataset.append(np.asarray(im.convert("L")).reshape([30 * 96]) / 255)

        label = prediction.eval(feed_dict={x: dataset, keep_prob: 1.0}, session=session)[0]
        string = ''
        for i in range(4):
            string += chr(label[i] + ord('0'))
        print(string)


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        captcha = download(1)[0]
    else:
        captcha = sys.argv[1]
    test_model(captcha)
