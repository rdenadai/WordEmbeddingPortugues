import os
import time
import warnings
import codecs

import numpy as np
import pandas as pd
from nltk.corpus import machado, mac_morpho, floresta

from ...processing.utils import CleanUp


warnings.filterwarnings("ignore")


def carregar_sentencas(filename):
    sentences = pd.read_csv(filename, header=None, sep="\\n", iterator=True, chunksize=5000)
    for sents in sentences:
        for sent in sents.to_numpy(dtype=str):
            frase = normalizar.fit(sent[0])
            if len(frase) >= 5:
                yield frase


def corpus_nltk(model):
    with codecs.open(
        f"{os.getcwd()}/data/embedding/corpus.txt", "ab", encoding="utf-8"
    ) as fh:
        for fileid in model.fileids():
            for sent in model.sents(fileid):
                sentence = normalizar.fit(" ".join(sent))
                if len(sentence) >= 5:
                    np.savetxt(fh, [f"{' '.join(sentence).strip()}"], fmt="%s")


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
        f"{os.getcwd()}/data/embedding/copiados_manualmente.txt",
        f"{os.getcwd()}/data/embedding/temario_2.txt",
        f"{os.getcwd()}/data/embedding/frases_outras.txt",
        f"{os.getcwd()}/data/embedding/por-br_newscrawl_2011_1M-sentences.txt",
        f"{os.getcwd()}/data/embedding/por_wikipedia_2016_1M-sentences.txt",
        f"{os.getcwd()}/data/embedding/pt_dedup_part.txt",
    ]

    print("Carregando sentenças dos corpus criados...")
    with codecs.open(
        f"{os.getcwd()}/data/embedding/corpus.txt", "ab", encoding="utf-8"
    ) as fh:
        for filename in filenames:
            print(f"Carregando sentenças: {filename}")
            for sentence in carregar_sentencas(filename):
                np.savetxt(fh, [f"{' '.join(sentence).strip()}"], fmt="%s")

    print(f"Tempo total da compressao: {round(time.time() - start, 2)}s")
