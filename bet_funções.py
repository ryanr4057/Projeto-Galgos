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
        if race_id != None:
            horario = fbd.buscar_race_h(race_id[0])
            nome = fbd.buscar_race_nome(race_id[0])
            pista_id = fbd.buscar_race_pis(race_id[0])
            pista_nome = fbd.buscar_pista_nome(pista_id[0])
            r_dist = fbd.buscar_race_dist(race_id[0])


            for i in range(0, len(dogs), 2):
                # print(f"{dogs[i].get_text().strip()} vs {dogs[i+1].get_text().strip()}")
                a = dogs[i].get_text().strip()
                b = dogs[i+1].get_text().strip()

                d_dogs_a, d_dogs_b, venc = f.compara(race_id, a, b )

                if venc[11] > venc[12] and abs(venc[11] - venc[12]) > 7:
                    mensagem = f"RR TIPS - AvB: 🐶\n \n{pista_nome[0]} {horario[0]} - ({nome[0]}) - {r_dist[0]} \n \n*TRAP: {d_dogs_a[0]}- {d_dogs_a[1]} ({venc[11]})*\n  \nVENCE:   \n \nTRAP: {d_dogs_b[0]}- {d_dogs_b[1]} ({venc[12]})\n \nOdd: @{odds[i].get_text()}💸\n \nLink:{driver.current_url}"
                    ind = mensagem.find('@')
                    v_mens = mensagem[:ind] + mensagem[:ind+5]
                    if (v_mens in env_mens) is False:
                        bot.mens_telegram(mensagem)
                        env_mens.append(v_mens)
                elif venc[11] < venc[12] and abs(venc[11] - venc[12]) > 7:
                    mensagem = f"RR TIPS - AvB: 🐶\n \n{pista_nome[0]} {horario[0]} - ({nome[0]}) - {r_dist[0]} \n \n*TRAP: {d_dogs_b[0]}- {d_dogs_b[1]} ({venc[12]})*\n  \nVENCE:   \n \nTRAP: {d_dogs_a[0]}- {d_dogs_a[1]} ({venc[11]})\n \nOdd: @{odds[i+1].get_text()}💸\n \nLink:{driver.current_url}"
                    ind = mensagem.find('@')
                    v_mens = mensagem[:ind] + mensagem[:ind+5]
                    if (v_mens in env_mens) is False:
                        bot.mens_telegram(mensagem)
                        env_mens.append(v_mens)

        driver, race_count = proc_prox_race(driver, race_count)
        time.sleep(3)

        proc_avb(driver, race_count, env_mens)

    else:
        driver, race_count = proc_prox_race(driver, race_count)
        time.sleep(3)

        proc_avb(driver, race_count, env_mens)

def proc_prox_race(driver, race_count):
    p_race = driver.find_elements(By.CLASS_NAME,"ipn-FixtureNoScores_Wrapper")
    if p_race is None:
        driver.refresh()
        time.sleep(2)
        p_race = driver.find_elements(By.CLASS_NAME,"ipn-FixtureNoScores_Wrapper")

    qtd_race = len(p_race) - 1
    if qtd_race < race_count:
        race_count = 0
    p_race[race_count].click()
    time.sleep(3)

    current_url = driver.current_url
    driver.get(current_url)
    if race_count < len(p_race) - 1:
        race_count = race_count + 1
    elif race_count == len(p_race) - 1:
        time.sleep(30)
        race_count = 0

    return driver, race_count

def proc_avb_w(driver, race_count, env_mens):

    while True:
        avb_dogs = driver.find_elements(By.CLASS_NAME,"ir-RacingGreyhoundsMatchUpParticipant_Name")

        if len(avb_dogs) > 0:
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            dogs = soup.find_all('span', {'class': 'ir-RacingGreyhoundsMatchUpParticipant_Name'})
            odds = soup.find_all('span', {'class': 'ir-RacingGreyhoundsMatchUpParticipant_Odds'})
            race_id = fbd.buscar_dog_rid(dogs[0].get_text().strip())
            if race_id != None:
                horario = fbd.buscar_race_h(race_id[0])
                nome = fbd.buscar_race_nome(race_id[0])
                pista_id = fbd.buscar_race_pis(race_id[0])
                pista_nome = fbd.buscar_pista_nome(pista_id[0])
                r_dist = fbd.buscar_race_dist(race_id)
                r_cat = fbd.buscar_race_cat(race_id)
                for i in range(0, len(dogs), 2):
                    # print(f"{dogs[i].get_text().strip()} vs {dogs[i+1].get_text().strip()}")
                    a = dogs[i].get_text().strip()
                    b = dogs[i+1].get_text().strip()

                    d_dogs_a, d_dogs_b, venc = f.compara_av(race_id, a, b )

                    if venc[11] > venc[12] and abs(venc[11] - venc[12]) > 7:
                        if (d_dogs_a[12] == 2 or d_dogs_a[12] == 1):
                            mensagem = f"RR TIPS - AvB: 🐶\n \n{pista_nome[0]} {horario[0]} - ({nome[0]}) - {r_cat[0]} - {r_dist[0]}m \n \n*TRAP: {d_dogs_a[0]}- {d_dogs_a[1]} ({venc[11]})*\n  \nVENCE:   \n \nTRAP: {d_dogs_b[0]}- {d_dogs_b[1]} ({venc[12]})\n \nOdd: @{odds[i].get_text()}💸\n \nLink:{driver.current_url}"
                            ind = mensagem.find('@')
                            # print(ind)
                            v_mens = mensagem[:ind]
                            # print(v_mens)
                            if (v_mens in env_mens) is False:
                                bot.mens_telegram(mensagem)
                                env_mens.append(v_mens)
                    elif venc[11] < venc[12] and abs(venc[11] - venc[12]) > 7:
                        if (d_dogs_b[12] == 2 or d_dogs_b[12] == 1):
                            mensagem = f"RR TIPS - AvB: 🐶\n \n{pista_nome[0]} {horario[0]} - ({nome[0]}) - {r_cat[0]} - {r_dist[0]}m \n \n*TRAP: {d_dogs_b[0]}- {d_dogs_b[1]} ({venc[12]})*\n  \nVENCE:   \n \nTRAP: {d_dogs_a[0]}- {d_dogs_a[1]} ({venc[11]})\n \nOdd: @{odds[i+1].get_text()}💸\n \nLink:{driver.current_url}"
                            ind = mensagem.find('@')
                            # print(ind)
                            v_mens = mensagem[:ind]
                            # print(v_mens)
                            if (v_mens in env_mens) is False:
                                bot.mens_telegram(mensagem)
                                env_mens.append(v_mens)

            driver, race_count = proc_prox_race(driver, race_count)
            time.sleep(3)


        else:
            driver, race_count = proc_prox_race(driver, race_count)
            time.sleep(3)



