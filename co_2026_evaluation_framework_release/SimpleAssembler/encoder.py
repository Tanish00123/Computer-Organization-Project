# Encoder

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
    
    # R-Type Encoding
    # Format: funct7 | rs2 | rs1 | funct3 | rd | opcode
    
    def encode_r_type(self, name, rd, rs1, rs2):

        # Get instruction metadata
        data = self.metadata.instruction_info(name)

        if data["type"] != "R":
            raise KeyError(f"{name} is not an R-type instruction")

        opcode = data["opcode"]
        funct3 = data["funct3"]
        funct7 = data["funct7"]

        # Getting register binary form
        rd_binary = self.register_encoder.get_binary(rd)
        rs1_binary = self.register_encoder.get_binary(rs1)
        rs2_binary = self.register_encoder.get_binary(rs2)

        # Constructing instruction according to the instruction format
        binary_instruction = (funct7 +rs2_binary +rs1_binary +funct3 +rd_binary +opcode)

        if len(binary_instruction) != 32:
            raise KeyError("Generated instruction is not 32 bits")

        return binary_instruction

    #I-Type Encoding
    #Format: imm[11:0] | rs1 | funct3 | rd | opcode
       
    def encode_i_type(self, name, rd, rs1, imm_value):

        data = self.metadata.instruction_info(name)

        if data["type"] != "I":
            raise KeyError(f"{name} is not an I-type instruction")

        funct3 = data["funct3"]
        opcode = data["opcode"]

        imm_binary = self.convert_immediate(int(imm_value), 12)

        rd_bin = self.register_encoder.get_binary(rd)
        rs1_bin = self.register_encoder.get_binary(rs1)

        binary_instruction = (imm_binary +rs1_bin +funct3 +rd_bin +opcode)

        if len(binary_instruction) != 32:
            raise KeyError("I-type instruction is not 32 bits")

        return binary_instruction

    #S-Type Encoding
    # Format: imm[11:5] | rs2 | rs1 | funct3 | imm[4:0] | opcode

    def encode_s_type(self, name, rs2, rs1, imm_value):

        data = self.metadata.instruction_info(name)

        if data["type"] != "S":
            raise KeyError(f"{name} is not an S-type instruction")

        funct3 = data["funct3"]
        opcode = data["opcode"]

        imm_bin = self.convert_immediate(int(imm_value), 12)

        imm_upper = imm_bin[:7]   # bits [11:5]
        imm_lower = imm_bin[7:]   # bits [4:0]

        rs1_bin = self.register_encoder.get_binary(rs1)
        rs2_bin = self.register_encoder.get_binary(rs2)

        binary_instruction = (imm_upper +rs2_bin +rs1_bin +funct3 +imm_lower +opcode)

        if len(binary_instruction) != 32:
            raise KeyError("S-type instruction is not 32 bits")

        return binary_instruction
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

if __name__ == "__main__":
    encoder = InstructionEncoder()

    # Test R-Type encoder
    print("R-Type Test:")
    print(encoder.encode_r_type("add", "s1", "s2", "s3"))

    #Test I-Type encoder
    print("\nI-Type Test:")
    print(encoder.encode_i_type("addi", "s1", "s2", -5))

    #Test S-Type encoder
    print("\nS-Type Test:")
    print(encoder.encode_s_type("sw", "ra", "sp", 32))


    #Test B-Type encoder
    print("\nB-Type Test:")
    print(encoder.encode_b_type("beq", "s1", "s2", 8))
    print(encoder.encode_b_type("bne", "a0", "a1", -4))






    #Testing immediate function
    '''print(InstructionEncoder.convert_immediate(10, 12))    # Expected Output ----> 000000001010
       print(InstructionEncoder.convert_immediate(-5, 12))    # Expected Output ----> 111111111011
       print(InstructionEncoder.convert_immediate(2047, 12))  # Expected Output ----> 011111111111'''

