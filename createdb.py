import sqlite3
import json
import random
import string

con = sqlite3.connect("database.db")

cur = con.cursor()

with open("config.json","r") as archivo:
    config = json.load(archivo)
    
def generar_codigo_aleatorio():
    caracteres = string.ascii_uppercase + string.digits
    codigo = ''.join(random.choice(caracteres) for _ in range(6))
    return codigo


def generar_base_de_datos(config):
    listas = config["listas"].keys()
    #print(stringColumnas)
    cur.execute("CREATE TABLE IF NOT EXISTS codigos (codigo TEXT, curso TEXT, utilizado INT)")
    con.commit()
    codigos = set()
    for curso in config["cursos"].items():
        #print(f"CREATE TABLE {curso[0]} ({(stringColumnas)})")
        cur.execute(f"CREATE TABLE IF NOT EXISTS {curso[0]} (lista TEXT, votos INT)")
        con.commit()
        for lista in listas:
            cur.execute(f"INSERT INTO {curso[0]} VALUES (?, ?)",(lista,0))
            
        with open(f"codigos/{curso[0]}.txt","w") as archivo:
            for _ in range(curso[1]):
                while True:
                    codigo = generar_codigo_aleatorio()
                    if codigo not in codigos:
                        codigos.add(codigo)
                        break
                    #else: print("codigo repetido")
                cur.execute(f"INSERT INTO codigos VALUES (?,?,?)",(codigo,curso[0],0))
                con.commit()
                archivo.write(f"{codigo}\n")
            
generar_base_de_datos(config)
    
    
