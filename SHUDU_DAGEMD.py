import Generat_SHUDU
import tool


def look_shudu_falg(shudu99,falg_number):#次函数用来根据数独获取基数的位置下标

    shudu=[]
    flag=[]
    ww=[]

    for k in range(9):
        for i in range(9):
            for j in range(9):
                if k==0 and i <=2 and j<=2:
                    ww.append(shudu99[i][j])
                    if len(ww)==9:
                        shudu.append(ww)
                        ww=[]
                elif k==1 and i<=2 and j>=3 and j<=5:
                    ww.append(shudu99[i][j])
                    if len(ww)==9:
                        shudu.append(ww)
                        ww=[]
                elif k==2 and i<=2 and j>=6 and j<=8:
                    ww.append(shudu99[i][j])
                    if len(ww)==9:
                        shudu.append(ww)
                        ww=[]
                elif k==3 and i>=3 and i<=5 and j<=2:
                    ww.append(shudu99[i][j])
                    if len(ww)==9:
                        shudu.append(ww)
                        ww=[]
                elif k==4 and i>=3 and i<=5 and j>=3 and j<=5:
                    ww.append(shudu99[i][j])
                    if len(ww)==9:
                        shudu.append(ww)
                        ww=[]
                elif k==5 and i>=3 and i<=5 and j>=6 and j<=8:
                    ww.append(shudu99[i][j])
                    if len(ww)==9:
                        shudu.append(ww)
                        ww=[]
                elif k==6 and i>=6 and i<=8 and j<=2:
                    ww.append(shudu99[i][j])
                    if len(ww)==9:
                        shudu.append(ww)
                        ww=[]
                elif k==7 and i>=6 and i<=8 and j>=3 and j<=5:
                    ww.append(shudu99[i][j])
                    if len(ww)==9:
                        shudu.append(ww)
                        ww=[]
                elif k==8 and i>=6 and i<=8 and j>=6 and j<=8:
                    ww.append(shudu99[i][j])
                    if len(ww)==9:
                        shudu.append(ww)
                        ww=[]

    for i in range(9):
        for j in range(9):
            if shudu[i][j]==falg_number:
                flag.append(j)
    return flag
def hide_message(cover_img_address,secret_message,output_address,shudu99,shudu_flag_number):
    cover_pix=tool.get_gray_pix(cover_img_address)#获取覆盖像素
    hide_message_quan=tool.pix_cover_to_hide(cover_pix)
    for i in range(int(len(secret_message)/12)):#以12个秘密消息为一组进行嵌入,秘密消息长度除以12就是循环次数
        secert_message_falg=0
        group_pix9=[]#存储每次嵌入的9个覆盖像素
        group_pix_div_4=[]#存储像素除以4之后的值
        group_pix_rem_4=[]#获得RR矩阵，存储的像素每个除以4取余数
        jishu_falg_number=[]#根据数独产生的基数位置
        group_pix9_train=[]#做了防止下溢的像素
        group_pix_hide_message=[]#隐藏了秘密消息的像素
        d=[]#获取除4之后的每个数与基数直接的差值
        for j in range(9):#获取每组嵌入的9个覆盖像素
            group_pix9.append(cover_pix[i*9+j])
            group_pix_div_4.append(int(group_pix9[j]/4))
            group_pix_rem_4.append(int(group_pix9[j]%4))
        group_pix9_train=tool.pix_cover_to_hide(group_pix9)
        print(group_pix_rem_4)
        jishu_falg_number=look_shudu_falg(shudu99,shudu_flag_number)
        print("得到每个3*3数独当中%d的位置下标"%(shudu_flag_number),jishu_falg_number)
        for k in range(9):
            d.append(abs(group_pix_div_4[k]-group_pix_div_4[jishu_falg_number[i%9]]))
        for s in range(9):
            if d[s]!=0:
                if group_pix_rem_4[s]==0:
                    group_pix_rem_4[s]=group_pix_rem_4[s]+1
                elif group_pix_rem_4[s]==3:
                    group_pix_rem_4[s] = group_pix_rem_4[s] -1
        for q in range(9):  # d为0的地方覆盖像素不做更改，d不为0的地方做更改
            if d[q]!=0:
                group_pix9_train[q]=group_pix_div_4[q]*4+group_pix_rem_4[q]
        group_pix_hide_message=tool.pix_cover_to_hide(group_pix9)
        #下面进行嵌入操作
        d_no_zero_pix=[]
        d_no_zero_pix_bao=[]
        use_GEMD_secert=[]
        for t in range(9):#首先在d=0的地方进行2LSB嵌入
            if d[t]==0:
                group_pix_hide_message[t]=LSB2(secret_message[secert_message_falg],secret_message[secert_message_falg+1],group_pix9_train[t])
                secert_message_falg=secert_message_falg+2
        for z in range(9):#再在d不为0的地方进行GAEMD嵌入
            if d[z]!=0:
                d_no_zero_pix.append(group_pix9_train[z])
        for s in range(secert_message_falg,12):
            use_GEMD_secert.append(secret_message[s])
        for zz in range(len(use_GEMD_secert)-1):
            d_no_zero_pix_bao.append(d_no_zero_pix[zz])
        GEMD_get_pix=GEMD(use_GEMD_secert,d_no_zero_pix_bao)
        falg_gemd=0
        for aa in range(9):
            if d[aa]!=0:
                group_pix_hide_message[aa]=GEMD_get_pix[falg_gemd]
                falg_gemd=falg_gemd+1
                if falg_gemd>len(GEMD_get_pix)-1:
                    break
        for j in range(9):#获取每组嵌入的9个覆盖像素
            hide_message_quan[i*9+j]=group_pix_hide_message[j]
        tool.pix_to_img(cover_img_address,hide_message_quan,output_address)
        print("需要嵌入的秘密消息",secret_message)
        print("更改之前的像素",group_pix9)
        print("更改之后的像素",group_pix9_train)
        print("d矩阵",d)
        print("嵌入了秘密消息的像素",group_pix_hide_message)
        print("嵌入完成")

def get_secret_message(hide_img_address,secert_message_lenth,shudu99,shudu_flag_number):
    hide_img_pix=tool.get_gray_pix(hide_img_address)
    get_secert_message=[]
    for i in range(int(secert_message_lenth / 12)):  # 以12个秘密消息为一组进行嵌入,秘密消息长度除以12就是循环次数
        group_pix9=[]
        group_pix_div_4=[]
        group_pix_rem_4=[]
        d=[]
        for j in range(9):#获取每组嵌入的9个覆盖像素
            group_pix9.append(hide_img_pix[i*9+j])
            group_pix_div_4.append(int(group_pix9[j]/4))
            group_pix_rem_4.append(int(group_pix9[j]%4))
        jishu_falg_number = look_shudu_falg(shudu99, shudu_flag_number)
        for k in range(9):
            d.append(abs(group_pix_div_4[k]-group_pix_div_4[jishu_falg_number[i%9]]))
        #下面开始提取过程
        Use_LSB_get=[]
        #下面是2LSB的提取过程
        SS=0
        for aa in range(9):
            if d[aa]==0:
                SS=SS+1#标记有SS个像素进行了2LSB嵌入
                Use_LSB_get=Use_LSB_get+LSB2_get(group_pix9[aa])
        #下面的GEMD的提取过程
        d_no_zero_pix=[]
        Use_DA_GEMD_get=[]
        flag=[]
        for z in range(9):#再在d不为0的地方进行GAEMD提取
            if d[z]!=0:
                d_no_zero_pix.append(group_pix9[z])
        qq=secert_message_lenth-SS*2#表示有qq个秘密消息进行了GEMD嵌入,那么有qq-1个像素进行了GMED嵌入
        for q in range(qq-1):
            flag.append(d_no_zero_pix[q])
        num=GEMD_get(flag)#获取嵌入的十进制消息
        Use_DA_GEMD_get=ten_to_two(num,qq)
        get_secert_message=Use_LSB_get+Use_DA_GEMD_get
        return get_secert_message



# def hide_message(cover_img_address,secret_message,output_address,shudu99,shudu_flag_number):
#     lenth_secert_message=len(secret_message)
#     i=0
#     while(lenth_secert_message>=1):
#         cover_pix = tool.get_gray_pix(cover_img_address)  # 获取覆盖像素
#         group_pix9=[]#存储每次嵌入的9个覆盖像素
#
#         group_pix_div_4=[]#存储像素除以4之后的值
#         group_pix_rem_4=[]#获得RR矩阵，存储的像素每个除以4取余数
#         jishu_falg_number=[]#根据数独产生的基数位置
#         d=[]#获取除4之后的每个数与基数直接的差值
#         for j in range(9):#获取每组嵌入的9个覆盖像素
#             group_pix9.append(cover_pix[i*9+j])
#             group_pix_div_4.append(int(group_pix9[j]/4))
#             group_pix_rem_4.append(int(group_pix9[j]%4))
#         print("原来的像素值",group_pix9)
#         group_pix9_train = tool.pix_cover_to_hide(group_pix9)
#         print("更改之前成r矩阵",group_pix_rem_4)
#         jishu_falg_number=look_shudu_falg(shudu99,shudu_flag_number)
#         print("得到每个3*3数独当中%d的位置下标"%(shudu_flag_number),jishu_falg_number)
#         for k in range(9):
#             d.append(abs(group_pix_div_4[k]-group_pix_div_4[jishu_falg_number[i%9]]))
#         for s in range(9):
#             if d[s]!=0:
#                 if group_pix_rem_4[s]==0:
#                     group_pix_rem_4[s]=group_pix_rem_4[s]+1
#                 elif group_pix_rem_4[s]==3:
#                     group_pix_rem_4[s] = group_pix_rem_4[s] -1
#         for q in range(9):#d为0的地方覆盖像素不做更改，d不为0的地方做更改
#             if d[q]!=0:
#                 group_pix9_train[q]=group_pix_div_4[q]*4+group_pix_rem_4[q]
#         ss = 0
#         dd = 0
#         for e in range(9):
#
#             if d[e]==0:
#                 dd=dd+1
#             elif d[e]!=0:
#                 ss=ss+1
#         lenth_secert_message=lenth_secert_message-(dd*2)-(ss+1)
#
#         #下面开始嵌入操作
#         for r in range(9):#先将d=0的部分用2LSB进行嵌入
#             Use_LSB = []
#             if d[r]==0:
#
#
#
#         # print("一次嵌入之后的长度",lenth_secert_message)
#         # print("更改之后的r矩阵",group_pix_rem_4)
#         # print("d矩阵",d)
#         # print("更改之后的像素值",group_pix9_train)
def LSB2(secert1,secert2,cover_pix):#将secert1嵌入cover_pix1LSB，将secert2嵌入cover_pix2LSB当中
    tt=0
    if (cover_pix&1)!=secert1:
        cover_pix=cover_pix^1
    if cover_pix & 2!=0:
        tt=1
    if tt!=secert2:
        cover_pix=cover_pix^2
    return cover_pix
def LSB2_get(hide_pix):
    hide=[]
    hide.append(hide_pix&1)
    if (hide_pix&2)!=0:
        hide.append(1)
    else:hide.append(0)
    return hide
def GEMD(secert,cover_pix):
    lenth=len(cover_pix)
    number=0
    s=0
    for i in range(lenth):
        number=number+cover_pix[i]*((2**(i+1)-1))
    t=number%(2**(lenth+1))
    for i in range(len(secert)):
        s=s+secert[i]*(2**(len(secert)-i-1))
    D=(s-t)%(2**(lenth+1))
    if D==2**(lenth):
        cover_pix[lenth-1]=cover_pix[lenth-1]+1
        cover_pix[0]=cover_pix[0]+1
    elif D<2**(lenth):
        b=ten_to_two(D,lenth+1)
        for w in range(lenth):
            if (b[len(b)-w-1]==0 and b[len(b)-w-2]==0) or (b[len(b)-w-1]==1 and b[len(b)-w-2]==1):
                cover_pix[w]=cover_pix[w]
            elif b[len(b)-w-1]==1 and b[len(b)-w-2]==0:
                cover_pix[w] = cover_pix[w]+1
            elif b[len(b)-w-1]==0 and b[len(b)-w-2]==1:
                cover_pix[w] = cover_pix[w]-1
    else:
        D=2**(lenth+1)-D
        b=ten_to_two(D,lenth+1)
        for w in range(lenth):
            if (b[len(b)-w-1]==0 and b[len(b)-w-2]==0) or (b[len(b)-w-1]==1 and b[len(b)-w-2]==1):
                cover_pix[w]=cover_pix[w]
            elif b[len(b)-w-1]==1 and b[len(b)-w-2]==0:
                cover_pix[w] = cover_pix[w]-1
            elif b[len(b)-w-1]==0 and b[len(b)-w-2]==1:
                cover_pix[w] = cover_pix[w]+1
    return cover_pix
def GEMD_get(hide_pix):
    lenth = len(hide_pix)
    number = 0
    for i in range(lenth):
        number = number + hide_pix[i] * ((2 ** (i + 1) - 1))
    t = number % (2 ** (lenth + 1))
    return t
def ten_to_two(num,lenth):
    ss=bin(num)
    gg=[]
    for i in range(2,len(ss)):
        gg.append(int(ss[i]))
    for j in range(lenth-len(gg)):
        gg=[0]+gg
    return gg

# print(GEMD([0,1,0,1],[152,157,158]))
# print(GEMD_get(GEMD([0,1,0,1],[152,157,158])))
# print(ten_to_two(GEMD_get(GEMD([0,1,0,1],[152,157,158])),4))
# print(GEMD_get([226,225,230,228,229]))
# print(ten_to_two(38,6))
