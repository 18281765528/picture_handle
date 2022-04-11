
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
import cv2 as cv

from skimage import io,data,color
import cv2

flag=0
def pic_analysis(address):#获取图像信息的函数
    img = io.imread(address)
    width=img.shape[0]#宽度
    hight=img.shape[1]#高度
    tuceng=img.shape[2]#通道
    size=img.size#图像大小
    return width,hight,tuceng,size

def pic_train(address,star_width,star_hight,end_width,end_hight,R,G,B): #更改像素值的函数
    img = io.imread(address)
    for x in range(star_width,end_width):
        for y in range(star_hight,end_hight):
            img[x,y,2]=R
            img[x,y,1]=G
            img[x,y,0]=B

    if flag==2:
        io.imsave("2.jpg",img)
    elif flag==1:
        io.imsave("3.jpg", img)



class picture(QWidget): #Pyqt的信号和槽

    def __init__(self):
        super(picture, self).__init__()
        self.resize(900, 800)
        self.setWindowTitle("图片像素处理")
        #、、、、、、、、、、、、、、、、、、、、、、、、、、
        self.label1= QLabel(self)
        self.label1.setText("   处理前图片")
        self.label1.setFixedSize(300, 300)
        self.label1.move(60, 30)

        self.label1.setStyleSheet("QLabel{background:white;}"
                                 "QLabel{color:rgb(300,300,300,120);font-size:30px;font-weight:bold;font-family:宋体;}"
                                 )
        #、、、、、、、、、、、、、、、、、、、、、、、
        self.label2 = QLabel(self)
        self.label2.setText("   处理后图片")
        self.label2.setFixedSize(300, 300)
        self.label2.move(500, 30)

        self.label2.setStyleSheet("QLabel{background:white;}"
                                  "QLabel{color:rgb(300,300,300,120);font-size:30px;font-weight:bold;font-family:宋体;}"
                                  )
        #、、、、、、、、、、、、、、、、、、、、、、、、、、

        btn = QPushButton(self)
        btn.setText("打开图片")
        btn.move(370, 500)
        btn.clicked.connect(self.openimage)
        #、、、、、、处理前的图片信息、、、、、、、、、、、、、、、、、、、、、
        pic_pro_inf = QLabel("图片信息", self)  # 创建标签对象
        pic_pro_inf.setGeometry(5, 350, 80, 30)
        #、、、处理之后的图片信息、、、、、、、、
        pic_pro_inf = QLabel("图片信息", self)  # 创建标签对象
        pic_pro_inf.setGeometry(445, 350, 80, 30)
        #、、、、、、、、、、、、、、、、、、、、、、、、、、、、、
        self.pic_inf_pro=QTextBrowser(self)
        self.pic_inf_pro.setGeometry(70, 350, 250, 100)
        #、、、、、、、、、、、、、、、、、、、、、、、、
        self.pic_inf_then = QTextBrowser(self)
        self.pic_inf_then.setGeometry(510, 350, 250, 100)

        #、、、、、、star、、、、、、、、、、、、、、、
        self.star_piex= QLineEdit(self)  # 设置一个编辑框 属于my_win 这个框
        self.star_piex.setGeometry(330, 540, 200, 30)  # 设置编辑框的位置
        star_inf = QLabel("开始坐标", self)  # 创建标签对象
        self.star_piex.setPlaceholderText("格式如:22,34")
        star_inf.setGeometry(250, 540, 80, 30)

        #、、、、、、、、end、、、、、、、
        self.end_piex = QLineEdit(self)  # 设置一个编辑框 属于my_win 这个框
        self.end_piex.setGeometry(330, 580, 200, 30)  # 设置编辑框的位置
        self.end_piex.setPlaceholderText("格式如:22,34")
        end_inf = QLabel("结束坐标", self)  # 创建标签对象
        end_inf.setGeometry(250, 580, 80, 30)
        #、、、、、、、、、R、、、、、、、
        self.R_piex = QLineEdit(self)  # 设置一个编辑框 属于my_win 这个框
        self.R_piex.setGeometry(330, 620, 200, 30)  # 设置编辑框的位置
        self.R_piex.setPlaceholderText("大小0~255")
        R_inf = QLabel("B层的值", self)  # 创建标签对象
        R_inf.setGeometry(250, 620, 80, 30)
        #、、、、、、、G、、、、、、、、、
        self.G_piex = QLineEdit(self)  # 设置一个编辑框 属于my_win 这个框
        self.G_piex.setGeometry(330, 660, 200, 30)  # 设置编辑框的位置
        self.G_piex.setPlaceholderText("大小0~255")
        G_inf = QLabel("G层的值", self)  # 创建标签对象
        G_inf.setGeometry(250, 660, 80, 30)
        #、、、、、、、B、、、、、、、、
        self.B_piex = QLineEdit(self)  # 设置一个编辑框 属于my_win 这个框
        self.B_piex.setGeometry(330, 700, 200, 30)  # 设置编辑框的位置
        self.B_piex.setPlaceholderText("大小0~255")
        B_inf = QLabel("R层的值", self)  # 创建标签对象
        B_inf.setGeometry(250, 700, 80, 30)
        #、、、、、处理按钮
        btn1 = QPushButton(self)
        btn1.setText("开始处理")
        btn1.move(370, 740)
        btn1.clicked.connect(self.pic_prograss)
        #、、、、、、prograss、、、、、

        self.prograss= QLabel("", self)  # 创建标签对象
        self.prograss.setGeometry(480, 740, 200, 30)
        #、、、、pic_take、、、、
        btn3 = QPushButton(self)
        btn3.setText("打开摄像头")
        btn3.move(370, 465)
        btn3.clicked.connect(self.pic_take)


    def openimage(self):#打开文件对话框
        global imgName
        global flag
        flag=2
        imgName, imgType = QFileDialog.getOpenFileName(self, "上传图片", "", "*.jpg;;*.png;;All Files(*)")
        jpg = QtGui.QPixmap(imgName).scaled(self.label1.width(), self.label1.height())

        width,hight,tuceng,size=pic_analysis(imgName)

        self.pic_inf_pro.setText("宽度："+str(width)+"\n"+"高度：" + str(hight) + "\n"+"图层：" + str(tuceng) + "\n"+"大小：" + str(size) + "\n")
        self.label1.setPixmap(jpg)



    def pic_prograss(self):#获取输入框的值 并且调用像素更改函数
        self.prograss.setText("处理中")

        star_width=int(self.star_piex.text().split(',')[0])
        star_hight=int(self.star_piex.text().split(',')[1])
        end_width=int(self.end_piex.text().split(',')[0])
        end_hight=int(self.end_piex.text().split(',')[1])
        R=int(self.R_piex.text())
        G=int(self.G_piex.text())
        B=int(self.B_piex.text())
        pic_train(imgName,star_width,star_hight,end_width,end_hight,R,G,B)
        self.prograss.setText("处理完成")
        if flag==2:
            jpg = QtGui.QPixmap("E:/postgruaduat_demo/pixel_change/ui/2.jpg").scaled(self.label2.width(), self.label2.height())
            self.label2.setPixmap(jpg)
            width, hight, tuceng, size = pic_analysis("E:/postgruaduat_demo/pixel_change/ui/2.jpg")
        elif flag==1:
            jpg = QtGui.QPixmap("E:/postgruaduat_demo/pixel_change/ui/3.jpg").scaled(self.label2.width(),self.label2.height())
            self.label2.setPixmap(jpg)
            width, hight, tuceng, size = pic_analysis("E:/postgruaduat_demo/pixel_change/ui/3.jpg")

        self.pic_inf_then.setText(
            "宽度：" + str(width) + "\n" + "高度：" + str(hight) + "\n" + "图层：" + str(tuceng) + "\n" + "大小：" + str(
                size) + "\n")


    def pic_take(self):#摄像头采集和人脸识别
        # 摄像头
        global flag
        flag=1
        global imgName
        imgName="E:/postgruaduat_demo/pixel_change/ui/take.jpg"
        cap = cv2.VideoCapture(0)

        num = 1
        while (cap.isOpened()):  # 检测是否在开启状态
            ret_flag, Vshow = cap.read()  # 得到每帧图像
            cv2.imshow("Capture_Test", Vshow)  # 显示图像
            k = cv2.waitKey(1) & 0xFF  # 按键判断
            if k == ord('s'):  # 保存
                cv2.imwrite(imgName, Vshow)
            elif k == ord(' '):  # 退出
                break
        # 释放摄像头
        cap.release()
        # 释放内存
        cv2.destroyAllWindows()

        img = cv.imread(imgName)
        gary = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        face_detect = cv.CascadeClassifier('E:/opencv/sources/data/haarcascades/haarcascade_frontalface_alt2.xml')
        face = face_detect.detectMultiScale(gary, 1.01, 5, 0, (100, 100), (300, 300))
        global x,y,w,h


        for x, y, w, h in face:
            cv.rectangle(img, (x, y), (x + w, y + h), color=(0, 0, 255), thickness=2)
        io.imsave(imgName,img)

        jpg = QtGui.QPixmap(imgName).scaled(self.label1.width(), self.label1.height())
        width, hight, tuceng, size = pic_analysis("E:/postgruaduat_demo/pixel_change/ui/take.jpg")
        self.pic_inf_pro.setText(
            "宽度：" + str(width) + "\n" + "高度：" + str(hight) + "\n" + "图层：" + str(tuceng) + "\n" + "大小：" + str(
                size) + "\n"+"人脸框图坐标：" + "("+str(y) +","+str(x)+")"+ "("+str(y+h) +","+str(x+w)+")" )
        self.label1.setPixmap(jpg)
        print(x, y, w, h)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    my = picture()
    my.show()
    sys.exit(app.exec_())