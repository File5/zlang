#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from exceptions import InvalidIdentifierError, ParseError


class Token:
    TYPE_CONST = 1
    TYPE_KEYWORD = 2
    TYPE_IDENTIFIER = 3
    TYPE_DELIMITER = 4

    def __init__(self, table, index, pos, value):
        self.table = table
        self.index = index
        self.pos = pos
        self.value = value

    def __str__(self):
        return "({}, {})".format(self.table, self.index)

    def __repr__(self):
        return "<Token {}>".format(str(self))

    @staticmethod
    def token_list_to_str(token_list):
        return " ".join(map(lambda token: token.value, token_list))


class LexicalParser:
    def __init__(self, keywords, identifier_regex=r'[A-Za-z_][A-Za-z0-9_]*'):
        self.constants = []
        self.identifiers = []
        self.keywords = keywords
        self.delimiters = []

        self.identifierRegex = re.compile(identifier_regex)

        self.pos = 0
        self.length = 0

        self.line_pos = 1
        self.line = 1

        self.source_string = ""
        self.token_list = []

    def parse(self, source_string):
        self.source_string = source_string
        self.length = len(source_string)

        while True:
            self._parse_whitespaces()

            if self.pos == self.length:
                break

            token_word = self._parse_token_word()
            token_type = self._get_type(token_word)

            if token_type == Token.TYPE_CONST:
                self.token_list.append(self._get_const_token(token_word))

            elif token_type == Token.TYPE_KEYWORD:
                self.token_list.append(self._get_keyword_token(token_word))

            elif token_type == Token.TYPE_IDENTIFIER:
                self.token_list.append(self._get_identifier_token(token_word))

            elif token_type == Token.TYPE_DELIMITER:
                self.token_list.append(self._get_delimiter_token(token_word))

            else:
                raise ParseError(self.line, self.line_pos, "not a valid token for token word '{}'".format(token_word))

            if not self._has_next():
                break

        return self.token_list

    def _get_type(self, token_word):
        if token_word in self.keywords:
            return Token.TYPE_KEYWORD
        elif token_word.isidentifier():
            if self.identifierRegex.fullmatch(token_word):
                return Token.TYPE_IDENTIFIER
            else:
                raise InvalidIdentifierError(self.line, self.line_pos - len(token_word), token_word)
        else:
            if token_word in ('==', '<=', '>=', '!='):
                return Token.TYPE_DELIMITER
            if len(token_word) == 1 and not token_word.isdigit():
                return Token.TYPE_DELIMITER
            else:
                try:
                    value = float(token_word)
                    return Token.TYPE_CONST
                except ValueError:
                    return None

    def _parse_token_word(self):
        predicate = lambda x: x.isalnum() or x in ('_', )
        c = self._current_char()
        if c == '=' and self._peek_next() == '=':
            self._next() # parse first '='
            self._next() # parse second '='
            return '=='

        if c == '<' and self._peek_next() == '=':
            self._next() # parse '<'
            self._next() # parse '='
            return '<='

        if c == '>' and self._peek_next() == '=':
            self._next() # parse '>'
            self._next() # parse '='
            return '>='

        if c == '!' and self._peek_next() == '=':
            self._next() # parse '!'
            self._next() # parse '='
            return '!='

        if not predicate(c):

            if self._has_next():
                self._next()

            return c
        else:
            word = self._parse_while(predicate)
            if word.isnumeric() and self._current_char() == '.' and self._peek_next().isdigit():
                self._next() # parse '.'
                second_word = self._parse_while(predicate)
                return word + '.' + second_word
            else:
                return word

    def _parse_whitespaces(self):
        predicate = lambda x: x.isspace()
        c = self._current_char()
        if not predicate(c):
            return ""
        else:
            word = self._parse_while(predicate)
            return word

    def _get_keyword_token(self, word):
        table = Token.TYPE_KEYWORD
        index = self.keywords.index(word)
        return Token(table, index, self._current_pos(), word)

    def _get_identifier_token(self, word):
        table = Token.TYPE_IDENTIFIER

        if word not in self.identifiers:
            self.identifiers.append(word)

        index = self.identifiers.index(word)
        return Token(table, index, self._current_pos(), word)

    def _get_const_token(self, word):
        table = Token.TYPE_CONST

        if word not in self.constants:
            self.constants.append(word)

        index = self.constants.index(word)
        return Token(table, index, self._current_pos(), word)

    def _get_delimiter_token(self, word):
        table = Token.TYPE_DELIMITER

        if word not in self.delimiters:
            self.delimiters.append(word)

        index = self.delimiters.index(word)
        return Token(table, index, self._current_pos(), word)

    def _parse_while(self, predicate):
        c = self._current_char()
        word = ""

        if predicate(c):
            while predicate(c):
                word += c

                if not self._has_next():
                    self.pos = self.length
                    break

                c = self._next()

            return word
        else:
            raise ParseError(self.line, self.line_pos, "not started with predicate: '{}' found".format(c))

    def _current_char(self):
        return self.source_string[self.pos]

    def _current_pos(self):
        return self.line, self.line_pos

    def _peek_next(self):
        if self.pos + 1 < self.length:
            return self.source_string[self.pos + 1]
        else:
            return None

    def _has_next(self):
        return self.pos + 1 < self.length

    def _next(self):
        if self._current_char() == '\n':
            self.line += 1
            self.line_pos = 0

        self.pos += 1
        self.line_pos += 1

        if self.pos < self.length:
            return self.source_string[self.pos]
        else:
            raise IndexError("source_string index is out of range")