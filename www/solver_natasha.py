from PIL import Image, ImageDraw
import natasha, pytesseract


def ocr_core(img):

   text = pytesseract.image_to_string(img, config=r'-l rus --psm 6')
   if len(text) < 5:return img

   extractor = natasha.NamesExtractor()
   matches = extractor(text)
   spans = [_.span for _ in matches]

   fioList = [text[slice(*sl)] for sl in spans if len(text[slice(*sl)]) > 2]  # [Протасов Александр Сергеевич, ...]
  
   name_str = "|".join(fioList)\
                 .replace(" ", "|") \
                 .replace("\n", "|")              # "Протасов|Александр|Сергеевич|Киселев|Филипп|Михайлович|Вишневская|Елена|Владимировна"


   if name_str == "": return img
            
   df = pytesseract.image_to_data(img, config=r'-l rus --psm 6', output_type=pytesseract.Output.DATAFRAME)
   
   df1 = df[['left', 'top', 'width', 'height', 'text']].fillna('')
   df1 = df1[df1['text'].str.contains(name_str)]

   df1 = df1[df1['left'] > 10]
   df1 = df1[df1['top'] > 10]

   for idx, row in df1[:].iterrows():
      (x, y, w, h) = (row['left'], row['top'], row['width'], row['height'])
      pencil = ImageDraw.Draw(img)
      pencil.rectangle((x, y, x + w, y + h), fill='green')

   return img
