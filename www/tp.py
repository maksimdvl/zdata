import PIL
import pytesseract
import numpy as np
import pdf2image
from deeppavlov import configs, build_model

def ocr_core(img, ner):  
   df = ocr(img)
   df_words = df_extract(df) 
  
   tokens, tags = ner([df_words['text'].to_list()])
   df_name = df_filter(df_words, tokens, tags)
   return img

def ocr(img):
   return pytesseract.image_to_data(img, config=r'-l rus --psm 6 --oem 1', output_type=pytesseract.Output.DATAFRAME)

def df_extract(df):
   df_words = df[['level', 'left', 'top', 'width', 'height', 'text', 'conf']]
   df_words = df_words.fillna(f'\t')
   df_words = df_words[df_words['level']==5]
   return df_words  

def df_filter(df_words, tokens, tags):
   df_words.loc[:, "tok"] = tokens[0]
   df_words.loc[:, "tag"] = tags[0]
  
   df_name = df_words[(df_words['tag'].isin(["B-PER", "I-PER"]))]

   df_name = df_name[df_name['left'] > 5]
   df_name = df_name[df_name['top'] > 5]
   return df_name

def img_draw(img, df_name):
   for idx, row in df_name[:].iterrows():
      (x, y, w, h) = (row['left'], row['top'], row['width'], row['height'])
      pencil = PIL.ImageDraw.Draw(img)
      pencil.rectangle((x, y, x + w, y + h), fill='green')
   return img

def build_ner():
   config_path = configs.ner.ner_rus_bert
   ner = build_model(config_path, download=False)
   return ner

def pdf_to_image(pdf_file):
   return pdf2image.convert_from_path(pdf_file, dpi=300, fmt='png')

def images_ocr(images, ner):
   image_ocr = list() #list(map(easyner.ocr_core, param))
   for img in images:
      img_blur = ocr_core(img, ner)
      image_ocr.append(img_blur)
   return image_ocr
