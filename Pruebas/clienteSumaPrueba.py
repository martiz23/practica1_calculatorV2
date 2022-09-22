import socket
import marshal

h_name = socket.gethostname()
host = socket.gethostbyname(h_name)
port = 1233

ClientSocket = socket.socket()
hostNS = '192.168.56.1'
portNS = 1233

print('Esperando conexión')
try:
    ClientSocket.connect((hostNS, portNS))
except socket.error as e:
    print('No se pudo conectar con NS!')
    print(str(e))


# Enviar
ClientSocket.send(("Servidor Operando").encode())

# Aceptar
response = ClientSocket.recv(1024)
print(response.decode())

# Enviar
data = ('+', host, port)
serializados = marshal.dumps(data)
ClientSocket.send(serializados)

# Aceptar
response = ClientSocket.recv(1024)
print(response.decode())

ClientSocket.close()
#print("Host {} y Puerto {} enviados al {}".format(host,port,hostNS))
