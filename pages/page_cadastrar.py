import flet as ft
import time
import firebase_connection as fc
import sys
sys.path.insert(1, "./functions")

import f_audio as ad

def main(page):


    page.title = "EasyTalk"

    def go_to_login(e):
        page.route = "/"
        close_banner(e)
        page.update()
        
    nome = ft.TextField(
        label="Nome", 
        border_radius=15,
        color=ft.colors.BLACK,
        focused_border_color="#771AC9",
    )

    login = ft.TextField(
        label="E-mail", 
        border_radius=15,
        color=ft.colors.BLACK,
        focused_border_color="#771AC9",
    )

    password = ft.TextField(
        label="Senha", 
        border_radius=15,
        color=ft.colors.BLACK,
        focused_border_color="#771AC9",
        password=True,
        can_reveal_password=True
    )

    confirm_password = ft.TextField(
        label="Confirme sua senha", 
        border_radius=15,
        color=ft.colors.BLACK,
        focused_border_color="#771AC9",
        password=True,
        can_reveal_password=True
    )

    def close_banner(e):
        page.banner.open = False
        page.update()

    def show_banner(e):
        page.banner.open = True
        page.update()

    page.banner = ft.Banner(
        bgcolor="#dedcde",
        leading=ft.Icon(ft.icons.ERROR_OUTLINE,
                        color=ft.colors.RED, size=40),
        actions=[
            ft.TextButton(content=ft.Text("OK", color=ft.colors.BLACK), on_click=close_banner),
        ],
    )

    def cadastrar(e):

                    
        #Verifica se os campos estão devidamente preenchidos
        if nome.value == "" or login.value == "" or password.value == "" or confirm_password.value == "":
            msg = "Ainda há campos obrigatórios a serem preenchidos. Tente novamente."
            page.banner.content = ft.Text(msg, color=ft.colors.BLACK)
            show_banner(e)
            page.update()
        #Verifica se as senha coincidem 
        elif password.value != confirm_password.value:
            msg = "As senhas não coincidem."
            page.banner.content = ft.Text(msg, color=ft.colors.BLACK)
            show_banner(e)
            page.update()
        #Verifica se a senha possue o tamanho mínimo necessário
        elif password.value.__len__() < 6:
            msg = "A senha precisa ter no mínimo seis caracteres."
            page.banner.content = ft.Text(msg, color=ft.colors.BLACK)
            show_banner(e)
            page.update()
        else:
           try:
                email = login.value
                senha = password.value
                nome_usuario = nome.value
                #Realiza o cadastro do usuário
                user = fc.auth.create_user_with_email_and_password(email, senha)

                #Armazena o nome do usuário e email em um dictionary
                data = {'usuario': nome_usuario, 'email': email}

                #Adiciona os dados armazenados no Realtime Database do Firebase
                fc.db.child('user').push(data)

                #Envia uma confirmação de e-mail para o usuário
                fc.auth.send_email_verification(user['idToken'])

                nome.value = ""
                login.value = ""
                password.value = ""
                confirm_password.value = ""
                msg = "Tudo certo! Cadastro realizado com sucesso. Verifique sua conta a partir do link de confirmação enviado para você por e-mail."
                page.banner.leading = ft.Icon(ft.icons.CHECK_CIRCLE, color=ft.colors.GREEN, size=30)
                page.banner.content = ft.Text(msg, color=ft.colors.BLACK)
                page.banner.actions = [ft.TextButton(content=ft.Text("Fazer login", color=ft.colors.BLACK), on_click=go_to_login)]
                page.update()


           except:
                usuarios = fc.db.child('user').get()

                for usuario in usuarios.each():
                    #Caso o usuário possua um registro, é informado que o email já está cadastrado
                    if usuario.val()['email'] == login.value:
                        msg= "O e-mail informado já possui um cadastro."
                        page.banner.leading = ft.Icon(ft.icons.ERROR_OUTLINE, color=ft.colors.RED, size=40)
                        page.banner.content = ft.Text(msg, color=ft.colors.BLACK)
                        page.banner.actions = [ft.TextButton(content=ft.Text("Fazer login", color=ft.colors.BLACK), on_click=go_to_login)]
                        page.update()
                    else:
                        #Erro de Cadastro não Realizado
                        msg = "Erro ao cadastrar usuário, verifique as informações inseridas e tente novamente."
                        page.banner.leading = ft.Icon(ft.icons.ERROR_OUTLINE, color=ft.colors.RED, size=40)
                        page.banner.content = ft.Text(msg, color=ft.colors.BLACK)
                        page.banner.actions = [ft.TextButton(content=ft.Text("OK", color=ft.colors.BLACK), on_click=close_banner)]
                        page.update()

               

        show_banner(e) 
        ad.audiodescricao(msg)
        time.sleep(6)
        page.banner.open = False
        page.update()




    def btn_on_hover(e):
        e.control.bgcolor = ft.colors.PURPLE_800 if e.data == "true" else "#771AC9"
        e.control.update()


    btn_cadastrar = ft.ElevatedButton(
        "Cadastrar",
        width=1000,
        height=50,
        bgcolor="#771AC9",
        color=ft.colors.WHITE,
        on_hover=btn_on_hover,
        on_click=cadastrar
        )
    

    column_login = ft.Column(
        controls=[
            ft.Text("Cadastro", color=ft.colors.BLACK, font_family="Arial", weight="BOLD" ,size=35), 
            nome,
            login, 
            password,
            confirm_password,
            btn_cadastrar,
            ft.Column(controls=[
                ft.TextButton(content=ft.Text("Já tenho uma conta. Fazer login.", color="#771AC9"), on_click=go_to_login)
            ], spacing=5)
            
            ], 
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment="CENTER",
        spacing=10
    )


    container_cadastro = ft.Container(
        content=column_login, 
        bgcolor=ft.colors.WHITE,
        width=1000, 
        height=600, 
        border_radius=20,
        padding=50,

        
    )

    view = ft.View(
            "/page_cadastrar",
            [
                container_cadastro
            ],
            bgcolor="#771AC9",
            vertical_alignment="CENTER",
            horizontal_alignment="CENTER"

    )
    #page.views.append(view)
    page.update()
      
    return view

    

    
    
    
