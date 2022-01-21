import shutil


class Tape:

    def __init__(self, arquivo, elemento):
        self.arquivo = open(arquivo, 'r')
        self.__setElemento__(elemento)


    def obterTape20(self):
        
        for linha in self.arquivo:
            campo = linha.split()
            if campo[0] == self.elemento:
                self.tape20 = campo[1]
    
    def __setElemento__(self, elemento):
        elemento = elemento.replace('\n','')
        elemento = elemento.replace(' ', '')
        elemento = elemento.replace("'", '')
        self.elemento = elemento

    def copiarTapePara(self, origem , novoCaminho):
        shutil.copyfile(origem, novoCaminho)
    
    def obterMat(self):
        comeca = self.tape20.find('_')
        termina = self.tape20.rfind('_')
        self.mat = self.tape20[comeca+1:termina]
    
    def getElemento(self):
        return self.elemento
    
    def getTape20(self):
        return self.tape20
    
    def getMat(self):
        return self.mat
    
    def __del__(self):
        try:
            self.arquivo.close()
        except:
            pass

    elemento = ''
    arquivo = None
    tape20 = ''
    mat = ''

#tape = Tape('tapes_lista.txt', '3Li7')

#tape.obterTape20()
#print(tape.getTape20())
#tape.obterMat()
#print(tape.getMat())
#print(tape.getElemento())

#origem = r"C:\Users\Win10\Desktop\tapes20\n_0328_3-Li-7.dat"
#alvo = r"C:\Users\Win10\Desktop\criadorInput\nova_versão\tape20"

#tape.copiarTapePara(origem, alvo)