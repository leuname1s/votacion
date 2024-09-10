import socket
import json
import sqlite3
import traceback
    
class servidor():
    def verificar_codigo(self,codigo):
        try:
            conexion = sqlite3.connect('database.db')
            cursor = conexion.cursor()

            # Consulta SQL para verificar el código
            query = """
            SELECT 
                CASE 
                    WHEN EXISTS (
                        SELECT 1 
                        FROM codigos 
                        WHERE codigo = ? AND utilizado = 0
                    ) 
                    THEN 1 
                    ELSE 0 
                END AS resultado;
            """

            # Ejecutar la consulta
            cursor.execute(query, (codigo,))
            resultado = cursor.fetchone()[0]

            # Cerrar la conexión
            conexion.close()
            return resultado
        except Exception as e:
            print(f"error al verificar codigo")
            return "error"
            

    
    def votar(self,voto,codigo):
        try:
            conexion = sqlite3.connect('database.db')
            cursor = conexion.cursor()

            cursor.execute("SELECT curso FROM codigos WHERE codigo = ?",(codigo,))
            curso = cursor.fetchone()[0]

            cursor.execute(f"UPDATE {curso} SET votos = votos + 1 WHERE lista = ?",(voto,))
            cursor.execute(f"UPDATE codigos SET utilizado = 1 WHERE codigo = ?",(codigo,))
            conexion.commit()
            return 1    #operacion exitosa
        except Exception as e:
            return 0
    def __init__(self,config):
        self.codigoPrueba = config["codigoPrueba"]
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((config["ipPrivada"], config["puerto"]))
        server_socket.listen(config["colaEspera"])
        print("Servidor esperando conexiones...")


        while True:
            try:
                client_socket, addr = server_socket.accept()

                data = client_socket.recv(1024).decode()

                data = json.loads(data)

                pc = data["pc"]
                #print(f"coneccion desde la pc {pc}")

                if data["tipo"] == "codigo":
                    codigo = data["contenido"].upper()
                    if codigo == self.codigoPrueba:
                        print(f"codigo de prueba desde la PC {data["pc"]}")
                        client_socket.send("aceptado".encode())
                        continue
                    else:
                        verificacion = self.verificar_codigo(codigo)
                        if verificacion == 1:
                            print(f"codigo verificado correctamente desde la PC {data["pc"]}")
                            client_socket.send("aceptado".encode())
                        elif verificacion == 0:
                            print(f"!codigo denegado desde la PC {data["pc"]}")
                            client_socket.send("denegado".encode())
                        elif verificacion == "error":
                            print(f"!!!ocurrio un error en la verificacion del codigo de la pc {data["pc"]}")
                            client_socket.send("error".encode())

                elif data["tipo"] == "voto":
                    codigo = data["contenido"][1].upper()
                    voto = data["contenido"][0]
                    if codigo == self.codigoPrueba:
                        print(f"codigo de prueba desde la PC {data["pc"]}")
                        client_socket.send("aceptado".encode())
                    elif self.votar(voto,codigo):
                        print(f"Voto emitido desde la pc {data["pc"]}")
                        client_socket.send("aceptado".encode())
                    else:
                        print(f"error al emitir el voto desde la pc{data["pc"]}")
                        client_socket.send("error".encode())


                #client_socket.send("Voto recibido".encode())
                client_socket.close()
            except Exception as e:
                print(f"error en el loop principal: {type(e).__name__}\n , ")
                print(f"args: {str(e.args)}\n")
                print(f"{traceback.format_exc()}\n")
                #messagebox.showwarning(title="Error Inesperado",message="Por favor contactece con la autoridad de la sala")
                print("\n---------------------\n")


if __name__ == "__main__":
    with open("config.json","r") as archivo:
        config = json.load(archivo)
        config = config["server"]
    server = servidor(config)
    
    