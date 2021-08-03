# zlang
Translator from ZLang to ASM (Course Work)

## Overview

ZLang program example (`main.zl`).
```
program
var
    a123a, b123b : integer;
    c123c, d123d : real;
    e123e, f123f : boolean;
begin
    a123a = 0;
    b123b = 1;
    switch a123a + 10 {
        case 10:
            {
                a123a = 10;
                b123b = 10
            }
        case 11:
            {
                a123a = 11;
                b123b = 11
            }
    }
end.
```

<details>
<summary>The output of lexical analyzer</summary>

```
1. Constants: ['0', '1', '10', '11']
2. Keywords: ['program', 'var', 'begin', 'end', 'integer', 'real', 'boolean',
'let', 'switch', 'case', 'for', 'to', 'do', 'while', 'loop', 'readln',
'writeln', 'true', 'false']
3. Identifiers: ['a123a', 'b123b', 'c123c', 'd123d', 'e123e', 'f123f']
4. Delimiters: [',', ':', ';', '=', '+', '{', '}', '.']
program var a123a , b123b : integer ; c123c , d123d : real ; e123e , f123f :
boolean ; begin a123a = 0 ; b123b = 1 ; switch a123a + 10 { case 10 : { a123a =
10 ; b123b = 10 } case 11 : { a123a = 11 ; b123b = 11 } } end .
(2, 0), (2, 1), (3, 0), (4, 0), (3, 1), (4, 1), (2, 4), (4, 2), (3, 2), (4, 0),
(3, 3), (4, 1), (2, 5), (4, 2), (3, 4), (4, 0), (3, 5), (4, 1), (2, 6), (4, 2),
(2, 2), (3, 0), (4, 3), (1, 0), (4, 2), (3, 1), (4, 3), (1, 1), (4, 2), (2, 8),
(3, 0), (4, 4), (1, 2), (4, 5), (2, 9), (1, 2), (4, 1), (4, 5), (3, 0), (4, 3),
(1, 2), (4, 2), (3, 1), (4, 3), (1, 2), (4, 6), (2, 9), (1, 3), (4, 1), (4, 5),
(3, 0), (4, 3), (1, 3), (4, 2), (3, 1), (4, 3), (1, 3), (4, 6), (4, 6), (2, 3),
(4, 7)
```
</details>

<details>
<summary>The output of syntax analyzer</summary>

```
S [
  program
  var
  S [
    S [
      S [
        a123a
        ,
        S [
          b123b
        ]
      ]
      :
      S [
        integer
      ]
    ]
    ;
    S [
      S [
        S [
          c123c
          ,
          S [
            d123d
          ]
        ]
        :
        S [
          real
        ]
      ]
      ;
      S [
        S [
          S [
            e123e
            ,
            S [
              f123f
            ]
          ]
          :
          S [
            boolean
          ]
        ]
        ;
      ]
    ]
  ]
  begin
  S [
    S [
      a123a
      =
      S [
        0
      ]
    ]
    ;
    S [
      S [
        b123b
        =
        S [
          1
        ]
      ]
      ;
      S [
        switch
        S [
          S [
            a123a
          ]
          +
          S [
            10
          ]
        ]
        {
        S [
          S [
            case
            S [
              10
              :
              S [
                {
                S [
                  S [
                    a123a
                    =
                    S [
                      10
                    ]
                  ]
                  ;
                  S [
                    b123b
                    =
                    S [
                      10
                    ]
                  ]
                ]
                }
              ]
            ]
          ]
          case
          S [
            11
            :
            S [
              {
              S [
                S [
                  a123a
                  =
                  S [
                    11
                  ]
                ]
                ;
                S [
                  b123b
                  =
                  S [
                    11
                  ]
                ]
              ]
              }
            ]
          ]
        ]
        }
      ]
    ]
  ]
  end
  .
]
```
</details>

Generated assembly code can be found in `main.asm`.

## Syntax

The syntax of the program written in ZLang can be defined as follows.

```
PROGRAM ::= program var TYPE_DEFINITION_N begin OPERATOR_N end .
TYPE_DEFINITION_N ::= TYPE_DEFINITION ; | TYPE_DEFINITION ; TYPE_DEFINITION_N
TYPE_DEFINITION ::= ID_N : TYPE
ID_N ::= ID | ID , ID_N
TYPE ::= integer | real | boolean
OPERATOR_N ::= OPERATOR | OPERATOR ; OPERATOR_N
OPERATOR ::= COMPLEX_OPERATOR | ASSIGNMENT_OPERATOR | SWITCH_OPERATOR | FOR_OPERATOR | WHILE_OPERATOR | INPUT_OPERATOR | OUTPUT_OPERATOR
COMPLEX_OPERATOR ::= { OPERATOR_N }
ASSIGNMENT_OPERATOR ::= ID = EXPRESSION | let ID = EXPRESSION
SWITCH_OPERATOR ::= switch EXPRESSION { CASE_N }
CASE_N ::= case CASE_CONTENT | CASE_N case CASE_CONTENT
CASE_CONTENT ::= CONSTANT : OPERATOR
FOR_OPERATOR ::= for ASSIGNMENT_OPERATOR to EXPRESSION do OPERATOR
WHILE_OPERATOR ::= do while EXPRESSION ; OPERATOR loop
INPUT_OPERATOR ::= readln ID_N
OUTPUT_OPERATOR ::= writeln EXPRESSION | OUTPUT_OPERATOR \ EXPRESSION
EXPRESSION ::= A < A | A <= A | A > A | A >= A | A == A | A != A | A
A ::= A + T | A - T | T
T ::= T * P | T / P | P
P ::= ( A ) | ID | CONSTANT
```

The program is compiled into assembly language of computer model (ISBN 5-94157-719-2, p. 235)
