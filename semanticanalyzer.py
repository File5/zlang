#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from exceptions import UndefinedIdentifierError


class SemanticAnalyzer:

    def __init__(self, get_node_children=lambda x: None, get_identifiers_def=lambda x: None, get_identifiers_used=lambda x: None):
        self.defined_identifiers = []
        self.get_identifiers_def = get_identifiers_def
        self.get_identifiers_used = get_identifiers_used
        self.get_node_children = get_node_children

    def parse_tree(self, tree):
        nodes_queue = [tree]

        while len(nodes_queue) > 0:
            current_node = nodes_queue.pop(0)

            current_id_defs = self.get_identifiers_def(current_node)
            current_id_used = self.get_identifiers_used(current_node)

            if current_id_used is not None:
                for identifier in current_id_used:
                    if identifier not in self.defined_identifiers:
                        raise UndefinedIdentifierError(identifier, *current_node.get_line_pos())

            if current_id_defs is not None:
                self.defined_identifiers += current_id_defs

            next_nodes = self.get_node_children(current_node)

            if next_nodes is not None:
                nodes_queue += next_nodes

        return True
