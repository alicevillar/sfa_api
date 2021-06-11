import pyodbc as p
import json as js
import os
from senhas import *

cnxn = p.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

with open("C:/Users/Alice/Desktop/provisorio/APOD_365") as file:
    data = js.load(file)
    #print(data[0]["date"])
    #data_json=data

size_json = len(data)
print(data[0].keys())


from requests import get
import json

PATH = os.path.abspath(os.path.dirname(__file__)) # This function receives a path and returns the absolute path on the pc
print(PATH)

for line in data:
    response = get(line['url'])
    #Separando a ultima parte da url, q contém no nome do arquivo. O primeiro parametro é o nome do arquivo e o segundo
    # (opcional) diz qual o modo de abertura do arquivo. Estou lendo um dado binário. Se não colocar o parâmetro ele presume que é leitura 'r'. 'wb' = write/binary
    print(line['url'])
    file=open("images/" + line['url'].split('/')[-1], 'wb')
    #escrevendo no arquivo a resposta da API
    file.write(response.content)
    file.close()
    #memorizando o caminho absoluto da imagem q acavou de ser baixada
    line['path_image'] = os.path.join(PATH, os.path.join('images', line['url'].split('/')[-1])) #essa função recebe dois parametros: o caminho a eh o PATH e o segundo será o caminho relativo da imagem
    print(line['path_image'])


# Populating the database tables
for line in data:
    print(line)
    sql=f"""
        INSERT INTO TB_SFA_Images (Ima_Date,Ima_Explanation,Ima_Title,Ima_Url) 
        values (?,?,?,?)"""
    cursor.execute(sql,(line['date'], line['explanation'], line['title'], line['path_image']))

# NOTE -> The last argument is not the url but the image itself.
# Thus, the user will not receive a link, but the real image :)

cursor.commit() # para de fato executar o comando

