#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys import stderr
from exceptions import InvalidIdentifierError
from syntaxanalyzer import SyntaxAnalyzer
from lexicalanalyzer import LexicalParser, Token


class Compiler:
    def __init__(self):
        pass


if __name__ == '__main__':
    lexicalAnalyzer = LexicalParser([
        "program",
        "var",
        "begin",
        "end",
        "integer",
        "real",
        "boolean",
        "let",
        "switch",
        "case",
        "for",
        "to",
        "do",
        "while",
        "loop",
        "readln",
        "writeln",
        "true",
        "false"
    ], r'[A-Za-z][0-9]*[A-Za-z]')
    program = """
        program
        var
            a123a, b123b : integer;
            c123c, d123d : real;
            e123e, f123f : boolean;
        begin
            let a123a = 123;
            c123c = 12.3;
            f123f = false;
            switch 12 + 3 {
                case 1:
                    d123d = 5.0
                case 15:
                    e123e = true
            }
            for b123b = 1 to 30 do
                writeln 1 + 2
            do while a123a == 123
                a123a = 1234
            loop
        end.
    """
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
            token_list,
            lexicalAnalyzer.constants + ['true', 'false'],
            lexicalAnalyzer.keywords,
            lexicalAnalyzer.identifiers,
            lexicalAnalyzer.delimiters
        )
        print(nodes[1].to_format_str())

    except InvalidIdentifierError as e:
        print("Invalid identifier error at {}:{} : ".format(*e.get_line_pos()) + e.get_info(), file=stderr)
