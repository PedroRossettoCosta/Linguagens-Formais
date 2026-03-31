from platform import node


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
        elif ntype == 'CONST_STATE':
            return node[1] # Retorna 'HIGH' ou 'LOW'
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
            return f"digitalWrite({self.visit(node[1])}, {self.visit(node[2])});\n"
        elif ntype == 'DELAY':
            # BUG NINJA CORRIGIDO AQUI! (De node[2] para node[1])
            return f"delay({self.visit(node[1])});\n"
        elif ntype == 'RETURN':
            return f"return {self.visit(node[1])};\n"
        elif ntype == 'PRINT':
            return f"Serial.println({self.visit(node[1])});\n"
        elif ntype == 'STRING_LIT':
            return f'"{node[1]}"'
        return ""
