# -*-codeing=utf-8-*-
# @Time:2022/7/1018:54
# @Author:xyp
# @File:HCD.py
# @Software:PyCharm
#本代码复现于论文《High capacity data hiding scheme based on multi-bit encoding function》
#代码中k任意取值，n表示n个像素为一组
import tool
def hide_message(cover_img_address,secret_message,output_address,k,n):
    cover_pix=tool.get_gray_pix(cover_img_address)

    hide_pix=tool.pix_cover_to_hide(cover_pix)

    for i in range(int(len(secret_message)/(n*k+1))):
        ba=[]

        two=[]
        a=[cover_pix[i*4],cover_pix[i*4+1],cover_pix[i*4+2],cover_pix[i*4+3]]
        t=f(a,4,3)
        for j in range(n*k+1):
            two.append(secret_message[i*13+j])
        s=two_to_ten(two)

        D=(s-t)%(2**(n*k+1))
        if D==0:
            hide_pix[i*4]=cover_pix[i*4]
            hide_pix[i*4+1]=cover_pix[i*4+1]
            hide_pix[i * 4 + 2] = cover_pix[i * 4 + 2]
            hide_pix[i * 4 + 3] = cover_pix[i * 4 + 3]
        elif D==2**(n*k):
            hide_pix[i * 4 + 3] = cover_pix[i * 4 + 3]+(2**k-1)
            hide_pix[i * 4] = cover_pix[i * 4]+1
        elif D<2**(n*k):
            ba=ten_to_egiht(D)#将十进制的D转换成八进制 d3 d2 d1 d0
            for j in range(n):
                if j ==(n-1):
                    hide_pix[i * 4 + 3] = hide_pix[i * 4 + 3]+ba[0]
                    hide_pix[i * 4 + 2] = hide_pix[i * 4 + 2]-ba[0]
                elif j==(n-2):
                    hide_pix[i * 4 + 2] = hide_pix[i * 4 + 2]+ba[1]
                    hide_pix[i * 4 + 1] = hide_pix[i * 4 + 1]-ba[1]
                elif j==(n-3):
                    hide_pix[i * 4 + 1] = hide_pix[i * 4 + 1]+ba[2]
                    hide_pix[i * 4] = hide_pix[i * 4]-ba[2]
                elif j==(n-4):
                    hide_pix[i * 4] = cover_pix[i * 4]+ba[3]
        elif D>2**(n*k):
            D=2**(n*k+1)-D
            ba = ten_to_egiht(D)  # 将十进制的D转换成八进制 d3 d2 d1 d0

            for j in range(n):
                if j ==(n-1):
                    hide_pix[i * 4 + 3] = hide_pix[i * 4 + 3]-ba[0]
                    hide_pix[i * 4 + 2] = hide_pix[i * 4 + 2]+ba[0]

                elif j==(n-2):
                    hide_pix[i * 4 + 2] = hide_pix[i * 4 + 2]-ba[1]
                    hide_pix[i * 4 + 1] = hide_pix[i * 4 + 1]+ba[1]

                elif j==(n-3):

                    hide_pix[i * 4 + 1] = hide_pix[i * 4 + 1]-ba[2]
                    hide_pix[i * 4] = hide_pix[i * 4]+ba[2]

                elif j==(n-4):
                    hide_pix[i * 4] = hide_pix[i * 4]-ba[3]
    tool.pix_to_img(cover_img_address,hide_pix,output_address)

def get_secret_message(hide_img_address,secert_message_lenth,n,k):
    pixs=[]
    fs=[]
    ten=[]
    bins=[]
    pix=tool.get_gray_pix(hide_img_address)
    for i in range(int(secert_message_lenth/(n*k+1))):
        for j in range(n):
            pixs.append(pix[i*n+j])#将n个像素设置为一组
        fs.append(f(pixs,n,k))
    for i in range(len(fs)):
        bins=bins+ten_to_two(fs[i],n*k+1)
    return bins

def ten_to_two(number,lens):
    two=[]
    b=bin(number)
    for i in range(2,len(b)):
        two.append(int(b[i]))
    if len(two)<lens:
        flag=lens-len(two)
        for j in range(flag):
            two=[0]+two
    return two

def f(x,n,k):
    f=0
    for i in range(len(x)):
        if i==0:
            f=f+x[i]
            c=1
        else:
            c=(2**k)*c+1
            f=f+c*x[i]

    f=f%(2**(n*k+1))
    return f

def two_to_ten(arr):
    d=0
    for i in range(len(arr)):
        d=d+arr[i]*(2**(len(arr)-i-1))
    return d
def ten_to_egiht(number):
    ba=[]
    b = oct(number)  # 将十进制的D转换成八进制
    for j in range(2, len(b)):
        ba.append(int(b[j]))
    if len(ba) == 1:
        ba = [0] + [0] + [0] + ba
    elif len(ba) == 2:
        ba = [0] + [0] + ba
    elif len(ba) == 3:
        ba = [0] + ba
    return ba