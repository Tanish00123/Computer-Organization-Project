# Instruction metadata

class InstructionMetadata:
    def __init__(self):
        self.instructions = self._build_instruction_table()

    def _build_instruction_table(self):
        """
        Builds dictionary containing instruction encoding metadata.
        """

        instruction_table = {

            # R-Type
            "add":  {"type": "R", "opcode": "0110011", "funct3": "000", "funct7": "0000000"},
            "sub":  {"type": "R", "opcode": "0110011", "funct3": "000", "funct7": "0100000"},
            "sll":  {"type": "R", "opcode": "0110011", "funct3": "001", "funct7": "0000000"},
            "slt":  {"type": "R", "opcode": "0110011", "funct3": "010", "funct7": "0000000"},
            "sltu": {"type": "R", "opcode": "0110011", "funct3": "011", "funct7": "0000000"},
            "xor":  {"type": "R", "opcode": "0110011", "funct3": "100", "funct7": "0000000"},
            "srl":  {"type": "R", "opcode": "0110011", "funct3": "101", "funct7": "0000000"},
            "or":   {"type": "R", "opcode": "0110011", "funct3": "110", "funct7": "0000000"},
            "and":  {"type": "R", "opcode": "0110011", "funct3": "111", "funct7": "0000000"},

            # I-Type
            "addi":  {"type": "I", "opcode": "0010011", "funct3": "000"},
            "sltiu": {"type": "I", "opcode": "0010011", "funct3": "011"},
            "lw":    {"type": "I", "opcode": "0000011", "funct3": "010"},
            "jalr":  {"type": "I", "opcode": "1100111", "funct3": "000"},

            # S-Type
            "sw": {"type": "S", "opcode": "0100011", "funct3": "010"},

            # B-Type (for reference later)
            "beq":  {"type": "B", "opcode": "1100011", "funct3": "000"},
            "bne":  {"type": "B", "opcode": "1100011", "funct3": "001"},
            "blt":  {"type": "B", "opcode": "1100011", "funct3": "100"},
            "bge":  {"type": "B", "opcode": "1100011", "funct3": "101"},
            "bltu": {"type": "B", "opcode": "1100011", "funct3": "110"},
            "bgeu": {"type": "B", "opcode": "1100011", "funct3": "111"},

            # U-Type (reference)
            "lui":   {"type": "U", "opcode": "0110111"},
            "auipc": {"type": "U", "opcode": "0010111"},

            # J-Type (reference)
            "jal": {"type": "J", "opcode": "1101111"},
        }

        return instruction_table

    def get_instruction_info(self, mnemonic):
        """
        Returns metadata dictionary for instruction.
        Raises error if invalid instruction.
        """
        mnemonic = mnemonic.strip()

        if mnemonic not in self.instructions:
            raise ValueError(f"Invalid instruction: {mnemonic}")

        return self.instructions[mnemonic]


# ----------------- Testing -----------------

if __name__ == "__main__":
    metadata = InstructionMetadata()

    print(metadata.get_instruction_info("add"))
    print(metadata.get_instruction_info("addi"))
    print(metadata.get_instruction_info("sw"))