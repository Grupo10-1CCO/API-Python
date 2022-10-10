import datetime
import time
from psutil import * # Importanto TODAS as funções da PSUTIL
import os
import platform # Biblioteca para acesso aos dados do sistema operacional da maquina
from database import insert, select 
import cpuinfo
from uuid import getnode as get_mac #Biblioteca para captirar o endereço mac da maquina
from random import randint #Gerando um número serial aleatorio

# Coletando qual o sistema operacional
sistema = platform.system()

# Definindo o comando para o terminal
if sistema == "Windows":
    codeCleaner = "cls"
elif sistema == "Linux":
    codeCleaner = "clear"

# Gerando um número serial aleatório
def randomSerial():
    num = randint(100000000,999999999)
    serial = "BRJ" + str(num)
    return serial

# Função para converter bytes em KB, MB ou GB
def conversao_bytes(valor, tipo):
    if tipo == 1:  # KB
        return valor / 1024
    elif tipo == 2:  # MB
        return valor / 1024 / 1024
    elif tipo == 3:  # GB
        return f'{valor / 1024 / 1024 / 1024: .2f}'

# 
def monitorar():
    while (True):
        try:
            os.system(codeCleaner)
            # MEMORIA RAM
            memoriaTotal = f'{conversao_bytes(virtual_memory().total, 3)}GB'
            memoriaDisponivel = f'{conversao_bytes(virtual_memory().available, 3)}GB'
            memoriaEmUsoPerc = virtual_memory().percent
            usoAtualMemoria = f'{conversao_bytes(virtual_memory().used, 3)}GB'

            # CPU
            usoCpuPorc = f'{cpu_percent()}%'
            usoPorCore = cpu_percent(percpu=True)


            # DISCO
            # o vetor partições serve para armazenar as divisões do disco na maquina
            # Exemplo: Cado tenhas mais de um disco (E:, C: e D:), a estrutura de decisão armazena a identificação dos disco em partições
            particoes = []
            if sistema == "Windows":
                for part in disk_partitions(all=False): # identificando partições
                    if part[0] == "F:\\":
                        break
                    elif part[0] == "E:\\":
                        break
                    else:
                        particoes.append(part[0])
            elif sistema == "Linux":
                particoes.append("/")

            # Coletando o uso em cada partição 
            porcentagemOcupados = [] 
            for j in particoes:
                porcentagemOcupados.append(disk_usage(j).percent) 


            # Print parte da memória
            print("\033[1mInformações de memória\033[0m\n")
            print("\033[1mTotal:\033[0m", memoriaTotal)
            print("\033[1mMemória Disponível:\033[0m", memoriaDisponivel)
            print("\033[1mUso atual:\033[0m", usoAtualMemoria)
            print("\033[1mPorcentagem de uso:\033[0m", memoriaEmUsoPerc)

            print("\n", "-" * 100, "\n")

            # Print CPU
            print("\033[1mInformações de CPU\033[0m\n")
            print("\033[1mUso total:\033[0m ", usoCpuPorc)

            print("\033[1mUso por core:\033[0m")
            
            # A Função enumarate() é semelhnate ao JSON, pois sua formatação permite que selecionemos os indices 
            for i in enumerate(usoPorCore):
                print(f'CPU_{i[0]}: {i[1]}%')

            print("\n", "-" * 100, "\n")

            # Print disco
            print("\033[1mInformações do disco\033[0m\n")
            print("\033[1mPartições encontradas:\033[0m ")

            for i in enumerate(particoes):
                print(f"Uso da partição {i[1]}: {porcentagemOcupados[0]}")

            print("\n\nAperte ctrl + c para retornar")


            time.sleep(1)
        except KeyboardInterrupt:
            return "0"

    # 
def info():
    os.system(codeCleaner)
    
    # Capturando valores os dados da CPU através da PSUTIL
    freqCpu = f'{round(cpu_freq().max, 0)}Mhz'
    qtdCores = cpu_count()
    qtdThreads = cpu_count(logical=False)
    tempoGasto = f"{round(cpu_times().user / 60 / 60, 2)} Horas"
    processador = cpuinfo.get_cpu_info()['brand_raw']

    # Capturando os dados de arquitetura da maquina
    arquitetura = cpuinfo.get_cpu_info()['arch']
    if arquitetura == "X86_32":
        arquitetura = "32 bits"
    elif arquitetura == "X86_64":
        arquitetura = "64 bits"
        # Endereço mac
        mac = get_mac() #numero do mac

    # Editando a o numero do endereço mac em forma de string
    macString = ':'.join(("%012X" % mac) [i:i+2] for i in range(0,12,2))

    
    versaoSistemas = platform.version()
    memoriaTotal = f'{conversao_bytes(virtual_memory().total, 3)}GB'

    print("\033[1mInformações sobre o computador\033[0m\n\n")

    print("\033[1mSistema Operacional\033[0m", sistema)
    print("\033[1mVersão do sistema\033[0m", versaoSistemas)
    print("\033[1mMac Address\033[0m", macString)
    print("\033[1mArquitetura: \033[0m", arquitetura)
    print("\033[1mProcessador:\033[0m", processador)
    print("\033[1mQuantidade total de núcleos do processador:\033[0m", qtdCores)
    print("\033[1mQuantidade de Threads:\033[0m ", qtdThreads)
    print("\033[1mFrequência do processador:\033[0m ", freqCpu)
    print("\033[1mTotal de RAM :\033[0m", memoriaTotal)
    print("\033[1mTempo gasto pelo usuário no computador desde a última vez em que foi ligado:\033[0m", tempoGasto)

    input("\n\n\033[1mPressione Enter para prosseguir...\033[0m")
    return 0 


  # Insert no banco a cada 20s definidos no time.sleep      
def insertPeriodico(idMaquina):
    while True:
            usoAtualMemoria = virtual_memory().percent
            usoCpuPorc = cpu_percent()
            freqCpu = round(cpu_freq().current,0)

            particoes = []
            if sistema == "Windows":
                for part in disk_partitions(all=False): # identificando partições
                    if part[0] == "F:\\":
                        break
                    elif part[0] == "E:\\":
                        break
                    else:
                        particoes.append(part[0])
            elif sistema == "Linux":
                particoes.append("/")


            porcentagemOcupados = [] 
            for j in particoes:
                porcentagemOcupados.append(disk_usage(j).percent) 

            usoDisco = porcentagemOcupados[0]

            dataHora = datetime.datetime.now()
            marcaCpu = 'CPU ' + cpuinfo.get_cpu_info()['brand_raw']
            query = f"INSERT INTO Dados VALUES(NULL, {usoCpuPorc}, '{dataHora}', (select idComponente from componente where nomeComponente = '{marcaCpu}' and fkMaquina = {idMaquina[0]})), (NULL, {usoAtualMemoria}, '{dataHora}', (select idComponente from componente where nomeComponente = 'RAM' and fkMaquina = {idMaquina[0]})), (NULL, {usoDisco}, '{dataHora}', (select idComponente from componente where nomeComponente = 'Disco {particoes[0]}\\' and fkMaquina = {idMaquina[0]}));"
            

            insert(query)
            print(query)

            time.sleep(4)


# CAPTURA TODOS OS DADOS NOVAMENTE E GERA UM TXT COM OS DADOS
def relatorio():
    os.system(codeCleaner)

    hora = datetime.datetime.now() # Momento do registro
    # with open usando w = sobreescrever ou entao criar um arquivo novo, do 0
    with open('DadosMaquina.txt','w', encoding='utf-8') as arquivo: #UTF-8 teclado brasileiro
        arquivo.write("Data e hora do momento que foi salvo os dados:\n" + str(hora))


    versaoSistemas = platform.version()
    arquitetura = cpuinfo.get_cpu_info()['arch']
    if arquitetura == "X86_32":
        arquitetura = "32 bits"
    elif arquitetura == "X86_64":
        arquitetura = "64 bits"

        mac = get_mac()
    macString = ':'.join(("%012X" % mac) [i:i+2] for i in range(0,12,2))
    tempoGasto = f"{round(cpu_times().user / 60 / 60, 2)} Horas" # Tempo que o computador esteve ligado
    processador = cpuinfo.get_cpu_info()['brand_raw']
    with open('DadosMaquina.txt','a', encoding='utf-8') as arquivo: # WITH OPEN COM A = CONTINUAR ESCREVENDO NO FIM DO ARQUIVO!!!!!!!!!!!!!!!!!! | UTF = VOCE JA SABE
        arquivo.write("\n\n━━━━━ Informações do computador ━━━━━\n\nSistema operacional: {}\nVersão do sistema: {}\nMac Address: {}\nArquiterura: {}\nProcessador: {}\nTempo gasto do computador desde a última vez em que foi ligado: {}\n".format(sistema, versaoSistemas, macString, arquitetura, processador, tempoGasto))


    memoriaTotal = f'{conversao_bytes(virtual_memory().total, 3)}GB'
    memoriaDisponivel = f'{conversao_bytes(virtual_memory().available, 3)}GB'
    usoAtualMemoria = f'{conversao_bytes(virtual_memory().used, 3)}GB'
    memoriaEmUsoPerc = virtual_memory().percent
    with open('DadosMaquina.txt','a', encoding='utf-8') as arquivo:# WITH OPEN COM A = VOCE JA SABE | UTF = VOCE JA SABE TAMBEM
        arquivo.write("\n━━━━━ MEMÓRIA RAM ━━━━━\n\nMemória total: {} \nMemória disponivel: {} \nUso atual: {} \nPorcentagem de uso: {}%\n".format(memoriaTotal, memoriaDisponivel, usoAtualMemoria, memoriaEmUsoPerc))
    

    usoCpuPorc = f'{cpu_percent()}%'
    usoPorCore = cpu_percent(percpu=True)
    freqCpu = round(cpu_freq().current, 0)
    qtdCores = cpu_count()
    qtdThreads = cpu_count(logical=False)
    with open('DadosMaquina.txt','a', encoding='utf-8') as arquivo:# WITH OPEN COM A = VOCE JA SABE | UTF = VOCE JA SABE TAMBEM
        arquivo.write("\n━━━━━ CPU ━━━━━\n\nUso total: {}\nFrequência da CPU: {}Mhz\nQuantidade de núcleos: {}\nQuantidade de Threads: {}\nUso por core: {}\n".format(usoCpuPorc, freqCpu, qtdCores, qtdThreads, usoPorCore))
    

    particoes = []
    if sistema == "Windows":
        for part in disk_partitions(all=False): # identificando partições
            if part[0] == "F:\\":
                break
            elif part[0] == "E:\\":
                break
            else:
                particoes.append(part[0])
    elif sistema == "Linux":
        particoes.append("/")


    porcentagemOcupados = [] 
    for j in particoes:
        porcentagemOcupados.append(disk_usage(j).percent) 
    with open('DadosMaquina.txt','a', encoding='utf-8') as arquivo:# WITH OPEN COM A = VOCE JA SABE | UTF = VOCE JA SABE TAMBEM
        arquivo.write("\n━━━━━ Disco ━━━━━\n\nPartições: {} \nPorcentagem ocupada de cada partição: {}\n".format(particoes, porcentagemOcupados))


    print('Sucesso!!\n\nSeus dados foram salvos em um relatório chamado DadosMaquina.txt\n')
    input("\nPressione Enter para voltar ao menu...\n")
    return 0
