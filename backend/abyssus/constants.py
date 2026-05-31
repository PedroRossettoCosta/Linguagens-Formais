# ==========================================================
# LÉXICO SAGRADO - Palavras Reservadas e Constantes
# ==========================================================

# Mapeamento de palavras-chave da linguagem Abyssus para os Tokens
ritual_keywords = {
    # --- Tipos primitivos ---
    'Sanguis': 'SANGUIS',                 # int
    'Sanguis_Fluens': 'SANGUIS_FLUENS',   # float
    'Veritas': 'VERITAS',                 # bool
    'Vazium': 'VAZIUM',                   # void

    # --- Literais booleanos ---
    'Verum': 'VERUM',                     # true
    'Falsum': 'FALSUM',                   # false

    # --- Blocos Arduino ---
    'Exordium': 'EXORDIUM',               # setup()
    'Inferna': 'INFERNA',                 # loop()

    # --- Estados digitais ---
    'Ignis': 'IGNIS',                     # HIGH
    'Tenebrae': 'TENEBRAE',               # LOW

    # --- Direção de pinos ---
    'Entrada': 'ENTRADA',                 # INPUT
    'Saida': 'SAIDA',                     # OUTPUT

    # --- Funções nativas ---
    'Habitus': 'HABITUS',                 # pinMode
    'Incantare': 'INCANTARE',             # digitalWrite
    'Sentire': 'SENTIRE',                 # digitalRead
    'Anima': 'ANIMA',                     # analogRead
    'Mora': 'MORA',                       # delay
    'Cronos': 'CRONOS',                   # millis
    'Vox': 'VOX',                         # Serial.begin
    'Revelare': 'REVELARE',               # Serial.println
    'Susurro': 'SUSURRO',                 # Serial.print (sem newline)

    # --- Controle de fluxo ---
    'Si': 'SI',                           # if
    'Aliter': 'ALITER',                   # else
    'Tormentum': 'TORMENTUM',             # while
    'Iterum': 'ITERUM',                   # for
    'Frangere': 'FRANGERE',               # break
    'Pergere': 'PERGERE',                 # continue
    'Redditum': 'REDDITUM',               # return

    # --- Diretivas de pre-processador / metaprogramacao ---
    'Invocare': 'INVOCARE',               # #include <X.h>
    'Decretum': 'DECRETUM',               # #define NAME val
    'Imutabile': 'IMUTABILE',             # const
    'Aeternum': 'AETERNUM',               # unsigned long
    'Verbum': 'VERBUM',                   # String (Arduino)
    'Nihil': 'NIHIL',                     # nullptr
    'Caos': 'CAOS',                       # escape de C++ literal

    # --- Tipos adicionais ---
    'Inscriptio': 'INSCRIPTIO',           # const char*
    'Littera': 'LITTERA',                 # char

    # --- Novos rituais e constantes para Pureza de Hardware ---
    'TemperareCronos': 'TEMPERARE_CRONOS',
    'Aevum': 'AEVUM',
    'VerbumAevum': 'VERBUM_AEVUM',
    'SignareCaos': 'SIGNARE_CAOS',
    'Inanis': 'INANIS',
    'Sacratum': 'SACRATUM',
    'NexusFidelis': 'NEXUS_FIDELIS',
    'Albus': 'ALBUS',
    'SSD1306_Tensa': 'SSD1306_TENSA',
}

# Padrões Regex (Expressões Regulares)
REGEX_ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
