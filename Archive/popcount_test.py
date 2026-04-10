"""
Tests for popcount -- count set bits in a 16-bit word (popcount.asm)

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

with open("asm/popcount.asm") as fh:
    prog = fh.readlines()

for load_r1, line in enumerate(prog):
    if "LOADI R1" in line:
        break

cases = [
    pytest.param("#0", 0, id="0x0000 --> 0"),
    pytest.param("#1", 1, id="0x0001 --> 1"),
    pytest.param("#3", 2, id="0x0003 --> 2"),
    pytest.param("#0x0F", 4, id="0x000F --> 4"),
    pytest.param("#85", 4, id="0x0055 --> 4"),
    pytest.param("#127", 7, id="0x007F --> 7"),
    pytest.param("#-1", 16, id="0xFFFF --> 16"),
    pytest.param("#-128", 9, id="0xFF80 --> 9"),
]


@pytest.mark.parametrize("immed,expected", cases)
def test_popcount(immed, expected):
    this_prog = prog[:]
    this_prog[load_r1] = this_prog[load_r1].replace("#0x0F", immed)
    c = make_cpu(assemble(this_prog))
    while c.running:
        c.tick()
    assert c.get_reg(2) == expected
