"""
Catamount Processing Unit
A toy 16-bit Harvard architecture CPU.

CS 2210 Computer Organization
Clayton Cafiero <cbcafier@uvm.edu>

Nico Milazzo, Kent Schneider
"""

from alu import Alu
from constants import STACK_TOP
from instruction_set import Instruction
from memory import DataMemory, InstructionMemory
from register_file import RegisterFile


class Cpu:
    """
    Catamount Processing Unit
    """

    def __init__(self, *, alu, regs, d_mem, i_mem):
        """
        Constructor
        """
        self._i_mem = i_mem
        self._d_mem = d_mem
        self._regs = regs
        self._alu = alu
        self._pc = 0  # program counter
        self._ir = 0  # instruction register
        self._sp = STACK_TOP  # stack pointer
        self._decoded = Instruction()
        self._halt = False

    @property
    def running(self):
        return not self._halt

    @property
    def pc(self):
        return self._pc

    @property
    def sp(self):
        return self._sp

    @property
    def ir(self):
        return self._ir

    @property
    def decoded(self):
        return self._decoded

    def get_reg(self, r):
        """
        Public accessor (getter) for single register value.
        """
        return self._regs.execute(ra=r)[0]

    def tick(self):
        """
        Fetch-decode-execute
        """
        if not self._halt:
            self._fetch()
            self._decode()

            # execute...
            match self._decoded.mnem:
                case "LOADI":
                    # Load the two registers used
                    rd = self._decoded.rd
                    # Get the immediate value
                    op = self._decoded.imm
                    # Load the operand into the destination register
                    self._regs.execute(rd=rd, data=op, write_enable=True)
                case "LUI":
                    # Load upper immediate (shifted left by 8 bits)
                    rd = self._decoded.rd
                    upper = self._decoded.imm << 8
                    lower, _ = self._regs.execute(ra=rd)
                    lower &= 0x00FF  # clear upper bits
                    data = upper | lower
                    self._regs.execute(rd=rd, data=data, write_enable=True)
                case "LOAD":
                    # gets destination in register
                    dest = self._decoded.rd

                    #gets start and offset for where we want to pull from memory
                    start = self._decoded.ra
                    offset = self._decoded.imm

                    #access data memory and read at index (start+offset)
                    data = self._d_mem.read(start + offset)

                    #write data to dest in register
                    self._regs.execute(rd=dest, data=data, write_enable=True)

                    #Fields: opcode(4), rd(3), ra(3), imm(6)
                    #Semantics: Rd <– MEM[Ra + signextend(imm6)]
                case "STORE":
                    #Fields: opcode(4), ra(3), rb(3), imm(6)
                    #Semantics: MEM[Rb + signextend(imm6)] <– Ra
                    pass
                case "ADDI":
                    pass  # complete implementation here
                case "ADD":
                    pass  # complete implementation here
                case "SUB":
                    pass  # complete implementation here
                case "AND":
                    # Set the alu current operation (AND)
                    self._alu.set_op("AND")

                    # Get the destination register of the decoded instruction
                    rd = self._decoded.rd
                    # Get the operand a register...
                    ra = self._decoded.ra
                    # Get the operand b register
                    rb = self._decoded.rb

                    # Get the values of a and b from registers a and b
                    op_a, op_b = self._regs.execute(ra=ra, rb=rb)
                    # Calculate result with alu
                    result = self._alu.execute(op_a, op_b)
                    # Execute the value into the destination register
                    self._regs.execute(rd=rd, data=result, write_enable=True)
                case "OR":
                    pass  # complete implementation here

                    # Set the alu current operation (OR)
                    self._alu.set_op("OR")

                    # Get the destination register of the decoded instruction
                    rd = self._decoded.rd
                    # Get the operand a register...
                    ra = self._decoded.ra
                    # Get the operand b register
                    rb = self._decoded.rb

                    # Get the values of a and b from registers a and b
                    op_a, op_b = self._regs.execute(ra=ra, rb=rb)
                    # Calculate result with alu
                    result = self._alu.execute(op_a, op_b)
                    # Execute the value into the destination register
                    self._regs.execute(rd=rd, data=result, write_enable=True)
                case "XOR":
                    # Set the alu current operation (XOR)
                    self._alu.set_op("XOR")

                    # Get the destination register of the decoded instruction
                    rd = self._decoded.rd
                    # Get the operand a register...
                    ra = self._decoded.ra
                    # Get the operand b register
                    rb = self._decoded.rb

                    # Get the values of a and b from registers a and b
                    op_a, op_b = self._regs.execute(ra=ra, rb=rb)
                    # Calculate result with alu
                    result = self._alu.execute(op_a, op_b)
                    # Execute the value into the destination register
                    self._regs.execute(rd=rd, data=result, write_enable=True)
                case "SHFT":
                    self._alu.set_op("SHFT")
                    rd = self._decoded.rd
                    ra = self._decoded.ra
                    rb = self._decoded.rb
                    op_a, op_b = self._regs.execute(ra=ra, rb=rb)
                    result = self._alu.execute(op_a, op_b)
                    self._regs.execute(rd=rd, data=result, write_enable=True)
                case "BEQ":
                    if self._alu.zero:
                        offset = self.sext(self._decoded.imm, 8)
                        self._pc += offset  # take branch
                case "BNE":
                    pass  # complete implementation here
                case "BLT":
                    pass  # complete implementation here
                case "BGE":
                    pass  # complete implementation here
                case "B":
                    pass  # complete implementation here
                case "CALL":
                    self._sp -= 1  # grow stack downward
                    # PC is incremented immediately upon fetch so already
                    # pointing to next instruction, which is return address.
                    ret_addr = self._pc  # explicit
                    self._d_mem.write_enable(True)
                    # push return address...
                    self._d_mem.write(self._sp, ret_addr, from_stack=True)
                    offset = self._decoded.imm
                    self._pc += self.sext(offset, 8)  # jump to target
                case "RET":
                    # Get return address from memory via SP
                    # Increment SP
                    # Update PC
                    pass  # complete implementation here
                case "HALT":
                    pass  # complete implementation here
                case _:  # default
                    raise ValueError(
                        "Unknown mnemonic: " + str(self._decoded) + "\n" + str(self._ir)
                    )

            return True
        return False

    def _decode(self):
        """
        We're effectively delegating decoding to the Instruction class.
        """
        self._decoded = Instruction(raw=self._ir)

    def _fetch(self):
        self._ir = self._i_mem.read(self._pc)
        self._pc += 1

    def load_program(self, prog):
        self._i_mem.load_program(prog)

    @staticmethod
    def sext(value, bits=16):
        mask = (1 << bits) - 1
        value &= mask
        sign_bit = 1 << (bits - 1)
        return (value ^ sign_bit) - sign_bit


# Helper function
def make_cpu(prog=None):
    alu = Alu()
    d_mem = DataMemory()
    i_mem = InstructionMemory()
    if prog:
        i_mem.load_program(prog)
    regs = RegisterFile()
    return Cpu(alu=alu, d_mem=d_mem, i_mem=i_mem, regs=regs)
