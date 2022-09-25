from queue import Empty
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


def get_result_from_serv_op(oprnd1, operation, oprnd2):
    # Validate that there's an ip for the server of that operation
    if(operation in ipTable):
        host, port = ipTable[operation]

        ss = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM)

        datos = (int(oprnd1), int(oprnd2))
        serializados = marshal.dumps(datos)
        msg = "Conectando a Host {} y Puerto {}".format(host, port)

        try:
            ss.connect((host, port))
            # print("Conectado.")
            # print((ss.recv(port)).decode())
            ss.send(serializados)
            msg = ss.recv(port)
            ss.close()

            # Enviar resultado de operación al cliente que la pidió
            return msg

        except socket.error as e:
            print("Imposible conectar con servidor operador " + operation)
            print(str(e))

    else:
        print("¡Servidor "+operation+" aún no en tabla de direcciones!")

    output = "Imposible realizar la operación en estos momentos, intente después."
    return output.encode()


def serv_client(connection):
    # Enviar
    connection.send(str.encode('Bienvenido, Cliente.'))

    # Recibir Suma
    data = connection.recv(1024)
    if(len(data) > 0):
        deserializado = marshal.loads(data)

        # Enviar Resultado
        connection.send(get_result_from_serv_op(
            deserializado[0], deserializado[1], deserializado[2]))


def save_in_ip_Table(connection):
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
        try:
            serv_client(connection)
        except ConnectionResetError as e:
            print('Conexión con ' + address[0] +
                  ' interrumpida por parte del cliente.')
    elif(data.decode() == "Servidor Operador"):
        save_in_ip_Table(connection)
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
