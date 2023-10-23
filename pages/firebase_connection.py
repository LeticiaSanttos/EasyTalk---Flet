
#Biblioteca para usar o Firebase com python
import pyrebase

#Conexão com o Firebase
firebaseConfig = {
    "apiKey": "AIzaSyBmlnkLE8ddvIn4LFD8Yq6JZsEj2DJqDgE",
    "authDomain": "tcc---chat-de-mensagens.firebaseapp.com",
    "projectId": "tcc---chat-de-mensagens",
    "storageBucket": "tcc---chat-de-mensagens.appspot.com",
    "messagingSenderId": "35064349027",
    "appId": "1:35064349027:web:87664124ef9f7ac6119356",
    "measurementId": "G-S4TYL3DE57",
    "databaseURL": "https://tcc---chat-de-mensagens-default-rtdb.firebaseio.com"
}

#Inicia a conexão com o Firebase 
firebase = pyrebase.initialize_app(firebaseConfig)

#Istancia uma variável para usar os métodos de autentificação
auth = firebase.auth()

#Istancia uma variável para usar o Realtime Database do Firebase
db = firebase.database()

auth.languageCode = 'pt'