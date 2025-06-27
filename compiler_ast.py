from dataclasses import dataclass
from typing import List, Optional
from lexer import TokenInfo

@dataclass(kw_only=True)
class ASTNode:
    """Classe base para todos os nós da AST."""
    token: Optional[TokenInfo] = None  # Campo com valor padrão

    @property
    def position(self):
        """Retorna a posição (linha, coluna) para mensagens de erro."""
        if self.token:
            return (self.token.line, self.token.column)
        return (0, 0)

@dataclass
class Program(ASTNode):
    statements: List['ASTNode']

@dataclass
class VarDeclaration(ASTNode):
    var_name: str
    var_type: str
    value: 'ASTNode'

@dataclass
class PrintStatement(ASTNode):
    expression: 'ASTNode'

@dataclass
class IfStatement(ASTNode):
    condition: 'ASTNode'
    body: List['ASTNode']
    else_body: Optional[List[ASTNode]] = None
    
@dataclass
class WhileStatement(ASTNode):
    condition: 'ASTNode'
    body: List['ASTNode']

@dataclass
class BinaryOp(ASTNode):
    left: 'ASTNode'
    op: str
    right: 'ASTNode'

@dataclass
class Number(ASTNode):
    value: int

@dataclass
class String(ASTNode):
    value: str

@dataclass
class Variable(ASTNode):
    name: str

@dataclass
class Boolean(ASTNode):
    value: bool

@dataclass
class WhileStatement(ASTNode):
    condition: 'ASTNode'
    body: List['ASTNode']
    
@dataclass
class ForStatement(ASTNode):
    var_name: str
    start_expr: ASTNode
    end_expr: ASTNode
    body: List[ASTNode]   