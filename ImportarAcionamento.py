from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

from Login import realizar_login

chrome_options = Options()
chrome_options.add_argument("--start-maximized")

nav = realizar_login()

action = ActionChains(nav)

nav.get("https://www.moozcobranca.com.br/homologacao/servlet/hbranco")


opcoes = nav.find_element(by= By.XPATH, value="//*[@id='MSG_MPAGE']/ul/li[7]/a")
action.move_to_element(opcoes).perform()

importar = nav.find_element(by=By.XPATH, value="//*[@id='MSG_MPAGE']/ul/li[7]/ul/li/a")
importar.click()

icarteira = input("Informe a Carteira (carcod): ")
iempresa = input("Informe a Empresa: ")
itratar = input ("Tratar Inconsistências Automaticamente? (s ou n) ")
ilayout = input("Informe um Layout: ")

scarteira = nav.find_element(by=By.XPATH, value="//*[@id='TABLE1']/tbody/tr[1]/td[2]/select")
sempresa = nav.find_element(by=By.XPATH, value="//*[@id='TABLE1']/tbody/tr[2]/td[2]/select" )
slayout = nav.find_element(by=By.XPATH, value="//*[@id='TABLE1']/tbody/tr[7]/td[2]/p/select")

selectcarteira = Select(scarteira)
selectcarteira.select_by_value(icarteira)

selectempresa = Select(sempresa)
selectempresa.select_by_value(iempresa)

tratar = nav.find_element(by=By.XPATH, value="//*[@id='TABLE1']/tbody/tr[5]/td[2]/p/span/input")

if itratar.upper() == "S":
    tratar.click()


selectlayout = Select(slayout)
selectlayout.select_by_value(ilayout)

arquivo = nav.find_element(by=By.XPATH, value="//*[@id='_FILE']")
# Substituir pelo caminho do arquivo que deseja importar#
caminho = r"C:\Users\gabriel.mauricio\Desktop\2239\Arquivos de acionamento para o teste\layout-1 - Todas inconsistencias.txt"
arquivo.send_keys(caminho)

confirmar = nav.find_element(by=By.XPATH, value="//*[@id='TABLE1']/tbody/tr[10]/td/input[2]").click()

confirmar = nav.find_element(by=By.XPATH, value="/html/body/div[3]/div/div[6]/button[1]").click()

mensagem = nav.find_element(by=By.XPATH, value="//*[@id='span__MSG']")
mensagem = mensagem.text

if mensagem == "Inconsistências Diversas":
    print("Erro na importação do arquivo")
else:
    print("Sucesso na importação do arquivo")

time.sleep(5)

nav.quit()

