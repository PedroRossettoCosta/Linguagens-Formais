class LDSemanticAnalyzer:
    def __init__(self):
        self.erros_semanticos = []
        # O escopo global inicial começa puramente com as definições de hardware místicas do Abyssus
        self.scopes = [{
            'Ignis': 'Sanguis',
            'Tenebrae': 'Sanguis',
            'Entrada': 'Sanguis',
            'Saida': 'Sanguis',
            'NexusFidelis': 'Sanguis',
            'Albus': 'Sanguis',
            'SSD1306_Tensa': 'Sanguis',
            'DHT11': 'Sanguis',
            'DHT22': 'Sanguis',
            'Nihil': 'any',
        }]  # Pilha de escopos para tabela de símbolos
        self.functions = {}  # Tabela global de funções customizadas
        self.current_function = None  # Nome da função atual sob inspeção

        # O Grimório de hardware nativo oficial da linguagem Abyssus (Pure Domain)
        self.native_functions = {
            'Habitus': ('Vazium', ['Sanguis', 'Sanguis']),
            'Incantare': ('Vazium', ['Sanguis', 'Sanguis']),
            'Sentire': ('Sanguis', ['Sanguis']),
            'Anima': ('Sanguis', ['Sanguis']),
            'Mora': ('Vazium', ['Sanguis']),
            'Cronos': ('Aeternum', []),
            'Vox': ('Vazium', ['Sanguis']),
            'Revelare': ('Vazium', ['any']),
            'Susurro': ('Vazium', ['any']),
            'Verbum': ('Verbum', ['any']), # Conversor de tipo místico (Verbum)
            
            # Novos rituais nativos puros de hardware do Abyssus
            'TemperareCronos': ('Vazium', ['Sanguis', 'Sanguis', 'Inscriptio', 'Inscriptio']),
            'Aevum': ('Aeternum', ['any']),
            'VerbumAevum': ('Verbum', ['any']),
            'SignareCaos': ('Vazium', ['any', 'any']),
            'Inanis': ('Veritas', ['any']),
            'Sacratum': ('Verbum', ['Verbum']),
        }

    def error(self, line, msg, sug=None):
        """Registra um erro semântico formatado."""
        self.erros_semanticos.append({
            "linha": line if line is not None else 1,
            "mensagem": f"Erro Semântico: {msg}",
            "sugestao": sug
        })

    def declare_var(self, name, var_type, line):
        """Insere uma variável na tabela de símbolos do escopo atual."""
        current_scope = self.scopes[-1]
        if name in current_scope:
            self.error(
                line,
                f"Selo Duplicado: A variável '{name}' já foi consagrada anteriormente neste mesmo escopo.",
                f"Declare a variável com outro nome ou remova a redeclaração."
            )
        else:
            current_scope[name] = var_type

    def lookup_var(self, name):
        """Busca o tipo de uma variável na pilha de escopos (do mais interno pro externo)."""
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None

    def push_scope(self):
        self.scopes.append({})

    def pop_scope(self):
        if len(self.scopes) > 1:
            self.scopes.pop()

    def analyze(self, ast):
        """Inicia a análise semântica sobre a AST gerada."""
        self.erros_semanticos = []
        self.scopes = [{
            'Ignis': 'Sanguis',
            'Tenebrae': 'Sanguis',
            'Entrada': 'Sanguis',
            'Saida': 'Sanguis',
            'NexusFidelis': 'Sanguis',
            'Albus': 'Sanguis',
            'SSD1306_Tensa': 'Sanguis',
            'DHT11': 'Sanguis',
            'DHT22': 'Sanguis',
            'Nihil': 'any',
        }]
        self.current_function = None

        if not ast or ast[0] != 'PROGRAM':
            return self.erros_semanticos

        # 1ª Passada: Registrar assinaturas das funções customizadas globais
        for node in ast[1]:
            if node and node[0] == 'FUNC_DEF':
                ret_type, name, params, _ = node[1], node[2], node[3], node[4]
                if name in self.functions:
                    self.error(
                        node.lineno if hasattr(node, 'lineno') else 1,
                        f"Invocação Conflituosa: A função '{name}' já possui um ritual registrado com este mesmo nome.",
                        "Evite duplicidade criando um nome alternativo para esta nova função."
                    )
                else:
                    # Salva (tipo_retorno, [lista_de_tipos_dos_params])
                    param_types = [p[0] for p in params]
                    self.functions[name] = (ret_type, param_types)

        # 2ª Passada: Análise detalhada de escopos e tipos
        for node in ast[1]:
            self.visit(node)

        return self.erros_semanticos

    def visit(self, node):
        if node is None:
            return 'Vazium'
        
        ntype = node[0]

        # ---------- Pré-processador / Metaprogramação ----------
        if ntype == 'DEFINE':
            name, expr_node = node[1], node[2]
            expr_type = self.visit(expr_node)
            self.declare_var(name, expr_type, 1)
            return 'Vazium'
        elif ntype == 'INCLUDE':
            lib_name = node[1]
            self.declare_var(lib_name, 'Library', 1)
            return 'Vazium'
        elif ntype == 'RAW_CPP':
            import re
            cpp_code = node[1]
            matches = re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*(?:;|=|\()', cpp_code)
            if matches:
                self.declare_var(matches[-1], 'any', 1)
            return 'Vazium'

        # ---------- Declarações de variáveis ----------
        if ntype in ('VAR_DECL', 'VAR_DECL_NOSEMI'):
            # ('VAR_DECL', tipo, nome, expr)
            var_type, name, expr_node = node[1], node[2], node[3]
            expr_type = self.visit(expr_node)
            self.declare_var(name, var_type, 1)

            # Validação simples de tipo
            if var_type.startswith('const '):
                clean_type = var_type[6:]
            else:
                clean_type = var_type

            # Evitar string atribuída para int/float diretamente
            if clean_type in ('Sanguis', 'Sanguis_Fluens', 'Aeternum') and expr_type == 'Verbum':
                self.error(
                    1,
                    f"Atribuição Profana: O receptáculo '{name}' (tipo {clean_type}) não pode receber uma oferenda de Texto (Verbum).",
                    "Converta o Texto ou altere o tipo do receptáculo."
                )
            return 'Vazium'

        elif ntype == 'VAR_DECL_CUSTOM':
            # ('VAR_DECL_CUSTOM', tipo, nome, expr)
            var_type, name, expr_node = node[1], node[2], node[3]
            if expr_node:
                self.visit(expr_node)
            self.declare_var(name, var_type, 1)
            return 'Vazium'

        elif ntype == 'CONSTRUCTOR_DECL':
            # ('CONSTRUCTOR_DECL', tipo, nome, args)
            var_type, name, args = node[1], node[2], node[3]
            for a in args:
                self.visit(a)
            self.declare_var(name, var_type, 1)
            return 'Vazium'

        elif ntype == 'ARRAY_DECL':
            # ('ARRAY_DECL', tipo, nome, size)
            var_type, name, size = node[1], node[2], node[3]
            self.declare_var(name, f"{var_type}[]", 1)
            return 'Vazium'

        # ---------- Atribuições ----------
        elif ntype in ('ASSIGN', 'ASSIGN_NOSEMI'):
            name, expr_node = node[1], node[2]
            expr_type = self.visit(expr_node)
            var_type = self.lookup_var(name)

            if var_type is None:
                self.error(
                    1,
                    f"Altar Desconhecido: A variável '{name}' está sendo alterada sem ter sido consagrada (declarada) anteriormente.",
                    f"Declare '{name}' usando Sanguis, Sanguis_Fluens, Veritas ou Verbum antes de atribuir valores."
                )
            else:
                # Verificar se está alterando uma constante
                if var_type.startswith('const ') or 'Imutabile' in var_type:
                    self.error(
                        1,
                        f"Decreto Imutável: A variável '{name}' foi selada como constante (Imutabile) e não pode ser reatribuída.",
                        "Remova a atribuição ou declare a variável sem o modificador 'Imutabile'."
                    )
                # Tipo estrito: int/float recebendo String
                elif var_type in ('Sanguis', 'Sanguis_Fluens', 'Aeternum') and expr_type == 'Verbum':
                    self.error(
                        1,
                        f"Atribuição Profana: O receptáculo '{name}' (tipo {var_type}) não suporta recebimento de texto diretamente.",
                        "Converta ou adeque a expressão para corresponder aos tipos."
                    )
            return 'Vazium'

        elif ntype == 'INDEX_ASSIGN':
            # nome[chave] = valor
            name, key_expr, val_expr = node[1], node[2], node[3]
            self.visit(key_expr)
            self.visit(val_expr)
            if self.lookup_var(name) is None:
                self.error(
                    1,
                    f"Altar Desconhecido: O arranjo '{name}' não foi declarado."
                )
            return 'Vazium'

        # ---------- Operadores (Expressões) ----------
        elif ntype == 'BINOP':
            op, esq_node, dir_node = node[1], node[2], node[3]
            esq_type = self.visit(esq_node)
            dir_type = self.visit(dir_node)

            # Filtro Anti Heresia: Divisão por Zero estática
            if op in ('/', '%') and dir_node and dir_node[0] == 'INT_LIT' and dir_node[1] == 0:
                self.error(
                    1,
                    "Heresia Matemática: Tentativa de realizar uma divisão por zero (0) em um ritual místico.",
                    "Altere o divisor para um número diferente de zero para manter a ordem do universo."
                )

            # Operações aritméticas em Strings (exceto concatenação)
            if op != '+' and (esq_type == 'Verbum' or dir_type == 'Verbum'):
                self.error(
                    1,
                    f"Heresia Aritmética: O operador '{op}' não faz sentido sobre oferendas do tipo Texto (Verbum).",
                    "Textos (Verbum) apenas aceitam concatenação através do operador '+'."
                )

            if esq_type == 'Verbum' or dir_type == 'Verbum':
                return 'Verbum'
            if esq_type == 'Sanguis_Fluens' or dir_type == 'Sanguis_Fluens':
                return 'Sanguis_Fluens'
            return 'Sanguis'

        elif ntype == 'LOGOP':
            self.visit(node[2])
            self.visit(node[3])
            return 'Veritas'

        elif ntype == 'UNARY':
            op, sub_expr = node[1], node[2]
            sub_type = self.visit(sub_expr)
            if op == '!' and sub_type == 'Verbum':
                self.error(1, "Heresia Lógica: Negação lógica '!' aplicada incorretamente sobre Texto (Verbum).")
            return sub_type

        elif ntype == 'CONDITION':
            op, esq, dir = node[1], node[2], node[3]
            self.visit(esq)
            self.visit(dir)
            return 'Veritas'

        elif ntype == 'TERNARY':
            self.visit(node[1])
            t_type = self.visit(node[2])
            self.visit(node[3])
            return t_type

        elif ntype == 'INDEX':
            self.visit(node[1])
            self.visit(node[2])
            return 'any'

        # ---------- Literais e Átomos ----------
        elif ntype == 'INT_LIT':
            return 'Sanguis'
        elif ntype == 'FLOAT_LIT':
            return 'Sanguis_Fluens'
        elif ntype == 'STRING_LIT':
            return 'Verbum'
        elif ntype == 'BOOL_LIT':
            return 'Veritas'
        elif ntype == 'HEX_LIT':
            return 'Sanguis'
        elif ntype == 'CONST_STATE':
            return 'Sanguis'
        elif ntype == 'CONST_PIN_MODE':
            return 'Sanguis'
        elif ntype == 'VAR':
            name = node[1]
            var_type = self.lookup_var(name)
            if var_type is None:
                # Regra Semântica Abyssus: Identificadores totalmente em maiúsculas
                # são tratados como decretos/macros externos implícitos herdados de bibliotecas invocadas.
                if name.isupper() and len(name) >= 2:
                    return 'Sanguis'
                
                self.error(
                    1,
                    f"Espírito Errante: A variável '{name}' está sendo invocada em uma expressão sem ter sido consagrada.",
                    f"Declare '{name}' no início do seu ritual."
                )
                return 'any'
            return var_type
        
        elif ntype == 'NULLPTR':
            return 'any'

        # ---------- Estruturas de controle ----------
        elif ntype == 'IF_STMT':
            # cond, block, else_clause
            self.visit(node[1])
            self.push_scope()
            for s in node[2]:
                self.visit(s)
            self.pop_scope()
            if node[3]:
                self.visit(node[3])
            return 'Vazium'

        elif ntype == 'ELSE_BLOCK':
            self.push_scope()
            for s in node[1]:
                self.visit(s)
            self.pop_scope()
            return 'Vazium'

        elif ntype == 'WHILE_STMT':
            self.visit(node[1])
            self.push_scope()
            for s in node[2]:
                self.visit(s)
            self.pop_scope()
            return 'Vazium'

        elif ntype == 'FOR_STMT':
            # init, cond, update, block
            self.push_scope()  # Variável de controle pertence ao escopo interno do FOR
            if node[1]:
                self.visit(node[1])
            if node[2]:
                self.visit(node[2])
            if node[3]:
                self.visit(node[3])
            for s in node[4]:
                self.visit(s)
            self.pop_scope()
            return 'Vazium'

        elif ntype in ('BREAK', 'CONTINUE'):
            return 'Vazium'

        # ---------- Retornos ----------
        elif ntype == 'RETURN':
            # return expr
            expr_node = node[1]
            ret_type = self.visit(expr_node) if expr_node else 'Vazium'

            if self.current_function:
                expected_type = self.functions.get(self.current_function, ('Vazium', []))[0]
                if expected_type != ret_type and ret_type != 'any':
                    self.error(
                        1,
                        f"Retorno Profano: O ritual '{self.current_function}' deveria retornar oferendas do tipo {expected_type}, mas está retornando {ret_type}.",
                        f"Adequar o comando Redditum para retornar um valor compatível com {expected_type}."
                    )
            else:
                # Fora de função customizada (ex: em Exordium ou Inferna)
                if ret_type != 'Vazium':
                    self.error(
                        1,
                        "Heresia Estrutural: Retorno de expressão ('Redditum valor') detectado fora de um ritual customizado.",
                        "Os blocos padrões Exordium() e Inferna() não aceitam devoluções de valores."
                    )
            return 'Vazium'

        # ---------- Blocos Arduino ----------
        elif ntype in ('SETUP_BLOCK', 'LOOP_BLOCK'):
            self.push_scope()
            for s in node[1]:
                self.visit(s)
            self.pop_scope()
            return 'Vazium'

        # ---------- Funções customizadas ----------
        elif ntype == 'FUNC_DEF':
            # ('FUNC_DEF', ret_type, name, params, block)
            ret_type, name, params, block = node[1], node[2], node[3], node[4]
            self.current_function = name
            
            self.push_scope()
            for ptype, pname in params:
                self.declare_var(pname, ptype, 1)

            for s in block:
                self.visit(s)

            self.pop_scope()
            self.current_function = None
            return 'Vazium'

        elif ntype in ('FUNC_CALL', 'FUNC_CALL_STMT'):
            name, args = node[1], node[2]
            
            # 1. É nativa oficial do Abyssus (Pure Domain)?
            if name in self.native_functions:
                expected_ret, param_types = self.native_functions[name]
                if param_types != ['any']:
                    if len(param_types) != len(args):
                        self.error(
                            1,
                            f"Invocação Profana: A função sagrada '{name}' requer exatamente {len(param_types)} argumento(s), mas recebeu {len(args)}.",
                            f"Consulte o grimório do compilador. Assinatura de '{name}': {', '.join(param_types)}"
                        )
                # Visita argumentos
                for a in args:
                    self.visit(a)
                return expected_ret

            # 2. É um objeto consagrado via Invocare?
            elif self.lookup_var(name) is not None:
                for a in args:
                    self.visit(a)
                return 'any'

            # 3. É customizada pelo usuário no ritual?
            elif name in self.functions:
                expected_ret, param_types = self.functions[name]
                if len(param_types) != len(args):
                    self.error(
                        1,
                        f"Invocação Profana: O ritual customizado '{name}' requer {len(param_types)} argumento(s), mas recebeu {len(args)}.",
                        f"Envie a quantidade exata de argumentos consagrados na definição do ritual."
                    )
                for a in args:
                    self.visit(a)
                return expected_ret
            
            else:
                self.error(
                    1,
                    f"Invocação Fantasma: O ritual ou função '{name}' está sendo chamado mas nunca foi conjurado (declarado).",
                    "Verifique a grafia ou crie a função mística correspondente."
                )
                for a in args:
                    self.visit(a)
                return 'any'

        elif ntype in ('METHOD_CALL', 'METHOD_CALL_STMT'):
            # obj.metodo(args)
            obj, method, args = node[1], node[2], node[3]
            for a in args:
                self.visit(a)
            if self.lookup_var(obj) is None:
                self.error(
                    1,
                    f"Convocação Cega: Tentativa de invocar '{method}' em um construtor ou objeto '{obj}' que não foi consagrado.",
                    f"Declare '{obj}' no topo antes de conjurar seus métodos."
                )
            return 'any'

        # ---------- Novos rituais nativos puros de hardware ----------
        elif ntype == 'TEMPERARE_CRONOS':
            for a in node[1]:
                self.visit(a)
            return 'Vazium'
        elif ntype == 'SIGNARE_CAOS':
            for a in node[1]:
                self.visit(a)
            return 'Vazium'
        elif ntype == 'SACRATUM':
            sub_type = self.visit(node[1])
            if sub_type != 'Verbum':
                self.error(1, "Heresia de Consagração: Sacratum requer uma oferenda de Texto (Verbum).")
            return 'Verbum'
        elif ntype == 'INANIS':
            self.visit(node[1])
            return 'Veritas'
        elif ntype == 'AEVUM':
            self.visit(node[1])
            return 'Aeternum'
        elif ntype == 'VERBUM_AEVUM':
            self.visit(node[1])
            return 'Verbum'

        # ---------- Nativas Arduino ----------
        elif ntype == 'PIN_MODE':
            self.visit(node[1])
            self.visit(node[2])
            return 'Vazium'
        elif ntype == 'DIGITAL_WRITE':
            self.visit(node[1])
            self.visit(node[2])
            return 'Vazium'
        elif ntype == 'DIGITAL_READ':
            self.visit(node[1])
            return 'Sanguis'
        elif ntype == 'ANALOG_READ':
            self.visit(node[1])
            return 'Sanguis'
        elif ntype == 'MILLIS':
            return 'Aeternum'
        elif ntype == 'DELAY':
            self.visit(node[1])
            return 'Vazium'
        elif ntype == 'PRINT_EMPTY':
            return 'Vazium'
        elif ntype == 'PRINT':
            self.visit(node[1])
            return 'Vazium'
        elif ntype == 'PRINT_NO_NL':
            self.visit(node[1])
            return 'Vazium'
        elif ntype == 'SERIAL_BEGIN':
            self.visit(node[1])
            return 'Vazium'

        return 'Vazium'
