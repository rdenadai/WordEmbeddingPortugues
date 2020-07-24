import os
import sys
import time
import pickle
import asyncio
import unicodedata
from itertools import chain

import httpx
from bs4 import BeautifulSoup
from aiomultiprocess import Pool
import feedparser


rss = [
    "https://noticias.r7.com/hora-7/feed.xml",
    "http://noticias.r7.com/saude/feed.xml",
    "http://noticias.r7.com/distrito-federal/feed.xml",
    "http://noticias.r7.com/economia/feed.xml",
    "http://noticias.r7.com/brasil/feed.xml",
    "http://noticias.r7.com/educacao/feed.xml",
    "http://noticias.r7.com/internacional/feed.xml",
    "http://noticias.r7.com/tecnologia-e-ciencia/feed.xml",
    "http://diversao.r7.com/pop/jovem/feed.xml",
    "http://noticias.r7.com/cidades/feed.xml",
]


async def get_link_content(url):
    phrases = []
    try:
        d = feedparser.parse(url)
        phrases = [
            unicodedata.normalize(
                "NFKD",
                BeautifulSoup(item["content"][0]["value"], "lxml").get_text(strip=False),
            ).split(".")
            for item in d["entries"]
        ]
    except Exception as e:
        print(f"1. Erro ao carregar posts: {url}, {str(e)}")
    return phrases


async def carregar(func, urls):
    async with Pool() as pool:
        result = await pool.map(func, urls)
    return result


if __name__ == "__main__":
    print("Iniciando R7")
    print("-" * 30)
    phrases = list(
        filter(None, chain(*chain(*asyncio.run(carregar(get_link_content, rss)))),)
    )
    phrases = [phrase.strip() for phrase in phrases if len(phrase) > 15]

    try:
        sentences = []
        with open(f"{os.getcwd()}/data/embedding/r7.pkl", "rb") as fh:
            sentences = pickle.load(fh)
            sentences = [sent.strip() for sent in sentences]
        with open(f"{os.getcwd()}/data/embedding/r7.pkl", "wb") as fh:
            sents = set(sentences + phrases)
            pickle.dump(list(sents), fh)
    except:
        with open(f"{os.getcwd()}/data/embedding/r7_sec.pkl", "wb") as fh:
            sents = set(phrases)
            pickle.dump(list(sents), fh)
    print()
