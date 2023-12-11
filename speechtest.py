import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source:
  print("Listening")
  audio = r.listen(source)

try:
    print("I thinks you said " + r.recognize_(audio))
except sr.UnknownValueError:
    print("I could not understand audio")
except sr.RequestError as e:
    print("error; {0}".format(e))
