"""
Tests for in-memory swap using a temporary register (swap.asm)

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

with open("asm/swap.asm") as fh:
    prog = fh.readlines()

for load_r2, line in enumerate(prog):
    if "LOADI R2" in line:
        break

for load_r3, line in enumerate(prog):
    if "LOADI R3" in line:
        break

# Each case: (a, b) -- initial M[0]=a, M[1]=b; after swap M[0]=b, M[1]=a
cases = [
    pytest.param("#42", "#99", 42, 99, id="42, 99"),
    pytest.param("#0", "#1", 0, 1, id="0, 1"),
    pytest.param("#5", "#5", 5, 5, id="5, 5 (equal)"),
    pytest.param("#1", "#100", 1, 100, id="1, 100"),
]


@pytest.mark.parametrize("immed_a,immed_b,a,b", cases)
def test_swap(immed_a, immed_b, a, b):
    this_prog = prog[:]
    this_prog[load_r2] = this_prog[load_r2].replace("#42", immed_a)
    this_prog[load_r3] = this_prog[load_r3].replace("#99", immed_b)
    c = make_cpu(assemble(this_prog))
    while c.running:
        c.tick()
    assert c._d_mem.read(0) == b  # M[0] now holds original M[1]
    assert c._d_mem.read(1) == a  # M[1] now holds original M[0]
