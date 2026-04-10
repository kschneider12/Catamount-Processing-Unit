"""
Tests for multiply by powers of two in a loop (multiply_p2_loop.asm)

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

with open("asm/multiply_p2_loop.asm") as fh:
    prog = fh.readlines()

c = make_cpu(assemble(prog))

while c.running:
    c.tick()

# At this point, CPU is halted, and we should have these values in registers:


@pytest.mark.parametrize(
    "addr,expected",
    [
        pytest.param(0, 0x000A, id="MEM(0x0)=0x000A (10))"),
        pytest.param(1, 0x0014, id="MEM(0x1)=0x0014 (20)"),
        pytest.param(2, 0x0028, id="MEM(0x2)=0x0028 (40)"),
        pytest.param(3, 0x0050, id="MEM(0x3)=0x0050 (80)"),
        pytest.param(4, 0x00A0, id="MEM(0x4)=0x00A0 (160)"),
        pytest.param(5, 0x0140, id="MEM(0x5)=0x0140 (320)"),
        pytest.param(6, 0x0280, id="MEM(0x6)=0x0280 (640)"),
        pytest.param(7, 0x0500, id="MEM(0x7)=0x0500 (1280)"),
        pytest.param(8, 0x0A00, id="MEM(0x8)=0x0A00 (2560)"),
    ],
)
def test_reg(addr, expected):
    # Need to mask to force to unsigned
    assert c._d_mem.read(addr) == expected


@pytest.mark.parametrize(
    "instr,count",
    [
        pytest.param("LUI", 0),
        pytest.param("SHFT", 1),
        pytest.param("STORE", 1),
        pytest.param("HALT", 1),
    ],
)
def test_correct_num_instr(instr, count):
    filtered = [line for line in prog if instr in line]
    assert len(filtered) == count
