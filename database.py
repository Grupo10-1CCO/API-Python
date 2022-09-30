import mysql.connector

# cnx = conexão com o banco
# cursor = manipulação do banco 

cnx = mysql.connector.connect(user="sampUser",
                              password="samp", 
                              host="localhost", 
                              database="dadosMaquina", 
                              autocommit=True)

def insert(query): 
    try: # o comando try serve para verificar se toos os comandos serão executados de maneira exata, caso o contrário, ele para no momento em que detectou um erro, indo para o except que informa o erro.
        cnx.reconnect()
        cursor = cnx.cursor()
        cursor.execute(query)
    except mysql.connector.connector.Error as error:
        print("ERRO {}".format(error))
    finally: # Após a execução dos comandos acima, o finally fecha as conexões
        if cnx.is_connected():
            linhas = cursor.rowcount
            cursor.close()
            cnx.close()
            return linhas

def select(query, isAllRequested = False):
    try:
        cnx.reconnect()
        cursor = cnx.cursor()
        cursor.execute(query)
        if isAllRequested: # verificando se retornou do banco
            dados = cursor.fetchall() # retornando os dados do banco
        else:
            dados = cursor.fetchone()
    except mysql.connector.Error as error:
        print('Erro')
        dados = error
    finally:
        if cnx.is_connected():
            cursor.close()
            cnx.close()
            return dados

