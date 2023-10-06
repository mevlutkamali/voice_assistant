import os
import cv2
import time
import random
import pyttsx3
import webbrowser
from gtts import gTTS
from playsound import playsound
import speech_recognition as sr
from selenium import webdriver
from selenium.webdriver.common.by import By

class VoiceAssistant:

    def __init__(self):
        self.recognizer = sr.Recognizer()

    def voice(self, texts):
        text_Voice = gTTS(text=texts, lang="tr")
        file = f"{random.randint(0, 1000000)}.mp3"
        text_Voice.save(file)
        playsound(file)
        os.remove(file)

    def microphone(self):
        with sr.Microphone() as value_source:
            print("Sizi dinliyorum...")
            listen = self.recognizer.listen(value_source)
            value = ""

            try:
                value = self.recognizer.recognize_google(listen, language="tr-TR")

            except sr.UnknownValueError:
                self.voice("Dedikleriniz anlaşılamadı...")

            return value.lower()

    def sound_response(self, incoming_voice):
        if incoming_voice == "merhaba":
            self.voice("Size de merhabalar. Size nasıl yardımcı olabilirim ?")

        elif incoming_voice in ['çıkış', 'exit', 'uygulamayı kapat', 'kendini kapatır mısın', 'sistemi kapat']:
            self.voice("Tabii, tekrar görüşmek üzere .")
            quit()

        elif incoming_voice in ['teşekkürler', 'teşekkürler life']:
            self.voice("Rica ederim .")

        elif incoming_voice == "sen kimsin" or incoming_voice == "bana kendinden bahseder misin":
            self.voice("Elbette size kendimden bahsedebilirim . Ben Life size yardımcı olmak için buradayım. Başka bir sorunuz var mı ?")

        elif incoming_voice in ['life', 'hey life', 'merhaba life']:
            self.voice("Sizi dinliyorum.")

        elif incoming_voice == "fotoğraf çek":
            self.voice("Kamera açılıyor .")

            camera = cv2.VideoCapture(0)
            control, image = camera.read()

            self.voice("Lütfen poz verin , çekiyorum . . .")

            cv2.imwrite('camera_Image.jpg', image)
            camera.release()
            cv2.destroyAllWindows()
            time.sleep(2)

            self.voice("Fotoğrafınızı görmek ister misiniz ?")

            reply = self.microphone().lower()

            if reply in "evet":
                image = cv2.imread('camera_Image.jpg')
                cv2.imshow('camera_image.jpg', image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

        elif incoming_voice in ['oyun aç', 'oyun açar mısın', 'game time']:
            self.voice("Hangi oyunu oynamak istersiniz ?")

            reply = self.microphone().lower()

            if reply in ['days', 'days gone']:
                self.voice("Oyununuzu hemen açıyorum .")
                os.startfile("D:\Days Gone\BendGame\Binaries\Win64\DaysGone.exe")

        elif incoming_voice in ['tarayıcı aç', 'tarayıcı açar mısın', 'google aç', 'google açar mısın', 'arama yap', 'arama yapar mısın']:
            self.voice("Ne aramamı istersiniz ?")

            reply = self.listen()

            url = "https://www.google.com/search?q=" + reply

            self.voice("{} ile ilgili bulduğum içerikler .".format(reply))

            browser = webdriver.Chrome()
            browser.get(url)

            site = browser.find_element(By.XPATH,"//*[@id='rso']/div[1]/div/div/div/div/div/div/div[1]/a/h3").click()

            time.sleep(5)
            browser.quit()

        elif incoming_voice in ['müzik aç', 'müzik açar mısın', 'şarkı aç',  'şarkı açar mısın', 'video aç', 'video açar mısın', 'film aç', 'film açar mısın',  'belgesel aç', 'belgesel açar mısın']:
            self.voice("Ne açmamı istersiniz?")

            self.open_youtube(self.listen())

    def open_youtube(self, query):
        url = f"https://www.youtube.com/results?search_query={query}"
        webbrowser.open(url)

    def listen(self):
        with sr.Microphone() as source:
            print("Dinliyorum...")
            audio = self.recognizer.listen(source)

            try:
                text = self.recognizer.recognize_google(audio, language="tr-TR")
                print("Algılanan metin:", text)
                return text.lower()

            except sr.UnknownValueError:
                print("Anlaşılamadı.")
                return ""

    def speak(self, text):
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

if __name__ == "__main__":
    assistant = VoiceAssistant()

    while True:
        incoming_voice = assistant.microphone().lower()

        if incoming_voice != "":
            print("Algılanan ses:", incoming_voice)
            assistant.sound_response(incoming_voice)

            if incoming_voice == "dur":
                break

    print("finish . . .")
