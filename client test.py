import socket
import json
def enviar_voto(voto):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((config["server"]["ipPrivada"], config["server"]["puerto"]))

    client_socket.send(voto.encode())
    respuesta = client_socket.recv(1024).decode()
    print(f"Respuesta del servidor: {respuesta}")

    client_socket.close()

if __name__ == "__main__":
    with open("config.json","r") as archivo:
        config = json.load(archivo)
    voto = input("Introduce tu voto: ")
    enviar_voto(voto)
