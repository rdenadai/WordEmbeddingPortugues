import os
import pickle
from itertools import chain

from bs4 import BeautifulSoup
import wikipediaapi


if __name__ == "__main__":

    wiki_wiki = wikipediaapi.Wikipedia(
        "pt", extract_format=wikipediaapi.ExtractFormat.WIKI
    )

    termos = sorted(
        list(
            set(
                """
                Doença,febre,Cefaleia,tosse,coriza,covid-19,pandemia,epidemia,Economia,presidente,parlamento,
                medicina,medico,diarreia,virus,influenza,gripe,sistema imunitário,imunologia,dengue,Célula,coração,
                pulmão,rim,remédio,medicamento,cloroquina,hidroxicloroquina,medicação antimalárica,anvisa,parlamento,
                presidencialismo,deputado,ministro,infusão,xarope,alquimia,farmacologia,carbocisteína,náuseas,doutor,
                tontura,palpitação,insônia,stresse psicológico,Insuficiência_cardíaca,demência,hipnótico,Transtorno_de_ansiedade,
                ansiedade,corpo humano,fenomenologia,inflamação,infecção,toxina,hospital,hospital psiquiátrico,placebo,
                analgésico,comprimido,inalação,via respiratória,coronavírus,vírus_ebola,doença_por_vírus_ébola,
                organização_mundial_da_saúde,índice_de_massa_corporal,exercício_físico,transtorno_mental,neurocirurgia,
                biópsia,asma,bronquite,pneumonia,tuberculose,sputum,sono,alergia,Matemática,Estatística,Significância_estatística,
                Distribuição_normal,Variável_aleatória,Inferência_estatística,História_da_medicina,Garganta,Amor,Sistema_límbico,
                Mamíferos,Cabelo,Poluição,Química,Programação_de_computadores,Linguagem_de_programação,Computador,Processamento_de_dados,
                Banco_de_dados,Modelo_hierárquico_de_banco_de_dados,Modelo_entidade_relacionamento,Engenharia_de_software,
                Biblioteca_(computação),Orientação_a_objetos,Trauma_físico,Música,Ritmo,Poesia,Links,Libélula,
                Portugal,Brasil,Insetos,Ecossistema,Espécie,Presidencialismo,BRICS,Banco_Mundial,Ditadura_militar_brasileira,
                Intervenção_federal,Brasil_na_Segunda_Guerra_Mundial,Segunda_Guerra_Mundial,Rio_de_Janeiro,Natal,
                Proclamação_da_República_do_Brasil,Guerra_dos_Ossos,Vazamento_de_gás_em_Vishakhapatnam,Prisão_perpétua,
                Fertilização_in_vitro,Reprodução_medicamente_assistida,Espermatozoide,Cabeça,Órgãos_dos_sentidos,
                Cérebro,Cerebelo,Fundação_Nobel,Teoria_das_cordas,Dimensão,Espaço-tempo,Mecânica_clássica,Relatividade_restrita,
                Velocidade_da_luz,Lei_de_Gauss,Magnetismo,Ciência_natural,Geociência,Astronomia,Corpo_celeste,
                Espaço_sideral,Radiação_eletromagnética,Vibração,Engenharia,Meio_ambiente,Aquecimento_global,
                Ventilação_mecânica,Reanimação_cardiorrespiratória,Sangue,Hormona,Sistema_endócrino,Glândula,
                Muco,Estômago,Duodeno,Python,Linguagem_interpretada,JavaScript,Linguagem_de_programação_multiparadigma,
                Programação_estruturada,Edsger_Dijkstra,Sistema_de_processamento_distribuído,Supercomputador,
                Bomba_nuclear,Relações_internacionais,Agorafobia,Fobia_social,Transtorno_de_pânico,Medo,Psicologia,
                Ciência_cognitiva,Filosofia_da_mente,Percepção,Imagem_por_ressonância_magnética,Radiação,Luz_solar,
                Usina_solar,Turbina_a_vapor,Combustível,Gás_natural,Micro-organismo,Taxonomia,Biologia,Organismo_multicelular,
                Pediatria,Neurologia,Fisioterapia,Evolução,Genética,Organismo,Enxofre,Massa_atômica,Carbono,Diamante,
                Sistema_cristalino_cúbico,Alotropia,Grafite,Bateria_(eletricidade),Cátodo,Eletrodoméstico,Exaustor,
                Cozinha,Máquina_de_lavar_roupa,Motor_elétrico,Frenagem_regenerativa,Energia_elétrica,Usina_termoelétrica,
                Vapor_de_água,Gás,Estados_físicos_da_matéria,Velocidade,Aceleração,Gravidade,Eletromagnetismo,Fenilefrina,
                Agonista,Substância,Membrana_plasmática,Midríase,Pupila,Olho,Vertebrados,Medula_espinhal,Suor,Transpiração,
                Proteína,Macromolécula,Lípido,Vesícula,Bicapa_lipídica,Enzima,Via_metabólica,Vitamina,Ácido_ascórbico,
                Osso,Dente,Tendão,Vaso_sanguíneo,Aorta,Diástole,Músculo,Tecido,Floema,Flor,Semente,Embrião,Óvulo,
                Feminilidade,Masculinidade,Zigoto,Meiose,Reprodução_sexuada,Fecundação,Cromossomo,Núcleo_celular,Diâmetro,
                Vagina,Órgão_sexual,Vulva,Hímen,Pênis,Sémen,Ejaculação,Hermes_e_Renato,Puberdade,Menstruação,Terror_(gênero),
                Fantasia_(gênero),Jogo_eletrônico,Oseltamivir,Fenilefrina,Midríase,Receptor_adrenérgico_alfa_1,Pulp,
                Western_(gênero),Velho_Oeste,Evolução_territorial_dos_Estados_Unidos,Orfenadrina,Clorfeniramina,Influenzavirus_A_subtipo_H1N1,
                Gripe_espanhola,Agente_patogénico,Protozoário,Pandemia_de_gripe_A_de_2009,Paciente_zero,Síndrome_da_imunodeficiência_adquirida,
                Anarcocapitalismo,Astronomia,América_Latina,Anarquismo,Aquecimento_global,Agricultura,Algoritmo,Abacaxi,Aipim,
                Arqueologia,Antropologia,Alemanha,Arte,América_do_Norte,Ateísmo,Artesanato,Administração,Agnóstico,Rei_Artur,
                Agrofloresta,Brasil,Biologia,Bioquímica,Bromelaína,Biologia_celular,Barroco,Bíblia,Cânon_bíblico,Beato,Bom_Despacho,
                Geociência,Computação,Canadá,Criador,Cristianismo,Cientologia,Computador_quântico,China,Cinema,Cinética_química,Carnívoros,
                Conscienciologia,Computadores,Ciência,Célula_Combustível,Cerveja,Criptografia,Cidadania,Clima_Polar,Urso-polar,
                Caribe,Capitalismo,Clima,Cometa,Zoologia,Deus,Darwinismo,Damas,Dante_Alighieri,Desenho,Esperanto,Estatística,Fascismo
                """.split(
                    ","
                )
            )
        )
    )

    for term in termos:
        page_py = wiki_wiki.page(term.strip())
        if page_py.exists():
            phrases = []
            texto = BeautifulSoup(page_py.text, "lxml").get_text()
            for parag in texto.split("\n"):
                phrases += [frase for frase in parag.split(".")]
            phrases = set(filter(None, phrases))
            phrases = [phrase.strip() for phrase in phrases if len(phrase) > 15]

            sentences = []
            try:
                with open(f"{os.getcwd()}/data/embedding/wikipedia.pkl", "rb") as fh:
                    sentences = pickle.load(fh)
                    sentences = [sent.strip() for sent in sentences]
            except:
                pass
            with open(f"{os.getcwd()}/data/embedding/wikipedia.pkl", "wb") as fh:
                sents = set(sentences + phrases)
                pickle.dump(list(sents), fh)
        else:
            print(f"Impossível carregar {term}")

    # with open(f"{os.getcwd()}/data/wikipedia.pkl", "wb") as fh:
    #     pickle.dump(phrases, fh)
    # with open(f{os.getcwd()}/data/wikipedia.pkl, rb) as fh:
    #     phrases = pickle.load(fh)
