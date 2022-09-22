import socket
import os
import marshal
from _thread import *


ServerSocket = socket.socket()
h_name = socket.gethostname()
host = socket.gethostbyname(h_name)

port = 1233
ThreadCount = 0

ipTable = {}

try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))
print("Host NS: " + host)
print("Puerto NS: " + str(port))
print('Esperando conexiones...')
ServerSocket.listen(5)


def serv_client(connection):
    # Enviar
    connection.send(str.encode('Bienvenido, Cliente.'))

    # Recibir Suma
    data = connection.recv(1024)
    print(data)
    deserializado = marshal.loads(data)
    #msg = data.decode()

    print("Operación recibida.")

    #operation_list = marshal.loads(data)
    if(len(deserializado) == 3):
        oprnd1 = deserializado[0]
        operation = deserializado[1]
        oprnd2 = deserializado[2]
        print("Operación en curso...")

        # Enviar datos como cliente al servidor operador específico
        ss = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM)

        host, port = ipTable[operation]

        datos = (int(oprnd1), int(oprnd2))
        serializados = marshal.dumps(datos)
        msg = "Conectando a Host {} y Puerto {}".format(host, port)

        try:
            ss.connect((host, port))
            print("Conectado.")
        except socket.error as e:
            print("Imposible conectar con servidor operador " + operation)
            print(str(e))

        print((ss.recv(port)).decode())
        ss.send(serializados)
        msg = ss.recv(port)
        ss.close()

        # Enviar resultado de operación al cliente que la pidió
        connection.send(msg)

    else:
        output = "¡operación no válida!"
        connection.send(output.encode())

    print("Resultado enviado al cliente.")


def accept_connection(connection):
    # Enviar
    connection.send(str.encode('Bienvenido, servidor subrogado.'))

    # Recibir
    data = connection.recv(1024)
    deserializados = marshal.loads(data)

    if(len(deserializados) == 3):
        ipTable[deserializados[0]] = (deserializados[1], deserializados[2])
        msg = "Host {} y Puerto {} aceptados de {}".format(
            deserializados[1], deserializados[2], deserializados[0])
    else:
        msg = "Ups. Algo salió mal."

    # Enviar
    connection.send(str.encode(msg))
    print(msg + "\n")


def threaded_client(connection):
    print("Aceptando conexión de ", end=" ")

    # Aceptar
    data = connection.recv(1024)

    print(data.decode())

    if(data.decode() == "Cliente"):
        serv_client(connection)
    elif(data.decode() == "Servidor Operador"):
        accept_connection(connection)
    else:
        print("Interación con el servidor no válida.")

    connection.close()


while True:
    Client, address = ServerSocket.accept()
    print('\nConexión con: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))

ServerSocket.close()
