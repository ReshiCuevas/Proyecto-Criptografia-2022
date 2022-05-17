
import socket

IP = socket.gethostbyname(socket.gethostname())
PORT = 4455
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024

def main():
    """ Creando el socket TCP """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    """ Conectando con el servidor """
    client.connect(ADDR)
    
    """Preguntando nombre del archivo"""
    print("Nombre del archivo a enviar y cifrar: ")
    nof = input(str())
    
    """Leyendo el archivo y guardando los datos """
    file = open(nof, "r")
    data = file.read()

    """Enviando nombre del archivo al servidor. """
    client.send("test.txt".encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {msg}")

    """Enviando datos al servidor """
    client.send(data.encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {msg}")

    """ Cerrando el archivo """
    file.close()

    """Cerrando la conexion con el servidor """
    client.close()


if __name__ == "__main__":
    main()
