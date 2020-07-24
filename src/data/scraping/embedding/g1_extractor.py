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
    "http://g1.globo.com/dynamo/brasil/rss2.xml",
    "http://g1.globo.com/dynamo/carros/rss2.xml",
    "http://g1.globo.com/dynamo/ciencia-e-saude/rss2.xml",
    "http://g1.globo.com/dynamo/concursos-e-emprego/rss2.xml",
    "http://g1.globo.com/dynamo/economia/rss2.xml",
    "http://g1.globo.com/dynamo/mundo/rss2.xml",
    "http://g1.globo.com/dynamo/educacao/rss2.xml",
    "hhttp://g1.globo.com/dynamo/musica/rss2.xml",
    "http://g1.globo.com/dynamo/natureza/rss2.xml",
    "http://g1.globo.com/dynamo/planeta-bizarro/rss2.xml",
    "http://g1.globo.com/dynamo/politica/mensalao/rss2.xml",
    "http://g1.globo.com/dynamo/pop-arte/rss2.xml",
    "http://g1.globo.com/dynamo/tecnologia/rss2.xml",
    "http://g1.globo.com/dynamo/turismo-e-viagem/rss2.xml",
    "http://g1.globo.com/dynamo/vc-no-g1/rss2.xml",
    "https://g1.globo.com/rss/g1/sc/santa-catarina/",
    "https://g1.globo.com/rss/g1/sp/piracicaba-regiao/",
    "https://g1.globo.com/rss/g1/sp/santos-regiao/",
    "https://g1.globo.com/rss/g1/rs/rio-grande-do-sul/",
    "https://g1.globo.com/rss/g1/rio-de-janeiro/",
    "https://g1.globo.com/rss/g1/pr/norte-noroeste/",
    "https://g1.globo.com/rss/g1/goias/",
    "https://g1.globo.com/rss/g1/minas-gerais/",
    "https://g1.globo.com/rss/g1/ma/maranhao/",
    "http://revistagalileu.globo.com/Revista/Common/Rss/0,,DMI0-17579,00-MATERIAS.xml",
    "http://revistaepoca.globo.com/Revista/Epoca/Rss/0,,DMI0-15210,00.xml",
    "http://revistaepoca.globo.com/Revista/Epoca/Rss/0,,EDT0-15224,00.xml",
    "http://revistapegn.globo.com/Revista/Common/Rss/0,,DMI0-17148,00.xml",
    "http://revistacriativa.globo.com/Revista/Common/Rss/0,,DMS0-17111,00.xml",
    "http://revistacriativa.globo.com/Revista/Common/Rss/0,,DMS0-17111,00.xml",
    "http://revistacasaejardim.globo.com/Revista/Common/Rss/0,,DMS0-16802,00-GIRO.xml",
    "http://revistaepoca.globo.com/Revista/Epoca/Rss/0,,EDT0-15257,00.xml",
]


async def get_link_content(url):
    phrases = []
    try:
        d = feedparser.parse(url)
        phrases = [
            BeautifulSoup(item["description"], "lxml").get_text().split(".")
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
    print("Iniciando G1")
    print("-" * 30)
    phrases = list(
        filter(None, chain(*chain(*asyncio.run(carregar(get_link_content, rss)))),)
    )
    phrases = [phrase.strip() for phrase in phrases if len(phrase) > 15]

    try:
        sentences = []
        with open(f"{os.getcwd()}/data/embedding/g1.pkl", "rb") as fh:
            sentences = pickle.load(fh)
            sentences = [sent.strip() for sent in sentences]
        with open(f"{os.getcwd()}/data/embedding/g1.pkl", "wb") as fh:
            sents = set(sentences + phrases)
            pickle.dump(list(sents), fh)
    except:
        with open(f"{os.getcwd()}/data/embedding/g1_sec.pkl", "wb") as fh:
            sents = set(phrases)
            pickle.dump(list(sents), fh)
    print()
