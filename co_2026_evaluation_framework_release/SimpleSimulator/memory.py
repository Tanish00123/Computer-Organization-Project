STACK_LO= 0x00000000
STACK_HI= 0x000001FC   
DATA_LO= 0x00010000
DATA_HI= 0x0001007C   #128 bytes
DATA_WORDS= 32
SP_INIT=0x0000017C

class InvalidMemAccess(Exception):
    pass

class Memory:
    def __init__(self):
        self._words = {}

    def _check(self, addr):
        if addr % 4 != 0:
            raise InvalidMemAccess("unaligned address 0x{:08X} (must be 4-byte aligned)".format(addr))
        
        in_stack = STACK_LO <= addr <= STACK_HI
        in_data = DATA_LO  <= addr <= DATA_HI
        if not (in_stack or in_data):
            raise InvalidMemAccess(
                "out of bounds address 0x{:08X} "
                "(valid: stack 0x{:08X}-0x{:08X}, data 0x{:08X}-0x{:08X})".format(addr, STACK_LO, STACK_HI, DATA_LO, DATA_HI)
            )

    def lw(self, addr):
        self._check(addr)
        val = self._words.get(addr, 0) &0xFFFFFFFF
        if val >= 0x80000000:
            val -= 0x100000000
        return val

    def sw(self, addr, val):
        self._check(addr)
        self._words[addr] = val &0xFFFFFFFF

    def dump_data(self):
        out = []
        for i in range(DATA_WORDS):
            addr = DATA_LO + i * 4
            val = self._words.get(addr, 0) & 0xFFFFFFFF
            out.append(("0x{:08X}".format(addr), format(val, "032b")))
        return out

def init_registers():
    regs = [0]*32
    regs[2] = SP_INIT   
    return regs