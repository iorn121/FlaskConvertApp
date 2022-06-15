from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import numpy as np
import cv2
import os
from datetime import datetime as dat

app = Flask(__name__, static_url_path='')

# 画像を保存するpathを指定
IMG_DIR = '/static/images/'
BASE_DIR = os.path.dirname(__file__)
IMG_PATH = BASE_DIR+IMG_DIR



@app.route('/')
def index():
    return 'hello world'


if __name__ == '__main__':
    app.run()
