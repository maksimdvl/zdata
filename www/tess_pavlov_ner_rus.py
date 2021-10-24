from PIL import Image, ImageDraw
import pytesseract

from deeppavlov import configs, build_model

def ocr_core(img):
   config_path = configs.ner.ner_rus_bert
   #ner = build_model(config_path, download=True)
   ner = build_model(config_path, download=True)

   #custom_config = r'-l rus --psm 6'
   df = pytesseract.image_to_data(img,
                                  config=r'-l rus --psm 6',
                                  output_type=pytesseract.Output.DATAFRAME
                                 )

   df1 = df[['left', 'top', 'width', 'height', 'text', 'conf']].fillna(f'\t')

   tokens, tags = ner([df1['text'].to_list()])
   del ner
   df1.loc[:, "tok"] = tokens[0]
   df1.loc[:, "tag"] = tags[0]

   print(df1.head(3))

   df2 = df1[(df1['tag'].isin(["B-PER", "I-PER"]))]

   df2 = df2[df2['left'] > 10]
   df2 = df2[df2['top'] > 10]
   for idx, row in df2[:].iterrows():
      (x, y, w, h) = (row['left'], row['top'], row['width'], row['height'])
      pencil = ImageDraw.Draw(img)
      pencil.rectangle((x, y, x + w, y + h), fill='green')

   #img.save(f'{name_f}_out.jpg')
   return img
