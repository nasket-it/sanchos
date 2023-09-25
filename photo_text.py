import pytesseract
import easyocr
import cv2
import matplotlib.pyplot as plt
from PIL import Image
# from all_functions import get_keyword_tiker_moex, decorator_speed
from Config import Config
from PIL import Image
import pytesseract
import io
import re

def raspoznavanie_texta_na_photo(photo):
    # читать изображение с помощью OpenCV
    image = cv2.imread(photo)
    # или вы можете использовать подушку
    # image = Image.open("test.png")

    # получаем строку
    string = pytesseract.image_to_string(image, lang='eng' )
    # string2 = pytesseract.image_to_string(image,lang='rus')
    # rezult = string2 + string
    # r = re.compile("[а-яА-Я]+")
    # words = str(string2).split()
    # russian = [w for w in filter(r.match, words)]

    # печатаем
    return string
# raspoznavanie_texta_na_photo()

# def raspoznavanie_texta_na_photo():
#     reader = easyocr.Reader(['en'])
#     rezult = reader.readtext("exempl_goodwin_signals.jpg")
#     print(rezult)
# raspoznavanie_texta_na_photo()




def fast_image_to_text(image_path):
    # Загрузка изображения
    image = cv2.imread(image_path)

    # Преобразование в оттенки серого
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Применение размытия по Гауссу
    blur = cv2.GaussianBlur(gray, (3, 3), 0)

    # Применение порогового значения Оцу
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Применение морфологических операций для удаления шума
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)

    # Распознавание текста
    text = pytesseract.image_to_string(opening, lang='eng', config='--psm 6')

    return text


def photo_to_text(photo):
    text = pytesseract.image_to_string(photo, lang='rus+eng')
    return text


async def download_photo(event, client):
    if event.photo:
        # Скачиваем фото
        photo_bytes = await client.download_media(event.photo, bytes)
        image = Image.open(io.BytesIO(photo_bytes))
        return image


def filter_words_rus_en(lst):
    pattern = re.compile(r'^[а-яА-Яa-zA-Z]+$')
    filtered_list = [word for word in lst if pattern.match(word)]
    text = ' '.join(filtered_list)
    return f'🌿🌿🌿 Текст из фото \n{text}'
