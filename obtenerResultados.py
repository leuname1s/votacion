import sqlite3
import json

con = sqlite3.connect("database.db")
cur = con.cursor()

with open("config.json","r") as archivo:
    config = json.load(archivo)


with open("result.txt","w") as archivo:
    total = [0 for _ in config["listas"]]
    total.append(0)
    tittleList = (x["titulo"] for x in config["listas"].values())
    header = "\t".join(tittleList)+"\tno Voto"
    # print(f"\t{header}")
    archivo.write(f"\t"+header+"\n")
    for cursoTabla in config["cursos"].keys():
        cur.execute(f"SELECT votos FROM {cursoTabla}")
        result = cur.fetchall()
        result = [x[0] for x in result]
        totalCurso = sum(result)
        ausentes =  config["cursos"][cursoTabla]-totalCurso
        for index,value in enumerate(result):
            total[index] += value
        total[-1] += ausentes
        row = f"{cursoTabla}\t"+"\t".join(str(x) for x in result)+f"\t{ausentes}\n"
        archivo.write(row)
    archivo.write(f"Total\t"+"\t".join(str(x) for x in total))