;Count the number of set bits in a 16-bit word.
;Example: If we have 0010 0011 1111 0100 there are eight bits set.
;If we have 0000 0000 0000 0000 there are zero bits set.

; Input:  R1 (16-bit value)
; Output: R2 (number of set bits, 0-16)
; Uses:   R3 (loop counter), R4 (limit = 16), R5 (LSB mask),
;         R6 (shift control), R7 (throwaway for AND / flag-setting)
;
; Strategy: test LSB, shift right by 1, repeat 16 times.

    LOADI R1, #0x0F       ; test value (4 set bits)
    LOADI R2, #0b0          ; count = 0
    LOADI R3, #0b0
    LOADI R4, #0x0F
    LOADI R5, #0b1
    LOADI R6, #0x8001       ; This could be wrong

LOOP:
    ; complete loop
    AND R7, R2, R5        ; Check if bit set
    ADD R2, R2, R7        ; Add to accumulator
    SHFT R2, R6           ; shift right
    SUB R7, R3, R4        ; set ALU flag
    BLT   LOOP            ; if counter < 16, continue
DONE:
    HALT
