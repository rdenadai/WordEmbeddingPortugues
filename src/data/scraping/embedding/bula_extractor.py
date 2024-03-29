import os
import random
import time
from concurrent.futures import ProcessPoolExecutor
from string import ascii_lowercase

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

from .utils import chunks, save_phrases


def chrome_options():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")  # linux only
    options.add_argument("--headless")
    options.add_argument("--lang=pt-br")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    return options


def browser_loader(url):
    print(url)

    service = ChromeService(executable_path=f"{os.getcwd()}/src/data/scraping/driver/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options())
    driver.get(url)

    elems = []
    not_found = True
    while not_found:
        try:
            elems = driver.find_elements(By.CLASS_NAME, "product-block__title")
            not_found = False
            time.sleep(0.1)
        except Exception as e:
            print(f"ERROR: Not found : {str(e)}")

    leaflets = []
    for elem in elems:
        medicine = elem.find_element(By.TAG_NAME, "a")
        leaflets += [medicine.get_attribute("href")]

    time.sleep(random.randint(1, 2))

    for leaflet in random.sample(leaflets, len(leaflets)):
        driver.get(leaflet)

        contents = None
        not_found = True
        while not_found:
            try:
                contents = driver.find_elements(By.CLASS_NAME, "leaflet-content")
                not_found = False
                time.sleep(0.1)
            except Exception as e:
                print(f"ERROR: Not found : {str(e)}")

        phrases = []
        for content in contents:
            phrases += content.text.strip().split(".")

        phrases = filter(None, phrases)
        phrases = [pphrase for phrase in phrases if len(pphrase := phrase.strip()) > 10]

        save_phrases(phrases, "/data/embedding/bulas.txt")
        time.sleep(random.randint(1, 3))
    time.sleep(random.randint(4, 6))

    driver.close()


if __name__ == "__main__":
    urls = [
        f"https://consultaremedios.com.br/bulas/{w}"
        if p == 1
        else f"https://consultaremedios.com.br/bulas/{w}?pagina={p}"
        for p in range(1, 55)
        for w in [w for w in ascii_lowercase]
    ]
    with ProcessPoolExecutor(max_workers=2) as executor:
        for chunked_urls in chunks(urls, 10):
            executor.map(browser_loader, chunked_urls)
