from http.server import executable
from selenium import webdriver
import glob
import os
from selenium.webdriver.firefox.options import Options

def WebScraping(materiais):
    
    myFiles = [os.path.splitext(files)[0] for files in glob.glob('*.txt')]
    ausentes = list()
    
    for elemento in materiais:

        elemento[0] = elemento[0].replace("'",'')
        elemento[1] = elemento[1].replace("'",'')

        if not elemento[0] in myFiles: ausentes.append([elemento[0]])


    if ausentes:        
        controle = ausentes
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

    return materiais
