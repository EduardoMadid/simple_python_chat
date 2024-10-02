# Simple GUI Chat em Python 🧑‍💻

O passo a passo de como fazer um ``chat`` simples em ``python``!
Para utiliza-ló lembre sempre de rodar o servidor primeiro e depois rodar quantos clientes quiser!


***IMPORTANTE***

Isso funciona apenas localmente, já que utilizamos o localhost!

<img src='https://camo.githubusercontent.com/0d0779a129f1dcf6c31613b701fe0646fd4e4d2ed2a7cbd61b27fd5514baa938/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f707974686f6e2d3336373041303f7374796c653d666f722d7468652d6261646765266c6f676f3d707974686f6e266c6f676f436f6c6f723d666664643534'>

# Índice
- [Server](#server-side-%EF%B8%8F)
    - [Importação de módulos](#importação-de-módulos)
    - [Definição do Host e Porta](#definição-do-host-e-porta)
    - [Criação do Socket do servidor](#criação-do-socket-do-servidor)
    - [Listas para clientes](#listas-para-clientes)
    - [Função de broadcast](#função-de-broadcast)
    - [Função de manipulação de cliente](#função-de-manipulação-de-cliente)
    - [Função de recepção de conexões](#função-de-recepção-de-conexões)
    - [Resumo](#resumo)
- [Cliente](#client-side)
    - [Importação de módulos](#importação-de-módulos-1)
    - [Definição do Host e Porta](#definição-do-host-e-porta-1)
    - [Classe Client](#classe-client)
    - [Método Construtor](#método-construtor)
    - [Criação e Conexão do Socket](#criação-e-conexão-do-socket)
    - [Configuração da janela de diálogo](#configuração-da-janela-de-diálogo)
    - [Solicitação de nickname](#solicitação-de-nickname)
    - [Váriaveis de controle](#variáveis-de-controle)
    - [Criação de threads](#criação-de-threads)
    - [Início das threads](#início-das-threads)
    - [Método da interface gráfica](#método-da-interface-gráfica)
    - [Criação da janela principal](#criação-da-janela-principal)
    - [Configuração do rótulo chat](#configuração-do-rótulo-do-chat)
    - [Área de texto com rolagem](#área-de-texto-com-rolagem)
    - [Configuração do rótulo da mensagem](#configuração-do-rótulo-da-mensagem)
    - [Área de texto de entrada](#área-de-texto-de-entrada)
    - [Botão de envio](#botão-de-envio)
    - [Indicador de que a GUI foi inicicializada](#indica-que-a-gui-foi-inicializada)
    - [Tratamento de fechamento da janela](#tratamento-de-fechamento-da-janela)
    - [Loop principal da GUI](#loop-principal-da-gui)
    - [Método de envio de mensagens](#método-de-envio-de-mensagens)
    - [Criação da mensagem](#criação-da-mensagem)
    - [Envio da mensagem](#envio-da-mensagem)
    - [Limpeza da área de entrada](#limpeza-da-área-de-entrada)
    - [Método para parar o cliente](#método-para-parar-o-cliente)
    - [Finalização do cliente](#finalização-do-cliente)
    - [Método de recepção de mensagens](#método-de-recepção-de-mensagens)
    - [Loop de recepção](#loop-de-recepção)
    - [Recebendo mensagens](#recebendo-mensagens)
    - [Tratamento de erros de conexão](#tratamento-de-erros-de-conexão)
    - [Tratamento geral de erros](#tratamento-geral-de-erros)
    - [Instanciação do cliente](#instanciação-do-cliente)

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

## Client Side 💻

### Importação de Módulos

```py
import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog
```
- ``socket``: para criar a conexão de rede.
- ``threading``: para lidar com múltiplas threads (conexões simultâneas).
- ``tkinter``: biblioteca padrão do Python para criar interfaces gráficas.
- ``tkinter.scrolledtext``: um widget para uma área de texto com barra de rolagem.
- ``simpledialog``: para abrir uma janela de diálogo simples onde o usuário pode inserir texto.

### Definição do Host e Porta

```py
HOST = "127.0.0.1"
PORT = 9090
```

- ``HOST`` é o endereço IP do servidor. 127.0.0.1 refere-se ao ``localhost``, ou seja, o servidor está rodando na mesma máquina.
- ``PORT`` é o número da porta que o servidor usará para escutar as conexões dos clientes.

### Classe Client

```py
class Client:
    
    def __init__(self, host, port):
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host,port))
        
        msg = tkinter.Tk()
        msg.withdraw()
        
        self.nickname = simpledialog.askstring("Nickname", "Escolha seu nickname", parent=msg)
        
        self.gui_done = False
        self.running = True
        
        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)
        
        gui_thread.start()
        receive_thread.start()
        
    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.configure(bg="lightgray")
        
        self.chat_label = tkinter.Label(self.win, text="Chat", bg="lightgray")
        self.chat_label.config(font=("Arial", 12))
        self.chat_label.pack(padx=20, pady=5)
        
        self.text_area = tkinter.scrolledtext.ScrolledText(self.win,  height=10, width=50)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disabled')
        
        self.msg_label = tkinter.Label(self.win, text="MESSAGE", bg="lightgray")
        self.msg_label.config(font=("Arial", 12))
        self.msg_label.pack(padx=20, pady=5)
        
        self.input_area  = tkinter.Text(self.win, height=3, width=50)
        self.input_area.pack(padx=20, pady=5)
        
        
        self.send_button = tkinter.Button(self.win, text="ENVIAR", command=self.write)
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx=20, pady=5)
        
        self.gui_done = True
        
        self.win.protocol("WN_DELETE_WINDOW", self.stop)
        
        self.win.mainloop()
    
    def write(self):
        message = (f'{self.nickname}: {self.input_area.get('1.0', 'end')}')
        self.sock.send(message.encode("utf-8"))
        self.input_area.delete('1.0','end')
    
    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)
    
    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message == "NICK":
                    self.sock.send(self.nickname.encode("utf-8"))
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', message)
                        self.text_area.yview("end")
                        self.text_area.config(state='disabled')
            except ConnectionAbortedError:
                break
            except:
                print("ERROR")
                self.sock.close()
                break
```
- Cria uma classe chamada ``Client`` que encapsula a lógica do cliente.
Vamos nos aprofundar mais em cada etapa dessa classe.

### Método Construtor

```py
def __init__(self, host, port):
```
- Inicializa a classe com os parâmetros ``host`` e ``port``.

### Criação e Conexão do Socket

```py
self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
self.sock.connect((host,port))
```
- Cria um socket TCP e conecta-se ao servidor usando o endereço e a porta fornecidos.

### Configuração da Janela de Diálogo

```py
msg = tkinter.Tk()
msg.withdraw()
```
- Cria uma instância de uma janela Tkinter e a oculta (``withdraw()``) para não aparecer na tela, pois usaremos apenas o diálogo.

### Solicitação de Nickname

```py
self.nickname = simpledialog.askstring("Nickname", "Escolha seu nickname", parent=msg)
```
- Abre uma caixa de diálogo simples para o usuário inserir seu nickname. O resultado é armazenado em ``self.nickname``.

### Variáveis de Controle

```py
self.gui_done = False
self.running = True
```
- ``self.gui_done``: um indicador para verificar se a GUI foi inicializada.
- ``self.running``: um indicador para controlar o loop principal do cliente.

### Criação de Threads

```py
gui_thread = threading.Thread(target=self.gui_loop)
receive_thread = threading.Thread(target=self.receive)
```
- Cria duas threads: uma para a interface gráfica (``gui_loop``) e outra para receber mensagens do servidor (``receive``)

### Início das Threads

```py
gui_thread.start()
receive_thread.start()
```
- Inicia as threads criadas anteriormente, permitindo que a GUI e o recebimento de mensagens ocorram simultaneamente.

### Método da Interface Gráfica

```py
def gui_loop(self):
```
- Define o método que configura e gerencia a interface gráfica do usuário (GUI)

### Criação da Janela Principal

```py
self.win = tkinter.Tk()
self.win.configure(bg="lightgray")
```
- Cria uma nova janela Tkinter e define a cor de fundo como cinza claro.

### Configuração do Rótulo do Chat

```py
self.chat_label = tkinter.Label(self.win, text="Chat", bg="lightgray")
self.chat_label.config(font=("Arial", 12))
self.chat_label.pack(padx=20, pady=5)
```
- Cria um rótulo na janela com o texto "Chat", configura a fonte e empacota (adiciona) o rótulo à janela com margens.

### Área de Texto com Rolagem

```py
self.text_area = tkinter.scrolledtext.ScrolledText(self.win,  height=10, width=50)
self.text_area.pack(padx=20, pady=5)
self.text_area.config(state='disabled')
```
- Cria uma área de texto com barra de rolagem, define seu tamanho e a empacota na janela. Inicialmente, a área de texto é configurada como desabilitada para que não possa ser editada pelo usuário

### Configuração do Rótulo da Mensagem

```py
self.msg_label = tkinter.Label(self.win, text="MESSAGE", bg="lightgray")
self.msg_label.config(font=("Arial", 12))
self.msg_label.pack(padx=20, pady=5)
```
- Cria um rótulo com o texto "MESSAGE", configura a fonte e empacota na janela.

### Área de Texto de Entrada

```py
self.input_area  = tkinter.Text(self.win, height=3, width=50)
self.input_area.pack(padx=20, pady=5)
```
- Cria uma área de texto onde o usuário pode digitar suas mensagens, define seu tamanho e a empacota na janela.

### Botão de Envio

```py
self.send_button = tkinter.Button(self.win, text="ENVIAR", command=self.write)
self.send_button.config(font=("Arial", 12))
self.send_button.pack(padx=20, pady=5)
```
- Cria um botão com o texto "ENVIAR" e define o comando ``self.write`` para ser chamado quando o botão for clicado. O botão é empacotado na janela.

### Indica que a GUI foi Inicializada

```py
self.gui_done = True
```
- Define ``self.gui_done`` como verdadeiro, indicando que a interface gráfica está pronta.

### Tratamento de Fechamento da Janela

```py
self.win.protocol("WM_DELETE_WINDOW", self.stop)
```
- Define o comportamento da janela ao ser fechada para chamar o método ``stop()``, que encerra o cliente.

### Loop Principal da GUI

```py
self.win.mainloop()
```
- Inicia o loop principal da interface gráfica, que permite que a janela permaneça aberta e interativa.

### Método de Envio de Mensagens

```py
def write(self):
```
- Define o método que será chamado quando o botão "ENVIAR" for clicado.

### Criação da Mensagem

```py
message = (f'{self.nickname}: {self.input_area.get("1.0", "end")}')
```
- Cria a mensagem concatenando o nickname do usuário e o texto que foi inserido na área de entrada.

### Envio da Mensagem

```py
self.sock.send(message.encode("utf-8"))
```
- Codifica a mensagem como UTF-8 e a envia para o servidor através do socket.

### Limpeza da Área de Entrada

```py
self.input_area.delete('1.0','end')
```
- Limpa o texto na área de entrada após o envio da mensagem

### Método para Parar o Cliente

```py
def stop(self):
```
- Define o método que será chamado quando o cliente precisar ser encerrado.

### Finalização do Cliente

```py
self.running = False
self.win.destroy()
self.sock.close()
exit(0)
```
- Define ``self.running`` como falso para sair do loop de recebimento, destrói a janela da GUI, fecha o socket e encerra o programa.

### Método de Recepção de Mensagens

```py
def receive(self):
```
- Define o método que será responsável por receber mensagens do servidor.

### Loop de Recepção

```py
while self.running:
```
- Inicia um loop que continua enquanto ``self.running`` for verdadeiro.

### Recebendo Mensagens

```py
try:
    message = self.sock.recv(1024).decode('utf-8')
    if message == "NICK":
        self.sock.send(self.nickname.encode("utf-8"))
    else:
        if self.gui_done:
            self.text_area.config(state='normal')
            self.text_area.insert('end', message)
            self.text_area.yview("end")
            self.text_area.config(state='disabled')
```
- Dentro do bloco ``try``, tenta receber uma mensagem do servidor e a decodifica de bytes para string.
- Se a mensagem recebida for "NICK", o cliente envia seu nickname de volta ao servidor.
- Se a mensagem não for "NICK" e a GUI estiver pronta (self.gui_done), o código:
    - Altera a área de texto para o estado 'normal' (para permitir edição).
    - Insere a mensagem no final da área de texto.
    - Ajusta a visualização para mostrar a última mensagem inserida.
    - E finalmente, define a área de texto como 'disabled' novamente para evitar edição.

 ### Tratamento de Erros de Conexão

 ```py
except ConnectionAbortedError:
    break
```
- Se ocorrer um erro de conexão, o loop é encerrado.

### Tratamento Geral de Erros

```py
except:
    print("ERROR")
    self.sock.close()
    break
```
- Para qualquer outro erro, imprime uma mensagem de erro, fecha o socket e sai do loop.

### Instanciação do Cliente

```py
client = Client(HOST, PORT)
```
- Cria uma nova instância da classe ``Client``, passando o ``HOST`` e o ``PORT`` definidos anteriormente.

### Resumo
Essa estrutura do cliente de chat é baseada em sockets e usa uma interface gráfica simples para permitir que os usuários se comuniquem em tempo real. O uso de threads permite que o cliente continue recebendo mensagens enquanto o usuário interage com a GUI.
