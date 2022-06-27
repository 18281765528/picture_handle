# -*-codeing=utf-8-*-
# @Time:2022/5/615:25
# @Author:xyp
# @File:test.py
# @Software:PyCharm
from PIL import Image
img=Image.open("./img/xyp.jpg")
print(img.size)
img2=img.resize((295,415))
img2.save("./img/xyp2.jpg")