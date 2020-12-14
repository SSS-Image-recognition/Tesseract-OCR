from PIL import Image
import pyocr
import pyocr.builders

# Getting the OCR engine
tools = pyocr.get_available_tools()
tool = tools[0]

# Loading the original image
img_org = Image.open("zairyucard_omote.jpg")

# Crop out the numbered parts
img_box = img_org.crop((770, 40, 1100, 90))

# Execute OCR
builder = pyocr.builders.TextBuilder()
result = tool.image_to_string(img_box, lang="jpn", builder=builder)

print(result)