"""
Tests for linear.asm

CS 2210 Computer Organization
Clayton Cafiero <cbcafier@uvm.edu>
"""

import os
import sys

module_dir = os.path.abspath(".")
sys.path.insert(0, module_dir)

from assembler import assemble  # noqa: E402
from cpu import make_cpu  # noqa: E402

with open("asm/linear.asm") as fh:
    prog = fh.readlines()

c = make_cpu(assemble(prog))
print(assemble(prog))

counter = 0

while c.running:
    c.tick()
    counter += 1


def test_counter():
    assert counter == 6  # Lame, but roll with it.


def test_registers():
    assert c.get_reg(1) == 1
    assert c.get_reg(2) == 2
    assert c.get_reg(3) == 3
    assert c.get_reg(4) == 4
    assert c.get_reg(5) == 14
