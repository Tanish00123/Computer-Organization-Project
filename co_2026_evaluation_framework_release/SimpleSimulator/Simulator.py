import sys
from instruction_decoder import InstructionDecoder
from memory import Memory, init_registers, InvalidMemAccess
from encoder import Executor

MAX_STEPS = 100000          #globally defining max no of steps;

def fmt_bin32(val):
    return "0b" + format(val & 0xFFFFFFFF, "032b")

def make_trace_line(pc, regs):
    parts = [fmt_bin32(pc)] + [fmt_bin32(r) for r in regs]
    return " ".join(parts) + " "

def simulate(prog):
    decoder = InstructionDecoder()
    decoder.program_memory = prog
    decoded_all = decoder.decode_all()

    mem = Memory()
    regs= init_registers()
    exe = Executor(regs, mem)

    trace_lines = []
    pc = 0
    halted = False
    steps = 0

    while steps < MAX_STEPS:
        idx =pc // 4
        if pc < 0 or idx >= len(decoded_all):
            break
        dec = decoded_all[idx]

        if exe.is_halt(dec):
            trace_lines.append(make_trace_line(pc, regs))
            halted = True
            break

        try:
            npc = exe.execute(dec, pc)
        except InvalidMemAccess as err:
            line_no = (pc // 4) + 1
            print("Error at line {}: Invalid memory access ({})".format(line_no, err))
            return trace_lines, mem, False

        trace_lines.append(make_trace_line(npc, regs))
        pc = npc
        steps += 1

    return trace_lines, mem, halted


def make_mem_dump(mem):
    lines = []
    for addr_str, val_str in mem.dump_data():
        lines.append("{}:0b{}".format(addr_str, val_str))
    return lines

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 Simulator.py <input.txt> <output.txt> [readable.txt]")
        sys.exit(1)

    in_file = sys.argv[1]
    out_file = sys.argv[2]
    read_file = sys.argv[3] if len(sys.argv) > 3 else None

    prog = []
    with open(in_file, "r") as fh:
        for line in fh:
            line = line.strip()
            if line:
                prog.append(line)

    if not prog:
        print("Error: empty input file")
        sys.exit(1)

    trace_lines, mem, halted = simulate(prog)

    all_lines = trace_lines[:]
    if halted:
        all_lines += make_mem_dump(mem)

    content = "\n".join(all_lines)
    if all_lines:
        content += "\n"

    with open(out_file, "w") as fh:
        fh.write(content)

    if read_file:
        with open(read_file, "w") as fh:
            fh.write(content)

if __name__ == "__main__":
    main()