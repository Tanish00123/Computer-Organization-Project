
import sys
from instruction_decoder import instruction_decoder
from memory import Memory, init_registers
from encoder import Executor

def binary_32(val):
    return format(val & 0xFFFFFFFF,'032b')


def trace(pc, regs, file):
    line = binary_32(pc)
    
    for i in range(32):
        line += " "+ binary_32(regs[i])
    file.write(line +"\n")


def run_simu(input_file,output_file):

    decoder = instruction_decoder()
    
    decoder.load_program(input_file)

    memory = Memory()
    regs = init_registers()

    instructions= [int(instr,2) for instr in decoder.program_memory]
    memory.load_program(instructions)


    executor =Executor(regs, memory)

    pc = 0

    
    with open(output_file,"w") as f:

        while True:
            
            index = pc // 4
            
            decoded =decoded_program[index]

            trace(pc, regs, f)

            if executor.is_virtual_halt(decoded):
                break

          
            pc = executor.execute(decoded, pc)
    
        dump =memory.dump_data()
        for addr, val in dump:
            f.write(f"{addr}:{val}\n")



if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file= sys.argv[2]

    run_simu(input_file, output_file)