from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import bet_funções as f
from selenium.webdriver.support import expected_conditions as EC
import subprocess
import time

race_count = 1
env_mens = []


subprocess.Popen(
   '"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --remote-debugging-port=9222', shell=True)

options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

driver = webdriver.Chrome(options=options)
driver.maximize_window()
driver.get('https://www.bet365.com/#/IP/B4')

time.sleep(5)

corrida = driver.find_elements(By.CLASS_NAME,"ovm-RacingViewAllLink ")

# print(len(corrida))

corrida[0].click()

time.sleep(3)

current_url = driver.current_url
driver.get(current_url)

time.sleep(5)

env_mens = f.proc_avb(driver, race_count, env_mens)





