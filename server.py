from datetime import datetime
import socket
import json
import sqlite3
import traceback
import customtkinter
import threading
from PIL import Image
from tkinter import CENTER
class servidor(customtkinter.CTk):
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
        
    def setServer(self):
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((config["ipPrivada"], config["puerto"]))
            server_socket.listen(config["colaEspera"])
            self.insertLog("Servidor esperando conexiones...")


            while True:
                try:

                    
                    client_socket, addr = server_socket.accept()

                    data = client_socket.recv(1024).decode()

                    data = json.loads(data)

                    pc = data["pc"]
                    #self.insertLog(f"coneccion desde la pc {pc}")
                    if pc in self.pcs:
                        pc = self.pcs[pc]
                    else:
                        self.pcs[pc] = compuFrame(self.mainFrame,pc,fg_color="#1D1E1E")
                        pc = self.pcs[pc]
                        pc.grid(row=self.row,column=self.column,padx=10,pady=10)
                        self.column +=1
                        if self.column > 6:
                            self.column = 0
                            self.row += 1
                    if data["tipo"] == "codigo":
                        codigo = data["contenido"].upper()
                        if codigo == self.codigoPrueba:
                            self.insertLog(f"codigo de prueba desde la PC {data["pc"]}")
                            pc.changeState("prueba")
                            client_socket.send("aceptado".encode())
                            continue
                        else:
                            verificacion = self.verificar_codigo(codigo)
                            if verificacion == 1:
                                self.insertLog(f"codigo verificado correctamente desde la PC {data["pc"]}")
                                pc.changeState("valido")
                                client_socket.send("aceptado".encode())
                            elif verificacion == 0:
                                self.insertLog(f"!codigo denegado desde la PC {data["pc"]}")
                                pc.changeState("denegado")
                                client_socket.send("denegado".encode())
                            elif verificacion == "error":
                                pc.changeState("empty")
                                self.insertLog(f"!!!ocurrio un error en la verificacion del codigo de la pc {data["pc"]}")
                                client_socket.send("error".encode())

                    elif data["tipo"] == "voto":
                        codigo = data["contenido"][1].upper()
                        voto = data["contenido"][0]
                        if codigo == self.codigoPrueba:
                            self.insertLog(f"codigo de prueba desde la PC {data["pc"]}")
                            pc.changeState("prueba")
                            client_socket.send("aceptado".encode())
                        elif self.votar(voto,codigo):
                            self.insertLog(f"Voto emitido desde la pc {data["pc"]}")
                            pc.changeState("voto")
                            client_socket.send("aceptado".encode())
                        else:
                            self.insertLog(f"error al emitir el voto desde la pc{data["pc"]}")
                            pc.changeState("empty")
                            client_socket.send("error".encode())


                    #client_socket.send("Voto recibido".encode())
                    client_socket.close()
                except Exception as e:
                    self.insertLog(f"error en el loop principal: {type(e).__name__}\n , ")
                    self.insertLog(f"args: {str(e.args)}\n")
                    self.insertLog(f"{traceback.format_exc()}\n")
                    #messagebox.showwarning(title="Error Inesperado",message="Por favor contactece con la autoridad de la sala")
                    self.insertLog("\n---------------------\n")
                    
    def insertLog(self,text):
        hora = datetime.today().strftime("%H:%M  / ")
        self.logFrame.insert("1.0",hora+text+"\n")  
        
    def __init__(self,config):
        super().__init__()
        self.title("servidor")
        self.state("zoomed")
        self.geometry("400x400+0+0")
        
        self.codigoPrueba = config["codigoPrueba"]
        self.pcs = dict()
        self.column=0
        self.row=0
        self.logFrame = customtkinter.CTkTextbox(self,)
        self.mainFrame = customtkinter.CTkScrollableFrame(self,)
        
        self.columnconfigure((0),weight=1)
        self.rowconfigure((0),weight=1)
        self.rowconfigure((1),weight=4)
        
        self.logFrame.grid(row=0,column=0,sticky="nsew",padx=20,pady=10)
        self.mainFrame.grid(row=1,column=0,sticky="nsew",padx=20,pady=10)
        
        server_thread = threading.Thread(target=self.setServer, daemon=True)
        server_thread.start()

class compuFrame(customtkinter.CTkFrame):
    def createEntry(self,type):
        if type == "denegado":
            text = "Codigo Denegado"
            color = "red"
        elif type == "valido":
            text = "Codigo Valido"
            color = "blue"
        elif type == "prueba":
            text = "Codigo de Prueba"
            color = "yellow"
        elif type == "voto":
            text = "Voto Recibido"
            color = "green"
        elif type == "empty":
            color = "#1D1E1E"
            text = ""
        entry = customtkinter.CTkEntry(self,250,60,justify="center",border_color=color,border_width=7,font=("Arial Rounded MT Bold",25),fg_color="transparent")
        entry.insert(0,text)
        entry.configure(state="disabled")
        return entry
    
    def __init__(self,master,pc,**kwargs):
        super().__init__(master,**kwargs)
        imagen = customtkinter.CTkImage(light_image=Image.open("pc.png"),
                                  dark_image=Image.open("pc.png"),
                                  size=(250,250))
        label = customtkinter.CTkLabel(self,image=imagen,text="",font=("Arial Rounded MT Bold",24))
        label.grid(row=0,column=0,padx=10,pady=10)
        label2 = customtkinter.CTkLabel(self,text=str(pc),font=("Arial Rounded MT Bold",60))
        label2.grid(row=0,column=0,padx=10,pady=(0,70))

        self.state = self.createEntry("empty")
        self.lastState = self.createEntry("empty")
        
        self.state.grid(row=1,column=0,padx=10,pady=10)
        self.lastState.grid(row=2,column=0,padx=10,pady=(0,10))

    def changeState(self,type):
        self.lastState = self.state
        self.lastState.grid(row=2,column=0,padx=10,pady=(0,10))
        self.state = self.createEntry(type)
        self.state.grid(row=1,column=0,padx=10,pady=10)
        border = self.state.cget("border_color")
        print(border)
        self.configure(border_width=5)
        self.configure(border_color=border)
        self.after(200,lambda: self.configure(border_color="#1D1E1E"))
        self.after(400,lambda: self.configure(border_color=border))
        self.after(600,lambda: self.configure(border_color="#1D1E1E"))
        self.after(800,lambda: self.configure(border_width=0))
        
if __name__ == "__main__":
    with open("config.json","r") as archivo:
        config = json.load(archivo)
        config = config["server"]
    server = servidor(config)
    server.mainloop()
    server.after(10,lambda: server.state("zoomed"))
    #server.after(10,lambda: server.attributes("-fullscreen",True))
    
    
    