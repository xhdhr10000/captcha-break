#!/usr/bin/env python
# coding:utf-8
from __future__ import print_function

import os

import requests
import uuid
from PIL import Image
from bs4 import BeautifulSoup

url = "http://apply.bjhjyd.gov.cn/apply/validCodeImage.html"
downloader_dir = os.path.dirname(os.path.abspath(__file__))
captchas_dir = os.path.join(downloader_dir, 'captchas')

def download(number):
    files = []
    for i in range(number):
        try:
            resp = requests.get(url)
            filename = str(uuid.uuid4()) + ".png"
            filepath = os.path.join(captchas_dir, filename)
            with open(filepath, 'wb') as f:
               f.write(resp.content)

            print(filename)
            files.append(filename)
        except Exception as ex:
            raise
            print(Exception, ":", ex)
    return files

if __name__ == "__main__":
    download(10)