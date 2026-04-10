; Nested call
;
; CS 2210 Computer Organization
; Clayton Cafiero <cbcafier@uvm.edu>
;
; Input:  (none)
; Output: (none)
; Uses:   stack (return addresses for two levels of nested calls)

CALL F
HALT
F:
CALL G
RET
G:
RET
