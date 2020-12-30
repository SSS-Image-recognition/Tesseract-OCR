#utility.py内の関数check_text_stamp_detectionに少しコードを付け加えました。

 def check_text_stamp_detection(self,img):
        # 画像の読み込み
        img_org = Image.open('IMG_1294.png')

        # OCRエンジンの取得
        tools = pyocr.get_available_tools()
        tool = tools[0]


        circle = self.circle_detection(img)
        string = self.string_detection(img)
        

        for i in circle:
            pt1 = (i[1],i[2])
            pt2 = (i[1]+i[3],i[2]+i[4])
            cv2.rectangle(img,pt1,pt2,(0,255,0),5)

            #スタンプと認識したところを切り取り円に囲まれた１つの単語としてOCRする。
            img_box = img_org.crop((i[1], i[2], i[1]+i[3], i[2]+i[4]))
            builder = pyocr.builders.TextBuilder(tesseract_layout=9)
            result_stamp = tool.image_to_string(img_box, lang="jpn", builder=builder)
            
            #読み取った結果をresult_stamp.txtに保存する
            with open('result_stamp.txt','a',newline='\n') as f:
                f.write(result_stamp)
                f.write('\n')


        for j in string:
            pt1 = (j[1],j[2])
            pt2 = (j[1]+j[3],j[2]+j[4])
            cv2.rectangle(img,pt1,pt2,(0,0,255),5)

            #文章と認識したところを切り取り単一行テキストとしてOCRする。
            img_box = img_org.crop((j[1], j[2], j[1]+j[3], j[2]+j[4]))
            builder = pyocr.builders.TextBuilder(tesseract_layout=7)
            result = tool.image_to_string(img_box, lang="jpn", builder=builder)
            
            #読み取った結果をresult.txtに保存する
            with open('result.txt','a',newline='\n') as f:
                f.write(result)
                f.write('\n')

        cv2.namedWindow('detected circles',cv2.WINDOW_NORMAL)
        cv2.imshow('detected circles',img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

