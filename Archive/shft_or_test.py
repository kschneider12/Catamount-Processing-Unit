"""
Tests for SHFT and OR (shft_or.asm)

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

with open("asm/shft_or.asm") as fh:
    prog = fh.readlines()

c = make_cpu(assemble(prog))

while c.running:
    c.tick()

# At this point, CPU is halted, and we should have these values in registers:
#   R1 = 3         (initial value)
#   R2 = 0x8002    (right-shift control: direction bit + amount 2)
#   R3 = 12        (3 << 2)
#   R4 = 3         (12 >> 2)
#   R5 = 15        (12 | 3)


@pytest.mark.parametrize(
    "reg,expected",
    [
        pytest.param(1, 3, id="R1=3 (initial)"),
        pytest.param(3, 12, id="R3=12 (3 << 2)"),
        pytest.param(4, 3, id="R4=3 (12 >> 2)"),
        pytest.param(5, 15, id="R5=15 (12 | 3)"),
    ],
)
def test_reg(reg, expected):
    assert c.get_reg(reg) == expected
