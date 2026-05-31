class LDTranspiler:
    def map_type(self, t):
        """Converte tipos místicos puros do Abyssus em tipos compiláveis do C++."""
        type_map = {
            'Sanguis': 'int',
            'Sanguis_Fluens': 'float',
            'Veritas': 'bool',
            'Vazium': 'void',
            'Verbum': 'String',
            'Aeternum': 'unsigned long',
            'Inscriptio': 'const char*',
            'Littera': 'char',
        }
        if t.startswith('const '):
            base = t[6:]
            return f"const {type_map.get(base, base)}"
        return type_map.get(t, t)

    def translate(self, ast):
        """Gera o C++ separando a AST em 4 seções pela ordem correta de um .ino:
        1. Includes / defines / Caos de topo
        2. Variáveis globais e construtores de objetos
        3. Funções customizadas
        4. setup() e loop()
        """
        topo, globais, funcs, blocos = [], [], [], []

        for node in ast[1]:
            ntype = node[0]
            if ntype in ('INCLUDE', 'DEFINE', 'RAW_CPP'):
                topo.append(node)
            elif ntype == 'FUNC_DEF':
                funcs.append(node)
            elif ntype in ('SETUP_BLOCK', 'LOOP_BLOCK'):
                blocos.append(node)
            else:
                globais.append(node)

        out = "#include <Arduino.h>\n"
        for n in topo:
            out += self.visit(n)
        out += "\n"
        for n in globais:
            out += self.visit(n)
        if globais:
            out += "\n"
        for n in funcs:
            out += self.visit(n)
        for n in blocos:
            out += self.visit(n)
        return out

    def visit(self, node):
        if node is None:
            return ""
        ntype = node[0]

        # ---------- Pre-processador / topo ----------
        if ntype == 'INCLUDE':
            return f"#include <{node[1]}.h>\n"
        elif ntype == 'DEFINE':
            return f"#define {node[1]} {self.visit(node[2])}\n"
        elif ntype == 'RAW_CPP':
            return f"{node[1]}\n"

        # ---------- Declarações / atribuições ----------
        elif ntype == 'VAR_DECL':
            return f"{self.map_type(node[1])} {node[2]} = {self.visit(node[3])};\n"
        elif ntype == 'VAR_DECL_NOSEMI':
            return f"{self.map_type(node[1])} {node[2]} = {self.visit(node[3])}"
        elif ntype == 'VAR_DECL_CUSTOM':
            tipo, nome, valor = node[1], node[2], node[3]
            mapped_type = self.map_type(tipo)
            if valor is None:
                return f"{mapped_type} {nome};\n"
            return f"{mapped_type} {nome} = {self.visit(valor)};\n"
        elif ntype == 'CONSTRUCTOR_DECL':
            tipo, nome, args = node[1], node[2], node[3]
            args_str = ", ".join([self.visit(a) for a in args])
            return f"{self.map_type(tipo)} {nome}({args_str});\n"
        elif ntype == 'ARRAY_DECL':
            return f"{self.map_type(node[1])} {node[2]}[{node[3]}];\n"
        elif ntype == 'INDEX_ASSIGN':
            return f"{node[1]}[{self.visit(node[2])}] = {self.visit(node[3])};\n"
        elif ntype == 'ASSIGN':
            return f"{node[1]} = {self.visit(node[2])};\n"
        elif ntype == 'ASSIGN_NOSEMI':
            return f"{node[1]} = {self.visit(node[2])}"

        # ---------- Operadores ----------
        elif ntype == 'BINOP':
            return f"({self.visit(node[2])} {node[1]} {self.visit(node[3])})"
        elif ntype == 'LOGOP':
            return f"({self.visit(node[2])} {node[1]} {self.visit(node[3])})"
        elif ntype == 'UNARY':
            return f"({node[1]}{self.visit(node[2])})"
        elif ntype == 'CONDITION':
            return f"({self.visit(node[2])} {node[1]} {self.visit(node[3])})"
        elif ntype == 'TERNARY':
            return f"({self.visit(node[1])} ? {self.visit(node[2])} : {self.visit(node[3])})"
        elif ntype == 'INDEX':
            return f"{self.visit(node[1])}[{self.visit(node[2])}]"

        # ---------- Literais ----------
        elif ntype == 'HEX_LIT':
            return str(node[1])
        elif ntype == 'INT_LIT' or ntype == 'FLOAT_LIT':
            return str(node[1])
        elif ntype == 'BOOL_LIT':
            return "true" if node[1] else "false"
        elif ntype == 'STRING_LIT':
            return f'"{node[1]}"'
        elif ntype == 'NULLPTR':
            return "nullptr"
        elif ntype == 'VAR':
            return node[1]
        elif ntype == 'CONST_STATE':
            val = node[1]
            state_map = {
                'Ignis': 'HIGH',
                'Tenebrae': 'LOW',
                'NexusFidelis': 'WL_CONNECTED',
                'Albus': 'WHITE',
                'SSD1306_Tensa': 'SSD1306_SWITCHCAPVCC',
            }
            return state_map.get(val, val)
        elif ntype == 'CONST_PIN_MODE':
            val = node[1]
            pin_map = {
                'Entrada': 'INPUT',
                'Saida': 'OUTPUT',
            }
            return pin_map.get(val, val)

        # ---------- Controle ----------
        elif ntype == 'IF_STMT':
            inner = "".join(["    " + self.visit(s) for s in node[2]])
            cond = self.visit(node[1])
            code = f"if ({cond}) {{\n{inner}}}"
            else_clause = node[3]
            if else_clause:
                if else_clause[0] == 'ELSE_BLOCK':
                    else_inner = "".join(["    " + self.visit(s) for s in else_clause[1]])
                    code += f" else {{\n{else_inner}}}"
                elif else_clause[0] == 'IF_STMT':
                    code += " else " + self.visit(else_clause).rstrip()
            return code + "\n"

        elif ntype == 'WHILE_STMT':
            inner = "".join(["    " + self.visit(s) for s in node[2]])
            return f"while ({self.visit(node[1])}) {{\n{inner}}}\n"

        elif ntype == 'FOR_STMT':
            init = self.visit(node[1]) if node[1] else ""
            cond = self.visit(node[2]) if node[2] else ""
            update = self.visit(node[3]) if node[3] else ""
            inner = "".join(["    " + self.visit(s) for s in node[4]])
            return f"for ({init}; {cond}; {update}) {{\n{inner}}}\n"

        elif ntype == 'BREAK':
            return "break;\n"
        elif ntype == 'CONTINUE':
            return "continue;\n"
        elif ntype == 'RETURN':
            if node[1] is None:
                return "return;\n"
            return f"return {self.visit(node[1])};\n"

        # ---------- Blocos Arduino ----------
        elif ntype == 'SETUP_BLOCK':
            inner = "".join(["    " + self.visit(s) for s in node[1]])
            return f"void setup() {{\n{inner}}}\n\n"
        elif ntype == 'LOOP_BLOCK':
            inner = "".join(["    " + self.visit(s) for s in node[1]])
            return f"void loop() {{\n{inner}}}\n\n"

        # ---------- Funções customizadas ----------
        elif ntype == 'FUNC_DEF':
            ret_type = self.map_type(node[1])
            name = node[2]
            params = ", ".join([f"{self.map_type(ptype)} {pname}" for ptype, pname in node[3]])
            inner = "".join(["    " + self.visit(s) for s in node[4]])
            return f"{ret_type} {name}({params}) {{\n{inner}}}\n\n"

        elif ntype == 'FUNC_CALL_STMT':
            args = ", ".join([self.visit(a) for a in node[2]])
            return f"{node[1]}({args});\n"

        elif ntype == 'FUNC_CALL':
            args = ", ".join([self.visit(a) for a in node[2]])
            return f"{node[1]}({args})"

        elif ntype == 'METHOD_CALL_STMT':
            args = ", ".join([self.visit(a) for a in node[3]])
            return f"{node[1]}.{node[2]}({args});\n"

        elif ntype == 'METHOD_CALL':
            args = ", ".join([self.visit(a) for a in node[3]])
            return f"{node[1]}.{node[2]}({args})"

        # ---------- Novos rituais nativos puros de hardware ----------
        elif ntype == 'TEMPERARE_CRONOS':
            args = ", ".join([self.visit(a) for a in node[1]])
            return f"configTime({args});\n"
        elif ntype == 'SIGNARE_CAOS':
            args = ", ".join([self.visit(a) for a in node[1]])
            return f"serializeJson({args});\n"
        elif ntype == 'SACRATUM':
            return f"F({self.visit(node[1])})"
        elif ntype == 'INANIS':
            return f"isnan({self.visit(node[1])})"
        elif ntype == 'AEVUM':
            return f"time({self.visit(node[1])})"
        elif ntype == 'VERBUM_AEVUM':
            return f"ctime({self.visit(node[1])})"

        # ---------- Nativas Arduino ----------
        elif ntype == 'PIN_MODE':
            return f"pinMode({self.visit(node[1])}, {self.visit(node[2])});\n"
        elif ntype == 'DIGITAL_WRITE':
            return f"digitalWrite({self.visit(node[1])}, {self.visit(node[2])});\n"
        elif ntype == 'DIGITAL_READ':
            return f"digitalRead({self.visit(node[1])})"
        elif ntype == 'ANALOG_READ':
            return f"analogRead({self.visit(node[1])})"
        elif ntype == 'MILLIS':
            return "millis()"
        elif ntype == 'DELAY':
            return f"delay({self.visit(node[1])});\n"
        elif ntype == 'PRINT_EMPTY':
            return "Serial.println();\n"
        elif ntype == 'PRINT':
            return f"Serial.println({self.visit(node[1])});\n"
        elif ntype == 'PRINT_NO_NL':
            return f"Serial.print({self.visit(node[1])});\n"
        elif ntype == 'SERIAL_BEGIN':
            return f"Serial.begin({self.visit(node[1])});\n"

        return ""
