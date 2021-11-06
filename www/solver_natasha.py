from PIL import Image, ImageDraw
import natasha, pytesseract

from www.snils_pasport_phone_detect import Get_All_spans

def ocr_core(img):
   #Распознаем изображение в текст
   text = pytesseract.image_to_string(img, config=r'-l rus --psm 6')
   # Если мало текста, считаем что анализировать нечего, возвращаем исходное изображение
   if len(text) < 5:return img 

   # Для лингвистического анализа используем библиотеку Natasha
   #extractor = natasha.NamesExtractor()
   #matches = extractor(text)
   #spans = [_.span for _ in matches]

   # ----------------------------
   extractors = [
      natasha.NamesExtractor(),
      natasha.AddressExtractor(),
   ]
   spans = []
   for extractor in extractors:
      matches = extractor(text)
      spans.extend(_.span for _ in matches)

   for i in Get_All_spans(text):
      spans.append(i)
   # -------------------------------


   fioList = [text[slice(*sl)] for sl in spans if len(text[slice(*sl)]) > 2]  # [Протасов Александр Сергеевич, ...]
   # Формируем список для закрашивания именованных сущностей из текста
   name_str = "|".join(fioList)\
                 .replace(" ", "|") \
                 .replace("\n", "|")              # "Протасов|Александр|Сергеевич|Киселев|Филипп|Михайлович|Вишневская|Елена|Владимировна"

   if name_str == "": return img
   
   #Распознаем изображение в блоки с координатами
   df = pytesseract.image_to_data(img, config=r'-l rus --psm 6', output_type=pytesseract.Output.DATAFRAME)
   
   df1 = df[['left', 'top', 'width', 'height', 'text']].fillna('')
   # Формируем массив исключенных ФИО с координатами
   df1 = df1[df1['text'].str.contains(name_str)]

   df1 = df1[df1['left'] > 10]
   df1 = df1[df1['top'] > 10]

   for idx, row in df1[:].iterrows():
      (x, y, w, h) = (row['left'], row['top'], row['width'], row['height'])
      pencil = ImageDraw.Draw(img)
      # Рисуем зеленый квадрат по координатам 
      pencil.rectangle((x, y, x + w, y + h), fill='green')

   return img
