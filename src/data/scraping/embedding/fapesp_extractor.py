import os
import sys
import pickle
import asyncio
from itertools import chain

import httpx
from bs4 import BeautifulSoup
from aiomultiprocess import Pool

main_urls = [
    "https://revistapesquisa.fapesp.br/category/impressa/humanidades/",
    "https://revistapesquisa.fapesp.br/saude/",
    "https://revistapesquisa.fapesp.br/category/impressa/tecnologia/",
    "https://revistapesquisa.fapesp.br/category/impressa/ciencia/",
    "https://revistapesquisa.fapesp.br/ambiente/",
    "https://revistapesquisa.fapesp.br/category/impressa/carreiras/",
    "https://revistapesquisa.fapesp.br/tag/etica/",
    "https://revistapesquisa.fapesp.br/category/impressa/entrevista/",
    "https://revistapesquisa.fapesp.br/category/impressa/politica/",
]

urls = []
for url in main_urls:
    urls += [url]
    for i in range(2, 50):
        urls += [f"{url}page/{i}/"]


async def get_link_content(url):
    phrases = []
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(url, timeout=240)
            if r.status_code == 200:
                html = BeautifulSoup(r.content, "lxml")
                posts = html.findAll("div", {"class": "post-content"})
                for post in posts:
                    phrases += post.get_text().split(".")
    except Exception as e:
        print(f"2. Erro ao carregar frases: {url}, {str(e)}")
    return phrases


async def get_links(url):
    links = []
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(url, timeout=60)
            if r.status_code == 200:
                html = BeautifulSoup(r.content, "lxml")
                try:
                    post = html.findAll("div", {"class": "posts"})[0]
                    for dd in post.findAll("div"):
                        links += [dd.find("a").get("href")]
                except:
                    print(f"Erro ao carregar posts: {url}")
    except Exception as e:
        print(f"1. Erro ao carregar pagina: {url}, {str(e)}")
    return links


async def carregar(func, urls):
    async with Pool() as pool:
        result = await pool.map(func, urls)
    return result


if __name__ == "__main__":
    links = filter(None, chain(*asyncio.run(carregar(get_links, urls))))
    phrases = filter(None, chain(*asyncio.run(carregar(get_link_content, links))))
    phrases = [phrase for phrase in phrases if len(phrase) > 15]
    with open(f"{os.getcwd()}/data/embedding/fapesp.pkl", "wb") as fh:
        pickle.dump(phrases, fh)
