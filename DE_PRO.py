import tools
import math
import numpy as np
def Depro_embedding(OriginalPixBlock,n):
    '''
    :param OriginalPixBlock: 超级像素块
    :param n: 秘密消息，为一个数组
    :return: 更改之后的超级像素块
    '''

    OriginalPixBlock=np.array(OriginalPixBlock).reshape(2,2)

    X=OriginalPixBlock[0][0]+OriginalPixBlock[1][1]
    Y=OriginalPixBlock[0][1]+OriginalPixBlock[1][0]
    h=X-Y
    l=math.floor((X+Y)/2)
    h_next=2**len(n)*h+tools.bin_to_ten(n)
    X_next=l+math.floor((h_next+1)/2)
    Y_next=l-math.floor(h_next/2)
    X_gain=X_next-X
    Y_gain=Y_next-Y
    #对x和y的增加量进行拆分
    x00=math.floor(X_gain/2)
    OriginalPixBlock[0][0] =OriginalPixBlock[0][0]+x00
    x11=math.ceil(X_gain/2)
    OriginalPixBlock[1][1]=OriginalPixBlock[1][1]+x11
    y01 = math.floor(Y_gain / 2)
    OriginalPixBlock[0][1]=OriginalPixBlock[0][1]+y01
    y10 = math.ceil(Y_gain / 2)
    OriginalPixBlock[1][0]=OriginalPixBlock[1][0]+y10

    return OriginalPixBlock

Original_img="./img/Original/lena.tiff"
Original_imgs="./img/Original/lena32de.tiff"
Original_pix=tools.pic_to_arry(Original_img)
for i in range(0,512,2):
    for j in range(0,512,2):

        Pixblock=[Original_pix[i][j],Original_pix[i][j+1],Original_pix[i+1][j],Original_pix[i+1][j+1]]

        Pixblock_next=Depro_embedding(Pixblock,tools.generate_random_number(0,1,4))
        Original_pix[i][j]=Pixblock_next[0][0]
        Original_pix[i][j + 1]=Pixblock_next[0][1]
        Original_pix[i + 1][j]=Pixblock_next[1][0]
        Original_pix[i + 1][j + 1]=Pixblock_next[1][1]
        if Pixblock_next[0][0]>255 or Pixblock_next[0][0]<0 or Pixblock_next[0][1]>255 or Pixblock_next[0][1]<0 or Pixblock_next[1][0]>255 or Pixblock_next[1][0]<0 or Pixblock_next[1][1]>255 or Pixblock_next[1][1]<0 :
            print(Pixblock_next)
#tools.pixarry_to_img(Original_img,Original_pix,Original_imgs)
