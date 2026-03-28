from sly import Parser
from abyssus.lexer import LDLexer

class LDParser(Parser):
    tokens = LDLexer.tokens

    # Precedência Matemática (Hierarquia de operações)
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
    @_('HABITUS LPAREN expr COMMA ID RPAREN SEMI')
    def statement(self, p):
        return ('PIN_MODE', p.expr, p.ID)

    @_('INCANTARE LPAREN expr COMMA ID RPAREN SEMI')
    def statement(self, p):
        return ('DIGITAL_WRITE', p.expr, p.ID)

    @_('MORA LPAREN expr RPAREN SEMI')
    def statement(self, p):
        return ('DELAY', p.expr)
    
    # --- EXPRESSÕES MATEMÁTICAS ---
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

    # --- CONDIÇÕES ---
    @_('expr DEQUALS expr', 'expr LT expr', 'expr GT expr')
    def condition(self, p):
        return ('CONDITION', p[1], p.expr0, p.expr1)

    @_('')
    def empty(self, p):
        pass