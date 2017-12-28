#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
@author: luigi


"""

import sys
import lexicalAnalyzer as lac
import SemanticAnalysis as sac

production = ""
tokens = []
lookahead = 0
n = 0 # size of tokens
la = lac.lexicalAnalyzer()
sa = sac.SemanticAnalysis()
datatype = None

def loadTokens():
    global n, tokens, lookahead
    try:

        with open("Tokens.txt") as f:

            for line in f:
                words =  line.split()

                record = []
                for w in words:
                  record.append(w)
                tokens.append(record)

        n = len(tokens)
    except:
        print "Error reading Tokens.txt"
        exeptionMsg()
        sys.exit()
# F or [ <Primary> ]
def F_p():
    global tokens, lookahead, production
    try:
        production = "\t<Identifier Prime> -> [ <IDs> ]"

        if tokens[lookahead][1] == '[':
            printTL()
            lookahead +=1
            I_prime()

            if tokens[lookahead][1] == ']':
                printTL()
                lookahead +=1
            else:
                print 'Invalid use of {} token, "{}" , line {}'.format(tokens[lookahead][0],tokens[lookahead][1],tokens[lookahead][2])
                print 'Expected tokens: "]"'
        else:
            #do nothing
            pass
    except IndexError:
        print "No more tokens to parse, finished"
        exeptionMsg()
        sys.exit()

def R(): #R() is <expression>
    printTL()
    production = "\t<Expression> -> + <Term> <Expression Prime>"
    print production
    Q()
    S()
    # after evaluating the expressions,
    # the last first variables data type is still in stack
    sa.pop_type()

def Q(): #Q is a non terminal that leads to U() that produces terminals w/ w/o expression

    U()
    T()

def S(): # S() produces + and - expressions
    global n, tokens, lookahead, production
    try:
        tok = tokens[lookahead][1]
        
        if tok == '+':
            production = "\t<Expression Prime> -> +<Term> <Expression Prime>"
            printTL()
            print production
            lookahead +=1
            Q()

            # generate instruction just before a repetition of +QS happens
            sa.gen_instruction("ADD", '')
            check_type()
            S()
        elif tok == '-':
            production = "\t<Expression Prime> -> -<Term> <Expression Prime>"
            printTL()
            print production
            lookahead +=1
            Q()

            # generate instruction just before a repetition of +QS happens
            sa.gen_instruction("SUB", '')
            check_type()
            S()
        else:
            #Do nothing since its optional
            pass

    except IndexError:
        print "No more tokens to parse, finished"
        exeptionMsg()
        sys.exit()

def U():
    global n, tokens, lookahead, production
    try:
        if tokens[lookahead][1] == '-':
            production = "\t<Factor> -> - <Primary>"
            printTL()
            lookahead +=1
        else:
            production = "\t<Factor> -> <Primary>"
        print production

        terminal()
    except IndexError:
        print "No more tokens to parse"

def T():
    global n, tokens, lookahead,production
    try:
        tok = tokens[lookahead][1]
        if tok == '*':

            production = "\t<Term> -> <Factor> * <Term>"
            print production
            printTL()
            lookahead +=1
            U()
            
            # generate instruction just before a repetition of *UT happens
            sa.gen_instruction("MUL", '')
            check_type()
            T()
        elif tok == '/':
            printTL()
            production = "\t<Term> -> <Factor> / <Term>"
            print production
            lookahead+=1
            U()

            # generate instruction just before a repetition of /UT happens
            sa.gen_instruction("DIV", '')
            check_type()
            T()
        else:
            #Do nothing'
            pass
    except IndexError:
        print "No more tokens to parse, finished"
        exeptionMsg()
        sys.exit()


def terminal(): # X()
    global n, tokens, lookahead, production
    addr = None
    printTL()
    production = "\t<Primary> ->"
    try:

        if tokens[lookahead][0] == "Identifier":
            production += " <Identifier> "
            print production

            #generate instructions for F -> id using PUSM and addr of lexeme
            addr = sa.get_address(tokens[lookahead][1], tokens[lookahead][2])
            sa.gen_instruction("PUSHM", addr)

            #push type to type stack to check if two operands are the same datatype
            sa.push_type(sa.get_type(tokens[lookahead][1], tokens[lookahead][2]))

            lookahead +=1
            F_p()

        elif tokens[lookahead][0] == "Integer":
            production += " <Integer>"
            print production

            sa.gen_instruction("PUSHI", tokens[lookahead][1])
            sa.push_type(tokens[lookahead][0].lower())
            lookahead +=1
            #print path of integer
        elif tokens[lookahead][0] == "Float":
            production += " <Float>"
            print production
            lookahead +=1
            #print path of float
        elif tokens[lookahead][1] == "true":
            production += " <Keyword>"
            print production
            lookahead +=1
            #print path
        elif tokens[lookahead][1] == "false":
            production += " <Keyword>"
            print production
            lookahead +=1
        elif tokens[lookahead][1] == '(':

            production += "( <Expression> )"
            printTL()
            print production
            lookahead +=1
            R()
            if tokens[lookahead][1] == ')':
                printTL()
                lookahead+=1
            else:
                print 'Invalid use of {} token, "{}" , line {}'.format(tokens[lookahead][0],tokens[lookahead][1],tokens[lookahead][2])
                print 'Expected tokens: ")"'

        else:
            print 'Invalid use of {} token, "{}" , line {}'.format(tokens[lookahead][0],tokens[lookahead][1],tokens[lookahead][2])
            print "Expected tokens: int, float, identifier, bool"
            exeptionMsg()#
            sys.exit() # OPTIONAL EXIT

    except IndexError:
        print "No more tokens to parse, finished"
        exeptionMsg()
        sys.exit()

#FUNCTION DEFN

def rat17F():

    global tokens, lookahead, production
    production = "\t<Rat17F> -> <Opt Function Definition> %% <Opt Declaration List> <Statement List>"
    print production
    A()
    try:

        if tokens[lookahead][1] == "%%":
            printTL()
            lookahead +=1
            B()
            C()

        else:
            print 'Invalid use of {} token, "{}" , line {}'.format(tokens[lookahead][0],tokens[lookahead][1],tokens[lookahead][2])
            print "Expected tokens:  %%"
            exeptionMsg()
            sys.exit()
    except IndexError:
        print "No more tokens to parse"
        print "Expected tokens: %%"
        exeptionMsg()
        sys.exit()
#<Opt Function Definition
def A():
    global production
    try:
        production = "\t<Opt Function Definition> -> <Function Definition> | <Empty>"
        print production
        if tokens[lookahead][1] == "@":
            printTL()
            D()
        else:
            pass
            #Do not thing its optional
    except IndexError:
        print "No more tokens to be parsed, function definition incomplete"
        exeptionMsg()
        sys.exit()

def D():
    E()
    D_prime()
# D' allows multiple function definitions
def D_prime():
    try:
        if tokens[lookahead][1] == "@":
            printTL()
            production = "\t<Function Definition> -> <Function Definition>"
            print production
            D()
        else:
            #Do nothing
            pass
    except IndexError:
        print "No more tokens to parse, function definition incomplete"
        exeptionMsg()
        sys.exit()

#Function Definition
def E():
    global tokens, lookahead, production
    try:
        production = "\t<Function Definition> -> <Function>"
        print production
        if tokens[lookahead][1] == "@":

            lookahead += 1
            if tokens[lookahead][0] == "Identifier":
                printTL()
                lookahead +=1
                if tokens[lookahead][1] == '(':
                    printTL()
                    lookahead +=1
                    G()
                else:
                     print 'Invalid use of {} token, "{}" , line {}'.format(tokens[lookahead][0],tokens[lookahead][1],tokens[lookahead][2])
                     print "Expected token: '(' "

                if tokens[lookahead][1] == ')':
                         printTL()
                         lookahead +=1
                         #<Opt Dec List>
                         B()
                         body()
                else:
                     print 'Invalid use of {} token, "{}" , line {}'.format(tokens[lookahead][0],tokens[lookahead][1],tokens[lookahead][2])
                     print "Expected token: ')' "
                     exeptionMsg()
                     sys.exit()
            else:
                 print 'Invalid use of {} token, "{}" , line {}'.format(tokens[lookahead][0],tokens[lookahead][1],tokens[lookahead][2])
                 print "Expected tokens: Identifier"
        else:
            pass
        #Do nothing, this line will never be executed
    except IndexError:
        print "No more tokens to parse, finished"
        exeptionMsg()
        sys.exit()

# <Opt Parameter List> -> <parameter list> | <Empty>
def G():
    global tokens, lookahead, production
    try:
        if tokens[lookahead][0] == "Identifier":
            printTL()
            production = "\t<Opt Parameter List> -> <Parameter List>"
            print production
            H()
        else:
            #Do nothing since its optional
            pass
    except IndexError:
        print "No more tokens to parse, finished"
        exeptionMsg()

        sys.exit()

def H():
    I()
    H_prime()

# allows multiple parameter
def H_prime():
    global tokens, lookahead, production
    try:

        if tokens[lookahead][1] == ',':
            printTL()
            lookahead +=1
            H()
        else:
            pass
            # Do not take multiple parameters
    except IndexError:
        print "No more tokens to parse, finished"
        exeptionMsg()
        sys.exit()
#<Parameter>
def I():
    global tokens, lookahead, production
    try:
        production = "\t<Parameter> -> <IDs> : <Qualifier>"
        print production
        I_prime()
        if tokens[lookahead][1] == ':':
            printTL()
            lookahead +=1
            K()
        else:
            print 'Invalid use of {} token, "{}" , line {}'.format(tokens[lookahead][0], tokens[lookahead][1], tokens[lookahead][2])
            print "Expected tokens: ':'"
    except IndexError:
        print "No more tokens to parse, finished"
        exeptionMsg()
        sys.exit()

# <Identifier>
def I_prime():
    global tokens, lookahead, production
    try:
        if tokens[lookahead][0] == "Identifier":
            printTL()
            lookahead +=1
            I_double_prime()
        else:
            print 'Invalid use of {} token, "{}" , line {}'.format(tokens[lookahead][0], tokens[lookahead][1], tokens[lookahead][2])
            print "Expected tokens: Identifier"
    except IndexError:
        print "No more tokens to parse, finished"
        exeptionMsg()
        sys.exit()
# <Identifier>, <IDs>
def I_double_prime():
    global tokens, lookahead, production
    try:
        if tokens[lookahead][1] == ',':
            printTL()
            lookahead +=1
            production = "\t<IDs> -> <Identifier>,<IDs>"
            print production
            I_prime()
        else:
            # No more identifier
            production = "\t<IDs> -> <Identifier>"
            print production

    except IndexError:
        print "No more tokens to parse, finished"
        exeptionMsg()
        sys.exit()

def body():
    global tokens, lookahead, production
    try:
        production = "\t<Body> -> { <Statement List> }"
        print production

        if tokens[lookahead][1] == '{':
            printTL()
            lookahead +=1
            C()
            if tokens[lookahead][1] == '}':
                printTL()
                lookahead +=1
                #Do nothing because I don't expect any next token or lexeme
            else:
                print 'Invalid use of {} token, "{}" , line {}'.format(tokens[lookahead][0], tokens[lookahead][1], tokens[lookahead][2])
                print 'Expected tokens: "}"'
                exeptionMsg()
                sys.exit()
        else:
            print 'Invalid use of {} token, "{}" , line {}'.format(tokens[lookahead][0], tokens[lookahead][1], tokens[lookahead][2])
            print 'Expected tokens: "{"'
            exeptionMsg()
            sys.exit()

    except IndexError:
        print "No more tokens to parse, finished"
        exeptionMsg()
        sys.exit()

#K() Determines if the tokens are terminals
def K():
    global tokens, lookahead, production, datatype
    try:
        printTL()
        production = "\t<Qualifier> -> "
        tok = tokens[lookahead][1]
        if tok == 'integer' or tok == 'int':
            lookahead +=1
            datatype = "integer"
            production += " integer"
            print production
        elif tok == 'float' or tok == 'floating' or tok == 'real':
            lookahead +=1
            production += "floating"
            datatype = "float"
            print production
        elif tok == 'boolean' or tok == 'bool':
            lookahead +=1
            production += "boolean"
            datatype = "boolean"
            print production
        else:
             print 'Invalid use of {} token, "{}" , line {}'.format(tokens[lookahead][0], tokens[lookahead][1], tokens[lookahead][2])
             print "Expected tokens: integer, float, true, false"
    except IndexError:
        print "No more tokens to parse, finished"
        exeptionMsg()
        sys.exit()

#<Opt Declaration List>
def B():
    global tokens, lookahead, production
    try:
        tok = tokens[lookahead][1]
        if tok == 'int' or tok == 'integer' or tok == 'floating' or tok == 'float' or tok == 'boolean':
            printTL()
            production = "\t<Opt Declaration List> -> <Declaration List>"
            print production
            L()
        else:
            pass
            #Do nothing since its optional
    except IndexError:
        print "No more tokens to parse"
        exeptionMsg()
        sys.exit()
#Declaration List
def L():
    global tokens, lookahead, production
    M()
    try:
        if tokens[lookahead][1] == ";":
            printTL()
            lookahead +=1
            L_prime()
        else:
            print 'Invalid use of {} token, "{}" , line {}'.format(tokens[lookahead][0], tokens[lookahead][1], tokens[lookahead][2])
            print 'Expected tokens: ";"'
    except IndexError:
        print "No more tokens to parse"
        exeptionMsg()
        sys.exit()
def L_prime():
    global tokens, lookahead, production
    try:
        tok = tokens[lookahead][1]
        if tok == 'int' or tok == 'integer' or tok == 'floating' or tok == 'float' or tok == 'boolean':
            production = "\t<Declaration List> -> <Declaration List>"
            print production
            L()
        else:
            pass
            #Do nothing since its optional extra declaration
            production = "\t<Declaration List> -> <Declaration>"
            print production
    except IndexError:
        print "No more tokens to parse"
        exeptionMsg()
        sys.exit()
#Declaration -> Qualifier ID
def M():
    production = "\t<Declaration> -> <Qualifier> <IDs>"
    print production
    K()
    declareId() # I_prime() equive

    # I_prime() equivalent
def declareId():
    global tokens, lookahead, production, datatype

    try:
        if tokens[lookahead][0] == "Identifier":
            printTL()

             # identifier isn't in the symbol table then ok
            if not sa.check(tokens[lookahead][1]):

                sa.insert(tokens[lookahead][1], datatype)

            else:
                print("Redeclaration of variable is not allowed")
                exeptionMsg()
                sys.exit()
            lookahead +=1
#            I_double_prime()
            declaredId_prime()
        else:
            print 'Invalid use of {} token, "{}" , line {}'.format(tokens[lookahead][0], tokens[lookahead][1], tokens[lookahead][2])
            print "Expected tokens: Identifier"
    except IndexError:
        print "No more tokens to parse, finished"
        exeptionMsg()
        sys.exit()

def declaredId_prime():
    global tokens, lookahead, production, datatype
    try:
        if tokens[lookahead][1] == ',':
            printTL()
            lookahead +=1
            production = "\t<IDs> -> <Identifier>,<IDs>"
            print production
#            I_prime()
            declareId()
        else:
            # No more identifier
            production = "\t<IDs> -> <Identifier>"
            print production
            datatype = None

    except IndexError:
        print "No more tokens to parse, finished"
        exeptionMsg()
        sys.exit()
def exeptionMsg():
        print "No more tokens to parse, finished"
        sa.printSymbolTable()
        sa.printAsmCodeList()



def check_type():

    op2 = sa.pop_type()
    op1 = sa.pop_type()
    if op1 == op2:
        if op1 != 'boolean' and op2 != 'boolean':
            # return the top 2nd operand to be used in multiple operands
            sa.push_type(op2)
            return
        else:
            print("\nERROR\nNo arithmetic operations allowed for boolean type")
            exeptionMsg()
            sys.exit()
    else:
        print("\nERROR\nType mismatch of operands: {}, {}".format(op1, op2))
        exeptionMsg()
        sys.exit()


#Statement List
def C():
    production = "\t<Statement List> -> <Statement>"
    print production
    O()
    O_prime()
# Statement
def O():
    global tokens, lookahead, production
    try:
        production = "\t<Statement> -> "
        tok = tokens[lookahead][0]
        lexeme = tokens[lookahead][1]

        if lexeme == '{':
            #Compound
            production += "<Compound>"
            printTL()
            print production
            compound()
        elif tok == "Identifier":
            #Assign
            production += "<Assign>"
            printTL()
            print production
            assign()
        elif lexeme == "if":
            #if statement
            production += "<If>"
            printTL()
            print production
            if_stmt()
        elif lexeme == "return":
            #return
            printTL()
            production += "<Return>"
            print production
            ret()
        elif lexeme == "write":
            #write
            printTL()
            production += "<Write>"
            print production
            write()
        elif lexeme == "read":
            #read"
            printTL()
            production += "<Read>"
            print production
            read()
        elif lexeme == "while":
            #while
            printTL()
            production += "<While>"
            print production
            while_stmt()
        else:
            #lexeme == '=' or lexeme == '/=' or lexeme == '>' or lexeme == '<' or lexeme == '=>' or lexeme == '<=':
            print 'Invalid use of {} token, "{}" , line {}'.format(tokens[lookahead][0], tokens[lookahead][1], tokens[lookahead][2])
            print 'Expected tokens: "{", "Identifier", "if", "return", "write", "read", "while"'
            exeptionMsg()
            sys.exit()
    except IndexError:
        print "No more tokens to parse, finished"
        exeptionMsg()
        sys.exit()
#Statement_prime
def O_prime():
    global tokens, lookahead, production
    try:
        tok = tokens[lookahead][0]
        lexeme = tokens[lookahead][1]

        if lexeme == '{':
            #Compound
            production = "\t<Statement List> -> <Statement List>"
            print production
            C()
        elif tok == "Identifier":
            #Assign
            production = "\t<Statement List> -> <Statement List>"
            print production
            C()
        elif lexeme == "if":
            #if statement
            production = "\t<Statement List> -> <Statement List>"
            print production
            C()
        elif lexeme == "return":
            #return
            production = "\t<Statement List> -> <Statement List>"
            print production
            C()
        elif lexeme == "write":
            #write
            production = "\t<Statement List> -> <Statement List>"
            print production
            C()
        elif lexeme == "read":
            #read
            production = "\t<Statement List> -> <Statement List>"
            print production
            C()
        elif lexeme == "while":
            #while
            production = "\t<Statement List> -> <Statement List>"
            print production
            C()
        else:
            pass
            #Do nothing since O' is optinal to extend statement

    except IndexError:
        print "No more tokens to parse, finished"
        exeptionMsg()
        sys.exit()

def compound():
    global tokens, lookahead, production
    try:
        production = "\t<Compound> -> { <Condition> }"
        print production
        if tokens[lookahead][1] == '{':
            printTL()
            lookahead +=1
            C()
            if tokens[lookahead][1] == '}':
                printTL()
                lookahead +=1
                #Do nothing because I don't expect any next token or lexeme
            else:
                print 'Invalid use of {} token, "{}" , line {}'.format(tokens[lookahead][0], tokens[lookahead][1], tokens[lookahead][2])
                print 'Expected tokens: "}"'
                exeptionMsg()
                sys.exit()
        else:
            print 'Invalid use of {} token, "{}" , line {}'.format(tokens[lookahead][0], tokens[lookahead][1], tokens[lookahead][2])
            print 'Expected tokens: "{"'
            exeptionMsg()
            sys.exit()

    except IndexError:
        print "No more tokens to parse, finished"
        exeptionMsg()
        sys.exit()

def assign():
    global tokens, lookahead, production

    try:
        production = "\t<Assign> -> <Identifier> := <Expression>"
        print production

        if tokens[lookahead][0] == "Identifier":
            save = tokens[lookahead][1]
            lookahead +=1 #lexer()

            if tokens[lookahead][1] == ":=":
                printTL()
                lookahead+=1
                R()
                addr = sa.get_address(save,tokens[lookahead][2])
                sa.gen_instruction("POPM", addr)

                if tokens[lookahead][1] == ';':
                    printTL()
                    lookahead +=1

                else:
                    print 'Invalid use of {} token, "{}" , line {}'.format(tokens[lookahead][0], tokens[lookahead][1], tokens[lookahead][2])
                    print 'Expected tokens: ";"'
                    exeptionMsg()
                    sys.exit()
            else:
                print 'Invalid use of {} token, "{}" , line {}'.format(tokens[lookahead][0], tokens[lookahead][1], tokens[lookahead][2])
                print 'Expected tokens: ":="'
                exeptionMsg()
                sys.exit()
        else:
            print 'Invalid use of {} token, "{}" , line {}'.format(tokens[lookahead][0], tokens[lookahead][1], tokens[lookahead][2])
            print 'Expected tokens: "Identifier"'
            exeptionMsg()
            sys.exit()

    except IndexError:
        print "No more tokens to parse, finished"
        exeptionMsg()
        sys.exit()


def if_stmt():
    global tokens, lookahead, production
    try:
        if tokens[lookahead][1] == "if":         
            lookahead +=1
            printTL()
            if tokens[lookahead][1] == "(":
                printTL()
                lookahead +=1
                W()
                if tokens[lookahead][1] == ")":
                    printTL()
                    lookahead +=1
                    O() # statement

                    sa.back_patch(sa.instr_address)
                    if_stmt_prime()
                else:
                    print 'Invalid use of {} token, "{}" , line {}'.format(tokens[lookahead][0], tokens[lookahead][1], tokens[lookahead][2])
                    print 'Expected tokens: ")"'
                    exeptionMsg()
                    sys.exit()
            else:
                print 'Invalid use of {} token, "{}" , line {}'.format(tokens[lookahead][0], tokens[lookahead][1], tokens[lookahead][2])
                print 'Expected tokens: "("'
                exeptionMsg()
                sys.exit()
        else:
            print 'Invalid use of {} token, "{}" , line {}'.format(tokens[lookahead][0], tokens[lookahead][1], tokens[lookahead][2])
            print 'Expected tokens: "if"'
            exeptionMsg()
            sys.exit()

    except IndexError:
        print "No more tokens to parse, finished"
        exeptionMsg()
        sys.exit()

def if_stmt_prime():
    global tokens, lookahead, production
    try:

        if tokens[lookahead][1] == "fi":
            printTL()
            lookahead +=1
            production = "\t<If> -> if (<Condition>) <Statement> fi"
            print production
            #Do nothing if statement is finished
        elif tokens[lookahead][1] == "else":
            printTL()
            lookahead +=1
            production += "\t<If> -> if (<Condition>) <Statement fi else <Statement> fi"
            O()
            if tokens[lookahead][1] == "fi":
                printTL()
                lookahead +=1
                #Do nothing if statement is finished
            else:
                print 'Invalid use of {} token, "{}" , line {}'.format(tokens[lookahead][0], tokens[lookahead][1], tokens[lookahead][2])
                print 'Expected tokens: "fi"'
                exeptionMsg()
                sys.exit()
        else:
            print 'Invalid use of {} token, "{}" , line {}'.format(tokens[lookahead][0], tokens[lookahead][1], tokens[lookahead][2])
            print 'Expected tokens: "fi", "else"'
            exeptionMsg()
            sys.exit()

    except IndexError:
        print "No more tokens to parse, finished"
        exeptionMsg()
        sys.exit()


def W():
    production = "\t<Condition> -> <Expression> <Relop> <Expression>"
    print production
    R()
    relop()


def relop():
    global tokens, lookahead, production
    try:
        production = "\t<Relop> -> = | /= | > | < | => | <="
        print production
        op = tokens[lookahead][1]
        if op == '=' or op == '/=' or op == '>' or op == '<' or op == '=>' or op == '<=':
            printTL()
            lookahead +=1
            R()

            if op == '<':
                sa.gen_instruction("LES", '')
            elif op == '>':
                sa.gen_instruction("GRT", '')
            elif op == '=':
                sa.gen_instruction("EQU", '')
            elif op == '/=':
                sa.gen_instruction("NEQ", '')
            elif op == '<=':
                sa.gen_instruction("LEQ", '')
            elif op == '=>':
                sa.gen_instruction("GEQ", '')

            sa.push_jumpstack(sa.instr_address)
            sa.gen_instruction("JUMPZ", '')

        else:
            print 'Invalid use of {} token, "{}" , line {}'.format(tokens[lookahead][0], tokens[lookahead][1], tokens[lookahead][2])
            print 'Expected tokens: "=", "/=", ">", "<", "=>", "<="'
            exeptionMsg()
            sys.exit()

    except IndexError:
        print "No more tokens to parse, finished"
        exeptionMsg()
        sys.exit()

def ret():
    global tokens, lookahead, production
    try:
        if tokens[lookahead][1] == "return":
            printTL()
            lookahead +=1
            ret_prime()
        else:
            print 'Invalid use of {} token, "{}" , line {}'.format(tokens[lookahead][0], tokens[lookahead][1], tokens[lookahead][2])
            print 'Expected tokens: "return"'
            exeptionMsg()

            sys.exit()
    except IndexError:
        print "No more tokens to parse, finished"
        exeptionMsg()
        sys.exit()
def ret_prime():
    global tokens, lookahead, production
    try:
        primarySet = {'Identifier', 'Integer', 'Float', '-', '(', 'true', 'false'}
        if tokens[lookahead][1] == ";":
            printTL()
            lookahead +=1
            # Satisfied return;
            production = "\t<Return> -> return ;"
            print production

            #CHECK MINUS
        elif tokens[lookahead][0] in primarySet or tokens[lookahead][1] in primarySet:
            #DO not consume token, <U> terminal will consume if found
            R()
            if tokens[lookahead][1] == ";":
                printTL()
                lookahead +=1
                production += "\t<Return> -> return <Expression>"
                print production

            else:
                print 'Invalid use of {} token, "{}" , line {}'.format(tokens[lookahead][0], tokens[lookahead][1], tokens[lookahead][2])
                print 'Expected tokens: ";"'
                exeptionMsg()
                sys.exit()
        else:
            print 'Invalid use of {} token, "{}" , line {}'.format(tokens[lookahead][0], tokens[lookahead][1], tokens[lookahead][2])
            print 'Expected tokens: ";", "Identifier"'
    except IndexError:
        print "No more tokens to parse, finished"
        exeptionMsg()
        sys.exit()


def write():
    global tokens, lookahead, production
    try:
        production = "\t<Write> -> write (<Expression>)"
        print production
        if tokens[lookahead][1] == "write":
            printTL()
            lookahead +=1

            if tokens[lookahead][1] == "(":
                printTL()
                lookahead +=1
                # R will call U which consumes token on use
                R()
                '''STDOUT should take top of stack and outputs to the console'''
                sa.gen_instruction("STDOUT", '')
                if tokens[lookahead][1] == ")":
                    printTL()
                    lookahead +=1

                    if tokens[lookahead][1] == ";":
                        printTL()
                        lookahead +=1
                        #Satisfied write(<expression>);
                    else:
                        print 'Invalid use of {} token, "{}" , line {}'.format(tokens[lookahead][0], tokens[lookahead][1], tokens[lookahead][2])
                        print 'Expected tokens: ";"'
                        exeptionMsg()
                        sys.exit()
                else:
                    print 'Invalid use of {} token, "{}" , line {}'.format(tokens[lookahead][0], tokens[lookahead][1], tokens[lookahead][2])
                    print 'Expected tokens: ")"'
                    sys.exit()
            else:
                print 'Invalid use of {} token, "{}" , line {}'.format(tokens[lookahead][0], tokens[lookahead][1], tokens[lookahead][2])
                print 'Expected tokens: "("'
                exeptionMsg()
                sys.exit()
        else:
            print 'Invalid use of {} token, "{}" , line {}'.format(tokens[lookahead][0], tokens[lookahead][1], tokens[lookahead][2])
            print 'Expected tokens: "write"'
            exeptionMsg()

            sys.exit()
    except IndexError:
        print "No more tokens to parse, finished"
        exeptionMsg()
        sys.exit()

def read():
    global tokens, lookahead, production
    try:
        production = "\t<Read> -> read (<IDs>)"
        print production
        if tokens[lookahead][1] == "read":
            printTL()
            '''STDN should read value from console and push on stack'''
            sa.gen_instruction("STDIN", '')

            lookahead += 1

            if tokens[lookahead][1] == "(":
                printTL()
                lookahead +=1

                addr = sa.get_address(tokens[lookahead][1], tokens[lookahead][2])

                I_prime()
                sa.gen_instruction("POPM", addr)
                if tokens[lookahead][1] == ")":
                    printTL()
                    lookahead +=1

                    if tokens[lookahead][1] == ";":
                        printTL()
                        lookahead +=1
                        #Satisfied read(<identifier>);
                    else:
                        print 'Invalid use of {} token, "{}" , line {}'.format(tokens[lookahead][0], tokens[lookahead][1], tokens[lookahead][2])
                        print 'Expected tokens: ";"'
                        exeptionMsg()
                        sys.exit()
                else:
                    print 'Invalid use of {} token, "{}" , line {}'.format(tokens[lookahead][0], tokens[lookahead][1], tokens[lookahead][2])
                    print 'Expected tokens: ")"'
                    exeptionMsg()
                    sys.exit()
            else:
                print 'Invalid use of {} token, "{}" , line {}'.format(tokens[lookahead][0], tokens[lookahead][1], tokens[lookahead][2])
                print 'Expected tokens: "("'
                exeptionMsg()
                sys.exit()
        else:
            print 'Invalid use of {} token, "{}" , line {}'.format(tokens[lookahead][0], tokens[lookahead][1], tokens[lookahead][2])
            print 'Expected tokens: "read"'
            exeptionMsg()
            sys.exit()
    except IndexError:
        print "No more tokens to parse, finished"
        exeptionMsg()
        sys.exit()

def while_stmt():
    global tokens, lookahead, production
    try:
        production = "\t<While> -> while(<Condition>)"
        print production
        if tokens[lookahead][1] == "while":
            printTL()
            #get next instruction address
            addr = sa.instr_address
            # update intruction address
#            sa.instr_address +=1
            sa.gen_instruction("LABEL", '')
            lookahead +=1
            if tokens[lookahead][1] == "(":
                printTL()
                lookahead +=1
                W() # CONDITION
                if tokens[lookahead][1] == ")":
                    printTL()
                    lookahead +=1
                    O() # Statement

                    sa.gen_instruction("JUMP", addr)
                    sa.back_patch(sa.instr_address)
                else:
                    print 'Invalid use of {} token, "{}" , line {}'.format(tokens[lookahead][0], tokens[lookahead][1], tokens[lookahead][2])
                    print 'Expected tokens: ")"'
                    exeptionMsg()
                    sys.exit()
            else:
                print 'Invalid use of {} token, "{}" , line {}'.format(tokens[lookahead][0], tokens[lookahead][1], tokens[lookahead][2])
                print 'Expected tokens: "("'
                exeptionMsg()
                sys.exit()
        else:
            print 'Invalid use of {} token, "{}" , line {}'.format(tokens[lookahead][0], tokens[lookahead][1], tokens[lookahead][2])
            print 'Expected tokens: "while"'
            exeptionMsg()
            sys.exit()
    except IndexError:
        print "No more tokens to parse, finished"
        exeptionMsg()
        sys.exit()

def printTL():
    print "Token: {} \t Lexeme: {}".format(tokens[lookahead][0], tokens[lookahead][1])

def parse():
    global n, tokens, lookahead, production

        #    abc#c# := 10 * 20 / 30 - 10.0 + true
        #  @abc#(a: int, b :float) %% boolean x, y, z; int w, p, e;
    while(lookahead < n):
        validate = rat17F()
        if validate == -1 and lookahead != n:
            # Error has occur
            print("Token's not consumed completely, Error")

def main():

    la.main() # PERFORM LEXICAL ANALYSIS
    sa.main() # LOAD SEMANTIC ANALYSIS FUNCTIONS
    print("==========================PARSE===========================")
    loadTokens()
    parse() # PERFORM SYNTAX-DIRECT TRANSLATION

main()

