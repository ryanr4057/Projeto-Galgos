import funções_ as f
import f_banco_avbs as fbd
import f_busca
import cria_bd_avb as avb
from selenium import webdriver
import time
import re

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import pyautogui

avbs = fbd.buscar_todos_avb()



driver = webdriver.Chrome()

url ='https://greyhoundbet.racingpost.com/#results-list/r_date=2023-03-30'
driver.get(url)
time.sleep(2)

pyautogui.click(654,555)
time.sleep(1)
pyautogui.click(634,709)
time.sleep(1)
for i in range(0,6):
    pyautogui.hotkey('ctrl','-')



# pist = driver.find_elements(By.CLASS_NAME,"results-race-list-row")

# for i in range(0, len(pist)):
#     r = pist[i].find_elements(By.TAG_NAME,"a")
#     pistas.append(r)
print(len(avbs))
for i in range(0,len(avbs)):
    # if (avbs[i][7] >= 7 and avbs[i][8] < 2) or (avbs[i][8] >= 7 and avbs[i][7] < 2):
    pistas = []

    pist = driver.find_elements(By.CLASS_NAME,"results-race-list-row")
    # print(len(pist))

    for j in range(0, len(pist)):
        r = pist[j].find_elements(By.TAG_NAME,"a")
        pistas.append(r)

    a = avbs[i][3]
    b = avbs[i][4]
    id_avb = fbd.buscar_id_avb(a)
    race_id = f_busca.buscar_dog_rid(a)
    pista_id = f_busca.buscar_pista_id_r(race_id[0])
    n_pista = pista_id[0] - 1

    c = (avbs[i][2].strip()).index(' ')
    n_race = int( (avbs[i][2])[c:].strip()) - 1

    # print(n_pista)
    # print(n_race)
    # print(avbs[i][2])
    # print(avbs[i][1])
    # print(pistas[n_pista][n_race].text)

    try:
        pistas[n_pista][n_race].click()
    except Exception:
        driver.refresh()
        pistas = []

        pist = driver.find_elements(By.CLASS_NAME,"results-race-list-row")
        # print(len(pist))

        for j in range(0, len(pist)):
            r = pist[j].find_elements(By.TAG_NAME,"a")
            pistas.append(r)

        a = avbs[i][3]
        b = avbs[i][4]
        id_avb = fbd.buscar_id_avb(a)
        race_id = f_busca.buscar_dog_rid(a)
        pista_id = f_busca.buscar_pista_id_r(race_id[0])
        n_pista = pista_id[0] - 1

        c = (avbs[i][2].strip()).index(' ')
        n_race = int( (avbs[i][2])[c:].strip()) - 1
        pistas[n_pista][n_race -1].click()



    time.sleep(2)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    dogs = soup.find_all('div', {'class': 'name'})
    n_nomes = []

    for i in range(0, len(dogs)):
        n = dogs[i].get_text().strip()
        n = re.sub(r'\(.*?\)', '', n).strip()
        # print(n)
        n_nomes.append(n)
    try:
        pos_a = n_nomes.index(a) + 1
        pos_b = n_nomes.index(b) + 1
    except Exception:
        n_race = n_race + 1
        pyautogui.click(48,84)
        driver.refresh()
        time.sleep(2)

        pistas = []

        pist = driver.find_elements(By.CLASS_NAME,"results-race-list-row")

        for j in range(0, len(pist)):
            r = pist[j].find_elements(By.TAG_NAME,"a")
            void = pist[j].find_elements(By.CLASS_NAME,"noLink")
            t_void = len(void)
            if t_void > 0:
                r.append(t_void)
            pistas.append(r)

        a = avbs[i][3]
        b = avbs[i][4]
        id_avb = fbd.buscar_id_avb(a)
        race_id = f_busca.buscar_dog_rid(a)
        pista_id = f_busca.buscar_pista_id_r(race_id[0])
        n_pista = pista_id[0] - 1

        c = (avbs[i][2].strip()).index(' ')
        n_race = int( (avbs[i][2])[c:].strip()) - 1

        time.sleep(2)

        pistas[n_pista][n_race].click()
        # print(n_pista)
        # print(n_race)

        time.sleep(2)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        dogs = soup.find_all('div', {'class': 'name'})
        n_nomes = []

        for i in range(0, len(dogs)):
            n = dogs[i].get_text().strip()
            n = re.sub(r'\(.*?\)', '', n).strip()
            # print(n)
            n_nomes.append(n)

        pos_a = n_nomes.index(a) + 1
        pos_b = n_nomes.index(b) + 1



    if pos_a < pos_b:
        fbd.atribuir_result(id_avb[0],0)
    elif pos_a > pos_b:
        fbd.atribuir_result(id_avb[0],1)

    # print(pos_a)
    # print(pos_b)
    # print(len(dogs))
    # print(a)
    # print(b)
    # print(n_race)
    # print(n_pista)

    pyautogui.click(48,84)
    driver.refresh()
    time.sleep(2)










    # html = driver.page_source
    # soup = BeautifulSoup(html, 'html.parser')
    # pistas = soup.find_all('a', {'data-eventid': 'cards_meetings_click'})
