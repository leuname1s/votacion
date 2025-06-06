import socket
import json
import customtkinter
from tkinter import messagebox,END
from random import shuffle  
from PIL import Image
import traceback


class App(customtkinter.CTk):   
    def obtener_codigo_pc(self):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.config["server"]["ipPrivada"], self.config["server"]["puerto"]))  
            
            data = {"tipo" : "newPc"}   
            
            client_socket.send(json.dumps(data).encode())
            respuesta = client_socket.recv(1024).decode()
            client_socket.close()  
            return respuesta 
            

        except Exception as e:
            return "error"
        
    def __init__(self):
        super().__init__()
        self.geometry("600x500")
        self.title("Votacion")
        with open("config.json","r",encoding="utf-8") as archivo:
            self.config = json.load(archivo)
        self.columnconfigure((0),weight=1)
        self.rowconfigure((0),weight=1)
        self.codigo = ""
        self.codigoFrame = customtkinter.CTkFrame(self)
        self.codigoFrame.grid(row=0,column=0,sticky="nsew")
        self.codigoFrame.columnconfigure((0),weight=1)
        self.codigoFrame.rowconfigure((0,2),weight=1)
        label = customtkinter.CTkLabel(self.codigoFrame,text="Introduzca su codigo: ",font=("Arial Rounded MT Bold",24))
        label.grid(row=0,column=0,sticky="s")
        self.codigoEntry = customtkinter.CTkEntry(self.codigoFrame,font=("Arial Rounded MT Bold",24),justify="center",width=200)
        self.codigoEntry.grid(row=1,column=0,pady=20)
        button = customtkinter.CTkButton(self.codigoFrame,text="Aceptar",font=("Arial Rounded MT Bold",24),command=self.aceptarHandle)
        button.grid(row=2,column=0,sticky="n")
        
        self.votacionFrame = customtkinter.CTkFrame(self,fg_color="transparent")
        #self.votacionFrame.grid(row=0,column=0,sticky="nsew")
        self.votacionFrame.columnconfigure((0),weight=1)
        
        self.listas = []
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
            self.listas.append(lista_frame)
        

        self.pc = self.obtener_codigo_pc()
        if self.pc == "error":
            messagebox.showerror("error","No se establecio coneccion con el servidor")
            self.destroy()

    def enviar_voto(self,voto,codigo):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.config["server"]["ipPrivada"], self.config["server"]["puerto"]))  

            data = {"tipo" : "voto", "pc":self.pc,"contenido":[voto,codigo]}   

            client_socket.send(json.dumps(data).encode())
            respuesta = client_socket.recv(1024).decode()
            client_socket.close()   

            return respuesta
        except Exception as e:
            error.write(f"error {type(e).__name__}\n , enviando voto")
            error.write(f"args: {str(e.args)}\n")
            error.write(f"{traceback.format_exc()}\n")
            messagebox.showwarning(title="Error Inesperado",message="Por favor contactece con la autoridad de la sala")
            error.write("\n---------------------\n")

    def enviar_codigo(self,codigo):  
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.config["server"]["ipPrivada"], self.config["server"]["puerto"]))

            data = {"tipo" : "codigo", "pc":self.pc,"contenido":codigo}

            client_socket.send(json.dumps(data).encode())
            respuesta = client_socket.recv(1024).decode()
            print(f"Respuesta del servidor: {respuesta}")
            client_socket.close()
            return respuesta
        except Exception as e:
            error.write(f"error {type(e).__name__}\n , enviando codigo")
            error.write(f"args: {str(e.args)}\n")
            error.write(f"{traceback.format_exc()}\n")
            messagebox.showwarning(title="Error Inesperado",message="Por favor contactece con la autoridad de la sala")
            error.write("\n---------------------\n")
    
    def aceptarHandle(self):
        try:
            codigo = self.codigoEntry.get()
            self.codigoEntry.delete(0,END)
            respuesta = self.enviar_codigo(codigo=codigo)
            if respuesta == "aceptado":
                self.codigo = codigo
                self.codigoFrame.grid_forget()
                shuffle(self.listas)
                if len(self.listas) == 2:
                    self.votacionFrame.columnconfigure((0,1),weight=1)
                    self.votacionFrame.rowconfigure((0),weight=1)
                    self.listas[0].grid(row=0,column=0)
                    self.listas[1].grid(row=0,column=1)
                elif len(self.listas) == 3:
                    self.votacionFrame.columnconfigure((0,1,2),weight=1)
                    self.votacionFrame.rowconfigure((0),weight=1)
                    self.listas[0].grid(row=0,column=0)
                    self.listas[1].grid(row=0,column=1)
                    self.listas[2].grid(row=0,column=2)
                elif len(self.listas) == 4:
                    self.votacionFrame.columnconfigure((0,1),weight=1)
                    self.votacionFrame.rowconfigure((0,1),weight=1)
                    self.listas[0].grid(row=0,column=0)
                    self.listas[1].grid(row=0,column=1)
                    self.listas[2].grid(row=1,column=0)
                    self.listas[3].grid(row=1,column=1)
                elif len(self.listas) == 5:
                    self.votacionFrame.columnconfigure((0,1,2),weight=1)
                    self.votacionFrame.rowconfigure((0,1),weight=1)
                    self.listas[0].grid(row=0,column=0)
                    self.listas[1].grid(row=0,column=1)
                    self.listas[2].grid(row=0,column=2)
                    self.listas[3].grid(row=1,column=0,columnspan=2)
                    self.listas[4].grid(row=1,column=1,columnspan=2)
                elif len(self.listas) == 6:
                    self.votacionFrame.columnconfigure((0,1,2),weight=1)
                    self.votacionFrame.rowconfigure((0,1),weight=1)
                    self.listas[0].grid(row=0,column=0)
                    self.listas[1].grid(row=0,column=1)
                    self.listas[2].grid(row=0,column=2)
                    self.listas[3].grid(row=1,column=0)
                    self.listas[4].grid(row=1,column=1)
                    self.listas[5].grid(row=1,column=2)
                self.votacionFrame.grid(row=0,column=0,sticky="nsew")
            elif respuesta == "denegado":
                messagebox.showwarning("codigo erroneo","El codigo que ingreso no fue aceptado, intente de nuevo")
            elif respuesta == "error":
                messagebox.showerror("error del servidor","ocurrio un error en el servidor. Por favor notifiquelo a las autoridades de la sala")
        except Exception as e:
            error.write(f"error {type(e).__name__}\n , al aceptar codigo (boton aceptar)")
            error.write(f"args: {str(e.args)}\n")
            error.write(f"{traceback.format_exc()}\n")
            messagebox.showwarning(title="Error Inesperado",message="Por favor contactece con la autoridad de la sala")
            error.write("\n---------------------\n")
            
    def votoHandle(self,voto,titulo):
        try:
            if messagebox.askokcancel(f"Confirmar voto",f"Esta seguro de votar a {titulo}"):
                respuesta = self.enviar_voto(voto,self.codigo) 
                if respuesta == "aceptado":
                    messagebox.showinfo("Operacion satisfactoria","El voto fue emitido con exito. Muchas gracias")
                    self.votacionFrame.grid_forget()
                    for lista in self.listas:
                        lista.grid_forget()
                        
                    self.codigoFrame.grid(row=0,column=0,sticky="nsew")
                elif respuesta == "error":
                    messagebox.showerror("error del servidor","ocurrio un error en el servidor. Por favor notifiquelo a las autoridades de la sala")
        except Exception as e:
            error.write(f"error {type(e).__name__}\n , al confirmar voto")
            error.write(f"args: {str(e.args)}\n")
            error.write(f"{traceback.format_exc()}\n")
            messagebox.showwarning(title="Error Inesperado",message="Por favor contactece con la autoridad de la sala")
            error.write("\n---------------------\n")
                
class listaFrame(customtkinter.CTkFrame):
    def __init__(self, master, name,titulo,subtitulo,imagen,size):
        super().__init__(master,cursor="hand2")
        self.columnconfigure((0),weight=1)
        self.bind("<Button-1>",self.clickHandle)
        self.name = name
        self.tittle = titulo
        imagen = Image.open(imagen)
        imagen = customtkinter.CTkImage(imagen,imagen,(500*size,500*size))
        imagenLabel = customtkinter.CTkLabel(self,image=imagen,text="")
        imagenLabel.bind("<Button-1>",self.clickHandle)
        imagenLabel.grid(row=0,column=0,pady=10,padx=10)
        label = customtkinter.CTkLabel(self,text=titulo,font=("Arial",72*size),width=500*size)
        label.bind("<Button-1>",self.clickHandle)
        label.grid(row=1,column=0,padx=10)
        label = customtkinter.CTkLabel(self,text=str(subtitulo),font=("Arial",26*size),width=500*size)
        label.bind("<Button-1>",self.clickHandle)
        label.grid(row=2,column=0,pady=(0,10),padx=10)
        
    def clickHandle(self,event):
        app.votoHandle(self.name,self.tittle)
        
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"   

app = App()
app.after(10,lambda: app.attributes("-fullscreen",True))
with open("errores.txt","w") as error:
    app.mainloop()
