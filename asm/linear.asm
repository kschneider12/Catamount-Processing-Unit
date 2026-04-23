; Just a linear sequence of instructions.
; No jumps, no branching.
;
; CS 2210 Computer Organization
; Clayton Cafiero <cbcafier@uvm.edu>
;
; Input:  (none)
; Output: R3 = 3, R4 = 4, R5 = 14
; Uses:   R1, R2

LOADI R1, #0x01
LOADI R2, #0x02
ADD R3, R1, R2      ; r3 <-- 1 + 2
ADD R4, R3, R1      ; r4 <-- 3 + 1
ADDI R5, R4 #0x0A   ; r5 <-- 4 + 10
HALT
