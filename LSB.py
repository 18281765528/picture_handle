# -*-codeing=utf-8-*-
# @Time:2022/6/618:30
# @Author:xyp
# @File:LSB.py
# @Software:PyCharm
#本代码是LSB嵌入算法的复现
#嵌入函数需要传递覆盖图像像素，秘密信息的数组，保存隐藏图像的地址。提取函数需要传入隐藏图像的地址，秘密信息的长度，同时返回提取出来的密码信息数组
import tool
def hide_message(cover_img_address,secret_message,output_address):
    cover_pix=tool.get_gray_pix(cover_img_address)
    hide_pix=tool.pix_cover_to_hide(cover_pix)
    for i in range(len(secret_message)):
        if cover_pix[i]&1!=secret_message[i]:
            hide_pix[i]=cover_pix[i]^1
    tool.pix_to_img(cover_img_address,hide_pix,output_address)

def get_secret_message(hide_img_address,secert_message_lenth):
    hide_pix=tool.get_gray_pix(hide_img_address)
    get_secret_message=[]
    for i in range(secert_message_lenth):
        secret_message=hide_pix[i]&1
        get_secret_message.append(secret_message)
    return get_secret_message
