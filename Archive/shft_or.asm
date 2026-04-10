; Demonstrate SHFT (shift left/right) and OR operations
;
; CS 2210 Computer Organization
; Clayton Cafiero <cbcafier@uvm.edu>
;
; Input:  (none -- values are hardcoded)
; Output: R3 (3 << 2 = 12), R4 (12 >> 2 = 3), R5 (12 | 3 = 15)
; Uses:   R1 (initial value), R2 (shift control)

START:
    LOADI  R1, #0x03      ; R1 = 0000 0000 0000 0011
    LOADI  R2, #0x02      ; R2 = shift amount (2)
    SHFT   R3, R1, R2     ; R3 = R1 << R2  = 0000 0000 0000 1100
    LUI    R2, #0x80      ; R2 = 0x8002: bit 15 = right, lower nibble = 2
    SHFT   R4, R3, R2     ; R4 = R3 >> 2   = 0000 0000 0000 0011
    OR     R5, R3, R4     ; R5 = R3 | R4   = 0000 0000 0000 1111
END:
    HALT
