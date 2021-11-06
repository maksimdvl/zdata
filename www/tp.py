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

def get_contours(image):
   # удаление цвета
   gray_image= image[:,:,0]

   # (1) thresholding image
   ret,thresh_value = cv2.threshold(gray_image,180,255,cv2.THRESH_BINARY_INV)

   # (2) dilating image to glue letter with e/a
   kernel = np.ones((2,2),np.uint8)    
   dilated_value = cv2.dilate(thresh_value,kernel,iterations = 1)

   # (3) просмотр контуров
   contours, hierarchy = cv2.findContours(dilated_value,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

   # (4) поиск координат 
   coordinates = []
   for contour in contours:
      x, y, w, h = cv2.boundingRect(contour)
      if h> 50 and w>50 and h*w<350000:  
         coordinates.append((x,y,w,h))
   return coordinates

def sort2(val):   #helper for sorting by y
   return val[1]

def recognize_table(image, coordinates):
   recognized_table = row = []
   prev_y = 0
   coordinates.sort() #sort by x
   coordinates.sort(key = sort2) # sort by y
   for coord in coordinates:
      x,y,w,h = coord
      if y > prev_y+5: #new row if y is changed
         recognized_table.append(row)
         row = [] 
      crop_img = image[y:y+h, x:x+w]
      recognized_string = pytesseract.image_to_string(crop_img, lang="rus")
      row.append(recognized_string.replace("\n"," "))
      prev_y = y
   return recognized_table

def func(pic):
   image = numpy.array(pic) #np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
   image = np.ascontiguousarray(image[..., [2, 1, 0]])  
   contours_coords = get_contours(page)
   recognize_table(pic, contours_coords)
      

# Then, after you make your changes to the array, you should be able to do either pic.putdata(pix) or create a new image with Image.fromarray(pix).
