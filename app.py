from datetime import datetime as dat
import os
import cv2
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, send_from_directory

app = Flask(__name__, static_url_path="")


IMG_DIR = "/static/images/"
BASE_DIR = os.path.dirname(__file__)
IMG_PATH = BASE_DIR+IMG_DIR

# 保存先のフォルダがないときは作成
if not os.path.exists(IMG_PATH):
    os.mkdir(IMG_PATH)

# 画像処理


def rgb_to_gray(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray


@app.route("/", methods=["GET", "POST"])
def index():
    img_name = ""

    if request.method == "POST":
        # 画像をロード
        stream = request.files["raw_image"].stream
        img_array = np.asarray(bytearray(stream.read()), dtype=np.uint8)

        if len(img_array) > 0:
            # グレースケールに変換
            img = cv2.imdecode(img_array, 1)
            gray = rgb_to_gray(img)
            # 識別器を読み込み
            face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades+'haarcascade_frontalface_default.xml')

            faces = face_cascade.detectMultiScale(
                gray, scaleFactor=1.1, minNeighbors=2, minSize=(30, 30))
            for (x, y, w, h) in faces:
                img = cv2.rectangle(
                    img, (x, y), (x+w, y+h), (255, 0, 0), 3)

            # データの保存名
            now_date = dat.now()
            img_name = "gray"+now_date.strftime("%Y-%m-%d-%H-%M-%S")+".png"
            cv2.imwrite(os.path.join(IMG_PATH+img_name), img)
    return render_template("index.html", img_name=img_name)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
