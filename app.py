from datetime import datetime as dat
import os
import cv2
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session

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
    # 笑い男の画像を投下して用意
    warai = cv2.imread("nc73730.png", -1)

    img_name = ""

    text1 = "いらっしゃい"
    text2 = "顔の写った写真を送信するんだ"

    if request.method == "POST":
        # 画像をロード
        stream = request.files["raw_image"].stream
        img_array = np.asarray(bytearray(stream.read()), dtype=np.uint8)

        if len(img_array) > 0:
            # グレースケールに変換
            img = cv2.imdecode(img_array, 1)
            width, height = img.shape[:2]
            gray = rgb_to_gray(img)
            # 識別器を読み込み
            face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades+'haarcascade_frontalface_default.xml')

            faces = face_cascade.detectMultiScale(
                gray, scaleFactor=1.15, minNeighbors=2, minSize=(50, 50))
            for (x, y, w, h) in faces:
                warai_resize = cv2.resize(warai, (w, h))
                img[y:y+h, x:x+w] = img[y:y+w, x:x+w] * \
                    (1-warai_resize[:, :, 3:]/255)+warai_resize[:,
                                                                :, :3]*(warai_resize[:, :, 3:]/255)

            # データの保存名
            now_date = dat.now()
            img_name = "gray"+now_date.strftime("%Y-%m-%d-%H-%M-%S")+".png"
            cv2.imwrite(os.path.join(IMG_PATH+img_name), img)
            text1 = "おめでとう"
            text2 = "これであなたも笑い男だ"
    return render_template("index.html", img_name=img_name, text1=text1, text2=text2)


if __name__ == "__main__":
    app.run(debug=False)
