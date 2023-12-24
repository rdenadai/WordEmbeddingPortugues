import asyncio
from itertools import chain

import httpx
from bs4 import BeautifulSoup

from .utils import chunks, loader, save_phrases

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

urls = main_urls + [f"{url}page/{i}/" for i in range(2, 50) for url in main_urls]


async def get_link_content(url):
    phrases = []
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(url, timeout=240)
            if r.status_code == 200:
                html = BeautifulSoup(r.content, "lxml")
                posts = html.findAll("div", {"class": "post-content"})
                for post in posts:
                    phrases += post.get_text().strip().split(".")
    except Exception as e:
        print(f"2. Erro ao carregar frases: {url}, {str(e)}")
    return phrases


async def get_links(url):
    links = []
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(url, timeout=240)
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


if __name__ == "__main__":
    for chunked in chunks(urls, 10):
        links = filter(None, chain(*asyncio.run(loader(get_links, chunked))))
        phrases = filter(None, chain(*asyncio.run(loader(get_link_content, links))))
        phrases = [pphrase for phrase in phrases if len(pphrase := phrase.strip()) > 10]
        save_phrases("/data/embedding/fapesp.txt", phrases)
    print()
