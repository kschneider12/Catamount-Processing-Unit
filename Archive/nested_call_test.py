"""
Tests for nested CALL (nested_call.asm)

CS 2210 Computer Organization
Clayton Cafiero <cbcafier@uvm.edu>
"""

import os
import sys

module_dir = os.path.abspath(".")
sys.path.insert(0, module_dir)

from assembler import assemble  # noqa: E402
from constants import STACK_TOP  # noqa: E402
from cpu import make_cpu  # noqa: E402

with open("asm/nested_call.asm") as fh:
    prog = fh.readlines()

c = make_cpu(assemble(prog))

while c.running:
    c.tick()


def test_halts():
    assert not c.running


def test_stack_balanced():
    assert c.sp == STACK_TOP


def test_no_registers_modified():
    for r in range(8):
        assert c.get_reg(r) == 0
