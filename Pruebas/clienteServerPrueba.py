import socket
import os
import marshal

oprnd1 = "12"
operation = "+"
oprnd2 = "3"

# here we change str to int converstion
#num1 = int(oprnd1)
#num2 = int(oprnd1)

# Enviar datos como cliente al servidor específico
ss = socket.socket(socket.AF_INET,
                   socket.SOCK_STREAM)
if operation == "+":
    #result = num1 + num2
    host = '169.254.24.126'
    #host = socket.gethostname()
elif operation == "-":
    #result = num1 - num2
    host = 'localhost'
elif operation == "/":
    #result = num1 / num2
    host = 'localhost'
elif operation == "*":
    #result = num1 * num2
    host = 'localhost'
#host = '192.168.291.40'
#host = socket.gethostname()
port = 1233
datos = (int(oprnd1), int(oprnd1))
serializados = marshal.dumps(datos)
print("connecten't " + host)

ss.connect((host, port))
print("connected")
print((ss.recv(port)).decode())
ss.send(serializados)
msg = ss.recv(port)
ss.close()
print("{} = {}".format(datos, msg.decode()))
input("enter")
