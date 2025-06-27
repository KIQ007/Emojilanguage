import sys
from pathlib import Path
from lexer import Lexer
from parser import Parser, ParserError
from compiler_ast import ForStatement
from compiler_ast import Program, VarDeclaration, PrintStatement, IfStatement, BinaryOp, Number, String, Variable, Boolean, WhileStatement


def imprimir_ast(no, indent=0):
    prefixo = '  ' * indent
    if isinstance(no, Program):
        print(f"{prefixo}Programa")
        for stmt in no.statements:
            imprimir_ast(stmt, indent + 1)
    elif isinstance(no, ForStatement):
        print(f"{prefixo}For (variável: {no.var_name})")
        print(f"{prefixo}  Início:")
        imprimir_ast(no.start_expr, indent + 2)
        print(f"{prefixo}  Fim:")
        imprimir_ast(no.end_expr, indent + 2)
        print(f"{prefixo}  Corpo:")
        for stmt in no.body:
            imprimir_ast(stmt, indent + 2)
    elif isinstance(no, VarDeclaration):
        print(f"{prefixo}Declaração de variável: {no.var_name} (Tipo: {no.var_type})")
        imprimir_ast(no.value, indent + 1)
    elif isinstance(no, PrintStatement):
        print(f"{prefixo}Comando imprimir:")
        imprimir_ast(no.expression, indent + 1)
    elif isinstance(no, IfStatement):
        print(f"{prefixo}Se")
        print(f"{prefixo}  Condição:")
        imprimir_ast(no.condition, indent + 2)
        print(f"{prefixo}  Corpo:")
        for stmt in no.body:
            imprimir_ast(stmt, indent + 2)
        if hasattr(no, 'else_body') and no.else_body is not None:
            print(f"{prefixo}  Senão:")
            for stmt in no.else_body:
                imprimir_ast(stmt, indent + 2)
    elif isinstance(no, WhileStatement):
        print(f"{prefixo}Enquanto")
        print(f"{prefixo}  Condição:")
        imprimir_ast(no.condition, indent + 2)
        print(f"{prefixo}  Corpo:")
        for stmt in no.body:
            imprimir_ast(stmt, indent + 2)
    elif isinstance(no, BinaryOp):
        op_map = {
            'ADD': '+',
            'SUB': '-',
            'MUL': '*',
            'DIV': '/',
            'GREATER': '>',
            'LESS': '<',
            'EQUAL': '=='
        }
        op_simbolo = op_map.get(no.op, no.op)
        print(f"{prefixo}Operação Binária: {op_simbolo}")
        imprimir_ast(no.left, indent + 1)
        imprimir_ast(no.right, indent + 1)
    elif isinstance(no, Number):
        print(f"{prefixo}Número: {no.value}")
    elif isinstance(no, String):
        print(f'{prefixo}Texto: "{no.value}"')
    elif isinstance(no, Variable):
        print(f"{prefixo}Variável: {no.name}")
    elif isinstance(no, Boolean):
        valor = "Verdadeiro" if no.value else "Falso"
        print(f"{prefixo}Booleano: {valor}")
    else:
        print(f"{prefixo}Nó desconhecido: {no}")

class Interpretador:
    def __init__(self):
        self.ambiente = {}

    def visitar(self, no):
        if isinstance(no, Program):
            for stmt in no.statements:
                self.visitar(stmt)

        elif isinstance(no, VarDeclaration):
            valor = self.visitar(no.value)
            self.ambiente[no.var_name] = valor

        elif isinstance(no, PrintStatement):
            valor = self.visitar(no.expression)
            print(f">>> {valor}")

        elif isinstance(no, ForStatement):
            self.ambiente[no.var_name] = self.visitar(no.start_expr)
            while self.ambiente[no.var_name] <= self.visitar(no.end_expr):
                for stmt in no.body:
                    self.visitar(stmt)
                self.ambiente[no.var_name] += 1

        elif isinstance(no, IfStatement):
            condicao = self.visitar(no.condition)
            if condicao:
                for stmt in no.body:
                    self.visitar(stmt)
            else:
                if hasattr(no, 'else_body') and no.else_body is not None:
                    for stmt in no.else_body:
                        self.visitar(stmt)

        elif isinstance(no, WhileStatement):
            while self.visitar(no.condition):
                for stmt in no.body:
                    self.visitar(stmt)

        elif isinstance(no, BinaryOp):
            esquerda = self.visitar(no.left)
            direita = self.visitar(no.right)
            if no.op == 'ADD':
                return esquerda + direita
            elif no.op == 'SUB':
                return esquerda - direita
            elif no.op == 'MUL':
                return esquerda * direita
            elif no.op == 'DIV':
                return esquerda / direita
            elif no.op == 'GREATER':
                return esquerda > direita
            elif no.op == 'LESS':
                return esquerda < direita
            elif no.op == 'EQUAL':
                return esquerda == direita
            else:
                raise Exception(f"Operador binário não suportado: {no.op}")

        elif isinstance(no, Number):
            return no.value

        elif isinstance(no, String):
            return no.value

        elif isinstance(no, Variable):
            if no.name in self.ambiente:
                return self.ambiente[no.name]
            else:
                raise Exception(f"Variável não definida: '{no.name}'")

        elif isinstance(no, Boolean):
            return no.value

        else:
            raise Exception(f"Nó desconhecido: {type(no)}")


def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <arquivo.emj>")
        return
    
    caminho_arquivo = Path(sys.argv[1])
    if not caminho_arquivo.exists():
        print(f"Erro: Arquivo '{caminho_arquivo}' não encontrado")
        return
    
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            codigo = f.read()
        
        lexer = Lexer(codigo)
        tokens = lexer.tokenize()
        
        parser = Parser(tokens)
        ast = parser.parse()
        
        print("\nCompilação concluída com sucesso!\n")
        print("=== Árvore Sintática Abstrata (AST) ===")
        imprimir_ast(ast)
        
        print("\n=== Saída do programa ===")
        interpretador = Interpretador()
        interpretador.visitar(ast)
        print("=== Fim da execução ===\n")
    
    except Exception as e:
        print(f"Erro: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
