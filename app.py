import streamlit as st
from PIL import Image
from ultralytics import YOLO
#import easyocr
from paddleocr import PaddleOCR
import ssl
import cv2
import numpy as np
ssl._create_default_https_context = ssl._create_unverified_context

model = YOLO("runs/detect/yolov8/weights/best.pt")

def preprocessing(image):
  norm_img = np.zeros((img.shape[0], img.shape[1]))
  img = cv2.normalize(img, norm_img, 0, 255, cv2.NORM_MINMAX)
  img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

  return image

def main():
    style()

    uploaded_file = st.file_uploader("Choose a image file", type=['jpg', 'png', 'jpeg'])

    if uploaded_file is not None:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        opencv_image = cv2.imdecode(file_bytes, 1)

        st.image(opencv_image, channels="BGR")

        results = model.predict(source=image, save=False)

        for result in results:
            coordinates = result.boxes.xyxy

            x1, y1, x2, y2 = map(int, coordinates[0])

            cropped_image = opencv_image[y1:y2, x1:x2]
            image = preprocessing(cropped_image)

            '''
            reader = easyocr.Reader(['en'])
            result = reader.readtext(cropped_image, detail = 0, allowlist='0123456789')
            #print(result)
            for res in result:
                st.write(res)
            '''

            ocr = PaddleOCR(lang='en')
            result = ocr.ocr(image, cls=False)

            st.image(image, caption="Brojilo", use_column_width=True)

            for idx in range(len(result)):
                res = result[idx]
                for line in res:
                    st.write(line[0])


def style():
  st.set_page_config(page_title='Čitač plina')
  st.title("Očitavanje brojila plina")


if __name__ == '__main__':
  main()