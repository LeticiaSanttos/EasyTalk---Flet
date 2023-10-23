import socket
import threading

HOST = '0.0.0.0'
PORT = 8080
usuarios = []

def broadcast(message, usuario_socket):
    for client in usuarios:
        if client != usuario_socket:
            try:
                client.send(message)
            except:
        
                client.close()
                remove(client)

def remove(usuario_socket):
    if usuario_socket in usuarios:
        usuarios.remove(usuario_socket)

def handle_client(usuario_socket):
    while True:
        try:
            message = usuario_socket.recv(1024)
            if not message:
              
                remove(usuario_socket)
                break
            else:
               
                broadcast(message, usuario_socket)
        except:
            continue


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
# Aqui é a parte de informar a conexão no servidor
print(f"Servidor conectado:{HOST}:{PORT}")

while True:
    usuario_socket, client_address = server.accept()
    usuarios.append(usuario_socket)
    print(f"Para a conexão {client_address}")
    client_handler = threading.Thread(target=handle_client, args=(usuario_socket,))
    client_handler.start()

    