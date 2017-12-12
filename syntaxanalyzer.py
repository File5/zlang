#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gen_tables import Grammar
from lexicalanalyzer import Token
from exceptions import SyntaxPrecedenceError, SyntaxRuleError

CONSTANT_TERMINAL = 'CONSTANT'
IDENTIFIER_TERMINAL = 'ID'


class GrammarNode(Token):

    def __init__(self, pos, value, content):
        super().__init__(0, 0, pos, value)
        self.content = content

    def __str__(self):
        return "({}, {})".format(self.value, self.content)

    def __repr__(self):
        return "<GrammarNode {}>".format(str(self))

    def to_format_str(self, indent=0):
        result = " " * indent + self.value + " [\n"

        for token in self.content:
            if type(token) is GrammarNode:
                result += token.to_format_str(indent + 2)
            else:
                result += " " * (indent + 2) + token.value + '\n'

        result += " " * indent + "]\n"
        return result

    def get_line_pos(self):
        return self.pos

class SyntaxAnalyzer:

    def __init__(self):
        self.g = Grammar()
        self.stack = []

    def parse(self, token_list, constants, keywords, ids, delimiters):
        begin_token = Token(0, 0, (0, 0), self.g.begin_terminal)
        self.stack.append(begin_token)
        end_token = Token(0, 0, (0, 0), self.g.end_terminal)
        token_list.append(end_token)

        def is_terminal(x):
            return (x.value in self.g.terminals) or (x.value in constants) or (x.value in keywords) or\
                   (x.value in ids) or (x.value in delimiters) or (x == begin_token) or (x == end_token)

        def get_top_terminal(token_list=self.stack):
            for x in reversed(token_list):
                if is_terminal(x):
                    return x

        def get_next_token():
            nonlocal token_list
            return token_list[0]

        def get_op_table_index(x):
            if x in constants:
                return self.g.terminals.index(CONSTANT_TERMINAL)
            elif x in ids:
                return self.g.terminals.index(IDENTIFIER_TERMINAL)
            elif x == self.g.begin_terminal or x == self.g.end_terminal:
                return len(self.g.terminals)
            else:
                return self.g.terminals.index(x)

        def get_token_for_rule(x):
            if is_terminal(x):
                index = get_op_table_index(x.value)
                return self.g.terminals[index]
            else:
                return x.value

        def get_op_table_content(row_item, col_item):
            row = get_op_table_index(row_item.value)
            col = get_op_table_index(col_item.value)
            return self.g.op_table[row][col]

        def find_rule_with_right(token_list):
            right = list(map(get_token_for_rule, token_list))
            for rule in self.g.skeleton_rules:
                if rule.right == right:
                    return rule
            return None

        def shift(token_list):
            self.stack.append(token_list.pop(0))

        def has_terminal(token_list):
            for i in token_list:
                if is_terminal(i):
                    return True
            return False

        def reduce():
            basis = []

            while not has_terminal(basis):
                basis.append(self.stack.pop())

            aj = get_top_terminal(basis)
            sj = get_top_terminal()
            precedence = get_op_table_content(sj, aj)
            while precedence == '=':
                basis.append(self.stack.pop())
                aj = get_top_terminal(basis)
                sj = get_top_terminal()
                precedence = get_op_table_content(sj, aj)

            stack_top = self.stack[-1]
            if not is_terminal(stack_top):
                basis.append(self.stack.pop())

            basis.reverse()

            rule = find_rule_with_right(basis)
            if rule is not None:
                new_token = GrammarNode(basis[0].pos, rule.left, basis)
                self.stack.append(new_token)
            else:
                raise SyntaxRuleError(*basis[0].pos)

        while True:
            # step 2: main loop
            sj = get_top_terminal()
            aj = get_next_token()

            if sj == begin_token and aj == end_token:
                return self.stack

            precedence = get_op_table_content(sj, aj)

            if precedence == '=' or precedence == '<':
                shift(token_list)
            elif precedence == '>':
                reduce()
            else:
                raise SyntaxPrecedenceError(*aj.pos)
