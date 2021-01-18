import imageio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from PIL import Image
import cv2
import pyocr
import os

class utility(object):

    def __init__(self):
        self.pixel_margin = 20
    
    def binarization(self,img,th=None):
        img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        if not th == None:
            _, binary = cv2.threshold(img,th,255,cv2.THRESH_BINARY)

        else:
            blur = cv2.GaussianBlur(img,(5,5),0)
            _, binary = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            

        return binary

    def circle_detection(self,img,show_flag=False):
        
        cimg = img
        img = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
        img = cv2.medianBlur(img,5)

        circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,dp=1,minDist=50,param1=80,param2=90,minRadius=0,maxRadius=0)
        
        circles = np.uint16(np.around(circles))
        
        ret = []
        for i in circles[0,:]:
            x = i[0]
            y = i[1]
            r = i[2]
            ret.append(['stamp' , x-r-self.pixel_margin , y-r-self.pixel_margin , 2*r+self.pixel_margin , 2*r+self.pixel_margin])

        if show_flag:
            for i in circles[0,:]:
                cv2.rectangle(cimg,(i[0]-i[2],i[1]-i[2]),(i[0]+i[2],i[1]+i[2]),(0,255,0),5)

            cv2.namedWindow('detected circles',cv2.WINDOW_NORMAL)
            cv2.imshow('detected circles',cimg)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return ret

    def string_detection(self,img,show_flag=False):

        moji = []
        string = []
        j = -1
        high_line = 10000
        
        minA = 100
        maxA = 800
        margin = 60
        

        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        mser = cv2.MSER_create()
        mser.setMinArea(minA)
        mser.setMaxArea(maxA)

        regions,_ = mser.detectRegions(gray)

        
        for coord in regions:
            bbox = cv2.boundingRect(coord)
            x,y,w,h = bbox

            aspect_ratio = w / h

            if w < 10 or h < 10 or aspect_ratio > 5:
                continue

            moji.append([x, y, w, h])


        moji_sort = sorted(moji, key=lambda x: x[1])

        for i in range(len(moji_sort)):
            x = moji_sort[i][0]
            y = moji_sort[i][1]
            w = moji_sort[i][2]
            h = moji_sort[i][3]
            left_top = np.array([x,y])
            right_bottom = np.array([x+w , y+h])

            if high_line >= y - margin and high_line <= (y + h + margin):
                string[j].append(left_top)
                string[j].append(right_bottom)
            else:
                high_line = y + h/2

                string.append([])
                j = j + 1
                string[j].append(left_top)
                string[j].append(right_bottom)

        
        clear_string = []
            
        for mojis in string:
            bbox = cv2.boundingRect(np.float32(mojis))
            x,y,w,h = bbox

            if w < 100 or h < 100:
                continue

            clear_string.append(['text' , x-self.pixel_margin , y-self.pixel_margin , w+self.pixel_margin , h+self.pixel_margin])
            

            if show_flag:
                p1 = (x-self.pixel_margin,y-self.pixel_margin)
                p2 = (x+w+self.pixel_margin,y+h+self.pixel_margin)
                cv2.rectangle(img,p1,p2,(0,0,255),5)
                

        if show_flag:
            cv2.namedWindow('detected circles',cv2.WINDOW_NORMAL)
            cv2.imshow('detected circles',img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        
        
        return clear_string


    def check_text_stamp_detection(self,img):
        circle = self.circle_detection(img)
        string = self.string_detection(img)
        img_org = Image.open('IMG.png')
        tools = pyocr.get_available_tools()
        tool = tools[0]
        
        global stamp_list
        stamp_list=[]
        for i in circle:
            pt1 = (i[1],i[2])
            pt2 = (i[1]+i[3],i[2]+i[4])
            cv2.rectangle(img,pt1,pt2,(0,255,0),5)
            img_box = img_org.crop((i[1], i[2], i[1]+i[3], i[2]+i[4]))
            builder = pyocr.builders.TextBuilder(tesseract_layout=9)
            result_stamp = tool.image_to_string(img_box, lang="jpn", builder=builder)                      
            
            stamp_list.append(result_stamp)
        n=0  
        index_counter = 0  
        stickerPackageId_list = []
        stickerId_list = []
        message_list = []
        index = []

        for j in string:
            pt1 = (j[1],j[2])
            pt2 = (j[1]+j[3],j[2]+j[4])
            cv2.rectangle(img,pt1,pt2,(0,0,255),5)
            
            for i in circle:
                #スタンプの緑四角と文章の赤四角が重なっているとき
                if j[1]+j[3] > i[1] and j[1]+j[3] < i[1]+i[3] and j[2]+j[4] > i[2] and j[2]+j[4] < i[2]+i[4] or j[1] >  i[1] and j[1] < i[1]+i[3] and j[2] > i[2] and j[2] < i[2]+i[4]:

                    if stamp_list[n] == '(4か':  #笑うのスタンプ
                        message = "スタンプ"
                        stickerPackageId_list.append("1")
                        stickerId_list.append("2")

                    if stamp_list[n] == '0':   #怖いのスタンプ
                        message = "スタンプ"
                        stickerPackageId_list.append("2")
                        stickerId_list.append("24")
                      
                    if stamp_list[n] == "焦":
                        message = "スタンプ"
                        stickerPackageId_list.append("1")
                        stickerId_list.append("3")
                       
                    if stamp_list[n] == "怒":
                        message = "スタンプ"
                        stickerPackageId_list.append("2")
                        stickerId_list.append("33")

                    
                    flag = 0
                    n = n + 1 
                    index.append(index_counter)
                    break
                #文章とスタンプが重なっていないとき
                else:
                	flag = 1

            #文章とスタンプが重なっていないとき、文章1行のOCRを行う。
            if flag == 1:
                #四角で切り取ったところの文章を単一行テキストとしてOCRする。
                img_box = img_org.crop((j[1], j[2], j[1]+j[3], j[2]+j[4]))
                builder = pyocr.builders.TextBuilder(tesseract_layout=7)
                message = tool.image_to_string(img_box, lang="jpn", builder=builder) 
                message_list.append(message)
                index_counter = index_counter + 1 
        
        for i in range(len(index)):
            if i == 0:
                pass
            else:
                index[i] += 2
        
        return  message_list,stickerId_list,stickerPackageId_list,index


