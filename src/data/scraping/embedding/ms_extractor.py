import os
import sys
import pickle
import asyncio
from itertools import chain

import httpx
from bs4 import BeautifulSoup
from aiomultiprocess import Pool


urls = []
url = "https://www.saude.gov.br/saude-de-a-z/"


async def get_links(url):
    links = []
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(url, timeout=120)
            if r.status_code == 200:
                html = BeautifulSoup(r.content, "lxml")
                links_ = html.findAll(
                    "a", {"class": "list-group-item list-group-item-action"}
                )
                for link in links_:
                    links.append(link.get("href"))
        except Exception as e:
            print(f"1. Erro ao carregar frases: {url}, {str(e)}")
    return links


async def get_content_from_links(url):
    phrases = []
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(url, timeout=120)
            if r.status_code == 200:
                html = BeautifulSoup(r.content, "lxml")
                phrases_ = html.findAll("div", {"id": "content"})
                for phrase in phrases_:
                    phrases += phrase.get_text().strip().split(".")
        except Exception as e:
            print(f"1. Erro ao carregar frases: {url}, {str(e)}")
    return phrases


async def carregar(func, urls):
    async with Pool() as pool:
        result = await pool.map(func, urls)
    return result


if __name__ == "__main__":
    print("Iniciando Ministerio da Saude:")
    links = filter(None, chain(*asyncio.run(carregar(get_links, [url]))))
    phrases = filter(None, chain(*asyncio.run(carregar(get_content_from_links, links))))
    phrases = list(set([phrase.strip() for phrase in phrases if len(phrase) > 10]))

    try:
        sentences = []
        with open(f"{os.getcwd()}/data/embedding/ministerio.pkl", "rb") as fh:
            sentences = pickle.load(fh)
        with open(f"{os.getcwd()}/data/embedding/ministerio.pkl", "wb") as fh:
            sents = set(sentences + phrases)
            pickle.dump(list(sents), fh)
    except:
        with open(f"{os.getcwd()}/data/embedding/ministerio.pkl", "wb") as fh:
            sents = set(phrases)
            pickle.dump(list(sents), fh)
