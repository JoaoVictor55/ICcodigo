from Parametros import Parametros, ParametrosAdmin
import os
from entrada import Entrada
import tape
import webScraping
import json
from  macroCalculador import MacroSeccao
from time import sleep

def rodar(arquivoEntrada, caminho, tapes, outputNome, njoy):

   # arquivoEntrada = arquivoEntrada.replace('\n','')
   # arquivoEntrada = arquivoEntrada.replace(' ','')

    #caminho = caminho[0].replace("'",'')

    comeco = caminho.find("bin")
    comeco += 3

    njoyloco = njoy + 'njoy21'

    os.system("sudo mkdir "+caminho)
    
    comando = "sudo cp ./" + arquivoEntrada + " " + caminho
    os.system(comando)

    comando = "sudo cp "+njoyloco+ ' ' + caminho
    os.system(comando)

    for tape in tapes:
        os.system("sudo mv ./"+tape+" "+caminho)

  #  pwd = os.getcwd()

    os.chdir(caminho)

    #outputNome = outputNome[0].replace("'","")

    try:
        os.system("sudo rm "+ outputNome)
    except FileNotFoundError: pass
    comando = 'sudo ./njoy21 < ' + arquivoEntrada + ' -o ' + outputNome

    os.system(comando)

    sleep(2)

    #comando = 'sudo mv ./' + outputNome[0] + " " + pwd
    #os.system(comando)

    #sleep(2)

    #os.chdir(pwd)


def macro_seccao(outputNome, ingredientes, elementos,pwd):
    
    atual = os.getcwd()

    #comando = "sudo cp "+pwd+"/"+ingredientes+ " "+atual
    #comando2 = "sudo cp "+pwd+"/"+elementos+ " "+atual
    #os.system(comando)
    #os.system(comando2)

    macroSec = MacroSeccao(outputNome, material=pwd+"/"+ingredientes, elementos=pwd+"/"+elementos)

    macroSec.calcularMacroscopicaTotal()

    result = macroSec.returnMacroTotal()

    with open(pwd+"/"+"macroSaida" + outputNome+'.txt',"w") as macroSAIDA:

        indice = 0
        for elemento in result:
            for a in elemento:

                string = '['+str(indice)+']'+str(a)+'\n'

                macroSAIDA.write(string)
                indice += 1

            macroSAIDA.write("*************************************************************\n\n\n")
            indice = 0

def renomear(materiais_code):

    lista_tapes = list()
    contador = 20

    for chave in materiais_code:

        nome = 'tape'+str(contador)
        os.system('cp '+materiais_code[chave]+'.txt'+' '+nome)
        lista_tapes.append(nome)
        contador += 1

    return lista_tapes
def main(arquivoEntrada = "testeAki.txt", arquivoSaida = 'inputGeradoMAIN.txt', padrao = 'inputPraTestarGAMIRN.txt'):
    entradaInput = Entrada(arquivoEntrada)

    
    entradaInput.leia()
    entradaUser = entradaInput.getEntrada()

    materiais = webScraping.WebScraping(entradaUser['material'])

    tape20 = tape.Tape(materiais)
    tape20.procurarTAPE()

    parametro = Parametros()
    parametro.receberParametros(entradaUser)

    mats = tape20.obterMats()

    parametro.setMatb(list(mats.keys()))

    parametros = parametro.getParametros()

    entrada = ParametrosAdmin(padrao,parametros,arquivoSaida)
    entrada.preencheInput()

#entradaUser['caminho']
#entradaUser['output']
    return arquivoSaida, renomear(mats) 

if __name__ == "__main__":

    try:
        arquivoJson = input("Digite o nome do arquivo de configuração json\nOu ctrl + c para usar o padrão\n>")
        
        if not '.json' in arquivoJson: arquivoJson =+ '.json'
    except KeyboardInterrupt:

        arquivoJson = "configuracao.json"
        print("Usando nome configuração padrão")


    with open("configuracao.json", "r") as config:

        configuracao = json.load(config)

    njoy = configuracao['njoy']
    chaves = tuple(configuracao.keys())[1:]
    
    for elemento in chaves:
        
        pwd=os.getcwd()

        arquivoEntrada = configuracao[elemento]['arquivoEntrada']
        arquivoSaida = configuracao[elemento]['arquivoSaida']
        padrão = configuracao[elemento]['padrao']
        caminho = configuracao[elemento]['caminho']
        outputNome = configuracao[elemento]['output']

        entrada, tapes = main(arquivoEntrada, arquivoSaida,padrão)
        rodar(entrada,caminho,tapes, outputNome,njoy)

        try:
            ingredientes = configuracao[elemento]['ingredientes']
            elementos = configuracao[elemento]['elementos']

            macro_seccao(outputNome=outputNome, ingredientes=ingredientes, elementos=elementos,pwd=pwd)
        except KeyError: pass




