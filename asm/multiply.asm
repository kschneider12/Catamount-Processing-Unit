; Integer multiplication via repeated addition
;
; CS 2210 Computer Organization
; Clayton Cafiero <cbcafier@uvm.edu>
;
; Computes a * b by adding a to itself b times.
; Assumes b >= 0. Result is undefined if a * b overflows 16 bits.
;
; Input:  R1 (a, multiplicand), R2 (b, multiplier, non-negative)
; Output: R3 (a * b)
; Uses:   R4 (loop counter), R5 (throwaway for flag-setting)

    LOADI R1, #6          ; a (test value)
    LOADI R2, #7          ; b (test value)
    LOADI R3, #0          ; product = 0
    LOADI R4, #0          ; counter = 0
LOOP:
    SUB   R5, R4, R2      ; counter - b
    BGE   DONE            ; if counter >= b, exit
    ADD   R3, R3, R1      ; product += a
    ADDI  R4, R4, #1      ; counter++
    B     LOOP
DONE:
    HALT
