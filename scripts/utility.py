import imageio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from PIL import Image
import cv2

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

        ##############調整パラメータ##############
        minA = 100
        maxA = 800
        margin = 60
        #######################################

        #グレースケール変換
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        #MSER特徴量で文字っぽいのもを検出
        mser = cv2.MSER_create()
        mser.setMinArea(minA)
        mser.setMaxArea(maxA)

        #それぞれの文字を表すMSER特徴量点群に分割
        regions,_ = mser.detectRegions(gray)
        #regionsの構造：形状が(特徴点群の数,2)のnumpy配列で表された特徴量を各要素にもつリスト。
        #regions -> [文字数][特徴点群の数,2]
        
        for coord in regions:
            #文字のbounding boxを計算
            bbox = cv2.boundingRect(coord)

            #bounding boxの左上の点(x,y)と,幅w,高さhを取得
            x,y,w,h = bbox

            #アスペクト比
            aspect_ratio = w / h

            #サイズが小さすぎる、またはアスペクト比が大きすぎる文字を削除
            if w < 10 or h < 10 or aspect_ratio > 5:
                continue

            moji.append([x, y, w, h])


        #文字を上にあるものからソート
        moji_sort = sorted(moji, key=lambda x: x[1])

        for i in range(len(moji_sort)):
            x = moji_sort[i][0]
            y = moji_sort[i][1]
            w = moji_sort[i][2]
            h = moji_sort[i][3]
            #左上の点
            left_top = np.array([x,y])
            #右下の点
            right_bottom = np.array([x+w , y+h])

            if high_line >= y - margin and high_line <= (y + h + margin):
                #high_line(文字の中心線)付近にある文字を一つのstring(文字列)とみなす
                string[j].append(left_top)
                string[j].append(right_bottom)
            else:
                #文字がhigh_line付近から離れたら、その文字の中心線を新たなhigh_lineに設定
                high_line = y + h/2

                #新たな文字列として文字を格納
                string.append([])
                j = j + 1
                string[j].append(left_top)
                string[j].append(right_bottom)

            
        #最終出力の文字列のbounding boxを格納する変数
        clear_string = []
            
        for mojis in string:
            #文字列のbounding boxを計算
            bbox = cv2.boundingRect(np.float32(mojis))
            x,y,w,h = bbox

            #文字列として小さすぎるものを削除
            if w < 100 or h < 100:
                continue

            #bounding boxに余裕を持たせる
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
        

        for i in circle:
            pt1 = (i[1],i[2])
            pt2 = (i[1]+i[3],i[2]+i[4])
            cv2.rectangle(img,pt1,pt2,(0,255,0),5)

        for j in string:
            pt1 = (j[1],j[2])
            pt2 = (j[1]+j[3],j[2]+j[4])
            cv2.rectangle(img,pt1,pt2,(0,0,255),5)

        cv2.namedWindow('detected circles',cv2.WINDOW_NORMAL)
        cv2.imshow('detected circles',img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


        

