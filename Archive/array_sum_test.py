"""
Tests for array sum (array_sum.asm)

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

with open("asm/array_sum.asm") as fh:
    prog = fh.readlines()

for load_n, line in enumerate(prog):
    if "LOADI R2" in line:
        break

# Sum of 1..N = N*(N+1)/2
cases = [
    pytest.param("#1", 1, id="N=1  --> 1"),
    pytest.param("#4", 10, id="N=4  --> 10"),
    pytest.param("#5", 15, id="N=5  --> 15"),
    pytest.param("#8", 36, id="N=8  --> 36"),
    pytest.param("#10", 55, id="N=10 --> 55"),
]


@pytest.mark.parametrize("n_str,expected", cases)
def test_array_sum(n_str, expected):
    this_prog = prog[:]
    this_prog[load_n] = this_prog[load_n].replace("#8", n_str)
    c = make_cpu(assemble(this_prog))
    while c.running:
        c.tick()
    assert c.get_reg(3) == expected
