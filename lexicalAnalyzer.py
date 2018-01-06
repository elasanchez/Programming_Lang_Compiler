'''
    Program: lexicalAnalyzer.py
    Programmer: Edgard Luigi Sanchez
    Date: Saturday, Sept. 30, 2017

    Desc: This program simulates the use of Deterministic Finite Automata,
    This finite state machine or finite state automata reads in a source file character by character and feeds it into the machine.
    The machine changes states as it traverses through the states. For convenience, once the machine encounteres an invalid
    symbol, it stops and prints the token. Token is a tuple of class and lexeme, where the class is categorized as Identifier,
    Integer, Float, Separator, Operator, and Keywords.

    This program uses sets to simplify the states a set of symbols may be at a given time. For example, a state self.intState
    represents a digit has been read and the self.langState implies that some symbol in the alphabet has been read but it
    doesn't kknow exactly what symbol that is. This is ok for this program since it uses a variable to store previously read
    symbols for the purpose of printing.

Modified: Jan. 1, 2018
    Modified display format of code on github.
'''


class lexicalAnalyzer:


    def __init__(self):


        self.f =  open("src.txt", 'r')
        self.fw = open('Tokens.txt', 'w')
        # filename = input("Enter filename: ")

        # THE SETS ARE USED TO QUICKLY CHECK MEMBERSHIP OF A SYMBOL OR IDENTIFIER
        # Define the set of keywords
        self.KEYWORD_SET = { 'integer', 'boolean', 'float', 'floating', 'int',
                        'if', 'else', 'fi', 'return', 'write',
                        'read', 'while', 'true', 'false'}
        # Define the set of relational operators
        self.operatorSet = {'<', '<=',
                        ':=','/=', '>',
                        '=', '=>',
                        '/', '*', '-', '+'}
        # Define the set of separators
        self.separatorSet = {'@', '{', '}', ';', '(', ')','[', ']', ','}

        # List the Alphabets
        self.langState = ['a','b','c','d','e',
                    'f','g','h','i','j',
                    'k','l','m','n','o',
                    'p','q','r','s','t',
                    'u','v','w','x','y','z']
        #null state
        self.deadState = 'null'
        # # state
        self.hashState = '#'
        #start state
        self.startState = 'start'
        #state when % has been seen
        self.declarationState = '%'
        #state when < symbom has been seen and predicts = come next
        self.lessRelopState = '<'
        #
        self.greatRelopState = '>'
        #state when : has been seen and predicts = to come next
        self.assignState = ':'
        #state when / has been seen and predicts = to come next
        self.divisionState = '/'
        #state when = has been seen and predict another symbol to follow
        self.equalState = '='

        # Int and Float states
        self.digitSet = {'1','2','3','4','5','6','7','8','9','0'}
        #state when an int was read last
        self.intState = 'int'
        #state when a float was read last
        self.floatState = 'float'
        #state when . was read last
        self.periodState = '.'


    def lexer(self,a):
        #let lexeme be an empty string
        lexeme = ''
        # init state to start state everytime
        state = self.startState

        #check if character belongs to identifier
        if a.isalpha() or a == '#':
            while(1):

                '''ENCOUNTERED A LETTER AFTER A VALID LETTER'''
                if a in self.langState:
                    lexeme += a
                    state = a
                    '''ENCOUNTERED A # SYMBOL AFTER A VALID LETTER'''
                elif state in self.langState and a == '#':
                    lexeme += a
                    state = self.hashState
                    '''ENCOUNTERED A # SYMBOL AT THE START STATE'''
                elif self.startState == state and a == '#':
                    lexeme += a
                    a = self.f.read(1).lower()
                    return ("Invalid use of ", lexeme, a)
                elif state == self.hashState and a == '#':
                   # a = self.f.read(1).lower()
                    if lexeme in self.KEYWORD_SET:
                        return("Keyword", lexeme, a)
                    else:
                        return ("Identifier", lexeme, a)
                elif state == self.hashState and a in self.langState:
                    lexeme += a
                    state = self.langState


                #check next token
                a = self.f.read(1).lower()
                #a = self.nextSymbol() - This shold not be used in the identifier because it gets ride of extra spaces
                #PRINT, RESET STATES AND RESET VARIABLES IF NEXT SYMBOL WONT BE PROCESSED HERE
                if not (a.isalpha() or a == '#'):
                    if lexeme != '':
                        if lexeme in self.KEYWORD_SET:
                            return ("Keyword", lexeme, a)
                        else:
                            return ("Identifier", lexeme, a)
        #ASSUME ITS FLOAT AND HANDLE DIGIT + PERIOD + DIGIT,
        #IF PERIOD IS FOUND, ASSUME ITS FLOAT AND TURN ON FLOAT FLAG
        #IF DIGITS ARE NOT FOLLOWED BY PERIOD THEN IT MUST BE INTEGER
        elif a.isdigit() or a == '.':

            while(1):
                if state == self.startState and a in self.digitSet:
                    lexeme += a
                    state = self.intState
                elif state == self.intState and a in self.digitSet:
                    lexeme += a
                    state = self.intState
                elif state == self.intState and a == '.':
                    lexeme += a
                    state = self.periodState
                elif state == self.periodState and a in self.digitSet:
                    lexeme += a
                    state = self.floatState
                elif state == self.floatState and a in self.digitSet:
                    lexeme += a
                    state = self.floatState
                elif state == self.floatState and a == '.':
                    return ("Float", lexeme, a)
                else:
                    lexeme += a
                    a = self.f.read(1).lower()
                    return ("Invalid use of ", lexeme, a)

                a = self.f.read(1).lower()
                if not (a.isdigit() or a == '.'):
                    if state == self.intState:
                        return ("Integer", lexeme, a)
                    elif state == self.floatState:
                        return ("Float", lexeme, a)

        elif a == '\n' or a == ' ':
        # WHITE SPACES ARE IGNORED
            a = self.f.read(1).lower()
            return ("", "", a)
        #OPERATORS CAN BE PRINTED
        else:
            while(1):
                if state == self.startState and a == '%':
                    lexeme += a
                    a = self.f.read(1).lower()
                    state = self.declarationState
                elif state == self.declarationState and a == '%':
                    lexeme += a
                    a = self.f.read(1).lower()
                    return ("Separator", lexeme, a)
                elif state == self.startState and a == '<':
                    lexeme += a
                    state = self.lessRelopState
                    a = self.f.read(1).lower()
                elif state == self.startState and a == ':':
                    lexeme += a
                    state = self.assignState
                    a = self.f.read(1).lower()
                elif state == self.startState and a == '/':
                    lexeme += a
                    state = self.divisionState
                    a = self.f.read(1).lower()
                elif state == self.startState and a == '=':
                    lexeme += a
                    a = self.f.read(1).lower()
                    state = self.greatRelopState
                elif state == self.greatRelopState and a == '>':
                    lexeme += a
                    a = self.f.read(1).lower()
                    return ("Operator", lexeme, a)
                elif state == self.greatRelopState and a != '>':
                    if a.isalpha() or a.isdigit() or a == ' ':
                        return("Operator", lexeme, a)
                    else:
                        lexeme += a
                        a = self.f.read(1).lower()
                        return ("Not recognized", lexeme, a)
                elif state == self.lessRelopState and a == '=':
                    lexeme += a
                    a = self.f.read(1).lower()
                    return ("Operator", lexeme, a)
                #LESS THAN OR EQUAL TO STATE, CHECK IF < IS FOLLOWED BY = ELSE FALSE
                elif state == self.lessRelopState and a != '=':
                    if not (a in self.operatorSet or a.isalpha() or a.isdigit()):
                        return ("Operator", lexeme, a)
                    else:
                        lexeme += a
                        a = self.f.read(1).lower()
                        return ("Not recognized", lexeme, a)
                #ASSIGNMENT STATE ONCE : SYMBOL HAS BEEN SEEN, NEXT STATE CHECKS IF ITS VALID
                elif state == self.assignState and a == '=' :
                    lexeme += a
                    a = self.f.read(1).lower()
                    return ("Operator", lexeme, a)
                elif state == self.assignState and a != '=':
                    if a.isalpha() or a == ' ' or a == '\n':
                        return ("Operator", lexeme, a)
                    else:
                        lexeme += a
                        a = self.f.read(1).lower()
                        return ("Not recognized", lexeme, a)
                # /= states, check if / is followed by =, digits, or integer which are potential terms
                elif state == self.divisionState and a == '=':
                    lexeme += a
                    a = self.f.read(1).lower()
                    return("Operator", lexeme, a)
                elif state == self.divisionState and a != '=':
                    if a.isalpha() or a.isdigit() or a == ' ':
                        return ("Operator", lexeme, a)
                    else:
                        lexeme += a
                        a = self.f.read(1).lower()
                        return ("Not recognized", lexeme,a)
                elif state == self.startState and a in self.separatorSet:
                    lexeme += a
                    a = self.f.read(1).lower()
                    return ("Separator", lexeme, a)
                elif state == self.startState and a in self.operatorSet:
                    lexeme += a
                    a = self.f.read(1).lower()
                    return("Operator", lexeme, a)
                else:
                    lexeme += a
                    a = self.f.read(1).lower()
                    return ("Not recognized", lexeme, a)

    def nextSymbol(self):
        symbol = self.f.read(1).lower()
        while symbol == ' ':
            symbol = self.f.read(1).lower()
        return symbol


    def E(self,l):
        if l == 'a':
            #l = self.nextSymbol()
            l = self.match(l, 'a')
            self.E_p(l)
        else:
            return

    def E_p(self,l):
        if l == '+':
            #l = self.nextSymbol()
            l = self.match(l, '+')
            l = self.T(l)
            self.E_p(l)
        else:
            return

    def T(self,l):
        if l == "b":
            # l = self.nextSymbol()
#            print ("a + b success")
            #return self.nextSymbol()
            return self.match(l, 'b')
        else:
            return

    def match(self,l, symbol):
        if l == symbol:
            return self.nextSymbol()
        else:
            print("Error matching {} {}".format(l, symbol))

    def tokenize(self):

        lineCounter = 1
        # print character
        l = self.nextSymbol()
            #while its not end of file then keep reading
        while  l != '':
            if l == '\n':
                lineCounter = lineCounter + 1
          
            #calls the lexer to get a token
            tokenClass, tokenLexeme, l = self.lexer(l)
            
            # if lexeme that was passed is empty, it was a whitespace
            # then do not print
            if tokenClass == 'Not recognized':
                tokenLexeme = ' '
           
            if tokenLexeme != '':
                print("{0} \t\t{1}\t\t{2} ".format(tokenClass, tokenLexeme, lineCounter))
                self.fw.write('{0} \t {1} \t {2} \n'.format(tokenClass, tokenLexeme,lineCounter))

#            '''Reset the state since we are already printing the token'''
#            lexeme = ""
#            state = self.startState


    def main(self):
        
        self.tokenize()
        
        self.f.close()
        self.fw.close()
#la = lexicalAnalyzer()
#la.tokenize()


