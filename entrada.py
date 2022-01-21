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

        #Retorna: o nome da variável e seu valor.
        return variavel, valor
    
    #Ler as entradas encontradas em "arquivo_entrada".
    def leia(self):
        
        #Conta o número da linha
        posicao = 0

        for linha in self.arquivo_entrada:
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

#entrada = Entrada('testeAki.txt')

#print(entrada.getEntrada())

#entrada.leia()

#resultado = entrada.getEntrada()

#for chave in resultado:
#    print("[",chave,"]"," = ",resultado[chave])




        


