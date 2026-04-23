; Maximum of two signed integers
;
; CS 2210 Computer Organization
; Clayton Cafiero <cbcafier@uvm.edu>
;
; Input:  R1 (a), R2 (b) -- signed 16-bit integers
; Output: R3 (max(a, b))
; Uses:   R4 (throwaway for flag-setting)

    LOADI R1, #3          ; a (test value)
    LOADI R2, #5          ; b (test value)
    SUB   R4, R1, R2      ; a - b; sets N=1 if a < b
    BGE   A_GE_B          ; if a >= b, R1 is the max
B_LT_A:
    MOV   R3, R2          ; max = b
    B     DONE
A_GE_B:
    MOV   R3, R1          ; max = a
DONE:
    HALT
