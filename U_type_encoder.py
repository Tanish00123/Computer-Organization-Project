def encode_u_type(self, name, rd, imm_value):
    data = self.metadata.instruction_info(name)
    if data["type"] != "U":
        raise KeyError(f"{name} is not a U-type instruction")
    opcode = data["opcode"]

    imm_int = int(imm_value)
    # U-type: unsigned 20-bit, range 0 to 2^20 - 1
    if imm_int < 0 or imm_int > (1 << 20) - 1:
        raise KeyError(f"U-type immediate {imm_int} out of range")
    
    imm_binary = format(imm_int, "020b")
    rd_bin = self.register_encoder.get_binary(rd)
    binary_instruction = imm_binary + rd_bin + opcode
    
    if len(binary_instruction) != 32:
        raise KeyError("U-type instruction is not 32 bits")
    return binary_instruction