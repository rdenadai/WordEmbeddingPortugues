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
    "https://olhardigital.com.br/rss",
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
    print("Iniciando Olhar Digital")
    print("-" * 30)
    phrases = list(
        filter(None, chain(*chain(*asyncio.run(carregar(get_link_content, rss)))),)
    )
    phrases = [phrase.strip() for phrase in phrases if len(phrase) > 15]

    try:
        sentences = []
        with open(f"{os.getcwd()}/data/embedding/olhar.pkl", "rb") as fh:
            sentences = pickle.load(fh)
            sentences = [sent.strip() for sent in sentences]
        with open(f"{os.getcwd()}/data/embedding/olhar.pkl", "wb") as fh:
            sents = set(sentences + phrases)
            pickle.dump(list(sents), fh)
    except:
        with open(f"{os.getcwd()}/data/embedding/olhar_sec.pkl", "wb") as fh:
            sents = set(phrases)
            pickle.dump(list(sents), fh)
    print()
