"""
Tests for addition with OR (add_and_or.asm)

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

with open("asm/add_and_or.asm") as fh:
    prog = fh.readlines()

load_a = -1  # sentinel
load_b = -1  # sentinel
# brittle!
for num, line in enumerate(prog):
    if "LOADI R0" in line:
        load_a = num
    elif "LOADI R1" in line:
        load_b = num


@pytest.mark.parametrize(
    "immed_a,immed_b,expected",
    [
        pytest.param(0b0000, 0b0000, 0b0000),
        pytest.param(0b0001, 0b0010, 0b0011),
        pytest.param(0b0001, 0b0001, 0b0000),
        pytest.param(0b1000, 0b1000, 0b0000),
        pytest.param(0b1000, 0b0100, 0b1100),
        pytest.param(0x2A, 0x55, 0x7F),
        pytest.param(0b1111, 0b0100, 0b0000),
        pytest.param(0b0100, 0b0010, 0b0110),
        pytest.param(0b1000, 0b0001, 0b1001),
    ],
)
def test_reg(immed_a, immed_b, expected):
    this_prog = prog[:]
    this_prog[load_a] = this_prog[load_a].replace("#0x2A", str(immed_a))
    this_prog[load_b] = this_prog[load_b].replace("#0x55", str(immed_b))
    c = make_cpu(assemble(this_prog))
    while c.running:
        c.tick()

    # At this point, CPU is halted, and we should have these values in registers:
    assert c.get_reg(2) == expected


@pytest.mark.parametrize(
    "instr,count",
    [
        pytest.param("LUI", 0),
        pytest.param("LOADI", 3),
        pytest.param("ADD", 0),  # captures ADDI too
        pytest.param("SUB", 0),
        pytest.param("SHFT", 0),
    ],
)
def test_correct_num_instr(instr, count):
    filtered = [line for line in prog if instr in line]
    assert len(filtered) == count
