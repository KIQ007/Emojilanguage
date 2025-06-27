# interpreter.py
class Interpreter:
    """Interpretador com estado de execução e melhor tratamento de erros."""
    def __init__(self):
        self.state = {}
    
    def interpret(self, node):
        return node.accept(self)
    
    def visit_Program(self, node):
        results = []
        for stmt in node.statements:
            results.append(stmt.accept(self))
        return results
    
    def visit_VarDeclaration(self, node):
        value = node.value.accept(self)
        self.state[node.var_name] = value
        return value
    
    def visit_PrintStatement(self, node):
        value = node.expression.accept(self)
        print(f"👉 {value} 👈")
        return value
    
    def visit_IfStatement(self, node):
        condition = node.condition.accept(self)
        if isinstance(condition, bool) and condition:
            for stmt in node.body:
                stmt.accept(self)
        return condition
    
    def visit_BinaryOp(self, node):
        left = node.left.accept(self)
        right = node.right.accept(self)
        
        if node.op == 'ADD':
            return left + right
        elif node.op == 'SUB':
            return left - right
        elif node.op == 'MUL':
            return left * right
        elif node.op == 'DIV':
            if right == 0:
                raise RuntimeError("Division by zero", node.token)
            return left / right
        elif node.op == 'GREATER':
            return left > right
        elif node.op == 'LESS':
            return left < right
        elif node.op == 'EQUAL':
            return left == right
        else:
            raise RuntimeError(f"Unknown operator: {node.op}", node.token)
    
    def visit_Number(self, node):
        return node.value
    
    def visit_String(self, node):
        return node.value
    
    def visit_Boolean(self, node):
        return node.value
    
    def visit_Variable(self, node):
        if node.name not in self.state:
            raise RuntimeError(f"Undefined variable: {node.name}", node.token)
        return self.state[node.name]
