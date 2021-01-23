import os
import time
import warnings
import codecs
from functools import partial
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import pandas as pd
from nltk.corpus import machado, mac_morpho, floresta

from ...processing.utils import CleanUp, divide_chunks


warnings.filterwarnings("ignore")


def load_sentences(tipo, sentence):
    sentence = sentence[0] if tipo == 0 else " ".join(sentence)
    sentence = normalizar.fit(sentence)
    if len(sentence) >= 5:
        return ' '.join(sentence).strip()
    return None


def carregar_sentencas(fh, filename):
    with ProcessPoolExecutor() as exc:
        sentences = pd.read_csv(filename, header=None, sep="\\n", iterator=True, chunksize=5000)
        for sents in sentences:
            sentences_ = list(filter(None, exc.map(partial(load_sentences, 0), sents.to_numpy(dtype=str), chunksize=100)))
            if len(sentences_) > 0:
                np.savetxt(fh, sentences_, fmt="%s")


def corpus_nltk(fh, model):
    with ProcessPoolExecutor() as exc:
        for fileid in model.fileids():
            for sents in divide_chunks(model.sents(fileid), 5000):
                sentences_ = list(filter(None, exc.map(partial(load_sentences, 1), sents, chunksize=100)))
                if len(sentences_) > 0:
                    np.savetxt(fh, sentences_, fmt="%s")


if __name__ == "__main__":

    start = time.time()

    print("Carregando sentenças...")

    normalizar = CleanUp(
        remove_accentuation=False,
        remove_4_comment=False,
        remove_numbers=False,
        return_tokens=True,
    )

    with codecs.open(
        f"{os.getcwd()}/data/embedding/corpus.txt", "ab", encoding="utf-8"
    ) as fh:
        print("Carregando sentenças dos corpus da NLTK...")
        for md in [machado, mac_morpho, floresta]:
            corpus_nltk(fh, md)

        filenames = [
            f"{os.getcwd()}/data/embedding/olhar.txt",
            f"{os.getcwd()}/data/embedding/uol.txt",
            f"{os.getcwd()}/data/embedding/g1.txt",
            f"{os.getcwd()}/data/embedding/r7.txt",
            f"{os.getcwd()}/data/embedding/elpais.txt",
            f"{os.getcwd()}/data/embedding/ministerio.txt",
            f"{os.getcwd()}/data/embedding/frases.txt",
            f"{os.getcwd()}/data/embedding/livros.txt",
            f"{os.getcwd()}/data/embedding/textos.txt",
            f"{os.getcwd()}/data/embedding/wikipedia.txt",
            f"{os.getcwd()}/data/embedding/fapesp.txt",
            f"{os.getcwd()}/data/embedding/mundo.txt",
            f"{os.getcwd()}/data/embedding/bulas.txt",
            f"{os.getcwd()}/data/embedding/history.txt",
            f"{os.getcwd()}/data/embedding/copiados_manualmente.txt",
            f"{os.getcwd()}/data/embedding/temario_2.txt",
            f"{os.getcwd()}/data/embedding/frases_outras.txt",
            f"{os.getcwd()}/data/embedding/por-br_newscrawl_2011_1M-sentences.txt",
            f"{os.getcwd()}/data/embedding/por_wikipedia_2016_1M-sentences.txt",
            f"{os.getcwd()}/data/embedding/pt_dedup_part.txt",
        ]

        print("Carregando sentenças dos corpus criados...")
        for filename in filenames:
            print(f"Carregando sentenças: {filename}")
            carregar_sentencas(fh, filename)

    print(f"Tempo total da compressao: {round(time.time() - start, 2)}s")
