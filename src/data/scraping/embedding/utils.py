import codecs
import os

import numpy as np
from aiomultiprocess import Pool


async def loader(func, urls):
    async with Pool() as pool:
        result = await pool.map(func, urls)
    return result


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def save_phrases(phrases, filename):
    try:
        sentences = []
        with codecs.open(f"{os.getcwd()}{filename}", "rb", encoding="utf-8") as fh:
            sentences = fh.readlines()
            sentences = [sent.strip() for sent in sentences]
        with codecs.open(f"{os.getcwd()}{filename}", "wb", encoding="utf-8") as fh:
            sents = sorted(list(set(filter(None, sentences + phrases))))
            np.savetxt(fh, sents, fmt="%s")
    except Exception as e:
        with codecs.open(f"{os.getcwd()}{filename}.sec", "wb", encoding="utf-8") as fh:
            sents = list(set(phrases))
            np.savetxt(fh, sents, fmt="%s")
        print(str(e))
