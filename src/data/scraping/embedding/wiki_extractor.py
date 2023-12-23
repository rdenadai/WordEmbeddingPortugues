import asyncio
import codecs
import os
from itertools import chain
from sys import setrecursionlimit

import numpy as np
import wikipediaapi
from aiomultiprocess import Pool
from bs4 import BeautifulSoup

setrecursionlimit(20_000)


CATEGORIES = (
    "Filosofia",
    "Pensamento",
    "Física",
    "Pesquisa",
    "Biblioteconomia e ciência da informação",
    "Cultura",
    "Artes",
    "Geografia",
    "Lugares",
    "Saúde",
    "Cuidado pessoal",
    "Ocupações da saúde",
    "História",
    "Eventos",
    "Ciências formais",
    "Ciências",
    "Ciências naturais",
    "Natureza",
    "Pessoas",
    "Vida pessoal",
    "Ego",
    "Sobrenomes",
    "Religião",
    "Crença",
    "Sociedade",
    "Ciências sociais",
    "Tecnologia",
    "Ciências aplicadas",
)


async def load_wiki(term):
    phrases = []

    wiki = wikipediaapi.Wikipedia(
        "MyProjectName (rdenadai@gmail.com)",
        "pt",
        extract_format=wikipediaapi.ExtractFormat.WIKI,
    )
    page_py = wiki.page(term.strip())
    if page_py.exists():
        phrases = []
        text = BeautifulSoup(page_py.text, "lxml").get_text().strip()
        for parag in text.split("\n"):
            phrases += [phrase for phrase in parag.split(".")]
        phrases = set(filter(None, phrases))
        phrases = [phrase.strip() for phrase in phrases if len(phrase) > 15]
    else:
        print(f"Impossível carregar {term}")
    return phrases


def get_category_members(categorymembers, level=0, max_level=1):
    pages = []
    for c in categorymembers.values():
        pages.append(c.title)
        if c.ns == wikipediaapi.Namespace.CATEGORY and level < max_level:
            pages += get_category_members(c.categorymembers, level=level + 1, max_level=max_level)
    return pages


async def loader(func, urls):
    async with Pool() as pool:
        result = await pool.map(func, urls)
    return result


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


if __name__ == "__main__":
    print("Iniciando Wikipedia")
    print("-" * 30)

    wiki = wikipediaapi.Wikipedia(
        "MyProjectName (rdenadai@gmail.com)",
        "pt",
        extract_format=wikipediaapi.ExtractFormat.WIKI,
    )

    terms = []
    for categ in CATEGORIES:
        cat = wiki.page(f"Categoria:{categ}")
        print(f"Categoria:{categ}")
        q_terms = get_category_members(cat.categorymembers)
        print(f"Quantidade de termos: {len(q_terms)}")
        terms += q_terms

    for chunked in chunks(terms, 100):
        phrases = list(filter(None, chain(*asyncio.run(loader(load_wiki, chunked)))))
        sentences = [pphrase for phrase in phrases if len(pphrase := phrase.strip()) > 10]
        try:
            with codecs.open(f"{os.getcwd()}/data/embedding/wikipedia.txt", "rb", encoding="utf-8") as fh:
                sentences = fh.readlines()
        except:
            pass
        with codecs.open(f"{os.getcwd()}/data/embedding/wikipedia.txt", "wb", encoding="utf-8") as fh:
            sents = list(set(sentences + phrases))
            np.savetxt(fh, sents, fmt="%s")
