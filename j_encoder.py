def encode_j_type(self, name, rd, imm_value):
        data = self.metadata.instruction_info(name)

        if data["type"] != "J":
            raise KeyError(f"{name} is not a J type instruction")

        opcode = data["opcode"]

        imm_int = int(imm_value)
        if imm_int % 2 != 0:
            raise KeyError(f"jal offset must be even")

        immJ = self.convert_immediate(imm_int, 21)

        if len(immJ) != 21:
            raise KeyError("Immediate out of 21 bit range")

        imm20    = immJ[0]        # bit 20
        imm10_1  = immJ[10:20]   # bits 10:1
        imm11    = immJ[9]        # bit 11
        imm19_12 = immJ[1:9]     # bits 19:12

        rd_j = self.register_encoder.get_binary(rd)
        j_instruction = (imm20 + imm10_1 + imm11 + imm19_12 + rd_j + opcode)

        if len(j_instruction) != 32:
            raise KeyError("J type instruction is not 32 bits")

        return j_instruction