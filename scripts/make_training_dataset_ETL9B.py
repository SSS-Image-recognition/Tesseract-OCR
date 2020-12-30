#this code is refered to http://cedro3.com/ai/kmnist-vae/
import numpy as np
import matplotlib.pyplot as plt
import random
import csv
from PIL import Image
from utility import utility
import os

util = utility()

#一行の文字数
line_length = 40

#学習データの画像数
all_datasets = 90

#文字の種類の数
PATH = '/Users/okamotoyuutarou/test'
class_num = len(os.listdir(PATH))


# reading ETL9B dataset
[x_train, x_test, y_train, y_test] = util.devide_DATA(PATH)

# make a table of pyplot
# refer to 'https://qiita.com/gaku8/items/90167693f142ebb55a7d#3-subplots%E3%81%A8axxx'
fig,axes = plt.subplots(nrows=1, ncols=line_length, figsize=(12, 12))
plt.subplots_adjust(wspace=0)

# deleting backspace, refer to 'http://kaisk.hatenadiary.com/entry/2014/11/30/163016'
fig.patch.set_alpha(1)


for r in range(all_datasets):
    #ラベルの文字列を格納する変数
    texts = []
    for c in range(line_length):
        
        #学習データセットからランダムに一文字選ぶ
        index = random.randint(0, y_train.shape[0]-1)
        img = x_train[index]
        char = y_train[index]
        
        axes[c].axis("off")
        axes[c].imshow(255-img, cmap='Greys_r')
        texts.append(char)

    #ファイル名
    img_file = f'ETL9B.{r}.tif'
    txt_file = f'ETL9B.{r}.gt.txt'

    # make a ***.git.txt using 'texts'
    with open(txt_file, mode='w') as f:
        f.write(''.join(texts))


    # saving ***.tif (at bottom, i cannot avoid to generate unnecessary space)
    plt.savefig(img_file, bbox_inches="tight", pad_inches=0.0)
    

    # by usin PIL method, trimming the unnecessary space in *.tif
    # refer to 'https://note.nkmk.me/python-pillow-image-crop-trimming/'
    im = Image.open(img_file)
    im_crop = im.crop((1, 1, 963, 30))
    im_crop.save(img_file, quality=100)