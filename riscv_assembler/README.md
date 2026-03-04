#riscv_assembler references of code

--------------register_map.py-----------------
1. The logic of converting number to binary in register_map.py file was taken from Chatgpt
  The exact line that was taken:- register_map[f"x{i}"] = format(i, "05b")

2. The use of KeyError Execption:- raise KeyError(f"Invalid register: {register_name}")

------------------encoder.py------------------
1. The alternate logic to represent negative number in their 2's complement form:-
  value = (1 << bit_width) + value