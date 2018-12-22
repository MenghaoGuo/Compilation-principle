from utils import *


class Lexer:
    def __init__(self, file):
        self._idx = 0
        self._tokenBuffer = ""
        with open(file, 'r') as f:
            self.src = f.read()

    def _addIntoTokenString(self, char):
        self._tokenBuffer += char


    def _getChar(self):
        self._idx += 1
        return self.src[self._idx-1]

    def getToken(self):
        token = Token(Token_Type.ERRTOKEN, "", 0.0, None)
        if self._idx >= len(self.src):
            token = Token(Token_Type.NONTOKEN, "", 0.0, None)
            return token
        char = self._getChar()
        if (char == ' ') or (char == '\n') or (char == '\t'):
            while True:
                if self._idx >= len(self.src):
                    token = Token(Token_Type.NONTOKEN, "", 0.0, None)
                    return token
                char = self._getChar()
                if (char == ' ') or (char == '\n') or (char == '\t'):
                    pass
                else:
                    break
        # self._addIntoTokenString(char)
        if char.isalpha():
            self._addIntoTokenString(char)
            while True:
                if self._idx >= len(self.src):
                    token = Token(Token_Type.ERRTOKEN, self._tokenBuffer, 0.0, None)
                    self._tokenBuffer = ""
                    return token
                char = self._getChar()
                if not char.isalpha():
                    self._idx -= 1
                    break
                self._addIntoTokenString(char)
            for _, table in enumerate(TokenTab):
                if (self._tokenBuffer == table[1]) or (self._tokenBuffer == table[1].lower()):
                    token.type = table[0]
                    token.lexeme = table[1]
                    token.value = table[2]
                    token.func = table[3]
                    self._tokenBuffer = ""
                    return token
            token.lexeme = self._tokenBuffer
            self._tokenBuffer = ""
            return token

        elif char.isdigit():
            self._addIntoTokenString(char)
            while True:
                char = self._getChar()
                if char.isdigit() or (char == '.'):
                    self._addIntoTokenString(char)
                else:
                    self._idx -= 1
                    break
            token.type = Token_Type.CONST_ID
            token.lexeme = self._tokenBuffer
            token.value = float(self._tokenBuffer)
            token.func = None
            self._tokenBuffer = ""
            return token

        else:
            if char == ';':
                token.type = Token_Type.SEMICO
                token.lexeme = ';'
                return token
            elif char == '+':
                token.type = Token_Type.PLUS
                token.lexeme = '+'
                return token
            elif char == ',':
                token.type = Token_Type.COMMA
                token.lexeme = ','
                return token
            elif char == '(':
                token.type = Token_Type.L_BRACKET
                token.lexeme = '('
                return token
            elif char == ')':
                token.type = Token_Type.R_BRACKET
                token.lexeme = ')'
                return token
            elif char == '*':
                if self.src[self._idx] == '*':
                    self._idx += 1
                    token.type = Token_Type.POWER
                    token.lexeme = '**'
                    return token
                else:
                    token.type = Token_Type.MUL
                    token.lexeme = '*'
                    return token
            elif char == '-':
                if self.src[self._idx] == '-':
                    self._idx += 1
                    token.type = Token_Type.COMMENT
                    token.lexeme = '--'
                    return token
                else:
                    token.type = Token_Type.MINUS
                    token.lexeme = '-'
                    return token
            elif char == '/':
                if self.src[self._idx] == '/':
                    self._idx += 1
                    token.type = Token_Type.COMMENT
                    token.lexeme = '//'
                    return token
                else:
                    token.type = Token_Type.DIV
                    token.lexeme = '/'
                    return token
    def getSameToke(self):
        temptation = self.getToken()
        self._idx -= 1
        return temptation



if __name__ == '__main__':
    lexer = Lexer('test.txt')
    # print (123)
    while True:
        token = lexer.getToken()
        if token.type != Token_Type.NONTOKEN:
            print('{:<20s}, {:<10s}, {:<10.2f}, {}'.format(token.type, token.lexeme, token.value, token.func))
        else:
            break

