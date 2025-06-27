import re
from collections import namedtuple

TokenInfo = namedtuple('TokenInfo', ['type', 'value', 'line', 'column'])

class Lexer:
    def __init__(self, code):
        self.code = code
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        
        self.token_specs = [
            ('INT_TYPE', r'🔢', None),
            ('STRING_TYPE', r'🔤', None),
            ('PRINT', r'👀', None),
            ('IF', r'🙂‍↕️', None),
            ('ELSE', r'🙂‍↔️', None),  
            ('ADD', r'➕', None),
            ('SUB', r'➖', None),
            ('WHILE', r'🤸‍♂️', None),
            ('FOR', r'🌀', None),
            ('MUL', r'✖️', None),
            ('DIV', r'➗', None),
            ('GREATER', r'▶️', None),
            ('LESS', r'◀️', None),
            ('ASSIGN', r'🟰', None),
            ('ASSIGN', r'⬅️', None),
            ('ARROW', r'➡️', None),
            ('SEMICOLON', r'🛑', None),
            ('LPAREN', r'🫸', None),
            ('RPAREN', r'🫷', None),
            ('LBRACE', r'🤜', None),
            ('RBRACE', r'🤛', None),
            ('STRING', r'👉([^👈]*)👈', lambda m: m.group(1)),
            ('NUMBER', r'\d+', lambda m: int(m.group(0))),
            ('BOOL', r'👍|👎', lambda m: m.group(0) == '👍'),
            ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*', None),
            ('WHITESPACE', r'\s+', None),
            ('COMMENT', r'💬.*?💬', None),
            ('NEWLINE', r'\n', None)
        ]

    def tokenize(self):
        while self.pos < len(self.code):
            match = None
            for token_type, pattern, converter in self.token_specs:
                regex = re.compile(pattern)
                match = regex.match(self.code, self.pos)
                if match:
                    value = match.group(0)
                    if token_type in ('WHITESPACE', 'COMMENT'):
                        self.update_pos(value)
                    elif token_type == 'NEWLINE':
                        self.line += 1
                        self.column = 1
                        self.pos += 1
                    else:
                        if converter:
                            value = converter(match)
                        token = TokenInfo(token_type, value, self.line, self.column)
                        self.tokens.append(token)
                        self.update_pos(match.group(0))
                    break
            
            if not match:
                raise Exception(f"Unexpected character '{self.code[self.pos]}' at line {self.line}, column {self.column}")
        
        return self.tokens

    def update_pos(self, text):
        lines = text.split('\n')
        if len(lines) > 1:
            self.line += len(lines) - 1
            self.column = len(lines[-1]) + 1
        else:
            self.column += len(text)
        self.pos += len(text)