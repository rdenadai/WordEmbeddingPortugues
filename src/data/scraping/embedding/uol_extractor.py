import asyncio
import codecs
import os
from itertools import chain

import feedparser
import httpx
import numpy as np
from aiomultiprocess import Pool
from bs4 import BeautifulSoup

rss = [
    "http://rss.uol.com.br/feed/tecnologia.xml",
    "http://rss.home.uol.com.br/index.xml",
    "https://www.uol.com.br/esporte/ultimas/index.xml",
    "http://rss.uol.com.br/feed/jogos.xml",
    "http://rss.uol.com.br/feed/cinema.xml",
    "http://rss.uol.com.br/feed/economia.xml",
    "http://rss.uol.com.br/feed/noticias.xml",
]


async def get_link_content(url):
    phrases = []
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(url, timeout=60)
            if r.status_code == 200:
                html = BeautifulSoup(r.content, "lxml")
                posts = html.findAll("div", {"class": "text"})
                for post in posts:
                    phrases += post.get_text().split(".")
    except Exception as e:
        print(f"2. Erro ao carregar posts: {url}, {str(e)}")
    return phrases


async def get_links(url):
    links = []
    try:
        d = feedparser.parse(url)
        links = [item["link"] for item in d["entries"]]
    except Exception as e:
        print(f"1. Erro ao carregar posts: {url}, {str(e)}")
    return links


async def loader(func, urls):
    async with Pool() as pool:
        result = await pool.map(func, urls)
    return result


if __name__ == "__main__":
    print("Iniciando Uol")
    print("-" * 30)
    links = list(filter(None, chain(*asyncio.run(loader(get_links, rss)))))
    print(f"links carregados... {len(links)}")
    phrases = filter(None, chain(*asyncio.run(loader(get_link_content, links))))
    phrases = [pphrase for phrase in phrases if len(pphrase := phrase.strip()) > 10]

    try:
        sentences = []
        with codecs.open(f"{os.getcwd()}/data/embedding/uol.txt", "rb", encoding="utf-8") as fh:
            sentences = fh.readlines()
            sentences = [sent.strip() for sent in sentences]
        with codecs.open(f"{os.getcwd()}/data/embedding/uol.txt", "wb", encoding="utf-8") as fh:
            sents = sorted(list(set(sentences + phrases)))
            np.savetxt(fh, sents, fmt="%s")
    except:
        with codecs.open(f"{os.getcwd()}/data/embedding/uol_sec.txt", "wb", encoding="utf-8") as fh:
            sents = sorted(list(set(phrases)))
            np.savetxt(fh, sents, fmt="%s")
    print()
