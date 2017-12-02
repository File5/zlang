#!/usr/bin/env python3
# -*- coding: utf-8 -*-

TERMINALS = 'program var begin end . : ; ID , integer real boolean { } = let switch case for to do while loop readln writeln + - * / ( ) CONSTANT < <= > >= == !='.split(' ')


class GrammarRule:

    def __init__(self, left, right_list):
        self.left = left
        self.right = right_list

    def __repr__(self):
        return "<Rule {} ::= {}>".format(self.left, ' '.join(self.right))

    def rightmost_symbol(self):
        return self.right[-1]

    def leftmost_symbol(self):
        return self.right[0]

    def leftmost_terminal(self):
        for symbol in self.right:
            if symbol in TERMINALS:
                return symbol

        return None

    def rightmost_terminal(self):
        for symbol in reversed(self.right):
            if symbol in TERMINALS:
                return symbol

        return None

if __name__ == '__main__':
    grammar = """PROGRAM ::= program var TYPE_DEFINITION_N begin OPERATOR_N end .
TYPE_DEFINITION_N ::= TYPE_DEFINITION | TYPE_DEFINITION TYPE_DEFINITION_N
TYPE_DEFINITION ::= ID_N : TYPE ;
ID_N ::= ID | ID , ID_N
TYPE ::= integer | real | boolean
OPERATOR_N ::= OPERATOR | OPERATOR ; OPERATOR_N
OPERATOR ::= COMPLEX_OPERATOR | ASSIGNMENT_OPERATOR | SWITCH_OPERATOR | FOR_OPERATOR | WHILE_OPERATOR | INPUT_OPERATOR | OUTPUT_OPERATOR
COMPLEX_OPERATOR ::= { OPERATOR_N }
ASSIGNMENT_OPERATOR ::= ID = EXPRESSION | let ID = EXPRESSION
SWITCH_OPERATOR ::= switch EXPRESSION { CASE_N }
CASE_N ::= CASE | CASE CASE_N
CASE ::= case CONSTANT : OPERATOR
FOR_OPERATOR ::= for ASSIGNMENT_OPERATOR to EXPRESSION do OPERATOR
WHILE_OPERATOR ::= do while EXPRESSION OPERATOR loop
INPUT_OPERATOR ::= readln ID_N
OUTPUT_OPERATOR ::= writeln EXPRESSION_N
EXPRESSION_N ::= EXPRESSION | EXPRESSION , EXPRESSION_N
EXPRESSION ::= A < A | A <= A | A > A | A >= A | A == A | A != A | A
A ::= A + T | A - T | T
T ::= T * P | T / P | P
P ::= ( A ) | ID | CONSTANT"""
    rules = []

    # генерация правил по текстовому представлению грамматики
    for i, row in enumerate(grammar.split('\n')):
        rule_list = row.split(' ')

        if rule_list[1] != '::=':
            raise ValueError("'::=' expected at line {}".format(i + 1))

        for item in rule_list:
            if item.isspace():
                raise ValueError("check whitespaces at {}!".format(str(rule_list)))

        rule = GrammarRule(rule_list[0], rule_list[2:])
        rules.append(rule)

    # разбиение правил, содержащих '|'
    def split_rule(rule):
        additional_rules = []

        while '|' in rule.right:
            split_index = rule.right.index('|')

            additional_rules.append(GrammarRule(rule.left, rule.right[:split_index]))
            rule.right = rule.right[split_index + 1:]

        return additional_rules

    for i, rule in enumerate(rules):
        if '|' in rule.right:
            new_rules = split_rule(rule)

            for new_rule in new_rules:
                rules.insert(i, new_rule)

    print("Rules:")
    print(*rules, sep='\n')

    


