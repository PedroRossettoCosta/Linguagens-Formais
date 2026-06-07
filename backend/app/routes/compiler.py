from flask import Blueprint, request, jsonify
from abyssus.lexer import LDLexer
from abyssus.parser import LDParser
from abyssus.transpiler import LDTranspiler
from abyssus.interpreter import LDInterpreter
from abyssus.semantic import LDSemanticAnalyzer


compiler_bp = Blueprint('compiler', __name__)

def ast_to_graph_node(node):
    """Converte recursivamente a AST complexa do compilador em uma estrutura de grafo 
    unificada e simplificada, tornando o backend a única fonte de verdade para a estrutura.
    """
    if node is None:
        return None
    
    if not isinstance(node, (tuple, list)):
        return {
            "type": "LITERAL",
            "label": str(node),
            "children": []
        }
        
    ntype = node[0]
    
    # Tabela de Tipos Místicos do Abyssus
    abyssus_type_map = {
        'Sanguis': 'Sanguis',
        'Sanguis_Fluens': 'Sanguis_Fluens',
        'Veritas': 'Veritas',
        'Vazium': 'Vazium',
        'Verbum': 'Verbum',
        'Aeternum': 'Aeternum',
        'Inscriptio': 'Inscriptio',
        'Littera': 'Littera',
        'Tempus': 'Tempus',
    }
    
    label = ntype
    children = []
    
    if ntype == 'PROGRAM':
        label = 'Ritual'
        children = node[1]
    elif ntype in ('SETUP_BLOCK', 'LOOP_BLOCK'):
        label = 'Exordium()' if ntype == 'SETUP_BLOCK' else 'Inferna()'
        children = node[1]
    elif ntype in ('VAR_DECL', 'VAR_DECL_NOSEMI'):
        tipo = abyssus_type_map.get(node[1], node[1])
        label = f"{tipo}\n{node[2]}"
        if node[3]:
            children = [node[3]]
    elif ntype == 'VAR_DECL_CUSTOM':
        label = f"{node[1]}\n{node[2]}"
        if node[3]:
            children = [node[3]]
    elif ntype == 'CONSTRUCTOR_DECL':
        label = f"{node[1]} {node[2]}"
        children = node[3]
    elif ntype == 'ARRAY_DECL':
        label = f"{node[1]} {node[2]}[{node[3]}]"
    elif ntype in ('ASSIGN', 'ASSIGN_NOSEMI'):
        label = f"{node[1]} ="
        children = [node[2]]
    elif ntype == 'INDEX_ASSIGN':
        label = f"{node[1]}[key] ="
        children = [node[2], node[3]]
    elif ntype == 'IF_STMT':
        label = 'Si'
        children = [node[1]]
        if isinstance(node[2], list):
            children.extend(node[2])
        if node[3]:
            children.append(node[3])
    elif ntype == 'ELSE_BLOCK':
        label = 'Aliter'
        children = node[1]
    elif ntype == 'WHILE_STMT':
        label = 'Tormentum'
        children = [node[1]]
        if isinstance(node[2], list):
            children.extend(node[2])
    elif ntype == 'FOR_STMT':
        label = 'Iterum'
        children = []
        if node[1]: children.append(node[1])
        if node[2]: children.append(node[2])
        if node[3]: children.append(node[3])
        if isinstance(node[4], list):
            children.extend(node[4])
    elif ntype in ('BINOP', 'LOGOP', 'CONDITION'):
        label = f"( {node[1]} )"
        children = [node[2], node[3]]
    elif ntype == 'UNARY':
        label = f"{node[1]}"
        children = [node[2]]
    elif ntype == 'TERNARY':
        label = "?"
        children = [node[1], node[2], node[3]]
    elif ntype == 'INDEX':
        label = "[index]"
        children = [node[1], node[2]]
    elif ntype in ('INT_LIT', 'FLOAT_LIT', 'HEX_LIT'):
        label = str(node[1])
    elif ntype == 'STRING_LIT':
        label = f'"{node[1]}"'
    elif ntype == 'BOOL_LIT':
        label = 'Verum' if node[1] else 'Falsum'
    elif ntype == 'VAR':
        label = node[1]
    elif ntype == 'CONST_STATE':
        label = node[1]
    elif ntype == 'CONST_PIN_MODE':
        label = node[1]
    elif ntype == 'NULLPTR':
        label = 'Nihil'
    elif ntype == 'RETURN':
        label = 'Redditum'
        if node[1]:
            children = [node[1]]
    elif ntype in ('BREAK', 'CONTINUE'):
        label = 'Frangere' if ntype == 'BREAK' else 'Pergere'
    elif ntype == 'FUNC_DEF':
        label = f"{node[1]} {node[2]}"
        children = []
        if isinstance(node[4], list):
            children.extend(node[4])
    elif ntype in ('FUNC_CALL', 'FUNC_CALL_STMT'):
        label = node[1]
        children = node[2]
    elif ntype in ('METHOD_CALL', 'METHOD_CALL_STMT'):
        label = f"{node[1]}.{node[2]}"
        children = node[3]
    elif ntype == 'PIN_MODE':
        label = 'Habitus'
        children = [node[1], node[2]]
    elif ntype == 'DIGITAL_WRITE':
        label = 'Incantare'
        children = [node[1], node[2]]
    elif ntype == 'DIGITAL_READ':
        label = 'Sentire'
        children = [node[1]]
    elif ntype == 'ANALOG_READ':
        label = 'Anima'
        children = [node[1]]
    elif ntype == 'DELAY':
        label = 'Mora'
        children = [node[1]]
    elif ntype == 'MILLIS':
        label = 'Cronos'
    elif ntype == 'PRINT_EMPTY':
        label = 'Revelare'
    elif ntype == 'PRINT':
        label = 'Revelare'
        children = [node[1]]
    elif ntype == 'PRINT_NO_NL':
        label = 'Susurro'
        children = [node[1]]
    elif ntype == 'SERIAL_BEGIN':
        label = 'Vox'
        children = [node[1]]
    elif ntype == 'INCLUDE':
        label = f"Invocare\n{node[1]}"
    elif ntype == 'DEFINE':
        label = f"Decretum\n{node[1]}"
        children = [node[2]]
    elif ntype == 'RAW_CPP':
        label = 'Caos'
    elif ntype == 'TEMPERARE_CRONOS':
        label = 'TemperareCronos'
        children = node[1]
    elif ntype == 'SIGNARE_CAOS':
        label = 'SignareCaos'
        children = node[1]
    elif ntype == 'SACRATUM':
        label = 'Sacratum'
        children = [node[1]]
    elif ntype == 'INANIS':
        label = 'Inanis'
        children = [node[1]]
    elif ntype == 'AEVUM':
        label = 'Aevum'
        children = [node[1]]
    elif ntype == 'VERBUM_AEVUM':
        label = 'VerbumAevum'
        children = [node[1]]
        
    graph_children = []
    for c in children:
        child_node = ast_to_graph_node(c)
        if child_node:
            graph_children.append(child_node)
            
    return {
        "type": ntype,
        "label": label,
        "children": graph_children
    }

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
            
        # 4. Análise Semântica
        semantic_analyzer = LDSemanticAnalyzer()
        erros_semanticos = semantic_analyzer.analyze(ast)
        if len(erros_semanticos) > 0:
            return jsonify({
                "status": "error",
                "erros": [erros_semanticos[0]]
            }), 400
            
        # Se tudo passar, gera C++ e roda simulação
        cpp_output = transpiler.translate(ast)
        logs_execucao = interpreter.execute(ast)
        
        # Gera o grafo da AST pré-estruturado
        graph_ast = ast_to_graph_node(ast)
        
        return jsonify({
            "status": "success",
            "ast": ast,
            "graph_ast": graph_ast,
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
