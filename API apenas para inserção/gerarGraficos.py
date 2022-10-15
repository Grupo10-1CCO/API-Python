import time
import matplotlib.pyplot as plt
import psutil
import cpuinfo
import os
import datetime # Biblioteca para capturar a data e hora da maquina
from database import select # Importando a função select para fazer select do banco de dados
from functions import conversao_bytes #Importando a função coversao_bytes para converter bytes para outras medidas
from functions import codeCleaner # Importando a função codeCleaner para limpar o terminal


# Indentificando o sitema operacional e direcionando o dirtório padrão 
# (se for Linux: /)
# (se for Windows: C:\\ )
if os.name == 'nt':
    sistem="C:\\"
    nome='Windows'
else:
    sistem="/"
    nome='Linux'

#Comentar por bloco 
def gerarGraficoDisco():
    uso_disco = psutil.disk_usage(sistem).used
    free_disco = psutil.disk_usage(sistem).free

    vt_dados_disco = []

    vt_dados_disco.append(uso_disco)
    vt_dados_disco.append(free_disco)

    label = []
    label.append('Espaço utilizado no disco: {}GB'.format(conversao_bytes(uso_disco, 3)))
    label.append('Espaço disponível no disco: {}GB'.format(conversao_bytes(free_disco, 3)))

    color = ['firebrick', 'limegreen']
    myexplode = [0.1, 0]

    os.system(codeCleaner)
    figura = plt.figure(figsize=(15,7))
    plt.pie(vt_dados_disco, autopct='%.1f%%', colors=color, explode=myexplode, textprops={'fontsize': 14})
    plt.legend(title='Dados', labels=label, loc='center right', bbox_to_anchor=(1.5, 0.6))
    plt.title ('Diagnóstico do disco')
    plt.show()

#Comentar em bloco
def gerarGraficoCpu(idMaquina):
    query = f"select captura, dataHoraRegistro from registro where fkComponente = (select idComponente from componente where nomeComponente = '{cpuinfo.get_cpu_info()['brand_raw']}' and fkMaquina = {idMaquina}) order by momento desc limit 8;"
    dados = []
    dados.append(select(query, True))

    usoCpuPorc = []
    #freqCpu = []
    dataHoraRegis = []

    for linha in select(query,True):
        usoCpuPorc.append(linha[0])
        #freqCpu.append(linha[1])
        data_format = linha[1].strftime("%d/%m \n %H:%M:%S")
        dataHoraRegis.append(data_format)
    
    dataHoraFormatado = dataHoraRegis[::-1]

    figura = plt.figure(figsize=(15,7))
    facecolor='blue'
    plt.plot(dataHoraFormatado, usoCpuPorc)
    plt.title ('Uso da CPU (%)')
    plt.show()

#Comentar em bloco
def gerarGraficoCpu2(idMaquina):
    query = f"select captura, dataHoraRegistro from registro where fkComponente = (select idComponente from componente where nomeComponente = '{cpuinfo.get_cpu_info()['brand_raw']}' and fkMaquina = {idMaquina}) order by momento desc limit 8;"
    dados = []
    dados.append(select(query, True))

    usoCpuPorc = []
    #freqCpu = []
    dataHoraRegis = []

    for linha in select(query,True):
        usoCpuPorc.append(linha[0])
        #freqCpu.append(linha[1])
        data_format = linha[1].strftime("%d/%m \n %H:%M:%S")
        dataHoraRegis.append(data_format)
    
    dataHoraFormatado = dataHoraRegis[::-1]

    figura = plt.figure(figsize=(15,7))
    facecolor='blue'
    plt.plot(dataHoraFormatado, usoCpuPorc)
    plt.title ('Uso da CPU (%)')
    plt.show()
    time.sleep(3)

#Comentar em bloco
def gerarGraficoMemoria(idMaquina):
    query = f"select captura, dataHoraRegistro from registro where fkComponente = (select idComponente from componente where nomeComponente = 'RAM' and fkMaquina = {idMaquina}) order by momento desc limit 8;"
    dados = []
    dados.append(select(query, True))

    usoMemoria = []
    dataHoraRegis = []

    for linha in select(query,True):
        usoMemoria.append(linha[0])
        data_format = linha[1].strftime("%d/%m \n %H:%M:%S")
        dataHoraRegis.append(data_format)

    dataHoraFormatado = dataHoraRegis[::-1]

    figura = plt.figure(figsize=(15,7))
    facecolor='blue'
    plt.plot(dataHoraFormatado, usoMemoria)
    plt.title ('Uso da Memória RAM (%)')
    plt.show()
