import difflib
from sly import Lexer
from abyssus.constants import ritual_keywords

class LDLexer(Lexer):
    tokens = {
        'ID', 'NUMBER', 'FLOAT_NUM', 'HEX_NUM', 'STRING_LIT',
        # Aritméticos
        'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD',
        # Atribuição / igualdade / comparação
        'EQUALS', 'DEQUALS', 'NEQ', 'LT', 'GT', 'LE', 'GE',
        # Lógicos
        'AND', 'OR', 'NOT', 'AMP',
        # Ternário
        'QUEST', 'COLON',
        # Indexação / arrays
        'LBRACKET', 'RBRACKET',
        # Pontuação
        'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
        'SEMI', 'COMMA', 'DOT'
    } | set(ritual_keywords.values())

    ignore = ' \t'
    ignore_newline = r'\n+'
    # Comentários de linha estilo C: //...
    ignore_comment = r'//[^\n]*'

    def __init__(self):
        # O Lexer guarda seus próprios erros de digitação
        self.erros_lexicos = []

    # ===== Operadores multi-caractere PRIMEIRO =====
    DEQUALS = r'=='
    NEQ     = r'!='
    LE      = r'<='
    GE      = r'>='
    AND     = r'&&'
    OR      = r'\|\|'

    # ===== Operadores simples =====
    EQUALS   = r'='
    NOT      = r'!'
    PLUS     = r'\+'
    MINUS    = r'-'
    TIMES    = r'\*'
    DIVIDE   = r'/'
    MOD      = r'%'
    LT       = r'<'
    GT       = r'>'
    AMP      = r'&'
    QUEST    = r'\?'
    COLON    = r':'
    LBRACKET = r'\['
    RBRACKET = r'\]'
    SEMI     = r';'
    COMMA    = r','
    DOT      = r'\.'
    LPAREN   = r'\('
    RPAREN   = r'\)'
    LBRACE   = r'\{'
    RBRACE   = r'\}'

    # === A MÁGICA DA VALIDAÇÃO LÉXICA ===
    @_(r'[a-zA-Z_][a-zA-Z0-9_]*')
    def ID(self, t):
        # 1. É uma palavra reservada exata?
        if t.value in ritual_keywords:
            t.type = ritual_keywords[t.value]
        else:
            # 2. Se não for, verifica se o usuário não digitou errado!
            # Ignoramos variáveis muito curtas (como 'led', 'x', 'y') para não dar falso positivo
            if len(t.value) >= 3:
                sugestoes = difflib.get_close_matches(t.value, ritual_keywords.keys(), n=1, cutoff=0.75)
                if sugestoes:
                    self.erros_lexicos.append({
                        "linha": t.lineno,
                        "mensagem": f"Heresia Léxica: Palavra '{t.value}' desconhecida. Você quis invocar '{sugestoes[0]}'?"
                    })
        return t

    @_(r'0x[0-9a-fA-F]+')
    def HEX_NUM(self, t):
        return t  # mantém string "0x3C" para o transpiler preservar formato

    @_(r'\d+\.\d+')
    def FLOAT_NUM(self, t):
        t.value = float(t.value)
        return t

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    @_(r'\".*?\"')
    def STRING_LIT(self, t):
        t.value = t.value[1:-1]
        return t

    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        self.erros_lexicos.append({
            "linha": self.lineno,
            "mensagem": f"Caractere totalmente alienígena e profano '{t.value[0]}'."
        })
        self.index += 1
