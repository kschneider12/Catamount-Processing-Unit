; Check to see if "safe" to add two positive operands by OR.
; If safe, apply OR and store result in R2.
; If not safe, store 0 in R2.
;
; CS 2210 Computer Organization
; Clayton Cafiero <cbcafier@uvm.edu>
;
; Input:  R0 (a), R1 (b)
; Output: R2 (a | b if no overlapping bits, 0 otherwise)
; Uses:   R3 (AND result / throwaway for flag-setting)

LOADI R0, #0x2A   ; whatever
LOADI R1, #0x55   ; whatever
CHECK_SAFE:
    AND R3, R0, R1
    BNE NO_CAN_DO
    OR R2, R0, R1
    B DONE
NO_CAN_DO:
    LOADI R2, #0
DONE:
    HALT
