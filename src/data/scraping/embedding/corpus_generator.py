import os
import re
import codecs
import pickle
from itertools import chain

import pdftotext


if __name__ == "__main__":

    sentences = []

    path = f"{os.getcwd()}/data/corpus/pdf/"
    for root, dirs, files in os.walk(path):
        for filename in files:
            with open(f"{path}/{filename}", "rb") as f:
                try:
                    pdf = pdftotext.PDF(f)
                    for page in pdf:
                        for s, e in [
                            (r"\n+", r" . "),
                            (r"\s+", r" "),
                            (r"(\.){2,}", " . "),
                        ]:
                            page = re.sub(s, e, page)
                    for phrase in page.strip().split("."):
                        phrase = phrase.strip()
                        if len(phrase) > 15:
                            sentences += [phrase]
                except:
                    print(filename)

    path = f"{os.getcwd()}/data/corpus/txt/"
    for root, dirs, files in os.walk(path):
        for filename in files:
            with open(f"{path}/{filename}", "r") as f:
                content = f.read()
                for s, e in [
                    (r"\n+", r" . "),
                    (r"\s+", r" "),
                    (r"(\.){2,}", " . "),
                ]:
                    content = re.sub(s, e, content)
                for phrase in content.strip().split("."):
                    phrase = phrase.strip()
                    if len(phrase) > 15:
                        sentences += [phrase]

    sentences = list(set(filter(None, sentences)))
    with open(f"{os.getcwd()}/data/embedding/livros.pkl", "wb") as fh:
        pickle.dump(sentences, fh)
