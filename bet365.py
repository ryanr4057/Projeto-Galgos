from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
url = "https://www.bet365.com/#/IP/EV207292515854660372C4"
driver.get(url)

while True:
    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "ir-RacingFullWidthMarket gl-Market gl-Market_General gl-Market_General-topborder gl-Market_General-pwidth100 gl-Market_General-lastinrow")))
        break
    except:
        continue

print(element.text)

driver.quit()
