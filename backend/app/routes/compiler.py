from flask import Blueprint, request, jsonify
from abyssus.lexer import LDLexer
from abyssus.parser import LDParser
from abyssus.transpiler import LDTranspiler
from abyssus.interpreter import LDInterpreter

compiler_bp = Blueprint('compiler', __name__)

@compiler_bp.route('/compile', methods=['POST'])
def compile_ritual():
    data = request.json or {}
    code = data.get('code', '')
    
    lexer = LDLexer()
    parser = LDParser()
    transpiler = LDTranspiler()
    interpreter = LDInterpreter()
    
    try:
        # 1. Análise Léxica
        tokens = list(lexer.tokenize(code))
        
        # Filtro de Erro Léxico
        if len(lexer.erros_lexicos) > 0:
            return jsonify({
                "status": "error",
                "erros": [lexer.erros_lexicos[0]]
            }), 400
            
        # 2. Análise Sintática
        ast = parser.parse(iter(tokens))
        
        # Filtro de Erro Sintático
        if len(parser.erros_sintaticos) > 0:
            erro_principal = parser.erros_sintaticos[0]
            if "Token(" in erro_principal["mensagem"]:
                erro_principal["mensagem"] = "Desequilíbrio Estrutural: A ordem dos símbolos ou comandos não faz sentido neste ritual."
                
            return jsonify({
                "status": "error",
                "erros": [erro_principal]
            }), 400
            
        # 3. Validação de pergaminho vazio
        if not ast:
            return jsonify({
                "status": "error", 
                "erros": [{
                    "linha": 1, 
                    "mensagem": "O pergaminho está vazio. Escreva um ritual válido."
                }]
            }), 400
            
        # Se tudo passar, gera C++ e roda simulação
        cpp_output = transpiler.translate(ast)
        logs_execucao = interpreter.execute(ast)
        
        return jsonify({
            "status": "success",
            "ast": ast,
            "cpp": cpp_output,
            "tokens": [{"tipo": t.type, "valor": str(t.value), "linha": t.lineno} for t in tokens],
            "logs": logs_execucao
        })
    except Exception as e:
        # Fallback de segurança do servidor em caso de erros não mapeados
        return jsonify({
            "status": "error", 
            "erros": [{
                "linha": 1, 
                "mensagem": f"Falha catastrófica no motor: {str(e)}"
            }]
        }), 500
