#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from exceptions import KeywordError, LexicalError, ParseError, SyntaxAnalyzeError


class LexicalAnalyzer:
    def __init__(self, keywords, identifier_regex=r'[A-Za-z_][A-Za-z0-9_]*'):
        self.constants = []
        self.identifiers = []
        self.keywords = keywords
        self.delimiters = []

        self.identifierRegex = re.compile(identifier_regex)

        self.pos = 0
        self.length = 0

        self.line_pos = 0
        self.line = 1

        self.source_string = ""

    def analyze(self, source_string):
        self.source_string = source_string
        self.length = len(source_string)

        while self.pos < self.length:
            try:
                program = self._parse_keyword()

                if not program in self.keywords:
                    raise KeywordError(self.line, self.line_pos, "program", program)

            except KeywordError as e:
                raise SyntaxAnalyzeError(*e.get_line_pos(), "keyword", e.get_actual())
            except ParseError as e:
                raise SyntaxAnalyzeError(*e.get_line_pos(), "keyword", self._current_char())

    def _parse_whitespaces(self):
        word = self._parse_while(lambda x : x.isspace())
        return word

    def _parse_keyword(self):
        word = self._parse_while(lambda x : x.isalpha())
        return word

    def _parse_identifier(self):
        c = self._current_char()
        word = ""

        if c.isalpha():
            word += c

            c = self._next()
            while c.isdigit():
                word += c
                c = self._next()

            if c.isalpha():
                word += c
                c = self._next()

                if c.isspace():
                    return word
                else:
                    raise ParseError(self.line, self.line_pos, "not ended with 1 letter: '{}' found".format(c))
            else:
                raise ParseError(self.line, self.line_pos, "not ended with 1 letter: '{}' found".format(c))
        else:
            raise ParseError(self.line, self.line_pos, "not started with letter: '{}' found".format(c))

    def _parse_while(self, predicate):
        c = self._current_char()
        word = ""

        if predicate(c):
            while predicate(c):
                word += c
                c = self._next()

            return word
        else:
            raise ParseError(self.line, self.line_pos, "not started with predicate: '{}' found".format(c))

    def _current_char(self):
        return self.source_string[self.pos]

    def _peek_next(self):
        if self.pos + 1 < self.length:
            return self.source_string[self.pos + 1]
        else:
            return None

    def _next(self):
        if self._current_char() == '\n':
            self.line += 1
            self.line_pos = -1

        self.pos += 1
        self.line_pos += 1

        if self.pos < self.length:
            return self.source_string[self.pos]
        else:
            raise IndexError("source_string index is out of range")


class Compiler:
    def __init__(self):
        pass


if __name__ == '__main__':
    pass
    # lexicalAnalyzer = LexicalAnalyzer()
    # program = input()
