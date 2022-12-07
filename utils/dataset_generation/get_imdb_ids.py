import requests
from bs4 import BeautifulSoup

# a partir de la lista de la url saca las ids de las peliculas y las imprime en consola
urls = [
    "https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&ref_=adv_prv",
    "https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start=101&ref_=adv_nxt",
    "https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start=201&ref_=adv_nxt",
    "https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start=301&ref_=adv_nxt",
    "https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start=401&ref_=adv_nxt",
    "https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start=501&ref_=adv_nxt",
    "https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start=601&ref_=adv_nxt",
    "https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start=701&ref_=adv_nxt",
    "https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start=801&ref_=adv_nxt",
    "https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start=901&ref_=adv_nxt",
]

f = open("imdbIDS.txt", "a")
for url in urls:
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    movie_data = soup.find_all("div", attrs={"class": "lister-item mode-advanced"})

    for store in movie_data:
        imdbID = (
            store.find("span", "rating-cancel").a.get("href").split("/")[2]
            if store.find("span", "rating-cancel")
            else " "
        )
        f.write(imdbID + ",")

f.close()
print("Done!")
