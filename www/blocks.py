import cv2
import numpy as np

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
      if h > 50 and w > 50 and h*w < 350000:  
         coordinates.append((x, y, w, h))
   return coordinates

def sort2(val):   #helper for sorting by y
   return val[1]

def get_crop_image(image, coordinates):
  return 0
   
def recognize_table(image, coordinates):
   for coord in coordinates:
      x, y, w, h = coord
      crop_img = image[y : y+h, x : x+w]
      print(pytesseract.image_to_string(crop_img, lang="rus")
   return recognized_table

def block(pic):
   image = numpy.array(pic) #np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
   image = np.ascontiguousarray(image[..., [2, 1, 0]])  
   contours_coords = get_contours(page)
   recognize_table(pic, contours_coords)
      

#  pic.putdata(pix) Image.fromarray(pix).
