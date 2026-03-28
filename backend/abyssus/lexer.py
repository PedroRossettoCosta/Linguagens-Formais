from sly import Lexer
from abyssus.constants import ritual_keywords

class LDLexer(Lexer):
    # Usando STRINGS explicitamente para garantir que o SLY registre os tokens corretamente
    tokens = { 
        'ID', 'NUMBER', 'FLOAT_NUM', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 
        'EQUALS', 'DEQUALS', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 
        'SEMI', 'COMMA', 'LT', 'GT' 
    } | set(ritual_keywords.values())
    
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
    
    # Identificadores (Expressão regular inline para a metaclass do SLY não se perder)
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    
    # Mapeamento de Palavras-chave explícito
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