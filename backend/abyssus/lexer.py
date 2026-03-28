from sly import Lexer
from abyssus.constants import ritual_keywords, REGEX_ID

class LDLexer(Lexer):
    # O conjunto de tokens continua pegando os valores dinamicamente
    tokens = { ID, NUMBER, FLOAT_NUM, PLUS, MINUS, TIMES, DIVIDE, EQUALS, DEQUALS,
               LPAREN, RPAREN, LBRACE, RBRACE, SEMI, COMMA, LT, GT } | set(ritual_keywords.values())
    
    ignore = ' \t'
    ignore_newline = r'\n+'

    # Tokens de Operadores e Símbolos
    DEQUALS = r'=='
    EQUALS  = r'='
    PLUS    = r'\+'
    MINUS   = r'-'
    TIMES   = r'\*'
    DIVIDE  = r'/'
    LT      = r'<'
    GT      = r'>'
    SEMI    = r';'
    COMMA   = r','
    LPAREN  = r'\('
    RPAREN  = r'\)'
    LBRACE  = r'\{'
    RBRACE  = r'\}'

    # Números
    FLOAT_NUM = r'\d+\.\d+'
    NUMBER    = r'\d+'
    
    # Identificadores
    ID = REGEX_ID
    
    # Mapeamento de Palavras-chave explícito (evita o erro da metaclasse SLY)
    ID['Sanguis']        = 'SANGUIS'
    ID['Sanguis_Fluens'] = 'SANGUIS_FLUENS'
    ID['Vazium']         = 'VAZIUM'
    ID['Exordium']       = 'EXORDIUM'
    ID['Inferna']        = 'INFERNA'
    ID['Habitus']        = 'HABITUS'
    ID['Incantare']      = 'INCANTARE'
    ID['Mora']           = 'MORA'
    ID['Ignis']          = 'IGNIS'
    ID['Tenebrae']       = 'TENEBRAE'
    ID['Si']             = 'SI'
    ID['Tormentum']      = 'TORMENTUM'
    ID['Redditum']       = 'REDDITUM'

    @_(r'\d+\.\d+')
    def FLOAT_NUM(self, t):
        t.value = float(t.value)
        return t

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print(f"Erro Léxico: Caractere profano '{t.value[0]}' na linha {self.lineno}")
        self.index += 1