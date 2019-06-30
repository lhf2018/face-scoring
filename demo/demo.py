from aip import AipFace
import base64
import os
import time
import cv2

""" 你的 APPID AK SK """
APP_ID = '16676968'
API_KEY = 'KWgauGu2EMTmTLKnBrLuGzSW'
SECRET_KEY = 'nrBy2qvoE4QYWGzPeZmPneiSH7K4v96e'

client = AipFace(APP_ID, API_KEY, SECRET_KEY)

""" 读取图片 """


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


"""人脸检测"""


def face_test(face_image_path):
    f = get_file_content(face_image_path)  # 读取图片
    data = base64.b64encode(f)  # 将图片内容处理成base64数据

    image = data.decode()  # 转换位json可序列化

    """ 如果有可选参数 """
    options = {}
    options["face_field"] = "beauty"  # 颜值识别的参数
    options["max_face_num"] = 2

    """ 带参数调用人脸检测 """
    result = client.detect(image, "BASE64", options)
    try:
        if result['result']:
            return result['result']['face_list'][0]['beauty']
        else:
            return None
    except Exception as e:
        pass


"""使用电脑摄像头拍照"""


def videoCapture():
    cap = cv2.VideoCapture(0)  # 0为电脑内置摄像头
    f, frame = cap.read()  # 此刻拍照
    cv2.imwrite("./image/" + str(time.strftime("%Y-%m-%d-%H%M%S", time.localtime())) + ".jpg", frame)  # 将拍摄内容保存为jpg图片
    cv2.imshow("capture", frame)
    cv2.waitKey(10)  # 程序在这里挂起暂停执行
    cap.release()  # 关闭调用的摄像头
    cv2.destroyAllWindows()


if __name__ == '__main__':
    videoCapture()
    root_path = './image'
    list = os.listdir(root_path)  # 列出文件夹下所有的目录与文件
    for i in range(0, len(list)):
        time.sleep(1)  # 睡眠一秒,免费调用api有ops限制
        path = os.path.join(root_path, list[i])
        if os.path.isfile(path):
            print(list[i] + ' 评分为：' + str(face_test(path)))
