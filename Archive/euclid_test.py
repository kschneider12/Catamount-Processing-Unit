"""
Tests for Euclid's GCD (euclid.asm)

CS 2210 Computer Organization
Clayton Cafiero <cbcafier@uvm.edu>
"""

import os
import sys

import pytest


def gcd(a, b):
    assert a >= 1
    assert b >= 1
    assert isinstance(a, int)
    assert isinstance(b, int)
    while b:
        a, b = b, a % b
    return a


module_dir = os.path.abspath(".")
sys.path.insert(0, module_dir)

from assembler import assemble  # noqa: E402
from cpu import make_cpu  # noqa: E402

with open("asm/euclid.asm") as fh:
    prog = fh.readlines()

load_a = -1  # sentinel
load_b = -1  # sentinel
# brittle!
for num, line in enumerate(prog):
    if "LOADI R5" in line:
        load_a = num
    elif "LOADI R6" in line:
        load_b = num

cases = [
    pytest.param("#2", "#2", 2, id="2,2: 2"),
    pytest.param("#17", "#17", 17, id="17,17: 17"),
    pytest.param("#32", "#16", 16, id="32,16: 16"),
    pytest.param("#64", "#8", 8, id="64,8: 8"),
    pytest.param("#9", "#25", 1, id="9,25: 1"),
    pytest.param("#14", "#15", 1, id="14,15: 1"),
    pytest.param("#21", "#14", 7, id="21,14: 7"),
    pytest.param("#42", "#30", 6, id="42,30: 6"),
    pytest.param("#13", "#39", 13, id="13,39: 13"),
    pytest.param("#17", "#51", 17, id="17,51: 17"),
    pytest.param("#2", "#3", 1, id="2,3: 1"),
    pytest.param("#2", "#4", 2, id="2,4: 2"),
]


@pytest.mark.parametrize("immed_a,immed_b,expected", cases)
def test_reg(immed_a, immed_b, expected):
    this_prog = prog[:]
    this_prog[load_a] = this_prog[load_a].replace("#0x2A", immed_a)
    this_prog[load_b] = this_prog[load_b].replace("#0x5A", immed_b)
    c = make_cpu(assemble(this_prog))

    while c.running:
        c.tick()

    # At this point, CPU is halted, and we should have these values in registers:
    assert c.get_reg(5) == expected  # expected GCD
