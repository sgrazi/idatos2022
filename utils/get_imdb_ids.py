import requests
from bs4 import BeautifulSoup

# a partir de la lista de la url saca las ids de las peliculas y las imprime en consola
url = "https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start=901&ref_=adv_nxt"
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
movie_data = soup.find_all('div', attrs = {'class': 'lister-item mode-advanced'})

for store in movie_data:
    imdbID = store.find('span','rating-cancel').a.get('href').split('/')[2] if store.find('span','rating-cancel') else ' '
    print(imdbID)