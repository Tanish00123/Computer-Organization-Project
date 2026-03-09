from encoder import InstructionEncoder
import sys


class Assembler:
    def __init__(self):
        self.encoder = InstructionEncoder()

    def parse_line(self, line):
        line = line.strip()

        if line == "" or line.startswith("#"):
            return None

        if "#" in line:
            line = line[:line.index("#")].strip()
            if line == "":
                return None

        label = None
        if ":" in line:
            potential_label, _, rest = line.partition(":")
            if (" " not in potential_label and "\t" not in potential_label
                    and potential_label
                    and potential_label[0].isalpha()
                    and potential_label.replace("_", "").isalnum()):
                label = potential_label
                line = rest.strip()

        if line == "":
            return label, None, []

        line = line.replace(",", " ")
        parts = line.split()

        instruction = parts[0]

        return label, instruction, parts[1:]

    def assemble_instruction(self, instruction, operands):

        if instruction in ["add", "sub", "sll", "slt", "sltu", "xor", "srl", "or", "and"]:
            rd, rs1, rs2 = operands
            return self.encoder.encode_r_type(instruction, rd, rs1, rs2)

        elif instruction in ["addi", "sltiu", "jalr"]:
            rd, rs1, imm = operands
            return self.encoder.encode_i_type(instruction, rd, rs1, imm)

        elif instruction == "lw":
            rd = operands[0]
            offset, rs1 = operands[1].replace(")", "").split("(")
            return self.encoder.encode_i_type(instruction, rd, rs1, offset)

        elif instruction == "sw":
            rs2 = operands[0]
            offset, rs1 = operands[1].replace(")", "").split("(")
            return self.encoder.encode_s_type(instruction, rs2, rs1, offset)

        elif instruction in ["beq", "bne", "blt", "bge", "bltu", "bgeu"]:
            rs1, rs2, imm = operands
            return self.encoder.encode_b_type(instruction, rs1, rs2, imm)

        elif instruction in ["lui", "auipc"]:
            rd, imm = operands
            return self.encoder.encode_u_type(instruction, rd, imm)

        elif instruction == "jal":
            rd, imm = operands
            return self.encoder.encode_j_type(instruction, rd, imm)

        else:
            raise ValueError(f"Unsupported instruction: '{instruction}'")