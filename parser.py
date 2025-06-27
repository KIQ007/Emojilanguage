from compiler_ast import *
from lexer import TokenInfo

class ParserError(Exception):
    def __init__(self, message, token=None):
        if token:
            super().__init__(f"{message} at line {token.line}, column {token.column}")
        else:
            super().__init__(message)

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos] if self.tokens else None
    
    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None
    
    def eat(self, token_type, error_msg=None):
        if self.current_token and self.current_token.type == token_type:
            token = self.current_token
            self.advance()
            return token
        msg = error_msg or f"Expected '{token_type}'"
        raise ParserError(msg, self.current_token)
    
    def parse(self):
        statements = []
        while self.current_token:
            if self.current_token.type in ('INT_TYPE', 'STRING_TYPE'):
                statements.append(self.parse_var_declaration())
            elif self.current_token.type == 'PRINT':
                statements.append(self.parse_print())
            elif self.current_token.type == 'IF':
                statements.append(self.parse_if())
            elif self.current_token.type == 'FOR':
                statements.append(self.parse_for())
            elif self.current_token.type == 'WHILE':
                statements.append(self.parse_while())
            elif self.current_token.type == 'SEMICOLON':
                self.eat('SEMICOLON')
            else:
                raise ParserError(f"Unexpected token: {self.current_token.type}", self.current_token)
        return Program(statements=statements)
    
    def parse_for(self):
        token = self.eat('FOR')          # 🌀
        var_name = self.eat('ID').value  # i
        self.eat('ASSIGN', "Esperado '🟰' após variável do for")
        start_expr = self.parse_expression()
        self.eat('ARROW', "Esperado '➡️' depois do início do for")
        end_expr = self.parse_expression()
        self.eat('LBRACE', "Esperado '🤜' antes do corpo do for")

        body = []
        while self.current_token and self.current_token.type != 'RBRACE':
            if self.current_token.type in ('INT_TYPE', 'STRING_TYPE'):
                body.append(self.parse_var_declaration())
            elif self.current_token.type == 'PRINT':
                body.append(self.parse_print())
            elif self.current_token.type == 'IF':
                body.append(self.parse_if())
            elif self.current_token.type == 'FOR':
                body.append(self.parse_for())
            elif self.current_token.type == 'WHILE':
                body.append(self.parse_while())
            elif self.current_token.type == 'SEMICOLON':
                self.eat('SEMICOLON')
            else:
                raise ParserError("Comando inesperado dentro do corpo do for", self.current_token)

        self.eat('RBRACE', "Esperado '🤛' após corpo do for")
        return ForStatement(var_name=var_name, start_expr=start_expr, end_expr=end_expr, body=body, token=token)


    def parse_var_declaration(self):
        var_type = self.current_token.type
        token = self.eat(var_type)
        var_name = self.eat('ID').value
        self.eat('ASSIGN', "Expected '⬅️' or '🟰' after variable name")
        value = self.parse_expression()
        self.eat('SEMICOLON', "Expected '🛑' after declaration")
        return VarDeclaration(var_name=var_name, var_type=var_type, value=value, token=token)

    def parse_print(self):
        token = self.eat('PRINT')
        expr = self.parse_expression()
        self.eat('SEMICOLON', "Expected '🛑' after print statement")
        return PrintStatement(expression=expr, token=token)

    def parse_if(self):
        token = self.eat('IF')
        self.eat('LPAREN', "Expected '🫸' after if")
        condition = self.parse_expression()
        self.eat('RPAREN', "Expected '🫷' after condition")
        self.eat('LBRACE', "Expected '🤜' before if body")
        
        body = []
        while self.current_token and self.current_token.type != 'RBRACE':
            if self.current_token.type in ('INT_TYPE', 'STRING_TYPE'):
                body.append(self.parse_var_declaration())
            elif self.current_token.type == 'PRINT':
                body.append(self.parse_print())
            elif self.current_token.type == 'IF':
                body.append(self.parse_if())
            elif self.current_token.type == 'SEMICOLON':
                self.eat('SEMICOLON')
            else:
                raise ParserError("Unexpected statement in if body", self.current_token)
        
        self.eat('RBRACE', "Expected '🤛' after if body")
        return IfStatement(condition=condition, body=body, token=token)
    
    def parse_while(self):
        token = self.eat('WHILE')
        self.eat('LPAREN', "Esperado '🫸' após while")
        condition = self.parse_expression()
        self.eat('RPAREN', "Esperado '🫷' após condição")
        self.eat('LBRACE', "Esperado '🤜' antes do corpo do while")
        
        body = []
        while self.current_token and self.current_token.type != 'RBRACE':
            if self.current_token.type in ('INT_TYPE', 'STRING_TYPE'):
                body.append(self.parse_var_declaration())
            elif self.current_token.type == 'PRINT':
                body.append(self.parse_print())
            elif self.current_token.type == 'IF':
                body.append(self.parse_if())
            elif self.current_token.type == 'WHILE':
                body.append(self.parse_while())
            elif self.current_token.type == 'SEMICOLON':
                self.eat('SEMICOLON')
            else:
                raise ParserError("Comando inesperado no corpo do while", self.current_token)
        
        self.eat('RBRACE', "Esperado '🤛' após corpo do while")
        return WhileStatement(condition=condition, body=body, token=token)

    
    def parse_if(self):
        token = self.eat('IF')
        self.eat('LPAREN', "Esperado '🫸' após if")
        condition = self.parse_expression()
        self.eat('RPAREN', "Esperado '🫷' após condição")
        self.eat('LBRACE', "Esperado '🤜' antes do corpo do if")
        
        body = []
        while self.current_token and self.current_token.type != 'RBRACE':
            # parse declarações dentro do if
            # ex: var, print, if, etc.
            # exemplo:
            if self.current_token.type in ('INT_TYPE', 'STRING_TYPE'):
                body.append(self.parse_var_declaration())
            elif self.current_token.type == 'PRINT':
                body.append(self.parse_print())
            elif self.current_token.type == 'IF':
                body.append(self.parse_if())
            elif self.current_token.type == 'SEMICOLON':
                self.eat('SEMICOLON')
            else:
                raise ParserError("Esperado declaração válida dentro do if", self.current_token)
        
        self.eat('RBRACE', "Esperado '🤛' após corpo do if")

        else_body = None
        if self.current_token and self.current_token.type == 'ELSE':  # Lembre-se que ELSE deve estar no lexer
            self.eat('ELSE')
            self.eat('LBRACE', "Esperado '🤜' antes do corpo do else")
            else_body = []
            while self.current_token and self.current_token.type != 'RBRACE':
                if self.current_token.type in ('INT_TYPE', 'STRING_TYPE'):
                    else_body.append(self.parse_var_declaration())
                elif self.current_token.type == 'PRINT':
                    else_body.append(self.parse_print())
                elif self.current_token.type == 'IF':
                    else_body.append(self.parse_if())
                elif self.current_token.type == 'SEMICOLON':
                    self.eat('SEMICOLON')
                else:
                    raise ParserError("Esperado declaração válida dentro do else", self.current_token)
            self.eat('RBRACE', "Esperado '🤛' após corpo do else")

        return IfStatement(condition=condition, body=body, else_body=else_body, token=token)



    def parse_expression(self):
        return self.parse_comparison()

    def parse_comparison(self):
        return self.parse_binary_op(
            left_parser=self.parse_additive,
            ops=['GREATER', 'LESS', 'EQUAL'],
            right_parser=self.parse_additive
        )

    def parse_additive(self):
        return self.parse_binary_op(
            left_parser=self.parse_multiplicative,
            ops=['ADD', 'SUB'],
            right_parser=self.parse_multiplicative
        )

    def parse_multiplicative(self):
        return self.parse_binary_op(
            left_parser=self.parse_primary,
            ops=['MUL', 'DIV'],
            right_parser=self.parse_primary
        )

    def parse_binary_op(self, left_parser, ops, right_parser):
        left = left_parser()
        while self.current_token and self.current_token.type in ops:
            op_token = self.current_token
            self.advance()
            right = right_parser()
            left = BinaryOp(left=left, op=op_token.type, right=right, token=op_token)
        return left

    def parse_number(self):
        token = self.current_token
        self.advance()
        try:
            return Number(value=int(token.value), token=token)
        except ValueError:
            raise ParserError(f"Invalid number format: {token.value}", token)

    def parse_string(self):
        token = self.current_token
        self.advance()
        return String(value=token.value, token=token)

    def parse_boolean(self):
        token = self.current_token
        self.advance()
        return Boolean(value=token.value == '👍', token=token)

    def parse_variable(self):
        token = self.current_token
        self.advance()
        return Variable(name=token.value, token=token)

    def parse_primary(self):
        token = self.current_token
        if not token:
            raise ParserError("Unexpected end of input")
            
        if token.type == 'NUMBER':
            return self.parse_number()
        elif token.type == 'STRING':
            return self.parse_string()
        elif token.type == 'BOOL':
            return self.parse_boolean()
        elif token.type == 'ID':
            return self.parse_variable()
        elif token.type == 'LPAREN':
            self.advance()
            expr = self.parse_expression()
            self.eat('RPAREN', "Expected '🫷' after expression")
            return expr
        raise ParserError(
            "Expected number, string, boolean, variable or parenthesized expression", 
            token
        )