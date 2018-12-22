from Lexer import *
from treelib import Tree
from treelib import Node
import matplotlib.pyplot as plt
import numpy as np


class Parser :
    def __init__ (self, file_path) :
        self.ERROR = 0
        self.RIGHT = 1
        self.path = file_path
        self.lexer = Lexer (file_path)
        self.token = Token(Token_Type.ERRTOKEN, "", 0.0, None)
        self.state = self.RIGHT
        self.count = 0
        self.iters = 0
        self.origin_x = 0.0
        self.origin_y = 0.0
        self.rot_ang = 0.0
        self.scale_x = 1.0
        self.scale_y = 1.0

        self.tree = Tree ()
        self.root = Node ()

    def typecheck (self, _type) :
        if (self.token.type != _type) :
            self.state = self.ERROR

    def add_node (self, node_name, parents = None, _data = None) :
        node = Node (tag= node_name, data= _data)
        self.tree.add_node (node, parent= parents)
        return node


    def getValue (self) :
        fig = plt.figure()
        pic = plt.subplot()
        with open (self.path, 'r') as f :
            lines = f.readline ()

            while (lines) :
                lines = lines.lower ()
                if (lines.find ('pi') != -1) :
                    lines = lines.replace ('pi', '3.1415926')
                if (lines.find ('origin') != -1) :
                    start = lines.find ('(')
                    end = lines.find (',')
                    endd = lines.find (')')
                    self.origin_x = eval (lines [start + 1 : end])
                    self.origin_y = eval (lines[end + 1: endd])
                elif (lines.find ('rot') != -1) :
                    start = lines.find ('is')
                    self.rot_ang = eval (lines[start + 2: -2])
                elif (lines.find ('scale') != -1) :
                    start = lines.find ('(')
                    end = lines.find (',')
                    endd = lines.find (')')
                    self.scale_x = eval (lines [start + 1 : end])
                    self.scale_y = eval (lines [end + 1 : endd])
                elif (lines.find ('for') != -1) :
                    first = lines.find ('from')
                    second = lines.find ('to')
                    third = lines.find ('step')
                    fourth = lines.find ('draw')
                    start = eval (lines[first + 4 : second])
                    end = eval (lines[second + 2 : third])
                    steps = eval (lines[third + 4 : fourth])
                    ax = []
                    ay = []
                    l_c = lines.find ('(')
                    comma = lines.find (',')
                    r_c = lines.rfind (')')
                    # for iters in range (start, end, steps) :
                    #     t = iters
                    #     ax.append ( eval (lines[l_c + 1 : comma]) )
                    #     ay.append ( eval (lines[comma + 1 : r_c]) )
                    iters = start
                    while (iters < end) :
                        t = iters
                        ax.append ( eval (lines[l_c + 1 : comma]) )
                        ay.append ( eval (lines[comma + 1 : r_c]) )
                        iters += steps
                    ax = np.array (ax)

                    ay = np.array (ay)
                    ax = ax * self.scale_x
                    ay = ay * self.scale_y
                    temp = ax * np.cos (self.rot_ang) + ay * np.sin (self.rot_ang)
                    ay = ay * np.cos (self.rot_ang) - ax * np.sin (self.rot_ang)
                    ax = temp
                    ax += self.origin_x
                    ay += self.origin_y
                    color = ['blue', 'green', 'yellow', 'red']
                    ax = ax.tolist ()
                    ay = ay.tolist ()

                    self.count = self.count % 4
                    pic.scatter (ax, ay, s = 2, c = color[self.count])
                    # plt.show ()
                    self.count += 1
                    self.origin_x = 0
                    self.origin_y = 0
                    self.scale_x = 1
                    self.scale_y = 1
                    self.rot_ang = 0

                lines = f.readline ()
        print (self.origin_x, self.origin_y)
        print (self.scale_x, self.scale_y)
        print (self.rot_ang)
        plt.show ()


    def program (self) :
        '''
        Program → Statement SEMICO Program |ε
        P -> S ; P
        '''
        # node = Node (tag= 'a')
        self.root = Node(tag = 'Program')
        self.token = self.lexer.getToken ()
        self.tree.add_node (self.root)
        node = self.root
        while (self.token.type != Token_Type.NONTOKEN) :

            node1 = Node (tag= 'Statement')
            node2 = Node (tag= ';')
            node3 = Node (tag= 'Program')
            self.tree.add_node (node1, node)
            self.tree.add_node (node2, node)
            self.tree.add_node (node3, node)

            self.statement(node1)
            # self.token = self.lexer.getToken ()
            # print (self.token.type)
            self.typecheck (Token_Type.SEMICO)
            self.token = self.lexer.getToken ()
            node = node3
            if (self.state == self.ERROR) :
                raise SyntaxError ('SyntaxError !')
        self.add_node ('Empty', node)
        print ('---------------------Object Tree----------------------')
        self.tree.show ()
        self.getValue ()

    def statement (self, node) :
        '''
        Statement →  OriginStatment | ScaleStatment
        |  RotStatment    | ForStatment
        '''
        print ('--Enter Statement--')
        if (self.token.type == Token_Type.ORIGIN) :
            node_temp = self.add_node ('OriginStatment', node)
            self.originstatement (node_temp)
        elif (self.token.type == Token_Type.SCALE) :
            node_temp = self.add_node ('ScaleStatment', node)
            self.scalestatement (node_temp)
        elif (self.token.type == Token_Type.ROT) :
            node_temp = self.add_node ('RotStatment', node)
            self.rotstatement (node_temp)
        elif (self.token.type == Token_Type.FOR) :
            node_temp = self.add_node ('forstatement', node)
            self.forstatement (node_temp)
        else :
            self.state = self.ERROR

        print (self.state)
        print ('--End statement--')


    def originstatement (self, node) :
        '''
        OriginStatment → ORIGIN is
        L_BRACKET Expression COMMA Expression R_BRACKET

        '''
        print ('--Enter originstatement--')
        temp_node = Node (tag = ' ')
        if (self.token.type == Token_Type.ORIGIN) :
            temp_node = self.add_node ('ORIGIN', node)
            self.token = self.lexer.getToken ()
            if (self.token.type == Token_Type.IS) :
                self.token = self.lexer.getToken ()
                temp_node = self.add_node ('IS', node)
                if (self.token.type == Token_Type.L_BRACKET) :
                    temp_node = self.add_node ('L_BRACKET', node)
                    self.token = self.lexer.getToken ()
                    temp_node = self.add_node ('Expression', node)
                    self.expression (temp_node)
                    # self.token = self.lexer.getToken ()
                    self.typecheck (Token_Type.COMMA)
                    temp_node = self.add_node ('COMMA', node)
                    self.token = self.lexer.getToken ()
                    temp_node = self.add_node ('Expression', node)
                    self.expression (temp_node)

                    # self.token = self.lexer.getToken ()
                    if (self.token.type != Token_Type.R_BRACKET) :
                        self.state = self.ERROR
                    temp_node = self.add_node ('R_BRACKET', node)
                    self.token = self.lexer.getToken ()
                else :
                    self.state = self.ERROR

            else :
                self.state = self.ERROR

        print (self.state)
        print ('--End originstatement--')


    def scalestatement (self,node) :
        '''
        ScaleStatment  → SCALE IS
            L_BRACKET Expression COMMA Expression R_BRACKET
        '''
        print ('--Enter scalestatement--')
        temp_node = self.add_node ('SCALE', node)
        temp_node = self.add_node ('IS', node)
        temp_node = self.add_node ('L_BRACKET', node)

        self.token = self.lexer.getToken ()
        if (self.token.type != Token_Type.IS) :
            self.state = self.ERROR

        self.token = self.lexer.getToken ()
        if (self.token.type != Token_Type.L_BRACKET) :
            self.state = self.ERROR

        self.token = self.lexer.getToken ()
        temp_node = self.add_node ('Expression', node)
        self.expression (temp_node)
        temp_node = self.add_node ('COMMA', node)
        temp_node = self.add_node ('Expression', node)
        # self.token = self.lexer.getToken ()
        self.typecheck (Token_Type.COMMA)


        self.token = self.lexer.getToken ()

        self.expression (temp_node)
        # self.token = self.lexer.getToken ()
        if (self.token.type != Token_Type.R_BRACKET) :
            self.state = self.ERROR
        temp_node = self.add_node ('R_BRACKET', node)
        self.token = self.lexer.getToken ()
        print (self.state)
        print ('--End scalestatement--')



    def rotstatement (self, node) :
        '''
        RotStatment → ROT IS Expression
        '''
        print ('--Enter rotstatement --')
        temp_node = self.add_node ('ROT', node)
        temp_node = self.add_node ('IS', node)
        temp_node = self.add_node ('Expression', node)
        self.token = self.lexer.getToken ()
        if (self.token.type != Token_Type.IS) :
            self.state = self.ERROR
        self.token = self.lexer.getToken ()
        # print (self.token.type)

        self.expression (temp_node)
        print (self.state)
        print ('--End rotstatement--')


    def forstatement (self, node) :
        '''
        ForStatment → FOR T
        FROM Expression
        TO   Expression
        STEP Expression
        DRAW L_BRACKET Expression COMMA Expression R_BRACKET
        '''
        print ('--Enter forstatement--')
        temp_node = self.add_node ('FOR', node)
        temp_node = self.add_node ('T', node)
        temp_node = self.add_node ('FROM', node)
        temp_node = self.add_node ('Expression', node)
        self.token = self.lexer.getToken ()
        if (self.token.type != Token_Type.T) :
            self.state = self.ERROR
        self.token = self.lexer.getToken ()
        if (self.token.type != Token_Type.FROM) :
            self.state = self.ERROR
        self.token = self.lexer.getToken ()
        self.expression (temp_node)
        temp_node = self.add_node ('TO', node)
        temp_node = self.add_node ('Expression', node)
        # self.token = self.lexer.getToken ()
        self.typecheck (Token_Type.TO)
        self.token = self.lexer.getToken ()
        self.expression (temp_node)
        temp_node = self.add_node ('STEP', node)
        temp_node = self.add_node ('Expression', node)
        # self.token = self.lexer.getToken ()
        self.typecheck (Token_Type.STEP)
        self.token = self.lexer.getToken ()
        self.expression (temp_node)
        temp_node = self.add_node ('DRAW', node)
        temp_node = self.add_node ('L_BRACKET', node)
        temp_node = self.add_node ('Expression', node)
        # self.token = self.lexer.getToken ()
        self.typecheck  (Token_Type.DRAW)
        self.token = self.lexer.getToken ()
        self.typecheck  (Token_Type.L_BRACKET)
        self.token = self.lexer.getToken ()
        self.expression (temp_node)
        temp_node = self.add_node ('COMMA', node)
        temp_node = self.add_node ('Expression', node)
        # self.token = self.lexer.getToken ()
        self.typecheck (Token_Type.COMMA)
        self.token = self.lexer.getToken ()
        self.expression (temp_node)
        temp_node = self.add_node ('R_BRACKET', node)
        # self.token = self.lexer.getToken ()
        self.typecheck (Token_Type.R_BRACKET)
        self.token = self.lexer.getToken ()
        print (self.state)
        print ('--End forstatement--')

    def expression (self, node) :
        '''
        Expression → Term {(PLUS|MINUS)Term }
        E -> T {(PLUS | MINUS) T}
        '''
        print ('--Enter expression--')
        temp_node = self.add_node ('Term', node)
        self.term (temp_node)
        while (self.token.type == Token_Type.PLUS or self.token.type == Token_Type.MINUS) :
            if (token.type == Token_Type.PLUS) :
                temp_node = self.add_node ('PLUS', node, _data= '+')
            else :
                temp_node = self.add_node ('MINUS', node, _data= '-')
            temp_node = self.add_node ('Term', node)
            self.token = self.lexer.getToken ()
            self.term (temp_node)
            # self.token = self.lexer.getToken ()
        print (self.state)
        print ('--End expression--')

    def term (self, node) :
        '''
        Term       	→ Factor { ( MUL | DIV ) Factor }
        '''
        print ('--Enter term--')
        temp_node = self.add_node ('Factor', node)
        self.factor (temp_node)
        while (self.token.type == Token_Type.MUL or self.token.type == Token_Type.DIV) :
            if (self.token.type == Token_Type.MUL) :
                temp_node = self.add_node ('*', node)
            else :
                temp_node = self.add_node ('/', node)
            temp_node = self.add_node ('Factor', node)
            self.token = self.lexer.getToken ()
            self.factor (temp_node)
            # self.token = self.lexer.getToken ()
        print (self.state)
        print ('--End term--')

    def factor (self, node) :
        '''
        Factor  	→ PLUS Factor | MINUS Factor | Component
        '''
        print ('--Enter factor--')
        if (self.token.type == Token_Type.PLUS or self.token.type == Token_Type.MINUS) :
            if (self.token.type == Token_Type.PLUS) :
                temp_node = self.add_node ('+', node)
            else :
                temp_node = self.add_node ('-', node)

            temp_node = self.add_node ('Factor', node)
            self.token = self.lexer.getToken ()
            self.factor (temp_node)
        else :
            # print (self.token.type, self.token.value)
            temp_node = self.add_node ('Component', node)
            self.component (temp_node)
        print (self.state)
        print ('--End Factor--')
    def component (self, node) :
        '''
        Component 	→ Atom [POWER Component]
        '''
        print ('--Enter component--')
        temp_node = self.add_node ('Atom', node)
        self.atom (temp_node)
        self.token = self.lexer.getToken ()

        if (self.token.type == Token_Type.POWER) :
            # self.token = self.lexer.getToken ()
            self.token = self.lexer.getToken ()
            temp_node = self.add_node ('POWER', node)
            temp_node = self.add_node ('Component', node)
            self.component (temp_node)

        print (self.state)
        # print (self.token.type)
        print ('--End component--')



    def atom (self, node) :
        '''
        Atom → CONST_ID
         | T
	     | FUNC L_BRACKET Expression R_BRACKET
         | L_BRACKET Expression R_BRACKET
        '''
        print ('--Enter atom--')
        if (self.token.type == Token_Type.CONST_ID) :
            value = self.token.value
            print (value)
            temp_node = self.add_node ('CONST_ID', node, _data = value)


        elif (self.token.type == Token_Type.T) :
            temp_node = self.add_node ('T', node)

        elif (self.token.type == Token_Type.FUNC) :
            temp_node = self.add_node ('FUNC', node)
            temp_node = self.add_node ('L_BRACKET', node)
            temp_node = self.add_node ('Expression', node)
            self.token = self.lexer.getToken ()
            self.typecheck (Token_Type.L_BRACKET)
            self.token = self.lexer.getToken ()
            self.expression (temp_node)
            self.typecheck (Token_Type.R_BRACKET)
            temp_node = self.add_node ('R_BRACKET', node)
        elif (self.token.type == Token_Type.L_BRACKET) :
            temp_node = self.add_node ('L_BRACKET', node)
            temp_node = self.add_node ('Expression', node)
            self.token = self.lexer.getToken ()
            self.typecheck (Token_Type.R_BRACKET)
            temp_node = self.add_node ('R_BRACKET', node)
        else :
            self.state = self.ERROR
        print (self.state)
        print ('--End Atom--')

    def start (self) :
        print ('Begin !')
        self.program ()
        print ('End !')




def main () :
    file_path = 'test.txt'
    parser = Parser (file_path)
    parser.start ()

if __name__ == '__main__' :
    main ()

