; Stores values 1, 2, ..., N to memory[0..N-1], then finds
; the maximum using LOAD in a loop. Result (max) is left in R3.
;
; Input:  R2 (N, number of elements)
; Output: R3 (maximum value)
; Uses:   R0 (base address), R1 (current element), R4 (loop counter),
;         R5 (throwaway for flag-setting), R6 (memory address)

; Initial values stored in registers

    LOADI R0, #0          ; base address
    LOADI R1, #1          ; first value = 1
    LOADI R2, #8          ; N = 8
    LOADI R4, #0          ; counter = 0
    MOV   R6, R0          ; store address = base

SETUP:
    ; Here we add consecutive natural numbers into consecutive
    ; memory addresses in a loop.
    STORE R1, [R6 + #0]   ; M[R6] = value
    ADDI R4, R4, #1       ; Nico: Increment Counter
    SUB R5, R4, R2        ; Nico: set flags
    BLT   SETUP           ; if counter < N, continue

    ; reset counter
    ; reset address to base
    LOAD  R3, [R6 + #0]   ; max = M[0]  (seed with first element)
    ; advance past first element (just increment)
    LOADI R4, #1          ; counter = 1  (first element already processed)

; Complete the loop which finds the largest value and stores
; the result in R3. Do this work in the loop. Even though we
; know the largest value, show that you can write the assembly
; code to do this.

DONE:
    HALT