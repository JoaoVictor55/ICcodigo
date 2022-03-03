import time
from selenium import webdriver
import glob
import os
from selenium.webdriver.firefox.options import Options

class Tape:

    def __init__(self, material):

        self.material = material #Lista com o material e tipo de reação a ser buscado no formato [elemento, reaçao].
        self.mat = dict() #Dicionário com os materiais e simbolos químicos.
        self.ausentes = list()

    def WebScraping(self):
        
        controle = self.ausentes
        opcao = Options()
        opcao.headless = True
        driver = webdriver.Firefox(options=opcao)
        

        while controle:

            target = controle.pop(0)
            target = target[0]

            driver.get("https://www-nds.iaea.org/exfor/endf.htm")

            elemTarget = driver.find_element_by_name("Target")
            elemTarget.clear()
            elemTarget.send_keys(target)
            #time.sleep(3)
            driver.find_element_by_name("chkLib0").click()
            driver.find_element_by_css_selector("input[type=submit]").click()
            driver.find_element_by_css_selector("form > input:nth-child(14)").click()
            #time.sleep(4)
            driver.find_element_by_css_selector("form > input:nth-child(10)").click()
            #time.sleep(8)
            driver.find_element_by_css_selector("a[title='Show ENDF-6 file...']").click()
            #time.sleep(4)
            texto = driver.find_element_by_css_selector("pre").get_attribute("textContent").encode("utf-8")
            
            with open(target+'.txt', 'wb') as file:
                file.write(texto)
            file.close()

            assert "No results found." not in driver.page_source

        driver.close()

    def procurarTAPE(self):

        #O programa procura primeiro pelas fitas já baixadas. Para isso, são listados todos os txts.
        myFiles = [os.path.splitext(files)[0] for files in glob.glob('*.txt')]

        for elemento in self.material:

            #Se o elemento buscado tiver uma tape.
            elemento[0] = elemento[0].replace("'",'')
            elemento[1] = elemento[1].replace("'",'')

            if elemento[0] in myFiles:
                
                self.__getMat__(elemento)
        
        #self.mat = dict(sorted(self.mat.items()))
        self.mat = {str(key) : self.mat[key] for key in sorted(self.mat.keys())}
                
    def obterMats(self):

        return self.mat
    
    def __getMat__(self, elemento):
        tape = open(elemento[0]+'.txt','r') #Abre a tape do elemento.
                
        for linha in tape:
        
            #Localiza a reação na tape e obtem o mat correspondente.
            if elemento[1] in linha:
            
                self.mat.setdefault(int(linha.split()[-3]), elemento[0])
                tape.close()
                break #Acaba a procura uma vez que o mat for achado.

def teste():

    procurar = [['1-H-1','DECAY'], ['Li-7', 'DECAY'], ['8-O-0', 'PHOTO']]
    procurar2 = [['6-C-0', 'PHOTO']]
    tape = Tape(procurar)

    tape.procurarTAPE()

    print(tape.obterMats())



#web = WebScraping