from bs4 import BeautifulSoup
from selenium import webdriver


def coleta_races(link):
    driver = webdriver.Chrome()

    driver.get(link)

    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')

    races = soup.find_all('a', {'data-eventid': 'cards_card'})

    race_links = []

    for i in range(1, len(races)):
        race_link = races[i]['href']
        race_links.append(race_link)

    driver.quit()

    return(race_links)


