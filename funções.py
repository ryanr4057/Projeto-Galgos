from bs4 import BeautifulSoup
from selenium import webdriver

def coleta_pistas():
    driver = webdriver.Chrome()

    url ='https://greyhoundbet.racingpost.com/#meeting-list/view=meetings&r_date=2023-02-12'
    driver.get(url)

    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')

    pistas = soup.find_all('a', {'data-eventid': 'cards_meetings_click'})

    driver.quit()

    return(pistas)


def coleta_races(link):
    driver = webdriver.Chrome()

    url ='https://greyhoundbet.racingpost.com/{link}'
    driver.get(url)

    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')

    races = soup.find_all('a', {'data-eventid': 'cards_card'})

    race_links = []

    for i in range(1, len(races)):
        race_link = races[i]['href']
        race_links.append(race_link)

    driver.quit()

    return(race_links)


