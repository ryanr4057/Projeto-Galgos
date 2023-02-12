import requests
from bs4 import BeautifulSoup



#pagina que vamos trabalhar
url ='https://greyhoundbet.racingpost.com/#meeting-list/view=meetings&r_date=2023-02-10'

headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}

site = requests.get(url, headers=headers)
soup = BeautifulSoup(site.content, 'html.parser')
pistas = soup.find_all('div', {'class':'level level-2 list'})

print (soup)
