from flask import Flask, request, jsonify
from flask_cors import CORS
from sly import Lexer, Parser
import sys

app = Flask(__name__)
CORS(app)

# ==========================================================
# ANALISADOR LÉXICO (SCANNER) - Definição dos Tokens
# ==========================================================
class LDLexer(Lexer):
    tokens = { ID, NUMBER, FLOAT_NUM, SANGUIS, SANGUIS_FLUENS, VAZIUM, 
               EXORDIUM, INFERNA, HABITUS, INCANTARE, MORA, IGNIS, TENEBRAE, 
               SI, TORMENTUM, PLUS, MINUS, TIMES, DIVIDE, EQUALS, DEQUALS,
               LPAREN, RPAREN, LBRACE, RBRACE, SEMI, COMMA, LT, GT }
    
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

    # Números (RegEx para Float e Int)
    FLOAT_NUM = r'\d+\.\d+'
    NUMBER    = r'\d+'
    
    # Identificadores e Palavras-chave
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['Sanguis']        = SANGUIS   # int
    ID['Sanguis_Fluens'] = SANGUIS_FLUENS # float
    ID['Vazium']         = VAZIUM    # void
    ID['Exordium']       = EXORDIUM  # setup
    ID['Inferna']        = INFERNA   # loop
    ID['Habitus']        = HABITUS   # pinMode
    ID['Incantare']      = INCANTARE # digitalWrite
    ID['Mora']           = MORA      # delay
    ID['Ignis']          = IGNIS     # HIGH
    ID['Tenebrae']       = TENEBRAE  # LOW
    ID['Si']             = SI        # if
    ID['Tormentum']      = TORMENTUM # while

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

# ==========================================================
# ANALISADOR SINTÁTICO (PARSER) - Geração da AST
# ==========================================================
class LDParser(Parser):
    tokens = LDLexer.tokens

    # Precedência Matemática (Hierarquia de operações)
    precedence = (
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE),
    )

    @_('program statements')
    def program(self, p):
        return ('PROGRAM', p.statements)

    @_('statement statements')
    def statements(self, p):
        return [p.statement] + p.statements

    @_('empty')
    def statements(self, p):
        return []

    # Regras de Gramática Demoníaca

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

# ==========================================================
# BACK-END: GERADOR DE C++ (TRANSPILER)
# ==========================================================
class LDTranspiler:
    def translate(self, ast):
        cpp_code = "#include <Arduino.h>\n\n"
        for node in ast[1]:
            cpp_code += self.visit(node)
        return cpp_code

    def visit(self, node):
        ntype = node[0]
        if ntype == 'VAR_DECL':
            return f"{node[1]} {node[2]} = {self.visit(node[3])};\n"
        elif ntype == 'ASSIGN':
            return f"{node[1]} = {self.visit(node[2])};\n"
        elif ntype == 'BINOP':
            return f"({self.visit(node[2])} {node[1]} {self.visit(node[3])})"
        elif ntype == 'INT_LIT' or ntype == 'FLOAT_LIT':
            return str(node[1])
        elif ntype == 'VAR':
            return node[1]
        elif ntype == 'CONDITION':
            return f"{self.visit(node[2])} {node[1]} {self.visit(node[3])}"
        elif ntype == 'IF_STMT':
            inner = "".join(["    " + self.visit(s) for s in node[2]])
            return f"if ({self.visit(node[1])}) {{\n{inner}}}\n"
        elif ntype == 'WHILE_STMT':
            inner = "".join(["    " + self.visit(s) for s in node[2]])
            return f"while ({self.visit(node[1])}) {{\n{inner}}}\n"
        elif ntype == 'SETUP_BLOCK':
            inner = "".join(["    " + self.visit(s) for s in node[1]])
            return f"void setup() {{\n{inner}}}\n\n"
        elif ntype == 'LOOP_BLOCK':
            inner = "".join(["    " + self.visit(s) for s in node[1]])
            return f"void loop() {{\n{inner}}}\n\n"
        elif ntype == 'PIN_MODE':
            return f"pinMode({self.visit(node[1])}, OUTPUT);\n"
        elif ntype == 'DIGITAL_WRITE':
            return f"digitalWrite({self.visit(node[1])}, {node[2]});\n"
        elif ntype == 'DELAY':
            return f"delay({self.visit(node[2])});\n"
        return ""

# ==========================================================
# API ENDPOINT
# ==========================================================
@app.route('/compile', methods=['POST'])
def compile_ritual():
    data = request.json
    code = data.get('code', '')
    
    lexer = LDLexer()
    parser = LDParser()
    transpiler = LDTranspiler()
    
    try:
        tokens = list(lexer.tokenize(code))
        ast = parser.parse(iter(tokens))
        
        if not ast:
            return jsonify({"error": "O ritual está sintaticamente incompleto."}), 400
            
        cpp_output = transpiler.translate(ast)
        
        return jsonify({
            "status": "success",
            "ast": ast,
            "cpp": cpp_output,
            "tokens": [str(t) for t in tokens]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)