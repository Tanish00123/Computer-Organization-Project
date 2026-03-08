from register_map import RegisterEncoder
from instruction_metadata import InstructionMetadata

class InstructionEncoder:
    def __init__(self):
        self.register_encoder = RegisterEncoder()
        self.metadata = InstructionMetadata()

    def convert_immediate(self, value, bit_width):

        min_val = -(1 << (bit_width - 1))
        max_val = (1 << (bit_width - 1)) - 1

        if value < min_val or value > max_val:
            raise KeyError(
                f"Immediate value {value} out of range for {bit_width}-bit signed field"
            )

        if value < 0:
            value = (1 << bit_width) + value

        return format(value, f"0{bit_width}b")
    
# B-Type Encoding
# Format: imm[12] | imm[10:5] | rs2 | rs1 | funct3 | imm[4:1] | imm[11] | opcode

def encode_b_type(self, name, rs1, rs2, imm_value):

    data = self.metadata.instruction_info(name)

    if data["type"] != "B":
        raise KeyError(f"{name} is not a B-type instruction")

    funct3 = data["funct3"]
    opcode = data["opcode"]

    # B-type uses 13-bit immediate internally
    imm_bin = self.convert_immediate(int(imm_value), 13)

    imm12 = imm_bin[0]
    imm10_5 = imm_bin[2:8]
    imm4_1 = imm_bin[8:12]
    imm11 = imm_bin[1]

    rs1_bin = self.register_encoder.get_binary(rs1)
    rs2_bin = self.register_encoder.get_binary(rs2)

    binary_instruction = (
        imm12 +
        imm10_5 +
        rs2_bin +
        rs1_bin +
        funct3 +
        imm4_1 +
        imm11 +
        opcode
    )

    if len(binary_instruction) != 32:
        raise KeyError("B-type instruction is not 32 bits")

    return binary_instruction

# Testing 
if __name__ == "__main__":
    encoder = InstructionEncoder()

#Test B-Type encoder
print("\nB-Type Test:")
print(encoder.encode_b_type("beq", "s1", "s2", 8))
print(encoder.encode_b_type("bne", "a0", "a1", -4))

