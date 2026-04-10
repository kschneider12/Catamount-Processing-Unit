; Multiply by powers of two (loop)
;
; CS 2210 Computer Organization
; Clayton Cafiero <cbcafier@uvm.edu>
;
; Input:  R1 (operand), R3 (exponent limit -- stores exponents 1 through R3-1)
; Output: M[0..R3-2] (R1 * 2^k for k = 1 to R3-1)
; Uses:   R0 (memory address), R2 (exponent), R4 (shifted result),
;         R5 (throwaway for flag-setting)

START:
    LOADI R0, #0         ; memory address
    LOADI R1, #5         ; operand
    LOADI R2, #1         ; exponent
    LOADI R3, #10        ; max iters + 1
LOOP:
    SHFT R4, R1, R2
    STORE R4, [R0 + #0]
    ADDI R0, R0, #1      ; increment address
    ADDI R2, R2, #1      ; increment exponent
    SUB R5, R2, R3       ; exponent - limit
    BLT LOOP             ; if exponent < limit, continue loop
DONE:
    HALT
