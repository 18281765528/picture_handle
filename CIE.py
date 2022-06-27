# -*-codeing=utf-8-*-
# @Time:2022/5/1510:50
# @Author:xyp
# @File:CIE.py
# @Software:PyCharm
import tool
get_message=[]
hide_pic_pix=[]
codebook={0:[0,0],1:[1,0],2:[2,0],3:[3,0],4:[-2,1],5:[-1,1],6:[0,1],7:[1,1],8:[2,1],9:[3,1],10:[-2,2],11:[-1,2],12:[0,2],13:[1,2],
          14:[2,2],15:[3,2],16:[-3,-2],17:[-2,-2],18:[-1,-2],19:[0,-2],20:[1,-2],
          21:[-2,-2],22:[-3,-1],23:[-2,-1],24:[-1,-1],25:[0,-1],26:[1,-1],27:[2,-1],28:[-3,0],29:[-2,0],30:[-1,0]}
def hide_massege(secrt_massege,img):
    tool.rgb_to_gray(img,"./img/gary.png")#把图片转换成灰度图片
    cover_pix=tool.get_gray_pix(img)#获取灰度图像的像素值

    global hide_pix
    hide_pix=cover_pix
    for i in range(len(secrt_massege)):
        f=(cover_pix[i*2]*1+cover_pix[i*2+1]*6)%31
        if secrt_massege[i]>=f:
            s=secrt_massege[i]-f
        elif secrt_massege[i]<f:
            w=secrt_massege[i]-f
            if w<0:w=-w
            s=31-w
        hide_pix[i*2]=cover_pix[i*2]+codebook[s][0]
        hide_pix[i*2+1]=cover_pix[i*2+1]+codebook[s][1]
        if hide_pix[i*2]>255:hide_pix[i*2]=hide_pix[i*2]-31
        elif hide_pix[i*2+1]>255:hide_pix[i*2+1]=hide_pix[i*2+1]-31
        elif hide_pix[i*2]<0:hide_pix[i*2]=hide_pix[i*2]+31
        elif hide_pix[i*2+1]<0:hide_pix[i*2+1]=hide_pix[i*2+1]+31
    tool.pix_to_img("./img/img.png",hide_pix,"./img/hide.png")


def get_massege(img):
    hide_pic_pix=tool.get_gray_pix(img)
    for i in range(len(secrt_massege)):
        f=(hide_pic_pix[i*2]*1+hide_pic_pix[i*2+1]*6)%31
        get_message.append(f)

#本代码采用CIE嵌入算法，其中n=2，x=3
if __name__=="__main__":
    secrt_massege=[5,6,2,6,6,8,13,22,122]
    print("需要嵌入的10进制消息为:",secrt_massege)
    hide_massege(secrt_massege,"./img/img.png")
    get_massege("./img/hide.png")
    print("提取出来的10进制消息：",get_message)