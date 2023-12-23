import asyncio
import codecs
import os
from itertools import chain

import httpx
import numpy as np
from aiomultiprocess import Pool
from bs4 import BeautifulSoup

main_urls = list(
    set(
        [
            ("https://www.frasesdobem.com.br/frases-engracadas/", 0),
            ("https://www.frasesdobem.com.br/frases-de-dia-dos-namorados", 0),
            ("https://www.frasesdobem.com.br/frases-de-amizade", 0),
            ("https://www.frasesdobem.com.br/frases-de-carinho", 0),
            ("https://www.frasesdobem.com.br/frases-inspiradoras", 0),
            ("https://www.frasesdobem.com.br/frases-de-amor", 0),
            ("https://www.frasesdobem.com.br/frases-apaixonadas", 0),
            ("https://www.frasesdobem.com.br/frases-romanticas", 0),
            ("https://www.frasesdobem.com.br/frases-de-autoestima", 0),
            ("https://www.frasesdobem.com.br/frases-de-superacao", 0),
            ("https://www.frasesdobem.com.br/frases-de-otimismo", 0),
            ("https://www.frasesdobem.com.br/frases-de-positividade", 0),
            ("https://www.frasesdobem.com.br/frases-pensativas", 0),
            ("https://www.frasesdobem.com.br/frases-de-impacto", 0),
            ("https://www.frasesdobem.com.br/frases-filosoficas", 0),
            ("https://www.frasesdobem.com.br/frases-de-sabedoria", 0),
            ("https://www.frasesdobem.com.br/frases-religiosas", 0),
            ("https://www.frasesdobem.com.br/frases-de-motivacao", 0),
            ("https://www.frasesdobem.com.br/frases-legais", 0),
            ("https://www.frasesdobem.com.br/frases-perfeitas", 0),
            ("https://www.frasesdobem.com.br/frases-de-aventura", 0),
            ("https://www.frasesdobem.com.br/frases-de-determinacao", 0),
            ("https://www.frasesdobem.com.br/frases-de-arrependimento", 0),
            ("https://www.frasesdobem.com.br/frases-sobre-cultura", 0),
            ("https://www.frasesdobem.com.br/frases-de-liberdade", 0),
            ("https://www.frasesdobem.com.br/frases-sobre-mentira", 0),
            ("https://www.frasesdobem.com.br/frases-inveja", 0),
            ("https://www.frasesdobem.com.br/frases-ironicas", 0),
            ("https://www.pensador.com/frases_para_ofender/", 1),
            ("https://www.pensador.com/frases_de_amizade/", 1),
            ("https://www.pensador.com/recentes/", 1),
            ("https://www.pensador.com/epigrafe_para_tcc/", 1),
            ("https://www.pensador.com/mensagens_depressao/", 1),
            ("https://www.pensador.com/o_tempo_passa_depressa/", 1),
            ("https://www.pensador.com/autor/dalai_lama/", 1),
            ("https://www.pensador.com/autor/martin_luther_king/", 1),
            ("https://www.pensador.com/autor/sigmund_freud/", 1),
            ("https://www.pensador.com/autor/adolf_hitler/", 1),
            ("https://www.pensador.com/autor/adam_smith/", 1),
            ("https://www.pensador.com/autor/maisa_silva/", 1),
            ("https://www.pensador.com/autor/pabllo_vittar/", 1),
            ("https://www.pensador.com/autor/padre_fabio_de_melo/", 1),
            ("https://www.pensador.com/populares/", 1),
            ("https://www.pensador.com/frases_de_escritores_famosos/", 1),
            ("https://www.pensador.com/autor/pitagoras/", 1),
            ("https://www.pensador.com/autor/voltaire/", 1),
            ("https://www.pensador.com/frases_de_besteira/", 1),
            ("https://www.pensador.com/puta/", 1),
            ("https://www.pensador.com/vagabundo/", 1),
            ("https://www.pensador.com/pinto/", 1),
            ("https://www.pensador.com/cacete/", 1),
            ("https://www.pensador.com/puta_que_pariu/", 1),
            ("https://www.pensador.com/vara/", 1),
            ("https://www.pensador.com/vagina/", 1),
            ("https://www.pensador.com/autor/albert_einstein/", 1),
            ("https://www.pensador.com/frases_de_duvida/", 1),
            ("https://www.pensador.com/frases_para_refletir/", 1),
            ("https://www.pensador.com/frases_positivas/", 1),
            ("https://www.pensador.com/autor/edgar_allan_poe/", 1),
            ("https://www.pensador.com/maca/", 1),
            ("https://www.pensador.com/software/", 1),
            ("https://www.pensador.com/computador/", 1),
            ("https://www.pensador.com/internet/", 1),
            ("https://www.pensador.com/cozinha/", 1),
            ("https://www.pensador.com/gripe/", 1),
            ("https://www.pensador.com/morcego/", 1),
            ("https://www.pensador.com/imagem/", 1),
            ("https://www.pensador.com/guerra/", 1),
            ("https://www.pensador.com/paz/", 1),
            ("https://www.pensador.com/amor/", 1),
            ("https://www.pensador.com/rancor/", 1),
            ("https://www.pensador.com/desgosto/", 1),
            ("https://www.pensador.com/cueca/", 1),
            ("https://www.pensador.com/calcinha/", 1),
            ("https://www.pensador.com/estranho/", 1),
            ("https://www.pensador.com/remedio/", 1),
            ("https://www.pensador.com/conversa/", 1),
            ("https://www.pensador.com/pensamento/", 1),
            ("https://www.pensador.com/pensamento_para_odia_da_mulher/", 1),
            ("https://www.pensador.com/amor_de_marido_e_mulher/", 1),
            ("https://www.pensador.com/mudanca/", 1),
            ("https://www.pensador.com/confianca/", 1),
            ("https://www.pensador.com/medicamento/", 1),
            ("https://www.pensador.com/olho/", 1),
            ("https://www.pensador.com/tosse/", 1),
            ("https://www.pensador.com/nariz/", 1),
            ("https://www.pensador.com/doenca/", 1),
            ("https://www.pensador.com/errado/", 1),
            ("https://www.pensador.com/casamento/", 1),
            ("https://www.pensador.com/frases_de_tristeza/", 1),
            ("https://www.pensador.com/oculto/", 1),
            ("https://www.pensador.com/sofrimento/", 1),
            ("https://www.pensador.com/medo/", 1),
            ("https://www.pensador.com/curiosidade/", 1),
            ("https://www.pensador.com/geografia/", 1),
            ("https://www.pensador.com/medicina/", 1),
            ("https://www.pensador.com/farmacia/", 1),
            ("https://www.pensador.com/saude/", 1),
            ("https://www.pensador.com/rancor/", 1),
            ("https://www.pensador.com/sentimentos/", 1),
            ("https://www.pensador.com/intensidade/", 1),
            ("https://www.pensador.com/tortura/", 1),
            ("https://www.pensador.com/animal/", 1),
            ("https://www.pensador.com/homem/", 1),
            ("https://www.pensador.com/mulher/", 1),
            ("https://www.pensador.com/preguica/", 1),
            ("https://www.pensador.com/sarcasmo/", 1),
            ("https://www.pensador.com/poesia/", 1),
            ("https://www.pensador.com/estado/", 1),
            ("https://www.pensador.com/esquerda/", 1),
            ("https://www.pensador.com/direita/", 1),
            ("https://www.pensador.com/presidente/", 1),
            ("https://www.pensador.com/ditador/", 1),
            ("https://www.pensador.com/consciencia/", 1),
            ("https://www.pensador.com/poder/", 1),
            ("https://www.pensador.com/chefe/", 1),
            ("https://www.pensador.com/politico/", 1),
            ("https://www.pensador.com/preto/", 1),
            ("https://www.pensador.com/severo/", 1),
            ("https://www.pensador.com/merda/", 1),
            ("https://www.pensador.com/xingar/", 1),
            ("https://www.pensador.com/buceta/", 1),
            ("https://www.pensador.com/estupro/", 1),
            ("https://www.pensador.com/estupro/", 1),
            ("https://www.pensador.com/bicha/", 1),
            ("https://www.pensador.com/travesti/", 1),
            ("https://www.pensador.com/negro/", 1),
            ("https://www.pensador.com/preto/", 1),
            ("https://www.pensador.com/branco/", 1),
            ("https://www.pensador.com/pinto/", 1),
            ("https://www.pensador.com/autor/desconhecido/", 1),
            ("https://www.pensador.com/autor/pitagoras/", 1),
            ("https://www.pensador.com/autor/martin_luther_king/", 1),
            ("https://www.pensador.com/recentes/", 1),
        ]
    )
)

urls = main_urls + [f"{url}page/{i}/" if type_ == 0 else f"{url}{i}/" for i in range(2, 55) for url, type_ in main_urls]


async def get_link_content(url):
    phrases = []
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(url, timeout=240)
            if r.status_code == 200:
                html = BeautifulSoup(r.content, "lxml")
                posts = html.findAll("p", {"class": "frase"})
                for post in posts:
                    phrases += BeautifulSoup(post.get_text(), "lxml").get_text().replace("\n", " ").split(".")
        except Exception as e:
            print(f"1. Erro ao carregar frases: {url}, {str(e)}")
    return phrases


async def loader(func, urls):
    async with Pool() as pool:
        result = await pool.map(func, urls)
    return result


if __name__ == "__main__":
    phrases = filter(None, chain(*asyncio.run(loader(get_link_content, urls))))
    phrases = list(set([pphrase for phrase in phrases if len(pphrase := phrase.strip()) > 10]))

    try:
        sentences = []
        with codecs.open(f"{os.getcwd()}/data/embedding/frases.txt", "rb", encoding="utf-8") as fh:
            sentences = fh.readlines()
            sentences = [sent.strip() for sent in sentences]
        with codecs.open(f"{os.getcwd()}/data/embedding/frases.txt", "wb", encoding="utf-8") as fh:
            sents = list(set(sentences + phrases))
            np.savetxt(fh, sents, fmt="%s")
    except:
        with codecs.open(f"{os.getcwd()}/data/embedding/frases_sec.txt", "wb", encoding="utf-8") as fh:
            sents = list(set(phrases))
            np.savetxt(fh, sents, fmt="%s")
    print()
