# -*-codeing=utf-8-*-
# @Time:2023/1/1723:38
# @Author:xyp
# @File:Improvement_MED.py
# @Software:PyCharm
from matplotlib import pyplot as plt
import numpy as np
import tools
import Improvement_MED
import xlwt
import xlsxwriter
import random
# cover_pix=tools.pic_to_arry("../img/Lena.tiff")#获取图像的二维数组，数组为图像的长和宽
# cover_pix_2=tools.pic_to_arry("../img/Lena.tiff")#获取图像的二维数组，数组为图像的长和宽
# width,hight=tools.get_w_h("../img/Lena.tiff")



def bianli_pics(path):
    import os

    img_folder = path
    img_list = [os.path.join(nm) for nm in os.listdir(img_folder) if nm[-4:] in ['tiff','jpg', 'png', 'gif']]


    for i in img_list:
        path = os.path.join(path, i)
    return img_list


def traditon_Med(width,hight):#这个函数用来计算传统MED对于整个图像的预测误差
    e = []  # 用来存储传统MED检测器的预测误差
    for i in range(1,hight):
        for j in range(1,width):

            x=cover_pix[i][j]
            n=cover_pix[i-1][j]
            w=cover_pix[i][j-1]
            nw=cover_pix[i-1][j-1]
            if nw>=max(n,w):
                pre_x=min(n,w)
            elif nw<=max(n,w):
                pre_x=max(n,w)
            else:
                pre_x=n+w-nw
            e.append(x-pre_x)

    return e

# def tradition_and_adjacency_prediction(width,hight,block_size):#参数宽 高 分块的大小
#     block_len=int(width/block_size)
#     block_hig=int(hight/block_size)
#     flag_len=int(block_size/2)
#     flag_hig=int(block_size/2)#选取中间的像素点作为参考像素
#     for i in range(0,block_hig):#行
#         for j in range(0,block_len):#列   整体的效果就是块的话先按照行每次往下遍历
#             flag_pix=cover_pix[i*block_size+flag_len-1][j*block_size+flag_hig-1]#得到参考像素  i*block _size+flag_len得到的是参考像素的行，i*block_size+flag_hig得到的是参考像素的列
#             for x in range(j*block_size,j*block_size+block_size):#先进行参考像素行上面的预测误差计算
#                 if x<j*block_size+flag_hig-1:#先计算参考像素行上面在它左边的预测值
#                     e_pro_EMD.append(cover_pix[i*block_size+flag_len-1][x]-cover_pix[i*block_size+flag_len-1][x+1])
#                 elif x>j*block_size+flag_hig-1:
#                     e_pro_EMD.append(cover_pix[i * block_size + flag_len-1][x] - cover_pix[i * block_size + flag_len-1][x - 1])
#             for y in range(i*block_size,i*block_size+block_size):#先进行参考像素列上面的预测误差计算
#                 if y<j*block_size+flag_hig-1:#再进行参考像素列上面的预测
#                     e_pro_EMD.append(cover_pix[y][j*block_size+flag_hig-1]-cover_pix[y+1][j*block_size+flag_hig-1])
#                 elif y>j*block_size+flag_hig-1:
#                     e_pro_EMD.append(cover_pix[y][j * block_size + flag_hig - 1] - cover_pix[y - 1][j * block_size + flag_hig - 1])
#
#
#     return e_pro_EMD
#具体方法参考paper《High-Capacity Framework for Reversible Data Hiding in Encrypted Image Using Pixel Prediction and Entropy Encoding》
#New_MGEDP方法参考paper《基于多方向梯度边缘预测器快速边缘检测算法》
#方法来源于paper《基于多方向梯度边缘预测器快速边缘检测算法》

def New_MGEDP(width,hight):
    e_New_MGEDP = []
    for i in range(0, hight - 2):  # 行
        for j in range(0, width - 2):  # 列
            print("---------------------------------------------------")
            I=cover_pix[i][j]
            A=cover_pix[i][j+1]
            D=cover_pix[i][j+2]
            B=cover_pix[i+1][j]
            C=cover_pix[i+1][j+1]
            E=cover_pix[i+2][j]
            dh=abs(D-A)+abs(C-B)
            dv=abs(C-A)+abs(E-B)
            print("dh",dh,"dv",dv)
            if (dv-dh)>80:
                I_do=A
            elif (dv-dh)<(-80):
                I_do=B
            else:
                I_do=(3*(A+B)/2)+(C+D+E)/12
            e_New_MGEDP.append(I-I_do)
    return e_New_MGEDP


def tradition_and_adjacency_prediction_2(width,hight,block_size):#参数宽 高 分块的大小
    e_pro_EMD = []  # 用来存储改进EMD的预测误差
    block_len=int(width/block_size)
    block_hig=int(hight/block_size)
    flag_len=int(block_size/2)
    flag_hig=int(block_size/2)#选取中间的像素点作为参考像素
    for i in range(0,block_hig):#行
        for j in range(0,block_len):#列   整体的效果就是块的话先按照行每次往下遍历
            hang=i*block_size+flag_len-1
            lie=j*block_size+flag_hig-1
            for x in range(j*block_size,j*block_size+block_size):#先进行参考像素行上面的预测误差计算
                if x<lie:#先计算参考像素行上面在它左边的预测值
                    e_pro_EMD.append(cover_pix[hang][x]-cover_pix[hang][x+1])
                elif x>lie:
                    e_pro_EMD.append(cover_pix[hang][x] - cover_pix[hang][x - 1])
            for y in range(i*block_size,i*block_size+block_size):#先进行参考像素列上面的预测误差计算
                if y<hang:#再进列参考像素列上面的预测
                    e_pro_EMD.append(cover_pix[y][lie]-cover_pix[y+1][lie])
                elif y>hang:
                    e_pro_EMD.append(cover_pix[y][lie] - cover_pix[y - 1][lie])
            for a in range(i*block_size,i*block_size+block_size):#行
                for b in range(j*block_size,j*block_size+block_size):#列
                    if a<hang and b<lie:
                        e_pro_EMD.append(tools.MED(cover_pix[a+1][b+1],cover_pix[a+1][b],cover_pix[a][b+1],cover_pix[a][b]))
                    elif a>hang and b<lie:
                        e_pro_EMD.append(tools.MED(cover_pix[a-1][b+1],cover_pix[a-1][b],cover_pix[a][b+1],cover_pix[a][b]))
                    elif a<hang and b>lie:
                        e_pro_EMD.append(tools.MED(cover_pix[a+1][b-1],cover_pix[a+1][b],cover_pix[a][b-1],cover_pix[a][b]))
                    elif a>hang and b>lie:
                        e_pro_EMD.append(tools.MED(cover_pix[a-1][b-1],cover_pix[a-1][b],cover_pix[a][b-1],cover_pix[a][b]))
    return e_pro_EMD


#AGSP预测方法具体参考paper《Adaptive reversible data hiding based on block median preservation and modification of prediction errors》

def AGSP(width,hight):
    e_AGSP = []
    def AGSP_ger_predict_value(hang,lie,Dming):

        match Dming:
            case 'D1':
                Cming=cover_pix[hang][lie-1]
                return Cming
            case 'D2':
                Cming = cover_pix[hang-1][lie]
                return Cming
            case 'D3':
                Cming = cover_pix[hang-1][lie+1]
                return Cming
            case 'D4':
                Cming = cover_pix[hang-1 ][lie-1]
                return Cming

    block_len=int(width/4)
    block_hig=int(hight/3)
    for i in range(0,block_hig):#行遍历
        for j in range(0,block_len):#列遍历
            print("------------------------------------------------")
            #hang 和 lie 代表要进行预测像素在每个块里面的位置
            hang=i*3+2
            lie=j*4+2
            #下面记录每个特殊位置的像素
            NNW=cover_pix[i*3][j*4+1]
            NN = cover_pix[i * 3][j * 4 + 2]
            NNE = cover_pix[i * 3][j * 4 + 3]
            NWW=cover_pix[i*3+1][j*4]
            NW = cover_pix[i * 3 + 1][j * 4+1]
            N = cover_pix[i * 3 + 1][j * 4 + 2]
            NE = cover_pix[i * 3 + 1][j * 4 + 3]
            WW=cover_pix[i*3+2][j*4]
            W = cover_pix[i * 3 + 2][j * 4+1]
            print("NNW",NNW,"NN",NN,"NNE",NNE,"NWW",NWW,"NW",NW,"N",N,"NE",NE,"WW",WW,"W",W)
            D1=(2*abs(W-WW)+2*abs(N-NW)+2*abs(N-NE)+abs(NN-NNW)+abs(NN-NNE)+abs(NW-NWW))/10#水平 Horizontal
            D2=(2*abs(W-WW)+2*abs(N-NN)+abs(NE-NNE)+abs(WW-NWW)+abs(NW-NWW))/8#Vertical
            D3=(2*abs(W-N)+2*abs(N-NNE)+abs(WW-NW)+abs(NW-NN))/7#45Degree
            D4=(2*abs(W-NWW)+2*abs(N-NNW)+abs(NE-NN))/6
            print("D1",D1,"D2",D2,"D3",D3,"D4",D4)
            D={'D1':D1,'D2':D2,'D3':D3,'D4':D4}
            D=sorted(D.items(), key=lambda x: x[1])

            D_min=D[0][1]#取最小的值
            D_min2=D[1][1]#取倒数第二小的值
            print("D_min",D_min,"D_min2",D_min2)
            Cmin=AGSP_ger_predict_value(hang,lie,D[0][0])
            Cmin2 = AGSP_ger_predict_value(hang, lie, D[1][0])
            print("Cmin",Cmin,"Cmin2",Cmin2)
            if D_min==D2 and D_min2==D4:
                print("D2*NW+D4*N",D2*NW+D4*N,"D2+D4",D2+D4)
                px=int((D2*NW+D4*N)/(D2+D4))

            else:
                print("D_min*Cmin+D_min2*Cmin2",D_min*Cmin+D_min2*Cmin2,"D_min+D_min2",D_min+D_min2)
                px=int((D_min*Cmin+D_min2*Cmin2)/(D_min+D_min2))

            e_AGSP.append(int(cover_pix[hang][lie]-px))
    return e_AGSP


#复现论文《New predictor-based schemes for reversible data hiding》里面提到的GAP预测器

def GAP(width,hight):
   e_GAP = []
   for i in range(1,hight):
       for j in range(1,width):
           x=cover_pix[i][j]#原始像素
           if i==1 or j==1:
              w=ww=cover_pix[i][j-1]
              ne=nn=nne=n=cover_pix[i-1][j]
              nw=cover_pix[i-1][j-1]
           elif j==(width-1):
               w = cover_pix[i][j - 1]
               ww = cover_pix[i][j - 2]
               nw = cover_pix[i - 1][j - 1]
               n =nn=nne=ne= cover_pix[i - 1][j]

           else:
               w=cover_pix[i][j-1]
               ww=cover_pix[i][j-2]
               nw=cover_pix[i-1][j-1]
               n=cover_pix[i-1][j]
               nn=cover_pix[i-2][j]
               nne=cover_pix[i-2][j+1]
               ne=cover_pix[i-1][j+1]
           dh = abs(w - ww) + abs(n - nw) + abs(n - ne)
           dv = abs(w - nw) + abs(n - nn) + abs(ne - nne)
           d = dv - dh
           y = (w + n) / 2 + (ne - nw) / 4
           if d > 80:
               px = w
           elif d < -80:
               px = n
           elif d > 32 and d <= 80:
               px = (y + w) / 2
           elif d >= -80 and d < -32:
               px = (y + n) / 2
           elif d > 8 and d <= 32:
               px = (3 * y + w) / 4
           elif d >= -32 and d < -8:
               px = (3 * y + n) / 4
           elif d >= -8 and d <= 8:
               px = y
           e_GAP.append(x-int(px) )
   return e_GAP

#来自paper《New predictor-based schemes for reversible data hiding》

def GAP_1_or_2_or_3(width,hight,mode):
    e_GAP_1_or_2 = []
    for i in range(1, hight):
        for j in range(1, width):
            x = cover_pix[i][j]  # 原始像素
            if i == 1 or j == 1:
                w = ww = cover_pix[i][j - 1]
                ne = nn = nne = n = cover_pix[i - 1][j]
                nw = cover_pix[i - 1][j - 1]
            elif j == (width - 1):
                w = cover_pix[i][j - 1]
                ww = cover_pix[i][j - 2]
                nw = cover_pix[i - 1][j - 1]
                n = nn = nne = ne = cover_pix[i - 1][j]

            else:
                w = cover_pix[i][j - 1]
                ww = cover_pix[i][j - 2]
                nw = cover_pix[i - 1][j - 1]
                n = cover_pix[i - 1][j]
                nn = cover_pix[i - 2][j]
                nne = cover_pix[i - 2][j + 1]
                ne = cover_pix[i - 1][j + 1]
            dh = abs(w - ww) + abs(n - nw) + abs(n - ne)
            dv = abs(w - nw) + abs(n - nn) + abs(ne - nne)
            d = dv - dh
            if mode==1:
                if d>80:
                    alpha=1
                    beta=0
                elif d>32 and d<=80:
                    alpha = 0.75
                    beta = 0.125
                elif d>8 and d<=32:
                    alpha = 0.625
                    beta = 0.1875
                elif d>=(-8) and d<=8:
                    alpha = 0.5
                    beta = 0.25
                elif d>=(-32) and d<(-8):
                    alpha = 0.375
                    beta = 0.1875
                elif d>=(-80) and d<(-32):
                    alpha = 0.25
                    beta = 0.125
                elif d<(-80):
                    alpha = 0
                    beta = 0
            elif mode==2:
                if d>40:
                    alpha=1
                    beta=0
                elif d>16 and d<=40:
                    alpha = 0.75
                    beta = 0.125
                elif d>4 and d<=16:
                    alpha = 0.625
                    beta = 0.1875
                elif d>=(-4) and d<=4:
                    alpha = 0.5
                    beta = 0.25
                elif d>=(-16) and d<(-4):
                    alpha = 0.375
                    beta = 0.1875
                elif d>=(-40) and d<(-16):
                    alpha = 0.25
                    beta = 0.125
                elif d<(-40):
                    alpha = 0
                    beta = 0
            elif mode==3:
                if d>88:
                    alpha=1
                    beta=0
                elif d>40 and d<=88:
                    alpha = 0.875
                    beta = 0.0625
                elif d>16 and d<=40:
                    alpha = 0.75
                    beta = 0.125
                elif d>4 and d<=16:
                    alpha=0.625
                    beta=0.1875
                elif d>=(-4) and d<=4:
                    alpha = 0.5
                    beta = 0.25
                elif d>=(-16) and d<(-4):
                    alpha = 0.375
                    beta = 0.1875
                elif d>=(-40) and d<(-16):
                    alpha = 0.25
                    beta = 0.125
                elif d<(-40) and d>=(-88):
                    alpha = 0.125
                    beta = 0.0625
                elif d<(-88):
                    alpha=0
                    beta=0
            pre_x=alpha*w+(1-alpha)*n+beta*(ne-nw)
            e_GAP_1_or_2.append(x-int(pre_x))
    return e_GAP_1_or_2

def GAP_DARC(width,hight):
    e_GAP_DARC = []
    for i in range(1, hight):
        for j in range(1, width):
            x = cover_pix[i][j]  # 原始像素
            if i == 1 or j == 1:
                w = ww = cover_pix[i][j - 1]
                ne = nn = nne = n = cover_pix[i - 1][j]
                nw = cover_pix[i - 1][j - 1]
            elif j == (width - 1):
                w = cover_pix[i][j - 1]
                ww = cover_pix[i][j - 2]
                nw = cover_pix[i - 1][j - 1]
                n = nn = nne = ne = cover_pix[i - 1][j]

            else:
                w = cover_pix[i][j - 1]
                ww = cover_pix[i][j - 2]
                nw = cover_pix[i - 1][j - 1]
                n = cover_pix[i - 1][j]
                nn = cover_pix[i - 2][j]
                nne = cover_pix[i - 2][j + 1]
                ne = cover_pix[i - 1][j + 1]
            dh = abs(w - ww) + abs(n - nw) + abs(n - ne)
            dv = abs(w - nw) + abs(n - nn) + abs(ne - nne)
            if dh+dv==0:
                continue
            alpha=dv/(dh+dv)
            # beta=min(alpha,(1-alpha))
            beta=min(alpha,1-alpha)
            pre_x=alpha*w+(1-alpha)*n+beta*(ne-nw)
            e_GAP_DARC.append(x-int(pre_x))
    return e_GAP_DARC


from PIL import Image
if __name__=="__main__":

#--------------------------------------------------------------
    # img_base=bianli_pics("../img")
    # for i in range(0,len(img_base)):
    #     min_bin = -3
    #     max_bin = 2
    #     cover_pix = tools.pic_to_arry("../img/"+img_base[i])  # 获取图像的二维数组，数组为图像的长和宽
    #     cover_pix_2 = tools.pic_to_arry("../img/"+img_base[i])  # 获取图像的二维数组，数组为图像的长和宽
    #     width, hight = tools.get_w_h("../img/"+img_base[i])
    #
    #
    #     print("--------------图片"+img_base[i]+"-------------------------")
    #     #传统EMD
    #     e_tra=traditon_Med(width,hight)
    #     e_tra_num=0
    #     for a in range(0,len(e_tra)):
    #         if e_tra[a]>=min_bin and e_tra[a]<=max_bin:
    #             e_tra_num=e_tra_num+1
    #     print("MED  -3~2:",e_tra_num)
    #
    #     e_tra_p=Precision_gradient_2("../img/"+img_base[i])
    #     e_tra_num=0
    #     for a in range(0,len(e_tra_p)):
    #
    #         if e_tra_p[a]>=min_bin and e_tra_p[a]<=max_bin:
    #             e_tra_num=e_tra_num+1
    #     print("改进  -3~2:",e_tra_num)
        # #改进MED
        # bloke_size=64
        # e_pro_EMD = tradition_and_adjacency_prediction_2(width, hight, bloke_size)
        # e_pro_EMD_num=0
        # for i in range(0,len(e_pro_EMD)):
        #     if e_pro_EMD[i]>=min_bin and e_pro_EMD[i]<=max_bin:
        #         e_pro_EMD_num=e_pro_EMD_num+1
        # print("使用块大小为"+str(bloke_size)+"的改进MED预测器得到6个预测误差的数量",e_pro_EMD_num)
        # #GAP
        # e_GAP_num=0
        # e_GAP=GAP(width,hight)
        # for i in range(0,len(e_GAP)):
        #     if e_GAP[i]>=min_bin and e_GAP[i]<=max_bin:
        #         e_GAP_num=e_GAP_num+1
        # print("使用GAP得到6个预测误差的数量",e_GAP_num)
        #
        #
        # for j in range(0,3):
        #     e_GAP_1=GAP_1_or_2_or_3(width,hight,j+1)
        #     e_GAP_1_num=0
        #     for i in range(0,len(e_GAP_1)):
        #         if e_GAP_1[i]>=min_bin and e_GAP_1[i]<=max_bin:
        #             e_GAP_1_num=e_GAP_1_num+1
        #     print("使用GAP"+str(j+1)+"得到6个预测误差的数量",e_GAP_1_num)
        #
        # e_GAP_DARC_num = 0
        # e_GAP_DARC = GAP_DARC(width, hight)
        # for i in range(0, len(e_GAP_DARC)):
        #     if e_GAP[i] >= -3 and e_GAP[i] <= 2:
        #         e_GAP_DARC_num = e_GAP_DARC_num + 1
        # print("使用GAP_DARC得到6个预测误差的数量", e_GAP_DARC_num)
        #
        # e_Pre_gra_num=0
        # e_pre_gra=Precision_gradient(width,hight)
        # for i in range(0, len(e_pre_gra)):
        #     if e_pre_gra[i] >= -3 and e_pre_gra[i] <= 2:
        #         e_Pre_gra_num = e_Pre_gra_num + 1
        # print("使用Pre_gra得到6个预测误差的数量", e_Pre_gra_num)


#-----------------------------------------------------------------------------
    min_bin =-3
    max_bin = 2
    # cover_pix = tools.pic_to_arry("../img/Original/lena.tiff")  # 获取图像的二维数组，数组为图像的长和宽
    # cover_pix_2 = tools.pic_to_arry("../img/Original/lena.tiff")  # 获取图像的二维数组，数组为图像的长和宽
    # width, hight = tools.get_w_h("../img/Original/lena.tiff")
    #
    cover_pix = tools.pic_to_arry("../img/man.tiff")  # 获取图像的二维数组，数组为图像的长和宽
    cover_pix_2 = tools.pic_to_arry("../img/man.tiff")  # 获取图像的二维数组，数组为图像的长和宽
    width, hight = tools.get_w_h("../img/man.tiff")


    # 传统EMD
    e_tra = traditon_Med(width, hight)
    e_tra_num = 0
    for i in range(0, len(e_tra)):
        if e_tra[i] >= min_bin and e_tra[i] <= max_bin:
            e_tra_num = e_tra_num + 1
    print("使用传统MED得到6个预测误差的数量", e_tra_num)
    # 改进MED
    bloke_size = 64
    e_pro_EMD = tradition_and_adjacency_prediction_2(width, hight, bloke_size)
    e_pro_EMD_num = 0
    for i in range(0, len(e_pro_EMD)):
        if e_pro_EMD[i] >= min_bin and e_pro_EMD[i] <= max_bin:
            e_pro_EMD_num = e_pro_EMD_num + 1
    print("使用块大小为" + str(bloke_size) + "的改进MED预测器得到6个预测误差的数量", e_pro_EMD_num)
    # GAP
    e_GAP_num = 0
    e_GAP = GAP(width, hight)
    for i in range(0, len(e_GAP)):
        if e_GAP[i] >= min_bin and e_GAP[i] <= max_bin:
            e_GAP_num = e_GAP_num + 1
    print("使用GAP得到6个预测误差的数量", e_GAP_num)

    for j in range(0, 3):
        e_GAP_1 = GAP_1_or_2_or_3(width, hight, j + 1)
        e_GAP_1_num = 0
        for i in range(0, len(e_GAP_1)):
            if e_GAP_1[i] >= min_bin and e_GAP_1[i] <= max_bin:
                e_GAP_1_num = e_GAP_1_num + 1
        print("使用GAP" + str(j + 1) + "得到6个预测误差的数量", e_GAP_1_num)

    e_GAP_DARC_num = 0
    e_GAP_DARC = GAP_DARC(width, hight)
    for i in range(0, len(e_GAP_DARC)):
        if e_GAP[i] >= -3 and e_GAP[i] <= 2:
            e_GAP_DARC_num = e_GAP_DARC_num + 1
    print("使用GAP_DARC得到6个预测误差的数量", e_GAP_DARC_num)

    e_Pre_gra_num = 0
    e_pre_gra = Precision_gradient(width, hight)
    for i in range(0, len(e_pre_gra)):
        if e_pre_gra[i] >= -3 and e_pre_gra[i] <= 2:
            e_Pre_gra_num = e_Pre_gra_num + 1
    print("使用Pre_gra得到6个预测误差的数量", e_Pre_gra_num)













