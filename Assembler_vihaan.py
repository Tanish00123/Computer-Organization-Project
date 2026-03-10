from encoder import InstructionEncoder
import sys


class Assembler:
    def __init__(self):
        self.encoder = InstructionEncoder()

    def build_label_map(self, lines):
        label_map = {}
        current_address = 0

        for line in lines:
            parsed = self.parse_line(line)
            if parsed is None:
                continue

            label, instruction, operands = parsed

            if label is not None:
                label_map[label] = current_address

            if instruction is not None:
                current_address += 4

        return label_map

    def resolve_operands(self, instruction, operands, current_address, label_map):
        if instruction not in self.LABEL_INSTRUCTIONS:
            return operands

        last = operands[-1]

        try:
            int(last)
            return operands
        except ValueError:
            pass

        if last not in label_map:
            raise ValueError(f"Undefined label: '{last}'")

        offset = label_map[last] - current_address
        return operands[:-1] + [str(offset)]

    def assemble_file(self, input_file, output_file, readable_file=None):

        with open(input_file, "r") as infile:
            lines = infile.readlines()

        label_map = self.build_label_map(lines)

        with open(output_file, "w") as outfile:
            readable_lines = []
            current_address = 0

            for line in lines:
                parsed = self.parse_line(line)

                if parsed is None:
                    continue

                label, instruction, operands = parsed

                if instruction is None:
                    continue

                operands = self.resolve_operands(instruction, operands, current_address, label_map)
                binary = self.assemble_instruction(instruction, operands)

                outfile.write(binary + "\n")
                readable_lines.append(f"{hex(current_address)}: {binary} ; {line.strip()}\n")
                current_address += 4

        if readable_file:
            with open(readable_file, "w") as rf:
                rf.writelines(readable_lines)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("<input.asm> <output.txt>")
        sys.exit(1)

    input_file  = sys.argv[1]
    output_file = sys.argv[2]
    readable_file = sys.argv[3] if len(sys.argv) >= 4 else None

    assembler = Assembler()

    try:
        with open(input_file, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: input file '{input_file}' not found.")
        sys.exit(1)
    errors = []
    try:
        label_map = assembler.build_label_map(lines)
    except Exception as e:
        print(f"Error (label pass): {e}")
        sys.exit(1)

    output_lines   = []
    readable_lines = []
    current_address = 0

    for line_num, line in enumerate(lines, start=1):
        parsed = assembler.parse_line(line)

        if parsed is None:
            continue

        label, instruction, operands = parsed

        if instruction is None:
            continue

        try:
            operands = assembler.resolve_operands(instruction, operands, current_address, label_map)
            binary   = assembler.assemble_instruction(instruction, operands)
        except (ValueError, KeyError, TypeError) as e:
            print(f"Error on line {line_num}: {e}")
            sys.exit(1)

        output_lines.append(binary + "\n")
        readable_lines.append(f"{hex(current_address)}: {binary} ; {line.strip()}\n")
        current_address += 4

    with open(output_file, "w") as f2:
        f2.writelines(output_lines)

    if readable_file:
        with open(readable_file, "w") as rf:
            rf.writelines(readable_lines)
