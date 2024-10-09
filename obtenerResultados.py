import sqlite3
import json
import csv

con = sqlite3.connect("database.db")
cur = con.cursor()

with open("config.json","r") as archivo:
    config = json.load(archivo)


with open("result.txt","w") as archivo:
    with open('result.csv', mode='w', newline='', encoding='utf-8') as archivo_csv:
        write_csv = csv.writer(archivo_csv)
        total = [0 for _ in config["listas"]]
        total.append(0)
        tittleList = (x["titulo"] for x in config["listas"].values())
        tittleList = list(tittleList)
        l = ["lista"]
        l.extend(tittleList)
        l.append("no Voto")
        write_csv.writerow(l)
        header = "\t".join(tittleList)+"\tno Voto"
        archivo.write(f"\t"+header+"\n")
        # print(f"\t{header}")
        for cursoTabla in config["cursos"].keys():
            cur.execute(f"SELECT votos FROM {cursoTabla}")
            result = cur.fetchall()
            result = [x[0] for x in result]
            totalCurso = sum(result)
            ausentes =  config["cursos"][cursoTabla]-totalCurso
            for index,value in enumerate(result):
                total[index] += value
            if cursoTabla != "excepciones":
                total[-1] += ausentes
            row = f"{cursoTabla}\t"+"\t".join(str(x) for x in result)+f"\t{ausentes}\n"
            csvRow = ["",""]
            archivo.write(row)
            r = (row.replace("\n","").split("\t"))
            write_csv.writerow(r)
        t = f"Total\t"+"\t".join(str(x) for x in total)
        archivo.write(t)
        t_csv = t.split("\t")
        write_csv.writerow(t_csv)