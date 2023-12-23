import asyncio
import codecs
import os
from itertools import chain

import httpx
import numpy as np
from aiomultiprocess import Pool
from bs4 import BeautifulSoup

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


async def loader(func, urls):
    async with Pool() as pool:
        result = await pool.map(func, urls)
    return result


if __name__ == "__main__":
    print("Iniciando SuperInteressante")
    print("-" * 30)
    links = list(filter(None, chain(*asyncio.run(loader(get_links, urls)))))
    print("Links carregados...")
    phrases = filter(None, chain(*asyncio.run(loader(get_link_content, links))))
    phrases = [pphrase for phrase in phrases if len(pphrase := phrase.strip()) > 10]
    with codecs.open(f"{os.getcwd()}/data/embedding/mundo.txt", "wb", encoding="utf-8") as fh:
        np.savetxt(fh, phrases, fmt="%s")
