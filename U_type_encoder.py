# U-Type Encoding
    # Format: imm[31:12] | rd | opcode
    
def encode_u_type(self, name, rd, imm_value):
        data = self.metadata.instruction_info(name)

        if data["type"] != "U":
            raise KeyError(f"{name} is not a U type instruction")

        opcode = data["opcode"]

        # Replaced custom broken validation with your working converter
        imm_binary = self.convert_immediate(int(imm_value), 20)

        rd_bin = self.register_encoder.get_binary(rd)

        binary_instruction = imm_binary + rd_bin + opcode

        if len(binary_instruction) != 32:
            raise KeyError("U-type instruction is not 32 bits")

        return binary_instruction