import socket
import marshal

ClientSocket = socket.socket()
hostNS = '192.168.194.96'
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


# here we get the input from the user
print("Introduce la operación mátematica a realizar.")
print(
    "La operación debe tener la forma [operando] [operador] [operando]")
print("Los operadores disponibles son: \n   (+) Suma \n   (-) Resta \n   (*) Multiplicación \n   (/)División")
print("\nEjemplo: 4 + 5")
print("¡No olvides el espacio!")
inp = input(">> ")

inpList = inp.split()

if(len(inpList) == 3):
    prnd1 = inpList[0]
    operation = inpList[1]
    oprnd2 = inpList[2]

    if(operation == "/" or operation == "*" or operation == "+" or operation == "-"):
        if(oprnd2 != "0" ):
            serializados = marshal.dumps(inpList)
            print(oprnd2)
            print("lista")
            # Send operation
            ClientSocket.send(serializados)
            #ClientSocket.send(inp.encode())

            # Here we received output from the server socket
            response = ClientSocket.recv(1024)
            print("Resultado: "+inp+" = "+response.decode())
            input("\nPresiona enter para salir xD \n")
        else:
           print("Operación no válida")
    else: 
        print("No es un operando valido")   

            
else:
     output = "¡operación no válida!"

ClientSocket.close()


