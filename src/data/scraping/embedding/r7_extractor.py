import asyncio
import unicodedata
from itertools import chain

import feedparser
from bs4 import BeautifulSoup

from .utils import loader, save_phrases

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
                BeautifulSoup(item["content"][0]["value"], "lxml").get_text(strip=True),
            ).split(".")
            for item in d["entries"]
        ]
    except Exception as e:
        print(f"1. Erro ao carregar posts: {url}, {str(e)}")
    return phrases


if __name__ == "__main__":
    print("Iniciando R7")
    print("-" * 30)
    phrases = list(
        filter(
            None,
            chain(*chain(*asyncio.run(loader(get_link_content, rss)))),
        )
    )
    phrases = [pphrase for phrase in phrases if len(pphrase := phrase.strip()) > 10]
    save_phrases(phrases, "/data/embedding/r7.txt")
    print()
