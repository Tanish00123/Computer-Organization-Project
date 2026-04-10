OPCODE_TYPE = {
    "0110011": "R",
    "0010011": "I",
    "0000011": "I",
    "1100111": "I",
    "0100011": "S",
    "1100011": "B",
    "0110111": "U",
    "0010111": "U",
    "1101111": "J",
}

class InstructionDecoder:
    def __init__(self):
        self.program_memory = []  

    def load_file(self, file_path):
        with open(file_path, "r") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    self.program_memory.append(line)

    def sign_extend(self, value, bits):
        sign_bit = 1 << (bits - 1)
        if value & sign_bit:
            return value - (1 << bits)
        return value

    def get_immediate(self, instr, itype):
        if itype == "I":
            raw = int(instr[0:12], 2)
            return self.sign_extend(raw, 12)

        elif itype == "S":
            raw = int(instr[0:7] + instr[20:25], 2)
            return self.sign_extend(raw, 12)

        elif itype == "B":
            bits13 = instr[0] + instr[24] + instr[1:7] + instr[20:24] + "0"
            return self.sign_extend(int(bits13, 2), 13)

        elif itype == "U":
            raw = int(instr[0:20] + "0" * 12, 2)
            return self.sign_extend(raw, 32)

        elif itype == "J":
            bits21 = instr[0] + instr[12:20] + instr[11] + instr[1:11] + "0"
            return self.sign_extend(int(bits21, 2), 21)

        return 0

    def decode_one(self, instr):
        opcode= instr[25:32]
        rd= int(instr[20:25], 2)
        funct3= instr[17:20]
        rs1= int(instr[12:17], 2)
        rs2= int(instr[7:12],  2)
        funct7= instr[0:7]

        itype= OPCODE_TYPE.get(opcode, "UNKNOWN")
        imm= self.get_immediate(instr, itype)

        return {"opcode": opcode,"rd":rd,"funct3": funct3,"rs1": rs1,"rs2":rs2,"funct7": funct7,"type":itype,"imm":imm}

    def decode_all(self):
        return [self.decode_one(instr) for instr in self.program_memory]
