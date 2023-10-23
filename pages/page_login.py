import flet as ft
import page_cadastrar
import page_chat
import sys
import firebase_connection as fc
import time

sys.path.insert(1, "./functions")
sys.path.insert(2, "./functions")


import users as us
import f_audio as ad


def main(page: ft.Page):

    page.title = "EasyTalk"
    
    bem_vindo = ("Seja bem vindo ao EasyTalk! Para acessar o nosso aplicativo de mensagens com funcionalidades exclusivas"
    +"faça o seu login primeiro. Caso ainda não tenha um, realize seu cadastro.")
    

    def go_to_cadastrar(e):
        page.route = "/page_cadastrar"
        page.update()

    def go_to_chat(e):
        page.route = "/page_chat"
        page.update()
    

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

    def btn_on_hover(e):
        e.control.bgcolor = ft.colors.PURPLE_800 if e.data == "true" else "#771AC9"
        e.control.update()

    def click_login(e):
        email = login.value.strip()
        senha = password.value
        try:
            #Realiza o login do usuário
            user = fc.auth.sign_in_with_email_and_password(email, senha)

            #Pega as informações do usuário
            accountInfo = fc.auth.get_account_info(user['idToken'])

            #Armazena o valor 'emailVerified' como True ou False
            emailVerified = accountInfo['users'][0]['emailVerified']

            if emailVerified:

                #Adiciona todos os usuários do banco de dados em um array
                usuarios = fc.db.child('user').get()

                #Realiza uma busca em todos os usuário que estão no banco de dados 
                for usuario in usuarios.each():
                    #Caso o usuário possua um registro, é puxado o nome que aparecerá no chat
                    if usuario.val()['email'] == email:
                        nome_usuario = usuario.val()['usuario']



                        us.User.setUser(nome_usuario)

                go_to_chat(e)
                page.update()
            else:
                msg_error = "Esse e-mail não foi verificado. Para entrar no EasyTalk é necessário confirmar sua conta a partir do link enviado para você por e-mail."
                page.banner.leading = ft.Icon(ft.icons.ERROR_OUTLINE, color=ft.colors.RED, size=40)
                page.banner.content = ft.Text(msg_error, color=ft.colors.BLACK)
                page.banner.actions = [ft.TextButton(content=ft.Text("OK", color=ft.colors.BLACK), on_click=close_banner)]
                show_banner(e)
                ad.audiodescricao(msg_error)
                time.sleep(10)
                page.banner.open = False
                page.update()

        except:
            #Erro de Login não realizado
            login.value = ""
            password.value = ""
            msg_error = "E-mail ou senha incorretos."
            page.banner.leading = ft.Icon(ft.icons.ERROR_OUTLINE, color=ft.colors.RED, size=40)
            page.banner.content = ft.Text(msg_error, color=ft.colors.BLACK)
            page.banner.actions = [ft.TextButton(content=ft.Text("OK", color=ft.colors.BLACK), on_click=close_banner)]
            show_banner(e) 
            ad.audiodescricao(msg_error)
            time.sleep(6)
            page.banner.open = False
            page.update()

    btn_login = ft.ElevatedButton(
        "Continuar",
        width=1000,
        height=50,
        bgcolor="#771AC9",
        color=ft.colors.WHITE,
        on_hover=btn_on_hover,
        on_click=click_login
        )
    
    def resetPassword(e):
        email = login.value.strip
        usuarios = fc.db.child('user').get()

        for usuario in usuarios.each():
            #Caso o usuário possua um registro, é possível resetar a senha
            if usuario.val()['email'] == email:

                try:

                   
                    fc.auth.send_password_reset_email(email)
                    msg_error = "E-mail de redefinição de senha enviado com sucesso."
                    page.banner.leading = ft.Icon(ft.icons.CHECK_CIRCLE, color=ft.colors.GREEN, size=30)
                    page.banner.content = ft.Text(msg_error, color=ft.colors.BLACK)
                    page.banner.actions = [ft.TextButton(content=ft.Text("OK", color=ft.colors.BLACK), on_click=close_banner)]
                    ad.audiodescricao(msg_error)
                    page.update()

                except:
                    msg_error = "Falha ao enviar o e-mail de redefinição de senha."
                    page.banner.leading = ft.Icon(ft.icons.ERROR_OUTLINE, color=ft.colors.RED, size=40)
                    page.banner.content = ft.Text(msg_error, color=ft.colors.BLACK)
                    page.banner.actions = [ft.TextButton(content=ft.Text("OK", color=ft.colors.BLACK), on_click=close_banner)]
                    ad.audiodescricao(msg_error)

                    page.update()

            elif usuario.val()['email'] != email or email == "":
                page.banner.leading = ft.Icon(ft.icons.ERROR_OUTLINE, color=ft.colors.RED, size=40)
                page.banner.content = ft.Text("O e-mail informado não possui um cadastro.", color=ft.colors.BLACK)
                page.banner.actions = [ft.TextButton(content=ft.Text("OK", color=ft.colors.BLACK), on_click=close_banner)]

                page.update()

        show_banner(e) 
        time.sleep(6)
        page.banner.open = False
        page.update()
                    

    

    column_login = ft.Column(
        controls=[
            ft.Text("Login", color=ft.colors.BLACK, font_family="Arial", weight="BOLD" ,size=35), 
            login, 
            password,
            btn_login,
            ft.Column(controls=[
                ft.TextButton(content=ft.Text("Esqueci minha senha", color="#771AC9"), on_click=resetPassword),
                ft.TextButton(content=ft.Text("Não possuo cadastro", color="#771AC9"), on_click=go_to_cadastrar)
            ], spacing=5)
            
            ], 
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment="CENTER",
        spacing=10
    )


    container_login = ft.Container(
        content=column_login, 
        bgcolor=ft.colors.WHITE,
        width=1000, 
        height=600, 
        border_radius=20,
        padding=50,

        
    )

    page.update() 

    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    container_login
                ],
                bgcolor="#771AC9",
                vertical_alignment="CENTER",
                horizontal_alignment="CENTER",
            )
        )
        if page.route == "/page_cadastrar":
            page.views.append(
                page_cadastrar.main(page)
            )
        if page.route == "/page_chat":
            page.views.append(
                page_chat.main(page)
            )

        page.update()
        login.focus()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)
    
    ad.audiodescricao(bem_vindo)

ft.app(main, assets_dir="assets")