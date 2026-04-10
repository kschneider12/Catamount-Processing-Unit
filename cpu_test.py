"""
Integration tests for the CPU
Includes complete fetch-decode-execute

CS 2210 Computer Organization
Clayton Cafiero <cbcafier@uvm.edu>
"""

import pytest

from alu import N_FLAG, Z_FLAG, Alu
from assembler import assemble
from constants import STACK_TOP
from cpu import Cpu, make_cpu
from instruction_set import Instruction
from memory import DataMemory, InstructionMemory
from register_file import RegisterFile


def test_instantiation_without_prog():
    """
    Ensure constructor works as intended
    """
    alu = Alu()
    d_mem = DataMemory()
    i_mem = InstructionMemory()
    regs = RegisterFile()
    c = Cpu(alu=alu, d_mem=d_mem, i_mem=i_mem, regs=regs)
    assert c.running
    assert c.ir == 0
    assert c.sp == STACK_TOP
    assert c.pc == 0
    assert c.decoded == Instruction()


def test_load_program_after_instantiation():
    """
    Ensure we can load a program (once) after instantiation
    """
    alu = Alu()
    d_mem = DataMemory()
    i_mem = InstructionMemory()
    regs = RegisterFile()
    c = Cpu(alu=alu, d_mem=d_mem, i_mem=i_mem, regs=regs)
    prog = [0x1202, 0x1404, 0x6650, 0x68C8, 0x5B0A, 0x0000]
    c.load_program(prog)
    for i in prog:
        c.tick()
        assert int(c.decoded.raw_hex, 16) == i


def test_make_cpu():
    """
    Ensure `make_cpu` helper correctly constructs CPU
    """
    c = make_cpu()
    assert c.running
    assert c.ir == 0
    assert c.sp == STACK_TOP
    assert c.pc == 0
    assert c.decoded == Instruction()


def test_linear_fetch():
    """
    Ensure fetch correctly increments PC and gets correct instructions
    (this without branching / jumps)
    """
    # From linear.asm (no branches, no jumps)
    prog = [0x1202, 0x1404, 0x6650, 0x68C8, 0x5B0A, 0x0000]
    c = make_cpu(prog)
    assert c.pc == 0
    for i, instruction in enumerate(prog, 1):
        c._fetch()  # OK to access in tests
        assert c.ir == instruction
        assert c.pc == i


def test_decode():
    """
    Ensure correct decoding on fetch
    """
    # From linear.asm (no branches, no jumps)
    prog = [0x1202, 0x1404, 0x6650, 0x68C8, 0x5B0A, 0x0000]
    mnems = ["LOADI", "LOADI", "ADD", "ADD", "ADDI", "HALT"]
    c = make_cpu(prog)
    for i, _ in enumerate(prog):
        c._fetch()  # OK to access in tests
        c._decode()  # OK to access in tests
        assert isinstance(c.decoded, Instruction)
        assert c.decoded.mnem == mnems[i]


def test_bne_forward_label():
    """
    Ensure BNE branches correctly on forward label
    """
    prog = assemble(
        [
            "BNE SKIP",  # should branch if Z==0
            "LOADI R0, #99",  # this should be skipped
            "SKIP:",
            "HALT",
        ]
    )
    c = make_cpu(prog)
    c._alu._flags = 0b0000  # simulate ALU flags from prior op
    c.tick()  # execute branch
    old_flags = c._alu._flags  # OK to access in tests
    assert c.pc == 2  # PC jumped past LOADI to HALT
    assert old_flags == c._alu._flags  # flags unchanged on branch
    c.tick()
    assert c.decoded.mnem == "HALT"


def test_bne_backward_label():
    """
    Ensure BNE branches correctly on backward label
    """
    prog = assemble(
        [
            "LOADI R1 #2",
            "LOADI R2 #1",
            "LOOP:",
            "SUB R1, R2, R1",
            "BNE LOOP",
            "HALT",
        ]
    )
    c = make_cpu(prog)
    c.tick()  # LOADI
    c.tick()  # LOADI
    c.tick()  # SUB
    old_flags = c._alu._flags  # OK to access in tests
    c.tick()
    assert c.pc == 2  # PC jumped back to LOOP
    assert old_flags == c._alu._flags  # flags unchanged on branch
    c.tick()
    assert c.decoded.mnem == "SUB"


def test_beq_forward_label():
    """
    Ensure BEQ branches correctly on forward label
    """
    prog = assemble(
        [
            "BEQ SKIP",  # should branch if Z==1
            "LOADI R0, #99",  # this should be skipped
            "SKIP:",
            "HALT",
        ]
    )
    c = make_cpu(prog)
    c._alu._flags = 0b0000 | Z_FLAG  # simulate ALU flags from prior op
    old_flags = c._alu._flags  # OK to access in tests
    c.tick()  # execute branch
    assert c.pc == 2  # PC jumped past LOADI to HALT
    assert old_flags == c._alu._flags  # flags unchanged on branch
    c.tick()
    assert c.decoded.mnem == "HALT"


def test_beq_backward_label():
    """
    Ensure BEQ branches correctly on backward label
    """
    prog = assemble(
        [
            "LOADI R1 #3",
            "LOADI R2 #3",
            "LOOP:",
            "SUB R1, R1, R2",
            "BEQ LOOP",
            "HALT",
        ]
    )
    c = make_cpu(prog)
    c.tick()  # LOADI
    c.tick()  # LOADI
    c.tick()  # SUB
    # Now step BEQ and confirm it branches correctly
    old_flags = c._alu._flags  # OK to access in tests
    c.tick()
    assert c.decoded.mnem == "BEQ"
    assert c.pc == 2  # PC jumped back to LOOP
    assert old_flags == c._alu._flags  # flags unchanged on branch
    # One more tick should decode the target instruction
    c.tick()
    assert c.decoded.mnem == "SUB"


def test_blt_forward_label():
    """
    Ensure BLT branches correctly when N==1
    """
    prog = assemble(
        [
            "BLT SKIP",  # should branch if N==1
            "LOADI R0, #99",  # this should be skipped
            "SKIP:",
            "HALT",
        ]
    )
    c = make_cpu(prog)
    c._alu._flags = N_FLAG  # simulate negative result
    c.tick()  # execute branch
    assert c.pc == 2  # jumped past LOADI
    c.tick()
    assert c.decoded.mnem == "HALT"


def test_blt_not_taken():
    """
    Ensure BLT does not branch when N==0
    """
    prog = assemble(["BLT SKIP", "LOADI R0, #99", "SKIP:", "HALT"])
    c = make_cpu(prog)
    c._alu._flags = 0b0000  # N=0
    c.tick()  # BLT not taken
    assert c.pc == 1  # sequential execution
    c.tick()
    assert c.decoded.mnem == "LOADI"


def test_bge_forward_label():
    """
    Ensure BGE branches correctly when N==0
    """
    prog = assemble(
        [
            "BGE SKIP",  # should branch if N==0
            "LOADI R0, #99",  # this should be skipped
            "SKIP:",
            "HALT",
        ]
    )
    c = make_cpu(prog)
    c._alu._flags = 0b0000  # N=0
    c.tick()  # execute branch
    assert c.pc == 2  # jumped past LOADI
    c.tick()
    assert c.decoded.mnem == "HALT"


def test_bge_not_taken():
    """
    Ensure BGE does not branch when N==1
    """
    prog = assemble(["BGE SKIP", "LOADI R0, #99", "SKIP:", "HALT"])
    c = make_cpu(prog)
    c._alu._flags = N_FLAG  # N=1
    c.tick()  # BGE not taken
    assert c.pc == 1
    c.tick()
    assert c.decoded.mnem == "LOADI"


def test_beq_not_taken():
    """
    Ensure BEQ does not branch when Z==0
    """
    prog = assemble(["BEQ SKIP", "LOADI R0, #42", "SKIP:", "HALT"])
    c = make_cpu(prog)
    c._alu._flags = 0b0000  # Z=0
    c.tick()  # BEQ not taken
    assert c.pc == 1
    c.tick()
    assert c.decoded.mnem == "LOADI"


def test_bne_not_taken():
    """
    Ensure BNE does not branch when Z==1
    """
    prog = assemble(["BNE SKIP", "LOADI R0, #42", "SKIP:", "HALT"])
    c = make_cpu(prog)
    c._alu._flags = Z_FLAG  # Z=1
    c.tick()  # BNE not taken
    assert c.pc == 1
    c.tick()
    assert c.decoded.mnem == "LOADI"


def test_blt_backward_label():
    """
    Ensure BLT branches correctly on backward label (N==1 from SUB)
    """
    prog = assemble(
        [
            "LOADI R1, #5",
            "LOADI R2, #10",
            "LOOP:",
            "SUB R0, R1, R2",  # 5 - 10 = -5, sets N=1
            "BLT LOOP",
            "HALT",
        ]
    )
    c = make_cpu(prog)
    c.tick()  # LOADI R1
    c.tick()  # LOADI R2
    c.tick()  # SUB --> N=1
    old_flags = c._alu._flags
    c.tick()  # BLT LOOP --> N=1, branch taken
    assert c.pc == 2  # jumped back to LOOP
    assert old_flags == c._alu._flags  # flags unchanged on branch
    c.tick()
    assert c.decoded.mnem == "SUB"


def test_bge_backward_label():
    """
    Ensure BGE branches correctly on backward label (N==0 from SUB)
    """
    prog = assemble(
        [
            "LOADI R1, #10",
            "LOADI R2, #5",
            "LOOP:",
            "SUB R0, R1, R2",  # 10 - 5 = 5, sets N=0
            "BGE LOOP",
            "HALT",
        ]
    )
    c = make_cpu(prog)
    c.tick()  # LOADI R1
    c.tick()  # LOADI R2
    c.tick()  # SUB --> N=0
    old_flags = c._alu._flags
    c.tick()  # BGE LOOP --> N=0, branch taken
    assert c.pc == 2  # jumped back to LOOP
    assert old_flags == c._alu._flags  # flags unchanged on branch
    c.tick()
    assert c.decoded.mnem == "SUB"


def test_blt_integration():
    """
    BLT taken: SUB naturally sets N=1, branch skips an instruction
    """
    prog = assemble(
        [
            "LOADI R1, #3",
            "LOADI R2, #7",
            "SUB R0, R1, R2",  # 3 - 7 = -4, N=1
            "BLT DONE",
            "LOADI R5, #0xFF",  # should be skipped
            "DONE:",
            "HALT",
        ]
    )
    c = make_cpu(prog)
    c.tick()  # LOADI R1
    c.tick()  # LOADI R2
    c.tick()  # SUB --> N=1
    c.tick()  # BLT DONE --> taken
    assert c.pc == 5  # skipped LOADI R5
    c.tick()
    assert c.decoded.mnem == "HALT"
    assert c.get_reg(5) == 0  # LOADI R5 was skipped


def test_bge_integration():
    """
    BGE taken: SUB naturally sets N=0, branch skips an instruction
    """
    prog = assemble(
        [
            "LOADI R1, #7",
            "LOADI R2, #3",
            "SUB R0, R1, R2",  # 7 - 3 = 4, N=0
            "BGE DONE",
            "LOADI R5, #0xFF",  # should be skipped
            "DONE:",
            "HALT",
        ]
    )
    c = make_cpu(prog)
    c.tick()  # LOADI R1
    c.tick()  # LOADI R2
    c.tick()  # SUB --> N=0
    c.tick()  # BGE DONE --> taken
    assert c.pc == 5  # skipped LOADI R5
    c.tick()
    assert c.decoded.mnem == "HALT"
    assert c.get_reg(5) == 0  # LOADI R5 was skipped


def test_loadi():
    """
    Ensure LOADI writes correctly to specified register
    """
    prog = assemble(["LOADI R1, #3"])
    c = make_cpu(prog)
    c.tick()  # LOADI
    assert c._regs.execute(ra=1) == (3, None)  # OK to access in tests


@pytest.mark.parametrize(
    "prog,reg,expected",
    [
        (["LOADI R1, #0", "LUI R1, 128"], 1, 0x8000),
        (["LOADI R1, #0xAB", "LUI R1, #0xCD"], 1, 0xCDAB),
    ],
)
def test_lui(prog, reg, expected):
    """
    Ensure LUI writes correctly to upper byte of specified register, and
    combined result (upper and lower bytes) is correct.
    """
    prog = assemble(prog)
    c = make_cpu(prog)
    c.tick()  # LOADI
    c.tick()  # LUI
    # Interpret as unsigned
    assert c._regs.execute(ra=reg) == (expected, None)



def test_add():
    """
    Ensure ADD writes correct result to specified register
    """
    prog = assemble(["LOADI R1, #3", "LOADI R2, #2", "ADD R3, R1, R2"])
    c = make_cpu(prog)
    c.tick()  # LOADI
    c.tick()  # LOADI
    c.tick()  # ADD
    assert c._regs.execute(ra=3) == (5, None)  # OK to access in tests


def test_addi():
    """
    Ensure ADDI writes correct result to specified register
    """
    prog = assemble(["LOADI R1, #3", "ADDI R5, R1, #4"])
    c = make_cpu(prog)
    c.tick()  # LOADI
    c.tick()  # ADDI
    assert c._regs.execute(ra=5) == (7, None)  # OK to access in tests


def test_and():
    """
    Ensure AND writes correct result to specified register
    """
    prog = assemble(["LOADI R1, #5", "LOADI R2, #10", "AND R3, R1, R2"])
    c = make_cpu(prog)
    c.tick()  # LOADI
    c.tick()  # LOADI
    c.tick()  # AND
    assert c._regs.execute(ra=3) == (0, None)  # OK to access in tests


def test_or():
    """
    Ensure OR writes correct result to specified register
    """
    prog = assemble(["LOADI R1, #5", "LOADI R2, #10", "OR R3, R1, R2"])
    c = make_cpu(prog)
    c.tick()  # LOADI
    c.tick()  # LOADI
    c.tick()  # OR
    assert c._regs.execute(ra=3) == (15, None)  # OK to access in tests


def test_xor():
    """
    Ensure XOR writes correct result to specified register and sets no flags
    for a positive, non-zero result.
    """
    prog = assemble(
        ["LOADI R1, #0b10101010", "LOADI R2, #0b11001100", "XOR R3, R1, R2"]
    )
    c = make_cpu(prog)
    c.tick()  # LOADI
    c.tick()  # LOADI
    c.tick()  # XOR
    assert c._regs.execute(ra=3) == (0b01100110, None)
    assert not c._alu.zero
    assert not c._alu.negative
    assert not c._alu.carry  # logic ops never touch carry


def test_xor_self_clears():
    """
    XOR of a register with itself should produce zero and set Z flag.
    """
    prog = assemble(["LOADI R1, #0xFF", "XOR R2, R1, R1"])
    c = make_cpu(prog)
    c.tick()  # LOADI
    c.tick()  # XOR
    assert c._regs.execute(ra=2) == (0, None)
    assert c._alu.zero
    assert not c._alu.negative
    assert not c._alu.carry


def test_xor_sets_negative_flag():
    """
    XOR result with MSB set should set N flag.
    """
    # 0xAAAA ^ 0x5555 = 0xFFFF --> -1, N=1
    prog = assemble(
        [
            "LOADI R1, #0xAA",
            "LUI R1, #0xAA",
            "LOADI R2, #0x55",
            "LUI R2, #0x55",
            "XOR R3, R1, R2",
        ]
    )
    c = make_cpu(prog)
    c.tick()  # LOADI R1
    c.tick()  # LUI R1 --> R1 = 0xAAAA
    c.tick()  # LOADI R2
    c.tick()  # LUI R2 --> R2 = 0x5555
    c.tick()  # XOR
    assert c._regs.execute(ra=3) == (-1, None)  # 0xFFFF as signed
    assert c._alu.negative
    assert not c._alu.zero
    assert not c._alu.carry


def test_shift_left():
    """
    Ensure SHFT (left) writes correct result to specified register
    """
    prog = assemble(["LOADI R1, #5", "LOADI R2, #4", "SHFT R3, R1, R2"])
    c = make_cpu(prog)
    c.tick()  # LOADI
    c.tick()  # LOADI
    c.tick()  # SHFT
    # 0b0101 << 4 = 0b1010000
    assert c._regs.execute(ra=3) == (0b1010000, None)  # OK to access in tests


def test_shift_right():
    """
    Ensure SHFT (right) writes correct result to specified register
    """
    prog = assemble(
        ["LOADI R1, #128", "LUI R1, #0", "LOADI R2, #5", "LUI R2, #128", "SHFT R3, R1, R2"]
    )
    c = make_cpu(prog)
    c.tick()  # LOADI R1
    c.tick()  # LUI R1, #0  -- zero-extend: R1 = 0x0080 = 128
    c.tick()  # LOADI R2
    c.tick()  # LUI R2
    c.tick()  # SHFT
    assert c._regs.execute(ra=3) == (4, None)  # OK to access in tests


def test_store_with_nonzero_offset():
    """
    Ensure STORE correctly uses a non-zero address offset.
    """
    prog = assemble(
        [
            "LOADI R1, #0x2A",      # data (0x2A = 42, no sign-extension issue)
            "LOADI R2, #0x0",       # base addr
            "STORE R1, [R2 + #5]",  # store to [R2 + 5] = address 5
            "LOAD R3, [R2 + #5]",   # load from address 5 into R3
        ]
    )
    c = make_cpu(prog)
    c.tick()  # LOADI (data)
    c.tick()  # LOADI (base)
    c.tick()  # STORE
    assert c._d_mem.read(5) == 0x2A
    c.tick()  # LOAD
    assert c._regs.execute(ra=3) == (0x2A, None)


def test_load_uninitialized():
    """
    Ensure load from uninitialized address loads zero (default)
    """
    prog = assemble(["LOADI R1, #0x0", "LOAD R2, [R1 + #0]"])
    c = make_cpu(prog)
    c.tick()  # LOADI
    c.tick()  # LOAD
    assert c._regs.execute(ra=2) == (0x0, None)  # OK to access in tests


def test_load_store():
    """
    Ensure load / store round-trip
    """
    prog = assemble(
        [
            "LOADI R1, #0x2A     ; data (0x2A = 42, no sign-extension issue)",
            "LOADI R2, #0x0      ; base addr",
            "STORE R1, [R2 + #0]  ; store data in R1 to [R2 + #0]",
            "LOAD R3, [R2 + #0]   ; load from [R2 + #0] into R3",
        ]
    )
    c = make_cpu(prog)
    c.tick()  # LOADI (data)
    assert c._regs.execute(ra=1) == (0x2A, None)  # OK to access in tests
    c.tick()  # LOADI (target adddress)
    assert c._regs.execute(ra=2) == (0x0, None)  # OK to access in tests
    c.tick()  # STORE
    assert c._d_mem.read(0x0) == 0x2A  # OK to access in tests
    c.tick()  # LOAD (check round trip)
    assert c._regs.execute(ra=3) == (0x2A, None)  # OK to access in tests


@pytest.mark.parametrize(
    "instr",
    [
        0x0000,  # HALT
        0x1000,  # LOADI
        0x2120,  # LUI
        0x3545,  # LOAD  (rd=2, ra=5, offset=5; offset fits in 6-bit signed)
        0x4A16,  # STORE
        0x5B3E,  # ADDI
        0x6640,  # ADD
        0x78B8,  # SUB
        0x8CC0,  # AND
        0x9098,  # OR
        0xA298,  # XOR
        0xB550,  # SHFT
        0xC040,  # BEQ (Bcond cc=0b00, imm=4)
        0xC044,  # BNE (Bcond cc=0b01, imm=4)
        0xC048,  # BLT (Bcond cc=0b10, imm=4)
        0xC04C,  # BGE (Bcond cc=0b11, imm=4)
        0xDCF6,  # B
        0xE380,  # CALL
        # RET omitted: raises RuntimeError on empty stack (see test_ret_without_call_raises)
    ],
)
def test_opcode_smoke(instr):
    """
    Test representatives of each opcode
    """
    prog = [instr]
    c = make_cpu(prog)
    c.tick()  # [instr]


def test_call_ret():
    """
    Test RET after CALL
    """
    prog = assemble(["CALL FOO", "HALT", "FOO:", "RET"])
    c = make_cpu(prog)
    assert c.pc == 0
    assert c.sp == STACK_TOP
    initial_flags = c._alu._flags  # OK to access in tests
    c.tick()  # CALL FOO
    assert c.decoded.mnem == "CALL"
    assert c.pc == 2
    assert c.sp == STACK_TOP - 1
    assert c._d_mem.read(STACK_TOP - 1) == 1
    # assert c._d_mem.read(STACK_TOP) == 0  # PC was stored (return addr)
    assert c._alu._flags == initial_flags  # OK to access in tests
    c.tick()  # RET
    assert c.decoded.mnem == "RET"
    assert c.pc == 1
    assert c.sp == STACK_TOP  # SP restored
    assert c._alu._flags == initial_flags  # OK to access in tests
    c.tick()  # HALT
    assert not c.running
    assert c.pc == 2
    assert c.sp == STACK_TOP  # SP restored


def test_nested_call_ret():
    """
    Ensure nested calls work correctly
    """
    prog = assemble(
        [
            "CALL F",
            "HALT",
            "F:",
            "CALL G",
            "RET",
            "G:",
            "RET",
        ]
    )

    c = make_cpu(prog)
    TOP = STACK_TOP

    c.tick()
    assert c.decoded.mnem == "CALL"
    assert c.pc == 2  # jumps to F
    assert c.sp == TOP - 1
    assert c._d_mem.read(TOP - 1) == 1  # OK to access in tests

    c.tick()
    assert c.decoded.mnem == "CALL"
    assert c.pc == 4  # jumps to G
    assert c.sp == TOP - 2
    assert c._d_mem.read(TOP - 2) == 3  # OK to access in tests

    c.tick()
    assert c.decoded.mnem == "RET"  # OK to access in tests
    assert c.pc == 3  # return from G
    assert c.sp == TOP - 1

    c.tick()
    assert c.decoded.mnem == "RET"  # OK to access in tests
    assert c.pc == 1  # return from F
    assert c.sp == TOP

    c.tick()
    assert c.decoded.mnem == "HALT"  # OK to access in tests
    assert not c.running


def test_ret_without_call_raises():
    """
    RET with empty stack (no prior CALL) should raise RuntimeError.
    """
    prog = assemble(["RET"])
    c = make_cpu(prog)
    with pytest.raises(RuntimeError, match="Stack underflow"):
        c.tick()


def test_ret_after_stack_exhausted_raises():
    """
    RET after matching CALL/RET pair leaves stack empty;
    a second RET should raise RuntimeError.
    """
    prog = assemble(["CALL FOO", "RET", "FOO:", "RET"])
    c = make_cpu(prog)
    c.tick()  # CALL FOO -- pushes return address, jumps to FOO
    c.tick()  # RET at FOO -- returns to second instruction, stack now empty
    assert c.sp == STACK_TOP
    with pytest.raises(RuntimeError, match="Stack underflow"):
        c.tick()  # RET with empty stack


@pytest.mark.parametrize(
    "value,bits,expected",
    [
        # boundaries
        (0x0000, 16, 0),      # 0
        (0x7FFF, 16, 32767),  # max positive
        (0x8000, 16, -32768), # min negative
        (0xFFFF, 16, -1),     # -1
        (0x00, 8, 0),         # 0 (8-bit)
        (0x7F, 8, 127),       # max positive (8-bit)
        (0x80, 8, -128),      # min negative (8-bit)
        (0xFF, 8, -1),        # -1 (8-bit)
        # positive range
        (0x0001, 16, 1),
        (0x4000, 16, 16384),
        (0x3FFF, 16, 16383),
        (0x01, 8, 1),
        (0x40, 8, 64),
        # negative range
        (0x8001, 16, -32767),
        (0x8002, 16, -32766),
        (0xFFFE, 16, -2),
        (0x81, 8, -127),
        (0x82, 8, -126),
    ],
)
def test_sext(value, bits, expected):
    """
    Ensure sext() behaves correctly across boundaries, positive, and negative ranges
    """
    assert Cpu.sext(value, bits) == expected



def test_branch_forward_plus_one():
    """
    Ensure correct branch forward by one
    """
    prog = assemble(
        [
            "B SKIP",  # offset + 1
            "LOADI R1, #99",
            "SKIP:",
            "HALT",
        ]
    )
    c = make_cpu(prog)
    c.tick()
    assert c.pc == 2


def test_branch_backward_minus_one():
    """
    Ensure correct branch backward by one
    """
    prog = assemble(
        [
            "LOADI R1, #0",
            "LOOP:",
            "B LOOP",  # offset = -1
            "HALT",
        ]
    )
    c = make_cpu(prog)
    c.tick()  # LOADI
    c.tick()  # B LOOP
    assert c.pc == 1


def test_branch_max_forward():
    """
    Our ISA limits the size of jumps.
    Jump from instruction 0 to instruction 32 (max).
    """
    asm = ["B FAR"]
    asm += ["LOADI R0, #0"] * 31  # fill
    asm += ["FAR:", "HALT"]
    prog = assemble(asm)

    c = make_cpu(prog)
    c.tick()  # B FAR

    assert c.pc == 32
    c.tick()
    assert c.decoded.mnem == "HALT"


def test_branch_max_backward():
    """
    Our ISA limits the size of jumps.
    Jump from instruction 0 to instruction -31 (max).
    """
    asm = (
        [
            "ADDI R0, R0, #0",  # because we don't have a NOP
            "LOOP:",
        ]
        + ["ADDI R0, R0, #0"] * 30
        + [
            "B LOOP",  # With PC = 32, offset must be -31
            "HALT",
        ]
    )

    prog = assemble(asm)
    c = make_cpu(prog)
    for _ in range(32):
        c.tick()
    c.tick()

    assert c.pc == 2  # backward target


def test_branch_self_loop():
    """
    Ensure infinite loop is infinite!
    """
    prog = assemble(
        [
            "LOOP:",
            "B LOOP",
        ]
    )
    c = make_cpu(prog)
    c.tick()
    c.tick()

    # It should loop forever at PC = 0
    assert c.pc == 0


def test_sub_logic():
    prog = assemble(
        [
            "LOADI R5, #32",  # a
            "LOADI R6, #16",  # b
            "SUB R7, R5, R6",  # a - b
            "HALT",
        ]
    )
    c = make_cpu(prog)
    c.tick()  # LOADI
    c.tick()  # LOADI
    c.tick()  # SUB
    assert c.get_reg(7) == 16  # a - b = 16


def test_subtract_mutation_order():
    prog = assemble(
        [
            "LOADI R5, #32",  # a = 32
            "LOADI R6, #16",  # b = 16
            "SUB R6, R6, R5",  # b = b - a => should be -16 (0xFFF0)
            "HALT",
        ]
    )
    c = make_cpu(prog)
    c.tick()
    c.tick()
    c.tick()
    assert c.get_reg(6) == -16


def test_and_resets_negative_flag():
    prog = assemble(
        [
            "LOADI R1, #0",
            "LOADI R2, #0",
            "SUB R3, R1, R2",  # zero result, flags: Z=1, N=0
            "LOADI R1, #1",
            "SUB R3, R2, R1",  # negative result, flags: N=1, Z=0
            "AND R4, R2, R2",  # 0 & 0 --> should set Z=1, N=0
            "HALT",
        ]
    )
    c = make_cpu(prog)
    assert not c._alu.zero
    assert not c._alu.negative
    assert not c._alu.carry
    assert not c._alu.overflow
    c.tick()
    c.tick()
    c.tick()
    assert c._alu.zero
    assert not c._alu.negative
    assert c._alu.carry
    assert not c._alu.overflow
    c.tick()
    c.tick()
    assert not c._alu.zero
    assert c._alu.negative
    assert not c._alu.carry
    assert not c._alu.overflow
    c.tick()
    assert c._alu.zero
    assert not c._alu.negative
    assert not c._alu.carry
    assert not c._alu.overflow
