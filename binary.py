import imageio
import numpy as np

img = imageio.imread('/Users/okamotoyuutarou/main/IMG_1235.png')
img = np.max(img,axis=-1)

th = 115
new_img = np.where(img<th,0,255)
new_img = np.uint8(new_img)

imageio.imwrite('/Users/okamotoyuutarou/main/img.png',new_img)