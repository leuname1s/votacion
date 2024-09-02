import socket
import json


    
def iniciar_servidor(config):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((config["ipPrivada"], config["puerto"]))
    server_socket.listen(config["colaEspera"])
    print("Servidor esperando conexiones...")

    votos = []

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Conectado a {addr}")

        data = client_socket.recv(1024).decode()
        print(f"Voto recibido: {data}")

        votos.append(data)
        client_socket.send("Voto recibido".encode())
        client_socket.close()

    server_socket.close()

if __name__ == "__main__":
    with open("config.json","r") as archivo:
        config = json.load(archivo)
        config = config["server"]
    iniciar_servidor(config)