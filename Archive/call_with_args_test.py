"""
Tests for max of three values via subroutine call (call_with_args.asm)

CS 2210 Computer Organization
Clayton Cafiero <cbcafier@uvm.edu>
"""

import os
import sys

import pytest

module_dir = os.path.abspath(".")
sys.path.insert(0, module_dir)

from assembler import assemble  # noqa: E402
from constants import STACK_TOP  # noqa: E402
from cpu import make_cpu  # noqa: E402

with open("asm/call_with_args.asm") as fh:
    prog = fh.readlines()

for load_r1, line in enumerate(prog):
    if "LOADI R1" in line:
        break

for load_r2, line in enumerate(prog):
    if "LOADI R2" in line:
        break

for load_r5, line in enumerate(prog):
    if "LOADI R5" in line:
        break

cases = [
    pytest.param("#3", "#7", "#5", 7, id="3, 7, 5 --> 7"),
    pytest.param("#7", "#3", "#5", 7, id="7, 3, 5 --> 7"),
    pytest.param("#5", "#5", "#5", 5, id="5, 5, 5 --> 5"),
    pytest.param("#1", "#2", "#3", 3, id="1, 2, 3 --> 3"),
    pytest.param("#3", "#2", "#1", 3, id="3, 2, 1 --> 3"),
    pytest.param("#-1", "#-2", "#-3", -1, id="-1, -2, -3 --> -1"),
    pytest.param("#-5", "#0", "#5", 5, id="-5, 0, 5 --> 5"),
]


@pytest.mark.parametrize("immed_a,immed_b,immed_c,expected", cases)
def test_max3(immed_a, immed_b, immed_c, expected):
    this_prog = prog[:]
    this_prog[load_r1] = this_prog[load_r1].replace("#3", immed_a)
    this_prog[load_r2] = this_prog[load_r2].replace("#7", immed_b)
    this_prog[load_r5] = this_prog[load_r5].replace("#5", immed_c)
    c = make_cpu(assemble(this_prog))
    while c.running:
        c.tick()
    assert c.get_reg(3) == expected
    assert c.sp == STACK_TOP  # stack balanced after two calls
