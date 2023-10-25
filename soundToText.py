import speech_recognition as sr  # as~ : 별칭 의미
import os

r = sr.Recognizer()
os.chdir(r"C:\\Texts")  # 경로지정
f = open("speech.txt", "w", encoding="UTF-8")
with sr.Microphone() as source:
    audio = r.listen(source)

try:
    text = r.recognize_google(audio, language="ko")
    f.write(text)
except sr.UnknownValueError:
    print("인식 실패")
except sr.RequestError as e:
    print(f"요청 실패 : {e}")
