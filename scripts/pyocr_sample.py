from PIL import Image
import pyocr
import pyocr.builders

tools = pyocr.get_available_tools()
tool = tools[0]
 
img_org = Image.open("sample.png")
 
builder = pyocr.builders.TextBuilder()
result = tool.image_to_string(img_org, lang="jpn", builder=builder)
 
print(result)