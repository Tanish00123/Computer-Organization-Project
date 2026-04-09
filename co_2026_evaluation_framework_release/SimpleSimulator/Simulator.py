import sys
from instruction_decoder import instruction_decoder
from memory import Memory, init_registers
from encoder import Executor


def binary_32(val):
    return "0b" + format(val & 0xFFFFFFFF, '032b')


def trace(pc, regs):
    line = binary_32(pc)
    for i in range(32):
        line += " " + binary_32(regs[i])
    line += " "
    print(line)

def run_simu(lines):

    decoder = instruction_decoder()
    decoder.program_memory = lines

    memory = Memory()
    regs = init_registers()

    instructions = [int(instr, 2) for instr in decoder.program_memory]
    memory.load_program(instructions)

    executor = Executor(regs, memory)

    decoded_program = decoder.decode_program()

    pc = 0

    while True:
        index = pc // 4
        decoded = decoded_program[index]

        print(f"DEBUG: PC={pc}, type={decoded['type']}, funct3={decoded['funct3']}, imm={decoded['imm']}")

        if executor.is_virtual_halt(decoded):
            trace(pc, regs)
            break

        pc = executor.execute(decoded, pc)
        trace(pc, regs)

    dump = memory.dump_data()
    for addr, val in dump:
        print(f"{addr}:0b{val}")


if __name__ == "__main__":
    lines = sys.stdin.read().strip().split('\n')
    run_simu(lines)