from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import bet_funções as f
from selenium.webdriver.support import expected_conditions as EC
import subprocess
import time
import pyautogui
import funções_ as ff

try:
   ff.cria_bd()
except Exception:
   print("")
# # time.sleep(45)

race_count = 1
env_mens = []
env_avb = []


while True:
   try:
      subprocess.Popen(
         '"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --remote-debugging-port=9014', shell=True)

      options = webdriver.ChromeOptions()
      options.add_experimental_option("debuggerAddress", "127.0.0.1:9014")

      driver = webdriver.Chrome(options=options)
      driver.maximize_window()
      # driver.get('https://www.bet365.com/#/HO/')
      time.sleep(3)

      pyautogui.hotkey('ctrl','t')
      pyautogui.typewrite('bet365.com')
      pyautogui.press('enter')

      time.sleep(2)

      time.sleep(2)

      driver.switch_to.window(driver.window_handles[1])

      driver.get('https://www.bet365.com/#/IP/B4')

      # pyautogui.click(289,18)

      # for i in range(14):
      #    pyautogui.press('tab')
      # pyautogui.press('enter')

      time.sleep(2)

      corrida = driver.find_elements(By.CLASS_NAME,"ovm-RacingViewAllLink ")

      # print(len(corrida))
      while len(corrida) ==0:
         corrida = driver.find_elements(By.CLASS_NAME,"ovm-RacingViewAllLink ")
         time.sleep(1)

      corrida[0].click()

      time.sleep(3)

      # current_url = driver.current_url
      # driver.get(current_url)

      # time.sleep(15)

      f.proc_avb_ia(driver, race_count, env_mens, env_avb)

   except Exception:
      print(Exception.__cause__)
      subprocess.Popen('taskkill /F /IM chrome.exe', shell=True)
      time.sleep(5)







