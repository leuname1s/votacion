import sqlite3
import json

con = sqlite3.connect("database.db")
cur = con.cursor()

with open("config.json","r") as archivo:
    config = json.load(archivo)


with open("result.txt","w") as archivo:
    tittleList = (x["titulo"] for x in config["listas"].values())
    header = "\t".join(tittleList)+"\tno Voto"
    # print(f"\t{header}")
    archivo.write(f"\t"+header+"\n")
    for cursoTabla in config["cursos"].keys():
        cur.execute(f"SELECT votos FROM {cursoTabla}")
        result = cur.fetchall()
        total = sum(x[0] for x in result)
        row = f"{cursoTabla}\t"+"\t".join((str(x[0]) for x in result))+f"\t{config["cursos"][cursoTabla]-total}\n"
        archivo.write(row)
