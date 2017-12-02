#!/usr/bin/env python3
# -*- coding: utf-8 -*-

TERMINALS = 'program var begin end . : ; ID , integer real boolean { } = let switch case for to do while loop readln writeln + - * / ( ) CONSTANT < <= > >= == !='.split(' ')

OUT_FILENAME = 'operator-precedence-table.csv'

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
    print('\n', end='')

    NON_TERMINALS = []

    for rule in rules:
        for item in [rule.left] + rule.right:
            if item not in TERMINALS and item not in NON_TERMINALS:
                NON_TERMINALS.append(item)

    print("Non-terminals found: {}\n{}".format(len(NON_TERMINALS), NON_TERMINALS))
    print('\n', end='')

    def find_rules_with_left(left):
        result = []

        for rule in rules:
            if rule.left == left:
                result.append(rule)

        return result

    leftmost_and_rightmost_nt = {}

    for non_terminal in NON_TERMINALS:
        leftmost_and_rightmost_nt[non_terminal] = {}

        leftmost_and_rightmost_nt[non_terminal]['l'] = []
        leftmost_and_rightmost_nt[non_terminal]['r'] = []

    # начальное заполнение
    for rule in rules:
        leftmost = leftmost_and_rightmost_nt[rule.left]['l']
        symbol = rule.leftmost_symbol()
        if symbol not in leftmost:
            leftmost.append(symbol)

        rightmost = leftmost_and_rightmost_nt[rule.left]['r']
        symbol = rule.rightmost_symbol()
        if symbol not in rightmost:
            rightmost.append(symbol)

    # дополнение вложенными нетерминалами
    def complete_table(leftmost_and_rightmost_nt, lr_key):
        changed = True
        while changed:
            changed = False

            for non_terminal in leftmost_and_rightmost_nt:
                additional_symbols = []

                left_symbols = leftmost_and_rightmost_nt[non_terminal][lr_key]
                for symbol in left_symbols:
                    if symbol in NON_TERMINALS:
                        potential_symbols = leftmost_and_rightmost_nt[symbol][lr_key]

                        for potential_symbol in potential_symbols:
                            if potential_symbol not in left_symbols and potential_symbol not in additional_symbols:
                                additional_symbols.append(potential_symbol)

                changed = changed or len(additional_symbols) > 0
                leftmost_and_rightmost_nt[non_terminal][lr_key] += additional_symbols

    for lr_key in ('l', 'r'):
        complete_table(leftmost_and_rightmost_nt, lr_key)

    print("Non-terminal Leftmost and Rightmost symbols")
    for u, row in leftmost_and_rightmost_nt.items():
        print(u, 'L ' + str(row['l']), 'R ' + str(row['r']), sep='\n', end='\n' + '*' * 80 + '\n')
    print('\n', end='')

    leftmost_and_rightmost_t = {}

    for non_terminal in NON_TERMINALS:
        leftmost_and_rightmost_t[non_terminal] = {}

        leftmost_and_rightmost_t[non_terminal]['l'] = []
        leftmost_and_rightmost_t[non_terminal]['r'] = []

    # начальное заполнение
    for rule in rules:
        leftmost = leftmost_and_rightmost_t[rule.left]['l']
        symbol = rule.leftmost_terminal()
        if symbol is not None and symbol not in leftmost:
            leftmost.append(symbol)

        rightmost = leftmost_and_rightmost_t[rule.left]['r']
        symbol = rule.rightmost_terminal()
        if symbol is not None and symbol not in rightmost:
            rightmost.append(symbol)

    def complete_t_table(leftmost_and_rightmost_nt, lr_key, leftmost_and_rightmost_t):
        changed = True
        while changed:
            changed = False

            for non_terminal in leftmost_and_rightmost_nt:
                additional_symbols = []

                left_nt_symbols = leftmost_and_rightmost_nt[non_terminal][lr_key]
                left_t_symbols = leftmost_and_rightmost_t[non_terminal][lr_key]
                for symbol in left_nt_symbols:
                    if symbol in NON_TERMINALS:
                        potential_symbols = leftmost_and_rightmost_t[symbol][lr_key]

                        for potential_symbol in potential_symbols:
                            if potential_symbol not in left_t_symbols and potential_symbol not in additional_symbols:
                                additional_symbols.append(potential_symbol)

                changed = changed or len(additional_symbols) > 0
                leftmost_and_rightmost_t[non_terminal][lr_key] += additional_symbols

    for lr_key in ('l', 'r'):
        complete_t_table(leftmost_and_rightmost_nt, lr_key, leftmost_and_rightmost_t)

    print("Terminal Leftmost and Rightmost symbols")
    for u, row in leftmost_and_rightmost_t.items():
        print(u, 'Lt ' + str(row['l']), 'Rt ' + str(row['r']), sep='\n', end='\n' + '*' * 80 + '\n')
    print('\n', end='')

    op_table = []
    for i in range(len(TERMINALS)):
        op_table.append([' '] * len(TERMINALS))

    multiple_value_cells = []

    def find_basis_symbols(ai):
        result = []

        for rule in rules:
            search_pos = 0

            while ai in rule.right[search_pos:]:
                search_pos = rule.right.index(ai)

                try:
                    next = rule.right[search_pos + 1]
                    if next in TERMINALS and next not in result:
                        result.append(next)

                    else:
                        after_next = rule.right[search_pos + 2]
                        if after_next in TERMINALS and after_next not in result:
                            result.append(after_next)
                            search_pos += 1
                except IndexError:
                    pass

                finally:
                    search_pos += 1

        return result

    def find_next_prev_symbols(ai, delta=1):
        result = []

        for rule in rules:
            search_pos = 0
            while ai in rule.right[search_pos:]:
                search_pos = rule.right.index(ai)

                try:
                    # не использовать отрицательные значения!
                    if search_pos + delta < 0:
                        raise IndexError()

                    next = rule.right[search_pos + delta]
                    if next in NON_TERMINALS and next not in result:
                        result.append(next)

                except IndexError:
                    pass

                finally:
                    search_pos += 1

        return result

    def find_precedes_symbols(ai):
        return find_next_prev_symbols(ai, 1)

    def find_follows_symbols(ai):
        return find_next_prev_symbols(ai, -1)

    def set_or_append_op_table(row, col, value):
        if op_table[row][col] == ' ':
            op_table[row][col] = value
        else:
            if value not in op_table[row][col]:
                op_table[row][col] += value
                multiple_value_cells.append((row, col))

    for i, ai in enumerate(TERMINALS):
        basis = find_basis_symbols(ai)

        for bj in basis:
            j = TERMINALS.index(bj)
            set_or_append_op_table(i, j, '=')

        precedes = find_precedes_symbols(ai)

        for U in precedes:
            symbols = leftmost_and_rightmost_t[U]['l']

            for symbol in symbols:
                j = TERMINALS.index(symbol)
                set_or_append_op_table(i, j, '<')

        follows = find_follows_symbols(ai)

        for U in follows:
            symbols = leftmost_and_rightmost_t[U]['r']

            for symbol in symbols:
                j = TERMINALS.index(symbol)
                set_or_append_op_table(j, i, '>')

    # print(str(op_table).replace('], ', '],\n '))

    str_op_table = op_table[:]

    for i, row in enumerate(str_op_table):
        row.insert(0, TERMINALS[i])

    str_op_table.insert(0, [' '] + TERMINALS)

    with open(OUT_FILENAME, "w") as f:
        for row in str_op_table:
            f.write(";".join(map(lambda x : '"{}"'.format(x), row)) + '\n')

    print("Operator precedence table has been written to file '{}'".format(OUT_FILENAME))

    if len(multiple_value_cells) > 0:
        print()
        print("WARNING: Table contains cells with multiple values!\nConflicts should be solved manually!\n")

        print("List of cells with multiple values:")

        str_cells = []
        for i, j in multiple_value_cells:
            str_cells.append("('{}' '{}')".format(TERMINALS[i], TERMINALS[j]))

        print(" ".join(str_cells))
