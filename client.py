import socket
import json
import customtkinter
import tkinter

class App(customtkinter.CTk):   

    def __init__(self):
        super().__init__()
        self.geometry("600x500")
        self.title("Votacion")
        with open("config.json","r") as archivo:
            self.config = json.load(archivo)
        #codigo = input("Introduce su codigo: ")
        #verificacion = enviar_codigo(codigo)
        
    def enviar_voto(self,voto,codigo):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.config["server"]["ipPrivada"], self.config["server"]["puerto"]))  

        data = {"tipo" : "voto", "pc":self.config["pc"],"contenido":[voto,codigo]}   

        client_socket.send(json.dumps(data).encode())
        respuesta = client_socket.recv(1024).decode()
        print(f"Respuesta del servidor: {respuesta}")   

        client_socket.close()   

    def enviar_codigo(self,codigo):  
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.config["server"]["ipPrivada"], self.config["server"]["puerto"]))

        data = {"tipo" : "codigo", "pc":self.config["pc"],"contenido":codigo}

        client_socket.send(json.dumps(data).encode())
        respuesta = client_socket.recv(1024).decode()
        print(f"Respuesta del servidor: {respuesta}")
        if respuesta == "aceptado":
            print("aceptado")
            return("aceptado")
        elif respuesta == "denegado":
            print("denegado")
            return("denegado")
        elif respuesta == "error":
            print("error")
            return("error")

        client_socket.close()
    
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"   
app = App()
app.after(10,lambda: app.state("zoomed"))
app.mainloop()
