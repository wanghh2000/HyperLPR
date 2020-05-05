# coding=utf-8
import base64
import time
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

import cv2
import numpy as np

# 导入opencv

from hyperlpr_py3 import pipline
# 导入车牌识别库

# Flask是由python实现的一个web微框架，让我们可以使用Python语言快速实现一个网站或Web服务。
app = Flask(__name__)
# 设置App name


def recognize(filename):
    image = cv2.imread(filename)
    # 通过文件名读入一张图片 放到 image中
    return pipline.RecognizePlateJson(image)
    # 识别一张图片并返回json结果

# 识别函数


def recognizeBase64(base64_code):
    file_bytes = np.asarray(
        bytearray(base64.b64decode(base64_code)), dtype=np.uint8)
    image_data_ndarray = cv2.imdecode(file_bytes, 1)
    return pipline.RecognizePlateJson(image_data_ndarray)


@app.route('/uploader', methods=['GET', 'POST'])  # 设置请求路由
def upload_file():
    if request.method == 'POST':
        # 如果请求方法是POST
        f = request.files['file']
        f.save("./images_rec/"+secure_filename(f.filename))
        # 保存请求上来的文件
        t0 = time.time()
        res = recognize("./images_rec/"+secure_filename(f.filename))
        print("识别时间", time.time() - t0)
        return res
        # 返回识别结果

        # return 'file uploaded successfully'
    return render_template('upload.html')

def recog_method_1(imgfile):
    # 识别方法1
    # 通过文件名读入一张图片放到image中
    image = cv2.imread(imgfile)
    result = pipline.RecognizePlateJson(image)
    print("result = %s" % (result))

def recog_method_2(imgfile):
    # 识别方法2
    image = cv2.imread(imgfile)
    img, res_set = pipline.SimpleRecognizePlateByE2E(image)
    print("result = %s" % (res_set))
    cv2.imshow("img", img)
    cv2.waitKey(0)

def recog_method_3(imgfile):
    # 识别方法3
    image = cv2.imread(imgfile)
    img, res_set = pipline.SimpleRecognizePlate(image)
    print("result = %s" % (res_set))
    cv2.imshow("img", img)
    cv2.waitKey(0)

if __name__ == '__main__':
    # 入口函数
    # print("Run on http://127.0.0.1:8000/uploader")
    # app.run("0.0.0.0", port=8000)
    # 运行app 指定IP 指定端口

    #res = recognize("./images_rec/7.jpg")
    #print("res识别结果为:", res)


    filename = "./images_rec/6.jpg"
    
    # recog_method_1(filename)

    # recog_method_2(filename)

    recog_method_3(filename)



