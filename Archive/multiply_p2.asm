; Multiply by powers of two
;
; CS 2210 Computer Organization
; Clayton Cafiero <cbcafier@uvm.edu>
;
; Input:  R0 (operand)
; Output: R2 (operand * 2^1), R3 (operand * 2^2), R4 (operand * 2^3),
;         R5 (operand * 2^4), R6 (operand * 2^5), R7 (operand * 2^6)
; Uses:   R1 (shift amount)

LOADI R0, #0x03     ; operand (3)
LOADI R1, #0x01     ; start with 1
SHFT R2, R0, R1  ; R2 <-- 3 x 2**1 (6)
ADDI R1, R1, #1  ; increment shift amount by 1
SHFT R3, R0, R1  ; R3 <-- 3 x 2**2 (12)
ADDI R1, R1, #1  ; increment shift amount by 1
SHFT R4, R0, R1  ; R4 <-- 3 x 2**3 (24)
ADDI R1, R1, #1  ; increment shift amount by 1
SHFT R5, R0, R1  ; R5 <-- 3 x 2**4 (24)
ADDI R1, R1, #1  ; increment shift amount by 1
SHFT R6, R0, R1  ; R6 <-- 3 x 2**5 (96)
ADDI R1, R1, #1  ; increment shift amount by 1
SHFT R7, R0, R1  ; R7 <-- 3 x 2**7 (192)
HALT
