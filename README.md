# Word Embedding Portugues

Repositório contendo implementações e modelos prontos para utilização em projetos de língua portuguesa (pt-br)

## Model

Para realizar o download do modelo treinado (latest) acessar a tag: https://github.com/rdenadai/WordEmbeddingPortugues/releases/tag/0.5

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
$> python -m spacy download en_core_web_sm
$> python -m spacy download pt_core_news_sm
```

Adicionar quais fontes, por exemplo:

```bash
$> python -m src.data.scraping.embedding.g1_extractor && python -m src.data.scraping.embedding.r7_extractor && python -m src.data.scraping.embedding.uol_extractor && python -m src.data.scraping.embedding.olhar_extractor
$> python -m src.data.scraping.embedding.ms_extractor
$> python -m src.data.scraping.embedding.history_extractor
$> python -m src.data.scraping.embedding.super_extractor
$> python -m src.data.scraping.embedding.fapesp_extractor
$> python -m src.data.scraping.embedding.frases_extractor
$> python -m src.data.scraping.embedding.wiki_extractor
```

Realizar a compressão de todas as fontes no **corpus.txt**:

```bash
$> python -m src.data.scraping.embedding.compress
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

Tokens: 981032


preto:
----------------------------
branco               0.79271
dourado              0.75473
cinza                0.7517

branco:
----------------------------
branca               0.79388
preto                0.79271
roxo                 0.75019

pássaro:
----------------------------
pássaros             0.77602
rouxinol             0.76595
hipopótamo           0.76495

lobo:
----------------------------
lobos                0.68262
grilo                0.6768
cervo                0.65533

mulher:
----------------------------
homem                0.81129
menina               0.78433
mulheres             0.78332

masculino:
----------------------------
feminino             0.93773
masculina            0.78407
masculinos           0.75772

sexo:
----------------------------
anal                 0.75536
lésbicas             0.73125
casadas              0.72926

montanha:
----------------------------
montanhas            0.83201
cume                 0.76717
encosta              0.75054

oceano:
----------------------------
mar                  0.85017
atlântico            0.82862
índico               0.80854

lua:
----------------------------
lunar                0.77559
vênus                0.74723
saturno              0.74295

amor:
----------------------------
amar                 0.87775
ternura              0.82058
ama                  0.81664

senhor:
----------------------------
deus                 0.81284
bênção               0.73848
jesus                0.7338

cimegripe:
----------------------------
tylemax              0.94798
multigrip            0.92398
resfenol             0.91868

nimesulida:
----------------------------
piroxicam            0.87322
aceclofenaco         0.85994
cetorolaco           0.85348

médico:
----------------------------
médica               0.7801
farmacêutico         0.75659
enfermeiro           0.74377

doença:
----------------------------
enfermidade          0.8341
doenças              0.80768
diagnosticada        0.75124

coração:
----------------------------
corações             0.7691
peito                0.70349
alma                 0.69359

febre:
----------------------------
gripe                0.70652
febril               0.7033
calafrios            0.70099

dor:
----------------------------
dores                0.81258
fraqueza             0.75222
cansaço              0.74616

coriza:
----------------------------
espirros             0.92211
rinorreia            0.90646
congestão            0.89289

rancor:
----------------------------
mágoa                0.90915
ressentimento        0.88113
mágoas               0.85594

mau:
----------------------------
mal                  0.75896
ruim                 0.758
bom                  0.75281

ódio:
----------------------------
rancor               0.83729
ressentimento        0.83663
desprezo             0.8141

braço:
----------------------------
braços               0.78534
ombro                0.70091
pescoço              0.69574

maçã:
----------------------------
maça                 0.86816
fruta                0.83217
abacaxi              0.82906

coco:
----------------------------
côco                 0.85456
amêndoas             0.79517
limão                0.77927

['lobo', 'mau']:
----------------------------
aliás                0.70607
cão                  0.705
estúpido             0.70402

espada:
----------------------------
adaga                0.77907
cavaleiro            0.74836
espadas              0.74721

cavaleiro:
----------------------------
cavaleiros           0.78636
espada               0.74836
guerreiro            0.7291

rei:
----------------------------
rainha               0.78159
trono                0.77125
monarca              0.76254

arthur:
----------------------------
wallace              0.77768
artur                0.772
walter               0.77049

['rei', 'arthur']:
----------------------------
artur                0.76853
samuel               0.73962
conde                0.73692
```

## Referencias

- [Repositório de Word Embeddings do NILC](http://nilc.icmc.usp.br/nilc/index.php/repositorio-de-word-embeddings-do-nilc)
