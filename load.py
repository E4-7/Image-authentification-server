import pytesseract
import cv2
import os
from PIL import Image

global face_cascade
#from google.colab.patches import cv2_imshow

def cropFace(img, gray):
  faces = face_cascade.detectMultiScale(gray, 1.3, 5)
  for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
    faces = img[y:y + h, x:x + w]
  return faces

def scanId(img, id, name) :
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  filename = "{}.jpg".format(os.getpid())
  cv2.imwrite(filename, gray)
  text = pytesseract.image_to_string(Image.open(filename), lang = 'Hangul')
  text = text.replace(" ", "")  # 띄어쓰기 제거
  os.remove(filename)

  if str(id) or name in text :
    print("id scan success")
    face = cropFace(img,gray)
    return face
  
  else:
    return -1

def init():
  face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

  return face_cascade



