#!/usr/bin/env python3
# -*- coding: utf-8 -*-

TERMINALS = 'program var begin end . : ; id , integer real boolean { } = let switch case for to do while loop readln writeln + - * / ( ) constant < <= > >= == !='.split(' ')

class GrammarRule:

    def __init__(self, left, right_list):
        self.left = left
        self.right = right_list

if __name__ == '__main__':
    print(TERMINALS, len(TERMINALS))
