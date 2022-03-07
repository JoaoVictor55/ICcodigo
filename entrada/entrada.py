import re
from sqlite3 import paramstyle

class Entrada:

    def __init__(self, arquivo_entrada):

        self.setArquivoEntrada(arquivo_entrada)

    #Define o arquivo que contém as entradas.
    def setArquivoEntrada(self,arquivo_nome):
        try:
            self.arquivo_entrada = open(arquivo_nome,"r")
        except:
            print("Arquivo não encontrado")
        else:
            self.parametros = dict()
      
    #Distingue na entrada o que é variável e o que é valor.
    def __formatador__(self,entrada:str):
        
        #Caractere que identifica um comentário.
        COMETARIO = '#'


        #A linha inteira é um comentário.
        if entrada[0] == COMETARIO:
            return -1, -1

        igual = entrada.find('=')


        #A linha não tem variável.
        if igual < 0:
            variavel = None
        else:
            variavel = entrada[:igual].replace(' ', '')

        cometario = entrada.rfind(COMETARIO)

        #A linha não tem valor.
        if cometario < 0:
            valor =  entrada[igual+1:]
        else:
            valor = entrada[igual+1:cometario]
        
        valor = self.__criaVetor__(valor)
      

        #Retorna: o nome da variável e seu valor.
        return variavel, valor
    
    #Ler as entradas encontradas em "arquivo_entrada".
    def leia(self):
        
        #Conta o número da linha
        posicao = 0

        entrada = self.arquivo_entrada.readlines()
        tamanho = len(entrada)
        indice = 0

        while  indice < tamanho:

            linha = entrada[indice]

            if "(" in linha and not ")" in linha:
                #Se encontrar um parênteses aberto, o programa deve continuar preenchendo a linha até encontrar o fim.
                parentese = 1 #Será 0 se todos os parênteses forem abertos e fechados.
                  
                while True:
                    indice += 1

                    #Percorre uma linha e verifica a paridade dos parênteses.
                    #Quando todos os parênteses estiverem fechados, "parentese" será zero e o while
                    #se encerra.
                    for letra in entrada[indice]:
                        if letra == "(":
                            parentese += 1
                        
                        if letra == ")":
                            parentese -= 1

                    linha += entrada[indice]
                    if not parentese:
                        indice += 1
                        break

                    
            indice += 1
            variavel, valor = self.__formatador__(linha)

            #Indica erro de sintaxe "variavel =" 
            if valor == None:
                print('Erro na linha ', posicao,' variável sem valor')
                return

            #Caso uma linha não contenha a variável, o valor é armazenado na anterior.
            if variavel == None:
               variavel = list(self.parametros.keys())[-1]

            
            try:
                self.parametros[variavel] += valor 
            except:
                self.parametros.setdefault(variavel, valor)

            posicao += 1
    
    def __del__(self):
        try:
            self.arquivo_entrada.close()
        except:
            pass

    def getEntrada(self):
        return self.parametros

    def __criaVetor__(self,string):

        #O usuário irá subdividir um parâmetro com '()' indicando que cada uma dessa subparte irá pertencer a um material diferente.
        #A função, então, recebe essa string e cria um vetor de acordo com o número de subpartes.
        
        #Retorna o conteúdo do vetor se ele tiver o tamanho 1. Do contrário, retorna a lista.
        if not "'" in string:
            return string.split()

        base = 0
        topo = 0
        res = []
        topo = string.find(')')
        string = string.replace("(","")

        if topo == -1:
            return self.split(string)


       # string = string[base:]
        #res.append(string[:topo].split())
        res.append(self.split(string[:topo]))

        while string:
            base = topo
            base += 1
            topo = string[base:].find(')')

            string = string[base:]

            if topo == -1:
             #   res.append(string.split())
              #  res.append(self.split(string))
                return res

            res.append(self.split(string[:topo]))
    
    def split(self, string):
        if not "'" in string:
            return string.split()

        base = 0
        topo = 0
        res = []
        base = string.find("'")

        string = string[base:]

        topo = string[1:].find("'")

        res = [string[:topo+1] + string[topo+1]]
       
        string = string[topo+2:]

        while True:

            base = string.find("'")
            #topo = string[base+1:].find("'")
            
            if base == -1: break

            string = string[base:]
            topo = string[1:].find("'")

            buffer = string[:topo+1] + string[topo+1]

            res.append(buffer)

            string = string[topo+2:]
        return res

    

#entrada = Entrada('testeAki.txt')

#print(entrada.getEntrada())

#entrada.leia()

#resultado = entrada.getEntrada()

#for chave in resultado:
#   print("[",chave,"]"," = ",resultado[chave])




        


