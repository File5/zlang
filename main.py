#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys import stderr
from exceptions import InvalidIdentifierError, UndefinedIdentifierError, ParseError
from syntaxanalyzer import SyntaxAnalyzer, GrammarNode
from lexicalanalyzer import LexicalParser, Token
from semanticanalyzer import SemanticAnalyzer
from asmtranslator import AsmTranslator
import sys

filename = "main.zl"


class Compiler:
    def __init__(self):
        pass


if __name__ == '__main__':
    lexicalAnalyzer = LexicalParser([
        "dim",
        "integer",
        "real",
        "boolean",
        "let",
        "if",
        "else",
        "endif",
        "for",
        "to",
        "do",
        "while",
        "readln",
        "writeln",
        "true",
        "false"
    ], r'[A-Za-z]+[0-9]')

    if len(sys.argv) > 1:
        filename = sys.argv[1]

    with open(filename) as f:
        program = f.read()

    try:
        token_list = lexicalAnalyzer.parse(program)

        print("1. Constants:", lexicalAnalyzer.constants)
        print("2. Keywords:", lexicalAnalyzer.keywords)
        print("3. Identifiers:", lexicalAnalyzer.identifiers)
        print("4. Delimiters:", lexicalAnalyzer.delimiters)

        print(Token.token_list_to_str(token_list))

        print(", ".join(map(str, token_list)))

        s = SyntaxAnalyzer()
        nodes = s.parse(
            token_list[:],
            lexicalAnalyzer.constants + ['true', 'false'],
            lexicalAnalyzer.keywords,
            lexicalAnalyzer.identifiers,
            lexicalAnalyzer.delimiters
        )
        program_node = nodes[1]
        print(program_node.to_format_str())

        def get_node_children(node):
            if type(node) is GrammarNode:
                children = []

                for child in node.content:
                    if type(child) is GrammarNode:
                        children.append(child)

                return children
            else:
                return None

        IDENTIFIERS = lexicalAnalyzer.identifiers

        TYPES = ['integer', 'real', 'boolean']

        def IS_IDENTIFIER_DEF_NODE(node):
            try:
                return type(node) is GrammarNode and node.content[-2].value == ':' and node.content[-1].content[0].value in TYPES
            except (NameError, IndexError, AttributeError):
                return False

        def get_identifiers_def(node):
            if type(node) is GrammarNode:
                try:
                    if IS_IDENTIFIER_DEF_NODE(node):
                        identifiers_defined = []
                        # search Identifiers

                        node_queue = [node.content[0]]
                        while len(node_queue) > 0:
                            current_node = node_queue.pop(0)

                            for node in current_node.content:
                                if type(node) is GrammarNode:
                                    node_queue.append(node)
                                elif node.value in IDENTIFIERS:
                                    identifiers_defined.append(node.value)

                        return identifiers_defined

                except (NameError, IndexError):
                    return None
            return None

        def get_identifiers_used(node):
            if type(node) is GrammarNode:
                identifiers_used = []

                for i in node.content:
                    if i.value in IDENTIFIERS:
                        identifiers_used.append(i.value)

                if len(identifiers_used) > 0:
                    return identifiers_used
                else:
                    return None

            return None

        semantic = SemanticAnalyzer(
            get_node_children,
            get_identifiers_def,
            get_identifiers_used
        )

        try:
            semantic.parse_tree(program_node)
        except UndefinedIdentifierError as e:
            print("Semantic error: {}".format(e))
        else:
            print("Semantic analyze finished: OK")

        begin = 0
        end = 0
        for i, token in enumerate(token_list):
            if token.value == "begin":
                begin = i
            elif token.value == "end":
                end = i
        program_token_list = token_list[begin + 1 : end]
        asmt = AsmTranslator(lexicalAnalyzer.constants, lexicalAnalyzer.identifiers)
        asm_lines = "\n".join(asmt.to_asm(program_token_list))

        asm_lines += "\nHLT\n"
        with open("main.asm", "w") as f:
            f.write(asm_lines)

    except ParseError as e:
        print("Syntax error at {}:{} : ".format(*e.get_line_pos()))

    except InvalidIdentifierError as e:
        print("Invalid identifier error at {}:{} : ".format(*e.get_line_pos()) + e.get_info())
