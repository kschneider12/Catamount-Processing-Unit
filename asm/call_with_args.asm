; Input:  R1 (first value), R2 (second value), R5 (third value)
; Output: R3 (maximum of three values)
; Uses:   R4 (throwaway for flag-setting in MAX)
;
; MAX convention: arguments in R1, R2 (read only); result in R3; R5 untouched.

    LOADI R1, #3          ; first value (example)
    LOADI R2, #7          ; second value (example)
    LOADI R5, #5          ; third value (example)

    CALL  MAX             ; R3 = max(first, second)
    MOV   R1, R3          ; R1 = max so far
    MOV   R2, R5          ; R2 = third value
    CALL  MAX             ; R3 = max(max so far, third)
    HALT

MAX:
    ; Add appropriate comparison here
    SUB R4, R1, R2
    BGE A_GE_B          ; if a >= b, pick a

B_LT_A:
    ; Add appropriate MOV here
    MOV R3, R2
    RET
A_GE_B:
    ; Add appropriate MOV here
    MOV R3, R1
    RET