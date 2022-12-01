# Linha 3 a linha 12 = Importações de bibliotecas e funções de outros arquvios da API que são responsáveis por
# rodar a api, O QUE COMEÇAR COM IMPORT = Biblioteca, O QUE COMEÇAR COM FROM é de arquivo da própria API

from database import select
from psutil import * # Biblioteca que captura dados de componentes da maquina
import time # Biblioteca que utilizamos para parar o programa por X segundos
import os # Biblioteca que permite a utilização de comandos do SO em um terminal 'próprio', ela executa os comandos de forma própria
from functions import codeCleaner; # Função que limpa o terminal de comando 
from cadastroLogin import cadastro, login # Importando as funções do arquivo casdastroLogin, para realizar o cadastro e login
from dash import dashboard # Importando as funções do arquvio dash para executar a vizualição dos graficos no terminal
from functions import insertPeriodico # Importando a função do arquivo functions que faz insert dos dados de captura no banco
import threading #Biblioteca para pegar o serial number da maquina
from gerarGraficos import gerarGraficoCpu, gerarGraficoDisco, gerarGraficoCpu2, gerarGraficoMemoria 

# Importando as funções do arquivo gerarGraficos que utliza matplotlib.pyplotv para plotar gráficos

#Função que executa o menu no terminal
def menu(userId, nome, idMaquina):
    threading.Thread(target=insertPeriodico, kwargs={'idMaquina':idMaquina} ).start() # pesquisar sobre esta função

    os.system(codeCleaner)

    opcaoUser = input(f"\033[1mHardware Monitor\033[0m\n\n Bem vindo(a) {nome}!!\n\n[1] - Monitorar processos atuais da máquina \n[2] - Verificar informações sobre o dispositivo\n[3] - Análise de dados\n[4] - Documentar meus dados\n[5] - Sair\n\n\033[1mUsuário:\033[0m ")

    # Trazer informações dos componentes no terminal 
    while opcaoUser == "1":
        os.system(codeCleaner)
        res = input("\033[1tComo você deseja visualizar os dados?\033[0m \n\n[1] - Painel \n[2] - Informações detalhadas \n[3] - Sair\n\n\033[1mUsuário:\033[0m ")
        
        # Exibindo a dashboard no terminal
        if res == "1":
            print("Atenção, você está prestes a entrar no painel. Para sair pressione CTRL + C")
            time.sleep(2)
            opcaoUser = dashboard()
        #Informações detalhadas dos componentes
        elif res == "2":
            opcaoUser = monitorar()
        #Sair
        else:
            opcaoUser = "0"
            
    # Traz os dados gerais da maquina no terminal
    while opcaoUser == "2":
        opcaoUser = info()

    # Plotandos os graficos através do matplotlib.pyplotv
    while opcaoUser == "3":
        os.system(codeCleaner)
        res = input("\033[1mQual equipamento deseja efetuar a análise?\033[0m \n\n[1] - CPU \n[2] - Memória RAM \n[3] - Disco\n[4] - Sair\n\n\033[1mUsuário:\033[0m ")

        if res == "1":
            os.system(codeCleaner)
            res_cpu = input("\033[1mCPU\033[0m \n\n[1] - Porcentagem de uso \n[2] - Frequência \n[3] - Sair\n\n\033[1mUsuário:\033[0m ")
            if res_cpu == "1":
                os.system(codeCleaner)
                os.system(codeCleaner)
                print("Atenção! Preparando seus dados para análise...")
                time.sleep(2)

                gerarGraficoCpu(idMaquina)

            if res_cpu == "2":
                os.system(codeCleaner)
                
                os.system(codeCleaner)
                print("Atenção! Preparando seus dados para análise...")
                time.sleep(2)

                gerarGraficoCpu2(idMaquina)

        if res == "2":
            os.system(codeCleaner)
            
            os.system(codeCleaner)
            print("Atenção! Preparando seus dados para análise...")
            time.sleep(2)
            gerarGraficoMemoria(idMaquina)

        if res == "3":
            os.system(codeCleaner)
            print("Atenção! Preparando seus dados para análise...")
            time.sleep(2)
            gerarGraficoDisco()
        
        if res == "4":
            opcaoUser = "0"

    #Chamando a função relatorio() para registrar os dados capturadps em um documento .txt
    while opcaoUser == "4":
        opcaoUser = relatorio()
    while opcaoUser == "5":
        main()
        exit()
    while opcaoUser != 1 and opcaoUser != 2 and opcaoUser != 3 and opcaoUser != 4:
        menu(userId, nome, idMaquina)

# Função para exibir o menu de opções de login e cadastro
def main():
    os.system(codeCleaner)

    opcao1tela = input("\033[1mHardware Monitor - BEM VINDO \033[0m\n\n[1] - Entrar \n[2] - Cadastar máquina \n[3] - Sair\n\n\033[1mUsuário:\033[0m ")

    # Opção de login
    if opcao1tela == "1":
        dados = login()
        print(dados)
        time.sleep(10)
        userId = dados[0]
        nomeUser = dados[1]
        
        #INSERT PERIODICO APENAS PARA A INSERÇAO NO BANCO
        
        

    # Opção de cadastro
    elif opcao1tela == "2":
        cadastro()
        main()
    # Opção de sair
    elif opcao1tela == "3":
        print("Obrigado por utilizar nosso serviço!")
        time.sleep(1)
        exit()
    else: 
        print("Opção inválida.")
        main()

   # Exibindo arte  
print(r"""
         ___________
        ||         ||            _______
        ||  HDWR   ||           | _____ |
        || MONITOR ||           ||_____||
        ||_________||           |  ___  |
        |  + + + +  |           | |___| |
            _|_|_   \           |       |
        (_____)   \          |       |
                    \    ___  |       |
            ______  \__/   \_|       |
            |   _  |      _/  |       |
            |  ( ) |     /    |_______|
            |___|__|    /         
                \_____/

""") 

time.sleep(2)

# Chamando a função main quando iniciamos a aplicação (API)
main()