# Sinais especiais para controle de fluxo no simulador
class _BreakSignal: pass
class _ContinueSignal: pass
class _ReturnSignal:
    def __init__(self, value):
        self.value = value


def _num(v):
    """Coage valor para numero, tratando None/string como 0 (simulacao tolerante)."""
    if v is None: return 0
    if isinstance(v, bool): return 1 if v else 0
    if isinstance(v, (int, float)): return v
    try: return float(v)
    except (TypeError, ValueError): return 0


class LDInterpreter:
    LIMITE_ITERACOES = 1000  # trava de segurança para loops infinitos

    def __init__(self):
        self.variaveis = {}   # Memória RAM da nossa máquina virtual
        self.logs = []        # O Terminal
        self.functions = {}   # Funções customizadas registradas

    def log(self, mensagem, tipo="INFO"):
        self.logs.append(f"[{tipo}] {mensagem}")

    def execute(self, ast):
        self.log("Iniciando Ritual de Simulação...", "SISTEMA")
        # 1ª passada: registra funções customizadas e resolve diretivas de topo
        for node in ast[1]:
            if node[0] == 'FUNC_DEF':
                self.functions[node[2]] = node
            elif node[0] == 'DEFINE':
                # macros viram constantes em RAM para a simulação
                self.variaveis[node[1]] = self.visit(node[2])
        # 2ª passada: executa as outras declarações (globais, setup, loop)
        for node in ast[1]:
            if node[0] in ('FUNC_DEF', 'DEFINE'):
                continue
            self.visit(node)
        self.log("Ritual concluído com sucesso.", "SISTEMA")
        return self.logs

    def visit(self, node):
        if not node:
            return None
        ntype = node[0]

        # ---------- Pre-processador / metaprogramacao ----------
        if ntype == 'INCLUDE':
            self.log(f"Biblioteca '{node[1]}' invocada das brumas.", "SISTEMA")
            return None
        elif ntype == 'DEFINE':
            # ja resolvido na 1a passada, mas se chegar aqui revalida
            self.variaveis[node[1]] = self.visit(node[2])
            self.log(f"Decreto '{node[1]}' selado.", "SISTEMA")
            return None
        elif ntype == 'RAW_CPP':
            self.log(f"Trecho Caos: '{node[1][:40]}...' nao simulado.", "AVISO")
            return None

        # ---------- Declarações / atribuições ----------
        if ntype in ('VAR_DECL', 'VAR_DECL_NOSEMI'):
            valor = self.visit(node[3])
            self.variaveis[node[2]] = valor
            return None

        elif ntype == 'VAR_DECL_CUSTOM':
            tipo, nome, valor_node = node[1], node[2], node[3]
            valor = self.visit(valor_node) if valor_node else None
            self.variaveis[nome] = valor if valor is not None else {}  # objeto-stub vazio
            self.log(f"{tipo} '{nome}' materializado.", "HARDWARE")
            return None

        elif ntype == 'CONSTRUCTOR_DECL':
            tipo, nome, args = node[1], node[2], node[3]
            args_eval = [self.visit(a) for a in args]
            self.variaveis[nome] = {"__tipo__": tipo, "__args__": args_eval}
            self.log(f"{tipo} '{nome}' invocado com {len(args_eval)} argumento(s).", "HARDWARE")
            return None

        elif ntype == 'ARRAY_DECL':
            tipo, nome, tamanho = node[1], node[2], node[3]
            self.variaveis[nome] = [0] * tamanho
            self.log(f"Arranjo {tipo}[{tamanho}] '{nome}' consagrado.", "HARDWARE")
            return None

        elif ntype == 'INDEX_ASSIGN':
            nome = node[1]
            chave = self.visit(node[2])
            valor = self.visit(node[3])
            obj = self.variaveis.get(nome)
            if obj is None:
                obj = {}
                self.variaveis[nome] = obj
            if isinstance(obj, dict):
                obj[chave] = valor
            elif isinstance(obj, list):
                try:
                    obj[int(chave)] = valor
                except (TypeError, ValueError, IndexError):
                    pass
            else:
                # promove a dict
                self.variaveis[nome] = {chave: valor}
            return None

        elif ntype == 'INDEX':
            obj = self.visit(node[1])
            chave = self.visit(node[2])
            if isinstance(obj, dict):
                return obj.get(chave, 0)
            if isinstance(obj, list):
                try:
                    return obj[int(chave)]
                except (TypeError, ValueError, IndexError):
                    return 0
            return 0

        elif ntype in ('ASSIGN', 'ASSIGN_NOSEMI'):
            valor = self.visit(node[2])
            self.variaveis[node[1]] = valor
            return None

        elif ntype == 'VAR':
            return self.variaveis.get(node[1], 0)

        elif ntype == 'HEX_LIT':
            return int(node[1], 16)

        elif ntype in ('INT_LIT', 'FLOAT_LIT', 'STRING_LIT', 'CONST_STATE', 'CONST_PIN_MODE'):
            return node[1]

        elif ntype == 'BOOL_LIT':
            return node[1]

        elif ntype == 'NULLPTR':
            return None

        elif ntype == 'TERNARY':
            cond = self.visit(node[1])
            return self.visit(node[2]) if cond else self.visit(node[3])

        # ---------- I/O ----------
        elif ntype == 'PRINT_EMPTY':
            self.log("", "REVELAÇÃO")

        elif ntype == 'PRINT':
            valor = self.visit(node[1])
            self.log(str(valor), "REVELAÇÃO")

        elif ntype == 'PRINT_NO_NL':
            valor = self.visit(node[1])
            self.log(str(valor), "SUSSURRO")

        elif ntype == 'SERIAL_BEGIN':
            baud = self.visit(node[1])
            self.log(f"Vox da Serial canalizada a {baud} baud.", "SISTEMA")

        # ---------- Hardware ----------
        elif ntype == 'PIN_MODE':
            pino = self.visit(node[1])
            direcao = self.visit(node[2])
            self.log(f"Pino {pino} consagrado como {direcao}.", "HARDWARE")

        elif ntype == 'DIGITAL_WRITE':
            pino = self.visit(node[1])
            estado = self.visit(node[2])
            self.log(f"Corrente mágica no Pino {pino} alterada para {estado}.", "HARDWARE")

        elif ntype == 'DIGITAL_READ':
            pino = self.visit(node[1])
            self.log(f"Sentindo essência digital do Pino {pino}.", "HARDWARE")
            return 0  # leitura simulada

        elif ntype == 'ANALOG_READ':
            pino = self.visit(node[1])
            self.log(f"Inspirando anima analógica do Pino {pino}.", "HARDWARE")
            return 0  # leitura simulada

        elif ntype == 'MILLIS':
            return 0  # cronômetro fixo na simulação

        elif ntype == 'DELAY':
            tempo = self.visit(node[1])
            self.log(f"O tempo congela por {tempo} milissegundos...", "TEMPO")

        # ---------- Blocos Arduino ----------
        elif ntype == 'SETUP_BLOCK':
            self.log("Executando Exordium (Preparação)...", "SISTEMA")
            self._exec_block(node[1])

        elif ntype == 'LOOP_BLOCK':
            self.log("Executando Inferna (1 Ciclo de Simulação)...", "SISTEMA")
            self._exec_block(node[1])

        # ---------- Funções customizadas ----------
        elif ntype == 'FUNC_DEF':
            # Já registradas na 1ª passada
            return None

        elif ntype in ('FUNC_CALL', 'FUNC_CALL_STMT'):
            name = node[1]
            args = [self.visit(a) for a in node[2]]
            if name in self.functions:
                return self._chamar_funcao(name, args)
            else:
                self.log(f"Função desconhecida '{name}' invocada — ignorada na simulação.", "AVISO")
                return None

        elif ntype in ('METHOD_CALL', 'METHOD_CALL_STMT'):
            obj = node[1]
            metodo = node[2]
            args = [self.visit(a) for a in node[3]]
            args_str = ", ".join([str(a) for a in args])
            self.log(f"{obj}.{metodo}({args_str}) invocado.", "HARDWARE")
            return 0

        # ---------- Operadores ----------
        elif ntype == 'BINOP':
            esq = self.visit(node[2])
            dir = self.visit(node[3])
            # Concatenacao de strings com '+' (ex: "x"+String(y))
            if node[1] == '+' and (isinstance(esq, str) or isinstance(dir, str)):
                return f"{esq}{dir}"
            esq = _num(esq); dir = _num(dir)
            if node[1] == '+': return esq + dir
            if node[1] == '-': return esq - dir
            if node[1] == '*': return esq * dir
            if node[1] == '/': return esq / dir if dir != 0 else 0
            if node[1] == '%': return esq % dir if dir != 0 else 0

        elif ntype == 'LOGOP':
            esq = self.visit(node[2])
            if node[1] == '&&':
                if not esq: return False
                return bool(self.visit(node[3]))
            if node[1] == '||':
                if esq: return True
                return bool(self.visit(node[3]))

        elif ntype == 'UNARY':
            val = self.visit(node[2])
            if node[1] == '!': return not bool(val)
            if node[1] == '-':
                try: return -val
                except TypeError: return 0
            if node[1] == '&':
                # address-of: na simulacao retornamos o proprio valor (mock)
                return val

        elif ntype == 'CONDITION':
            esq = self.visit(node[2])
            dir = self.visit(node[3])
            op = node[1]
            if op == '==': return esq == dir
            if op == '!=': return esq != dir
            # comparacoes ordenadas: coage para numero (None vira 0) p/ nao explodir
            esq_n = _num(esq); dir_n = _num(dir)
            if op == '<':  return esq_n < dir_n
            if op == '>':  return esq_n > dir_n
            if op == '<=': return esq_n <= dir_n
            if op == '>=': return esq_n >= dir_n

        # ---------- IF / ELSE / ELSE IF ----------
        elif ntype == 'IF_STMT':
            cond = self.visit(node[1])
            if cond:
                return self._exec_block(node[2])
            else:
                else_clause = node[3]
                if not else_clause:
                    return None
                if else_clause[0] == 'ELSE_BLOCK':
                    return self._exec_block(else_clause[1])
                elif else_clause[0] == 'IF_STMT':
                    return self.visit(else_clause)

        # ---------- WHILE ----------
        elif ntype == 'WHILE_STMT':
            i = 0
            while self.visit(node[1]):
                i += 1
                if i > self.LIMITE_ITERACOES:
                    self.log("Loop demoníaco detectado, simulação abortada por segurança.", "AVISO")
                    break
                sinal = self._exec_block(node[2])
                if isinstance(sinal, _BreakSignal): break
                if isinstance(sinal, _ReturnSignal): return sinal
            return None

        # ---------- FOR ----------
        elif ntype == 'FOR_STMT':
            init, cond, update, body = node[1], node[2], node[3], node[4]
            if init: self.visit(init)
            i = 0
            while (cond is None or self.visit(cond)):
                i += 1
                if i > self.LIMITE_ITERACOES:
                    self.log("Loop demoníaco detectado, simulação abortada por segurança.", "AVISO")
                    break
                sinal = self._exec_block(body)
                if isinstance(sinal, _BreakSignal): break
                if isinstance(sinal, _ReturnSignal): return sinal
                if update: self.visit(update)
            return None

        elif ntype == 'BREAK':
            return _BreakSignal()

        elif ntype == 'CONTINUE':
            return _ContinueSignal()

        elif ntype == 'RETURN':
            val = self.visit(node[1]) if node[1] else None
            return _ReturnSignal(val)

        return None

    # ----- helpers -----
    def _exec_block(self, stmts):
        """Executa uma lista de statements, propagando sinais (break/continue/return)."""
        for stmt in stmts:
            sinal = self.visit(stmt)
            if isinstance(sinal, _ContinueSignal):
                return sinal
            if isinstance(sinal, (_BreakSignal, _ReturnSignal)):
                return sinal
        return None

    def _chamar_funcao(self, name, args):
        """Chama uma função customizada com escopo isolado."""
        func = self.functions[name]
        params = func[3]
        body = func[4]

        # Escopo isolado: salva variáveis atuais, injeta parâmetros
        escopo_anterior = self.variaveis.copy()
        for (ptype, pname), val in zip(params, args):
            self.variaveis[pname] = val

        ret_val = None
        sinal = self._exec_block(body)
        if isinstance(sinal, _ReturnSignal):
            ret_val = sinal.value

        self.variaveis = escopo_anterior
        return ret_val
