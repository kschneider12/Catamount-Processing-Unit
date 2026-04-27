;Count the number of set bits in a 16-bit word.
;Example: If we have 0010 0011 1111 0100 there are eight bits set.
;If we have 0000 0000 0000 0000 there are zero bits set.

; Input:  R1 (16-bit value)
; Output: R2 (number of set bits, 0-16)
; Uses:   R3 (loop counter), R4 (limit = 16), R5 (LSB mask),
;         R6 (shift control), R7 (throwaway for AND / flag-setting)
;
; Strategy: test LSB, shift right by 1, repeat 16 times.

    LOADI R1, #0x0F         ; test value (4 set bits)
    LOADI R2, #0b0          ; accumulator = 0
    LOADI R3, #0b0          ; loop counter = 0
    LOADI R4, #0x10         ; 16 bit limit (MAYBE)
    LOADI R5, #0b1          ; single bit mask

    LOADI   R6, #0x01       ; shift control (1000 0000 0000 0001)
    LUI     R6, #0x80

LOOP:
                          ; complete loop
    ADDI R3, R3, #1       ; Add 1 to R3
    AND R7, R1, R5        ; Store R1 and R5 in R7
    ADD R2, R2, R7        ; Add R7 to R2 (If bit set, add to R2)
    SHFT R1, R1, R6       ; shift R1 by R6 and store in R1
    SUB R7, R3, R4        ; Sub R3 - R4, store in R7        loop counter - 16 bit limit
    BLT   LOOP            ; if counter < 16, continue
DONE:
    HALT
