import re
import socket
import marshal
import re

ClientSocket = socket.socket()
hostNS = '192.168.56.1'
portNS = 1233

try:
    ClientSocket.connect((hostNS, portNS))
    print('Bienvenido a la calculadora de sockets!!')
except socket.error as e:
    print(str(e))

# Enviar
ClientSocket.send(("Cliente").encode())

# Recibir
response = ClientSocket.recv(1024)
print(response.decode())


# Prompts the user for input string
print("Introduce la operación mátematica a realizar.")
print(
    "La operación debe tener la forma [operando] [operador] [operando]")
print("Los operadores disponibles son: \n   (+) Suma \n   (-) Resta \n   (*) Multiplicación \n   (/)División \n   (%)Módulo \n   (^)Potencia")
print("\nEjemplo: 4 + 5")
print("¡No olvides el espacio!")
inp = input(">> ")

# compiling the pattern for the operation format
pat = re.compile("[0-9]+\s[+-/*%^]\s[0-9]+")

# Checks whether the whole string matches the re.pattern or not
if re.fullmatch(pat, inp):
    inpList = inp.split()
    prnd1 = inpList[0]
    operation = inpList[1]
    oprnd2 = inpList[2]
    if(operation == "/" and oprnd2 == "0"):
        print("División entre cero.")
    else:
        serializados = marshal.dumps(inpList)
        # Send operation
        ClientSocket.send(serializados)
        # ClientSocket.send(inp.encode())

        # Here we received output from the server socket
        response = ClientSocket.recv(1024)
        print("Resultado: "+inp+" = "+response.decode())

else:
    print("¡Formato no válido!")

input("\nPresiona enter para salir xD \n")
ClientSocket.close()
