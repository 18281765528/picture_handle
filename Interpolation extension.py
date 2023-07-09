from PIL import Image
import numpy as np
import math
import random
def bin_to_ten(bin_number):
    '''

    :param bin_number: 数组
    :return:
    '''
    ten_number=""
    for i in range(len(bin_number)):# 1111 0110
        ten_number=ten_number+str(bin_number[i])
    ten_number=int(ten_number,2)
    return ten_number
def encrypt_message(Origina_message,ke):#加密信息
    '''
    数据加密和解密都是这一个函数
    :param Origina_message: 原始信息,为二进制数组
    :param ke: 种子
    :return: 加密之后的图像
    '''
    rd = np.random.RandomState(ke)
    matrix = rd.randint(0, 2, (1, len(Origina_message)))
    encryption_message=[]
    for i in range(len(Origina_message)):
        encryption_message.append(Origina_message[i]^matrix[0][i])
    return encryption_message
def get_w_h(img):  # 获取图像的宽度和高度
    img = Image.open(img)
    width = img.width
    hight = img.height
    return width, hight
def get_gray_pix(img):
    pix=[]
    width, hight = get_w_h(img)
    img=Image.open(img).convert("L")
    for i in range(hight):
        for j in range(width):
            pix.append(img.getpixel((j,i)))
    return pix
def bin_to_ten(bin_number):
    '''

    :param bin_number: 数组
    :return:
    '''
    ten_number=""
    for i in range(len(bin_number)):# 1111 0110
        ten_number=ten_number+str(bin_number[i])
    ten_number=int(ten_number,2)
    return ten_number
def pixarry_to_img_2(img,width,hight,pix,lujing):
    img = Image.open(img).convert("L")
    img=img.resize((width,hight))

    for i in range(hight):
        for j in range(width):
            img.putpixel((j, i), int(pix[i][j]))

    img.save(lujing)
def generate_random_number(a,b,num):
    random_number=[]
    for i in range(num):
        random_number.append(random.randint(a, b))
    return random_number
def get_gray_pix(img):
    pix=[]
    width, hight = get_w_h(img)
    img=Image.open(img).convert("L")
    for i in range(hight):
        for j in range(width):
            pix.append(img.getpixel((j,i)))
    return pix
def ten_to_bin(number_ten,number_len):
    test_11=[]
    if number_len==0:
        return test_11
    number=[]
    number_bin=bin(number_ten)[2:]
    if len(number_bin)>number_len:
        print("cuowu")
    if len(number_bin)<number_len:
        for j in range(number_len-len(number_bin)):
            number_bin="0"+number_bin
    for i in range(len(number_bin)):
        number.append(int(number_bin[i],2))
    return number
def pic_to_arry(cover_pic_address):#将图像变成二维数组
    def get_gray_pix(img):#获取图像像素的一维数组
        pix = []
        width, hight = get_w_h(img)
        img = Image.open(img).convert("L")
        for i in range(hight):  # 行
            for j in range(width):  # 列
                pix.append(img.getpixel((j, i)))
        return pix

    width, hight = get_w_h(cover_pic_address)
    cover_pix = get_gray_pix(cover_pic_address)
    cover_pix = np.array(cover_pix)
    cover_pix = cover_pix.reshape(hight, width)
    return cover_pix
def Image_interpolation(first_label_encrypted_img, auxiliary, generate_address, Information_key):
    '''
    完成第二层辅助信息的嵌入
    :param first_label_encrypted_img: 第一次嵌入完之后的图像
    :param auxiliary: 全部需要嵌入的辅助信息
    :return: 完成辅助信息嵌入之后的图像，也就是接收方拿到的数据
    '''
    flag_2 = 0
    flag = 0
    test = 0

    secret_inf = []
    cover_pix = get_gray_pix(first_label_encrypted_img)

    second_image_interpolatic_pic = np.zeros((1024, 1024))  # 生成插值图像
    for i in range(1024):
        for j in range(1024):
            if i % 2 == 0 and j % 2 == 0:
                second_image_interpolatic_pic[i][j] = cover_pix[flag_2]
                flag_2 = flag_2 + 1

    for i in range(0, 1022, 2):
        for j in range(0, 1022, 2):
            second_image_interpolatic_pic[i][j + 1] = int(
                (second_image_interpolatic_pic[i][j] + second_image_interpolatic_pic[i][j + 2]) / 2)
            second_image_interpolatic_pic[i + 1][j] = int(
                (second_image_interpolatic_pic[i][j] + second_image_interpolatic_pic[i + 2][j]) / 2)
            second_image_interpolatic_pic[i + 1][j + 1] = int((second_image_interpolatic_pic[i][j] +
                                                               second_image_interpolatic_pic[i][j + 1] +
                                                               second_image_interpolatic_pic[i + 1][j]) / 3)
            if (second_image_interpolatic_pic[i][j + 1] - second_image_interpolatic_pic[i][j]) != 0 and second_image_interpolatic_pic[i][j + 1] != 255:
                Cp01_00 = math.log(abs(second_image_interpolatic_pic[i][j + 1] - second_image_interpolatic_pic[i][j]),2)  # 得到这个点的容量
                Cp01_255 = math.log((255 - second_image_interpolatic_pic[i][j + 1]), 2)
                Cp01 = int(min(Cp01_00, Cp01_255))

                if Cp01 != 0:  # 不等于0则进行秘密信息的嵌入
                    if flag + Cp01 <= 720125:
                        add_number =bin_to_ten(auxiliary[flag:flag + Cp01])
                        second_image_interpolatic_pic[i][j + 1] = second_image_interpolatic_pic[i][j + 1] + add_number
                        flag = flag + Cp01
                    else:
                        test = test + 1
                        inf = generate_random_number(0, 1, Cp01)
                        secret_inf.extend(inf)
                        inf =encrypt_message(inf, Information_key)
                        add_number = bin_to_ten(inf)
                        second_image_interpolatic_pic[i][j + 1] = second_image_interpolatic_pic[i][j + 1] + add_number

            if (second_image_interpolatic_pic[i + 1][j] - second_image_interpolatic_pic[i][j]) != 0 and second_image_interpolatic_pic[i + 1][j] != 255:
                Cp01_00 = math.log(abs(second_image_interpolatic_pic[i + 1][j] - second_image_interpolatic_pic[i][j]),2)  # 得到这个点的容量
                Cp01_255 = math.log((255 - second_image_interpolatic_pic[i + 1][j]), 2)
                Cp01 = int(min(Cp01_00, Cp01_255))

                if Cp01 != 0:  # 不等于0则进行秘密信息的嵌入
                    if flag + Cp01 <= 720125:
                        add_number = bin_to_ten(auxiliary[flag:flag + Cp01])
                        second_image_interpolatic_pic[i + 1][j] = second_image_interpolatic_pic[i + 1][j] + add_number
                        flag = flag + Cp01
                    else:
                        inf = generate_random_number(0, 1, Cp01)
                        secret_inf.extend(inf)
                        inf = encrypt_message(inf, Information_key)
                        add_number = bin_to_ten(inf)
                        second_image_interpolatic_pic[i + 1][j] = second_image_interpolatic_pic[i + 1][j] + add_number

            if (second_image_interpolatic_pic[i + 1][j + 1] - second_image_interpolatic_pic[i][j]) != 0 and second_image_interpolatic_pic[i + 1][j + 1] != 255:
                Cp01_00 = math.log(abs(second_image_interpolatic_pic[i + 1][j + 1] - second_image_interpolatic_pic[i][j]),2)  # 得到这个点的容量
                Cp01_255 = math.log((255 - second_image_interpolatic_pic[i + 1][j + 1]), 2)
                Cp01 = int(min(Cp01_00, Cp01_255))
                if Cp01 != 0:  # 不等于0则进行秘密信息的嵌入
                    if flag + Cp01 <= 720125:
                        add_number = bin_to_ten(auxiliary[flag:flag + Cp01])
                        second_image_interpolatic_pic[i + 1][j + 1] = second_image_interpolatic_pic[i + 1][j + 1] + add_number
                        flag = flag + Cp01
                    else:
                        inf = generate_random_number(0, 1, Cp01)
                        secret_inf.extend(inf)
                        inf = encrypt_message(inf, Information_key)
                        add_number = bin_to_ten(inf)
                        second_image_interpolatic_pic[i + 1][j + 1] = second_image_interpolatic_pic[i + 1][j + 1] + add_number

    pixarry_to_img_2(first_label_encrypted_img, 1024, 1024, second_image_interpolatic_pic, generate_address)
    return secret_inf
def Image_interpolation_extract(second_image_interpolatic, Information_key,De_second_image_interpolation_address):
    '''
    本函数对第二阶段的秘密信息和辅助信息进行提取
    :param second_image_interpolatic:
    :param Information_key:
    :return:
    '''

    cover_pix=[]
    flag=0

    second_image_interpolatic_pic=pic_to_arry(second_image_interpolatic)

    auxiliary=[]
    secret_inf=[]
    for i in range(1024):
        for j in range(1024):
            if i%2==0 and j%2==0:
                cover_pix.append(second_image_interpolatic_pic[i][j])

    cover_pix=np.array(cover_pix).reshape((512,512))

    pixarry_to_img_2(second_image_interpolatic,512,512,cover_pix,De_second_image_interpolation_address)
    for i in range(0,1022,2):
        for j in range(0,1022,2):
            second_image_interpolatic_pic01 = second_image_interpolatic_pic[i][j + 1] - \
                                              int((second_image_interpolatic_pic[i][j]+second_image_interpolatic_pic[i][j+2])/2)
            second_image_interpolatic_pic10 = second_image_interpolatic_pic[i + 1][j] - \
                                              int((second_image_interpolatic_pic[i][j] + second_image_interpolatic_pic[i+2][j ]) / 2)
            second_image_interpolatic_pic11 = second_image_interpolatic_pic[i + 1][j + 1] - \
                                              int((second_image_interpolatic_pic[i][j]+int((second_image_interpolatic_pic[i][j]+second_image_interpolatic_pic[i][j+2])/2)+int((second_image_interpolatic_pic[i][j] + second_image_interpolatic_pic[i+2][j ]) / 2))/3)
            second_image_interpolatic_pic[i][j+1]=int((second_image_interpolatic_pic[i][j]+second_image_interpolatic_pic[i][j+2])/2)
            second_image_interpolatic_pic[i+1][j] = int((second_image_interpolatic_pic[i][j] + second_image_interpolatic_pic[i+2][j ]) / 2)
            second_image_interpolatic_pic[i + 1][j+1]=int((second_image_interpolatic_pic[i][j]+second_image_interpolatic_pic[i][j+1]+second_image_interpolatic_pic[i+1][j])/3)
            if (second_image_interpolatic_pic[i][j + 1] - second_image_interpolatic_pic[i][j]) != 0 and second_image_interpolatic_pic[i][j + 1] != 255:
                Cp01_00 = math.log(abs(second_image_interpolatic_pic[i][j + 1] - second_image_interpolatic_pic[i][j]),2)  # 得到这个点的容量
                Cp01_255 = math.log((255 - second_image_interpolatic_pic[i][j + 1]), 2)
                Cp01 = int(min(Cp01_00, Cp01_255))

                if Cp01 != 0:  # 不等于0则进行秘密信息的嵌入
                    if flag + Cp01 <= 720125:
                        add_number = second_image_interpolatic_pic01
                        add_number=ten_to_bin(add_number,Cp01)
                        auxiliary.extend(add_number)

                        flag = flag + Cp01
                    else:
                        second_image_interpolatic_pic01=tools.ten_to_bin(second_image_interpolatic_pic01,Cp01)
                        second_image_interpolatic_pic01=encrypt_message(second_image_interpolatic_pic01,Information_key)
                        secret_inf.extend(second_image_interpolatic_pic01)
            if (second_image_interpolatic_pic[i + 1][j] - second_image_interpolatic_pic[i][j]) != 0 and second_image_interpolatic_pic[i + 1][j] != 255:
                Cp01_00 = math.log(abs(second_image_interpolatic_pic[i + 1][j] - second_image_interpolatic_pic[i][j]),2)  # 得到这个点的容量
                Cp01_255 = math.log((255 - second_image_interpolatic_pic[i + 1][j]), 2)
                Cp01 = int(min(Cp01_00, Cp01_255))

                if Cp01!=0:#不等于0则进行秘密信息的嵌入
                    if flag+Cp01<=720125:
                        add_number=second_image_interpolatic_pic10
                        add_number = ten_to_bin(add_number, Cp01)
                        auxiliary.extend(add_number)

                        flag=flag+Cp01
                    else:
                        second_image_interpolatic_pic10 = ten_to_bin(second_image_interpolatic_pic10, Cp01)
                        second_image_interpolatic_pic10 = encrypt_message(second_image_interpolatic_pic10, Information_key)
                        secret_inf.extend(second_image_interpolatic_pic10)

            if (second_image_interpolatic_pic[i+1][j+1]-second_image_interpolatic_pic[i][j])!=0 and second_image_interpolatic_pic[i+1][j+1]!=255:
                Cp01_00 = math.log(abs(second_image_interpolatic_pic[i+1][j+1] - second_image_interpolatic_pic[i][j]),2)  # 得到这个点的容量
                Cp01_255 = math.log((255 - second_image_interpolatic_pic[i+1][j+1]), 2)
                Cp01 = int(min(Cp01_00, Cp01_255))

                if Cp01!=0:#不等于0则进行秘密信息的嵌入
                    if flag+Cp01<=720125:
                        add_number=second_image_interpolatic_pic11
                        add_number =ten_to_bin(add_number, Cp01)
                        auxiliary.extend(add_number)

                        flag=flag+Cp01
                    else:
                        second_image_interpolatic_pic11 = ten_to_bin(second_image_interpolatic_pic11, Cp01)
                        second_image_interpolatic_pic11 = encrypt_message(second_image_interpolatic_pic11, Information_key)
                        secret_inf.extend(second_image_interpolatic_pic11)

    return auxiliary,secret_inf