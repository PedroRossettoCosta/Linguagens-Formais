class LDInterpreter:
    def __init__(self):
        self.variaveis = {} # Memória RAM da nossa máquina virtual
        self.logs = []      # O Terminal
        
    def log(self, mensagem, tipo="INFO"):
        self.logs.append(f"[{tipo}] {mensagem}")

    def execute(self, ast):
        self.log("Iniciando Ritual de Simulação...", "SISTEMA")
        for node in ast[1]:
            self.visit(node)
        self.log("Ritual concluído com sucesso.", "SISTEMA")
        return self.logs

    def visit(self, node):
        if not node: return None
        ntype = node[0]

        if ntype == 'VAR_DECL':
            valor = self.visit(node[3])
            self.variaveis[node[2]] = valor
            
        elif ntype == 'ASSIGN':
            valor = self.visit(node[2])
            self.variaveis[node[1]] = valor
            
        elif ntype == 'VAR':
            return self.variaveis.get(node[1], 0)
            
        elif ntype in ('INT_LIT', 'FLOAT_LIT', 'STRING_LIT', 'CONST_STATE'):
            return node[1]
            
        elif ntype == 'PRINT':
            valor = self.visit(node[1])
            self.log(str(valor), "REVELAÇÃO")

        elif ntype == 'PIN_MODE':
            pino = self.visit(node[1])
            self.log(f"Pino {pino} ativado no circuito.", "HARDWARE")

        elif ntype == 'DIGITAL_WRITE':
            pino = self.visit(node[1])
            estado = self.visit(node[2])
            self.log(f"Corrente mágica no Pino {pino} alterada para {estado}.", "HARDWARE")

        elif ntype == 'DELAY':
            tempo = self.visit(node[1])
            self.log(f"O tempo congela por {tempo} milissegundos...", "TEMPO")

        # Para rodar a simulação visualmente, executamos o setup e apenas 1 ciclo do loop
        elif ntype == 'SETUP_BLOCK':
            self.log("Executando Exordium (Preparação)...", "SISTEMA")
            for stmt in node[1]: self.visit(stmt)

        elif ntype == 'LOOP_BLOCK':
            self.log("Executando Inferna (1 Ciclo de Simulação)...", "SISTEMA")
            for stmt in node[1]: self.visit(stmt)
            
        # Funções matemáticas básicas para o simulador não quebrar
        elif ntype == 'BINOP':
            esq = self.visit(node[2])
            dir = self.visit(node[3])
            if node[1] == '+': return esq + dir
            if node[1] == '-': return esq - dir
            if node[1] == '*': return esq * dir
            if node[1] == '/': return esq / dir if dir != 0 else 0
            
        elif ntype == 'CONDITION':
            esq = self.visit(node[2])
            dir = self.visit(node[3])
            if node[1] == '==': return esq == dir
            if node[1] == '<': return esq < dir
            if node[1] == '>': return esq > dir

        elif ntype == 'IF_STMT':
            condicao = self.visit(node[1])
            if condicao:
                for stmt in node[2]: self.visit(stmt)