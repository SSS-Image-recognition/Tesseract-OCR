from tesserocr import PyTessBaseAPI, PSM
api = PyTessBaseAPI(psm=PSM.AUTO, lang='jpn')
api.SetImageFile('sample.png')
string = api.GetUTF8Text()
print(string)
