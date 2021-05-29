import socket
import base64
import hashlib

#Sockets
addr = ("10.2.126.2",19876) #Direccion ip y puerto objetivo
#addr = ("127.0.0.1",19876)
stcp = socket.socket()
stcp.connect(addr)
buffersize = 5000
sudp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sudp.bind(("0.0.0.0",19877))
sudp.settimeout(20)
i = 0
m = ()
rt =""
ru = ""
while (i==0):
    try:
        cont = 0
        t = False
        print("Para recibir su mensaje ingrese su correo UCAB sin @est.ucab.edu.ve")
        m = ("helloiam "+input()) 
        stcp.send(m.encode('utf-8'))  #Se conecta con el puerto 19876 del servidor
        rt = stcp.recv(buffersize).decode('utf-8')
        if ("ok" in rt):
            m = "msglen" 
            stcp.send(m.encode('utf-8'))       # Se regunta por el largo del mensaje
            rt = stcp.recv(buffersize).decode('utf-8')
            if ("ok" in rt):
                while (t == False):
                    try:
                        print("Esperando mensaje...")
                        m = "givememsg 19877"  
                        stcp.send(m.encode('utf-8'))  # Se pide el mensaje para recibirlo por el puerto 19877
                        rt = stcp.recv(buffersize).decode('utf-8')
                        ru = sudp.recv(buffersize)  # Se recibe el mensaje del puerto UDP
                        if (ru):
                            t = True
                    except(socket.timeout):
                        if (cont > 5):  #Solo se permiten 5 intentos de recuperar el mensaje
                            print("No se pudo recuperar el mensaje")
                            break
                        cont = cont + 1
                if (t == False):
                    break
                ru = base64.b64decode(ru)
                m = hashlib.md5(ru).hexdigest() # Se recibe el checksum
                ru = ru.decode('utf-8')
                m = "chkmsg " + m           
                stcp.send(m.encode('utf-8'))   # Se confirma el checksum
                rt = stcp.recv(buffersize).decode('utf-8')
                print("El mensaje es:")
                print(ru)
                if ("ok" in rt):
                    m = "bye"
                    stcp.send(m.encode('utf-8'))   # Se cierra la conexion al servidor
                    break
    
    except (socket.error):
        print("Error en la conexión")
        break

    except Exception as e :
        print(e)