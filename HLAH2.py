# -*-codeing=utf-8-*-
# @Time:2022/6/99:14
# @Author:xyp
# @File:HLAH2.py
# @Software:PyCharm
import tool
from PIL import Image

def hide_message(cover_img_address,secret_message,output_address):
    print("开始嵌入过程......")
    cover_RLSB0_pix=[]
    LSB2=[]
    edge_flag=0

    edge_flag_zuhe=0
    #先保存每个点的三个图层的像素值
    cover_R = tool.get_RGB_pix(cover_img_address, 0)
    cover_G = tool.get_RGB_pix(cover_img_address, 1)
    cover_B = tool.get_RGB_pix(cover_img_address, 2)

    #获取最低位请0之后的R图层的值
    for i in range(len(cover_R)):
        cover_RLSB0_pix.append(cover_R[i]&254)
    #保存R图层LSB清0之后的效果图
    tool.pix_to_img("./img/img.png", cover_RLSB0_pix, "./img/cover_RLSB0.png")
    #用最低位清0之后的R图层进行边缘检测
    tool.edge_detect("./img/cover_RLSB0.png", "./img/edge_detect.png")
    print("边缘检测完成......")
    #获取边缘检测的像素值  方便后面进行判断是不是边缘点
    edge_detect_pix = tool.get_gray_pix("./img/edge_detect.png")
    # 如果是边缘像素 那么将2LSB的值保存下来
    for j in range(len(edge_detect_pix)):
        if edge_detect_pix[j]==255:
            w = cover_G[j] & 2
            h = cover_B[j] & 2
            if w == 2: w = 1
            if h == 2: h = 1
            LSB2.append(w) # 将2LSB的像素保存起来 先保存g图层 再保存b图层
            LSB2.append(h)
    LSB2_2=tool.pix_cover_to_hide(LSB2)
    #开始根据是否是边缘像素进行嵌入
    it = iter(range(len(secret_message)))
    for i in it:
        #####如果不是边缘像素 进行下面的嵌入
        if edge_detect_pix[edge_flag]==0:
            #在RGB三个图层上面进行LSB嵌入
            if (cover_R[edge_flag]&1)!=secret_message[i]:
                cover_R[edge_flag]=cover_R[edge_flag]^1
            if i>=len(secret_message)-1:break
            if (cover_G[edge_flag]&1)!=secret_message[i+1]:
                cover_G[edge_flag]=cover_G[edge_flag]^1
            if (i+1)>=len(secret_message)-1:break
            if (cover_B[edge_flag]&1)!=secret_message[i+2]:
                cover_B[edge_flag]=cover_B[edge_flag]^1
            if (i+2)>=len(secret_message)-1:break


            for j in range(2):#0 12 3 45 6 78 9
                next(it)
            edge_flag = edge_flag + 1

        #####如果是边缘像素 进行下面的嵌入
        else:
            #先在RGB三个图层上面进行LSB嵌入
            if (cover_R[edge_flag]&1)!=secret_message[i]:
                cover_R[edge_flag]=cover_R[edge_flag]^1
            if i>=len(secret_message)-1:break
            if (cover_G[edge_flag]&1)!=secret_message[i+1]:
                cover_G[edge_flag]=cover_G[edge_flag]^1
            if (i+1)>=len(secret_message)-1:break
            if (cover_B[edge_flag]&1)!=secret_message[i+2]:
                cover_B[edge_flag]=cover_B[edge_flag]^1
            if (i+2)>=len(secret_message)-1:break
            #再在GB两个图层的2LSB上面进行（3,1)汉明码嵌入
            #用数组pp来记录返回的汉明码返回的更改值
            pp=tool.hanming_31_code([LSB2[edge_2LSB_flag],LSB2[edge_2LSB_flag+1],LSB2[edge_2LSB_flag+2]],[secret_message[i+3],secret_message[i+4]])
            #将返回的值重新赋值给GB的2LSB
            LSB2_2[edge_2LSB_flag], LSB2_2[edge_2LSB_flag + 1], LSB2_2[edge_2LSB_flag + 2]=pp
            for j in range(4):
                next(it)
            edge_flag = edge_flag + 1
            edge_2LSB_flag=edge_2LSB_flag+3
    edge_22LSB_flag = 0
    ###进行像素的组合 如果是非边缘像素则像素即为cover_R cover_G cover_B里面的像素值 如果是边缘像素那么需要对2LSB的值进行更改
    for i in range(len(edge_detect_pix)):
        if edge_detect_pix[i]==255:
            w = cover_G[i] & 2
            h = cover_B[i] & 2
            if w == 2: w = 1
            if h == 2: h = 1
            if w!=LSB2_2[edge_22LSB_flag]:
                cover_G[i]=cover_G[i]^2
            if h!=LSB2_2[edge_22LSB_flag+1]:
                cover_B[i]=cover_B[i]^2
            edge_22LSB_flag=edge_22LSB_flag+2#

    ###保存修改完的图片
    wight,hight=tool.get_w_h(cover_img_address)
    img = Image.open(cover_img_address)
    pix_flag = 0
    for i in range(hight):
        for j in range(wight):
            img.putpixel((j, i), (cover_R[pix_flag], cover_G[pix_flag], cover_B[pix_flag]))
            pix_flag = pix_flag + 1
    img.save(output_address)
    print("嵌入完成......")
    # for i in range(10):
    #     print(cover_R[i],end=",")
    # print()
    # for i in range(10):
    #     print(cover_G[i],end=",")
    # print()
    # for i in range(10):
    #     print(cover_B[i],end=",")
    # print()

def get_secret_message(hide_img_address,secert_message_lenth):
    print("开始提取过程......")
    LSB2=[]
    LSB2_flag=0
    cover_RLSB0_pix=[]
    get_secret_message=[]
    edge_flag=0
    # 先保存每个点的三个图层的像素值
    cover_R = tool.get_RGB_pix(hide_img_address, 0)
    cover_G = tool.get_RGB_pix(hide_img_address, 1)
    cover_B = tool.get_RGB_pix(hide_img_address, 2)
    # 获取最低位请0之后的R图层的值
    for i in range(len(cover_R)):
        cover_RLSB0_pix.append(cover_R[i] & 254)
    # 保存R图层LSB清0之后的效果图
    tool.pix_to_img("./img/img.png", cover_RLSB0_pix, "./img/cover_RLSB0_extract.png")
    # 用最低位清0之后的R图层进行边缘检测
    tool.edge_detect("./img/cover_RLSB0_extract.png", "./img/edge_detect_extract.png")
    print("边缘检测完成......")
    #保存边缘检测之后的像素值
    edge_detect_pix = tool.get_gray_pix("./img/edge_detect.png")
    # 如果是边缘像素 那么将2LSB的值保存下来
    for j in range(len(edge_detect_pix)):
        if edge_detect_pix[j] == 255:
            w = cover_G[j] & 2
            h = cover_B[j] & 2
            if w == 2: w = 1
            if h == 2: h = 1
            LSB2.append(w)  # 将2LSB的像素保存起来 先保存g图层 再保存b图层
            LSB2.append(h)

    it = iter(range(secert_message_lenth))
    for i in it:
        #####如果不是边缘像素 进行下面的提取
        if edge_detect_pix[edge_flag] == 0:
            #获取RGB三个图层的LSB
            get_secret_message.append(cover_R[edge_flag]&1)
            if i >= secert_message_lenth- 1: break
            get_secret_message.append(cover_G[edge_flag] & 1)
            if (i+1) >= secert_message_lenth - 1: break
            get_secret_message.append(cover_B[edge_flag] & 1)
            if (i+2)>= secert_message_lenth - 1: break
            for j in range(2):  # 0 12 3 45 6 78 9
                next(it)
            edge_flag = edge_flag + 1
        #####如果是边缘像素 进行下面的提取
        else:
            #获取RGB三个图层的LSB
            get_secret_message.append(cover_R[edge_flag] & 1)
            if i >= secert_message_lenth - 1: break
            get_secret_message.append(cover_G[edge_flag] & 1)
            if (i + 1) >= secert_message_lenth - 1: break
            get_secret_message.append(cover_B[edge_flag] & 1)
            if (i + 2) >= secert_message_lenth - 1: break
            #再获取GB两个图层的2LSB
            dd=tool.get_hanming_31_code([LSB2[LSB2_flag],LSB2[LSB2_flag+1],LSB2[LSB2_flag+2]])
            get_secret_message.append(dd[0])
            get_secret_message.append(dd[1])
            for j in range(4):
                next(it)
            edge_flag = edge_flag + 1
            LSB2_flag=LSB2_flag+3
    print("提取完成......")
    return get_secret_message