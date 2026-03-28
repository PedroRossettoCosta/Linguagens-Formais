import difflib

from sly import Parser
from abyssus.constants import ritual_keywords
from abyssus.lexer import LDLexer

class LDParser(Parser):
    tokens = LDLexer.tokens
    
    def __init__(self):
            self.erros_sintaticos = []

    precedence = (
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE),
    )

    @_('statements')
    def program(self, p):
        return ('PROGRAM', p.statements)

    @_('statement statements')
    def statements(self, p):
        return [p.statement] + p.statements

    @_('empty')
    def statements(self, p):
        return []

    # --- DECLARAÇÕES ---
    @_('SANGUIS ID EQUALS expr SEMI')
    def statement(self, p):
        return ('VAR_DECL', 'int', p.ID, p.expr)
    
    @_('SANGUIS_FLUENS ID EQUALS expr SEMI')
    def statement(self, p):
        return ('VAR_DECL', 'float', p.ID, p.expr)
    
    @_('ID EQUALS expr SEMI')
    def statement(self, p):
        return ('ASSIGN', p.ID, p.expr)
    
    # --- ESTRUTURAS DE CONTROLE ---
    @_('SI LPAREN condition RPAREN LBRACE statements RBRACE')
    def statement(self, p):
        return ('IF_STMT', p.condition, p.statements)

    @_('TORMENTUM LPAREN condition RPAREN LBRACE statements RBRACE')
    def statement(self, p):
        return ('WHILE_STMT', p.condition, p.statements)
    
    @_('REDDITUM expr SEMI')
    def statement(self, p):
        return ('RETURN', p.expr)

    # --- BLOCOS ARDUINO ---
    @_('VAZIUM EXORDIUM LPAREN RPAREN LBRACE statements RBRACE')
    def statement(self, p):
        return ('SETUP_BLOCK', p.statements)

    @_('VAZIUM INFERNA LPAREN RPAREN LBRACE statements RBRACE')
    def statement(self, p):
        return ('LOOP_BLOCK', p.statements)

    # --- FUNÇÕES NATIVAS ---
    # Agora aceitam expressões no lugar do estado, permitindo Ignis/Tenebrae
    @_('HABITUS LPAREN expr COMMA expr RPAREN SEMI')
    def statement(self, p):
        return ('PIN_MODE', p.expr0, p.expr1)

    @_('INCANTARE LPAREN expr COMMA expr RPAREN SEMI')
    def statement(self, p):
        return ('DIGITAL_WRITE', p.expr0, p.expr1)

    @_('MORA LPAREN expr RPAREN SEMI')
    def statement(self, p):
        return ('DELAY', p.expr)
    
    # --- EXPRESSÕES MATEMÁTICAS E CONSTANTES ---
    @_('expr PLUS expr', 'expr MINUS expr', 'expr TIMES expr', 'expr DIVIDE expr')
    def expr(self, p):
        return ('BINOP', p[1], p.expr0, p.expr1)

    @_('ID')
    def expr(self, p):
        return ('VAR', p.ID)

    @_('NUMBER')
    def expr(self, p):
        return ('INT_LIT', p.NUMBER)

    @_('FLOAT_NUM')
    def expr(self, p):
        return ('FLOAT_LIT', p.FLOAT_NUM)
        
    # Nossos novos tokens agora são tratados como valores!
    @_('IGNIS')
    def expr(self, p):
        return ('CONST_STATE', 'HIGH')

    @_('TENEBRAE')
    def expr(self, p):
        return ('CONST_STATE', 'LOW')

    # --- CONDIÇÕES ---
    @_('expr DEQUALS expr', 'expr LT expr', 'expr GT expr')
    def condition(self, p):
        return ('CONDITION', p[1], p.expr0, p.expr1)

    @_('')
    def empty(self, p):
        pass
    
    def error(self, p):
            if p:
                # Pega a palavra que causou o erro
                palavra_errada = str(p.value)
                
                # Tenta achar a palavra reservada mais parecida com o que foi digitado (mínimo de 60% de semelhança)
                sugestoes = difflib.get_close_matches(palavra_errada, ritual_keywords.keys(), n=1, cutoff=0.6)
                
                mensagem = f"Profanação Sintática: Token inesperado '{palavra_errada}'."
                
                # Se achou uma sugestão, adiciona na mensagem!
                if sugestoes:
                    mensagem += f" O ritual exige '{sugestoes[0]}'? (Você quis dizer '{sugestoes[0]}'?)"
                elif palavra_errada in ['{', '}', '(', ')', ';']:
                    mensagem = f"Desequilíbrio de escopo. Símbolo solto: '{palavra_errada}'"
                    
                self.erros_sintaticos.append({
                    "linha": p.lineno,
                    "mensagem": mensagem
                })
                
                # Descarta o token ruim e tenta continuar a compilação (para achar mais de 1 erro por vez)
                self.errok()
            else:
                self.erros_sintaticos.append({
                    "linha": 1, # Fallback
                    "mensagem": "O ritual terminou abruptamente. Faltou fechar uma chave '}' ou ponto e vírgula ';'?"
                })