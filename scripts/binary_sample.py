from PIL import Image
import pyocr
import pyocr.builders

# Getting the OCR engine
tools = pyocr.get_available_tools()
tool = tools[0]

# Loading the original image
img_org = Image.open("zairyucard_omote.jpg")
img_rgb = img_org.convert("RGB")
pixels = img_rgb.load()

# Manuscript image processing (set white=255,255,255 except for blackish colors)
c_max = 169
for j in range(img_rgb.size[1]):
    for i in range(img_rgb.size[0]):
        if (pixels[i, j][0] > c_max or pixels[i, j][1] > c_max or
                pixels[i, j][0] > c_max):
            pixels[i, j] = (255, 255, 255)

# Execute OCR
builder = pyocr.builders.TextBuilder()
result = tool.image_to_string(img_rgb, lang="jpn", builder=builder)

print(result)