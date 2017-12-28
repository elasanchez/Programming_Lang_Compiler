#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 22:31:07 2017

@author: luigi
"""
import sys
class SemanticAnalysis:
    
        # contructor
    def __init__(self):
        
        # Memory_address
        self.mem_address = 10000

        # Symbol Table
        self.symbolTable = []
        self.instrTable = []
        
        # instruction address
        self.instr_address = 1
        #stack
        self.stack =[]
        self.dataType  = []


    def populate(self):
        
#        for record in self.symbolTable:
#            x, y, z = record
#            print("x: {} y: {} z:{}".format(x,y,z))
        record = [300, 10001, 'integer']
        self.symbolTable.append(record)
    
    # Validate that id isn't already in the symbol table
    def check(self, id):
       # linearly search for the variable
        for record in self.symbolTable:
            identifier, memory, type = record
            if identifier == id:
                return 1
        #otherwise return false
        return 0
        
        
    # Insert id in the symbol table
    def insert(self, id, type):
        
        record = [id, self.mem_address, type]
        self.symbolTable.append(record)
        self.mem_address += 1
        
        
    # Get the address of the variable based on id and (line for error purpose)
    def get_address(self, id, line):
        
        # verify id exist first
        if self.check(id):
            # search table linearly
            for record in self.symbolTable:
                identifier, memory, type = record
                if id == identifier:
                    return memory
        else:   
            print("Undeclared variable: {} at line number {}".format(id, line))
            return 0
    # Get the data type based on id and line
    def get_type(self, id, line):
         # verify id exist first
        if self.check(id):
            # search table linearly
            for record in self.symbolTable:
                identifier, memory, type = record
                if id == identifier:
                    return type
        
        else:   
            print("Undeclared variable: {} at line number {}".format(id, line))
            return 0
    #generate instrutions based on ASM inctructions and variable address
    def gen_instruction(self, instr, addr):
        
        record = [self.instr_address, instr, addr]
        self.instrTable.append(record)
        self.instr_address +=1

    # Function to allow to fill in an instruction to jump to
    def back_patch(self, jump_addr):
        addr = self.pop_jumpstack()
       
        # on the [index    Instruction     Addr] replace address from nothing to jum_addr
        self.instrTable[addr-1][2] = jump_addr
    
    # push address in stack
    def push_jumpstack(self, jump_addr):
        self.stack.append(jump_addr)

    # pop address from stack
    def pop_jumpstack(self):
        return self.stack.pop()

    # push data type for type checking
    def push_type(self, data_type):
        self.dataType.append(data_type)
        
    # pop data type for type checking
    def pop_type(self):
        if len(self.dataType) != 0:
            return self.dataType.pop()
        else:
            print("Invalid memory access, stack is empty.")
            self.printSymbolTable()
            self.printAsmCodeList()
            sys.exit()

    # Print the symbol table
    def printSymbolTable(self):
        
        if len(self.symbolTable) != 0:
            print("\nIdentifier\tMem_Address\tType")
            for record in self.symbolTable:
                id, memory, type = record
                print("{}\t\t{}\t\t{}".format(id,memory,type))
        else:
            print("Table is empty")
        
    #print instructions
    def printAsmCodeList(self):
       
        if len(self.instrTable) != 0:
            print("\nInstr_id\tOperator\tOperand")
            for record in self.instrTable:
                instr_id, Op, Oprnd = record
                print("{}\t\t{}\t\t{}".format(instr_id, Op, Oprnd))
        else:
            print("Table is empty")
        
    
    def main(self):
        pass
        #sa = SemanticAnalysis()
#        self.populate()
        #sa.printSymbolTable()
        #print("Address: {}".format(sa.get_address(300, 1)))
        #print("Addresss: {}".format(sa.get_address(400,1)))
#
    
    






















