import math
import numpy as np
from PIL import Image
import random
import cv2 as cv
def get_w_h(img):
    img=Image.open(img)
    width=img.width
    hight=img.height
    return width,hight

def get_gray_pix(img):
    pix=[]
    width, hight = get_w_h(img)
    img=Image.open(img).convert("L")
    for i in range(hight):
        for j in range(width):
            pix.append(img.getpixel((j,i)))
    return pix

def rgb_to_gray(img,lujing):#传入彩色图片，保存的路径值
    img=Image.open(img).convert("L")
    img.save(lujing)


def pix_to_img(img,pix,lujing):
    width,hight=get_w_h(img)
    img=Image.open("./img/img.png").convert("L")
    a=0
    for i in range(hight):
        for j in range(width):
            img.putpixel((j,i),pix[a])
            a=a+1
    img.save(lujing)

def generate_random_number(a,b,num):
    random_number=[]
    for i in range(num):
        random_number.append(random.randint(a, b))
    return random_number

def pix_cover_to_hide(cover_pix):
    hide_img_pix=[]
    for i in range(len(cover_pix)):
        hide_img_pix.append(cover_pix[i])
    return hide_img_pix

def bin_to_hix(data):#2进制转16进制，4位2进制转1位16进制
    lenth=len(data)
    hix=[]
    for i in range(int(lenth/4)):
        hix_num=data[i*4]*8+data[i*4+1]*4+data[i*4+2]*2+data[i*4+3]
        hix.append(hix_num)
    return hix
def hix_to_bin(data):#16进制转换成2进制，1位16进制转换成4位2进制
    lenth=len(data)
    bin=[]
    for i in range(lenth):
        x=data[lenth-1-i]
        while(x!=0):

            r=x%2
            x=x//2
            bin=[r]+bin
            if x==0:
                if len(bin)!=i*4+4:
                    for j in range((i*4+4)-len(bin)):
                        bin=[0]+bin

    return bin

def get_PSNR(lenth,cover_pix,hide_pix):#lenth是需要计算的像素长度
    sum=0
    for i in range(lenth):
        sum=(cover_pix[i]-hide_pix[i])**2+sum
    MSE=sum/lenth
    PSNR=10*(math.log(((255**2)/MSE),10))

    return PSNR

#此代码为（3,1）汉明码的嵌入代码，传入覆盖的像素位，密码二进制消息，都用数组形式
def hanming_31_code(pix_ploat,secert_message):
    for i in range(int(len(pix_ploat)/3)):
        H=np.array([[0,1,1],
                    [1,0,1]])#检验矩阵
        cover_ploat=np.array([  #载体位的1或0组成的矩阵
            [pix_ploat[i*3]],
            [pix_ploat[i*3+1]],
            [pix_ploat[i*3+2]]
        ])
        x=(H@cover_ploat)%2#获得一个二行一列的矩阵 来与秘密矩阵进行相加操作
        secert=np.array([
            [secert_message[i*2]],
            [secert_message[i*2+1]]
        ])
        train=(secert+x)%2
        addrass=train[0][0]*2+train[1][0]
        if addrass==1:pix_ploat[i*3]=pix_ploat[i*3]^1
        elif addrass==2:pix_ploat[i*3+1]=pix_ploat[i*3+1]^1
        elif addrass==3:pix_ploat[i*3+2]=pix_ploat[i*3+2]^1
    return pix_ploat

def get_hanming_31_code(polat):
    get_secert=[]
    H = np.array([[0, 1, 1],
                  [1, 0, 1]])  # 检验矩阵
    for i in range(int(len(polat)/3)):
        m=np.array([
            [polat[i*3]],
            [polat[i*3+1]],
            [polat[i*3+2]]
        ])
        secrt=(H@m)%2

        get_secert=get_secert+[secrt[0][0]]+[secrt[1][0]]
    return get_secert

#边缘检测的代码
def edge_detect(image,save_lujing):
    def smooth(image, sigma=1.4, length=5):

        k = length // 2
        gaussian = np.zeros([length, length])
        for i in range(length):
            for j in range(length):
                gaussian[i, j] = np.exp(-((i - k) ** 2 + (j - k) ** 2) / (2 * sigma ** 2))
        gaussian /= 2 * np.pi * sigma ** 2
        # Batch Normalization
        gaussian = gaussian / np.sum(gaussian)

        # Use Gaussian Filter
        W, H = image.shape
        new_image = np.zeros([W - k * 2, H - k * 2])

        for i in range(W - 2 * k):
            for j in range(H - 2 * k):
                # 卷积运算
                new_image[i, j] = np.sum(image[i:i + length, j:j + length] * gaussian)

        new_image = np.uint8(new_image)
        return new_image

    def get_gradient_and_direction(image):

        Gx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
        Gy = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])

        W, H = image.shape
        gradients = np.zeros([W - 2, H - 2])
        direction = np.zeros([W - 2, H - 2])

        for i in range(W - 2):
            for j in range(H - 2):
                dx = np.sum(image[i:i + 3, j:j + 3] * Gx)
                dy = np.sum(image[i:i + 3, j:j + 3] * Gy)
                gradients[i, j] = np.sqrt(dx ** 2 + dy ** 2)
                if dx == 0:
                    direction[i, j] = np.pi / 2
                else:
                    direction[i, j] = np.arctan(dy / dx)

        gradients = np.uint8(gradients)
        return gradients, direction

    def NMS(gradients, direction):

        W, H = gradients.shape
        nms = np.copy(gradients[1:-1, 1:-1])

        for i in range(1, W - 1):
            for j in range(1, H - 1):
                theta = direction[i, j]
                weight = np.tan(theta)
                if theta > np.pi / 4:
                    d1 = [0, 1]
                    d2 = [1, 1]
                    weight = 1 / weight
                elif theta >= 0:
                    d1 = [1, 0]
                    d2 = [1, 1]
                elif theta >= - np.pi / 4:
                    d1 = [1, 0]
                    d2 = [1, -1]
                    weight *= -1
                else:
                    d1 = [0, -1]
                    d2 = [1, -1]
                    weight = -1 / weight

                g1 = gradients[i + d1[0], j + d1[1]]
                g2 = gradients[i + d2[0], j + d2[1]]
                g3 = gradients[i - d1[0], j - d1[1]]
                g4 = gradients[i - d2[0], j - d2[1]]

                grade_count1 = g1 * weight + g2 * (1 - weight)
                grade_count2 = g3 * weight + g4 * (1 - weight)

                if grade_count1 > gradients[i, j] or grade_count2 > gradients[i, j]:
                    nms[i - 1, j - 1] = 0
        return nms

    def double_threshold(nms, threshold1, threshold2):
        """ Double Threshold
        Use two thresholds to compute the edge.

        Args:
            nms: the input image
            threshold1: the low threshold
            threshold2: the high threshold

        Returns:
            The binary image.
        """
        visited = np.zeros_like(nms)
        output_image = nms.copy()
        W, H = output_image.shape

        def dfs(i, j):
            if i >= W or i < 0 or j >= H or j < 0 or visited[i, j] == 1:
                return
            visited[i, j] = 1
            if output_image[i, j] > threshold1:
                output_image[i, j] = 255
                dfs(i - 1, j - 1)
                dfs(i - 1, j)
                dfs(i - 1, j + 1)
                dfs(i, j - 1)
                dfs(i, j + 1)
                dfs(i + 1, j - 1)
                dfs(i + 1, j)
                dfs(i + 1, j + 1)
            else:
                output_image[i, j] = 0

        for w in range(W):
            for h in range(H):
                if visited[w, h] == 1:
                    continue
                if output_image[w, h] >= threshold2:
                    dfs(w, h)
                elif output_image[w, h] <= threshold1:
                    output_image[w, h] = 0
                    visited[w, h] = 1

        for w in range(W):
            for h in range(H):
                if visited[w, h] == 0:
                    output_image[w, h] = 0
        return output_image
    image = cv.imread(image, 0)
    smoothed_image = smooth(image)
    gradients, direction = get_gradient_and_direction(smoothed_image)
    nms = NMS(gradients, direction)
    output_image = double_threshold(nms, 40, 100)
    cv.imwrite(save_lujing,output_image)

def get_RGB_pix(img,tuceng):#tuceng 012分别为RGB  返回该图层的像素值
#getpixe函数获取出来的像素是rgb的顺序
    pix = []
    width, hight = get_w_h(img)
    img = Image.open(img)

    for i in range(hight):
        for j in range(width):
            pix.append(img.getpixel((j,i))[tuceng])
    return pix


