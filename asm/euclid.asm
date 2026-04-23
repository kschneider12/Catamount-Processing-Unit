; Euclid's GCD algorithm (repeated subtraction)
;
; CS 2210 Computer Organization
; Clayton Cafiero <cbcafier@uvm.edu>
;
; Input:  R5 (a, positive integer), R6 (b, positive integer)
; Output: M[0] (GCD of a and b)
; Uses:   R0 (base memory address), R7 (throwaway for flag-setting)

START:
    LOADI R0, #0          ; base memory address
    LOADI R5, #0x2A       ; a = 42 (test case)
    LOADI R6, #0x5A       ; b = 90
    CALL  GCD
    HALT

GCD:
    SUB R7, R5, R6        ; R7 = a - b (sets flags)
    BEQ DONE              ; if a == b, exit
    BLT B_GT_A            ; if a < b (N=1), branch
A_GE_B:
    SUB R5, R5, R6        ; a = a - b
    B GCD
B_GT_A:
    SUB R6, R6, R5        ; b = b - a
    B GCD
DONE:
    STORE R5, [R0 + #0]   ; write GCD to memory at address 0
    RET
