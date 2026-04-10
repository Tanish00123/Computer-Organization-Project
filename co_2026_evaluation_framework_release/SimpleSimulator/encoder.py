from memory import InvalidMemAccess

def to_u32(val):
    return val & 0xFFFFFFFF

def to_s32(val):
    val = to_u32(val)
    return val - 0x100000000 if val >= 0x80000000 else val

def set_reg(regs, rd, value):
    if rd != 0:
        regs[rd] = to_s32(value)

class Executor:
    def __init__(self, regs, memory):
        self.regs = regs
        self.mem  = memory

    def execute(self, decoded, pc):
        t= decoded["type"]
        f3= decoded["funct3"]
        f7= decoded["funct7"]
        rd= decoded["rd"]
        rs1= decoded["rs1"]
        rs2= decoded["rs2"]
        imm= decoded["imm"]
        opcode= decoded["opcode"]

        a= to_s32(self.regs[rs1])   
        b= to_s32(self.regs[rs2])   
        ua= to_u32(self.regs[rs1])   
        ub= to_u32(self.regs[rs2])   
        npc= pc + 4                  

        if t == "R":
            shamt= ub & 0x1F
            if f3== "000" and f7== "0000000":set_reg(self.regs, rd, a + b)
            elif f3== "000" and f7== "0100000":set_reg(self.regs, rd, a - b)
            elif f3== "001" and f7== "0000000":set_reg(self.regs, rd, ua << shamt)
            elif f3== "010" and f7== "0000000":set_reg(self.regs, rd, 1 if a < b else 0)
            elif f3== "011" and f7== "0000000":set_reg(self.regs, rd, 1 if ua < ub else 0)
            elif f3== "100" and f7== "0000000":set_reg(self.regs, rd, a ^ b)
            elif f3== "101" and f7== "0000000":set_reg(self.regs, rd, ua >> shamt)
            elif f3== "101" and f7== "0100000":set_reg(self.regs, rd, a >> shamt)   
            elif f3== "110" and f7== "0000000":set_reg(self.regs, rd, a | b)
            elif f3== "111" and f7== "0000000":set_reg(self.regs, rd, a & b)

        elif t == "I":
            shamt = imm & 0x1F
            i_f7  = decoded["funct7"]

            if opcode == "0000011":          
                if f3 == "010":             
                    addr = to_u32(a + imm)
                    val  = self.mem.lw(addr) 
                    set_reg(self.regs, rd, val)

            elif opcode=="0010011":
                if f3 == "000": set_reg(self.regs, rd, a + imm)
                elif f3== "001":set_reg(self.regs, rd, ua << shamt)          
                elif f3== "010":set_reg(self.regs, rd, 1 if a < imm else 0)  
                elif f3== "011":set_reg(self.regs, rd, 1 if ua < to_u32(imm) else 0)  
                elif f3== "100":set_reg(self.regs, rd, a ^ imm)   
                elif f3== "101" and i_f7 == "0000000": set_reg(self.regs, rd, ua >> shamt)       
                elif f3== "101" and i_f7 == "0100000": set_reg(self.regs, rd, a >> shamt)         
                elif f3== "110":set_reg(self.regs, rd, a | imm)              
                elif f3== "111":set_reg(self.regs, rd, a & imm)              

            elif opcode == "1100111":       
                if f3 == "000":
                    target = to_u32(a + imm) & 0xFFFFFFFE   
                    set_reg(self.regs, rd, pc + 4)
                    npc = target

        elif t == "S":
            if f3 == "010":                  
                addr = to_u32(a + imm)
                self.mem.sw(addr, to_u32(b))

        # ── B-type ──────────────────────────────────────
        elif t == "B":
            taken = False
            if   f3 == "000":  taken = (a  == b)
            elif f3 == "001":  taken = (a  != b)
            elif f3 == "100":  taken = (a  <  b)
            elif f3 == "101":  taken = (a  >= b)
            elif f3 == "110":  taken = (ua <  ub)
            elif f3 == "111":  taken = (ua >= ub)
            if taken:
                npc = pc + imm

        # ── U-type ────────────────────────────────
        elif t == "U":
            if opcode == "0110111":          # lui
                set_reg(self.regs, rd, to_s32(imm))
            elif opcode == "0010111":        # auipc
                set_reg(self.regs, rd, pc + imm)

        # ── J-type ───────────────────────────
        elif t == "J":                      
            set_reg(self.regs, rd, pc + 4)
            npc = pc + imm
        self.regs[0] = 0
        return npc

    def is_halt(self, decoded):
        return (decoded["type"]== "B" and decoded["funct3"] == "000" and decoded["rs1"]== 0 and decoded["rs2"]== 0 and decoded["imm"]== 0)
