import itertools
import sys

def get_value(opcodes, ip, mode):
    if mode == 0:
        return opcodes[opcodes[ip]]
    elif mode == 1:
        return opcodes[ip]
    else:
        raise ValueError("Unknown mode {}".format(mode))

def debug(*args):
    if DEBUG:
        print(*args)

DEBUG = False

class Program:
    def __init__(self, opcodes, input, output):
        self.opcodes = opcodes[:]
        self.input = input
        self.output = output
        self.ip = 0
        self.stopped = False

    def step(self):
        if self.stopped:
            return False
        opcodes = self.opcodes
        op = opcodes[self.ip]
        opcode = op % 100
        debug("Op: ", op)
        debug(opcodes)
        if opcode == 1:
            # Add
            assert opcodes[self.ip]//10000 == 0
            mode1 = (op//100) % 10
            mode2 = (op//1000) % 10
            mode3 = (op//10000) % 10
            assert mode3 == 0
            op1 = get_value(opcodes, self.ip + 1, mode1)
            op2 = get_value(opcodes, self.ip + 2, mode2)
            opcodes[opcodes[self.ip + 3]] = op1 + op2
            self.ip += 4
        elif opcode == 2:
            assert opcodes[self.ip]//10000 == 0
            mode1 = (op//100) % 10
            mode2 = (op//1000) % 10
            mode3 = (op//10000) % 10
            assert mode3 == 0
            op1 = get_value(opcodes, self.ip + 1, mode1)
            op2 = get_value(opcodes, self.ip + 2, mode2)
            opcodes[opcodes[self.ip + 3]] = op1 * op2
            self.ip += 4
        elif opcode == 3:
            # Input
            opcodes[opcodes[self.ip+1]] = self.input.pop(0)
            self.ip += 2
        elif opcode == 4:
            # Output
            mode = (op//100) % 10
            val = get_value(opcodes, self.ip + 1, mode)
            self.output.append(val)
            self.ip += 2
        elif opcode == 5:
            mode1 = (op//100) % 10
            mode2 = (op//1000) % 10
            op1 = get_value(opcodes, self.ip + 1, mode1)
            op2 = get_value(opcodes, self.ip + 2, mode2)
            if op1 != 0:
                self.ip = op2
            else:
                self.ip += 3
        elif opcode == 6:
            mode1 = (op//100) % 10
            mode2 = (op//1000) % 10
            op1 = get_value(opcodes, self.ip + 1, mode1)
            op2 = get_value(opcodes, self.ip + 2, mode2)
            if op1 == 0:
                self.ip = op2
            else:
                self.ip += 3
        elif opcode == 7:
            mode1 = (op//100) % 10
            mode2 = (op//1000) % 10
            op1 = get_value(opcodes, self.ip + 1, mode1)
            op2 = get_value(opcodes, self.ip + 2, mode2)
            op3 = opcodes[self.ip + 3]
            opcodes[op3] = int(op1 < op2)
            self.ip += 4
        elif opcode == 8:
            mode1 = (op//100) % 10
            mode2 = (op//1000) % 10
            op1 = get_value(opcodes, self.ip + 1, mode1)
            op2 = get_value(opcodes, self.ip + 2, mode2)
            op3 = opcodes[self.ip + 3]
            debug("Setting ", op1==op2, "at", op3)
            opcodes[op3] = int(op1 == op2)
            self.ip += 4
        elif opcode == 99:
            self.stopped = True
            return False
        else:
            raise RuntimeError("Unknown opcode %d at %d" % (opcode, self.ip))
        return True

def main():
    infile = "input.txt"
    if len(sys.argv) > 1:
        infile = sys.argv[1]
    program = [int(op) for op in open(infile).read().replace('\n', '').split(",")]

    # Part 1
    max_output = 0
    for permutation in itertools.permutations(range(5)):
        output = [0]
        for i in range(5):
            prev_result = output[0]
            output.clear()
            p = Program(program, input=[permutation[i], prev_result], output=output)
            while not output:
                p.step()
        if output[0] > max_output:
            max_output = output[0] 
    print(max_output)
    # Part 2
    max_output = 0
    for permutation in itertools.permutations((5,6,7,8,9)):
        output = [0]
        programs = [Program(program, input=[permutation[i]], output=output) for i in range(5)]
        while True:
            for i, p in enumerate(programs):
                prev_result = output[0]
                p.input.append(prev_result)
                output.clear()
                while not output and p.step():
                    pass
                if programs[0].stopped:
                    break
            if programs[0].stopped:
                break
        if programs[0].input[0] > max_output:
            max_output = programs[0].input[0]
    print(max_output)


if __name__ == "__main__":
    main()
