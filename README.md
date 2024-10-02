# Simple GUI Chat em Python 🧑‍💻

O passo a passo de como fazer um ``chat`` simples em ``python`` 

<img src='https://camo.githubusercontent.com/0d0779a129f1dcf6c31613b701fe0646fd4e4d2ed2a7cbd61b27fd5514baa938/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f707974686f6e2d3336373041303f7374796c653d666f722d7468652d6261646765266c6f676f3d707974686f6e266c6f676f436f6c6f723d666664643534'>

# Índice
[importação-de-módulos](ola)




## SERVER SIDE ⚙️

### Importação de Módulos

O primeiro passo é importar as duas bibliotecas 'socket' e 'threading' (cuidado para não escrever errado).

```py
import socket 
import threading
```

- ``socket``: usado para criar conexões de rede;
- ``threading``: usado para lidar com múltiplas conexões de clientes simultaneamente.

### Definição do Host e Porta

```py
HOST = "127.0.0.1"
PORT = 9090
```

- ``HOST`` é o endereço IP do servidor. 127.0.0.1 refere-se ao ``localhost``, ou seja, o servidor está rodando na mesma máquina.
- ``PORT`` é o número da porta que o servidor usará para escutar as conexões dos clientes.

### Criação do Socket do Servidor

```py
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
```

- Aqui, estamos criando um socket do tipo ``TCP`` (usando ``SOCK_STREAM``), que é adequado para comunicação de fluxo, como um chat
- O método ``bind()`` associa o socket ao endereço e porta definidos anteriormente, permitindo que o servidor escute por conexões nesse endereço.
- Com isso, o servidor começa a escutar as conexões dos clientes. Ele espera até que um cliente tente se conectar.

### Listas para Clientes

```py
clients = []
nicknames = []
```

- ``clients`` é uma lista que armazenará os sockets dos clientes conectados.
- ``nicknames`` é uma lista que armazenará os nomes de usuário (nicknames) dos clientes.

### Função de Broadcast

```py
def broadcast(message: str):
    '''
    Envia para todos os clientes as mensagens
    '''
    for client in clients:
        client.send(message)
```

- Esta função recebe uma mensagem como argumento e a envia a todos os clientes conectados. O ``for`` percorre todos os clientes na lista e usa o método ``send()`` para enviar a mensagem

### Função de Manipulação de Cliente

```py
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
```
- Esta função lida com a comunicação de um cliente específico. Ela entra em um loop infinito (usando ``while True``), onde tenta receber mensagens do cliente.
  
Dentro do ``try:``
- ``client.recv(1024)`` recebe até 1024 bytes de dados enviados pelo cliente.
- Aqui, o servidor imprime no console qual cliente (usando seu nickname) enviou a mensagem. ``clients.index(client)`` encontra a posição do cliente na lista e ``nicknames[...]`` obtém o nickname correspondente.
- Após receber a mensagem, o servidor a retransmite para todos os clientes conectados chamando a função ``broadcast()``.

Dentro do ``except:``
- Se ocorrer um erro (como o cliente se desconectar), o código dentro do ``except`` é executado. Ele remove o cliente da lista de clientes, fecha a conexão ``(client.close())`` e remove o nickname associado.
- ``break`` sai do loop ``while True``, encerrando a manipulação desse cliente.

### Função de Recepção de Conexões

```py
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
```

- Esta função entra em um loop infinito para aceitar novas conexões de clientes.
  
Vamos ver essa função por partes
```py
client, address = server.accept()
print(f"Conectado com {str(address)}\n")
```
- O método ``accept()`` bloqueia até que um cliente tente se conectar retornando o socket do cliente (``client``) e o endereço (``address``) do cliente que se conectou.
- Imprime no console que um cliente se conectou e mostra o endereço do cliente.

```py
client.send("NICK".encode("utf-8"))
nickname = client.recv(1024)
```
- Envia a mensagem "NICK" para o cliente, pedindo que ele envie seu nome de usuário.
- O servidor espera e recebe o nickname do cliente, que deve ser enviado após a solicitação anterior.

```py
nicknames.append(nickname)
clients.append(client)
```
- Adiciona o nickname e o socket do cliente às listas ``nicknames`` e ``clients``, respectivamente.

```py
print(f'Nickname: {nickname}\n')
broadcast(f'{nickname} conectou ao servidor!\n'.encode('utf-8'))
client.send("Conectado ao Servidor\n".encode("utf-8"))
```
- Imprime o nickname do cliente no console.
- Envia uma mensagem a todos os outros clientes informando que um novo cliente se conectou.
- Envia uma mensagem ao cliente informando que ele está conectado ao servidor.

```py
thread = threading.Thread(target=handle, args=(client,))
thread.start()
```
- Cria um novo thread para chamar a função ``handle()`` para lidar com as mensagens desse cliente. Isso permite que o servidor continue aceitando novas conexões enquanto lida com a comunicação do cliente atual.

```py
print("Server iniciado...\n")
```
- Imprime no console que o servidor foi iniciado

```py
receive()
```
- Inicia o processo de escuta por novas conexões de clientes.

### Resumo
Este código cria um servidor básico de chat simples que aceita conexões de múltiplos clientes. Ele utiliza threads para permitir que cada cliente se comunique simultaneamente com o servidor. Quando um cliente se conecta, ele deve enviar um nickname, e todas as mensagens enviadas pelos clientes são retransmitidas para todos os outros clientes conectados.











