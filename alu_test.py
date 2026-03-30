"""
Tests for Catamount Processor Unit ALU

CS 2210 Computer Organization
Clayton Cafiero <cbcafier@uvm.edu>
"""

import pytest

from alu import Alu

TEST_CASES = [
    {
        "opcode": 0b000,
        "mnemonic": "ADD",
        "a": 6,
        "b": 3,
        "expected": 9,
        "flags": {
            "zero": False,
            "negative": False,
            "carry": False,
            "overflow": False,
        },
        "comment": "Basic addition, no carry or overflow.",
    },
    {
        "opcode": 0b000,
        "mnemonic": "ADD",
        "a": 0,
        "b": 0,
        "expected": 0,
        "flags": {
            "zero": True,
            "negative": False,
            "carry": False,
            "overflow": False,
        },
        "comment": "Zero result sets Z flag.",
    },
    {
        "opcode": 0b000,
        "mnemonic": "ADD",
        "a": 0xFFFF,
        "b": 1,
        "expected": 0,
        "flags": {
            "zero": True,
            "negative": False,
            "carry": True,
            "overflow": False,
        },
        "comment": "Unsigned wraparound with carry out.",
    },
    {
        "opcode": 0b000,
        "mnemonic": "ADD",
        "a": 32767,
        "b": 1,
        "expected": -32768,
        "flags": {
            "zero": False,
            "negative": True,
            "carry": False,
            "overflow": True,
        },
        "comment": "Signed overflow on positive limit.",
    },
    {
        "opcode": 0b000,
        "mnemonic": "ADD",
        "a": -1,
        "b": 1,
        "expected": 0,
        "flags": {
            "zero": True,
            "negative": False,
            "carry": True,
            "overflow": False,
        },
        "comment": "Negative plus positive cancel to zero; carry set from unsigned wrap.",
    },
    {
        "opcode": 0b000,
        "mnemonic": "ADD",
        "a": -32768,
        "b": -1,
        "expected": 32767,
        "flags": {
            "zero": False,
            "negative": False,
            "carry": True,
            "overflow": True,
        },
        "comment": "Addition of two negatives causes signed overflow to positive range.",
    },
    {
        "opcode": 0b001,
        "mnemonic": "SUB",
        "a": 3,
        "b": 3,
        "expected": 0,
        "flags": {
            "zero": True,
            "negative": False,
            "carry": True,
            "overflow": False,
        },
        "comment": "No borrow; result zero sets Z and carry.",
    },
    {
        "opcode": 0b001,
        "mnemonic": "SUB",
        "a": 3,
        "b": 5,
        "expected": -2,
        "flags": {
            "zero": False,
            "negative": True,
            "carry": False,
            "overflow": False,
        },
        "comment": "Borrow required; carry cleared, result negative.",
    },
    {
        "opcode": 0b001,
        "mnemonic": "SUB",
        "a": -32768,
        "b": 1,
        "expected": 32767,
        "flags": {
            "zero": False,
            "negative": False,
            "carry": True,
            "overflow": True,
        },
        "comment": "Signed underflow on negative limit.",
    },
    {
        "opcode": 0b001,
        "mnemonic": "SUB",
        "a": 0,
        "b": -1,
        "expected": 1,
        "flags": {
            "zero": False,
            "negative": False,
            "carry": False,
            "overflow": False,
        },
        "comment": "Subtracting a negative equals addition.",
    },
    {
        "opcode": 0b010,
        "mnemonic": "AND",
        "a": 15,
        "b": 240,
        "expected": 0,
        "flags": {
            "zero": True,
            "negative": False,
            "carry": False,
            "overflow": False,
        },
        "comment": "Non-overlapping bitmasks yield zero.",
    },
    {
        "opcode": 0b010,
        "mnemonic": "AND",
        "a": 15,
        "b": 241,
        "expected": 1,
        "flags": {
            "zero": False,
            "negative": False,
            "carry": False,
            "overflow": False,
        },
        "comment": "Overlap of LSB only.",
    },
    {
        "opcode": 0b010,
        "mnemonic": "AND",
        "a": 0xFFFF,
        "b": 0x1234,
        "expected": 0x1234,
        "flags": {
            "zero": False,
            "negative": False,
            "carry": False,
            "overflow": False,
        },
        "comment": "Mask of all ones, result identical to operand.",
    },
    {
        "opcode": 0b010,
        "mnemonic": "AND",
        "a": 0x0000,
        "b": 0xFFFF,
        "expected": 0,
        "flags": {
            "zero": True,
            "negative": False,
            "carry": False,
            "overflow": False,
        },
        "comment": "Mask of zeros yields zero result.",
    },
    {
        "opcode": 0b010,
        "mnemonic": "AND",
        "a": 0xAAAA,
        "b": 0x5555,
        "expected": 0x0000,
        "flags": {
            "zero": True,
            "negative": False,
            "carry": False,
            "overflow": False,
        },
        "comment": "Complementary bit patterns yield zero.",
    },
    {
        "opcode": 0b011,
        "mnemonic": "OR",
        "a": 85,
        "b": 42,
        "expected": 127,
        "flags": {
            "zero": False,
            "negative": False,
            "carry": False,
            "overflow": False,
        },
        "comment": "Alternating bits produce full lower byte.",
    },
    {
        "opcode": 0b011,
        "mnemonic": "OR",
        "a": 0x0000,
        "b": 0x1234,
        "expected": 0x1234,
        "flags": {
            "zero": False,
            "negative": False,
            "carry": False,
            "overflow": False,
        },
        "comment": "OR with zero preserves operand.",
    },
    {
        "opcode": 0b011,
        "mnemonic": "OR",
        "a": 0xAAAA,
        "b": 0x5555,
        "expected": -1,
        "flags": {
            "zero": False,
            "negative": True,
            "carry": False,
            "overflow": False,
        },
        "comment": "Complementary bit patterns yield all ones.",
    },
    {
        "opcode": 0b011,
        "mnemonic": "OR",
        "a": -1,
        "b": 0,
        "expected": -1,
        "flags": {
            "zero": False,
            "negative": True,
            "carry": False,
            "overflow": False,
        },
        "comment": "OR with -1 leaves operand unchanged, negative result sets N.",
    },
    {
        "opcode": 0b101,
        "mnemonic": "XOR",
        "a": 0b1010,
        "b": 0b0110,
        "expected": 0b1100,
        "flags": {
            "zero": False,
            "negative": False,
            "carry": False,
            "overflow": False,
        },
        "comment": "XOR basic: non-overlapping and overlapping bits.",
    },
    {
        "opcode": 0b101,
        "mnemonic": "XOR",
        "a": 0x1234,
        "b": 0x1234,
        "expected": 0,
        "flags": {
            "zero": True,
            "negative": False,
            "carry": False,
            "overflow": False,
        },
        "comment": "XOR of value with itself yields zero.",
    },
    {
        "opcode": 0b101,
        "mnemonic": "XOR",
        "a": 0xAAAA,
        "b": 0x5555,
        "expected": -1,
        "flags": {
            "zero": False,
            "negative": True,
            "carry": False,
            "overflow": False,
        },
        "comment": "XOR complementary patterns yield all ones; N set.",
    },
    {
        "opcode": 0b101,
        "mnemonic": "XOR",
        "a": 0x1234,
        "b": 0xFFFF,
        "expected": -0x1235,  # 0xEDCB as signed 16-bit
        "flags": {
            "zero": False,
            "negative": True,
            "carry": False,
            "overflow": False,
        },
        "comment": "XOR with all-ones inverts operand; N set from MSB.",
    },
    {
        "opcode": 0b101,
        "mnemonic": "XOR",
        "a": 0x0000,
        "b": 0x1234,
        "expected": 0x1234,
        "flags": {
            "zero": False,
            "negative": False,
            "carry": False,
            "overflow": False,
        },
        "comment": "XOR with zero preserves operand.",
    },
    {
        "opcode": 0b100,
        "mnemonic": "SHFT",
        "a": 1,
        "b": 0x8001,
        "expected": 0,
        "flags": {
            "zero": True,
            "negative": False,
            "carry": True,
            "overflow": False,
        },
        "comment": "Right shift by 1; LSB shifted out sets carry.",
    },
    {
        "opcode": 0b100,
        "mnemonic": "SHFT",
        "a": 1,
        "b": 1,
        "expected": 2,
        "flags": {
            "zero": False,
            "negative": False,
            "carry": False,
            "overflow": False,
        },
        "comment": "Left shift by 1.",
    },
    {
        "opcode": 0b100,
        "mnemonic": "SHFT",
        "a": 1,
        "b": 15,
        "expected": -32768,
        "flags": {
            "zero": False,
            "negative": True,
            "carry": False,
            "overflow": False,
        },
        "comment": "Left shift by maximum magnitude (15).",
    },
    {
        "opcode": 0b100,
        "mnemonic": "SHFT",
        "a": 1,
        "b": 100,
        "expected": 16,
        "flags": {
            "zero": False,
            "negative": False,
            "carry": False,
            "overflow": False,
        },
        "comment": "Shift count masked to 4 bits (100 -> 4). Left shift by 4.",
    },
    {
        "opcode": 0b100,
        "mnemonic": "SHFT",
        "a": 32768,
        "b": 0b1000000000001111,
        "expected": 1,
        "flags": {
            "zero": False,
            "negative": False,
            "carry": False,
            "overflow": False,
        },
        "comment": "Right shift by 15; MSB determines direction.",
    },
    {
        "opcode": 0b100,
        "mnemonic": "SHFT",
        "a": 0x1234,
        "b": 0x8000,
        "expected": 0x1234,
        "flags": {
            "zero": False,
            "negative": False,
            "carry": False,
            "overflow": False,
        },
        "comment": "MSB set but shift count = 0; no shift performed.",
    },
    {
        "opcode": 0b100,
        "mnemonic": "SHFT",
        "a": 0x8000,
        "b": 1,
        "expected": 0,
        "flags": {
            "zero": True,
            "negative": False,
            "carry": True,
            "overflow": False,
        },
        "comment": "Left shift shifts out MSB; carry set.",
    },
    {
        "opcode": 0b100,
        "mnemonic": "SHFT",
        "a": 42,
        "b": 0,
        "expected": 42,
        "flags": {
            "zero": False,
            "negative": False,
            "carry": False,
            "overflow": False,
        },
        "comment": "Zero shift leaves operand unchanged.",
    },
    {
        "opcode": 0b100,
        "mnemonic": "SHFT",
        "a": 0b0000000000000010,
        "b": 0x800F,
        "expected": 0,
        "flags": {
            "zero": True,
            "negative": False,
            "carry": False,
            "overflow": False,
        },
        "comment": "Right shift by 15 clears all bits; final bit out sets carry.",
    },
    {
        "opcode": 0b100,
        "mnemonic": "SHFT",
        "a": 0b0000000000000001,
        "b": 0xF,
        "expected": -32768,
        "flags": {
            "zero": False,
            "negative": True,
            "carry": False,
            "overflow": False,
        },
        "comment": "Left shift by 15 moves low bit to MSB; sets N flag.",
    },
    {
        "opcode": 0b100,
        "mnemonic": "SHFT",
        "a": 0x0001,
        "b": 0x8FFF,
        "expected": 0,
        "flags": {
            "zero": True,
            "negative": False,
            "carry": False,
            "overflow": False,
        },
        "comment": "Right shift by 15 with MSB=1; all bits shifted out.",
    },
]


@pytest.mark.parametrize("case", TEST_CASES, ids=[c["comment"] for c in TEST_CASES])
def test_alu_operations(case):
    """
    Verify ALU result and flags for each operation.
    """
    alu = Alu()
    alu.decode(case["opcode"])
    result = alu.execute(case["a"], case["b"])
    assert result == case["expected"], (
        f"{case['mnemonic']}({case['a']}, {case['b']}): "
        f"expected {case['expected']}, got {result}"
    )

    for flag, expected_val in case["flags"].items():
        actual_val = getattr(alu, flag)
        assert actual_val == expected_val, (
            f"{case['mnemonic']} flag {flag}: expected {expected_val}, got {actual_val}"
        )


def test_shift_behavioral_details():
    """
    Verify direction and masking logic for SHFT tests.
    A test for the tests.
    """
    for case in TEST_CASES:
        if case["mnemonic"] == "SHFT":
            b = case["b"]
            direction = "RIGHT" if (b & 0x8000) else "LEFT"
            amt = b & 0xF
            # This asserts masking rule and direction convention
            assert 0 <= amt <= 15
            assert direction in ("LEFT", "RIGHT")
