"""
Memory interface

Harvard architecture: two separate address spaces, one for data and one for
instructions. A portion of data memory is reserved for the stack (addresses
between 0xFFFF and 0xFF00).

CS 2210 Computer Organization
Clayton Cafiero <cbcafier@uvm.edu>

STARTER CODE - REPLACE THIS LINE WITH YOUR NAME HERE
"""

from constants import STACK_BASE, WORD_SIZE, STACK_TOP


class Memory:
    """Sparse word-addressable memory for Catamount PU simulation."""

    def __init__(self, default=0):
        self._cells = {}
        self.default = default
        self._write_enable = False

    def _check_addr(self, address):
        # Make sure address is positive, in the desired range,
        # otherwise raise a `ValueError`. Replace `pass` below.
        if address < 0 or address > STACK_TOP: #TODO: UPPER BOUND FUNCTIONAL? HOW DEBUG?
            raise ValueError("Address out of range")

    def write_enable(self, b):
        # Make sure `b` is a Boolean (hint: use `isinstance()).
        # If not, raise `TypeError`. If OK, then set
        # `_write_enable` accordingly. Replace `pass` below.
        if isinstance(b, bool):
            _write_enable = b
        else:
            raise TypeError("Write enable must be bool.")

    def read(self, addr):
        """
        Return 16-bit word from memory (default if never written).
        """
        # Make sure `addr` is OK by calling `_check_addr`. If OK, return value
        # from `_cells` or default if never written. (Hint: use `.get()`.)
        self._check_addr(addr) #stops if not functional #TODO: BROKEN
        return self._cells.get(addr, 0)

    def write(self, addr, value):
        """
        Write 16-bit word to memory, masking to 16 bits.
        """
        # Check to see if `_write_enable` is true. If not, raise `RuntimeError`.
        # Otherwise, call `_check_addr()`. If OK, write masked value to the
        # selected address, then turn off `_write_enable` when done. Return
        # `True` on success. Replace `pass` below.
        if self._write_enable:
            self._check_addr(addr)
            self._cells[addr] = value
            self._write_enable = False
        else:
            raise RuntimeError(f"Write enable False. {addr}")
        return True

    def hexdump(self, start=0, stop=None, width=8):
        """
        Yield formatted lines showing memory cells in ascending order
        from `start` to the highest initialized address (or `stop` if provided).
        Uninitialized cells display as 0000.
        """
        if not self._cells:
            return  # nothing to show

        highest = max(self._cells)
        end = highest + 1 if stop is None else min(stop, highest + 1)

        for base in range(start, end, width):
            row = []
            for offset in range(width):
                addr = base + offset
                if addr >= end:
                    break
                val = self._cells.get(addr, 0)
                row.append(f"{val:04X}")
            yield f"{base:04X}: {' '.join(row)}"

    def __len__(self):
        return len(self._cells)

    def __contains__(self, addr):
        return addr in self._cells


class DataMemory(Memory):
    """
    Word-addressable memory for data. Reserves a portion for stack use.
    """

    def write(self, addr, value, from_stack=False):
        if addr >= STACK_BASE and not from_stack:
            raise RuntimeError(f"Write to stack region {addr:#06x} disallowed.")
        super().write(addr, value)
        return True


class InstructionMemory(Memory):
    """
    Word-addressable memory for instructions. Load once, then read-only
    thereafter.
    """

    def write(self, addr, value):
        """
        Prevent runtime writes to instruction memory.
        """
        raise RuntimeError("Cannot write to instruction memory outside of loader.")

    def load_program(self, words, start_addr=0x0000):
        """
        Load list of 16-bit words into consecutive memory cells.
        If you've not seen try / finally before, it's a way to ensure
        cleanup happens even if an exception is raised.
        """
        try:
            for offset, word in enumerate(words):
                self._write_enable = True
                super().write(start_addr + offset, word)
        finally:
            self._write_enable = False


if __name__ == "__main__":
    # Quick smoke test
    dm = DataMemory()
    dm.write_enable(True)
    dm.write(0x0000, 0x1234)
    dm.write_enable(True)
    dm.write(0x00F0, 0xABCD)
    dm.write_enable(False)
    for cell in dm.hexdump():
        print(cell)
    print()
    for cell in dm.hexdump(start=0x00F0):
        print(cell)
    print()
