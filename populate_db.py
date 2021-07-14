import pyodbc as p
import json as js
import os
from senhas import *

#########################################################################################################
# ==> OWASP C3:Secure Database Access
#
# NOTE: Here we comply with OWASP by securing the access to the database considering:
# a) Secure queries: To protect against SQL injection we use ‘Query Parameterization’
# b) Secure configuration: we run the database in a docker container, which has connectivity restrictions
# c) Secure communication: we use Pyodbc, an open source Python module to communicate with the database.
#
#########################################################################################################

# Secure communication: Pyodbc to communicate with the database:
cnxn = p.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

with open("APOD_365") as file:
    data = js.load(file)

size_json = len(data)
print(data[0].keys())

from requests import get
import json

PATH = os.path.abspath(os.path.dirname(__file__)) # This function receives a path and returns the absolute path on the pc
print(PATH)

for line in data:
    response = get(line['url']) # Separating the last part of the url, which contains the filename.
    # The first parameter is the name of the file and the second (optional) tells the opening mode of the file.
    # I'm reading binary data. If you don't put the parameter it assumes that it reads 'r'. 'wb' = write/binary
    print(line['url'])
    file=open("images/" + line['url'].split('/')[-1], 'wb')
    #writing the API response to the file
    file.write(response.content)
    file.close()
    # This function takes two parameters: first is the PATH and the second will be the relative path of the image
    line['path_image'] = os.path.join(PATH, os.path.join('images', line['url'].split('/')[-1]))
    print(line['path_image'])

             #################### Populating the database tables#########################
for line in data:
    print(line)
    sql=f"""
        INSERT INTO TB_SFA_Images (Ima_Date,Ima_Explanation,Ima_Title,Ima_Url) 
        values (?,?,?,?)""" # To protect against SQL injection we use ‘Query Parameterization’
    cursor.execute(sql,(line['date'], line['explanation'], line['title'], line['path_image']))

# NOTICE -> The last argument is not the url but the image itself.
# Thus, the user will not receive a link, but the real image :)

cursor.commit() # to execute the command

