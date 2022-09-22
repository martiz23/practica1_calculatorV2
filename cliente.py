import socket

ClientSocket = socket.socket()
hostNS = '192.168.56.1'
portNS = 1233

try:
    ClientSocket.connect((hostNS, portNS))
    print('Bienvenido a la calculadora de sockets!!!')
except socket.error as e:
    print(str(e))

# Enviar
ClientSocket.send(("Cliente").encode())

# Recibir
response = ClientSocket.recv(1024)
print(response.decode())


# here we get the input from the user
print("Introduce la operación mátematica a realizar.")
print(
    "La operación debe tener la forma [operando] [operador] [operando]")
print("Los operadores disponibles son: \n   (+) Suma \n   (-) Resta \n   (*) Multiplicación \n   (/)División")
print("\nEjemplo: 4 + 5")
print("¡No olvides el espacio!")
inp = input(">> ")

# Send operation
ClientSocket.send(inp.encode())

# Here we received output from the server socket
response = ClientSocket.recv(1024)
print("Resultado: "+inp+" = "+response.decode())
input("\nPresiona enter para salir xD \n")

ClientSocket.close()
