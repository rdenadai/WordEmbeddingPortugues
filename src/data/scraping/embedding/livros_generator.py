import codecs
import os
import re

import numpy as np
from pdftotext import PDF

if __name__ == "__main__":
    RM = [
        (r"\n+", r" "),
        (r"\s+", r" "),
        (r"(http[s]*?:\/\/)+[0-9a-zA-Z.-_\/?=]*\s*", r""),  # urls
    ]

    filename = f"{os.getcwd()}/data/embedding/livros.txt"

    with codecs.open(filename, "wb", encoding="utf-8") as fh:
        path = f"{os.getcwd()}/data/corpus/pdf/"
        for root, dirs, files in os.walk(path):
            for book_name in files:
                with open(f"{path}/{book_name}", "rb") as f:
                    sentences = []
                    try:
                        pdf = PDF(f)
                        for page in pdf:
                            for s, e in RM:
                                page = re.sub(s, e, page)
                            for phrase in page.strip().split("."):
                                if len(phrase := phrase.strip()) > 10:
                                    sentences.append(phrase)
                    except Exception as e:
                        print(book_name, str(e))
                    sentences = list(sorted(set(filter(None, sentences))))
                    np.savetxt(fh, sentences, fmt="%s")
