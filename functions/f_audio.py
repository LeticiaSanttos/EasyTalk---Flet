import gtts
from playsound import playsound
#from langdetect import detect

import os

#passa os parametros para o audia
def audiodescricao(resp):
   try:
      fala = gtts.gTTS(resp, lang="pt")
#salva o audio
   
      caminho = 'functions/audio.mp3'
      fala.save(caminho)
#executa o audio
      print(caminho)
      playsound(caminho)
      os.remove(caminho)
   except:
         print('audio cancelado')
         #os.remove(caminho)