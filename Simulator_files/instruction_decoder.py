class instruction_decoder:
    def __init__(self):
        self.program_memory = []


    def load_program(self, file_name):
        with open(file_name, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    self.program_memory.append(line)


    def get_bits(self, instr, start, end):
        return instr[31-end:32-start]

    def bin_to_int(self, b):
        return int(b, 2)

    def sign_extend(self, value, bits):
        if value & (1 << (bits - 1)):
            return value - (1 << bits)
        return value

    def get_type(self, opcode):
        opcode_map = {"0110011": "R","0010011": "I","0000011": "I","1100111": "I","0100011": "S","1100011": "B","0110111": "U","0010111": "U","1101111": "J"}
        return opcode_map.get(opcode, "UNKNOWN")


    def get_immediate(self, instr, instr_type):
        if instr_type == "I":
            imm = instr[0:12]
            return self.sign_extend(int(imm, 2), 12)

        elif instr_type == "S":
            imm = instr[0:7] + instr[20:25]
            return self.sign_extend(int(imm, 2), 12)

        elif instr_type == "B":
            # imm[12|10:5|4:1|11]
            imm = (instr[0] +instr[24] +instr[1:7] +instr[20:24] +"0")
            return self.sign_extend(int(imm, 2), 13)

        elif instr_type == "U":
            imm = instr[0:20] + "000000000000"
            return int(imm, 2)

        elif instr_type == "J":
            imm = (instr[0] +instr[12:20] +instr[11] +instr[1:11] +"0")
            return self.sign_extend(int(imm, 2), 21)
        return None


    def decode_instruction(self, instr):
        decoded = {}

        decoded["opcode"] = instr[25:32]
        decoded["rd"] = self.bin_to_int(instr[20:25])
        decoded["funct3"] = instr[17:20]
        decoded["rs1"] = self.bin_to_int(instr[12:17])
        decoded["rs2"] = self.bin_to_int(instr[7:12])
        decoded["funct7"] = instr[0:7]

        instr_type = self.get_type(decoded["opcode"])
        decoded["type"] = instr_type
        decoded["imm"] = self.get_immediate(instr, instr_type)
        return decoded

    def decode_program(self):
        decoded_program = []
        for instr in self.program_memory:
            decoded_program.append(self.decode_instruction(instr))
        return decoded_program