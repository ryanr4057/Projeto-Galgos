from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import f_busca as fbd
import funções_ as f
from selenium.webdriver.support import expected_conditions as EC
import subprocess
import time
import bot

def proc_avb(driver, race_count, env_mens):
    avb_dogs = driver.find_elements(By.CLASS_NAME,"ir-RacingGreyhoundsMatchUpParticipant_Name")

    if len(avb_dogs) > 0:
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        dogs = soup.find_all('span', {'class': 'ir-RacingGreyhoundsMatchUpParticipant_Name'})
        odds = soup.find_all('span', {'class': 'ir-RacingGreyhoundsMatchUpParticipant_Odds'})
        race_id = fbd.buscar_dog_rid(dogs[0].get_text().strip())
        horario = fbd.buscar_race_h(race_id[0])
        nome = fbd.buscar_race_nome(race_id[0])
        pista_id = fbd.buscar_race_pis(race_id[0])
        pista_nome = fbd.buscar_pista_nome(pista_id[0])

        for i in range(0, len(dogs), 2):
            # print(f"{dogs[i].get_text().strip()} vs {dogs[i+1].get_text().strip()}")
            a = dogs[i].get_text().strip()
            b = dogs[i+1].get_text().strip()

            d_dogs_a, d_dogs_b, venc = f.compara(race_id, a, b )

            if venc[11] > venc[12] and abs(venc[11] - venc[12]) > 0:
                mensagem = f"{pista_nome[0]} {nome[0]} {horario[0]}\n {d_dogs_a[0]} {d_dogs_a[1]} ({venc[11]}) @{odds[i].get_text()}  VENCE  {d_dogs_b[0]} {d_dogs_b[1]} ({venc[12]}) @{odds[i+1].get_text()}"
                if (mensagem in env_mens) is False:
                    bot.mens_telegram(mensagem)
                    env_mens.append(mensagem)
            elif venc[11] < venc[12] and abs(venc[11] - venc[12]) > 0:
                mensagem = f"{pista_nome[0]} {nome[0]} {horario[0]} \n {d_dogs_b[0]} {d_dogs_b[1]} ({venc[12]}) @{odds[i+1].get_text()} VENCE  {d_dogs_a[0]} {d_dogs_a[1]} ({venc[11]}) @{odds[i].get_text()}"
                if (mensagem in env_mens) is False:
                    bot.mens_telegram(mensagem)
                    env_mens.append(mensagem)

        driver, race_count = proc_prox_race(driver, race_count)
        time.sleep(3)

        proc_avb(driver, race_count, env_mens)

    else:
        driver, race_count = proc_prox_race(driver, race_count)
        time.sleep(3)

        proc_avb(driver, race_count, env_mens)

    return env_mens

def proc_prox_race(driver, race_count):
    p_race = driver.find_elements(By.CLASS_NAME,"ipn-FixtureNoScores_Wrapper")
    p_race[race_count].click()
    current_url = driver.current_url
    driver.get(current_url)
    if race_count < len(p_race) - 1:
        race_count = race_count + 1
    elif race_count == len(p_race) - 1:
        # time.sleep(30)
        race_count = 0

    return driver, race_count


