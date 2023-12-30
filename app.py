from enum import Enum
from typing import List, Union, Tuple

class TokenType(Enum):
    INTEGER = 1
    PLUS = 2
    MINUS = 3
    MULTIPLY = 4
    DIVIDE = 5
    LPAREN = 6
    RPAREN = 7
    ASSIGN = 8
    ID = 9
    IF = 10
    ELSE = 11
    ENDIF = 12
    THEN = 13
    LESS_THAN = 14
    LBRACE = 15
    RBRACE = 16
    LBRACKET = 17
    RBRACKET = 18
    COMMA = 19
    DOT = 20

class Token:
    def __init__(self, type: TokenType, value: str):
        self.type = type
        self.value = value

    def __str__(self):
        return f"({self.type.name}, {self.value})"

def tokenize(input_code):
    def read_number(position):
        result = ""
        while position < len(input_code) and input_code[position].isdigit():
            result += input_code[position]
            position += 1
        return result, position

    def read_identifier(position):
        result = ""
        while position < len(input_code) and (input_code[position].isalnum() or input_code[position] == '_'):
            result += input_code[position]
            position += 1
        return result, position

    special_chars = {
        '+': TokenType.PLUS,
        '-': TokenType.MINUS,
        '*': TokenType.MULTIPLY,
        '/': TokenType.DIVIDE,
        '(': TokenType.LPAREN,
        ')': TokenType.RPAREN,
        '=': TokenType.ASSIGN,
        '<': TokenType.LESS_THAN,
        '{': TokenType.LBRACE,
        '}': TokenType.RBRACE,
    }

    tokens = []

    position = 0
    while position < len(input_code):
        current_char = input_code[position]

        if current_char.isdigit():
            number, position = read_number(position)
            tokens.append(Token(TokenType.INTEGER, number))
        elif current_char.isspace():
            position += 1
        else:
            if current_char in special_chars:
                tokens.append(Token(special_chars[current_char], current_char))
                position += 1
            elif current_char == '<':
                # Handle special case for '<'
                if position + 1 < len(input_code) and input_code[position + 1] == '=':
                    tokens.append(Token(TokenType.LESS_THAN, '<='))
                    position += 2
                else:
                    print(f"Invalid character: {current_char}")
                    exit(1)
            elif current_char.isalpha():
                identifier, position = read_identifier(position)
                tokens.append(Token(TokenType.IF if identifier == "if" else TokenType.ELSE if identifier == "else" else TokenType.ID, identifier))
            else:
                print(f"Invalid character: {current_char}")
                exit(1)

    return tokens

def parse(tokens):
    def match(expected_types):
        nonlocal current
        for expected_type in expected_types:
            if current < len(tokens) and tokens[current].type == expected_type:
                token = tokens[current]
                current += 1
                return token
        return None

    def statement():
        nonlocal current
        if match((TokenType.ID,)):
            assignment()
        elif match((TokenType.IF,)):
            match((TokenType.LPAREN,))
            expression()
            match((TokenType.RPAREN,))
            match((TokenType.LBRACE,))
            statement()
            match((TokenType.RBRACE,))
            if match((TokenType.ELSE,)):
                match((TokenType.LBRACE,))
                statement()
                match((TokenType.RBRACE,))
        else:
            print(f"Syntax error at token: {tokens[current]}")
            exit(1)

    def expression():
        nonlocal current
        term()
        while match((TokenType.PLUS, TokenType.MINUS, TokenType.LESS_THAN)):
            term()

    def assignment():
        nonlocal current
        if match((TokenType.ID, TokenType.ASSIGN)):
            expression()
        else:
            print(f"Syntax error at token: {tokens[current]}")
            exit(1)

    def term():
        nonlocal current
        factor()
        while match((TokenType.MULTIPLY, TokenType.DIVIDE)):
            factor()

    def factor():
        nonlocal current
        if match((TokenType.INTEGER, TokenType.ID)):
            pass
        elif match((TokenType.LPAREN,)):
            expression()
            match((TokenType.RPAREN,))
        elif match((TokenType.MINUS,)):
            factor()
        else:
            print(f"Syntax error at token: {tokens[current]}")
            exit(1)

    current = 0
    while current < len(tokens):
        statement()

def main():
    input_code = """
        age = 10 * (2 + 3)
        if (age < 30) {
            val = 3
            12ab = 3
        } else {
            val = 5 
        }
        """    
    tokens = tokenize(input_code)
    print("Tokens:")
    for token in tokens:
        print(str(token))

    parse(tokens)
    print("Parsing successful.")

if __name__ == "__main__":
    main()