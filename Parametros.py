import os
from entrada import Entrada
import tape

class Parametros:
    
    def receberParametros(self,parametros:dict):
        
        self.__valorUnico__(parametros)

        self.__preencheCards__(parametros)

        self.parametrosMultiplos['title'] = parametros['material'].replace('\n','')

        try:
            self.__tlabel__(parametros)
        except:
             self.parametrosMultiplos['tlabel'] = 'fita pendf para o material: ' + self.parametrosMultiplos['matb']

        self.__preencheEgn__(parametros)

        self.__preencheReac__(parametros)
    
    #Preenche as fitas de reação: mfd, mtd e mtname.
    def __preencheReac__(self, parametros):
        try:
            self.parametrosMultiplos['mfd'] = parametros['mfd'].split()
            self.parametrosMultiplos['mtd'] = parametros['mtd'].split()
            self.parametrosMultiplos['mtname'] = parametros['mtname'].split()
        except:
            self.parametrosMultiplos['mfd'] = parametros['mfd']
            self.parametrosMultiplos['mtd'] = parametros['mtd']
            self.parametrosMultiplos['mtname'] = parametros['mtname']

        self.parametrosMultiplos['mfd'] += '0'         

    #Pega o matb
    def setMatb(self, matb):
        self.parametrosSimples['matb'] = matb
    def getMatb(self):
        return self.parametrosSimples['matb']

    #Preenche a variável egn:
    def __preencheEgn__(self, parametros):

            #Só recebe a entrada 'igg' tiver habilitando.
            if int(self.parametrosSimples['igg']) == 0:
                try: 
                    self.parametrosMultiplos['egn'] = parametros['egn'][:-1]
                except:
                    pass
                
             #   if len(self.parametrosMultiplos['egn']) != int(self.parametrosSimples['ngn']) + 1:
             #       raise Exception("egn precisa ter ngn + 1 valores!")
        

    #Preenche valores simples
    def __valorUnico__(self, parametro):
        for chave in self.parametrosSimples:

            try:
                self.parametrosSimples[chave] = self.__remove__(parametro[chave])
            except:
                continue
                
    def __tlabel__(self, parametros):
        self.parametrosMultiplos['tlabel'] = self.__remove__(parametros['tlabel'])

    def __preencheCards__(self, parametros):
        #Se 
        try:
            quantidadeMaxima = int(parametros['ncards'])
            self.parametrosMultiplos['cards'] = [self.__remove__(card) for card in parametros['cards'].split('\n')[:quantidadeMaxima] if len(card) <= 60]
        except:
            self.parametrosMultiplos['cards'] = [["'processado pelo NJOY'"],["'Veja a original para mais detalhes'"]]
            self.parametrosMultiplos['ncards'] = '2' 
    
    def __remove__(self,string):
    
            inicio = string.find("'")
            fim = string.rfind("'")
    
            res = ''
    
            if inicio != -1 and inicio != fim:
               # print(' ' in string[:inicio+1])
                for letra in string[:inicio]:
                    if letra == ' ' or letra == '\n':
                        continue
                    res += letra
        
                res += string[inicio:fim+1]
        
                for letra in string[fim+1:]:
                    if letra == ' ' or letra == '\n':
                        continue
                    res += letra        

                return res
    
            for letra in string:
                if letra == ' ' or letra == '\n':
                    continue
                res += letra

            return res 

    def getParametros(self):
        parametro = dict(self.parametrosSimples, **self.parametrosMultiplos)

        return parametro

    #Parametors que têm um valor para cada material.
    parametrosSimples = {
    'matb': '0', 'ncards' : '0', 'ngrid' : '0', 'enode':'0' ,'err' : '.005', 'ntemp2' : '1','temp2':'0',
    'errthn' : '0.005','ign' : '3','igg' : '0' ,'iwt': '3','lord' : '3', 'ntemp' : '1', 'nsigz' : '1', 
    'iprint' : '1', 'sigz': '1.e+10', 'ngn' : ''
    }

    #Parametros que comportam diversos valores para um mesmo material.
    parametrosMultiplos = {'cards' : '', 'egn' : '', 'tlabel' : '', 'title' : '', 'mfd' :
    '', 'mtd' : '', 'mtname' : '', 'matd' : '0'
    }



class ParametrosAdmin:
    parametros = dict()
    padrao = None
    input = None


    def __init__(self, padrao, parametros:dict, inputNome):
        self.padrao = open(padrao,'r')
        self.parametros = parametros

        self.setInput(inputNome)

    #Transforma um iterável em uma string
    def __vetorPraString__(self, vetor, meio = ' '):
        result = ''

        for elemento in vetor[:-1]:
            result += str(elemento) + meio
        
        return result + str(vetor[-1]) + '/\n'

    def __card9__(self):
        card = ''

        #As variáveis de reação (card 9) possuem o mesmo tamamho, com a exceção de mfd que possue um a mais
        #para indicar o termino.

        tam = range(len(self.parametros['mfd']) - 1)

        for elemento in tam:

            card += self.parametros['mfd'][elemento] + ' '
            card += self.parametros['mtd'][elemento] + ' '
            card += self.parametros['mtname'][elemento] + '/\n'
        
        card += self.parametros['mfd'][-1] + '/\n'
        return card

    def setInput(self,intputNome):
        self.input = open(intputNome,'w')

    #Preenche uma única linha
    def __preencheLinha__(self, variaveis):
        
        #Card é uma coleção de valores atribuídas a variáveis no NJOY
        card = ''
        try:

            if variaveis[0] in ('mfd', 'mtd', 'mtname'):
                a = self.__card9__()

                return a 
        except:
            pass
        
        try:
            if isinstance(self.parametros[variaveis[0]], list):
                return self.__vetorPraString__(self.parametros[variaveis[0]],'/\n')
        except:
            pass

        for argumento in variaveis[:-1]:
            if argumento in self.parametros.keys():
                card += str(self.parametros[argumento]) + ' '
            else:
                card += argumento + ' '
            
        if variaveis[-1] in self.parametros.keys():
            if  self.parametros[variaveis[-1]] != '':
                return card + str(self.parametros[variaveis[-1]]) + '/\n'
            
            return card
        
        return card + variaveis[-1] + '\n'
        

    
    def preencherInput(self):
        
        for linha in self.padrao:

            entrada = linha.split()
            if entrada:
                argumentos = self.__preencheLinha__(linha.split())
            else:
                argumentos = self.__preencheLinha__(linha)
                
            self.input.write(argumentos) 

    def __del__(self):
        try:
            self.arquivo.close()
            self.intpu.close()
        except:
            pass





