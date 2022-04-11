import utime
from Maix import GPIO
from board import board_info
from fpioa_manager import fm

fm.register(18,fm.fpioa.GPIO0)
led_b = GPIO(GPIO.GPIO0,GPIO.OUT)
led_b.value(1)

import utime
from Maix import GPIO

from fpioa_manager import fm




import sensor, image, lcd, time
import KPU as kpu
import utime
from Maix import GPIO
from board import board_info
from fpioa_manager import fm

fm.register(board_info.BOOT_KEY, fm.fpioa.GPIOHS1)
key = GPIO(GPIO.GPIOHS1, GPIO.IN)

color_R = (255, 0, 0)
color_G = (0, 255, 0)
color_B = (0, 0, 255)


class_IDs = ['no_mask', 'mask']


def drawConfidenceText(image, rol, classid, value):
    text = ""
    _confidence = int(value * 100)

    if classid == 1:
        text = 'mask: ' + str(_confidence) + '%'
        color_text=color_G
        led_b.value(1)
    else:
        text = 'no_mask: ' + str(_confidence) + '%'
        color_text=color_R
        led_b.value(0)
    image.draw_string(50,50, text, color=color_text, scale=2.5)



lcd.init()
sensor.reset(dual_buff=True)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_hmirror(0)
sensor.run(1)


task=kpu.load("/sd/20210308_141935_25_mask_a5de6d151641163cbeef21b83eb3832a.smodel")


anchor = (0.1606, 0.3562, 0.4712, 0.9568, 0.9877, 1.9108, 1.8761, 3.5310, 3.4423, 5.6823)
_ = kpu.init_yolo2(task, 0.5, 0.3, 5, anchor)
img_lcd = image.Image()
flag=0

clock = time.clock()
while (True):
    lcd.rotation(1)
    if key.value() == 0: # 等待按键按下
        if flag==0:
            flag=1
        elif flag==1:
            flag=0

    elif flag==1:



        clock.tick()
        img = sensor.snapshot()
        code = kpu.run_yolo2(task, img)
        if code:
            totalRes = len(code)

            for item in code:
                confidence = float(item.value())
                itemROL = item.rect()
                classID = int(item.classid())

                if confidence < 0.52:
                    _ = img.draw_rectangle(itemROL, color=color_B, tickness=5)
                    continue

                if classID == 1 and confidence > 0.65:
                    _ = img.draw_rectangle(itemROL, color_G, tickness=5)
                    if totalRes == 1:
                        drawConfidenceText(img, (0, 0), 1, confidence)
                else:
                    _ = img.draw_rectangle(itemROL, color=color_R, tickness=5)
                    if totalRes == 1:
                        drawConfidenceText(img, (0, 0), 0, confidence)

        _ = lcd.display(img)


        print(clock.fps())

    elif flag==0:
        lcd.rotation(0)
        led_b.value(1)
        lcd.draw_string(0, 0, "Please press the key to turn on the system ")

_ = kpu.deinit(task)
