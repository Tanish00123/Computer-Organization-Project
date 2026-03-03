# Register mapping

class RegisterEncoder:
    def __init__(self):
        self.register_map = self.register_map()

    def register_map(self):
        register_map = {}

        # x0 to x31
        for i in range(32):
            register_map[f"x{i}"] = format(i, "05b")

    #From Table 17 of assignment
        abi_names = {
            "zero": 0,
            "ra": 1,
            "sp": 2,
            "gp": 3,
            "tp": 4,
            "t0": 5,
            "t1": 6,"t2": 7,
            "s0": 8,"fp": 8,
            "s1": 9,
            "a0": 10,"a1": 11,
            "a2": 12,"a3": 13,"a4": 14,"a5": 15,"a6": 16,"a7": 17,
            "s2": 18,"s3": 19,"s4": 20,"s5": 21,"s6": 22,"s7": 23,"s8": 24,"s9": 25,"s10": 26,"s11": 27,
            "t3": 28,"t4": 29,"t5": 30,"t6": 31,
        }

        # Adding ABI names to the dictionary
        for name, number in abi_names.items():
            register_map[name] = format(number, "05b")

        return register_map

    def get_binary(self, register_name):        
        register_name = register_name.strip()

        if register_name not in self.register_map:
            raise KeyError(f"Invalid register: {register_name}")

        return self.register_map[register_name]


# Testing
if __name__ == "__main__":
    encoder = RegisterEncoder()

    print(encoder.get_binary("zero")) # 00000
    print(encoder.get_binary("ra")) # 00001
    print(encoder.get_binary("s1")) # 01001
    print(encoder.get_binary("x15")) # 01111