#this code is refered to http://cedro3.com/ai/kmnist-vae/

"""
これを実行する前に、make_dataset.pyを実行してください。
そうすると以下のようなディレクトリ構造になります。
ETL9B
├── 3a2b
│   ├── ETL9B_7_3a2b_1.png
│              .
│              .
│              .
│   └── ETL9B_7_3a2b_7.png
│
├── 3a2c
│   ├── ETL9B_7_3a2c_1.png
│              .
│              .
│              .
│   └── ETL9B_7_3a2c_9.png
│
└── 3a7c
    ├── ETL9B_7_3a7c_1.png
    │         .
              .
              .
    └── ETL9B_7_3a7c_7.png
    .
    .
    .

その上で、'ETL9B'のディレクトリに移動してから実行してください。
"""


import numpy as np
import matplotlib.pyplot as plt
import random
import csv
from PIL import Image
from utility import utility
import os
import imageio

util = utility()

#一行の文字数
line_length = 40

#学習データの画像数
all_datasets = 100

#文字の種類の数
PATH = '/Users/okamotoyuutarou/test'
class_num = len(os.listdir(PATH))


# reading ETL9B dataset
[x_train, y_train] = util.devide_DATA(PATH)
num_of_img = x_train.shape[0]
h = x_train.shape[1]
w = x_train.shape[2]


print('\n')
for r in range(all_datasets):
    print(f'\rmaking Trainging image and Ground Truth text {r+1}/{all_datasets}',end='')

    #出力画像を格納する変数
    string_img = np.zeros((h,w*line_length))
    
    #ラベルの文字列を格納する変数
    texts = line_length*['']
    for c in range(line_length):
        
        #学習データセットからランダムに一文字選ぶ
        index = random.randint(0, num_of_img-1)
        img = x_train[index]
        char = y_train[index]
        
        
        string_img[:, w*c : w*(c+1)] = 255-img
        texts[c] = char

    #ファイル名
    img_file = f'ETL9B.{r}.tif'
    txt_file = f'ETL9B.{r}.gt.txt'

    # make a ***.git.txt using 'texts'
    with open(txt_file, mode='w') as f:
        f.write(''.join(texts))

    Image.fromarray(string_img).save(img_file,quality=100)



    