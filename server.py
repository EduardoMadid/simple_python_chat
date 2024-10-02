import socket 
import threading

HOST = "127.0.0.1"
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

clients = []
nicknames = []

def broadcast(message:str):
    '''
    Envia para todos os clientes as mensagens
    '''
    for client in clients:
        client.send(message)
        

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f'{nicknames[clients.index(client)]} digitou {message}')
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break

def receive():
    '''
    Recebe as conexoes
    '''
    while True:
        client, address = server.accept()
        print(f"Conectado com {str(address)}\n")
        
        client.send("NICK".encode("utf-8"))
        nickname = client.recv(1024)

        nicknames.append(nickname)
        clients.append(client)
        
        print(f'Nickname: {nickname}\n')
        broadcast(f'{nickname} conectou ao servidor!\n'.encode('utf-8'))
        client.send("Conectado ao Servidor\n".encode("utf-8"))
        
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server iniciado...\n")

receive()


