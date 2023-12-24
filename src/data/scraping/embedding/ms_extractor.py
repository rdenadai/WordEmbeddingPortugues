import asyncio
from itertools import chain
from string import ascii_lowercase

import httpx
from aiomultiprocess import Pool
from bs4 import BeautifulSoup

from .utils import save_phrases

url = "https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z"
urls = [f"{url}/{l}" for l in ascii_lowercase]


async def get_links(url):
    links = []
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(url, timeout=240)
            if r.status_code == 200:
                html = BeautifulSoup(r.content, "lxml")
                links_ = html.findAll("a", {"class": "govbr-card-content"})
                for link in links_:
                    href = link.get("href")
                    if "https://www.gov.br" not in href:
                        href = f"https://www.gov.br{href}"
                    links.append(href)
        except Exception as e:
            print(f"1. Erro ao carregar frases: {url}, {str(e)}")
    return links


async def get_content_from_links(url):
    phrases = []
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(url, timeout=240)
            if r.status_code == 200:
                html = BeautifulSoup(r.content, "lxml")
                phrases_ = html.findAll("div", {"id": "content"})
                for phrase in phrases_:
                    phrases += phrase.get_text(strip=True).strip().split(".")
        except Exception as e:
            print(f"1. Erro ao carregar frases: {url}, {str(e)}")
    return phrases


async def carregar(func, urls):
    async with Pool() as pool:
        result = await pool.map(func, urls)
    return result


if __name__ == "__main__":
    print("Iniciando Ministerio da Saude:")
    links = filter(None, chain(*asyncio.run(carregar(get_links, urls))))
    phrases = filter(None, chain(*asyncio.run(carregar(get_content_from_links, links))))
    phrases = list(set([pphrase for phrase in phrases if len(pphrase := phrase.strip()) > 10]))

    save_phrases(phrases, "/data/embedding/ministerio.txt")
    print()
