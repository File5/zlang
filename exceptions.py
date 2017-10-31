#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class ParseError(Exception):

    def __init__(self, line, pos, info=None):
        super(ParseError, self).__init__(info)
        self.pos = pos
        self.line = line

    def get_line_pos(self):
        return self.line, self.pos


class LexicalError(ParseError):

    def __init__(self, line, pos, expected, actual):
        super(LexicalError, self).__init__(
            line,
            pos,
            "{} expected, but was '{}'".format(expected, actual)
        )
