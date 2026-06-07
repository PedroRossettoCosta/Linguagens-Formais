from sly import Parser
from abyssus.lexer import LDLexer

class LDParser(Parser):
    tokens = LDLexer.tokens

    def __init__(self):
        self.erros_sintaticos = []

    # Precedência: do menos pro mais forte (último item = maior precedência)
    precedence = (
        ('right', QUEST, COLON),               # ternário (mais fraco)
        ('left',  OR),
        ('left',  AND),
        ('left',  DEQUALS, NEQ),
        ('left',  LT, GT, LE, GE),
        ('left',  PLUS, MINUS),
        ('left',  TIMES, DIVIDE, MOD),
        ('right', UMINUS, NOT, UAMP),
        ('left',  DOT, LBRACKET),              # acesso (mais forte)
    )

    # ==========================================================
    # PROGRAMA
    # ==========================================================
    @_('statements')
    def program(self, p):
        return ('PROGRAM', p.statements)

    @_('statement statements')
    def statements(self, p):
        return [p.statement] + p.statements

    @_('empty')
    def statements(self, p):
        return []

    # ==========================================================
    # DIRETIVAS DE PRE-PROCESSADOR / METAPROGRAMACAO
    # ==========================================================
    # Invocare WiFi;  -> #include <WiFi.h>
    @_('INVOCARE ID SEMI')
    def statement(self, p):
        return ('INCLUDE', p.ID)

    # Decretum NOME = valor;  -> #define NOME valor
    @_('DECRETUM ID EQUALS expr SEMI')
    def statement(self, p):
        return ('DEFINE', p.ID, p.expr)

    # Caos "raw c++";  -> trecho literal
    @_('CAOS STRING_LIT SEMI')
    def statement(self, p):
        return ('RAW_CPP', p.STRING_LIT)

    # ==========================================================
    # DECLARAÇÕES DE VARIÁVEIS - tipos primitivos
    # ==========================================================
    @_('INSCRIPTIO ID EQUALS expr SEMI')
    def statement(self, p):
        return ('VAR_DECL', 'Inscriptio', p.ID, p.expr)

    @_('LITTERA ID LBRACKET NUMBER RBRACKET SEMI')
    def statement(self, p):
        return ('ARRAY_DECL', 'Littera', p.ID, p.NUMBER)

    @_('SANGUIS ID EQUALS expr SEMI')
    def statement(self, p):
        return ('VAR_DECL', 'Sanguis', p.ID, p.expr)

    @_('SANGUIS_FLUENS ID EQUALS expr SEMI')
    def statement(self, p):
        return ('VAR_DECL', 'Sanguis_Fluens', p.ID, p.expr)

    @_('VERITAS ID EQUALS expr SEMI')
    def statement(self, p):
        return ('VAR_DECL', 'Veritas', p.ID, p.expr)

    @_('AETERNUM ID EQUALS expr SEMI')
    def statement(self, p):
        return ('VAR_DECL', 'Aeternum', p.ID, p.expr)

    @_('VERBUM ID EQUALS expr SEMI')
    def statement(self, p):
        return ('VAR_DECL', 'Verbum', p.ID, p.expr)

    @_('TEMPUS ID EQUALS expr SEMI')
    def statement(self, p):
        return ('VAR_DECL', 'Tempus', p.ID, p.expr)

    # ----- Versões com modificador const (Imutabile) -----
    @_('IMUTABILE SANGUIS ID EQUALS expr SEMI')
    def statement(self, p):
        return ('VAR_DECL', 'const Sanguis', p.ID, p.expr)

    @_('IMUTABILE SANGUIS_FLUENS ID EQUALS expr SEMI')
    def statement(self, p):
        return ('VAR_DECL', 'const Sanguis_Fluens', p.ID, p.expr)

    @_('IMUTABILE VERITAS ID EQUALS expr SEMI')
    def statement(self, p):
        return ('VAR_DECL', 'const Veritas', p.ID, p.expr)

    @_('IMUTABILE AETERNUM ID EQUALS expr SEMI')
    def statement(self, p):
        return ('VAR_DECL', 'const Aeternum', p.ID, p.expr)

    @_('IMUTABILE VERBUM ID EQUALS expr SEMI')
    def statement(self, p):
        return ('VAR_DECL', 'const Verbum', p.ID, p.expr)

    @_('IMUTABILE TEMPUS ID EQUALS expr SEMI')
    def statement(self, p):
        return ('VAR_DECL', 'const Tempus', p.ID, p.expr)

    # ==========================================================
    # DECLARAÇÕES COM TIPO CUSTOM (qualquer ID como tipo)
    # ==========================================================
    # Tipo nome;            (ex: WiFiClient espClient;)
    @_('ID ID SEMI')
    def statement(self, p):
        return ('VAR_DECL_CUSTOM', p.ID0, p.ID1, None)

    # Tipo nome = valor;
    @_('ID ID EQUALS expr SEMI')
    def statement(self, p):
        return ('VAR_DECL_CUSTOM', p.ID0, p.ID1, p.expr)

    # Tipo nome(args);      (ex: PubSubClient client(espClient);)
    @_('ID ID LPAREN args RPAREN SEMI')
    def statement(self, p):
        return ('CONSTRUCTOR_DECL', p.ID0, p.ID1, p.args)

    # const Tipo nome = valor;
    @_('IMUTABILE ID ID EQUALS expr SEMI')
    def statement(self, p):
        return ('VAR_DECL_CUSTOM', f'const {p.ID0}', p.ID1, p.expr)

    # Tipo nome[N];         (ex: char perfMsg[128];)
    @_('ID ID LBRACKET NUMBER RBRACKET SEMI')
    def statement(self, p):
        return ('ARRAY_DECL', p.ID0, p.ID1, p.NUMBER)

    # nome[chave] = valor;  (ex: perfJson["t"] = t;)
    @_('ID LBRACKET expr RBRACKET EQUALS expr SEMI')
    def statement(self, p):
        return ('INDEX_ASSIGN', p.ID, p.expr0, p.expr1)

    # ==========================================================
    # ATRIBUIÇÃO SIMPLES
    # ==========================================================
    @_('ID EQUALS expr SEMI')
    def statement(self, p):
        return ('ASSIGN', p.ID, p.expr)

    # ==========================================================
    # ESTRUTURAS DE CONTROLE
    # ==========================================================
    # IF / ELSE / ELSE IF (encadeado via else_clause)
    @_('SI LPAREN expr RPAREN LBRACE statements RBRACE else_clause')
    def statement(self, p):
        return ('IF_STMT', p.expr, p.statements, p.else_clause)

    @_('ALITER LBRACE statements RBRACE')
    def else_clause(self, p):
        return ('ELSE_BLOCK', p.statements)

    @_('ALITER SI LPAREN expr RPAREN LBRACE statements RBRACE else_clause')
    def else_clause(self, p):
        return ('IF_STMT', p.expr, p.statements, p.else_clause)

    @_('empty')
    def else_clause(self, p):
        return None

    # WHILE
    @_('TORMENTUM LPAREN expr RPAREN LBRACE statements RBRACE')
    def statement(self, p):
        return ('WHILE_STMT', p.expr, p.statements)

    # FOR clássico (condição agora opcional para suportar for(;;))
    @_('ITERUM LPAREN for_init SEMI for_cond SEMI for_update RPAREN LBRACE statements RBRACE')
    def statement(self, p):
        return ('FOR_STMT', p.for_init, p.for_cond, p.for_update, p.statements)

    @_('SANGUIS ID EQUALS expr')
    def for_init(self, p):
        return ('VAR_DECL_NOSEMI', 'Sanguis', p.ID, p.expr)

    @_('SANGUIS_FLUENS ID EQUALS expr')
    def for_init(self, p):
        return ('VAR_DECL_NOSEMI', 'Sanguis_Fluens', p.ID, p.expr)

    @_('AETERNUM ID EQUALS expr')
    def for_init(self, p):
        return ('VAR_DECL_NOSEMI', 'Aeternum', p.ID, p.expr)

    @_('TEMPUS ID EQUALS expr')
    def for_init(self, p):
        return ('VAR_DECL_NOSEMI', 'Tempus', p.ID, p.expr)

    @_('ID EQUALS expr')
    def for_init(self, p):
        return ('ASSIGN_NOSEMI', p.ID, p.expr)

    @_('empty')
    def for_init(self, p):
        return None

    @_('expr')
    def for_cond(self, p):
        return p.expr

    @_('empty')
    def for_cond(self, p):
        return None

    @_('ID EQUALS expr')
    def for_update(self, p):
        return ('ASSIGN_NOSEMI', p.ID, p.expr)

    @_('empty')
    def for_update(self, p):
        return None

    # BREAK / CONTINUE
    @_('FRANGERE SEMI')
    def statement(self, p):
        return ('BREAK',)

    @_('PERGERE SEMI')
    def statement(self, p):
        return ('CONTINUE',)

    # RETURN (com e sem valor)
    @_('REDDITUM expr SEMI')
    def statement(self, p):
        return ('RETURN', p.expr)

    @_('REDDITUM SEMI')
    def statement(self, p):
        return ('RETURN', None)

    # ==========================================================
    # BLOCOS ARDUINO ESPECIAIS (Exordium / Inferna)
    # ==========================================================
    @_('VAZIUM EXORDIUM LPAREN RPAREN LBRACE statements RBRACE')
    def statement(self, p):
        return ('SETUP_BLOCK', p.statements)

    @_('VAZIUM INFERNA LPAREN RPAREN LBRACE statements RBRACE')
    def statement(self, p):
        return ('LOOP_BLOCK', p.statements)

    # ==========================================================
    # DEFINIÇÃO DE FUNÇÕES CUSTOMIZADAS (retorno primitivo)
    # ==========================================================
    @_('VAZIUM ID LPAREN params RPAREN LBRACE statements RBRACE')
    def statement(self, p):
        return ('FUNC_DEF', 'Vazium', p.ID, p.params, p.statements)

    @_('SANGUIS ID LPAREN params RPAREN LBRACE statements RBRACE')
    def statement(self, p):
        return ('FUNC_DEF', 'Sanguis', p.ID, p.params, p.statements)

    @_('SANGUIS_FLUENS ID LPAREN params RPAREN LBRACE statements RBRACE')
    def statement(self, p):
        return ('FUNC_DEF', 'Sanguis_Fluens', p.ID, p.params, p.statements)

    @_('VERITAS ID LPAREN params RPAREN LBRACE statements RBRACE')
    def statement(self, p):
        return ('FUNC_DEF', 'Veritas', p.ID, p.params, p.statements)

    @_('AETERNUM ID LPAREN params RPAREN LBRACE statements RBRACE')
    def statement(self, p):
        return ('FUNC_DEF', 'Aeternum', p.ID, p.params, p.statements)

    @_('VERBUM ID LPAREN params RPAREN LBRACE statements RBRACE')
    def statement(self, p):
        return ('FUNC_DEF', 'Verbum', p.ID, p.params, p.statements)

    @_('TEMPUS ID LPAREN params RPAREN LBRACE statements RBRACE')
    def statement(self, p):
        return ('FUNC_DEF', 'Tempus', p.ID, p.params, p.statements)

    @_('param_list')
    def params(self, p):
        return p.param_list

    @_('empty')
    def params(self, p):
        return []

    @_('param')
    def param_list(self, p):
        return [p.param]

    @_('param_list COMMA param')
    def param_list(self, p):
        return p.param_list + [p.param]

    @_('SANGUIS ID')
    def param(self, p):
        return ('Sanguis', p.ID)

    @_('SANGUIS_FLUENS ID')
    def param(self, p):
        return ('Sanguis_Fluens', p.ID)

    @_('VERITAS ID')
    def param(self, p):
        return ('Veritas', p.ID)

    @_('AETERNUM ID')
    def param(self, p):
        return ('Aeternum', p.ID)

    @_('VERBUM ID')
    def param(self, p):
        return ('Verbum', p.ID)

    @_('TEMPUS ID')
    def param(self, p):
        return ('Tempus', p.ID)

    # ==========================================================
    # FUNÇÕES NATIVAS (statements)
    # ==========================================================
    @_('HABITUS LPAREN expr COMMA expr RPAREN SEMI')
    def statement(self, p):
        return ('PIN_MODE', p.expr0, p.expr1)

    @_('INCANTARE LPAREN expr COMMA expr RPAREN SEMI')
    def statement(self, p):
        return ('DIGITAL_WRITE', p.expr0, p.expr1)

    @_('MORA LPAREN expr RPAREN SEMI')
    def statement(self, p):
        return ('DELAY', p.expr)

    @_('REVELARE LPAREN RPAREN SEMI')
    def statement(self, p):
        return ('PRINT_EMPTY',)

    @_('REVELARE LPAREN expr RPAREN SEMI')
    def statement(self, p):
        return ('PRINT', p.expr)

    @_('SUSURRO LPAREN expr RPAREN SEMI')
    def statement(self, p):
        return ('PRINT_NO_NL', p.expr)

    @_('VOX LPAREN expr RPAREN SEMI')
    def statement(self, p):
        return ('SERIAL_BEGIN', p.expr)

    # ==========================================================
    # CHAMADA DE FUNÇÃO / MÉTODO COMO STATEMENT
    # ==========================================================
    @_('ID LPAREN args RPAREN SEMI')
    def statement(self, p):
        return ('FUNC_CALL_STMT', p.ID, p.args)

    @_('ID DOT ID LPAREN args RPAREN SEMI')
    def statement(self, p):
        return ('METHOD_CALL_STMT', p.ID0, p.ID1, p.args)

    @_('arg_list')
    def args(self, p):
        return p.arg_list

    @_('empty')
    def args(self, p):
        return []

    @_('expr')
    def arg_list(self, p):
        return [p.expr]

    @_('arg_list COMMA expr')
    def arg_list(self, p):
        return p.arg_list + [p.expr]

    # ==========================================================
    # EXPRESSÕES
    # ==========================================================
    # Aritméticas
    @_('expr PLUS expr',
       'expr MINUS expr',
       'expr TIMES expr',
       'expr DIVIDE expr',
       'expr MOD expr')
    def expr(self, p):
        return ('BINOP', p[1], p.expr0, p.expr1)

    # Lógicas binárias
    @_('expr AND expr')
    def expr(self, p):
        return ('LOGOP', '&&', p.expr0, p.expr1)

    @_('expr OR expr')
    def expr(self, p):
        return ('LOGOP', '||', p.expr0, p.expr1)

    # Lógica unária / negação aritmética / address-of
    @_('NOT expr')
    def expr(self, p):
        return ('UNARY', '!', p.expr)

    @_('MINUS expr %prec UMINUS')
    def expr(self, p):
        return ('UNARY', '-', p.expr)

    @_('AMP expr %prec UAMP')
    def expr(self, p):
        return ('UNARY', '&', p.expr)

    # Comparações
    @_('expr DEQUALS expr',
       'expr NEQ expr',
       'expr LT expr',
       'expr GT expr',
       'expr LE expr',
       'expr GE expr')
    def expr(self, p):
        return ('CONDITION', p[1], p.expr0, p.expr1)

    # Ternário
    @_('expr QUEST expr COLON expr')
    def expr(self, p):
        return ('TERNARY', p.expr0, p.expr1, p.expr2)

    # Indexação como rvalue
    @_('expr LBRACKET expr RBRACKET')
    def expr(self, p):
        return ('INDEX', p.expr0, p.expr1)

    # Parênteses para agrupar
    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return p.expr

    # --- Átomos ---
    @_('ID')
    def expr(self, p):
        return ('VAR', p.ID)

    @_('NUMBER')
    def expr(self, p):
        return ('INT_LIT', p.NUMBER)

    @_('FLOAT_NUM')
    def expr(self, p):
        return ('FLOAT_LIT', p.FLOAT_NUM)

    @_('STRING_LIT')
    def expr(self, p):
        return ('STRING_LIT', p.STRING_LIT)

    @_('VERUM')
    def expr(self, p):
        return ('BOOL_LIT', True)

    @_('FALSUM')
    def expr(self, p):
        return ('BOOL_LIT', False)

    @_('HEX_NUM')
    def expr(self, p):
        return ('HEX_LIT', p.HEX_NUM)

    @_('NIHIL')
    def expr(self, p):
        return ('NULLPTR',)

    @_('IGNIS')
    def expr(self, p):
        return ('CONST_STATE', 'Ignis')

    @_('TENEBRAE')
    def expr(self, p):
        return ('CONST_STATE', 'Tenebrae')

    @_('ENTRADA')
    def expr(self, p):
        return ('CONST_PIN_MODE', 'Entrada')

    @_('SAIDA')
    def expr(self, p):
        return ('CONST_PIN_MODE', 'Saida')

    # Predefined mistic constants
    @_('NEXUS_FIDELIS')
    def expr(self, p):
        return ('CONST_STATE', 'NexusFidelis')

    @_('ALBUS')
    def expr(self, p):
        return ('CONST_STATE', 'Albus')

    @_('SSD1306_TENSA')
    def expr(self, p):
        return ('CONST_STATE', 'SSD1306_Tensa')

    # --- Chamadas como expressão ---
    @_('VERBUM LPAREN args RPAREN')
    def expr(self, p):
        return ('FUNC_CALL', 'Verbum', p.args)

    @_('TEMPERARE_CRONOS LPAREN args RPAREN SEMI')
    def statement(self, p):
        return ('TEMPERARE_CRONOS', p.args)

    @_('SIGNARE_CAOS LPAREN args RPAREN SEMI')
    def statement(self, p):
        return ('SIGNARE_CAOS', p.args)

    @_('SACRATUM LPAREN expr RPAREN')
    def expr(self, p):
        return ('SACRATUM', p.expr)

    @_('INANIS LPAREN expr RPAREN')
    def expr(self, p):
        return ('INANIS', p.expr)

    @_('AEVUM LPAREN expr RPAREN')
    def expr(self, p):
        return ('AEVUM', p.expr)

    @_('VERBUM_AEVUM LPAREN expr RPAREN')
    def expr(self, p):
        return ('VERBUM_AEVUM', p.expr)

    @_('ID LPAREN args RPAREN')
    def expr(self, p):
        return ('FUNC_CALL', p.ID, p.args)

    @_('ID DOT ID LPAREN args RPAREN')
    def expr(self, p):
        return ('METHOD_CALL', p.ID0, p.ID1, p.args)

    # Nativas que retornam valor
    @_('SENTIRE LPAREN expr RPAREN')
    def expr(self, p):
        return ('DIGITAL_READ', p.expr)

    @_('ANIMA LPAREN expr RPAREN')
    def expr(self, p):
        return ('ANALOG_READ', p.expr)

    @_('CRONOS LPAREN RPAREN')
    def expr(self, p):
        return ('MILLIS',)

    @_('')
    def empty(self, p):
        pass

    # ==========================================================
    # TRATAMENTO DE ERROS
    # ==========================================================
    def error(self, p):
        if p:
            mensagem = f"Desequilíbrio Estrutural: O token '{p.value}' causou uma falha na gramática do ritual nesta posição."
            if p.value in ['{', '}', '(', ')', ';']:
                mensagem = f"Escopo corrompido. Verifique a ordem ou a falta de '{p.value}' e pontos e vírgulas."

            self.erros_sintaticos.append({
                "linha": p.lineno,
                "mensagem": mensagem
            })
            self.errok()
        else:
            self.erros_sintaticos.append({
                "linha": 1,
                "mensagem": "O ritual terminou de forma abrupta. Faltou fechar alguma chave '}'?"
            })
