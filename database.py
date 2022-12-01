import mysql.connector
import pyodbc
import time

# cnx = conexão com o banco
# cursor = manipulação do banco 

# cnx = mysql.connector.connect(user="root",
#                               password="pjTw&XK^tmkA", 
#                               host="localhost", 
#                               database="SAMP", 
#                               autocommit=True)

server = 'tcp:projetosamp.database.windows.net' 
database = 'SAMP' 
username = 'adminsamp' 
password = 'Projetosamp3'

cnx = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';ENCRYPT=yes;UID='+username+';PWD='+ password)
cnx.autocommit = True

def insert(query):
    linhas = None
    try:
        print(query)
        cursor = cnx.cursor()
        linhas = cursor.execute(query).rowcount
        cnx.commit()
        print(linhas)
    except mysql.connector.Error as error:
        print("ERRO {}".format(error))
    finally:
         return linhas




def select(query):
    dados = None
    try:
        print(query)
        cursor = cnx.cursor()
        cursor.execute(query)
        dados = cursor.fetchall() # retornando os dados do banco
    except mysql.connector.Error as error:
        print(f"Erro: {error}")
        dados = error
    finally:
        return dados

