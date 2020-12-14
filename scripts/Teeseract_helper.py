import tesserocr
from PIL import Image

print(tesserocr.tesseract_version())

print(tesserocr.get_languages())  
image = Image.open('sample.png')

print(tesserocr.image_to_text(image, lang='jpn'))  

print(tesserocr.file_to_text('sample.png', lang='jpn'))
