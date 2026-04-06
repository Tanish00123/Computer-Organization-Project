def to_signed32(val):
    val = val & 0xFFFFFFFF
    if val & 0x80000000:
        val -= 0x100000000
    return val

def to_unsigned32(val):
    return val & 0xFFFFFFFF

def write_reg(regs, rd, value):
    if rd != 0:
        regs[rd] = to_signed32(value)

class Executor:
    def __init__(self, regs, memory):
        #regs   : list of 32 ints as in the register file (from memory.init_registers())
        #memory : memory instance (from memory.Memory())
        self.regs = regs
        self.mem  = memory

    def execute(self, decoded, pc):
        t = decoded["type"]
        f3 = decoded["funct3"]
        f7 = decoded["funct7"]
        rd = decoded["rd"]
        rs1 = decoded["rs1"]
        rs2 = decoded["rs2"]
        imm = decoded["imm"]
        opcode = decoded["opcode"]

        r1 = to_signed32(self.regs[rs1])
        r2 = to_signed32(self.regs[rs2])
        next_pc = pc + 4   

        #R-Type 
        if t == "R":
            if f3 == "000" and f7 == "0000000":   
                write_reg(self.regs, rd, r1 + r2)

            elif f3 == "000" and f7 == "0100000":   
                write_reg(self.regs, rd, r1 - r2)

            elif f3 == "001" and f7 == "0000000":   
                shamt = to_unsigned32(r2) & 0x1F
                write_reg(self.regs, rd, r1 << shamt)

            elif f3 == "010" and f7 == "0000000":   
                write_reg(self.regs, rd, 1 if r1 < r2 else 0)

            elif f3 == "011" and f7 == "0000000":   
                write_reg(self.regs, rd, 1 if to_unsigned32(r1) < to_unsigned32(r2) else 0)

            elif f3 == "100" and f7 == "0000000":   
                write_reg(self.regs, rd, r1^r2)

            elif f3 == "101" and f7 == "0000000":   
                shamt = to_unsigned32(r2) & 0x1F
                write_reg(self.regs, rd, to_unsigned32(r1) >> shamt)

            elif f3 == "110" and f7 == "0000000":   
                write_reg(self.regs, rd, r1 | r2)

            elif f3 == "111" and f7 == "0000000":   
                write_reg(self.regs, rd, r1 & r2)

            else:
                raise RuntimeError(f"Unknown R type:  funct3={f3} funct7={f7} at PC=0x{pc:08X}")

        #I-Type 
        elif t == "I":
            #lw with opcode = 0000011
            if opcode == "0000011" and f3 == "010":
                addr = to_unsigned32(r1 + imm)
                write_reg(self.regs, rd, self.mem.lw(addr))

            #addi with opcode = 0010011 and funct3 = 000
            elif opcode == "0010011" and f3 == "000":
                write_reg(self.regs, rd, r1 + imm)

            #sltiu with opcode = 0010011 and funct3 = 011
            elif opcode == "0010011" and f3 == "011":
                write_reg(self.regs, rd, 1 if to_unsigned32(r1) < to_unsigned32(imm) else 0)

            #jalr with opcode = 1100111 and funct3 = 000
            elif opcode == "1100111" and f3 == "000":
                return_addr = pc + 4
                target = to_unsigned32(r1 + imm) & ~1   # clear LSB
                write_reg(self.regs, rd, return_addr)
                next_pc = target

            else:
                raise RuntimeError(f"Unknown I type: opcode={opcode} funct3={f3} at PC=0x{pc:08X}")

        #0S Type 
        elif t == "S":
            #sw with funct3 = 010
            if f3 == "010":
                addr = to_unsigned32(r1 + imm)
                self.mem.sw(addr, to_unsigned32(r2))
            else:
                raise RuntimeError(f"Unknown S type: funct3={f3} at PC=0x{pc:08X}")

        #B Type 
        elif t == "B":
            taken = False
            if   f3 == "000":   # beq
                taken = (r1 == r2)
            elif f3 == "001":   # bne
                taken = (r1 != r2)
            elif f3 == "100":   # blt (signed)
                taken = (r1 < r2)
            elif f3 == "101":   # bge (signed)
                taken = (r1 >= r2)
            elif f3 == "110":   # bltu (unsigned)
                taken = (to_unsigned32(r1) < to_unsigned32(r2))
            elif f3 == "111":   # bgeu (unsigned)
                taken = (to_unsigned32(r1) >= to_unsigned32(r2))
            else:
                raise RuntimeError(f"Unknown B-type: funct3={f3} at PC=0x{pc:08X}")

            if taken:
                next_pc = pc + imm   

        #U Type
        elif t == "U":
            if opcode == "0110111":   # lui
                # imm already has lower 12 bits = 0 from decoder
                write_reg(self.regs, rd, to_signed32(imm))

            elif opcode == "0010111":  # auipc
                write_reg(self.regs, rd, to_signed32(pc + imm))

            else:
                raise RuntimeError(f"Unknown U-type: opcode={opcode} at PC=0x{pc:08X}")

        #J Type
        elif t == "J":
            return_addr = pc + 4
            target = pc + imm          
            write_reg(self.regs, rd, return_addr)
            next_pc = target

        else:
            raise RuntimeError(f"Unknown instruction type '{t}' at PC=0x{pc:08X}")

        return next_pc

    def is_virtual_halt(self, decoded):
        if decoded["type"] != "B":
            return False
        if decoded["funct3"] != "000":
            return False
        if decoded["rs1"] != 0:
            return False
        if decoded["rs2"] != 0:
            return False
        if decoded["imm"] != 0:
            return False
        else:
            return True