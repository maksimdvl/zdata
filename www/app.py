import os
import random
from PIL import Image
from flask import Flask, render_template, request

# import our OCR function
#from tess_pavlov_ner_rus import ocr_core
from solver_natasha import ocr_core
import convert_pdf
import fitz


def convert_pdf(file_pdf):
    doc = fitz.open(file_pdf)

    jpegs = list()
    for num, page in enumerate(doc.pages()):
        pix = page.get_pixmap()
        pix.save("temp1.jpeg")
        jpegs.append(Image.open("temp1.jpeg"))
    return jpegs

UPLOAD_FOLDER = '/static/uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'pdf'])

app = Flask(__name__)


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
            file.save(os.path.join(os.getcwd() + UPLOAD_FOLDER, file.filename)) #сохранение файла
            
            if file.filename.rsplit('.', 1)[1].lower() == 'pdf':
               jpegs = convert_pdf(os.path.join(os.getcwd() + UPLOAD_FOLDER, file.filename))
            else: jpegs = [Image.open(file)]
            
            jpegs_ocr = list(map(ocr_core, jpegs))
            print("ocr ok")
            if file.filename.rsplit('.', 1)[1].lower() == 'pdf':
               render_pdf = f"{random.randint(0, 32000)}_ocr.pdf"
               jpegs_ocr[0].save(os.path.join(os.getcwd() + UPLOAD_FOLDER, render_pdf),
                                 save_all=True,
                                 append_images=jpegs[1:])
               return render_template('upload.html',
                                      msg='Процесс закончен',
                                      type = 'pdf',
                                      pdf_src=UPLOAD_FOLDER + render_pdf)
            else:
               render_img = f"{random.randint(0, 32000)}_ocr.jpeg" 
               jpegs_ocr[0].save(os.path.join(os.getcwd() + UPLOAD_FOLDER, render_img))

               return render_template('upload.html',
                                      msg='Процесс закончен',
                                      type = 'jpeg',
                                      img_src=UPLOAD_FOLDER + render_img)
    elif request.method == 'GET':
        return render_template('upload.html')

if __name__ == '__main__':
    app.run()
