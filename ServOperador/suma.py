import socket
import marshal
import os
from _thread import *

ServerSocket = socket.socket()
h_name = socket.gethostname()
host = socket.gethostbyname(h_name)
print("host =" + host)
port = 1234
ThreadCount = 0


def stablish_conection_with_NS():
    ClientSocket = socket.socket()
    hostNS = '192.168.56.1'
    portNS = 1233

    print('Esperando conexión con NS')
    try:
        ClientSocket.connect((hostNS, portNS))
    except socket.error as e:
        print(str(e))

    # Enviar
    ClientSocket.send(("Servidor Operador").encode())

    # Aceptar
    response = ClientSocket.recv(1024)
    print('NS dice:', end=" ")
    print(response.decode())

    # Enviar
    data = ('+', host, port)
    serializados = marshal.dumps(data)
    ClientSocket.send(serializados)

    # Aceptar
    response = ClientSocket.recv(1024)
    print('NS dice:', end=" ")
    print(response.decode())
    ClientSocket.close()


def threaded_client(connection):
    #connection.send(str.encode('Operación de suma.'))
    data = connection.recv(1024)
    deserializados = marshal.loads(data)

    suma = 0
    for d in deserializados:
        suma += d

    if data:
        connection.send(str(suma).encode())
    connection.close()


stablish_conection_with_NS()

try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Esperando conexiones...')
ServerSocket.listen(5)

while True:
    Client, address = ServerSocket.accept()
    print('\nConectado a: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (Client, ))
    ThreadCount += 1
    print('Número de hilo: ' + str(ThreadCount))
ServerSocket.close()
