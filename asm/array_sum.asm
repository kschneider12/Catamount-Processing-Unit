; Sum of an integer array stored in memory
;
; CS 2210 Computer Organization
; Clayton Cafiero <cbcafier@uvm.edu>
;
; Stores values 1, 2, ..., N to memory[0..N-1], then sums
; them using LOAD in a loop. Result (sum) is left in R3.
;
; Input:  R2 (N, number of elements)
; Output: R3 (sum of elements 1..N)
; Uses:   R0 (base address), R1 (current element), R4 (loop counter),
;         R5 (throwaway for flag-setting), R6 (memory address)

    LOADI R0, #0          ; base address
    LOADI R1, #1          ; first value = 1
    LOADI R2, #8          ; N = 8
    LOADI R4, #0          ; counter = 0
    MOV   R6, R0          ; store address = base

SETUP:
    STORE R1, [R6 + #0]   ; M[R6] = value
    ADDI  R1, R1, #1      ; value++
    ADDI  R6, R6, #1      ; addr++
    ADDI  R4, R4, #1      ; counter++
    SUB   R5, R4, R2      ; counter - N
    BLT   SETUP           ; if counter < N, continue

    LOADI R3, #0          ; sum = 0
    LOADI R4, #0          ; reset counter
    MOV   R6, R0          ; reset load address to base

SUM:
    LOAD  R1, [R6 + #0]   ; R1 = M[R6]
    ADD   R3, R3, R1      ; sum += R1
    ADDI  R6, R6, #1      ; addr++
    ADDI  R4, R4, #1      ; counter++
    SUB   R5, R4, R2      ; counter - N
    BLT   SUM             ; if counter < N, continue

DONE:
    HALT
