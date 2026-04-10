"""
Tests for absolute value (abs.asm)

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

with open("asm/abs.asm") as fh:
    prog = fh.readlines()

for load_r1, line in enumerate(prog):
    if "LOADI R1" in line:
        break

cases = [
    pytest.param("#0", 0, id="0 -> 0"),
    pytest.param("#1", 1, id="1 -> 1"),
    pytest.param("#42", 42, id="42 -> 42"),
    pytest.param("#127", 127, id="127 -> 127"),
    pytest.param("#-1", 1, id="-1 -> 1"),
    pytest.param("#-5", 5, id="-5 -> 5"),
    pytest.param("#-42", 42, id="-42 -> 42"),
    pytest.param("#-128", 128, id="-128 -> 128"),
]


@pytest.mark.parametrize("immed,expected", cases)
def test_abs(immed, expected):
    this_prog = prog[:]
    this_prog[load_r1] = this_prog[load_r1].replace("#-5", immed)
    c = make_cpu(assemble(this_prog))
    while c.running:
        c.tick()
    assert c.get_reg(1) == expected
