import socket
import json
import customtkinter
import tkinter
import PIL

class App(customtkinter.CTk):   

    def __init__(self):
        super().__init__()
        self.geometry("600x500")
        self.title("Votacion")
        with open("config.json","r") as archivo:
            self.config = json.load(archivo)
        self.columnconfigure((0),weight=1)
        self.rowconfigure((0),weight=1)
        #self.mainFrame = customtkinter.CTkFrame(self)
        #self.mainFrame.grid(row=0,column=0,sticky="nsew")
        #self.mainFrame.columnconfigure((0),weight=1)
        self.codigoFrame = customtkinter.CTkFrame(self)
        self.codigoFrame.grid(row=0,column=0,sticky="nsew")
        self.codigoFrame.columnconfigure((0),weight=1)
        self.codigoFrame.rowconfigure((0,2),weight=1)
        label = customtkinter.CTkLabel(self.codigoFrame,text="Introduzca su codigo: ",font=("Arial Rounded MT Bold",24))
        label.grid(row=0,column=0,sticky="s")
        self.entry = customtkinter.CTkEntry(self.codigoFrame,font=("Arial Rounded MT Bold",24),justify="center",width=200)
        self.entry.grid(row=1,column=0,pady=20)
        self.button = customtkinter.CTkButton(self.codigoFrame,text="Aceptar",font=("Arial Rounded MT Bold",24))
        self.button.grid(row=2,column=0,sticky="n")
        
        self.votacionFrame = customtkinter.CTkFrame(self)
        #self.votacionFrame.grid(row=0,column=0,sticky="nsew")
        self.votacionFrame.columnconfigure((0),weight=1)
        

        
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
#app.after(10,lambda: app.state("normal"))
app.after(10,lambda: app.attributes("-fullscreen",True))
app.mainloop()
