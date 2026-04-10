"""
Tests for power of Two (power_of_two.asm)

CS 2210 Computer Organization
Clayton Cafiero <cbcafier@uvm.edu>
"""

import math
import os
import sys

import pytest

module_dir = os.path.abspath(".")
sys.path.insert(0, module_dir)

from assembler import assemble  # noqa: E402
from cpu import make_cpu  # noqa: E402

with open("asm/power_of_two.asm") as fh:
    prog = fh.readlines()

for num, line in enumerate(prog):
    if "LOADI R1" in line:  # this line loads test value
        break

# Generate test cases:
cases = []
for n in range(1, 17):
    immed = f"#{n}"
    # r1 holds test value
    # r2 holds counter
    # r3 unused except as dest for R1 & R2
    # r4 holds result
    # r5 holds constant 1
    r1 = n
    r4 = 0 if (math.log2(n) - int(math.log2(n))) != 0.0 else 1
    r5 = 1  # constant
    cases.append(pytest.param(immed, r1, r4, r5, id=immed))


# @pytest.mark.skip()
@pytest.mark.parametrize("immed,r1,r4,r5", cases)
def test_reg(immed, r1, r4, r5):
    this_prog = prog[:]
    this_prog[num] = this_prog[num].replace("#64", immed)
    c = make_cpu(assemble(this_prog))

    while c.running:
        c.tick()

    # At this point, CPU is halted, and we should have these values in registers:
    assert c.get_reg(1) == r1  # should match test value
    assert c.get_reg(4) == r4  # expected indicator
    assert c.get_reg(5) == r5  # expected constant
