"""
Tests for array maximum (array_max.asm)

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

with open("asm/array_max.asm") as fh:
    prog = fh.readlines()

for load_n, line in enumerate(prog):
    if "LOADI R2" in line:
        break

# Array is always 1..N, so max = N
cases = [
    pytest.param("#1", 1, id="N=1  --> max=1"),
    pytest.param("#4", 4, id="N=4  --> max=4"),
    pytest.param("#5", 5, id="N=5  --> max=5"),
    pytest.param("#8", 8, id="N=8  --> max=8"),
    pytest.param("#10", 10, id="N=10 --> max=10"),
]


@pytest.mark.parametrize("n_str,expected", cases)
def test_array_max(n_str, expected):
    this_prog = prog[:]
    this_prog[load_n] = this_prog[load_n].replace("#8", n_str)
    c = make_cpu(assemble(this_prog))
    while c.running:
        c.tick()
    assert c.get_reg(3) == expected
