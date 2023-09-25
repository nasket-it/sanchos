import uuid
import os
import speech_recognition as sr
from pydub import AudioSegment
import tempfile


def decorator_remove_file(func):
    def wrapper(*args, **kwargs):
        rez = func(*args, **kwargs)
        try:
            os.remove('voice_message.ogg')
            os.remove('voice_message.wav')
        except:
            pass
        return rez
    return wrapper
#
def convert_ogg_wav(file):
    wfn = file.replace('.ogg', '.wav')
    x = AudioSegment.from_file(file)
    x.export(wfn, format='wav')


language='ru_RU'


@decorator_remove_file
def audio_to_text(file):
    r = sr.Recognizer()
    with sr.AudioFile(file) as source:
        audio = r.record(source)
        text = r.recognize_google(audio_data=audio, language=language)
        return text



def convert_and_recognize(file_path):
    # Создаем временный файл, который будет автоматически удаляться после закрытия
    with tempfile.NamedTemporaryFile(delete=True) as temp_wav:
        audio = AudioSegment.from_ogg(file_path)
        audio.export(temp_wav.name, format="wav")  # Экспортируем аудио в wav-формате во временный файл

        recognizer = sr.Recognizer()
        with sr.AudioFile(temp_wav.name) as source:
            # Записываем аудио из файла
            audio_file = recognizer.record(source)
            # Применяем распознавание речи с помощью Google Speech Recognition
            try:
                result = recognizer.recognize_google(audio_file, language='ru-RU')
                print('Распознан текст:', result)
                return result
            except sr.UnknownValueError:
                print("Google Speech Recognition не смог понять аудио")
            except sr.RequestError:
                print("Could not request results from Google Speech Recognition service")


async def dewnload_and_converted_audio_text(event):
    if event.message.voice:
        # Получаем голосовое сообщение
        voice_message = await event.message.download_media()

        # Создаем временный файл, который будет автоматически удаляться после закрытия
        with tempfile.NamedTemporaryFile(delete=True) as temp_ogg:
            # Копируем голосовое сообщение во временный файл
            with open(voice_message, 'rb') as file:
                temp_ogg.write(file.read())

            # Преобразуем и распознаем речь
            text = convert_and_recognize(temp_ogg.name)
            return f'👺 Voice\n{text}'

async def esli_voice_to_text_ili_text_text(event):
    return f'💥🔊💭  {await dewnload_and_converted_audio_text(event)}\n{event.message.message}' if  event.message.voice else event.message.message
    # if event.message.voice:#если сообщение голосовое
    #     text =f'💥🔊💭  {await dewnload_and_converted_audio_text(event)}'
    # else:
    #     text = event.message.message # достаем только текст сообщени