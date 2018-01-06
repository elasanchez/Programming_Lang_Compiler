# Programming_Lang_Compiler
This program will consist 3 out of the 5 phases of the traditional language compilers,
lexical, syntax, and semantic analysis. These phases will produce and display the tokens, produciton rules used, symbol table, and a fictitious assembly code instruction listing.

The source code will be a simplified language without reals and function definition productions. The program must also consider that Boolean variables must not be able to perform arithmetic operations and no conversion of data type in operations are allowed.

###### Program Requirements
-   Python 2.7

###### How to Use the Program
1.  Open terminal
2.  Change directory to …/Programming_Lang_Compiler
3.  Type command:
    python compiler_driver.py


###### Input/output
The program produces “Tokens.txt” from input file “src.txt”.
Tokens.txt will contain tokens and lexemes with their corresponding line number.
The program will output tokens, lexemes, line number first then outputs the corresponding production rules used.
Lastly, prints out the symbol table and the assembly code listings.


###### Designing the Program

The program utilizes the previous two phases: lexical analyzer and syntax analyzer and performs a semantic analysis while performing the syntax analyzer. This method is call *Syntax-direct translation*. The semantic actions will be performed as the syntax analyzer traverses through the tokens. The program will keep track of variables declared and instructions generated in an array. It also uses a stack to allow a back patching of missing addresses of resulting control structures such as loops and if statements. When the program ends, it will print out the content of its symbol table and its generated instructions.

The program generates assembly instructions defined by a fictitious assembly language following:
PUSHI, PUSHM, POPM, STDOUT, STDIN, ADD, SUB, MUL, DIV, GRT, LES, EQU, NEQ,  GEQ, LEQ, JUMPZ, JUMP, and LABEL.


## Example

Input Source code:

%% 
    integer   i, max, sum;

    sum := 0;
    i := 1;
    read ( max);
    while (i <  max)  {
          sum := sum + i;
          i  := i + 1; 
     }
     write (sum+max);

Output: 

###### Symbol Table

Identifier Mem_Address Type

i 10000 integer

max 10001 integer

sum 10002 integer


###### Assembly code listing
Instr_id Operator Operand

1   PUSHI   0

2   POPM   10002

3   PUSHI  1

4   POPM   10000

5   STDIN  

6   POPM   10001

7   LABEL  

8   PUSHM  10000

9   PUSHM  10001

10  LES    

11  JUMPZ  21

12  PUSHM  10002

13  PUSHM  10000

14  ADD    

15  POPM   10002

16  PUSHM  10000

17  PUSHI  1

18  ADD    

19  POPM   10000

20  JUMP   7

21  PUSHM  10002

22  PUSHM  10001

23  ADD    

24  STDOUT
