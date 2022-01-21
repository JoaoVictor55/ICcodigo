from Parametros import Parametros
from Parametros import ParametrosAdmin
import os
from entrada import Entrada 
import tape

def rodar(arquivoEntrada, caminho):

    arquivoEntrada = arquivoEntrada.replace('\n','')
    arquivoEntrada = arquivoEntrada.replace(' ','')

    caminho = caminho.replace('\n','')
    caminho = caminho.replace(' ','')

    comando = "sudo cp ./" + arquivoEntrada + " " + caminho
    os.system(comando)

    os.chdir(caminho)
    comando = 'sudo ./njoy21 < ' + arquivoEntrada + ' -o output'
    
    os.system(comando)

def main():
    arquivoEntrada = 'testeAki.txt'
    arquivoSaida = 'intputGerado.txt'
    
    entrada = Entrada(arquivoEntrada)

    entrada.leia()
    entradaUser = entrada.getEntrada()

    fita = tape.Tape('tapes_lista.txt',entradaUser['material'])
    fita.obterTape20()
    fita.obterMat()

    parametro = Parametros()
    parametro.setMatb(fita.getMat())
    parametro.receberParametros(entradaUser)
    parametros = parametro.getParametros()

   # for chave in parametros:
    #    print('[',chave,']','=',parametros[chave])

    entrada = ParametrosAdmin('inputQualquer.txt',parametros,arquivoSaida)
    entrada.preencherInput()

    return arquivoSaida,  entradaUser['caminho']

entrada, caminho = main()

print(entrada, caminho)
rodar(entrada, caminho)

#entrada = Entrada('testeAki.txt')

#entrada.leia()
#entradaUser = entrada.getEntrada()