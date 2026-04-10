"""
Tests for integer division via repeated subtraction (divide.asm)

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

with open("asm/divide.asm") as fh:
    prog = fh.readlines()

for load_r1, line in enumerate(prog):
    if "LOADI R1" in line:
        break

for load_r2, line in enumerate(prog):
    if "LOADI R2" in line:
        break

# Each case: (a, b, quotient, remainder)
cases = [
    pytest.param("#17", "#5", 3,  2, id="17 / 5 = 3 r 2"),
    pytest.param("#10", "#2", 5,  0, id="10 / 2 = 5 r 0"),
    pytest.param("#0",  "#5", 0,  0, id="0 / 5 = 0 r 0"),
    pytest.param("#5",  "#5", 1,  0, id="5 / 5 = 1 r 0"),
    pytest.param("#1",  "#5", 0,  1, id="1 / 5 = 0 r 1"),
    pytest.param("#100","#7", 14, 2, id="100 / 7 = 14 r 2"),
]


@pytest.mark.parametrize("immed_a,immed_b,expected_q,expected_r", cases)
def test_divide(immed_a, immed_b, expected_q, expected_r):
    this_prog = prog[:]
    this_prog[load_r1] = this_prog[load_r1].replace("#17", immed_a)
    this_prog[load_r2] = this_prog[load_r2].replace("#5",  immed_b)
    c = make_cpu(assemble(this_prog))
    while c.running:
        c.tick()
    assert c.get_reg(3) == expected_q
    assert c.get_reg(4) == expected_r
