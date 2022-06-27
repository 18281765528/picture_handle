# -*-codeing=utf-8-*-
# @Time:2022/6/199:56
# @Author:xyp
# @File:MOPNA.py
# @Software:PyCharm

#本代码是MOPNA的复现
import tool
import math


def hide_message(cover_img_address,secret_message,output_address,k):

    cover_pix=tool.get_gray_pix(cover_img_address)
    hide_pix=tool.pix_cover_to_hide(cover_pix)
    C=[3,11]

    for i in range(int(len(secret_message)/(2*k+1))):
        d = 0
        CPV_MAX=0
        # f=f_function(C,cover_pix[i*2],cover_pix[i*2+1],k)
        for j in range(2*k+1):
            d=d+(secret_message[i*(2*k+1)+j]*(2**((2*k+1-j-1))))
    # CPV_valude_max=0
    # duan=[0,0]
    # for x0 in range(-255,256):
    #     for x1 in range(-255,256):
    #         flag=f_function(C,cover_pix[i*2]+x0,cover_pix[i*2+1]+x1,4)
    #         if flag==d:
    #             # hide_pix[i*2]=hide_pix[i*2]+x0
    #             # hide_pix[i*2+1]=hide_pix[i*2+1]+x1
    #             duan[0]=cover_pix[i*2]+x0
    #             duan[1]=cover_pix[i*2+1]+x1
    #             CPV_valude=CPV(cover_pix[i*2],cover_pix[i*2+1],duan[0],duan[1])
    #             if CPV_valude>CPV_valude_max:
    #                 CPV_valude_max=CPV_valude
    #                 hide_pix[i * 2]=duan[0]
    #                 hide_pix[i * 2 + 1]=duan[1]
    # for i in range(5):
    #     print(cover_pix[i],end=",")
    # print()
    # for i in range(5):
    #     print(hide_pix[i], end=",")
        for x0 in range(-255,256):
            for x1 in range(-255,256):
                f=f_function(C,cover_pix[i*2]+x0,cover_pix[i*2+1]+x1,k)
                if f==d:
                    CPV_value=CPV(cover_pix[i*2]+x0,cover_pix[i*2+1]+x1,cover_pix[i*2],cover_pix[i*2+1])
                    if CPV_value>=CPV_MAX:
                        CPV_MAX=CPV_value
                        hide_pix[i * 2]= hide_pix[i * 2]+x0
                        hide_pix[i*2+1]=hide_pix[i*2+1]+x1
    for i in range(5):
        print(cover_pix[i],end=",")
    print()
    for i in range(5):
        print(hide_pix[i],end=",")






def get_secret_message(hide_img_address,secert_message_lenth):
    pass

def f_function(C,num1,num2,k):
    f=(C[0]*num1+C[1]*num2)%(2**(2*k+1))
    return f

def CPV(G_1,G_2,G_next_1,G_next_2):

    G_model=G_1**2+G_2**2
    G_G_next_model=(G_1-G_next_1)**2+(G_2-G_next_2)**2
    if G_model!=0 and G_G_next_model!=0:
        CPV_value=10*(math.log((G_model/G_G_next_model),10))
    if G_model==0 and G_G_next_model!=0:
        CPV_value = 10 * (math.log((255 / G_G_next_model), 10))
    if G_G_next_model==0:
        CPV_value=100
    return CPV_value




