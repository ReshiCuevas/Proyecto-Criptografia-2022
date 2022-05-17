from hmac import new
import socket
import nacl.utils as pynapple
from nacl.signing import SigningKey, VerifyKey
import nacl.secret
from Crypto.Cipher import ChaCha20
import os
import json

a = socket.gethostbyname(socket.gethostname())
b = 4455
ADDR = (a, b)
SIZE = 1024
FORMAT = "utf-8"


"""Función para encriptar archivos"""
def encryptor(data, filename):
    x = nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)
    non = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)
    Zephyr = ChaCha20.new(key = x, nonce = non)
    
    newdata = Zephyr.encrypt(data)
    
    file = open(filename, "w")
    file.write(str(newdata))
    file.close()
    alldata = (newdata, non, x )
    return alldata

"""Función para desencriptar archivos"""
def decryptor(alldata):
    data = alldata[0]
    non = alldata[1]
    x = alldata[2]
    newZephyr = ChaCha20.new(key = x, nonce = non)
    oldtext = newZephyr.decrypt(data)
    with open('not_a_test.txt', 'w') as f:
        f.write(str(oldtext))

    return oldtext

    

def main():
    print("[STARTING] Inciciando el servidor.")
    """Creando el socket TCP """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    """ Bind del puerto y dirección IP con el servidor """
    server.bind(ADDR)

    """ Esperando la conexion con el cliente """
    server.listen()
    print("[LISTENING] Esperando al cliente.")

    while True:
        
        """ Se acepta la conexion deñ cliente """
        conn, addr = server.accept()
        print(f"[NEW CONNECTION] {addr} conectado.")

        """Reciviendo nombre del archivo """
        filename = conn.recv(SIZE).decode(FORMAT)
        print(f"[RECV] Reciviendo nombre del archivo.")
        file = open(filename, "r")
        conn.send("Filename recibido.".encode(FORMAT))

        """Se reciben los datos del cliente """
        data = conn.recv(SIZE).decode(FORMAT)
        print(f"[RECV] Recibiendo datos.")
        data = data.encode(FORMAT)
        conn.send("Datos recibidos".encode(FORMAT))
        file.close()
        """Se llama a la funcion para encriptar"""
        alldata = encryptor(data, filename)
        print(f"Los datos fueron encriptados")
        
        """Firma de los datos y se crea un nuevo archivo con a firma"""
        signx = SigningKey.generate()
        lapoderosa = signx.sign(alldata[0])
        with open('firma.txt', 'w') as f:
            f.write(str(lapoderosa))
        
        """Verificación de la firma y se crea un nuevo archivo"""
        vfx = VerifyKey(signx.verify_key.encode())
        confirmacion = vfx.verify(lapoderosa)
        with open('confirmada.txt', 'w') as f:
            f.write(str(confirmacion))
        
        """Se desencriptan los datos y se crea un archivo nuevo en el que se escriben"""
        decryptor(alldata)
        
        """ Cerrando la conexion con el cliente. """
        conn.close()
        print(f"[DISCONNECTED] {addr} desconectado.")
        return

if __name__ == "__main__":
    main()
