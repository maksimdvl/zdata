import PIL
import pytesseract
import numpy as np

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
