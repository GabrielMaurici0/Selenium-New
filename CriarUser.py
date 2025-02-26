from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
import time

from Login import realizar_login

chrome_options = Options()
chrome_options.add_argument("--start-maximized")

nav = realizar_login()

action = ActionChains(nav)

nav.get("https://www.moozcobranca.com.br/homologacao/servlet/hbranco")

time.sleep(2)



nav.quit()