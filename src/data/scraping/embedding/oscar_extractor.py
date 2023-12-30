import codecs
import os
from time import perf_counter

import numpy as np
from datasets import load_dataset


def save_phrases(phrases, filename):
    with codecs.open(f"{os.getcwd()}{filename}", "ab", encoding="utf-8") as fh:
        sents = sorted(list(filter(None, phrases)))
        np.savetxt(fh, sents, fmt="%s")


if __name__ == "__main__":
    dataset = load_dataset(
        "oscar-corpus/OSCAR-2301",
        "pt",
        token="<your token from huggingface here>",
        streaming=True,
        trust_remote_code=True,
        split="train",
    )
    dataset = dataset.take(300_000)

    print("Carregando sentenças...")
    start = perf_counter()
    sentences = [d.get("text") for d in dataset]
    print(f"Tempo de carregamento: {(perf_counter() - start):.2f}s")
    for i, sentence in enumerate(sentences):
        phrases = (phrase for phrase in sentence.replace("\n", ". ").strip().split("."))
        phrases = (pphrase for phrase in phrases if len(pphrase := phrase.strip()) > 15)
        save_phrases(list(phrases), "/data/embedding/pt_oscar_part.txt")
        if i > 0 and i % 100 == 0:
            print(f"{i} items processados")
    print(f"Tempo de execução: {(perf_counter() - start):.2f}s")
    print()
