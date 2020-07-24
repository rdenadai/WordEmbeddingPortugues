import os
import sys
import time
import pickle
import asyncio
from itertools import chain

import httpx
from bs4 import BeautifulSoup
from aiomultiprocess import Pool
import feedparser


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


async def carregar(func, urls):
    async with Pool() as pool:
        result = await pool.map(func, urls)
    return result


if __name__ == "__main__":
    print("Iniciando Uol")
    print("-" * 30)
    links = list(filter(None, chain(*asyncio.run(carregar(get_links, rss)))))
    print(f"links carregados... {len(links)}")
    phrases = filter(None, chain(*asyncio.run(carregar(get_link_content, links))))
    phrases = [phrase.strip() for phrase in phrases if len(phrase) > 15]

    try:
        sentences = []
        with open(f"{os.getcwd()}/data/embedding/uol.pkl", "rb") as fh:
            sentences = pickle.load(fh)
            sentences = [sent.strip() for sent in sentences]
        with open(f"{os.getcwd()}/data/embedding/uol.pkl", "wb") as fh:
            sents = set(sentences + phrases)
            pickle.dump(list(sents), fh)
    except:
        with open(f"{os.getcwd()}/data/embedding/uol_sec.pkl", "wb") as fh:
            sents = set(phrases)
            pickle.dump(list(sents), fh)
    print()
