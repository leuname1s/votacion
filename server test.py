import socket

def iniciar_servidor():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 9999))
    server_socket.listen(5)
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
    iniciar_servidor()