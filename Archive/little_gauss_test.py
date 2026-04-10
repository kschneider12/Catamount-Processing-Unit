"""
Tests for little Gauss (little_gauss.asm)

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

with open("asm/little_gauss.asm") as fh:
    prog = fh.readlines()

c = make_cpu(assemble(prog))

while c.running:
    c.tick()

# At this point, CPU is halted, and we should have these values in registers:


@pytest.mark.parametrize(
    "reg,expected",
    [
        pytest.param(0, 0x0001, id="R0=0x0001 (1)"),
        pytest.param(1, 0x0064, id="R1=0x0064 (100)"),
        pytest.param(2, 0x13BA, id="R2=0x13BA (5050)"),
        pytest.param(3, 0x0064, id="R3=0x0064 (100)"),
        pytest.param(4, 0x0000, id="R4=0x0000 (0)"),
        pytest.param(5, 0x0000, id="R5=0x0000 (0)"),
        pytest.param(6, 0x0000, id="R6=0x0000 (0)"),
        pytest.param(7, 0x0000, id="R7=0x0000 (0)"),
    ],
)
def test_reg(reg, expected):
    assert c.get_reg(reg) == expected
