from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from Dados import retornar_dados

chrome_options = Options()
chrome_options.add_argument("--start-maximized")

nav = webdriver.Chrome(options=chrome_options)
action = ActionChains(nav)

url = retornar_dados('url')
nav.get(url)

def realizar_login():
    usucod = nav.find_element(by=By.NAME, value="_USUCODC")
    ususen = nav.find_element(by=By.NAME, value="_USUSEN")
    btncon = nav.find_element(by=By.NAME, value="BUTTON1")

    usucod.clear()

    usuario = retornar_dados('usuario')
    usucod.send_keys(usuario)
    senha = retornar_dados('senha')
    ususen.send_keys(senha)

    btncon.click()

    btnsim = nav.find_element(by=By.NAME, value="BUTTON3")
    if btnsim.is_displayed():
        btnsim.click()

    return nav

