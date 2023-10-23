import language_tool_python
from langdetect import detect

class Corretor():

    def __init__(self, frase):
        self.__frase = frase
        idioma = detect(frase)
        if idioma == 'cy':
            idioma = 'pt'
            
        self.tool = language_tool_python.LanguageToolPublicAPI()


    def corrigir(self):
        # Verificação e correção da entrada do usuário
        self.__correcao = self.tool.correct(self.__frase)
        print(self.__frase)
        print(self.__correcao)
        
        return self.__correcao