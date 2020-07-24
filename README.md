# Word Embedding Portugues

Repositório contendo implementações e modelos prontos para utilização em projetos de língua portuguesa (pt-br)

## Extratores de frases

Todos os arquivos dentro do diretório **src/data/scraping/embedding** foram criados para a extração de frases de diversas fontes da língua portuguesa.

Cada fonte gera um arquivo em separado com os dados que vão crescendo conforme novas execuções são realizadas.

Todos os arquivos devem ser unidos em um único nomeado **corpus.txt** usando para isso o algoritmo implementado no arquivo **compress.py**.

Posteriormente este arquivo pode ser utilizado para o treinamento de um modelo Word2Vec ou Doc2Vec conforme implementado dentro do diretório **src/model/embedding.py**.

## Como executar

Instalar dependencias:

```bash
$> virtualenv venv
$> pip install -r requirements.txt
$> source venv/bin/activate
$> python -m nltk.downloader stopwords
$> python -m nltk.downloader punkt
$> python -m nltk.downloader rslp
$> python -m nltk.downloader perluniprops
$> python -m nltk.downloader machado
$> python -m nltk.downloader mac_morpho
$> python -m nltk.downloader floresta
$> python -m spacy download en
$> python -m spacy download pt
```

Adicionar quais fontes, por exemplo:
```bash
$> python -m src.data.scraping.g1_extractor
$> python -m src.data.scraping.r7_extractor
$> python -m src.data.scraping.super_extractor
$> python -m src.data.scraping.uol_extractor
$> python -m src.data.scraping.wiki_extractor
```

Realizar a compressão de todas as fontes no **corpus.txt**:
```bash
$> python -m src.data.scraping.compress
```

Para treinar **Word2Vec**:
```bash
$> python -m src.model.embedding --model 0
```

Para treinar **Doc2Vec**:
```bash
$> python -m src.model.embedding --model 1
```

## Exemplos

```python
from gensim.models import Word2Vec, KeyedVectors, Doc2Vec
from gensim.test.utils import get_tmpfile

# KeyedVectors
fname = get_tmpfile(f"{os.getcwd()}/../models/w2v.vectors.kv")
w2v = KeyedVectors.load(fname, mmap='r')

print(f"Tokens: {len(w2v.wv.vocab.keys())}")

for word in [
    "preto", "branco", "pássaro", "lobo", "mulher", "masculino", "sexo", "montanha", "oceano", 
    "lua", "amor", "senhor", "cimegripe", "nimesulida", "médico",  "doença", "coração", "febre",
    "dor", "coriza", "rancor", "mau", "ódio", "braço", "maçã", "coco", ["lobo", "mau"],
    "espada", "cavaleiro", "rei", "arthur", ["rei", "arthur"]
]:
    print(f"{word}:")
    print("-" * 28)
    for w in w2v.most_similar(word)[:3]:
        print(w[0].ljust(20), round(w[1], 5))
    print()

# -----------------------------------------------------------------------

Tokens: 470098


preto:
----------------------------
dourado              0.69609
cinza                0.6934
roxo                 0.6605

branco:
----------------------------
branca               0.69341
roxo                 0.68869
cor                  0.68784

pássaro:
----------------------------
papagaio             0.85398
elefante             0.84935
cervo                0.83688

lobo:
----------------------------
grilo                0.67553
lobos                0.67445
papagaio             0.66639

mulher:
----------------------------
homem                0.82249
marido               0.73247
menina               0.71697

masculino:
----------------------------
feminino             0.91455
masculina            0.72587
sexo                 0.72037

sexo:
----------------------------
masculino            0.72037
casadas              0.69381
gays                 0.68765

montanha:
----------------------------
montanhas            0.79327
cume                 0.78206
encosta              0.76285

oceano:
----------------------------
atlântico            0.84032
pacífico             0.8222
mares                0.80524

lua:
----------------------------
saturno              0.75039
vênus                0.74862
lunar                0.73247

amor:
----------------------------
amar                 0.83297
felicidade           0.79607
eterno               0.79195

senhor:
----------------------------
deus                 0.7443
vós                  0.68096
jacó                 0.67475

cimegripe:
----------------------------
tylemax              0.94386
tylenol              0.93661
resfenol             0.92632

nimesulida:
----------------------------
betaciclodextrina    0.85896
cetorolaco           0.84627
piroxicam            0.84337

médico:
----------------------------
prescrever           0.72763
farmacêutico         0.72713
enfermeiro           0.72338

doença:
----------------------------
doenças              0.78361
enfermidade          0.74385
parkinson            0.67882

coração:
----------------------------
bombear              0.65573
peito                0.64056
cardíaco             0.62405

febre:
----------------------------
calafrios            0.69845
chikungunya          0.68675
febril               0.68431

dor:
----------------------------
dores                0.79311
desconforto          0.75892
fraqueza             0.72801

coriza:
----------------------------
rinorreia            0.91968
congestão            0.90853
rinorréia            0.89808

rancor:
----------------------------
mágoa                0.90364
mágoas               0.90274
egoísmo              0.8758

mau:
----------------------------
ruim                 0.70129
prejudicado          0.68033
péssimo              0.65002

ódio:
----------------------------
rancor               0.81527
desprezo             0.79735
ressentimento        0.78899

braço:
----------------------------
braços               0.73446
esquerdo             0.5893
cega                 0.58108

maçã:
----------------------------
fruta                0.84694
maça                 0.82989
abóbora              0.82285

coco:
----------------------------
amêndoas             0.81718
limão                0.81387
abacate              0.81098

['lobo', 'mau']:
----------------------------
ruim                 0.69736
olhado               0.68966
preguiçoso           0.68806

espada:
----------------------------
flecha               0.80553
adaga                0.78984
armadura             0.77611

cavaleiro:
----------------------------
guerreiro            0.76632
espada               0.76358
samurai              0.76008

rei:
----------------------------
imperador            0.78201
monarca              0.73164
trono                0.72483

arthur:
----------------------------
wallace              0.79685
edgar                0.79551
simon                0.79144

['rei', 'arthur']:
----------------------------
dario                0.76836
herdeiro             0.75698
conde                0.75097
```

## Referencias

 - [Repositório de Word Embeddings do NILC](http://nilc.icmc.usp.br/nilc/index.php/repositorio-de-word-embeddings-do-nilc)