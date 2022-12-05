import datetime
import time
from psutil import * # Importanto TODAS as funções da PSUTIL
import os
import platform # Biblioteca para acesso aos dados do sistema operacional da maquina
from database import insert, select 
import cpuinfo
from uuid import getnode as get_mac #Biblioteca para captirar o endereço mac da maquina
from random import randint #Gerando um número serial aleatorio
from http import server
from slack_sdk import WebClient
from pydoc import doc
import requests
import json
from json import loads
from urllib3 import PoolManager
import pyautogui
from pynput import keyboard


# Coletando qual o sistema operacional
sistema = platform.system()
numeroRegistros = 0
chamados = 0



chamados = 0

def abrirChamado(tokenPipefy, componente, serial, valorAtual, metrica):
    url = "https://api.pipefy.com/graphql"

    query = {"query": "{allCards(pipeId: 302763672) {edges {node {id title age done}}}}"}

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJ1c2VyIjp7ImlkIjozMDIwODY5MjUsImVtYWlsIjoiam9hby5jb25jZWljYW9Ac3B0ZWNoLnNjaG9vbCIsImFwcGxpY2F0aW9uIjozMDAyMDc0NzZ9fQ.SRZx-58-x8HKCSTanwLU7MzGVoenpQwrmFpDppWzJduSo8NDJKtAw65ECGCGWEOO_1SJ65LnacQmgQ0aEIunXA"
    }

    response = requests.post(url, json=query, headers=headers)
    jason = response.text
    data = loads(jason)

    dados = data['data']['allCards']['edges']

    if valorAtual < metrica:
        problema = f'A {componente} está acima de {metrica}%!'
    elif valorAtual > metrica:
        problema = f'A {componente} está abaixo de {metrica}%!'

    temIgual = False
    i = 0
    while i < len(dados):
        age = dados[i]['node']['age']
        titulo = dados[i]['node']['title']
        feito = dados[i]['node']['done']
        if age >86400 and titulo == problema and feito == False:
            temIgual = True
        i += 1
    payload = {'query':  'mutation{createCard(input: {pipe_id:302763672, title: "Novo Card", fields_attributes: [{field_id: "qual_o_serial_da_m_quina", field_value: "%s"} {field_id: "qual_o_componente_afetado", field_value: "%s"}{field_id: "problema", field_value: "%s"}{field_id: "mais_informa_es", field_value: "A %s da máquina de serial %s atingiu um uso de %.2f. Valor fora do limite estabelecido de %.2f"}]}){card {title}}}' % (serial, componente, problema, componente, serial, valorAtual, metrica)}

    if temIgual:
        print('o card ja existe')
    else:
        criar = requests.post(url, json=payload, headers=headers)

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
    print("\033[1mTotal de RAM :\033[0m", memoriaTotal)
    print("\033[1mTempo gasto pelo usuário no computador desde a última vez em que foi ligado:\033[0m", tempoGasto)

    input("\n\n\033[1mPressione Enter para prosseguir...\033[0m")
    return 0 


  # Insert no banco a cada 20s definidos no time.sleep      
def insertPeriodico(tokenPipefy,idMaquina, serialMaquina):
    global numeroRegistros
    metricaCpu = select(f"select capturaMin, capturaMax from metrica join componente on idMetrica = fkMetrica where fkMaquina = {idMaquina[0]} and nomeComponente like 'CPU%'")
    metricaRam = select(f"select capturaMin, capturaMax from metrica join componente on idMetrica = fkMetrica where fkMaquina = {idMaquina[0]} and nomeComponente like 'RAM%'")
    if len(metricaRam) <= 0 or len(metricaCpu) <= 0:
        print(f"Atenção, esta máquina possui componentes que não têm métricas cadastradas! Portanto, não será capaz de abrir chamados\n Para atribuir métricas acesse a dashboard do site")
        time.sleep(5)
    idUsuario = select(f'select idUsuario from usuario join empresa on idEmpresa = usuario.fkEmpresa join maquina on idEmpresa = maquina.fkEmpresa where idMaquina = {idMaquina[0]};')
    
    inicio = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def on_press(key):
        try:
            if key.char == "s":
                insert(f"insert into Relatorio (fkUsuario, fkMaquina, numeroRegistros, numeroAlertas, inicio, fim) values({idUsuario[0][0]}, {idMaquina[0]}, {numeroRegistros}, {chamados}, '{inicio}', '{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}')")
                print("Encerrando API...")
                pyautogui.hotkey("Ctrl","c")
        except AttributeError:
            key
    while True:
        
            with keyboard.Listener(
                on_press=on_press) as listener:
        
                usoAtualMemoria = virtual_memory().percent
                usoCpuPorc = cpu_percent()
            
                
                if len(metricaRam) > 0 or len(metricaCpu) > 0:
                    if usoAtualMemoria > metricaRam[0][1]:
                        # client = WebClient('xoxb-4249231777856-4222605250757-vF1PjiBsrzxVo2rtfjGY4CDi')
                        # response = client.chat_postMessage(channel = 'C046JHG2RPF', text = 'ALERTA! Uso da memória RAM acima de 80%!')
                    
                        abrirChamado(tokenPipefy, 'RAM', serialMaquina, usoAtualMemoria, metricaRam[0][1])
                    if usoCpuPorc > metricaCpu[0][1]:
                        # client = WebClient('xoxb-4249231777856-4222605250757-vF1PjiBsrzxVo2rtfjGY4CDi')
                        # response = client.chat_postMessage(channel = 'C046JHG2RPF', text = 'ALERTA! Uso da CPU acima de 80%!')
                        abrirChamado(tokenPipefy, 'CPU', serialMaquina, usoAtualMemoria, metricaCpu[0][1])    

                    if usoAtualMemoria < metricaRam[0][0]:
                        # client = WebClient('xoxb-4249231777856-4222605250757-vF1PjiBsrzxVo2rtfjGY4CDi')
                        # response = client.chat_postMessage(channel = 'C046JHG2RPF', text = 'ALERTA! Uso da memória RAM abaixo de 5%!')
                        abrirChamado(tokenPipefy, 'RAM', serialMaquina, usoAtualMemoria, metricaRam[0][0])    

                    if usoCpuPorc < metricaCpu[0][0]:
                        # client = WebClient('xoxb-4249231777856-4222605250757-vF1PjiBsrzxVo2rtfjGY4CDi')
                        # response = client.chat_postMessage(channel = 'C046JHG2RPF', text = 'ALERTA! Uso da CPU abaixo de 5%!')
                        abrirChamado(tokenPipefy, 'CPU', serialMaquina, usoAtualMemoria, metricaCpu[0][0])


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

                dataHora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                marcaCpu = 'CPU ' + cpuinfo.get_cpu_info()['brand_raw']
                query = f"INSERT INTO Dados (registro, momento, fkComponente) VALUES ({usoCpuPorc}, '{dataHora}', (select idComponente from componente where nomeComponente = '{marcaCpu}' and fkMaquina = {idMaquina[0]})), ({usoAtualMemoria}, '{dataHora}', (select idComponente from componente where nomeComponente = 'RAM' and fkMaquina = {idMaquina[0]})), ({usoDisco}, '{dataHora}', (select idComponente from componente where nomeComponente = 'Disco {particoes[0]}\\' and fkMaquina = {idMaquina[0]}));"
                

                insert(query)
                
                numeroRegistros += 1
                time.sleep(4)
