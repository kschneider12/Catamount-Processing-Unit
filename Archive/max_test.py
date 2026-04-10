"""
Tests for maximum of two signed integers (max.asm)

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

with open("asm/max.asm") as fh:
    prog = fh.readlines()

for load_r1, line in enumerate(prog):
    if "LOADI R1" in line:
        break

for load_r2, line in enumerate(prog):
    if "LOADI R2" in line:
        break

cases = [
    pytest.param("#3", "#5", 5, id="3 vs 5 --> 5"),
    pytest.param("#5", "#3", 5, id="5 vs 3 --> 5"),
    pytest.param("#0", "#0", 0, id="0 vs 0 --> 0"),
    pytest.param("#1", "#1", 1, id="1 vs 1 --> 1"),
    pytest.param("#-3", "#-1", -1, id="-3 vs -1 --> -1"),
    pytest.param("#-5", "#3", 3, id="-5 vs 3 --> 3"),
    pytest.param("#3", "#-5", 3, id="3 vs -5 --> 3"),
    pytest.param("#-128", "#127", 127, id="-128 vs 127 --> 127"),
]


@pytest.mark.parametrize("immed_a,immed_b,expected", cases)
def test_max(immed_a, immed_b, expected):
    this_prog = prog[:]
    this_prog[load_r1] = this_prog[load_r1].replace("#3", immed_a)
    this_prog[load_r2] = this_prog[load_r2].replace("#5", immed_b)
    c = make_cpu(assemble(this_prog))
    while c.running:
        c.tick()
    assert c.get_reg(3) == expected
