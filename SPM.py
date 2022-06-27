# -*-codeing=utf-8-*-
# @Time:2022/5/3111:01
# @Author:xyp
# @File:SPM.py
# @Software:PyCharm
#代码介绍
#《A data hiding scheme based on single pixel modification with modulus operation》论文复现
import tool


def hide_message(cover_img_address,secret_message,output_address,n):#参数分别是覆盖图像，密码二进制信息，图片输出地址，分组个数
    x=[]
    cover_img_pix=tool.get_gray_pix(cover_img_address)
    hide_img_pix=tool.pix_cover_to_hide(cover_img_pix)
    hix_secret_message=tool.bin_to_hix(secret_message)
    print("将随机产生的二进制密码信息转换成十六进制的密码消息：", hix_secret_message)
    for i in range(-int((2**n/2)),int((2**n)/2+1)):
        x.append(i)
    for i in range(len(hix_secret_message)):
        for j in range(len(x)):
            f=(cover_img_pix[i]+x[j])%2**n
            if f==hix_secret_message[i]:
                hide_img_pix[i]=cover_img_pix[i]+x[j]
                if hide_img_pix[i]<=255 or hide_img_pix[i]>=0:
                    break

    tool.pix_to_img("./img/img.png",hide_img_pix,"./img/hide.png")

    #获取PSNR值  这个论文给的PSNR计算公式好像有点问题
    print("当算法n=%d时的PSNR值"%(n),tool.get_PSNR(len(hix_secret_message),cover_img_pix,hide_img_pix))
def get_secret_message(secret_len,hide_img_address,n):
    secret_hix=[]

    hide_pix=tool.get_gray_pix(hide_img_address)
    lenth=int(secret_len/n)
    for i in range(lenth):
        hix_secret=hide_pix[i]%(2**n)
        secret_hix.append(hix_secret)
    print("提取出来的十六进制消息:",secret_hix)
    secret_bin=tool.hix_to_bin(secret_hix)
    print("恢复之后的二进制消息:",secret_bin)



