#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class AsmSyntax:

    def __init__(self):
        self.tmp_mem = 499
        self.next_mem = 500
        self.id_mem = {}
        self.next_label = 0

    def get_tmp_mem(self):
        return self.tmp_mem

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
        return "RD #" + str(constant) + "\nWR " + str(to)

    def inc_mem(self, mem):
        return "RD " + str(mem) + "\n" + self.add_constant(1) + "\nWR " + str(mem)

    def mov_id_to(self, to, i):
        return "RD " + str(self.get_mem_for_id(i)) + "\nWR " + str(to)

    def add_constant(self, constant):
        return "ADD #" + str(constant)

    def add_mem(self, mem):
        return "ADD " + str(mem)

    def add_id(self, i):
        return "ADD " + str(self.get_mem_for_id(i))

    def sub_constant(self, constant):
        return "SUB #" + str(constant)

    def sub_mem(self, mem):
        return "SUB " + str(mem)

    def sub_id(self, i):
        return "SUB " + str(self.get_mem_for_id(i))

    def mul_constant(self, constant):
        return "MUL #" + str(constant)

    def mul_mem(self, mem):
        return "MUL " + str(mem)

    def mul_id(self, i):
        return "MUL " + str(self.get_mem_for_id(i))

    def div_constant(self, constant):
        return "DIV #" + str(constant)

    def div_mem(self, mem):
        return "DIV " + str(mem)

    def div_id(self, i):
        return "DIV " + str(self.get_mem_for_id(i))

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

    def rd_constant(self, constant):
        return "RD #" + str(constant)

    def rd_mem(self, mem):
        return "RD " + str(mem)

    def wr_mem(self, mem):
        return "WR " + str(mem)

    def push_constant(self, constant):
        return self.rd_constant(constant) + "\nWR R1\nPUSH R1"

    def push_mem(self, mem):
        return self.rd_mem(mem) + "\nWR R1\nPUSH R1"

    def pop(self):
        return "POP R1\nRD R1"

    def pop_mem(self, mem):
        return self.pop() + "\n" + self.wr_mem(mem)


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


class ForToken:

    def __init__(self, mem, const1, const2, for_label):
        self.mem = mem
        self.const1 = const1
        self.const2 = const2
        self.for_label = for_label
        self.end_for_label = FutureLabel()

    def __repr__(self):
        return "<for mem={} const1={} const2={}>".format(self.mem, self.const1, self.const2)

    def get_for_label(self):
        return self.for_label

    def get_mem(self):
        return self.mem

    def get_end_for_label(self):
        return self.end_for_label


class WhileToken:

    def __init__(self, while_label):
        self.while_label = while_label
        self.end_while_label = FutureLabel()

    def __repr__(self):
        return "<while>"

    def get_while_label(self):
        return self.while_label

    def get_end_while_label(self):
        return self.end_while_label


class JmpToken:

    def __init__(self, label):
        self.label = label

    def __repr__(self):
        return "JMP {}".format(self.label)


class JnzToken:

    def __init__(self, label):
        self.label = label

    def __repr__(self):
        return "JNZ {}".format(self.label)


class CmpToken:

    def __init__(self, constant, je_label):
        self.constant = constant
        self.je_label = je_label

    def __repr__(self):
        return "<CMP {}, JE {}>".format(self.constant, self.je_label)

    def __str__(self):
        return "SUB #{}\nJZ {}\nADD #{}".format(self.constant, str(self.je_label), self.constant)


class AsmTranslator:

    def __init__(self, constants, identifiers):
        self.constants = constants
        self.identifiers = identifiers
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
        poliz = self.to_poliz(token_list)
        asm_cmds = []
        current_stack = []

        def append_bin_op_to(cmd_list, op):
            op_cmd = self.asm_syntax.add_mem(self.asm_syntax.get_tmp_mem())
            if op == "-":
                op_cmd = self.asm_syntax.sub_mem(self.asm_syntax.get_tmp_mem())
            elif op == "*":
                op_cmd = self.asm_syntax.mul_mem(self.asm_syntax.get_tmp_mem())
            elif op_cmd == "/":
                op_cmd = self.asm_syntax.div_mem(self.asm_syntax.get_tmp_mem())

            for i in [
                self.asm_syntax.pop_mem(self.asm_syntax.get_tmp_mem()),
                self.asm_syntax.pop(),
                op_cmd,
                self.asm_syntax.wr_mem(self.asm_syntax.get_tmp_mem()),
                self.asm_syntax.push_mem(self.asm_syntax.get_tmp_mem())
            ]:
                cmd_list.append(i)
            current_stack.pop()
            current_stack.pop()
            current_stack.append("tmp")

        for i, cmd in enumerate(poliz):
            if cmd in self.constants:
                current_stack.append(cmd)
                asm_cmds.append(self.asm_syntax.push_constant(cmd))
            elif cmd in self.identifiers:
                current_stack.append(cmd)
                asm_cmds.append(self.asm_syntax.push_mem(self.asm_syntax.get_mem_for_id(cmd)))
            elif type(cmd) is str and cmd in "+-*/":
                append_bin_op_to(asm_cmds, cmd)
            elif cmd == "==":
                append_bin_op_to(asm_cmds, "-")
            elif cmd == "=":
                identifier = current_stack[-2]
                asm_cmds += [
                    self.asm_syntax.pop_mem(self.asm_syntax.get_tmp_mem()),
                    self.asm_syntax.pop(),
                    self.asm_syntax.rd_mem(self.asm_syntax.get_tmp_mem()),
                    self.asm_syntax.wr_mem(self.asm_syntax.get_mem_for_id(identifier))
                ]
                current_stack.pop()
                current_stack.pop()
            elif type(cmd) is FutureLabel or type(cmd) is AsmLabel:
                asm_cmds.append(str(cmd) + ":")
            elif type(cmd) is JmpToken or type(cmd) is JnzToken or type(cmd) is CmpToken:
                asm_cmds.append(str(cmd))
            elif cmd in ("true", "false"):
                constant = 0
                if cmd == "true":
                    constant = 1
                current_stack.append(constant)
                asm_cmds.append(self.asm_syntax.push_constant(constant))
            elif cmd == "let":
                continue
            elif type(cmd) is str:
                asm_cmds.append(cmd)
            else:
                print("Command not printed: ", cmd, repr(cmd))

        return asm_cmds

    def to_poliz(self, token_list):
        result_list = []
        op_stack = []

        def pop_until(x, extra_pop=True):
            while len(op_stack) > 0 and op_stack[-1] != x:
                result_list.append(op_stack.pop())
            if extra_pop and len(op_stack) > 0:
                op_stack.pop()

        def pop_until_any_of(*x, types=list(), extra_pop=True):
            while len(op_stack) > 0 and (op_stack[-1] not in x and type(op_stack[-1]) not in types):
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

            elif current_value in (")", "loop", ";", "}", "end", ":", "case", "for"):
                if current_value == ")":
                    pop_until("(")
                    token_list.pop(0)
                elif current_value == "loop":
                    pop_until_any_of([], types=[WhileToken], extra_pop=False)
                    # finish while
                    w = op_stack.pop()
                    end_while_label = AsmLabel(self.asm_syntax.get_label_for("end_while"))
                    w.get_end_while_label().set_label(end_while_label)
                    result_list.append(JmpToken(w.get_while_label()))
                    result_list.append(end_while_label)

                    token_list.pop(0)
                elif current_value == ";" or current_value == "end":
                    pop_until_any_of("while", "case", "=", types=[ForToken, SwitchToken, WhileToken], extra_pop=False)
                    if len(op_stack) > 0 and type(op_stack[-1]) is not WhileToken:
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
                elif current_value == "for":
                    for_tokens = token_list[:7]
                    token_list = token_list[7:]
                    mem = self.asm_syntax.get_mem_for_id(for_tokens[1].value)
                    const1 = for_tokens[3].value
                    const2 = for_tokens[5].value
                    for_label = AsmLabel(self.asm_syntax.get_label_for("for"))
                    f = ForToken(mem, const1, const2, for_label)
                    op_stack.append(f)
                    result_list.append(self.asm_syntax.mov_constant_to(mem, const1))
                    result_list.append(for_label)
                    result_list.append(CmpToken(const2, f.get_end_for_label()))

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
            if current_value == ";" and len(op_stack) > 0 and type(op_stack[-1]) is ForToken:
                # finish for
                f = op_stack.pop()
                end_for_label = AsmLabel(self.asm_syntax.get_label_for("end_for"))
                f.get_end_for_label().set_label(end_for_label)
                result_list.append(self.asm_syntax.inc_mem(f.get_mem()))
                result_list.append(JmpToken(f.get_for_label()))
                result_list.append(end_for_label)
            if op_stack[-2:] == ["do", "while"]:
                # before condition
                op_stack.pop()  # while
                op_stack.pop()  # do
                while_label = AsmLabel(self.asm_syntax.get_label_for("while"))
                result_list.append(while_label)
                op_stack.append(WhileToken(while_label))

            if len(op_stack) > 0 and type(op_stack[-1]) is WhileToken and current_value == ";":
                # after condition
                # find nearest "<while>"
                w = None
                for t in reversed(op_stack):
                    if type(t) is WhileToken:
                        w = t
                        break
                result_list.append(JnzToken(w.get_end_while_label()))

        print(result_list, op_stack, list(map(lambda x: x.value, token_list)), sep='\n')
        return result_list
