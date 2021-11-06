import os
import random
from PIL import Image
from flask import Flask, render_template, request
import numpy as np
import tp
import pdf2image
from itertools import zip_longest
from deeppavlov import configs, build_model


LOAD = '/load/'
UPLOAD_FOLDER = '/static/uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'pdf'])

app = Flask(__name__)

ner(download=False)

def ner(download=False):
   config_path = configs.ner.ner_rus_bert
   ner = build_model(config_path, download=False)
   return ner   

def pdf_to_image(pdf_file):
   return pdf2image.convert_from_path(pdf_file, dpi=300, fmt='png')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return render_template('upload.html', msg='Файл не выбран')
        file = request.files['file']
        
        if file.filename == '':
            return render_template('upload.html', msg='Файл не выбран')

        if file and allowed_file(file.filename):
            f = file.save(os.path.join(os.getcwd() + LOAD, file.filename)) #сохранение файла
            
            if file.filename.rsplit('.', 1)[1].lower() == 'pdf':
               images = pdf_to_image(os.path.join(os.getcwd() + LOAD, file.filename))
            else: images = [Image.open(file)]
            
            image_ocr = list() #list(map(easyner.ocr_core, param))
            for img in images:
               img_blur = tp.ocr_core(img, ner)
               image_ocr.append(img_blur)
            
            print("ocr ok")
            if file.filename.rsplit('.', 1)[1].lower() == 'pdf':
               render_pdf = f"{random.randint(0, 32000)}_ocr.pdf"
               image_ocr[0].save(os.path.join(os.getcwd() + UPLOAD_FOLDER, render_pdf),
                                 save_all=True,
                                 append_images=image_ocr[1:], resolution=100)
               
               return render_template('upload.html',
                                      msg='Процесс закончен',
                                      type = 'pdf',
                                      pdf_src=UPLOAD_FOLDER + render_pdf)
            else:
               render_img = f"{random.randint(0, 32000)}_ocr.jpeg" 
               image_ocr[0].save(os.path.join(os.getcwd() + UPLOAD_FOLDER, render_img))

               return render_template('upload.html',
                                      msg='Процесс закончен',
                                      type = 'jpeg',
                                      img_src=UPLOAD_FOLDER + render_img)
    elif request.method == 'GET':
        return render_template('upload.html')

if __name__ == '__main__':
    app.run()
