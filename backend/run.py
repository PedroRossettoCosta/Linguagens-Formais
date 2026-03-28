from flask import Flask, request, jsonify
from flask_cors import CORS
import sys

# Importando as configurações e o motor do compilador
from config import Config
from abyssus.lexer import LDLexer
from abyssus.parser import LDParser
from abyssus.transpiler import LDTranspiler

app = Flask(__name__)
app.config.from_object(Config) # <-- Carregando as configurações aqui!
CORS(app)

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
    print(f"Iniciando o servidor do Compilador Abyssus na porta {app.config['PORT']}...")
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])