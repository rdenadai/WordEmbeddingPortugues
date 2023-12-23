import time
from datetime import datetime

import arrow
import httpx
from aiomultiprocess import Pool
from bs4 import BeautifulSoup


async def get_link_content(url):
    phrases = []
    try:
        time.sleep(1.5)
        async with httpx.AsyncClient() as client:
            r = await client.get(url, timeout=240)
            if r.status_code == 200:
                html = BeautifulSoup(r.content, "lxml")
                posts = html.findAll("article", {"class": "hstEntry__content"})
                for post in posts:
                    phrases += post.get_text(strip=True).split(".")
    except Exception as e:
        print(f"2. Erro ao carregar posts: {url}, {str(e)}")
    return phrases


async def get_links(url):
    links = []
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(url, timeout=240)
            if r.status_code == 200:
                html = BeautifulSoup(r.content, "lxml")
                links_ = html.findAll("article", {"class": "block-opacable hstBlock"})
                for link in links_:
                    href = link.find("a").get("href")
                    if "https://history.uol.com.br" not in href:
                        href = f"https://history.uol.com.br{href}"
                    links.append(href)
    except Exception:
        # print(f"2. Erro ao carregar posts: {url}, {str(e)}")
        pass
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
        f"https://history.uol.com.br/hoje-na-historia/{start_date.shift(days=d).format('YYYY-MM-DD')}"
        for d in range(1, 366)
    ]
    print(links)
    # links = list(filter(None, chain(*asyncio.run(carregar(get_links, links)))))
    # print(f"Links carregados... {len(links)}")
    # phrases = filter(None, chain(*asyncio.run(carregar(get_link_content, links))))
    # phrases = [phrase.strip() for phrase in phrases if len(phrase) > 15 and not phrase.startswith("Imagem:")]

    # try:
    #     sentences = []
    #     with codecs.open(f"{os.getcwd()}/data/embedding/history.txt", "rb", encoding="utf-8") as fh:
    #         sentences = fh.readlines()
    #         sentences = [sent.strip() for sent in sentences]
    #     with codecs.open(f"{os.getcwd()}/data/embedding/history.txt", "wb", encoding="utf-8") as fh:
    #         sents = sorted(list(set(sentences + phrases)))
    #         np.savetxt(fh, sents, fmt="%s")
    # except:
    #     with codecs.open(f"{os.getcwd()}/data/embedding/history_sec.txt", "wb", encoding="utf-8") as fh:
    #         sents = sorted(list(set(phrases)))
    #         np.savetxt(fh, sents, fmt="%s")
    # print()
