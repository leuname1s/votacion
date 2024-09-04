import socket
import json
import customtkinter
from tkinter import messagebox
from random import shuffle
from PIL import Image

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
        #self.codigoFrame.grid(row=0,column=0,sticky="nsew")
        self.codigoFrame.columnconfigure((0),weight=1)
        self.codigoFrame.rowconfigure((0,2),weight=1)
        label = customtkinter.CTkLabel(self.codigoFrame,text="Introduzca su codigo: ",font=("Arial Rounded MT Bold",24))
        label.grid(row=0,column=0,sticky="s")
        self.codigoEntry = customtkinter.CTkEntry(self.codigoFrame,font=("Arial Rounded MT Bold",24),justify="center",width=200)
        self.codigoEntry.grid(row=1,column=0,pady=20)
        button = customtkinter.CTkButton(self.codigoFrame,text="Aceptar",font=("Arial Rounded MT Bold",24),command=self.aceptarHandle)
        button.grid(row=2,column=0,sticky="n")
        
        self.votacionFrame = customtkinter.CTkFrame(self,fg_color="transparent")
        self.votacionFrame.grid(row=0,column=0,sticky="nsew")
        self.votacionFrame.columnconfigure((0),weight=1)
        
        listas = []
        lenListas = len(self.config["listas"])
        size = {
            2:1,
            3:1,
            4:0.75,
            5:0.75,
            6:0.75
        }
        for lista in self.config["listas"].items():
            lista_frame = listaFrame(self.votacionFrame,lista[0],lista[1]["titulo"],lista[1]["subtitulo"],lista[1]["imagen"],size[lenListas])
            listas.append(lista_frame)
        shuffle(listas)
        if len(listas) == 2:
            self.votacionFrame.columnconfigure((0,1),weight=1)
            self.votacionFrame.rowconfigure((0),weight=1)
            listas[0].grid(row=0,column=0)
            listas[1].grid(row=0,column=1)
        elif len(listas) == 3:
            self.votacionFrame.columnconfigure((0,1,2),weight=1)
            self.votacionFrame.rowconfigure((0),weight=1)
            listas[0].grid(row=0,column=0)
            listas[1].grid(row=0,column=1)
            listas[2].grid(row=0,column=2)
        elif len(listas) == 4:
            self.votacionFrame.columnconfigure((0,1),weight=1)
            self.votacionFrame.rowconfigure((0,1),weight=1)
            listas[0].grid(row=0,column=0)
            listas[1].grid(row=0,column=1)
            listas[2].grid(row=1,column=0)
            listas[3].grid(row=1,column=1)
        elif len(listas) == 5:
            self.votacionFrame.columnconfigure((0,1,2),weight=1)
            self.votacionFrame.rowconfigure((0,1),weight=1)
            listas[0].grid(row=0,column=0)
            listas[1].grid(row=0,column=1)
            listas[2].grid(row=0,column=2)
            listas[3].grid(row=1,column=0,columnspan=2)
            listas[4].grid(row=1,column=1,columnspan=2)
            
        elif len(listas) == 6:
            self.votacionFrame.columnconfigure((0,1,2),weight=1)
            self.votacionFrame.rowconfigure((0,1),weight=1)
            listas[0].grid(row=0,column=0)
            listas[1].grid(row=0,column=1)
            listas[2].grid(row=0,column=2)
            listas[3].grid(row=1,column=0)
            listas[4].grid(row=1,column=1)
            listas[5].grid(row=1,column=2)


        
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
        client_socket.close()
        return respuesta
    
    def aceptarHandle(self):
        codigo = self.codigoEntry.get()
        respuesta = self.enviar_codigo(codigo=codigo)
        if respuesta == "aceptado":
            self.codigoFrame.grid_forget()
            self.votacionFrame.grid(row=0,column=0,sticky="nsew")
        elif respuesta == "denegado":
            messagebox.showwarning("codigo erroneo","El codigo que ingreso no fue aceptado, intente de nuevo")
        elif respuesta == "error":
            messagebox.showerror("error del servidor","ocurrio un error en el servidor. Por favor notifiquelo a las autoridades de la sala")
        
class listaFrame(customtkinter.CTkFrame):
    def __init__(self, master, name,titulo,subtitulo,imagen,size):
        super().__init__(master,cursor="hand2")
        self.columnconfigure((0),weight=1)
        self.bind("<Button-1>",self.clickHandle)
        imagen = Image.open(imagen)
        imagen = customtkinter.CTkImage(imagen,imagen,(500*size,500*size))
        imagenLabel = customtkinter.CTkLabel(self,image=imagen,text="")
        imagenLabel.bind("<Button-1>",self.clickHandle)
        imagenLabel.grid(row=0,column=0,pady=10,padx=10)
        label = customtkinter.CTkLabel(self,text=titulo,font=("Arial Rounded MT Bold",72*size),width=500*size)
        label.bind("<Button-1>",self.clickHandle)
        label.grid(row=1,column=0,padx=10)
        label = customtkinter.CTkLabel(self,text=subtitulo,font=("Arial Rounded MT Bold",26*size),width=500*size)
        label.bind("<Button-1>",self.clickHandle)
        label.grid(row=2,column=0,pady=(0,10),padx=10)
        
    def clickHandle(self,event):
        print("aa")

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"   
app = App()
#app.after(10,lambda: app.attributes("-fullscreen",True))
app.mainloop()
