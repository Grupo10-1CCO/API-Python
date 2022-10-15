import getpass
import os
import time
from database import *
from functions import codeCleaner, conversao_bytes, insertPeriodico, randomSerial
import cpuinfo
from psutil import *
import platform


def login():
    os.system(codeCleaner)
    print('\033[1mLogin\033[0m \n\n')
    email = input("E-mail: ")
    senha = getpass.getpass("Senha: ")

    query = f"select * from usuario where email = '{email}' and senha = md5('{senha}');"
    
    dados = select(query)

    if type(dados) == type(None):
        print('\033[1mFalha no login\033[0m\n\nUsuário ou senha inválidos')
        time.sleep(2)
        login()

    else: 
        os.system(codeCleaner)
        print("\033[1mSucesso no Login\033[0m\n\nLogin feito com sucesso\nAbrindo menu inicial...\n")
        
        # ALGUEM CORRIGI ISSO AQ QUANDO TIVER TEMPO
        idMaquina = select(f"select idMaquina from maquina where fkEmpresa = 1")
        time.sleep(2)
        insertPeriodico(idMaquina)
        return dados



def cadastro():
    os.system(codeCleaner)
    print('\033[1mCadastro\033[0m \n\n')
    nome = input("Nome: ")
    email = input("E-mail: ")
    senha = getpass.getpass("Senha: ")
    confSenha = getpass.getpass("Confirme a senha: ")

    if senha == confSenha:
        verifExistente = f"SELECT * FROM usuario where email = '{email}'"
        
        

        retorno = select(verifExistente)
        
        time.sleep(5)
        if retorno == None:
            query = f"INSERT INTO Usuario VALUES (NULL, '{nome}', '{email}', MD5('{senha}'), 'Responsável', 1);"
            resultadoInsert = insert(query)
            os.system(codeCleaner)
            print(resultadoInsert)
            time.sleep(3)
            if resultadoInsert == 1:
                print('\033[1mCadastro\033[0m\n\nCadastro realizado com sucesso!')
                time.sleep(2)
                os.system(codeCleaner)
                print("Para prosseguir é necessário que recolhamos algumas informações sobre sua máquina... \n\n Aguarde alguns instantes enquanto esse processo é realizado.\n\n")
                queryId = f"SELECT idEmpresa FROM Empresa where idEmpresa = (select fkEmpresa from Usuario where email ='{email}' and senha = MD5('{senha}'));"
                dados = select(queryId)
                idEmpresa = dados[0]
                
                dados = cadastroComponentes(idEmpresa)
                if dados:
                    
                    return 0
                else:
                    print('Ocorreu um erro')
                    time.sleep(3)
                    cadastro()


        else:
            print('Username já é utilizado!')
            time.sleep(2)
            cadastro()

    else:
        print("As senhas não coincidem.")
        time.sleep(1)
        cadastro()



def cadastroComponentes(idEmpresa):
    
    sistema = platform.system()

    particoes = []
    if sistema == "Windows":
        for part in disk_partitions(all=False): # identificando partições
            if part[0] == "F:\\":
                break
            else:
                particoes.append(part[0])
    elif sistema == "Linux":
        particoes.append("/")

    porcentagemOcupados = []
    for j in particoes:
        porcentagemOcupados.append(disk_usage(j).percent)

    freqCpu = f'{round(cpu_freq().max, 2)}Mhz'
    freqMinCpu = f'{cpu_freq().min, 2}Mhz'
    qtdCores = cpu_count()
    qtdThreads = cpu_count(logical=False)
    processador = 'CPU ' + cpuinfo.get_cpu_info()['brand_raw']
    discoPrincipal = particoes[0]
    capacidadeDiscoPrincipal = porcentagemOcupados[0]
    memoriaTotal = f'{conversao_bytes(virtual_memory().total, 3)}GB'

    arquitetura = cpuinfo.get_cpu_info()['arch']
    if arquitetura == "X86_32":
        arquitetura = "32 bits"
    elif arquitetura == "X86_64":
        arquitetura = "64 bits"

    
    serial = randomSerial()
   

  
    #query = f"INSERT INTO maquina VALUES ('{serial}', {idUsuario}, '{sistema}', '{processador}', {qtdCores}, {qtdThreads}, '{freqCpu}', '{freqMinCpu}', '{memoriaTotal}', '{discoPrincipal}\\', '{capacidadeDiscoPrincipal}')"
    query = f"insert into maquina values(NULL, '{serial}','Meu pc', {idEmpresa})"
    retorno = insert(query)
    
    idMaquina = select(f"select idMaquina from maquina where serialMaquina = '{serial}'")
    #query4 = f"insert into metrica values(NULL, {freqMinCpu}, {freqCpu}),(NULL, 0, {memoriaTotal}), (NULL, 0, {capacidadeDiscoPrincipal})"
    #query2 = f"insert into medida values(NULL, '%'), (NULL, 'Ghz'), (NULL, 'Gb')"
                 
    if sistema == "Windows":
        print("Processador: " + processador)
        print("ID máquina: " + str(idMaquina[0]))
        print("Memoria RAM " +conversao_bytes(virtual_memory().total, 3))
        print("Disco Principal " +discoPrincipal)
        print("Tamanho Disco " + str(capacidadeDiscoPrincipal))
        time.sleep(18)
        query3 = f"insert into componente values (NULL, '{processador}', NULL, {idMaquina[0]}, NULL, 1), (NULL, 'RAM', {conversao_bytes(virtual_memory().total, 3)}, {idMaquina[0]},  NULL, 1),(NULL, 'Disco {discoPrincipal}\\', {capacidadeDiscoPrincipal}, {idMaquina[0]}, NULL, 1)" 
        print(query3)
        time.sleep(10)
    elif sistema == "Linux":
        query3 = f"insert into componente values (NULL, '{processador}', {idMaquina[0]}, NULL, 1), (NULL, 'RAM', {idMaquina[0]}, NULL, 1),(NULL, 'Disco {discoPrincipal}', {idMaquina[0]}, NULL, 1)" 


    time.sleep(2)

    idExport = idMaquina[0]
    #retorno2 = insert(query2)
    retorno3 = insert(query3)

    print(f"{retorno} 1")
    #print(f"{retorno2} 2")
    print(f"{retorno3} 3")
    
    

    if (retorno > 0) and (retorno3 >0):
        print("Cadastro dos componentes realizado com sucesso, seu cadastro está completo.")
        time.sleep(2)
        return True
    else:
        print(f"{retorno} 4")
        #print(f"{retorno2} 5")
        print(f"{retorno3} 6")
        print("erro")
        time.sleep(2)
        return False
