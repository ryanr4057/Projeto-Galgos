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
import f_banco_avbs as favb
import teste as iaa
import pickle
import pyautogui



bot_mens = []

# ia = pickle.load(open('IA_81%.sav', 'rb'))

# rf = pickle.load(open('forest.sav', 'rb'))

# scaler = pickle.load(open('scaler.sav', 'rb'))


def proc_prox_race(driver, race_count):
    pyautogui.click(191,364)
    time.sleep(0.5)
    p_race = driver.find_elements(By.CLASS_NAME,"ipn-FixtureNoScores_Wrapper")
    if p_race is None:
        driver.refresh()
        time.sleep(2)
        pyautogui.click(191,364)
        time.sleep(0.5)
        p_race = driver.find_elements(By.CLASS_NAME,"ipn-FixtureNoScores_Wrapper")

    qtd_race = len(p_race) - 1
    if qtd_race < race_count:
        race_count = 0
    p_race[race_count].click()
    time.sleep(1)

    # current_url = driver.current_url
    # driver.get(current_url)
    #driver.refresh()
  #  time.sleep(3)
    if race_count < len(p_race) - 1:
        race_count = race_count + 1
    elif race_count == len(p_race) - 1:
        time.sleep(2)
        race_count = 0
    return driver, race_count

def proc_avb_w(driver, race_count, env_mens, env_avb):
    while True:
        n_dogs = []

        avb_dogs = driver.find_elements(By.CLASS_NAME,"ir-RacingGreyhoundsMatchUpParticipant_Name")
        all_dogs = driver.find_elements(By.CLASS_NAME,"ir-RacingGreyhoundsFixedOddsParticipant_ParticipantName ")
        off = driver.find_elements(By.CLASS_NAME,"ir-RaceOffBanner ")

        # print(len(off))
        for i in range(0, len(all_dogs) -1):
            n_dogs.append(all_dogs[i].text)

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
                    a = dogs[i].get_text().strip()
                    b = dogs[i+1].get_text().strip()

                    dog_a = fbd.buscar_dog_nome(a)
                    dog_b = fbd.buscar_dog_nome(b)

                    if dog_a != None and dog_b != None:

                        d_dogs_a, d_dogs_b, venc = f.compara_av(race_id, a, b )

                        if (venc[11] >= 7 and venc[12] < 2) or (venc[12] >= 7 and venc[11] < 2):

                            prev = iaa.previsao_ia(a,b)

                            if prev[0] == 0:
                                mensagem = f"RR TIPS - AvB: 🐶 \n{pista_nome[0]} {horario[0]} - ({nome[0]}) - {r_cat[0]} - {r_dist[0]}m \n*TRAP: {d_dogs_a[0]}- {d_dogs_a[1]} ({venc[11]})*  \nVENCE: \nTRAP: {d_dogs_b[0]}- {d_dogs_b[1]} ({venc[12]}) \nOdd: @{odds[i].get_text()}💸 \nLink:{driver.current_url} \n MÉTODO: {venc[13]} \n ENTRADA PADRÃO \n f1"
                                ind = mensagem.find('@')
                                v_men = mensagem[:ind]
                                if (v_men in bot_mens) is False:
                                    if len(off) == 0:
                                        bot.mens_telegram_ia(mensagem)
                                        bot_mens.append(v_men)

                            elif prev[0] == 1:
                                mensagem = f"RR TIPS - AvB: 🐶 \n{pista_nome[0]} {horario[0]} - ({nome[0]}) - {r_cat[0]} - {r_dist[0]}m \n*TRAP: {d_dogs_b[0]}- {d_dogs_b[1]} ({venc[12]})*  \nVENCE: \nTRAP: {d_dogs_a[0]}- {d_dogs_a[1]} ({venc[11]}) \nOdd: @{odds[i+1].get_text()}💸 \nLink:{driver.current_url} \n MÉTODO: {venc[13]} \n ENTRADA PADRÃO \n f2"
                                ind = mensagem.find('@')
                                v_men = mensagem[:ind]
                                if (v_men in bot_mens) is False:
                                    if len(off) == 0:
                                        bot.mens_telegram_ia(mensagem)
                                        bot_mens.append(v_men)

                        # print(d_dogs_a[0])
                        # print(d_dogs_b[0])
                        # print(venc[11])
                        # print(venc[12])
                        if venc[11] > venc[12]:
                            v = 'A'
                        elif venc[11] < venc[12]:
                            v = 'B'
                        else:
                            v = 'EMPATE'

                        avb = f"{d_dogs_a[1]} v {d_dogs_b[1]}"
                        if (avb in env_avb) is False:
                            if venc[11] != -10 and venc[12] != -10:
                                if venc[11] > 5 or venc[12] > 5:

                                    favb.inserir_avb(pista_nome[0], nome[0], d_dogs_a[1], d_dogs_b[1], odds[i].get_text(), odds[i+1].get_text(), venc[11], venc[12],v, 0)
                                    env_avb.append(avb)

                        if venc[11] > venc[12] and abs(venc[11] - venc[12]) > 4 and venc[11] >= 9 and venc[12] < 1.76:
                            if (d_dogs_b[1] != n_dogs[0]):
                                if ((d_dogs_a[12] == 2 or d_dogs_a[12] == 1) and (d_dogs_b[12] != 2) and (venc[11] != -10 and venc[12] != -10)) or ((d_dogs_a[12] == d_dogs_b[12] and d_dogs_a[12] != 0) and (venc[11] != -10 and venc[12] != -10)):
                                    odd = float(odds[i].get_text())
                                    if (odd > 1.59) and (odd <= 2.00):
                                        mensagem = f"RR TIPS - AvB: 🐶 \n{pista_nome[0]} {horario[0]} - ({nome[0]}) - {r_cat[0]} - {r_dist[0]}m \n*TRAP: {d_dogs_a[0]}- {d_dogs_a[1]} ({venc[11]})*  \nVENCE: \nTRAP: {d_dogs_b[0]}- {d_dogs_b[1]} ({venc[12]}) \nOdd: @{odds[i].get_text()}💸 \nLink:{driver.current_url} \n MÉTODO: {venc[13]} \n ENTRADA PADRÃO \n f1"
                                        ind = mensagem.find('@')
                                        v_mens = mensagem[:ind]
                                        if (v_mens in env_mens) is False:
                                            if len(off) == 0:
                                                bot.mens_telegram(mensagem)
                                                env_mens.append(v_mens)
                                    elif venc[11] >= 10 and (odd <= 2.25):
                                        mensagem = f"RR TIPS - AvB: 🐶 \n{pista_nome[0]} {horario[0]} - ({nome[0]}) - {r_cat[0]} - {r_dist[0]}m \n*TRAP: {d_dogs_a[0]}- {d_dogs_a[1]} ({venc[11]})*  \nVENCE: \nTRAP: {d_dogs_b[0]}- {d_dogs_b[1]} ({venc[12]}) \nOdd: @{odds[i].get_text()}💸 \nLink:{driver.current_url} \n MÉTODO: {venc[13]} \n ENTRADA ARRISCADA \n f1"
                                        ind = mensagem.find('@')
                                        v_mens = mensagem[:ind]
                                        if (v_mens in env_mens) is False:
                                            if len(off) == 0:
                                                bot.mens_telegram(mensagem)
                                                env_mens.append(v_mens)

                        if venc[11] < venc[12] and abs(venc[11] - venc[12]) > 4 and venc[12] >= 9 and venc[11] < 1.76:
                            if (d_dogs_a[1] != n_dogs[0]):
                                if ((d_dogs_b[12] == 2 or d_dogs_b[12] == 1) and (d_dogs_a[12] != 2) and (venc[11] != -10 and venc[12] != -10)) or ((d_dogs_a[12] == d_dogs_b[12] and d_dogs_b[12] != 0) and (venc[11] != -10 and venc[12] != -10)):
                                    odd = float(odds[i+1].get_text())
                                    if (odd > 1.59) and (odd <= 2.00):
                                        mensagem = f"RR TIPS - AvB: 🐶 \n{pista_nome[0]} {horario[0]} - ({nome[0]}) - {r_cat[0]} - {r_dist[0]}m \n*TRAP: {d_dogs_b[0]}- {d_dogs_b[1]} ({venc[12]})*  \nVENCE: \nTRAP: {d_dogs_a[0]}- {d_dogs_a[1]} ({venc[11]}) \nOdd: @{odds[i+1].get_text()}💸 \nLink:{driver.current_url} \n MÉTODO: {venc[13]} \n ENTRADA PADRÃO \n f2"
                                        ind = mensagem.find('@')
                                        v_mens = mensagem[:ind]
                                        if (v_mens in env_mens) is False:
                                            if len(off) == 0:
                                                bot.mens_telegram(mensagem)
                                                env_mens.append(v_mens)
                                    elif venc[12] >= 10 and (odd <= 2.25):
                                        mensagem = f"RR TIPS - AvB: 🐶 \n{pista_nome[0]} {horario[0]} - ({nome[0]}) - {r_cat[0]} - {r_dist[0]}m \n*TRAP: {d_dogs_b[0]}- {d_dogs_b[1]} ({venc[12]})*  \nVENCE: \nTRAP: {d_dogs_a[0]}- {d_dogs_a[1]} ({venc[11]}) \nOdd: @{odds[i+1].get_text()}💸 \nLink:{driver.current_url} \n MÉTODO: {venc[13]} \n ENTRADA ARRISCADA \n f2"
                                        ind = mensagem.find('@')
                                        v_mens = mensagem[:ind]
                                        if (v_mens in env_mens) is False:
                                            if len(off) == 0:
                                                bot.mens_telegram(mensagem)
                                                env_mens.append(v_mens)

                        if venc[11] > venc[12] and abs(venc[11] - venc[12]) > 4 and venc[11] > 5 and venc[12] < 1:
                            if (d_dogs_b[1] != n_dogs[0]) and (d_dogs_b[1] != n_dogs[1]):
                                if (d_dogs_a[12] == 2 or d_dogs_a[12] == 1) and (d_dogs_b[12] != 2) and (venc[11] != -10 and venc[12] != -10) :
                                    odd = float(odds[i].get_text())
                                    if (odd > 1.59) and (odd <= 1.90):
                                        mensagem = f"RR TIPS - AvB: 🐶 \n{pista_nome[0]} {horario[0]} - ({nome[0]}) - {r_cat[0]} - {r_dist[0]}m \n*TRAP: {d_dogs_a[0]}- {d_dogs_a[1]} ({venc[11]})*  \nVENCE: \nTRAP: {d_dogs_b[0]}- {d_dogs_b[1]} ({venc[12]}) \nOdd: @{odds[i].get_text()}💸 \nLink:{driver.current_url} \n MÉTODO: {venc[13]} \n ENTRADA ARRISCADA \n f3"
                                        ind = mensagem.find('@')
                                        v_mens = mensagem[:ind]
                                        if (v_mens in env_mens) is False:
                                            if len(off) == 0:
                                                bot.mens_telegram(mensagem)
                                                env_mens.append(v_mens)

                        if venc[11] < venc[12] and abs(venc[11] - venc[12]) > 4 and venc[12] > 5 and venc[11] < 1:
                            if (d_dogs_a[1] != n_dogs[0]) and (d_dogs_a[1] != n_dogs[1]):
                                if (d_dogs_b[12] == 2 or d_dogs_b[12] == 1) and (d_dogs_a[12] != 2) and (venc[11] != -10 and venc[12] != -10) :
                                    odd = float(odds[i+1].get_text())
                                    if (odd > 1.59) and (odd <= 1.90):
                                        mensagem = f"RR TIPS - AvB: 🐶 \n{pista_nome[0]} {horario[0]} - ({nome[0]}) - {r_cat[0]} - {r_dist[0]}m \n*TRAP: {d_dogs_b[0]}- {d_dogs_b[1]} ({venc[12]})*  \nVENCE: \nTRAP: {d_dogs_a[0]}- {d_dogs_a[1]} ({venc[11]}) \nOdd: @{odds[i+1].get_text()}💸 \nLink:{driver.current_url} \n MÉTODO: {venc[13]} \n ENTRADA ARRISCADA \n f4"
                                        ind = mensagem.find('@')
                                        v_mens = mensagem[:ind]
                                        if (v_mens in env_mens) is False:
                                            if len(off) == 0:
                                                bot.mens_telegram(mensagem)
                                                env_mens.append(v_mens)

                        # if venc[11] > venc[12] and abs(venc[11] - venc[12]) > 6 and venc[11] > 12 :
                        #     if (d_dogs_b[1] != n_dogs[0]):
                        #         if (d_dogs_a[12] == 2 or d_dogs_a[12] == 1) and (d_dogs_b[12] != 2) and (venc[11] != -10 and venc[12] != -10) :
                        #             odd = float(odds[i].get_text())
                        #             if (odd > 1.59) and (odd <= 1.90):
                        #                 mensagem = f"RR TIPS - AvB: 🐶 \n{pista_nome[0]} {horario[0]} - ({nome[0]}) - {r_cat[0]} - {r_dist[0]}m \n*TRAP: {d_dogs_a[0]}- {d_dogs_a[1]} ({venc[11]})*  \nVENCE: \nTRAP: {d_dogs_b[0]}- {d_dogs_b[1]} ({venc[12]}) \nOdd: @{odds[i].get_text()}💸 \nLink:{driver.current_url} \n MÉTODO: {venc[13]} \n ENTRADA ARRISCADA \n f5"
                        #                 ind = mensagem.find('@')
                        #                 v_mens = mensagem[:ind]
                        #                 if (v_mens in env_mens) is False:
                        #                     if len(off) == 0:
                        #                         bot.mens_telegram(mensagem)
                        #                         env_mens.append(v_mens)

                        # if venc[11] < venc[12] and abs(venc[11] - venc[12]) > 6 and venc[12] > 12 :
                        #     if (d_dogs_a[1] != n_dogs[0]):
                        #         if (d_dogs_b[12] == 2 or d_dogs_b[12] == 1) and (d_dogs_a[12] != 2) and (venc[11] != -10 and venc[12] != -10) :
                        #             odd = float(odds[i+1].get_text())
                        #             if (odd > 1.59) and (odd <= 1.90):
                        #                 mensagem = f"RR TIPS - AvB: 🐶 \n{pista_nome[0]} {horario[0]} - ({nome[0]}) - {r_cat[0]} - {r_dist[0]}m \n*TRAP: {d_dogs_b[0]}- {d_dogs_b[1]} ({venc[12]})*  \nVENCE: \nTRAP: {d_dogs_a[0]}- {d_dogs_a[1]} ({venc[11]}) \nOdd: @{odds[i+1].get_text()}💸 \nLink:{driver.current_url} \n MÉTODO: {venc[13]} \n ENTRADA ARRISCADA \n f6"
                        #                 ind = mensagem.find('@')
                        #                 v_mens = mensagem[:ind]
                        #                 if (v_mens in env_mens) is False:
                        #                     if len(off) == 0:
                        #                         bot.mens_telegram(mensagem)
                        #                         env_mens.append(v_mens)

                        if venc[11] > venc[12] and abs(venc[11] - venc[12]) > 5 and venc[11] > 8 and venc[12] < 1.76 and (venc[11] != -10 and venc[12] != -10):
                            if (d_dogs_b[1] != n_dogs[0]):
                                if(venc[11] and venc[12] != -10) :
                                    odd = float(odds[i].get_text())
                                    if (odd > 1.59) and (odd <= 1.90):
                                        mensagem = f"RR TIPS - AvB: 🐶 \n{pista_nome[0]} {horario[0]} - ({nome[0]}) - {r_cat[0]} - {r_dist[0]}m \n*TRAP: {d_dogs_a[0]}- {d_dogs_a[1]} ({venc[11]})*  \nVENCE: \nTRAP: {d_dogs_b[0]}- {d_dogs_b[1]} ({venc[12]}) \nOdd: @{odds[i].get_text()}💸 \nLink:{driver.current_url} \n MÉTODO: {venc[13]} \n ENTRADA ARRISCADA \n s/cat"
                                        ind = mensagem.find('@')
                                        v_mens = mensagem[:ind]
                                        if (v_mens in env_mens) is False:
                                            if len(off) == 0:
                                                bot.mens_telegram(mensagem)
                                                env_mens.append(v_mens)

                        if venc[11] < venc[12] and abs(venc[11] - venc[12]) > 5 and venc[12] > 8 and venc[11] < 1.76 and (venc[11] != -10 and venc[12] != -10):
                            if (d_dogs_a[1] != n_dogs[0]):
                                if (venc[11] and venc[12] != -10) :
                                    odd = float(odds[i+1].get_text())
                                    if (odd > 1.59) and (odd <= 1.90):
                                        mensagem = f"RR TIPS - AvB: 🐶 \n{pista_nome[0]} {horario[0]} - ({nome[0]}) - {r_cat[0]} - {r_dist[0]}m \n*TRAP: {d_dogs_b[0]}- {d_dogs_b[1]} ({venc[12]})*  \nVENCE: \nTRAP: {d_dogs_a[0]}- {d_dogs_a[1]} ({venc[11]}) \nOdd: @{odds[i+1].get_text()}💸 \nLink:{driver.current_url} \n MÉTODO: {venc[13]} \n ENTRADA ARRISCADA \n s/cat"
                                        ind = mensagem.find('@')
                                        v_mens = mensagem[:ind]
                                        if (v_mens in env_mens) is False:
                                            if len(off) == 0:
                                                bot.mens_telegram(mensagem)
                                                env_mens.append(v_mens)

            driver, race_count = proc_prox_race(driver, race_count)
            time.sleep(1)

        else:
            driver, race_count = proc_prox_race(driver, race_count)
            time.sleep(1)

def proc_avb_ia(driver, race_count, env_mens, env_avb):
    while True:
        n_dogs = []

        avb_dogs = driver.find_elements(By.CLASS_NAME,"ir-RacingGreyhoundsMatchUpParticipant_Name")
        all_dogs = driver.find_elements(By.CLASS_NAME,"ir-RacingGreyhoundsFixedOddsParticipant_ParticipantName ")
        off = driver.find_elements(By.CLASS_NAME,"ir-RaceOffBanner ")
        # print(len(off))
        for i in range(0, len(all_dogs) -1):
            n_dogs.append(all_dogs[i].text)

        if len(avb_dogs) > 0:
            link = driver.current_url
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
                    a = dogs[i].get_text().strip()
                    b = dogs[i+1].get_text().strip()

                    dog_a = fbd.buscar_dog_nome(a)
                    dog_b = fbd.buscar_dog_nome(b)

                    if dog_a != None and dog_b != None:

                        d_dogs_a, d_dogs_b, venc = f.compara_av(race_id, a, b)


                        if venc[11] > venc[12]:
                            v = 'A'
                        elif venc[11] < venc[12]:
                            v = 'B'
                        else:
                            v = 'EMPATE'

                        avb = f"{d_dogs_a[1]} v {d_dogs_b[1]}"
                        if (avb in env_avb) is False:
                            if venc[11] != -10 and venc[12] != -10:
                                if venc[11] > 5 or venc[12] > 5:

                                    favb.inserir_avb(pista_nome[0], nome[0], d_dogs_a[1], d_dogs_b[1], odds[i].get_text(), odds[i+1].get_text(), venc[11], venc[12],v, 0)
                                    env_avb.append(avb)
                        predict, risco = iaa.previsao(a, b, venc)
                        print(f"{predict} - {venc[11]} - {venc[12]} - {d_dogs_a[12]} - {d_dogs_b[12]}")

                        odd_a = float(odds[i].get_text())
                        odd_b = float(odds[i+1].get_text())
                        oddss = [odd_a, odd_b]

                        if predict == 0 and (d_dogs_a[12] !=3) and (venc[12] !=-10 ):
                            odd = float(odds[i].get_text())

                            if (odd >= 1.5) and (odd <= 2.00):
                                if risco == 0:
                                    mensagem = f"RR TIPS - AvB: 🐶 \n{pista_nome[0]} {horario[0]} - ({nome[0]}) - {r_cat[0]} - {r_dist[0]}m \n🥇*TRAP: {d_dogs_a[0]}- {d_dogs_a[1]}*  \nVENCE: \nTRAP: {d_dogs_b[0]}- {d_dogs_b[1]}\nOdd: @{odds[i].get_text()}💸 \nLink:{driver.current_url} \n ENTRADA PADRÃO"
                                    # av_men = cria_mens(oddss,0,risco,a,b,race_id, driver)
                                    ind = mensagem.find('@')
                                    v_mens = mensagem[:ind]
                                    if (v_mens in env_mens) is False:
                                        if len(off) == 0:
                                            # bot.mens_telegram_ia(av_men)
                                            bot.bot_mensagem_av(oddss,0,risco,a,b,race_id,link)
                                            bot.mens_telegram(mensagem)
                                            env_mens.append(v_mens)
                                if risco == 1:
                                    mensagem = f"RR TIPS - AvB: 🐶 \n{pista_nome[0]} {horario[0]} - ({nome[0]}) - {r_cat[0]} - {r_dist[0]}m \n🥇*TRAP: {d_dogs_a[0]}- {d_dogs_a[1]}*  \nVENCE: \nTRAP: {d_dogs_b[0]}- {d_dogs_b[1]}\nOdd: @{odds[i].get_text()}💸 \nLink:{driver.current_url}\n ENTRADA ARRISCADA"
                                    # av_men = cria_mens(oddss,0,risco,a,b,race_id, driver)
                                    ind = mensagem.find('@')
                                    v_mens = mensagem[:ind]
                                    if (v_mens in env_mens) is False:
                                        if len(off) == 0:
                                            # bot.mens_telegram_ia(av_men)
                                            bot.bot_mensagem_av(oddss,0,risco,a,b,race_id,link)
                                            bot.mens_telegram(mensagem)
                                            env_mens.append(v_mens)

                            elif (odd <= 2.25):
                                mensagem = f"RR TIPS - AvB: 🐶 \n{pista_nome[0]} {horario[0]} - ({nome[0]}) - {r_cat[0]} - {r_dist[0]}m \n🥇*TRAP: {d_dogs_a[0]}- {d_dogs_a[1]}*  \nVENCE: \nTRAP: {d_dogs_b[0]}- {d_dogs_b[1]}\nOdd: @{odds[i].get_text()}💸 \nLink:{driver.current_url} \n ENTRADA ARRISCADA"
                                # av_men = cria_mens(oddss,0,risco,a,b,race_id, driver)
                                ind = mensagem.find('@')
                                v_mens = mensagem[:ind]
                                if (v_mens in env_mens) is False:
                                    if len(off) == 0:
                                        bot.bot_mensagem_av(oddss,0,risco,a,b,race_id,link)
                                        # bot.mens_telegram_ia(av_men)
                                        bot.mens_telegram(mensagem)

                                        env_mens.append(v_mens)

                        if predict == 1 and (d_dogs_b[12] !=3) and (venc[11] !=-10 ):
                            odd = float(odds[i+1].get_text())
                            if (odd >= 1.5) and (odd <= 2.00):
                                if risco == 0:
                                    mensagem = f"RR TIPS - AvB: 🐶 \n{pista_nome[0]} {horario[0]} - ({nome[0]}) - {r_cat[0]} - {r_dist[0]}m \n🥇*TRAP: {d_dogs_b[0]}- {d_dogs_b[1]}*  \nVENCE: \nTRAP: {d_dogs_a[0]}- {d_dogs_a[1]}\nOdd: @{odds[i+1].get_text()}💸 \nLink:{driver.current_url}\n ENTRADA PADRÃO"
                                    # av_men = cria_mens(oddss,1,risco,a,b,race_id, driver)
                                    ind = mensagem.find('@')
                                    v_mens = mensagem[:ind]
                                    if (v_mens in env_mens) is False:
                                        if len(off) == 0:
                                            bot.bot_mensagem_av(oddss,1,risco,a,b,race_id,link)
                                            # bot.mens_telegram_ia(av_men)
                                            bot.mens_telegram(mensagem)

                                            env_mens.append(v_mens)
                                if risco == 1:
                                    mensagem = f"RR TIPS - AvB: 🐶 \n{pista_nome[0]} {horario[0]} - ({nome[0]}) - {r_cat[0]} - {r_dist[0]}m \n🥇*TRAP: {d_dogs_b[0]}- {d_dogs_b[1]}*  \nVENCE: \nTRAP: {d_dogs_a[0]}- {d_dogs_a[1]}\nOdd: @{odds[i+1].get_text()}💸 \nLink:{driver.current_url}\n ENTRADA ARRISCADA"
                                    # av_men = cria_mens(oddss,1,risco,a,b,race_id, driver)
                                    ind = mensagem.find('@')
                                    v_mens = mensagem[:ind]
                                    if (v_mens in env_mens) is False:
                                        if len(off) == 0:
                                            bot.bot_mensagem_av(oddss,1,risco,a,b,race_id,link)
                                            # bot.mens_telegram_ia(av_men)
                                            bot.mens_telegram(mensagem)

                                            env_mens.append(v_mens)

                            elif (odd <= 2.25):
                                mensagem = f"RR TIPS - AvB: 🐶 \n{pista_nome[0]} {horario[0]} - ({nome[0]}) - {r_cat[0]} - {r_dist[0]}m \n🥇*TRAP: {d_dogs_b[0]}- {d_dogs_b[1]}*  \nVENCE: \nTRAP: {d_dogs_a[0]}- {d_dogs_a[1]}\nOdd: @{odds[i+1].get_text()}💸 \nLink:{driver.current_url}\n ENTRADA ARRISCADA"
                                # av_men = cria_mens(oddss,1,risco,a,b,race_id, driver)
                                ind = mensagem.find('@')
                                v_mens = mensagem[:ind]
                                if (v_mens in env_mens) is False:
                                    if len(off) == 0:
                                        bot.bot_mensagem_av(oddss,1,risco,a,b,race_id,link)
                                        # bot.mens_telegram_ia(av_men)
                                        bot.mens_telegram(mensagem)

                                        env_mens.append(v_mens)

            driver, race_count = proc_prox_race(driver, race_count)
            time.sleep(1)

        else:
            driver, race_count = proc_prox_race(driver, race_count)
            time.sleep(1)



