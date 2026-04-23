; Call and return
;
; CS 2210 Computer Organization
; Clayton Cafiero <cbcafier@uvm.edu>
;
; Input:  (none)
; Output: (none)
; Uses:   stack (return address saved/restored by CALL/RET)

START:
    CALL FOO
    HALT
FOO:
    RET
