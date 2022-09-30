import numpy

class MacroSeccao:

    def __init__(self,njoyOutput,material,elementos,ordemElementosOutput):

        self.ingredientes = material 
        self.ordemElementosOutput = ordemElementosOutput #lista que mostr a ordem em que os elementos
        #irão aparecer no output.
        self.elementos = elementos
        self.ni = None #Ni é a densidade atômica.
        self.AVOGRADO = 6.02214076E+23
        self.njoyOutput = njoyOutput #Saída gerada pelo NJOY com as seções microscópicas.
        self.micro = None #Seção microscópica dos materiais vindo do njoyOutput.
        self.macroTotal = None 

    def calculaNI(self):

        fracoes = list()
        elementosMaterial = list()
        DENSIDADE = float()
        massaAtomica = list()

        with open(self.ingredientes,'r') as self.ingredientes:

            #Pega a densidade do material
            DENSIDADE = self.ingredientes.readline().split()[-1]

            DENSIDADE = float(DENSIDADE)

            #Ler a fração do peso
            #fracoes = [frac.split()[-1]  for frac in MATERIAL]

            ingredientes = self.ingredientes.readlines()

        for elemento in self.ordemElementosOutput:
            
            densidade = [buffer.split() for buffer in ingredientes if buffer.split()[0] == elemento][0]
            
            fracoes.append(densidade[-1])#Pega a fração de peso
            elementosMaterial.append(densidade[0]) #Pega o elemento que compõe o material


        fracoes = numpy.asarray(fracoes,dtype=float)

        with open(self.elementos,"r") as self.elementos:

            elementos = list()
            for linha in self.elementos:
                #Pega o nome do elemento e o peso atômico
                elementos.append(linha.split()[0])
                elementos.append(linha.split()[1])
        
        for massa in elementosMaterial:
            

            try:
                peso = elementos[elementos.index(massa) + 1]  #Pega a massa de cada elemento.            
                massaAtomica.append(peso)
            except ValueError: pass
        
        
        massaAtomica = numpy.asarray(massaAtomica,dtype=float)
    
        self.ni = ((self.AVOGRADO * DENSIDADE) * fracoes)/massaAtomica

    def calcularMacroscopicaTotal(self):

        self.calculaNI()
        self.secaoMicro()

        try:
            self.macroTotal = self.ni * self.micro
        except ValueError:
            self.macroTotal = self.ni * self.micro.T
            self.macroTotal = self.macroTotal.T

    def returnMacroTotal(self):
        return self.macroTotal

    def secaoMicro(self) :
        
        inicio = ' group  (barns)\n'
        vetorIndice = int(0) #Indice dos vetores gerados
        vetor = list() #Armazena os vetores produzidos pelo módulo do NJOY

        with open(self.njoyOutput,'r') as self.njoyOutput:
            self.njoyOutput = self.njoyOutput.readlines()

        while True:
            try:
                inicioIndex = self.njoyOutput.index(inicio)  #Pega o inicio do vetor
            except ValueError:
                break #Quando a string que marca o início está faltando, a iteração acaba.

            linha = self.njoyOutput[inicioIndex + 1].split()

            arquivoTamanho = len(self.njoyOutput[inicioIndex + 1:])

            vetorIndice = 2

            buffer = list() 

            while linha and arquivoTamanho > vetorIndice:
                buffer.append(linha[-1].replace('-','E-').replace('+','E+')) #Transforma o formato de notação científica para o padrão do Python
                linha = self.njoyOutput[inicioIndex + vetorIndice].split()
                vetorIndice+=1
            
            vetor.append(buffer)
            self.njoyOutput = self.njoyOutput[inicioIndex + vetorIndice:] #Próximo vetor
        
        self.micro = numpy.asarray(vetor,dtype=float)