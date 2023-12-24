import asyncio
import unicodedata
from itertools import chain

import feedparser
from aiomultiprocess import Pool
from bs4 import BeautifulSoup

from .utils import save_phrases

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
        filter(
            None,
            chain(*chain(*asyncio.run(carregar(get_link_content, rss)))),
        )
    )
    phrases = [pphrase for phrase in phrases if len(pphrase := phrase.strip().replace("jpg", "")) > 10]
    save_phrases(phrases, "/data/embedding/olhar.txt")
    print()
