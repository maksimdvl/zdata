from PIL import Image, ImageDraw
import pytesseract
import numpy as np
import pdf2image
from deeppavlov import configs, build_model

# список изображений отправляем на анализ
def images_ocr(images, ner):
   image_ocr = list()
   for img in images:
      img_blur = ocr_core(img, ner)
      image_ocr.append(img_blur)
   return image_ocr

# В данной функции процесс распознавания, анализа текста и корректировки изображения разбит по этапам
def ocr_core(img, ner):  
   df = ocr(img)
   df_words = df_extract(df) 
  
   tokens, tags = ner([df_words['text'].to_list()])
   df_name = df_filter(df_words, tokens, tags)
   return img_draw(img, df_name)

# распознаем избражение и отдаем DATAFRAME
def ocr(img):
   return pytesseract.image_to_data(img, config=r'-l rus --psm 6 --oem 1', output_type=pytesseract.Output.DATAFRAME)

# усечение датафрейма по строка и столбцам
def df_extract(df):
   df_words = df[['level', 'left', 'top', 'width', 'height', 'text', 'conf']]
   df_words = df_words.fillna(f'\t')
   
   # оставляем только распознаные слова которые находятся на уровне 5
   df_words = df_words[df_words['level']==5]
   return df_words  

# фильтруем данные "B-PER", "I-PER"
def df_filter(df_words, tokens, tags):
   df_words.loc[:, "tok"] = tokens[0]
   df_words.loc[:, "tag"] = tags[0]
  
   df_name = df_words[(df_words['tag'].isin(["B-PER", "I-PER"]))]

   df_name = df_name[df_name['left'] > 5]
   df_name = df_name[df_name['top'] > 5]
   return df_name

# рисуем на изображении прямоугольник по координатам слов
def img_draw(img, df_name):
   for idx, row in df_name[:].iterrows():
      (x, y, w, h) = (row['left'], row['top'], row['width'], row['height'])
      pencil = ImageDraw.Draw(img)
      pencil.rectangle((x, y, x + w, y + h), fill='green')
   return img

# создаем модель
def build_ner():
   config_path = configs.ner.ner_rus_bert
   ner = build_model(config_path, download=False)
   return ner

# конвертируем ПДФ в изображение
def pdf_to_image(pdf_file):
   return pdf2image.convert_from_path(pdf_file, dpi=300, fmt='png')
