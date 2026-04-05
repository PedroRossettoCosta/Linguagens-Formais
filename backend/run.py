from flask import Flask, request, jsonify
from flask_cors import CORS

from abyssus.interpreter import LDInterpreter
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
            # Roda as análises
            tokens = list(lexer.tokenize(code))
            ast = parser.parse(iter(tokens))
            
            # === O FILTRO ANTI-CASCATA ===
            # 1. Prioridade Máxima: Erros Léxicos (Palavras digitadas erradas)
            # Se houver erro léxico, a culpa é dele. Devolvemos SÓ o primeiro erro e paramos.
            if len(lexer.erros_lexicos) > 0:
                return jsonify({
                    "status": "error",
                    "erros": [lexer.erros_lexicos[0]] # Pega apenas a primeira heresia
                }), 400
                
            # 2. Prioridade Secundária: Erros Sintáticos (Estrutura quebrada)
            # Só olhamos para a sintaxe se todas as palavras existirem no nosso latim
            if len(parser.erros_sintaticos) > 0:
                # Pega o primeiro erro sintático e limpa a mensagem caso venha um objeto sujo do SLY
                erro_principal = parser.erros_sintaticos[0]
                if "Token(" in erro_principal["mensagem"]:
                    erro_principal["mensagem"] = "Desequilíbrio Estrutural: A ordem dos símbolos ou comandos não faz sentido neste ritual."
                    
                return jsonify({
                    "status": "error",
                    "erros": [erro_principal]
                }), 400
                
            # 3. Se a AST estiver vazia (usuário apagou todo o código)
            if not ast:
                return jsonify({"status": "error", "erros": [{"linha": 1, "mensagem": "O pergaminho está vazio. Escreva um ritual válido."}]}), 400
                
            # Se tudo estiver perfeito, gera o C++
            cpp_output = transpiler.translate(ast)
            
            interpretador = LDInterpreter()
            logs_execucao = interpretador.execute(ast)
            
            return jsonify({
                "status": "success",
                "ast": ast,
                "cpp": cpp_output,
                "tokens": [{"tipo": t.type, "valor": str(t.value), "linha": t.lineno} for t in tokens],
                "logs": logs_execucao # <--- Enviando para o Frontend
            })
    except Exception as e:
        # Fallback de segurança do servidor
        return jsonify({"status": "error", "erros": [{"linha": 1, "mensagem": f"Falha catastrófica no motor: {str(e)}"}]}), 400

if __name__ == '__main__':
    print(f"Iniciando o servidor do Compilador Abyssus na porta {app.config['PORT']}...")
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])