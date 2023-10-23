from translate import Translator
from playsound import playsound
from langdetect import detect
#from textblob import TextBlob
import sys
# from langdetect import detect
# sys.path.insert(1, "./functions")
# import f_corretor as ct

class Tradutor():


    def __init__(self, frase):
        #idioma = detect(frase)
        self.__from_lang = "en"
        self.__to_lang = "pt-br"
        self.__frase = frase
      #  if idioma == "so" or idioma == 'cy' or idioma == 'de' or idioma == 'sw':
      #      self.__from_lang = "en"
    # @staticmethod 
    # def verifica_idioma(e):
      
    #   cd_idioma = {"Inglês":"en", "Português":"pt", "Chinês":"zh-hk",
    #                "Espanhol":"es", "Francês":"fr-ch", "Árabe":"ar-sa",
    #                "Russo":"ro-mo"}

    #   idioma_selected = e.value 

    #   idioma = cd_idioma[idioma_selected]

    #   return idioma
    

    def traduzir(self):
    
        #detecta de qual lingua pertence essa frase
        print(self.__from_lang)

        #passa os parametros da linha que será traduzida para a que se quer traduzir
        s=Translator(from_lang=self.__from_lang, to_lang=self.__to_lang)

        #Corrigi a frase

        # objeto = ct.Corretor(self.__frase)

        # frase_corrigida = objeto.corrigir()

        # self.__frase = frase_corrigida

        #traduz a frase
        res = s.translate(self.__frase)
        print(s.from_lang, s.to_lang)
        #imprime a mensagem traduzida
        return res
        #passa os parametros para o audia...
   