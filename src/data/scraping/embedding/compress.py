import os
import time
import pickle
import codecs

import numpy as np
import pandas as pd
from nltk.corpus import machado, mac_morpho, floresta

from ...processing.utils import CleanUp


def carregar_sentencas(filename):
    sentences = pd.read_pickle(filename)
    for sent in sentences:
        frase = normalizar.fit(sent)
        if len(frase) > 15:
            yield frase


def corpus_nltk(model):
    with codecs.open(
        f"{os.getcwd()}/data/embedding/corpus.txt", "ab", encoding="utf-8"
    ) as fh:
        for fileid in model.fileids():
            for sent in model.sents(fileid):
                sentence = normalizar.fit(" ".join(sent))
                if len(sentence) > 15:
                    np.savetxt(fh, [f"{' '.join(sentence)}"], fmt="%s")


if __name__ == "__main__":

    start = time.time()

    print("Carregando sentenças...")

    normalizar = CleanUp(
        remove_accentuation=False,
        remove_4_comment=False,
        remove_numbers=False,
        return_tokens=True,
    )

    print("Carregando sentenças dos corpus da NLTK...")
    for md in [machado, mac_morpho, floresta]:
        corpus_nltk(md)

    filenames = [
        f"{os.getcwd()}/data/embedding/olhar.pkl",
        f"{os.getcwd()}/data/embedding/uol.pkl",
        f"{os.getcwd()}/data/embedding/g1.pkl",
        f"{os.getcwd()}/data/embedding/r7.pkl",
        f"{os.getcwd()}/data/embedding/elpais.pkl",
        f"{os.getcwd()}/data/embedding/ministerio.pkl",
        f"{os.getcwd()}/data/embedding/frases.pkl",
        f"{os.getcwd()}/data/embedding/livros.pkl",
        f"{os.getcwd()}/data/embedding/wikipedia.pkl",
        f"{os.getcwd()}/data/embedding/fapesp.pkl",
        f"{os.getcwd()}/data/embedding/mundo.pkl",
        f"{os.getcwd()}/data/embedding/bulas.pkl",
    ]

    print("Carregando sentenças dos corpus criados...")
    with codecs.open(
        f"{os.getcwd()}/data/embedding/corpus.txt", "ab", encoding="utf-8"
    ) as fh:
        for filename in filenames:
            print(f"Carregando sentenças: {filename}")
            for sentence in carregar_sentencas(filename):
                np.savetxt(fh, [f"{' '.join(sentence)}"], fmt="%s")

    print(f"Tempo total da compressao: {round(time.time() - start, 2)}s")
