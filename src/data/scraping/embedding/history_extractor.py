import asyncio
from datetime import datetime
from itertools import chain
from random import randint

import arrow
import httpx
from aiomultiprocess import Pool
from bs4 import BeautifulSoup

from .utils import save_phrases


async def get_link_content(url):
    phrases = []
    try:
        await asyncio.sleep(randint(1, 3))
        async with httpx.AsyncClient() as client:
            r = await client.get(url, timeout=240)
            if r.status_code == 200:
                html = BeautifulSoup(r.content, "lxml")
                posts = html.findAll("div", {"class": "content"})
                for post in posts:
                    phrases += post.get_text(strip=True).split(".")
    except Exception as e:
        print(f"2. Erro ao carregar posts: {url}, {str(e)}")
    return phrases


async def get_links(url):
    links = []
    try:
        await asyncio.sleep(randint(1, 2))
        async with httpx.AsyncClient() as client:
            r = await client.get(url, timeout=240, follow_redirects=True)
            if r.status_code == 200:
                html = BeautifulSoup(r.content, "lxml")
                links_ = html.findAll("div", {"class": "card-img"})
                for link in links_:
                    href = link.find("a").get("href")
                    if "https://www.canalhistory.com.br" not in href:
                        href = f"https://www.canalhistory.com.br{href}"
                    links.append(href)
    except Exception as e:
        print(f"2. Erro ao carregar links: {url}, {str(e)}")
    return links


async def carregar(func, urls):
    async with Pool(processes=4) as pool:
        result = await pool.map(func, urls)
    return result


if __name__ == "__main__":
    print("Iniciando History")
    print("-" * 30)
    start_date = arrow.get(datetime(2020, 1, 1))
    links = [
        f"https://history.uol.com.br/hoje-na-historia/{start_date.shift(days=d).format('DD/MM')}" for d in range(1, 366)
    ]
    links = list(filter(None, chain(*asyncio.run(carregar(get_links, links)))))
    print(f"Links carregados... {len(links)}")
    phrases = filter(None, chain(*asyncio.run(carregar(get_link_content, links))))
    phrases = [
        pphrase for phrase in phrases if len(pphrase := phrase.strip()) > 10 and not phrase.startswith("Imagem:")
    ]
    save_phrases(phrases, "/data/embedding/history.txt")
    print()
