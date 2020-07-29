import os
import codecs
import asyncio
import unicodedata
from itertools import chain

import numpy as np
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
                BeautifulSoup(item["content"][0]["value"], "lxml").get_text(strip=True),
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
    phrases = [phrase.strip().replace("jpg", "") for phrase in phrases if len(phrase.split()) > 5]

    try:
        sentences = []
        with codecs.open(f"{os.getcwd()}/data/embedding/olhar.txt", "rb", encoding="utf-8") as fh:
            sentences = fh.readlines()
            sentences = [sent.strip() for sent in sentences]
        with codecs.open(f"{os.getcwd()}/data/embedding/olhar.txt", "wb", encoding="utf-8") as fh:
            sents = sorted(list(set(sentences + phrases)))
            np.savetxt(fh, sents, fmt="%s")
    except:
        with codecs.open(f"{os.getcwd()}/data/embedding/olhar_sec.txt", "wb", encoding="utf-8") as fh:
            sents = sorted(list(set(phrases)))
            np.savetxt(fh, sents, fmt="%s")
    print()
