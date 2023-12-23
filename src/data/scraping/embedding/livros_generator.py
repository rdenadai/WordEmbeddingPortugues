import codecs
import os
import re

import numpy as np
import pdftotext

if __name__ == "__main__":
    RM = [
        (r"\n+", r" "),
        (r"\s+", r" "),
        (r"(http[s]*?:\/\/)+[0-9a-zA-Z.-_\/?=]*\s*", r""),  # urls
    ]

    with codecs.open(f"{os.getcwd()}/data/embedding/livros.txt", "wb", encoding="utf-8") as fh:
        path = f"{os.getcwd()}/data/corpus/pdf/"
        for root, dirs, files in os.walk(path):
            for filename in files:
                with open(f"{path}/{filename}", "rb") as f:
                    sentences = []
                    try:
                        pdf = pdftotext.PDF(f)
                        for page in pdf:
                            for s, e in RM:
                                page = re.sub(s, e, page)
                        for phrase in page.strip().split("."):
                            phrase = phrase.strip()
                            if len(phrase.split()) > 5:
                                sentences += [phrase]
                    except:
                        print(filename)
                    sentences = list(set(filter(None, sentences)))
                    np.savetxt(fh, sentences, fmt="%s")
