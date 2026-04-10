"""
Tests for iterative Fibonacci (fibonacci.asm)

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

with open("asm/fibonacci.asm") as fh:
    prog = fh.readlines()

c = make_cpu(assemble(prog))

while c.running:
    c.tick()

FIBS = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]

cases = [
    pytest.param(addr, val, id=f"M[{addr}]=F({addr + 1})={val}")
    for addr, val in enumerate(FIBS)
]


@pytest.mark.parametrize("addr,expected", cases)
def test_fibonacci(addr, expected):
    assert c._d_mem.read(addr) == expected
