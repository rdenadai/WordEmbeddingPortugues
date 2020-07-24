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
    "https://brasil.elpais.com/rss/brasil/portada_completo.xml",
]

urls = [
    "https://brasil.elpais.com/",
    "https://brasil.elpais.com/seccion/economia/",
    "https://brasil.elpais.com/seccion/ciencia/",
    "https://brasil.elpais.com/seccion/tecnologia/",
    "https://brasil.elpais.com/seccion/internacional/",
    "https://brasil.elpais.com/seccion/cultura/",
    "https://brasil.elpais.com/seccion/estilo/",
    "https://brasil.elpais.com/seccion/esportes/",
]


async def get_link_content(url):
    phrases = []
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(url, timeout=120)
            if r.status_code == 200:
                html = BeautifulSoup(r.content, "lxml")
                posts = html.findAll("div", {"class": "article_body"})
                for post in posts:
                    phrases += post.get_text().split(".")
    except Exception as e:
        # print(f"2. Erro ao carregar posts: {url}, {str(e)}")
        pass
    return phrases


async def get_links_pagina_inicial(url):
    links = []
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(url, timeout=120)
            if r.status_code == 200:
                html = BeautifulSoup(r.content, "lxml")
                links_ = html.findAll("h2", {"class": "headline"})
                for link in links_:
                    href = link.find("a").get("href")
                    if "https://brasil.elpais.com" not in href:
                        href = f"https://brasil.elpais.com{href}"
                    links.append(href)
    except Exception as e:
        # print(f"2. Erro ao carregar posts: {url}, {str(e)}")
        pass
    return links


async def get_links(url):
    links = []
    try:
        d = feedparser.parse(url)
        links = [item["link"] for item in d["entries"]]
    except Exception as e:
        # print(f"1. Erro ao carregar posts: {url}, {str(e)}")
        pass
    return links


async def carregar(func, urls):
    async with Pool() as pool:
        result = await pool.map(func, urls)
    return result


if __name__ == "__main__":
    print("Iniciando El Pais")
    print("-" * 30)
    links = list(filter(None, chain(*asyncio.run(carregar(get_links, rss)))))
    links += list(
        filter(None, chain(*asyncio.run(carregar(get_links_pagina_inicial, urls))),)
    )

    print(f"links carregados... {len(links)}")
    phrases = filter(None, chain(*asyncio.run(carregar(get_link_content, links))))
    phrases = [phrase.strip() for phrase in phrases if len(phrase) > 15]

    try:
        sentences = []
        with open(f"{os.getcwd()}/data/embedding/elpais.pkl", "rb") as fh:
            sentences = pickle.load(fh)
            sentences = [sent.strip() for sent in sentences]
        with open(f"{os.getcwd()}/data/embedding/elpais.pkl", "wb") as fh:
            sents = list(set(sentences + phrases))
            pickle.dump(sents, fh)
    except Exception as e:
        with open(f"{os.getcwd()}/data/embedding/elpais_sec.pkl", "wb") as fh:
            sents = set(phrases)
            pickle.dump(list(sents), fh)
    print()
