RD 500
WR R1
PUSH R1
RD #0
WR R1
PUSH R1
POP R1
RD R1
WR 499
POP R1
RD R1
RD 499
WR 500
RD 501
WR R1
PUSH R1
RD #1
WR R1
PUSH R1
POP R1
RD R1
WR 499
POP R1
RD R1
RD 499
WR 501
RD 500
WR R1
PUSH R1
RD #10
WR R1
PUSH R1
POP R1
RD R1
WR 499
POP R1
RD R1
ADD 499
WR 499
RD 499
WR R1
PUSH R1
POP R1
RD R1
SUB #11
JZ LABEL1_case
ADD #11
SUB #10
JZ LABEL0_case
ADD #10
JMP LABEL2_switch_end
LABEL0_case:
RD 500
WR R1
PUSH R1
RD #10
WR R1
PUSH R1
POP R1
RD R1
WR 499
POP R1
RD R1
RD 499
WR 500
RD 501
WR R1
PUSH R1
RD #10
WR R1
PUSH R1
POP R1
RD R1
WR 499
POP R1
RD R1
RD 499
WR 501
JMP LABEL2_switch_end
LABEL1_case:
RD 500
WR R1
PUSH R1
RD #11
WR R1
PUSH R1
POP R1
RD R1
WR 499
POP R1
RD R1
RD 499
WR 500
RD 501
WR R1
PUSH R1
RD #11
WR R1
PUSH R1
POP R1
RD R1
WR 499
POP R1
RD R1
RD 499
WR 501
LABEL2_switch_end:
HLT
