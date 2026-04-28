"""
Instruction set for Catamount Processing Unit (CPU)

This ISA commits the Catamount PU to a 16-bit address space, word-aligned
accesses, signed-offset addressing, and a linear memory model where all
effective-address computations happen in 16-bit two's-complement arithmetic.

CS 2210 Computer Organization
Clayton Cafiero <cbcafier@uvm.edu>

v. 1.0.0 2025-10-29
v. 1.0.1 2025-11-02
    - Cleaned up SHFT; added utility function for displaying
    raw bits, and added conditional formatting for __repr__.
v. 1.0.2 2025-11-10
    - Revised semantics for branch instructions (changed to PC relative)
v. 1.0.3 2025-11-11
    - Revised semantics for CALL
    - Fixed operands for LOAD/STORE
v. 1.0.4 2025-11-13
    - Picking nits, improving descriptions
v. 2.0.0 2026-03-11
    - Redesigned opcode assignments: HALT moved to 0x0, all others shifted
      to make 0x0000 a safe HALT encoding, and to group instructions
      logically (LOADI/LUI adjacent at 0x1-0x2, LOAD/STORE adjacent at
      0x3-0x4, control flow at 0xD-0xF). BEQ unchanged at 0xA; BNE moved
      to 0xC; SHFT moved to 0xB.
v. 2.1.0 2026-03-11
    - Replaced separate BEQ (0xA) and BNE (0xC) with a unified Bcond family
      at opcode 0xC. A 2-bit condition code (cc) field in bits [3:2] selects
      BEQ (cc=00), BNE (cc=01), BLT (cc=10), BGE (cc=11). Encoding:
      opcode(4) | imm(8) | cc(2) | zero(2). Opcode 0xA is now free.
v. 2.2.0 2026-03-11
    - Added XOR at opcode 0xA (R-format). Fills the slot freed by Bcond
      consolidation.
"""

from dataclasses import dataclass  # For Instruction class, below.

# Instruction set specification
ISA = {
    "HALT": {
        "opcode": 0x0,
        "format": "O",
        "variant": "halt",
        "fields": ["opcode(4)", "zero(12)"],
        "semantics": "stop execution",
        "description": "Halt CPU.",
        "register_write": False,
        "memory_write": False,
        "alu": False,
        "immediate": False,
        "branch": False,
    },
    "LOADI": {
        "opcode": 0x1,
        "format": "I",
        "variant": "imm-only",
        "fields": ["opcode(4)", "rd(3)", "imm(8)", "zero(1)"],
        "semantics": "Rd <-- imm8 (zero-extended)",
        "description": "Load immediate 8-bit constant into Rd.",
        "register_write": True,
        "memory_write": False,
        "alu": False,
        "immediate": True,
        "branch": False,
    },
    "LUI": {
        "opcode": 0x2,
        "format": "I",
        "variant": "imm-only",
        "fields": ["opcode(4)", "rd(3)", "imm(8)", "zero(1)"],
        "semantics": "Rd[15:8] <-- imm8 (leaves Rd[7:0] unchanged)",
        "description": "Load immediate into upper byte of Rd.",
        "register_write": True,
        "memory_write": False,
        "alu": False,
        "immediate": True,
        "branch": False,
    },
    "LOAD": {
        "opcode": 0x3,
        "format": "M",
        "fields": ["opcode(4)", "rd(3)", "ra(3)", "addr(6)"],
        "semantics": "Rd <-- MEM[Ra + signextend(addr6)]",
        "description": "Load word from memory at [Ra + offset] into Rd.",
        "register_write": True,
        "memory_write": False,
        "alu": False,  # assume aux adder for eff address
        "immediate": False,
        "branch": False,
    },
    "STORE": {
        "opcode": 0x4,
        "format": "M",
        "fields": ["opcode(4)", "ra(3)", "rb(3)", "addr(6)"],
        "semantics": "MEM[Rb + signextend(addr6)] <-- Ra",
        "description": "Store Ra (data source) to memory at Rb (base) + offset.",
        "register_write": False,
        "memory_write": True,
        "alu": False,  # assume aux adder for eff address
        "immediate": False,
        "branch": False,
    },
    "ADDI": {
        "opcode": 0x5,
        "format": "I",
        "variant": "reg+imm",
        "fields": ["opcode(4)", "rd(3)", "ra(3)", "imm(6)"],
        "semantics": "Rd <-- Ra + signextend(imm6)",
        "description": "Add signed 6-bit immediate value to Ra.",
        "register_write": True,
        "memory_write": False,
        "alu": True,
        "immediate": True,
        "branch": False,
    },
    "ADD": {
        "opcode": 0x6,
        "format": "R",
        "fields": ["opcode(4)", "rd(3)", "ra(3)", "rb(3)", "zero(3)"],
        "semantics": "Rd <-- Ra + Rb",
        "description": "Add values in two registers.",
        "register_write": True,
        "memory_write": False,
        "alu": True,
        "immediate": False,
        "branch": False,
    },
    "SUB": {
        "opcode": 0x7,
        "format": "R",
        "fields": ["opcode(4)", "rd(3)", "ra(3)", "rb(3)", "zero(3)"],
        "semantics": "Rd <-- Ra - Rb",
        "description": "Subtract value in Rb from value in Ra.",
        "register_write": True,
        "memory_write": False,
        "alu": True,
        "immediate": False,
        "branch": False,
    },
    "AND": {
        "opcode": 0x8,
        "format": "R",
        "fields": ["opcode(4)", "rd(3)", "ra(3)", "rb(3)", "zero(3)"],
        "semantics": "Rd <-- Ra & Rb",
        "description": "Bitwise AND of two registers.",
        "register_write": True,
        "memory_write": False,
        "alu": True,
        "immediate": False,
        "branch": False,
    },
    "OR": {
        "opcode": 0x9,
        "format": "R",
        "fields": ["opcode(4)", "rd(3)", "ra(3)", "rb(3)", "zero(3)"],
        "semantics": "Rd <-- Ra | Rb",
        "description": "Bitwise OR of two registers.",
        "register_write": True,
        "memory_write": False,
        "alu": True,
        "immediate": False,
        "branch": False,
    },
    "XOR": {
        "opcode": 0xA,
        "format": "R",
        "fields": ["opcode(4)", "rd(3)", "ra(3)", "rb(3)", "zero(3)"],
        "semantics": "Rd <-- Ra ^ Rb",
        "description": "Bitwise XOR of two registers.",
        "register_write": True,
        "memory_write": False,
        "alu": True,
        "immediate": False,
        "branch": False,
    },
    "SHFT": {
        "opcode": 0xB,
        "format": "R",
        "fields": ["opcode(4)", "rd(3)", "ra(3)", "rb(3)", "zero(3)"],
        "semantics": "if Rb & 0x8000: Rd <-- Ra >> (Rb & 0xF) "
        "else Rd <-- Ra << (Rb & 0xF)",
        "description": "Logical shift left or right depending on MSB of Rb. "
        "Absolute value of shift amount is limited to 15. "
        "We use the MSB of Rb to indicate direction of the shift."
        "If MSB is zero, then left shift; otherwise, right shift."
        "We use the lowest four bits of Rb for shift amount.",
        "register_write": True,
        "memory_write": False,
        "alu": True,
        "immediate": False,
        "branch": False,
    },
    # Bcond family: all share opcode 0xC, distinguished by cc field in bits [3:2].
    # Encoding: opcode(4) | imm(8) | cc(2) | zero(2)
    # OPCODE_MAP[0xC] resolves to "BGE" (last defined); _decode_from_word
    # overrides self.mnem using the cc field to yield the specific mnemonic.
    "BEQ": {
        "opcode": 0xC,
        "cc": 0b00,
        "format": "B",
        "variant": "cond",
        "fields": ["opcode(4)", "imm(8)", "cc(2)", "zero(2)"],
        "semantics": "if Z == 1: PC <-- PC + signextend(imm8)",
        "description": "Branch if zero flag is set (cc=00). "
        "Branch offset is PC-relative to the instruction after the branch.",
        "register_write": False,
        "memory_write": False,
        "alu": False,
        "immediate": True,
        "branch": True,
    },
    "BNE": {
        "opcode": 0xC,
        "cc": 0b01,
        "format": "B",
        "variant": "cond",
        "fields": ["opcode(4)", "imm(8)", "cc(2)", "zero(2)"],
        "semantics": "if Z == 0: PC <-- PC + signextend(imm8)",
        "description": "Branch if zero flag is clear (cc=01). "
        "Branch offset is PC-relative to the instruction after the branch.",
        "register_write": False,
        "memory_write": False,
        "alu": False,
        "immediate": True,
        "branch": True,
    },
    "BLT": {
        "opcode": 0xC,
        "cc": 0b10,
        "format": "B",
        "variant": "cond",
        "fields": ["opcode(4)", "imm(8)", "cc(2)", "zero(2)"],
        "semantics": "if N == 1: PC <-- PC + signextend(imm8)",
        "description": "Branch if negative flag is set (cc=10). "
        "Branch offset is PC-relative to the instruction after the branch.",
        "register_write": False,
        "memory_write": False,
        "alu": False,
        "immediate": True,
        "branch": True,
    },
    "BGE": {
        "opcode": 0xC,
        "cc": 0b11,
        "format": "B",
        "variant": "cond",
        "fields": ["opcode(4)", "imm(8)", "cc(2)", "zero(2)"],
        "semantics": "if N == 0: PC <-- PC + signextend(imm8)",
        "description": "Branch if negative flag is clear (cc=11). "
        "Branch offset is PC-relative to the instruction after the branch.",
        "register_write": False,
        "memory_write": False,
        "alu": False,
        "immediate": True,
        "branch": True,
    },
    "B": {
        "opcode": 0xD,
        "format": "B",
        "variant": "uncond",
        "fields": ["opcode(4)", "zero(4)", "imm(8)"],
        "semantics": "PC <-- PC + signextend(imm8)",
        "description": "Unconditional branch by signed 8-bit PC-relative "
        "offset. Branches apply this operation to PC after fetch, not PC "
        "before fetch. Branch offsets are PC-relative to the instruction "
        "after the branch (PC after fetch). imm8 is offset.",
        "register_write": False,  # writes directly to PC, not GP register
        "memory_write": False,
        "alu": False,
        "immediate": True,
        "branch": True,
    },
    "CALL": {
        "opcode": 0xE,
        "format": "B",
        "variant": "link",
        "fields": ["opcode(4)", "offset(8)", "zero(4)"],
        "semantics": "Push (PC after fetch); PC <-- PC after fetch + "
        "signextend(offset8). ",
        "description": "Call subroutine at address given by PC after fetch "
        "plus the signed 8-bit immediate. During fetch, PC is incremented. "
        "During execute, CALL pushes the PC value after fetch onto the stack "
        "(the return address), then jumps to the PC-relative target. ",
        "register_write": False,  # writes directly to PC, not GP register
        "memory_write": True,  # pushes return address onto stack
        "alu": False,  # assume aux adder for increment
        "immediate": True,  # offset
        "branch": True,
    },
    "RET": {
        "opcode": 0xF,
        "format": "B",
        "variant": "ret",
        "fields": ["opcode(4)", "zero(12)"],
        "semantics": "Pop PC",
        "description": "Return from subroutine.",
        "register_write": False,
        "memory_write": False,
        "alu": False,
        "immediate": False,
        "branch": True,
    },
}


# Pseudo-instructions: assembler-only; no opcode of their own.
# Same field structure as ISA entries where applicable; no opcode/format.
PSEUDO = {
    "MOV": {
        "expands_to": "ADDI Rd, Ra, #0",
        "fields": ["rd(3)", "ra(3)"],
        "semantics": "Rd <-- Ra",
        "description": "Copy register Ra into Rd. "
        "Pseudo-instruction; assembles as ADDI Rd, Ra, #0.",
        "register_write": True,
        "memory_write": False,
        "alu": True,
        "immediate": False,
        "branch": False,
    },
}


# Reverse map for opcode lookup
OPCODE_MAP = {v["opcode"]: k for k, v in ISA.items()}

# Condition code --> mnemonic for Bcond family
_CC_TO_MNEM = {0b00: "BEQ", 0b01: "BNE", 0b10: "BLT", 0b11: "BGE"}


def get_instruction_spec(key):
    """
    Helper function. Returns the ISA specification for a
    given mnemonic (str) or opcode (int).
    """
    if isinstance(key, str):
        return ISA[key.upper()]
    return ISA[OPCODE_MAP[key]]  # if it's not a str, assume it's an int


@dataclass
class Instruction:  # pylint: disable=too-many-instance-attributes
    """
    Represents a single decoded instruction for the Catamount
    Processing Unit (CPU).

    Fields correspond to the 16-bit ISA specification.

    We use Python dataclass for minimal, lightweight classes,
    almost like structs in C. When we instantiate an instruction,
    `i`, we can access its fields using dot notation, like this:

    i.opcode       # gets us the opcode of instruction i
    i.rd           # gets us the destination register of instruction i
    etc.
    """

    # Defaults (constructor is implicit)
    opcode: int = 0
    mnem: str = ""
    rd: int = 0
    ra: int = 0
    rb: int = 0
    imm: int = 0
    cc: int = 0  # condition code for Bcond family (BEQ/BNE/BLT/BGE)
    addr: int = 0
    zero: int = 0
    raw: int | None = None

    def __post_init__(self):
        """
        This is called immediately after the object is instantiated.
        If raw bytes have been provided, the instruction is auto-
        decoded. If not, then we assume all necessary fields have
        been supplied to the constructor.
        """
        if self.raw is not None:
            self._decode_from_word(self.raw)
        if not self.mnem and self.opcode:
            self.mnem = OPCODE_MAP.get(self.opcode, "???")
        if not self.opcode and self.mnem:
            self.opcode = ISA[self.mnem]["opcode"]

    @property
    def format(self):
        """
        Get the instruction format.
        """
        spec = ISA.get(self.mnem)
        if not spec:
            return None
        return spec["format"]

    def _decode_from_word(self, word):
        """
        Self-decode instruction from 16-bit word.
        """
        self.opcode = (word >> 12) & 0xF
        self.mnem = OPCODE_MAP.get(self.opcode, "???")
        fmt = self.format
        if fmt == "R":
            self.rd = (word >> 9) & 0x7
            self.ra = (word >> 6) & 0x7
            self.rb = (word >> 3) & 0x7
            self.zero = word & 0x7  # 4-bit zero padding
        elif self.mnem in ("LOADI", "LUI"):
            self.rd = (word >> 9) & 0x7
            self.imm = (word >> 1) & 0xFF
            self.zero = word & 1  # 1-bit zero padding
        elif self.mnem == "ADDI":
            self.rd = (word >> 9) & 0x7
            self.ra = (word >> 6) & 0x7
            self.imm = word & 0x3F
            self.zero = 0  # no zero padding
        elif fmt == "M":
            if self.mnem == "STORE":
                self.ra = (word >> 9) & 0x7  # source/data register
                self.rb = (word >> 6) & 0x7  # base register
            else:  # LOAD
                self.rd = (word >> 9) & 0x7  # destination register
                self.ra = (word >> 6) & 0x7  # base register
            self.addr = word & 0x3F  # 63 (6 bits)
            self.zero = 0  # no zero padding
        elif self.mnem == "CALL":
            self.imm = (word >> 4) & 0xFF
            self.zero = word & 0xF  # 4-bit zero padding
        elif self.mnem in ("RET", "HALT"):
            self.zero = word & 0xFFF  # 12-bit zero padding
        elif self.mnem in ("BEQ", "BNE", "BLT", "BGE"):
            self.imm = (word >> 4) & 0xFF
            self.cc = (word >> 2) & 0x3
            self.zero = word & 0x3
            self.mnem = _CC_TO_MNEM[self.cc]
        elif fmt == "B":  # B (unconditional)
            self.imm = word & 0xFF
            self.zero = 0
        else:
            raise ValueError(f"Unhandled instruction {self.mnem}")
        self.raw = word
        try:
            assert self.zero == 0
        except AssertionError:
            print(f"BAD zero padding on {self.mnem}!")
            print(f"Raw word (hex): {word:04X}")
            print(f"Raw word (bin): {word:16b}")
            print("Problem with decoding? Or assembler bug?")
            raise

    @property
    def raw_bin(self):
        """
        Return pretty, zero padded binary representation of raw bytes.
        """
        assert self.raw is not None
        return "0b" + bin(self.raw)[2:].zfill(16)

    @property
    def raw_hex(self):
        """
        Return pretty, zero padded, upper-case hex representation of raw bytes.
        """
        assert self.raw is not None
        return "0x" + hex(self.raw)[2:].zfill(4).upper()

    def __repr__(self):
        """
        Revised 2025-11-01 to include raw bytes and conditional
        formatting by opcode, and to format fields as hex.
        """
        s = f"Instruction({self.mnem} (opcode={self.opcode}): "
        fmt = self.format
        if fmt is None:
            raise ValueError("Instruction format unknown")
        if fmt == "R":
            s += (
                f"rd=0x{self.rd:01X}, ra=0x{self.ra:01X}, "
                f"rb=0x{self.rb:01X}, zero={self.zero:01X}, "
            )
        elif self.mnem in ("LOADI", "LUI"):
            s += f"rd=0x{self.rd:01X}, imm=0x{self.imm:02X}, zero=0x{self.zero:01X}, "
        elif self.mnem == "ADDI":
            s += f"rd=0x{self.rd:01X}, ra=0x{self.ra:01X}, imm=0x{self.imm:02X}, "
        elif self.mnem == "LOAD":
            s += f"rd=0x{self.rd:01X}, ra=0x{self.ra:01X}, addr=0x{self.addr:03X}, "
        elif self.mnem == "STORE":
            s += f"ra=0x{self.ra:01X}, rb=0x{self.rb:01X}, addr=0x{self.addr:03X}, "
        elif self.mnem == "CALL":
            s += f"imm=0x{self.imm:02X}, zero=0x{self.zero:01X}, "
        elif self.mnem in ("RET", "HALT"):
            s += f"zero=0x{self.zero:03X}, "
        elif self.mnem in ("BEQ", "BNE", "BLT", "BGE"):
            s += f"imm=0x{self.imm:02X}, cc=0b{self.cc:02b}, zero=0x{self.zero:01X}, "
        elif fmt == "B":
            s += f"imm=0x{self.imm:02X}, zero=0x{self.zero:01X}, "
        s += f"raw_hex={self.raw_hex}, raw_bin={self.raw_bin})"
        return s
