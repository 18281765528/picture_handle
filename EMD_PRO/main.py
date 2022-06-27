from PIL import Image
import numpy as np
five=[]
cover_pix=[]
cover_hide_pix=[]

get_secrt_message=[]
get_secrt=[]
secrt_five=[]
get_secrt_message_two=[]
x=[-1,-2,0,1,2]
def five_to_two(get_secrt_message_five):
    lenth=int(len(get_secrt_message_five)/2)
    for i in range(lenth):
        message=int(str(get_secrt_message_five[i*2])+str(get_secrt_message_five[i*2+1]))
        message=int(message/10)*5+message%10
        aa=bin(message)[2:]
        lentehs=len(aa)
        if lentehs==2:
            aa="0"+"0"+aa
        elif lentehs==3:
            aa="0"+aa
        elif lentehs==1:
            aa="0"+"0"+"0"+aa

        for j in aa:
            get_secrt_message_two.append(int(j))
def ten_to_five(a):#将十进制转换成5进制，并且用字符串的形式打印出来
    shang=[]
    yu=[]
    shangshu=1
    while(shangshu!=0):
        shangshu=int(a/5)
        yushu=a%5
        a=shangshu
        yu.append(yushu)
    lenth=len(yu)
    st = ""
    for i in range(lenth):
        aa = str(yu[lenth - i - 1])
        st = st + aa
    if len(st)==1:
        st="0"+st
    return st
def two_to_five(secrt_message):
    lenth=len(secrt_message)
    yu=int(lenth/4)
    for i in range(yu):
        dd=str(secrt_message[i*4])+str(secrt_message[i*4+1])+str(secrt_message[i*4+2])+str(secrt_message[i*4+3])
        dd=int(dd,2)#得到十进制的数,将每4位二进制分成一组，然后转换成10进制
        dd=ten_to_five(dd)#将十进制转换成5进制

        for j in dd:
            j=int(j)
            five.append(j)  # 将转换后的5进制放在一个列表当中，方便后面使用
def secrt_message_hide(img,secrt_message):
    global cover_hide_pix
    img=Image.open(img).convert("L")
    img.save("./img/img_gray.png")
    img_hide=img.copy()
    width=img.width
    hight=img.height
    for i in range(hight):
        for j in range(width):
            pix=img.getpixel((j,i))
            cover_pix.append(pix)
    for lenth in range(len(cover_pix)):
        cover_hide_pix.append(cover_pix[lenth])
    print("更改前的像素值:",end="")
    for flag in range(len(five)):
        print(cover_pix[flag],end=",")
   #消息嵌入的核心部分
    for flags in range(len(five)):
        for xx in x:
            f=(cover_pix[flags]+xx)%5
            if f==five[flags]:
                cover_hide_pix[flags]=cover_pix[flags]+xx
    print()
    print("更改后的像素值:", end="")
    for flag in range(len(five)):
        print(cover_hide_pix[flag],end=",")
        get_secrt_message.append(cover_hide_pix[flag]%5)
    a=0
    #对更改后的像素进行更改到灰度图像当中
    for i in range(hight):
        for j in range(width):
            img_hide.putpixel((j,i),cover_hide_pix[a])
            a=a+1
    img_hide.save("./img/img_hide.png")
def secrt_message_get(img):
    img=Image.open(img).convert("L")
    lenth=len(five)
    width=img.width
    hight=img.height
    for i in range(hight):
        for j in range(width):
            pix=img.getpixel((j,i))
            get_secrt.append(pix)
    for b in range(lenth):
        secrt_five.append(get_secrt[b]%5)
    print()
    print("提取出来的5进制消息：",secrt_five)
    five_to_two(secrt_five)
    print("转换之后的2进制消息：",get_secrt_message_two)
#采用峰值信噪比(PSNR)对算法进行评价，如果PSNR>30,那么表示人类视觉系统是难以察觉的
def evaluate(cover_pix,cover_hide_pix):
    img=Image.open("./img/img.png")
    width=img.width
    hight=img.height
    sum=0
    for i in range(width*hight):
        sum=sum+(cover_pix[i]-cover_hide_pix[i])*(cover_pix[i]-cover_hide_pix[i])
    print("-----------------------------评价隐藏算法-------------------------------------")
    MSE=sum/(width*hight)
    print("均方误差为：",MSE)
    PSNR=(10*int(np.log10(255*255)))/MSE
    print("PSNR值：",PSNR)

if __name__ == '__main__':
    print("本代码n取2，将2进制的秘密消息以5进制的形式进行嵌入")
    secrt_message = [1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1,1,0,1,1]
    two_to_five(secrt_message)
    print("需要嵌入的2进制消息：",secrt_message)
    print("转换之后的5进制秘密消息：",five)
    secrt_message_hide("./img/img.png",five)
    secrt_message_get("./img/img_hide.png")
    if secrt_message==get_secrt_message_two:
        print("------嵌入消息与提取消息相同，提取成功--------")
    else:print("------嵌入消息与提取消息不相同，提取失败--------")
    evaluate(cover_pix,cover_hide_pix)





