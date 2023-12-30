import re
from functools import lru_cache
from string import punctuation
from unicodedata import normalize

import emoji
import nltk
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def divide_chunks(lista, n):
    # looping till length l
    for i in range(0, len(lista), n):
        yield lista[i : i + n]


@lru_cache(maxsize=256)
def is_number(s):
    try:
        complex(s)  # for int, long, float and complex
    except ValueError:
        return False
    return True


@lru_cache(maxsize=256)
def get_stopwords():
    stpwords = stopwords.words("portuguese")
    punkt = [pk for pk in punctuation]
    rms = ["um", "não", "mais", "muito", "sem", "estou", "sou"]
    for rm in rms:
        del stpwords[stpwords.index(rm)]
    for rm in ["?", "!", ",", ";", ":", "'", '"']:
        del punkt[punkt.index(rm)]
    return stpwords, punkt


def remover_acentos(txt):
    return normalize("NFKD", txt).encode("ASCII", "ignore").decode("ASCII")


def normalizar(phrase, sort=True):
    if phrase:
        phrase = remover_acentos(phrase.lower())
        for punkt in punctuation:
            phrase = phrase.replace(punkt, " ")
        phrase = phrase.split()
        if sort:
            phrase = sorted(phrase)
        phrase = "".join(phrase).strip()
    return phrase


class CleanUp:
    def __init__(
        self,
        remove_stopwords=False,
        remove_emojis=True,
        remove_accentuation=True,
        remove_numbers=True,
        remove_4_comment=True,
        stemmer=None,
        lemmatizer=None,
        return_tokens=False,
    ) -> None:
        self.remove_stopwords = remove_stopwords
        self.remove_emojis = remove_emojis
        self.remove_accentuation = remove_accentuation
        self.remove_numbers = remove_numbers
        self.remove_4_comment = remove_4_comment
        self.stemmer = stemmer
        self.lemmatizer = lemmatizer
        self.return_tokens = return_tokens
        self.STOPWORDS, self.PUNCT = self.get_stopwords()
        self.RM = [
            (r"(http[s]*?:\/\/)+[0-9a-zA-Z.-_\/?=]*\s*", r""),  # urls
            # (r"(Em resposta)", ""),  # Reply
            (r"(@[0-9a-zA-Z_]+)", r""),  # Username
            (r"\n+", r" . "),
            (r'"', r" "),
            (r"\'", r" "),
            (r"#", r""),
            (r"[…]", " . "),
            (r"(kkk)+", " rir "),
            (r"“", r""),
            (r"”", ""),
            (r"\s+", r" "),
            (r"\b(RT)\b", r""),
            (r"\b(coronga)\b", r"corona"),
            (r"\b(vairus)\b", r"virus"),
            (r"\b(hcq)\b", r"hidroxicloroquina"),
            (r"\b(n)\b", "nao"),
            (r"\b(ñ)\b", "nao"),
            (r"\b(nã)\b", "nao"),
            (r"\b(nãoo)\b", "nao"),
            (r"\b(vc)\b", "voce"),
            (r"\b(vcs)\b", "voces"),
            (r"\b(vzs)\b", "voces"),
            (r"\b(crlh)\b", "caralho"),
            (r"\b(crl)\b", "caralho"),
            (r"\b(krl)\b", "caralho"),
            (r"\b(carai)\b", "caralho"),
            (r"\b(caraio)\b", "caralho"),
            (r"\b(trampo)\b", "trabalho"),
            (r"\b(to)\b", "estou"),
            (r"\b(tô)\b", "estou"),
            (r"\b(ta)\b", "esta"),
            (r"\b(cu)\b", "anus"),
            (r"\b(mds)\b", "meu deus"),
            (r"\b(plmdds)\b", "pelo amor de deus"),
            (r"\b(meudeus)\b", "meu deus"),
            (r"\b(dms)\b", "demais"),
            (r"\b(cm)\b", "com"),
            (r"\b(cmg)\b", "comigo"),
            (r"\b(ctz)\b", "certeza"),
            (r"\b(crtz)\b", "certeza"),
            (r"\b(fd)\b", "foda"),
            (r"\b(sfd)\b", "foda"),
            (r"\b(fodase)\b", "foda"),
            (r"\b(blz)\b", "beleza"),
            (r"\b(muie)\b", "mulher"),
            (r"\b(vey)\b", "velho"),
            (r"\b(vei)\b", "velho"),
            (r"\b(facul)\b", "faculdade"),
            (r"\b(slk)\b", "voce e louco"),
            (r"\b(loko)\b", "louco"),
            (r"\b(mlk)\b", "moleque"),
            (r"\b(qse)\b", "quase"),
            (r"\b(bomdia)\b", "bom dia"),
            (r"\b(febria)\b", "febre"),
            (r"\b(nmrl)\b", "na moral"),
            (r"\b(mt)\b", "muito"),
            (r"\b(mto)\b", "muito"),
            (r"\b(mta)\b", "muita"),
            (r"\b(sdd)\b", "saudade"),
            (r"\b(sds)\b", "saudades"),
            (r"\b(qm)\b", "quem"),
            (r"\b(vo)\b", "vou"),
            (r"\b(hj)\b", "hoje"),
            (r"\b(tb)\b", "tambem"),
            (r"\b(agr)\b", "agora"),
            (r"\b(obg)\b", "obrigado"),
            (r"\b(miga)\b", "amiga"),
            (r"\b(migo)\b", "amigo"),
            (r"\b(dps)\b", "depois"),
            (r"\b(coronavirusbrasil)\b", "corona virus brasil"),
            (r"\b(pqp)\b", "puta que pariu"),
            (r"\b(vtnc)\b", "vai tomar no anus"),
            (r"\b(tmnc)\b", "vai tomar no anus"),
            (r"\b(vtmnc)\b", "vai tomar no anus"),
            (r"\b(tossi)\b", "tosse"),
            (r"\b(fé)\b", "deus"),
            (r"\b(scrr)\b", "socorro"),
            (r"\b(dnv)\b", "de novo"),
            (r"\b(kct)\b", "cacete"),
            (r"\b(falta de ar)\b", "nao consigo respirar"),
        ]

        if self.remove_4_comment:
            self.RM += [
                (r"([aeiouqwtyupdfghjklçzxcvbnm|?!@$%&\.\[\]\(\)+-_=<>,;:])\1+", r"\1"),
                (r"[?]+", r" duvida"),
            ]

        if self.remove_numbers:
            self.RM += [
                (r"[0-9]*", r""),
            ]

    def remover_acentos(self, phrase):
        return normalize("NFKD", phrase).encode("ASCII", "ignore").decode("ASCII")

    @lru_cache(maxsize=256)
    def is_number(self, word):
        try:
            complex(word)  # for int, long, float and complex
        except ValueError:
            return False
        return True

    @lru_cache(maxsize=256)
    def get_stopwords(self):
        stpwords = stopwords.words("portuguese")
        punkt = [pk for pk in punctuation] + ["—"]
        rms = ["um", "não", "mais", "muito", "sem", "estou", "sou"]
        for rm in rms:
            del stpwords[stpwords.index(rm)]
        for rm in ["?", "!"]:
            del punkt[punkt.index(rm)]
        return stpwords, punkt

    def fit(self, phrase):
        # Transforma as hashtags em palavras
        try:
            for group in re.findall(r"#\S+\b", phrase, re.DOTALL):
                g2 = re.sub(r"([A-Z])", r" \1", group, flags=re.MULTILINE)
                phrase = re.sub(r"{}\b".format(group), g2, phrase, flags=re.MULTILINE)
        except Exception:
            pass
        # lowercase para fazer outros pre-processamentos
        phrase = phrase.lower()
        phrase = phrase.replace("?", " ? ")
        phrase = phrase.replace("!", " ! ")
        phrase = phrase.replace("'", " ' ")
        phrase = phrase.replace('"', ' " ')
        phrase = phrase.replace(";", " ; ")
        phrase = phrase.replace(":", " : ")
        # Remove strings padrão existente, como urls
        for o, r in self.RM:
            phrase = re.sub(o, r, phrase, flags=re.MULTILINE)
        # Remoção de emojis
        if self.remove_emojis:
            phrase = emoji.replace_emoji(phrase, "")
        if self.remove_stopwords:
            for stw in self.STOPWORDS:
                phrase = re.sub(r"\b{}\b".format(stw), "", phrase, flags=re.MULTILINE)
        # Remove pontuação
        for punct in self.PUNCT:
            phrase = phrase.replace(punct, " ")
        if self.remove_accentuation:
            phrase = self.remover_acentos(phrase)

        # Limpeza extra
        clean_frase = phrase
        if self.lemmatizer or self.stemmer:
            phrase = word_tokenize(phrase)
            clean_frase = []
            clfa = clean_frase.append
            for palavra in phrase:
                if len(palavra) > 2:
                    if self.lemmatizer:
                        palavra = "".join([word.lemma_ for word in self.lemmatizer(palavra)])
                    if self.stemmer:
                        clfa(self.stemmer.stem(palavra))
                    else:
                        clfa(palavra)
            clean_frase = " ".join(clean_frase).strip() if not self.return_tokens else clean_frase
        elif self.return_tokens:
            clean_frase = word_tokenize(phrase)
        return clean_frase


# GLOBALS
NLP_LEMMATIZER = spacy.load("pt_core_news_sm")
RSLP_STEMMER = nltk.stem.RSLPStemmer()
SNOWBALL_STEMMER = nltk.stem.SnowballStemmer("portuguese")
STOPWORDS, PUNCT = get_stopwords()
