"""
Tests for multiply by power of two (multiply_p2.asm)

CS 2210 Computer Organization
Clayton Cafiero <cbcafier@uvm.edu>
"""

import os
import sys

import pytest

module_dir = os.path.abspath(".")
sys.path.insert(0, module_dir)

from assembler import assemble  # noqa: E402
from cpu import make_cpu  # noqa: E402

with open("asm/multiply_p2.asm") as fh:
    prog = fh.readlines()

c = make_cpu(assemble(prog))

while c.running:
    c.tick()

# At this point, CPU is halted, and we should have these values in registers:


@pytest.mark.parametrize(
    "reg,expected",
    [
        pytest.param(0, 0x0003, id="R0=0x0003 (3))"),
        pytest.param(1, 0x0006, id="R1=0x0006 (6)"),
        pytest.param(2, 0x0006, id="R2=0x0006 (6)"),
        pytest.param(3, 0x000C, id="R3=0x000C (12)"),
        pytest.param(4, 0x0018, id="R4=0x0038 (24)"),
        pytest.param(5, 0x0030, id="R5=0x001C (48)"),
        pytest.param(6, 0x0060, id="R6=0x000E (96)"),
        pytest.param(7, 0x00C0, id="R7=0x0007 (192)"),
    ],
)
def test_reg(reg, expected):
    # Need to mask to force to unsigned
    assert c.get_reg(reg) & 0xFFFF == expected


@pytest.mark.parametrize(
    "instr,count",
    [
        pytest.param("LUI", 0),
        pytest.param("LOADI", 2),
        pytest.param("SHFT", 6),
        pytest.param("ADDI", 5),
        pytest.param("HALT", 1),
    ],
)
def test_correct_num_instr(instr, count):
    filtered = [line for line in prog if instr in line]
    assert len(filtered) == count
