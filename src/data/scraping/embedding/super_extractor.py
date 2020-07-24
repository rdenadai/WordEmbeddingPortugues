import os
import sys
import time
import pickle
import asyncio
from itertools import chain

import httpx
from bs4 import BeautifulSoup
from aiomultiprocess import Pool

urls = [f"https://super.abril.com.br/superarquivo/{i}/" for i in range(1, 416)]


async def get_link_content(url):
    phrases = []
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(url, timeout=60)
            if r.status_code == 200:
                html = BeautifulSoup(r.content, "lxml")
                posts = html.findAll("section")
                phrases += list(chain(*[post.get_text().split(".") for post in posts]))
    except Exception as e:
        print(f"2. Erro ao carregar posts: {url}, {str(e)}")
    return phrases


async def get_links(url):
    links = []
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(url, timeout=60)
            if r.status_code == 200:
                html = BeautifulSoup(r.content, "lxml")
                posts = html.findAll("h2", {"class": "list-item-title"})
                links = [dd.find("a").get("href") for dd in posts]
    except Exception as e:
        print(f"1. Erro ao carregar posts: {url}, {str(e)}")
    return links


async def carregar(func, urls):
    async with Pool() as pool:
        result = await pool.map(func, urls)
    return result


if __name__ == "__main__":
    links = list(filter(None, chain(*asyncio.run(carregar(get_links, urls)))))
    print("Links carregados...")
    phrases = filter(None, chain(*asyncio.run(carregar(get_link_content, links))))
    phrases = [phrase for phrase in phrases if len(phrase) > 10]
    with open(f"{os.getcwd()}/data/embedding/mundo.pkl", "wb") as fh:
        pickle.dump(phrases, fh)
