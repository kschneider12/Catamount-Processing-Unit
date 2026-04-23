; Determine if a number is a power of two
;
; CS 2210 Computer Organization
; Clayton Cafiero <cbcafier@uvm.edu>
;
; Input:  R1 (value to test)
; Output: R4 (1 if R1 is a power of two, 0 otherwise)
; Uses:   R2 (R1 - 1), R3 (R1 & R2), R5 (constant 1)

START:
    LOADI R1, #64         ; test value
    LOADI R5, #1          ; constant 1
    LOADI R4, #0          ; assume "not power of two"
LOOP:
    BEQ   DONE            ; if n == 0, skip (0 not power of 2)
    SUB   R2, R1, R5      ; R2 = n - 1
    AND   R3, R1, R2      ; R3 = n & (n - 1)
    BEQ   ISPOW2          ; if n & (n-1) == 0, it's a power of 2
    B     DONE
ISPOW2:
    LOADI R4, #1          ; mark "yes"
DONE:
    HALT
