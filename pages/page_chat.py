import flet as ft
import socket 
import threading
import time


import sys

from flet_core.connection import Connection

sys.path.insert(1, "./functions")

sys.path.insert(2, "./functions")

sys.path.insert(3, "./functions")

sys.path.insert(4, "./functions")

sys.path.insert(5, "./functions")

sys.path.insert(6, "./functions")


import users as us
import f_tradutor as td
import f_audio as ad
import f_transcricao as tr
import f_corretor as ct
import image as img

HOST = '192.168.150.51'
PORT = 8080

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

class Message:
    def __init__(self, text, sender):
        self.text = text
        self.sender = sender

class ChatApp(ft.UserControl):
    # ... (código do ChatApp aqui) ...
    def __init__(self, page:ft.Page):
        super().__init__()
        self.messages = []
        self.selected_message = None
        self.sent_messages = []
        self.msg_temporaria = []
        self.page = page
    
    def build(self):
        self.message_list = ft.Column()
        self.new_message = ft.TextField(label="Escreva uma mensagem", width=500,  border_radius=15,
        color=ft.colors.BLACK,
        border='NONE',
        on_focus=txt_on_focus,
        on_blur=txt_on_blur,
        on_submit=self.send_message,
        on_change=self.multiline,
        multiline=False,
        height=50,
        )
        pick_files_dialog = ft.FilePicker(on_result=self.pick_files_result)
        self.send_button = ft.IconButton(icon=ft.icons.SEND_ROUNDED, icon_color="#771AC9",on_click=self.send_message)
        transcribe_msg = ft.IconButton(icon=ft.icons.MIC, icon_color="#771AC9",on_click=self.transcrever)
        transcribe_img = ft.IconButton(icon=ft.icons.IMAGE_SEARCH, icon_color="#771AC9", on_click=lambda _: pick_files_dialog.pick_files(allow_multiple=True, file_type= ft.FilePickerFileType.IMAGE))
        self.page.overlay.append(pick_files_dialog)
        if self.page.height < 710:
           self.chat = ft.Column(height=550, scroll=ft.ScrollMode.ALWAYS)
        else:
           self.chat = ft.Column(height=650, scroll=ft.ScrollMode.ALWAYS) 
        #self.chat = ft.Container(height=550, scroll=ft.ScrollMode.ALWAYS,)
        icones = ft.Row(controls=[transcribe_img, transcribe_msg, self.send_button], alignment=ft.MainAxisAlignment.END)
        column_send_message = ft.Column(
        controls=[
            ft.Row(controls=[self.new_message, icones], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ],
        alignment=ft.MainAxisAlignment.CENTER
        )
        container_send_message = ft.Container(
        content=column_send_message, 
        bgcolor=ft.colors.WHITE, 
        width=1500, 
        height=70,  
        border_radius=15
        )
        container_send_message.padding = ft.padding.only(left=20)
        column_chat = ft.Column(
        controls=[
            self.chat,
            container_send_message],
            alignment=ft.MainAxisAlignment.END,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
            expand=True,
        )
        new_chat = ft.TextField(label="Pesquise ou inicie uma nova conversa",
                             color=ft.colors.WHITE,
                            border='NONE',
                            width=380,
                            on_focus=txt_on_focus)

        search = ft.IconButton(icon=ft.icons.SEARCH, icon_color=ft.colors.WHITE)

        column_search_chat = ft.Column(
        controls=[
            ft.Row(controls=[new_chat, search], alignment="CENTER"),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    
        container_search_chat = ft.Container(
        content=column_search_chat, 
        bgcolor="#771AC9", 
        width=450, 
        height=60,  
        border_radius=15
        )
    
        rail = ft.NavigationRail(
        label_type=ft.NavigationRailLabelType.ALL,
        #extended=True,
        #height=700,
        expand=True,
        min_width=500,
        min_extended_width=400,
        leading=container_search_chat,
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(

            ),
        ],
        bgcolor=ft.colors.WHITE
        )

        container = ft.Container(content=rail, border_radius=15)
   
        linha = ft.Row(
        controls=[
            container,
            column_chat
        ],
        expand=True,
        width=self.page.window_max_width,
        )
        
        view = ft.View(controls=[linha], bgcolor="#771AC9", vertical_alignment='END', horizontal_alignment="CENTER")
        
        return view

    def send_message(self, event):
        message_text = self.new_message.value
        message = Message(message_text, 'DESTINATARIO')
        self.sent_messages.append(message)
        self.messages.append(message)
        self.add_message_to_ui('',message)
        self.send_message_to_socket(message_text)
        self.new_message.value = ""

    def add_message_to_ui(self, user, message):
        message_text = message.text
        if message.sender == 'DESTINATARIO':
           print(message_text)
        #edit_button = ft.ElevatedButton(text="Editar", on_click=lambda event, msg=message: self.edit_message(event, msg))
           message_text = ft.Column(controls=[ft.Text(message.text, size=30, text_align=ft.CrossAxisAlignment.END, color=ft.colors.BLACK, no_wrap=False)])
           if message.text.__len__() >= 24:
              message_text.width = 350
           else:
              message_text.height = 50  
              self.page.update()

           self.chat.controls.append(
                ft.Row(
                    controls=[
                                ft.Container(content=message_text, bgcolor=ft.colors.WHITE, border_radius=10, padding=10)
                            ],                         
                            width = 1500, 
                            alignment=ft.MainAxisAlignment.END,
                            vertical_alignment=ft.MainAxisAlignment.END
                )
            )
           self.chat.auto_scroll = True
           self.new_message.value = " "
           self.page.update()
        else:
            message_text = ft.Text(message.text, size=30, text_align=ft.CrossAxisAlignment.END, color=ft.colors.BLACK)
            clm_message = ft.Column(controls=[  
                ft.Row(controls=[ft.CircleAvatar(bgcolor=ft.colors.PURPLE), ft.Text(user, color=ft.colors.BLACK, weight="bold")]),
                message_text,
                ft.Row(controls=[ft.IconButton(icon=ft.icons.TRANSLATE, icon_color="#771AC9", on_click=lambda event, msg=message: self.traduzir(event, msg)), 
                                 ft.IconButton(icon=ft.icons.MULTITRACK_AUDIO, icon_color="#771AC9", on_click=lambda event, msg=message: self.ouvir(event, msg))])])
            if message.text.__len__() >= 26:
                message_text.width = 400
                self.page.update()
    
            container_msg = ft.Container(content=clm_message, bgcolor=ft.colors.WHITE, border_radius=10, padding=10, expand=False)
            self.chat.controls.append(
                ft.Row(
                    controls=[
                                container_msg
                            ],
                         
                            width = 1500, 
                            alignment=ft.MainAxisAlignment.START,
                )
            )
            self.msg_temporaria.append(message_text)
            self.chat.auto_scroll = True
            self.page.update()

    def focus_msg(self):
        return self.new_message
    
    def traduzir(self, event, message):
        self.selected_message = message
        traducao = td.Tradutor(message.text)
        msg_traduzida = traducao.traduzir()
        print(msg_traduzida)
        for txt in self.msg_temporaria:
           if txt.value == message.text:
              txt.value = msg_traduzida
              self.page.update()
              time.sleep(10)
              txt.value = message.text
              self.page.update()
        #self.new_message.value = msg_traduzida
        #self.msg_temporaria.value = msg_traduzida
        # self.update()
        # time.sleep(10)
        # event.value = message.text
        #self.msg_temporaria.value = message.text
        #self.new_message.value = message.text
        
        
    def ouvir(self, event, message):
        self.selected_message = message
        msg = message.text
        #corretor = ct.Corretor(msg)
        #msg_corrigida = corretor.corrigir()
        ad.audiodescricao(msg)
        self.page.update()


    def send_message_to_socket(self, message_text):
        # Substitua 'HOST' e 'PORT' com os detalhes de conexão do seu servidor
        #sem user do login
        user = us.User.getUser()
        client_socket.send( (user+ ": "+message_text).encode('utf-8'))
        #client_socket.send(message_text.encode('utf-8'))
         #   s.sendall(message_text.encode())

    def update_ui(self):
        self.message_list.controls.clear()
        
        for message in self.messages:
            self.user = message.text[0]
            msg = message.text[1]
            message_text = ft.Text(msg, size=30, text_align=ft.CrossAxisAlignment.END, color=ft.colors.BLACK)
            clm_message = ft.Column(controls=[  
                ft.Row(controls=[ft.CircleAvatar(bgcolor=ft.colors.PURPLE), ft.Text(self.user, color=ft.colors.BLACK, weight="bold")]),
                message_text,
                ft.Row(controls=[ft.IconButton(icon=ft.icons.TRANSLATE, icon_color="#771AC9", on_click=lambda event, msg=message: self.traduzir(event, msg)), 
                                 ft.IconButton(icon=ft.icons.MULTITRACK_AUDIO, icon_color="#771AC9", on_click=lambda event, msg=message: self.ouvir(event, msg))])])
            container_msg = ft.Container(content=clm_message, bgcolor=ft.colors.BLUE, border_radius=10, padding=10)
            self.message_list.controls.append(container_msg)
            self.msg_temporaria.append(message_text)
            self.page.update()
            

    def transcrever(self, e):
        
        try:
            msg_transcrita = tr.transcrever()
            self.new_message.label = ""
            self.new_message.value = msg_transcrita
            self.send_message(e)
            self.page.update()
        except:
            msg_error = "Não conseguimos te escutar. Verifique se o seu microfone está funcionando perfeitamente e tente novamente."
            self.page.banner.leading = ft.Icon(ft.icons.ERROR_OUTLINE, color=ft.colors.RED, size=40)
            self.page.banner.content = ft.Text(msg_error, color=ft.colors.BLACK)
            self.page.banner.actions = [ft.TextButton(content=ft.Text("OK", color=ft.colors.BLACK), on_click=self.close_banner)]
            self.show_banner(e)
            ad.audiodescricao(msg_error)
            self.page.update()
            time.sleep(10)
            self.page.banner.open = False
            self.page.update()

    def close_banner(self, event):
        self.page.banner.open = False
        self.page.update()

    def show_banner(self, event):
        self.page.banner.open = True
        self.page.update()
    def multiline(self, event):

        if self.new_message.value.__len__() >= 64:
           self.new_message.multiline = True
           self.new_message.height = 70
        else:
           self.new_message.multiline = False
           self.new_message.height = 50

        self.page.update()


    def pick_files_result(self, e: ft.FilePickerResultEvent):
        
        try:
            caminho =  (
              ", ".join(map(lambda f: f.path, e.files)) if e.files else "Cancelled!"
                );
            
            if img.camImagem(caminho) != '':
               self.new_message.label = ""
               self.new_message.value = img.camImagem(caminho)
               self.send_message(e)
            #self.multiline(e)
               self.page.update()
               ad.audiodescricao(img.camImagem(caminho))
            else:
                msg_error = "Verifique se a imagem selecionada contém um texto."
                self.page.banner = ft.Banner(leading= ft.Icon(ft.icons.ERROR_OUTLINE, color=ft.colors.RED, size=40),
                                  content = ft.Text(msg_error, color=ft.colors.BLACK),
                                  actions = [ft.TextButton(content=ft.Text("OK", color=ft.colors.BLACK), on_click=self.close_banner)])
                self.show_banner(e)
                ad.audiodescricao(msg_error)
                self.page.update()
                time.sleep(10)
                self.page.banner.open = False
                self.page.banner.update()
        except Exception as err:
            print(err)
            msg_error = "Não conseguimos ler a imagem selecionada. Verifique se o arquivo não está corrompido ou se a imagem está nítida o suficiente."
            self.page.banner = ft.Banner(leading= ft.Icon(ft.icons.ERROR_OUTLINE, color=ft.colors.RED, size=40),
                                  content = ft.Text(msg_error, color=ft.colors.BLACK),
                                  actions = [ft.TextButton(content=ft.Text("OK", color=ft.colors.BLACK), on_click=self.close_banner)])
            self.show_banner(e)
            ad.audiodescricao(msg_error)
            self.page.update()
            time.sleep(10)
            self.page.banner.open = False
            self.page.banner.update()


def txt_on_focus(e):
    e.control.label = "" 
    e.control.update()

def txt_on_blur(e):
    e.control.label = "Escreva uma mensagem" 
    e.control.update()

def receive_messages(usuario_socket, chat_app):
    while True:
        try:
            message_recebida = usuario_socket.recv(1024).decode('utf-8')
            msg = message_recebida.split(":")
            user = msg[0]
            n_msg = msg[1]
            mensagem_exibida = msg
            print(user[0])
            print('recebe:', mensagem_exibida)
            
            if message_recebida not in chat_app.sent_messages:
                    message = Message(n_msg, 'REMETENTE')
                    chat_app.messages.append(message)
                    chat_app.add_message_to_ui(user, message)

        except Exception as e:
            print(e)
            usuario_socket.close()
            break


def main(page: ft.Page):

    chat_app = ChatApp(page)
    page.views.append(chat_app.build())
    page.update()
    bem_vindo = "Olá "+us.User.getUser()+" você acabou de entrar no chat, aproveite para explorar todas as funcionalidades que ele oferece!"
    ad.audiodescricao(bem_vindo)
    msg = chat_app.focus_msg()
    msg.focus()
    try:
       print('aquii')
       receive_messages(client_socket, chat_app)
       page.update()
    except Exception as e:
          #traceback.print_exc()
        print(e)
        receive_messages(client_socket, chat_app)
    
    

#ft.app(main, assets_dir="assets")
    return chat_app
