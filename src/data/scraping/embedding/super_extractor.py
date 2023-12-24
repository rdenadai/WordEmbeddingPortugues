import asyncio
from itertools import chain

import httpx
from bs4 import BeautifulSoup

from .utils import loader, save_phrases

urls = [f"https://super.abril.com.br/superarquivo/{i}/" for i in range(1, 3)]


async def get_link_content(url):
    phrases = []
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(url, timeout=120)
            if r.status_code == 200:
                html = BeautifulSoup(r.content, "lxml")
                posts = html.findAll("section", {"class": "content"})
                phrases += list(chain(*[post.get_text().strip().split(".") for post in posts]))
    except Exception as e:
        print(f"2. Erro ao carregar posts: {url}, {str(e)}")
    return phrases


async def get_links(url):
    links = []
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(url, timeout=120)
            if r.status_code == 200:
                html = BeautifulSoup(r.content, "lxml")
                posts = html.findAll("div", {"class": "list-item"})
                links = [dd.find("a").get("href") for dd in posts]
    except Exception as e:
        print(f"1. Erro ao carregar posts: {url}, {str(e)}")
    return links


if __name__ == "__main__":
    print("Iniciando SuperInteressante")
    print("-" * 30)
    links = list(filter(None, chain(*asyncio.run(loader(get_links, urls)))))
    print("Links carregados...")
    phrases = filter(None, chain(*asyncio.run(loader(get_link_content, links))))
    phrases = [pphrase for phrase in phrases if len(pphrase := phrase.strip()) > 10]
    save_phrases(phrases, "/data/embedding/mundo.txt")
    print()
