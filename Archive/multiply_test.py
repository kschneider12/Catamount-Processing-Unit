"""
Tests for integer multiplication via repeated addition (multiply.asm)

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

with open("asm/multiply.asm") as fh:
    prog = fh.readlines()

for load_r1, line in enumerate(prog):
    if "LOADI R1" in line:
        break

for load_r2, line in enumerate(prog):
    if "LOADI R2" in line:
        break

cases = [
    pytest.param("#6",  "#7",  42,  id="6 * 7 = 42"),
    pytest.param("#1",  "#1",  1,   id="1 * 1 = 1"),
    pytest.param("#0",  "#5",  0,   id="0 * 5 = 0"),
    pytest.param("#5",  "#0",  0,   id="5 * 0 = 0"),
    pytest.param("#3",  "#3",  9,   id="3 * 3 = 9"),
    pytest.param("#12", "#10", 120, id="12 * 10 = 120"),
]


@pytest.mark.parametrize("immed_a,immed_b,expected", cases)
def test_multiply(immed_a, immed_b, expected):
    this_prog = prog[:]
    this_prog[load_r1] = this_prog[load_r1].replace("#6", immed_a)
    this_prog[load_r2] = this_prog[load_r2].replace("#7", immed_b)
    c = make_cpu(assemble(this_prog))
    while c.running:
        c.tick()
    assert c.get_reg(3) == expected
