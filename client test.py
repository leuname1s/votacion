import socket

def enviar_voto(voto):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 9999))

    client_socket.send(voto.encode())
    respuesta = client_socket.recv(1024).decode()
    print(f"Respuesta del servidor: {respuesta}")

    client_socket.close()

if __name__ == "__main__":
    voto = input("Introduce tu voto: ")
    enviar_voto(voto)
