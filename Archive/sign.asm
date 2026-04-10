; Sign function: returns -1, 0, or 1
;
; CS 2210 Computer Organization
; Clayton Cafiero <cbcafier@uvm.edu>
;
; Input:  R1 (signed 16-bit integer)
; Output: R2 (-1 if R1 < 0, 0 if R1 == 0, 1 if R1 > 0)
; Uses:   R0 (zero constant), R3 (throwaway for flag-setting)

    LOADI R0, #0          ; zero constant
    LOADI R1, #-5         ; test value
    SUB   R3, R1, R0      ; R1 - 0; sets N=1 if R1 < 0, Z=1 if R1 == 0
    BLT   NEGATIVE        ; if R1 < 0, branch
    BEQ   ZERO            ; if R1 == 0, branch
POSITIVE:
    LOADI R2, #1          ; sign = +1
    B     DONE
NEGATIVE:
    LOADI R2, #-1         ; sign = -1
    B     DONE
ZERO:
    LOADI R2, #0          ; sign = 0
DONE:
    HALT
