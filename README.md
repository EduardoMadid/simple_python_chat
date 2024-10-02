# Simple GUI Chat em Python

O passo a passo de como fazer um ``chat`` simples em ``python`` 

## SERVER SIDE

O primeiro passo é importar as duas bibliotecas 'socket' e 'threading' (cuidado para não escrever errado).

```py
import socket 
import threading
```

- ``socket``: usado para criar conexões de rede;
- ``threading``: usado para lidar com múltiplas conexões de clientes simultaneamente.

# 

```py
HOST = "127.0.0.1"
PORT = 9090
```

- ``HOST`` é o endereço IP do servidor. 127.0.0.1 refere-se ao ``localhost``, ou seja, o servidor está rodando na mesma máquina.
- ``PORT`` é o número da porta que o servidor usará para escutar as conexões dos clientes.

#

```py
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
```

- Aqui, estamos criando um socket do tipo ``TCP`` (usando ``SOCK_STREAM``), que é adequado para comunicação de fluxo, como um chat
- O método ``bind()`` associa o socket ao endereço e porta definidos anteriormente, permitindo que o servidor escute por conexões nesse endereço.
- Com isso, o servidor começa a escutar as conexões dos clientes. Ele espera até que um cliente tente se conectar.
