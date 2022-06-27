# -*-codeing=utf-8-*-
# @Time:2022/5/2219:05
# @Author:xyp
# @File:U_PIX_VALUE.py
# @Software:PyCharm
#复现论文《An improved high capacity data hiding scheme using pixel value adjustment and modulus operation》
#本文采用一种在单像素上面隐藏信息的改进算法，本文当中的n取4，密码消息用的是十六进制的消息
import tool
x=[]
n=4
def hide_message(secrt_message,hide_pic):#传递参数 需要隐藏的16进制秘密信息和覆盖图像
    tool.rgb_to_gray(hide_pic,"./img/gary.png")
    cover_pix=tool.get_gray_pix(hide_pic)
    tran_pix=[]
    for i in range(len(cover_pix)):
        tran_pix.append(cover_pix[i])

    a=int((4*4)/2)
    for i in range(-a,a+1):
        x.append(i)

    for j in range(len(secrt_message)):  #嵌入是核心算法，用嵌入的长度作为外层循环，用需要比对的x值作为内层循环
        for w in range(len(x)):
            f=(cover_pix[j]+w)%16
            if f==secrt_message[j]:
                tran_pix[j]=cover_pix[j]+w
    tool.pix_to_img("./img/img.png",tran_pix,"./img/hide.png")


def get_message(secert_lenth,hide_secert_message_pix):#通过传入隐藏信息的图片来提取消息
    secrt_message=[]
    pix=tool.get_gray_pix(hide_secert_message_pix)
    for i in range(secert_lenth):
        secrt_message.append(pix[i]%16)
    return secrt_message


# hide_message(3,"./img/img.png")