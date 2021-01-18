import imageio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from PIL import Image
import cv2
import pyocr
import os
from utility import utility

img = cv2.imread('IMG.png')
img_org = Image.open('IMG.png')
tools = pyocr.get_available_tools()
tool = tools[0]

u = utility()
global message
message,stickerId,stickerPackageId,index = u.check_text_stamp_detection(img)

sticker_list_index = 0
for i in index:
    message.insert(i,stickerId[sticker_list_index])
    message.insert(i,stickerPackageId[sticker_list_index])
    sticker_list_index += 1
'''
messageは配列で、画像を上から1行ずつ読み取った結果を格納しています。
文章のときはその認識結果を、スタンプのときはstickerpackageID,stickerIDの順に配列に格納しています
'''
print(message)