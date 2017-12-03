#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class ParseError(Exception):

    def __init__(self, line, pos, info=None):
        super(ParseError, self).__init__(info)
        self.pos = pos
        self.line = line
        self.info = info

    def get_line_pos(self):
        return self.line, self.pos

    def get_info(self):
        return self.info


class LexicalError(ParseError):

    def __init__(self, line, pos, expected, actual):
        super(LexicalError, self).__init__(
            line,
            pos,
            "{} expected, but was '{}'".format(expected, actual)
        )


class InvalidIdentifierError(LexicalError):

    def __init__(self, line, pos, wrong_identifier):
        super(InvalidIdentifierError, self).__init__(
            line,
            pos,
            'identifier',
            wrong_identifier
        )
        self.wrong_identifier = wrong_identifier

    def get_wrong_identifier(self):
        return self.wrong_identifier


class KeywordError(LexicalError):

    def __init__(self, line, pos, keyword_expected, actual):
        super(KeywordError, self).__init__(line, pos, "keyword '{}'".format(keyword_expected), actual)
        self.actual = actual

    def get_actual(self):
        return self.actual


class SyntaxAnalyzeError(LexicalError):

    def __init__(self, line, pos, expected, actual):
        super(SyntaxAnalyzeError, self).__init__(line, pos, expected, actual)
        
        
class SyntaxPrecedenceError(ParseError):
    
    def __init__(self, line, pos):
        super(SyntaxPrecedenceError, self).__init__(line, pos)
        

class SyntaxRuleError(ParseError):
    
    def __init__(self, line, pos):
        super(SyntaxRuleError, self).__init__(line, pos)
