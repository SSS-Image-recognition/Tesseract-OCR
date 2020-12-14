# ocr_card.py
import os
from PIL import Image
from PIL import Image
import pyocr
import pyocr.builders
import os
 
# インストール済みのTesseractへパスを通す
path_tesseract = "C:\\Program Files\\Tesseract-OCR"
if path_tesseract not in os.environ["PATH"].split(os.pathsep):
    os.environ["PATH"] += os.pathsep + path_tesseract


# OCRエンジンの取得
tools = pyocr.get_available_tools()
tool = tools[0]
 
# 画像の読み込み
img_org = Image.open("./bunsho.jpg")
 
# OCRの実行
builder = pyocr.builders.TextBuilder()
result = tool.image_to_string(img_org, lang="jpn", builder=builder)
 
print(result)