# Encoder

from register_map import RegisterEncoder
from instruction_metadata import InstructionMetadata


class InstructionEncoder:
    def __init__(self):
        self.register_encoder = RegisterEncoder()
        self.metadata = InstructionMetadata()

    def convert_immediate(self, value, bit_width):
        """
        Converts signed integer into fixed-width 2's complement binary string.
        Raises error if value exceeds allowed signed range.
        """

        min_val = -(1 << (bit_width - 1))
        max_val = (1 << (bit_width - 1)) - 1

        # Range check
        if value < min_val or value > max_val:
            raise ValueError(
                f"Immediate value {value} out of range for {bit_width}-bit signed field"
            )

        # If negative, convert using 2's complement
        if value < 0:
            value = (1 << bit_width) + value

        return format(value, f"0{bit_width}b")
    
    # R-Type Encoding
    # Format: funct7 | rs2 | rs1 | funct3 | rd | opcode
    
    def encode_r_type(self, mnemonic, rd, rs1, rs2):
        """
        Encodes an R-type instruction into 32-bit binary string.
        Example: add s1,s2,s3
        """

        # Get instruction metadata
        info = self.metadata.get_instruction_info(mnemonic)

        if info["type"] != "R":
            raise ValueError(f"{mnemonic} is not an R-type instruction")

        opcode = info["opcode"]
        funct3 = info["funct3"]
        funct7 = info["funct7"]

        # Get register binaries
        rd_bin = self.register_encoder.get_register_binary(rd)
        rs1_bin = self.register_encoder.get_register_binary(rs1)
        rs2_bin = self.register_encoder.get_register_binary(rs2)

        # Construct instruction
        binary_instruction = (funct7 +rs2_bin +rs1_bin +funct3 +rd_bin +opcode)

        if len(binary_instruction) != 32:
            raise ValueError("Generated instruction is not 32 bits")

        return binary_instruction

    #I-Type Encoding
    #Format: imm[11:0] | rs1 | funct3 | rd | opcode
       
    def encode_i_type(self, mnemonic, rd, rs1, imm_value):

        info = self.metadata.get_instruction_info(mnemonic)

        if info["type"] != "I":
            raise ValueError(f"{mnemonic} is not an I-type instruction")

        funct3 = info["funct3"]
        opcode = info["opcode"]

        imm_bin = self.convert_immediate(int(imm_value), 12)

        rd_bin = self.register_encoder.get_register_binary(rd)
        rs1_bin = self.register_encoder.get_register_binary(rs1)

        binary_instruction = (imm_bin +rs1_bin +funct3 +rd_bin +opcode)

        if len(binary_instruction) != 32:
            raise ValueError("I-type instruction is not 32 bits")

        return binary_instruction

    #S-Type Encoding
    # Format: imm[11:5] | rs2 | rs1 | funct3 | imm[4:0] | opcode

    def encode_s_type(self, mnemonic, rs2, rs1, imm_value):

        info = self.metadata.get_instruction_info(mnemonic)

        if info["type"] != "S":
            raise ValueError(f"{mnemonic} is not an S-type instruction")

        funct3 = info["funct3"]
        opcode = info["opcode"]

        imm_bin = self.convert_immediate(int(imm_value), 12)

        imm_upper = imm_bin[:7]   # bits [11:5]
        imm_lower = imm_bin[7:]   # bits [4:0]

        rs1_bin = self.register_encoder.get_register_binary(rs1)
        rs2_bin = self.register_encoder.get_register_binary(rs2)

        binary_instruction = (
            imm_upper +
            rs2_bin +
            rs1_bin +
            funct3 +
            imm_lower +
            opcode
        )

        if len(binary_instruction) != 32:
            raise ValueError("S-type instruction is not 32 bits")

        return binary_instruction


# Testing 
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



    #Testing immediate function
    '''print(InstructionEncoder.convert_immediate(10, 12))    # Expected Output ----> 000000001010
       print(InstructionEncoder.convert_immediate(-5, 12))    # Expected Output ----> 111111111011
       print(InstructionEncoder.convert_immediate(2047, 12))  # Expected Output ----> 011111111111'''

