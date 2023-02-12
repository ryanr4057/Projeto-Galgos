import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# Gerando um cabeçalho HTTP com informações de um navegador
ua = UserAgent()
headers = {'User-Agent': ua.random}

# Página que vamos trabalhar
url ='https://greyhoundbet.racingpost.com/#meeting-list/view=meetings&r_date=2023-02-10'

# Realizando a requisição à página
site = requests.get(url, headers=headers)

# Criando o objeto BeautifulSoup
soup = BeautifulSoup(site.content, 'html.parser')

# Procurando elementos com a tag 'a' e um atributo 'data-eventid="cards_meetings_click"'
elementos = soup.find_all('a', {'data-eventid': 'cards_meetings_click'})

links = soup.find_all("a", attrs={"data-eventid": "cards_meetings_click"})
for link in links:
    print(link)

# Exibindo o número de elementos encontrados

