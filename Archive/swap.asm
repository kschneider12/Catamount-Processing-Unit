; Swap two values in memory using a temporary register
;
; CS 2210 Computer Organization
; Clayton Cafiero <cbcafier@uvm.edu>
;
; Stores two values to memory[0] and memory[1], then swaps them.
; Without the temporary register, one value would be overwritten
; before it could be saved.
;
; Input:  R2 (value for M[0]), R3 (value for M[1])
; Output: M[0] (original M[1]), M[1] (original M[0])
; Uses:   R0 (address 0), R1 (address 1)

    LOADI R0, #0          ; address 0
    LOADI R1, #1          ; address 1
    LOADI R2, #42         ; initial value for M[0]
    LOADI R3, #99         ; initial value for M[1]
    STORE R2, [R0 + #0]   ; M[0] = 42
    STORE R3, [R1 + #0]   ; M[1] = 99

    LOAD  R2, [R0 + #0]   ; R2 = M[0]  (load before overwriting)
    LOAD  R3, [R1 + #0]   ; R3 = M[1]
    STORE R3, [R0 + #0]   ; M[0] = old M[1]
    STORE R2, [R1 + #0]   ; M[1] = old M[0]
    HALT
