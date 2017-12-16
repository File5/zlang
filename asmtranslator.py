#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class AsmSyntax:

    def __init__(self):
        self.next_mem = 500
        self.id_mem = {}
        self.next_label = 0

    def get_mem_for_id(self, i):
        if i in self.id_mem:
            return self.id_mem[i]
        else:
            self.id_mem[i] = self.next_mem
            self.next_mem += 1
            return self.next_mem - 1

    def get_label_for(self, target=None):
        result = "LABEL" + str(self.next_label)
        if target is not None:
            result += "_" + target
        self.next_label += 1
        return result

    def mov_constant_to(self, to, constant):
        return "RD #" + constant + "\nWR " + to

    def mov_id_to(self, to, i):
        return "RD " + self.get_mem_for_id(i) + "\nWR " + to

    def add_constant(self, constant):
        return "ADD #" + constant

    def add_id(self, i):
        return "ADD " + self.get_mem_for_id(i)

    def sub_constant(self, constant):
        return "SUB #" + constant

    def sub_id(self, i):
        return "SUB " + self.get_mem_for_id(i)

    def mul_constant(self, constant):
        return "MUL #" + constant

    def mul_id(self, i):
        return "MUL " + self.get_mem_for_id(i)

    def div_constant(self, constant):
        return "DIV #" + constant

    def div_id(self, i):
        return "DIV " + self.get_mem_for_id(i)

    def in_(self):
        return "IN"

    def out_(self):
        return "OUT"

    def nop(self):
        return "NOP"

    def hlt(self):
        return "HLT"

    def make_label(self, label):
        return label + ":"

    def jmp_label(self, label):
        return "JMP " + label

    def jz_label(self, label):
        return "JZ " + label

    def jnz_label(self, label):
        return "JNZ " + label


class AsmCommand:

    def __init__(self, cmd):
        self.cmd = cmd

    def __str__(self):
        return self.cmd


class AsmLabel:

    def __init__(self, label):
        self.label = label

    def __repr__(self):
        return self.label


class FutureLabel:

    def __init__(self):
        self.label = None

    def set_label(self, label):
        self.label = label

    def get_label(self):
        return self.label

    def __repr__(self):
        if self.label is None:
            return "undefined"
        else:
            return str(self.label)

    def __str__(self):
        return repr(self)


class SwitchToken:

    def __init__(self, insert_pos):
        self.insert_pos = insert_pos
        self.end_label = FutureLabel()

    def __repr__(self):
        return "<switch insert_pos={} end={}>".format(self.insert_pos, self.end_label)

    def get_insert_pos(self):
        return self.insert_pos

    def get_end_label(self):
        return self.end_label


class JmpToken:

    def __init__(self, label):
        self.label = label

    def __repr__(self):
        return "JMP {}".format(self.label)


class CmpToken:

    def __init__(self, constant, je_label):
        self.constant = constant
        self.je_label = je_label

    def __repr__(self):
        return "<CMP {}, JE {}>".format(self.constant, self.je_label)


class AsmTranslator:

    def __init__(self, non_operators):
        self.non_operators = non_operators
        self.input_priority = {
            "=" : 100,
            "(" : 100,
            "switch" : 100,
            "case" : 1,
            "for" : 100,
            "while" : 100,
            "readln" : 100,
            "writeln" : 100,
            "{" : 1,
            ":" : 1,
            "do" : 1,
            ")" : 1,
            "loop" : 1,
            ";" : 1,
            "}" : 1,
            "<" : 10,
            "<=" : 10,
            ">" : 10,
            ">=" : 10,
            "==" : 10,
            "!=" : 10,
            "+" : 11,
            "-" : 11,
            "*" : 12,
            "/" : 12,
        }
        self.op_stack_priority = {
            "=" : 0,
            "(" : 0,
            "{" : 0,
            "switch" : 0,
            "case" : 0,
            "for" : 0,
            "while" : 0,
            "readln": 0,
            "writeln": 0,
            "do" : 0,
            "<" : 10,
            "<=" : 10,
            ">" : 10,
            ">=" : 10,
            "==" : 10,
            "!=" : 10,
            "+" : 11,
            "-" : 11,
            "*" : 12,
            "/" : 12,
        }
        self.asm_syntax = AsmSyntax()

    def to_asm(self, token_list):
        result_list = []
        op_stack = []

        def pop_until(x, extra_pop=True):
            while len(op_stack) > 0 and op_stack[-1] != x:
                result_list.append(op_stack.pop())
            if extra_pop and len(op_stack) > 0:
                op_stack.pop()

        def pop_until_any_of(*x, extra_pop=True):
            while len(op_stack) > 0 and op_stack[-1] not in x:
                result_list.append(op_stack.pop())
            if extra_pop and len(op_stack) > 0:
                op_stack.pop()

        while len(token_list) > 0:
            print("STEP", result_list, op_stack, token_list[0].value, sep='\n')
            current_token = token_list[0]
            current_value = current_token.value

            # IDs, CONSTANTs
            if current_value not in self.input_priority:
                result_list.append(current_value)
                token_list.pop(0)

            elif current_value in (")", "loop", ";", "}", "end", ":", "case"):
                if current_value == ")":
                    pop_until("(")
                    token_list.pop(0)
                elif current_value == "loop":
                    pop_until("while", False)
                    result_list.append(op_stack.pop())
                    token_list.pop(0)
                elif current_value == ";" or current_value == "end":
                    pop_until_any_of("for", "while", "switch", "case", "=", extra_pop=False)
                    if len(op_stack) > 0:
                        result_list.append(op_stack.pop())
                    token_list.pop(0)
                elif current_value == "case":
                    token_list.pop(0) # case
                    # find nearest "<switch>"
                    s = None
                    for t in reversed(op_stack):
                        if type(t) is SwitchToken:
                            s = t
                            break
                    pop_until(s, extra_pop=False)
                    result_list.append(JmpToken(s.get_end_label()))
                    case_label = self.asm_syntax.get_label_for("case")
                    constant = token_list.pop(0).value
                    result_list.append(AsmLabel(case_label))
                    result_list.insert(s.get_insert_pos(), CmpToken(constant, case_label))

                elif current_value == "}":
                    # find nearest "<switch>"
                    s = None
                    for t in reversed(op_stack):
                        if type(t) is SwitchToken:
                            s = t
                            break
                    if s is not None:
                        pop_until_any_of(s, "{", extra_pop=False)

                        if len(op_stack) > 0 and op_stack[-1] == "{":
                            op_stack.pop()
                        else:
                            # finish "<switch>"
                            end_label = AsmLabel(self.asm_syntax.get_label_for("switch_end"))
                            result_list.append(end_label)
                            s.get_end_label().set_label(end_label)

                    else:
                        # no "<switch>"
                        pop_until("{")
                    token_list.pop(0)
                elif current_value == ":":
                    token_list.pop(0)

            else:
                current_priority = self.input_priority[current_value]

                if len(op_stack) > 0:
                    last_op = op_stack[-1]
                    stack_priority = -1
                    if type(last_op) is str:
                        stack_priority = self.op_stack_priority[last_op]

                    if current_priority > stack_priority:
                        token_list.pop(0)
                        op_stack.append(current_value)

                    else:
                        result_list.append(op_stack.pop())

                else:
                    token_list.pop(0)
                    op_stack.append(current_value)

            if op_stack[-2:] == ["switch", "{"]:
                op_stack.pop() # {
                op_stack.pop() # switch
                op_stack.append(SwitchToken(len(result_list)))

        print(result_list, op_stack, list(map(lambda x: x.value, token_list)), sep='\n')
        return result_list
