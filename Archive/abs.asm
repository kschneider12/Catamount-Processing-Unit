; Compute the absolute value of a signed integer
;
; CS 2210 Computer Organization
; Clayton Cafiero <cbcafier@uvm.edu>
;
; Input:  R1 (signed 16-bit integer)
; Output: R1 (|R1|, non-negative)
; Uses:   R0 (zero constant), R2 (throwaway for flag-setting)

    LOADI R0, #0          ; zero constant (also used for negation)
    LOADI R1, #-5         ; test value (sign-extended to 16 bits)
    SUB   R2, R1, R0      ; R2 = R1 - 0; sets N=1 if R1 < 0
    BGE   DONE            ; if R1 >= 0, nothing to do
    SUB   R1, R0, R1      ; R1 = 0 - R1  (negate)
DONE:
    HALT
