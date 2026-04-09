PROG_START  = 0x00000000
PROG_END    = 0x000000FF

STACK_START = 0x00000100
STACK_END   = 0x0000017F

DATA_START  = 0x00010000
DATA_END    = 0x0001007F

SP_INIT     = 0x0000017C


class Memory:
    def __init__(self):
        # 64 slots for instructions
        self.prog=[0]*64
        
        self.stack=[0]*32
        self.data=[0]*32

    def _aligned(self, addr):
  
        if addr % 4!=0:
            raise MemoryError(f"Misaligned address: 0x{addr:08X}")

    def _find_region(self, addr):
        self._aligned(addr)

        if PROG_START<=addr<=PROG_END:
            return self.prog,(addr-PROG_START)//4

        if STACK_START<=addr<=STACK_END:
            return self.stack,(addr-STACK_START)//4

        if DATA_START<=addr<=DATA_END:
            return self.data,(addr-DATA_START)//4

       
        raise MemoryError(f"Invalid address: 0x{addr:08X}")

    def lw(self,addr):
        region,idx=self._find_region(addr)
        val=region[idx] & 0xFFFFFFFF

        
        if val & 0x80000000:
            val -= 0x100000000

        return val

    def sw(self,addr,val):
        region,idx=self._find_region(addr)
        region[idx]=val & 0xFFFFFFFF

    def load_program(self,instructions):
        if len(instructions)>64:
            raise MemoryError("Too many instructions — program memory is only 64 slots")

        for i,instr in enumerate(instructions):
            self.prog[i]=instr & 0xFFFFFFFF

    def fetch(self,pc):
        if not (PROG_START<=pc<=PROG_END):
            raise MemoryError(f"PC jumped outside program memory: 0x{pc:08X}")

        self._aligned(pc)
        return self.prog[(pc-PROG_START)//4] & 0xFFFFFFFF

    def dump_data(self):
        
        result=[]
        for i in range(32):
            addr = DATA_START+i*4
            result.append((f"0x{addr:08X}", format(self.data[i] & 0xFFFFFFFF, '032b')))
        return result


def init_registers():
    regs=[0]*32
    regs[2]=SP_INIT   
    return regs