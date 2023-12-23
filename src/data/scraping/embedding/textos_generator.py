import codecs
import os
import re

import numpy as np

if __name__ == "__main__":
    RM = [
        (r"\n+", r" "),
        (r"\s+", r" "),
        (r"(http[s]*?:\/\/)+[0-9a-zA-Z.-_\/?=]*\s*", r""),  # urls
    ]

    with codecs.open(f"{os.getcwd()}/data/embedding/textos.txt", "wb", encoding="utf-8") as fh:
        path = f"{os.getcwd()}/data/corpus/txt/"
        for root, dirs, files in os.walk(path):
            for filename in files:
                sentences = []
                with open(f"{path}/{filename}", "r") as f:
                    content = f.read()
                    for s, e in RM:
                        content = re.sub(s, e, content)
                    for phrase in content.strip().split("."):
                        phrase = phrase.strip()
                        if len(phrase.split()) > 5:
                            sentences += [phrase]
                sentences = list(set(filter(None, sentences)))
                np.savetxt(fh, sentences, fmt="%s")
