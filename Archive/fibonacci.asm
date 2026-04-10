; Iterative Fibonacci sequence
;
; CS 2210 Computer Organization
; Clayton Cafiero <cbcafier@uvm.edu>
;
; Stores the first N Fibonacci numbers to consecutive memory addresses
; starting at address 0: F(1)=1, F(2)=1, F(3)=2, F(4)=3, ...
; where N = R4 + 2  (R4 additional terms after F(1) and F(2)).
;
; Input:  R4 (number of additional terms after F(1) and F(2))
; Output: M[0..N-1] (first N Fibonacci numbers)
; Uses:   R0 (write address), R1 (a), R2 (b), R3 (loop counter),
;         R5 (next term), R6 (throwaway for flag-setting)

    LOADI R0, #0          ; start at address 0
    LOADI R1, #1          ; a = F(1) = 1
    LOADI R2, #1          ; b = F(2) = 1
    LOADI R3, #0          ; counter = 0
    LOADI R4, #8          ; 8 more terms after F(1) and F(2), for 10 total
    STORE R1, [R0 + #0]   ; M[0] = F(1)
    ADDI  R0, R0, #1      ; advance address
    STORE R2, [R0 + #0]   ; M[1] = F(2)
    ADDI  R0, R0, #1      ; advance address
LOOP:
    ADD   R5, R1, R2      ; next = a + b
    MOV   R1, R2          ; a = b
    MOV   R2, R5          ; b = next
    STORE R5, [R0 + #0]   ; store next term
    ADDI  R0, R0, #1      ; advance address
    ADDI  R3, R3, #1      ; increment counter
    SUB   R6, R3, R4      ; counter - limit
    BLT   LOOP            ; if counter < limit, continue
DONE:
    HALT
