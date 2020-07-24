import os
import sys
import time
import pickle
import random
from itertools import chain

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ProcessPoolExecutor


urls = []
for p in range(10, 54):
    for w in [w for w in "abcdefghijklmnopqrstuvwxyz"]:
        if p == 1:
            urls += [f"https://consultaremedios.com.br/bulas/{w}"]
        else:
            urls += [f"https://consultaremedios.com.br/bulas/{w}?pagina={p}"]


def chrome_options():
    options = Options()
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")  # linux only
    # options.add_argument("--headless")
    options.add_argument("--lang=pt-br")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    return options


if __name__ == "__main__":

    driver = webdriver.Chrome(
        options=chrome_options(),
        executable_path=f"{os.getcwd()}/src/scraping/driver/chromedriver",
    )

    for url in urls:
        print(url)
        driver.get(url)

        elems = []
        not_found = True
        while not_found:
            try:
                elems = driver.find_elements_by_class_name("product-block__title")
                not_found = False
                time.sleep(0.1)
            except Exception as e:
                print(f"ERROR: Not found : {str(e)}")

        bulas = []
        for elem in elems:
            remedio = elem.find_element_by_tag_name("a")
            bulas += [remedio.get_attribute("href")]

        time.sleep(1.5)

        for bula in random.sample(bulas, len(bulas)):
            driver.get(bula)

            contents = None
            not_found = True
            while not_found:
                try:
                    contents = driver.find_elements_by_class_name("leaflet-content")
                    not_found = False
                    time.sleep(0.1)
                except Exception as e:
                    print(f"ERROR: Not found : {str(e)}")

            phrases = []
            for content in contents:
                phrases += content.text.strip().split(".")

            phrases = filter(None, phrases)
            phrases = [phrase for phrase in phrases if len(phrase) > 10]

            sentences = []
            try:
                with open(f"{os.getcwd()}/data/embedding/bulas.pkl", "rb") as fh:
                    sentences = pickle.load(fh)
            except:
                pass
            with open(f"{os.getcwd()}/data/embedding/bulas.pkl", "wb") as fh:
                sents = set(sentences + phrases)
                pickle.dump(list(sents), fh)

            time.sleep(2)
        time.sleep(5)

    driver.close()
