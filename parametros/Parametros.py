class Parametros:
    
    def receberParametros(self,parametros:dict):
        
        self.__valorUnico__(parametros)

        self.__preencheCards__(parametros)

       # self.parametrosMultiplos['title'] = parametros['material']

        self.__title__(parametros)

        self.__tlabel__(parametros)

        self.__preencheEgn__(parametros)

        self.__preencheEgg_(parametros)

        self.__preencheReac__(parametros)

    #Preenche title:
    def __title__(self, parametros):
        LIMITE = 81 #Quantidade máxima de caracteres.

        if 'title' in parametros.keys():
            self.parametrosMultiplos['title'] = parametros['title'][0][:LIMITE]
            return

        #Só há um material
        if isinstance(parametros['material'][0], str):
            self.parametrosMultiplos['title'] = parametros['material'][0]
            return

        title = parametros['material'][0][0].replace("'",'')
        meteriais = parametros['material'][1:]
    
        
        for material in meteriais[:-1]:
            title += ', ' + material[0].replace("'",'')
        
        title += ' e ' + parametros['material'][-1][0].replace("'",'')

        self.parametrosMultiplos['title'] = "'" + title[:LIMITE] + "'"


    
    #Preenche as fitas de reação: mfd, mtd e mtname.
    def __preencheReac__(self, parametros):

        try:

            #if  len(parametros['mfd']) == 1:
            #    parametros['mfd'] = list(parametros['mfd'])
            #    parametros['mfd'] = list(parametros['mtd'])

            self.parametrosMultiplos['mfd'] = parametros['mfd']
            self.parametrosMultiplos['mtd'] = parametros['mtd']
            self.parametrosMultiplos['mtname'] = parametros['mtname']

            self.parametrosMultiplos['mfd'].append('0')
        except:
            pass

    #Pega o matb e define o nome dos arquivos de saída e entrada
    def setMatb(self, materiais):
        self.parametrosSimples['matb'] = materiais

        #Ordem dos arquivos; (nin nout) (nout npend) (npendf nout nout+1) (npendf nout+1 ngout1 = 0
        # ngout2) (nout+1 nout+1)

        #Gera uma lista para ser armazenada de nomes para as "tapes20" dos materiais
        self.parametrosMultiplos['nin'] = list()
        tamanho = len(self.parametrosSimples['matb'])
        for tape in range(tamanho):
            self.parametrosMultiplos['nin'].append(tape + 20)
        
        proximo = self.parametrosMultiplos['nin'][-1] + 1

        #Gera o nome para nout:
        self.parametrosSimples['nout'] =  str((proximo) * -1 )

        #Gera o nome para npend
        proximo += 1
        self.parametrosSimples['npend'] = str(proximo * (-1))

        #Gera o nome para nout + 1
        proximo += 1
        self.parametrosSimples['nout1'] = str(proximo * (-1))

        #Gera o nome para ngout + 1 + 1
        proximo +=1
        self.parametrosSimples['ngout2'] = str(proximo * (-1))
        
        #As unidades abaixo não são usadas nos problemas

        #Gera o nome para npendf
        #proximo += 1
        #self.parametrosSimples['npendf'] = str(proximo * (-1))

        ##Gera o nome para nout
        ##proximo += 1
       # self.parametrosSimples['nout'] = proximo * (-1)

        ##Gera o nome para nout2
        #proximo += 1
        #self.parametrosSimples['nout2'] = str(proximo)

    def getNin(self): #retorna o nin para renomear os arquivos ENDF
        return self.parametrosMultiplos['nin']

    def getMatb(self):
        return self.parametrosSimples['matb']
    
    #Preenche a variável egn:
    def __preencheEgn__(self, parametros):

            #Só recebe a entrada se 'ign' tiver habilitando.
            if self.parametrosSimples['ign'] == '1':

                #A quantidade de grupos deve ser igual ao valor de ngn
                self.parametrosMultiplos['egn'] = parametros['egn'] 

                self.parametrosSimples['ngn'] = str(len(self.parametrosMultiplos['egn']) - 1)
    
    #Preenche egg
    def __preencheEgg_(self, parametros):
            #Só recebe a entrada se 'igg' tiver habilitando.
            if self.parametrosSimples['igg'] == '1':

                #A quantidade de grupos deve ser igual ao valor de ngn
                self.parametrosMultiplos['egg'] = parametros['egg'] 

                self.parametrosSimples['ngg'] = str(len(self.parametrosMultiplos['egg']) - 1)

 
    #Preenche valores simples
    def __valorUnico__(self, parametro):
        for chave in self.parametrosSimples:

            try:
                #Variáveis terão apenas um valor.
                self.parametrosSimples[chave] = parametro[chave][-1]
            except:
                continue
                
    def __tlabel__(self, parametros):
        buffer = None
        LIMITE = 67
        try:
            self.parametrosMultiplos['tlabel'] = parametros['tlabel'][0][:LIMITE]
        except:
            buffer = 'fita pendf para o(s) material(is): '

            if len(parametros['material']) == 1:
                self.parametrosMultiplos['tlabel'] = buffer + parametros['material'][0].replace("'","")
                self.parametrosMultiplos['tlabel'] = "'" + self.parametrosMultiplos['tlabel'] + "'"
                return

            for material in parametros['material'][:-1]:
                buffer += material[0].replace("'","") + ', '
            
            buffer += parametros['material'][-1][0].replace("'","")

            
            self.parametrosMultiplos['tlabel'] = "'" + buffer[:LIMITE] + "'"

    def __preencheCards__(self, parametros):
        try:
            self.parametrosMultiplos['cards'] = parametros['cards']
        except:
            self.parametrosMultiplos['cards'] = ["'processado pelo NJOY'","'Veja a original para mais detalhes'"]
            self.parametrosMultiplos['ncards'] = '2'
            return

        #self.parametrosMultiplos['ncards'] = parametros['ncards']

        self.__verificarLimite__()

    def __verificarLimite__(self):
        LIMITE = 60
        #Verifica se o tamanho das strings em 'card' têm no máximo LIMITE caracteres

        tamanho = len(self.parametrosMultiplos['cards'])
        tam = range(tamanho)
        elemento = 0
    
        self.parametrosMultiplos['ncards'] = []

        if isinstance(self.parametrosMultiplos['cards'][0], list):
            while elemento in tam:
                self.parametrosMultiplos['cards'][elemento] = [card for card in self.parametrosMultiplos['cards'][elemento][:LIMITE]]
                
                #Conta a quantidade de cards
                self.parametrosMultiplos['ncards'].append(str(len(self.parametrosMultiplos['cards'][elemento]))) 
                elemento+=1
            
        else:
            self.parametrosMultiplos['ncards'] = str(tamanho)
            while elemento in tam:
                self.parametrosMultiplos['cards'][elemento] = self.parametrosMultiplos['cards'][elemento][:LIMITE]
                elemento+=1

    def getParametros(self):
        parametro = dict(self.parametrosSimples, **self.parametrosMultiplos)

        return parametro

    #Parametors que têm um valor para cada material.
    parametrosSimples = {
    'matb': '0', 'ngrid' : '0', 'enode':'0' ,'err' : '.005', 'ntemp2' : '1','temp2':'0',
    'errthn' : '0.005','ign' : '3','igg' : '3' ,'iwt': '3','lord' : '3', 'ntemp' : '1', 'nsigz' : '1', 
    'iprint' : '1', 'sigz': '1.e+10', 'ngn' : '', 'nendf' : None, 'npend' : None,
    'nout' : None, 'ngout1' : '0', 'ngout2' : None, 'nout2' : None, 'ngg' : ''
    }

    #Parametros que comportam diversos valores para um mesmo material.
    parametrosMultiplos = {'cards' : '', 'egn' : '', 'tlabel' : None, 'title' : None, 'mfd' :
    '30', 'mtd' : '1', 'mtname' : ['total'], 'matd' : '0', 'ncards' : '0', 'nin' : None, 'egg' : ''
    }



class ParametrosAdmin:
    parametros = dict()
    padrao = None
    input = None
    modeloInput = None
    quantidade = None #Quantidade de repetições
    ponteiroLaco = 0 #Aponta para um material.
    quantidadeRestante = None
    def __init__(self, padrao, parametros, inputGerado = 'inputGerado.txt') -> None:
        
        padrao = open(padrao,'r')
        self.input = open(inputGerado, 'w')

        self.parametros = parametros

        self.modeloInput = padrao.readlines()

        self.__inicializarLaco__()

        padrao.close()

    def printPadrao(self):
        for a in range(len(self.modeloInput)):
            print(self.modeloInput[a])

    def __obterParametros__(self, chave):
        pass
        

    def preencheInput(self):

        ponteiro = 0 #Indice do modeloInput
        ponteiroLaco = 0 #Indice dos laços internos dos parâmetros.
        comando = None #Corresponde a uma linha do modeloInput
        quantidade = self.quantidade #Quantidade de vezes que devemos repetir os parâmetros. É igual
        #número de elementos

        while True:
            
            #Pega uma linha no modelInput
            comando = self.modeloInput[ponteiro].split()

            #STOP indica o fim dos comandos no NJOY
            if comando[0] == 'STOP':
                self.input.write('STOP')
                self.input.close()
                break
            
                
            valor = self.__preencheLinha__(comando, self.ponteiroLaco)
            if valor != None:
                self.input.write(valor)

            #Repita é utilizado para pegar parâmetros para diversos materiais. A cada novo material
            #Adicionado, a pilha volta para pegar novos parâmetros.
            if comando[0] == 'VOLTE':
                
                #Repita tem o modelo: VOLTE POSICAO                
                if quantidade > 0:
                 #   print(comando)
                    ponteiro = int(comando[1])
                    self.ponteiroLaco += 1
                    quantidade -= 1
                    continue
                else:
                    self.ponteiroLaco = 0
                    quantidade = self.quantidade
                    self.input.write('0/\n')
            
         #   print(comando)
            ponteiro += 1
    
    #Inicializa as variaveis que indicam a quantidade de repetições.
    def __inicializarLaco__(self):
        
        matb = self.parametros['matb']

        self.quantidade = len(matb) - 1

        #Modifica o input de saída para multiplos elementos
 #       print(self.quantidade)
        if self.quantidade:
            
            self.input.write('moder\n')
#            print('to dentro',self.quantidade)
            
            self.input.write('1 '+ self.parametros['nout'] + '/\n')
            self.input.write(self.parametros['tlabel'] + '/\n')

            quantidade = len(self.parametros['nin'])
            quantidade = range(quantidade)

            for tape in quantidade:
                self.input.write(str(self.parametros['nin'][tape]) +' '
                +self.parametros['matb'][tape] + '/\n')
            
            self.input.write('0/\n')
        
        else:
            self.input.write('moder\n')
            self.input.write(str(self.parametros['nin'][0]) +' '+ str(self.parametros['nout']) + '/\n')

            
    
    #Preenche uma única linha de parâmetros
    def __preencheLinha__(self, variaveis, ponteiroLaco):

        if 'mfd' in variaveis:
           a = self.__card9__()
           return a
        
        #Variaveis como tlabel e cards nunca vem acompanhadas de outras.
        if variaveis[-1] == 'cards':
            a = self.__multiploElementos__(variaveis, ponteiroLaco)
            return a

        if 'title' == variaveis[-1] or 'tlabel' == variaveis[-1]:
            return self.parametros[variaveis[-1]] + '/\n'

        if not 'VOLTE' in variaveis:
           return self.__parametrosComuns__(variaveis,ponteiroLaco)
    
    #Cada linha do card9 é formado pelos valores dos parâmetros mdf, mtd e mtname
    def __card9__(self):


        tam = range(len(self.parametros['mfd']) - 1)
        card9 = ''

        if self.ponteiroLaco != 0:
            card9 += self.parametros['matb'][self.ponteiroLaco] + '/\n'

        for elemento in tam:
            card9 += self.parametros['mfd'][elemento] + ' '
            card9 += self.parametros['mtd'][elemento] + ' '
            card9 += self.parametros['mtname'][elemento] + '/\n'
        
        card9 += self.parametros['mfd'][-1] + '/\n'
        return card9
    
    #Preenche parâmetros como tlabel e cards que podem ser um vetor de string ou uma matriz, a
    #depender da quantidade de elementos
    def __multiploElementos__(self,valor,posicao):
        
        buffer = ''

        parametros = self.parametros[valor[0]]

        if(isinstance(parametros[0], list)):

            #Para cada elemento, é atribuida um valor. Caso tenha menos valores que elementos
            #Os o último valor é atribuído ao resto
            if posicao >= len(parametros):
                posicao = -1
            
            for elemento in parametros[posicao]:
                buffer += elemento + '/\n'
            
        else:
            for elemento in parametros:
                buffer += elemento + '/\n' 
        
        return buffer
    
    #Parâmetros sem preenchimento especial e com um valor por material, além de matb.
    def __parametrosComuns__(self, valor, posicao):
        
        buffer = ''

        #Preenche egn ou egg num formato de matriz.
        if valor[-1] == 'egn' or valor[-1] == 'egg':
            string = ''
            contador = 1
            variavel = valor[-1]

            if self.parametros[variavel] == '' : return ''

            for elemento in self.parametros[variavel]:
                if contador % 10:
                    string += elemento + ' '
                else:
                    string += elemento + '\n'
                contador += 1

            string = string[:-1] + '/\n'
            return string
        
        #Matb são os materiais a serem processados e sempre aparecem no início da linha de parâmetros
        if 'matb' in valor:

            valor = valor[1:]
            buffer = self.parametros['matb'][self.ponteiroLaco] + ' '

            if not valor:
                buffer = ''

                for elemento in self.parametros['matb'][self.ponteiroLaco + 1:]:
                    buffer += elemento + '/\n'

                return buffer + '0/\n'

            for variavel in valor[:-1]:
                try:
                    buffer += self.parametros[variavel] + ' '
                except:
                    buffer += variavel + ' '

            try:
                if valor[-1] == 'ncards':
                    #O valor de ncards pode mudar de acordo com os elementos

                    #Para cada elemento, é atribuida um valor. Caso tenha menos valores que elementos
                    #Os o último valor é atribuído ao resto
                    if posicao >= len(self.parametros['ncards']):
                        posicao = -1

                    linha = self.parametros['ncards'][posicao]
                else:
                    linha = self.parametros[valor[-1]]

                return buffer + linha + '/\n'
            except:
                return buffer + valor[-1] + '\n'
        
        for variavel in valor[:-1]:
            try:
                buffer += self.parametros[variavel] + ' '
            except:
                buffer += variavel + ' '
        try:
            buffer += self.parametros[valor[-1]]

            if buffer == '': 
                return buffer  #Parâmetros que ocupam uma única linha e que podem estar vazios
            if valor[-1] == 'ngg': return buffer + '\n' #ngg não pode terminar em /, do contrário, o NJOY não executa.

            return buffer + '/\n' 
        except:
            return buffer + valor[-1] + '\n'
    
    #def __del_(self):