import random, requests, os, math
from time import sleep
from bs4 import BeautifulSoup


""" GLOBAL VARIABELS """

PASTES_LIMIT = 40  # 40 pastes for each keyword =>

""" GLOBAL VARIABELS """


with open('keywords.txt', 'r') as file:
    keywords = [i.replace("\n", "") for i in file.readlines()]
    links = {i: [] for i in keywords}

for keyword in keywords:
    original_keyword = keyword
    keyword = keyword.replace(' ', '+')

    c = 0
    for _ in range(math.ceil(PASTES_LIMIT / 10)):
        r = requests.get(f'https://www.google.com/search?q={keyword}+site%3Ahttps%3A%2F%2Fpastebin.com&start={c}',
                         timeout=20, headers={'User-Agent': 'Mozilla/5.0'})

        site = BeautifulSoup(r.content, 'html.parser')

        search_links = [i['href'] for i in site.find_all('a') if "/url?q=https://pastebin" in i['href']]

        if not any("/url?q=https://pastebin" in l for l in search_links):
            break

        for link in search_links:
            key = keyword.replace("+", " ")
            link = link.split('/url?q=')[1].split('&')[0]
            if link not in links[key]:
                links[key].append(link)

        print(f"searching for: {original_keyword}...")
        c += 10
        sleep(5)

    if keyword == keywords[-1]:
        break

    print("waiting...")
    sleep(random.uniform(17, 22))



if not os.path.exists("results"):
    os.mkdir("results")

for k in links.keys():
    txt = f"==> {k} <==\n\n"
    for v in links[k]:
        txt += f"{v}\n"
    txt += "\n\n"

    with open(f'results/{k}.txt', 'w+') as file:
        file.write(txt)