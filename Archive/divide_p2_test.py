"""
Tests for division by powers of two (divide_p2.asm)

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

with open("asm/divide_p2.asm") as fh:
    prog = fh.readlines()

c = make_cpu(assemble(prog))

while c.running:
    c.tick()

# At this point, CPU is halted, and we should have these values in registers:


@pytest.mark.parametrize(
    "reg,expected",
    [
        pytest.param(0, 0x01C0, id="R0=0x01C0 (448)"),
        pytest.param(1, 0x8006, id="R1=0x8006 (32774)"),
        pytest.param(2, 0x00E0, id="R2=0x00E0 (224)"),
        pytest.param(3, 0x0070, id="R3=0x0070 (112)"),
        pytest.param(4, 0x0038, id="R4=0x0038 (56)"),
        pytest.param(5, 0x001C, id="R5=0x001C (28)"),
        pytest.param(6, 0x000E, id="R6=0x000E (14)"),
        pytest.param(7, 0x0007, id="R7=0x0007 (7)"),
    ],
)
def test_reg(reg, expected):
    # Need to mask to force to unsigned
    assert c.get_reg(reg) & 0xFFFF == expected


@pytest.mark.parametrize(
    "instr,count",
    [
        pytest.param("LUI", 2),
        pytest.param("LOADI", 2),
        pytest.param("SHFT", 6),
        pytest.param("ADDI", 5),
        pytest.param("HALT", 1),
    ],
)
def test_correct_num_instr(instr, count):
    filtered = [line for line in prog if instr in line]
    assert len(filtered) == count
