import itertools
import sys



def debug(*args):
    if DEBUG:
        print(*args)

DEBUG = False

class Program:
    def __init__(self, opcodes, input, output):
        self.opcodes = opcodes[:] + [0] * 1000000
        self.input = input
        self.output = output
        self.ip = 0
        self.relative_base = 0
        self.stopped = False

    def get_value(self, ip, mode):
        if mode == 0:
            return self.opcodes[self.opcodes[ip]]
        elif mode == 1:
            return self.opcodes[ip]
        elif mode == 2:
            return self.opcodes[self.relative_base + self.opcodes[ip]]
        else:
            raise ValueError("Unknown mode {}".format(mode))

    def step(self):
        if self.stopped:
            return False
        opcodes = self.opcodes
        op = opcodes[self.ip]
        opcode = op % 100
        debug("Op: ", op)
        if opcode == 1:
            # Add
            assert opcodes[self.ip]//10000 == 0
            mode1 = (op//100) % 10
            mode2 = (op//1000) % 10
            mode3 = (op//10000) % 10
            assert mode3 == 0
            op1 = self.get_value(self.ip + 1, mode1)
            op2 = self.get_value(self.ip + 2, mode2)
            opcodes[opcodes[self.ip + 3]] = op1 + op2
            self.ip += 4
        elif opcode == 2:
            # Mul
            assert opcodes[self.ip]//10000 == 0
            mode1 = (op//100) % 10
            mode2 = (op//1000) % 10
            mode3 = (op//10000) % 10
            assert mode3 == 0
            op1 = self.get_value(self.ip + 1, mode1)
            op2 = self.get_value(self.ip + 2, mode2)
            opcodes[opcodes[self.ip + 3]] = op1 * op2
            self.ip += 4
        elif opcode == 3:
            # Input
            opcodes[opcodes[self.ip+1]] = self.input.pop(0)
            self.ip += 2
        elif opcode == 4:
            # Output
            mode = (op//100) % 10
            val = self.get_value(self.ip + 1, mode)
            self.output.append(val)
            self.ip += 2
        elif opcode == 5:
            # Not equal 0
            mode1 = (op//100) % 10
            mode2 = (op//1000) % 10
            op1 = self.get_value(self.ip + 1, mode1)
            op2 = self.get_value(self.ip + 2, mode2)
            if op1 != 0:
                self.ip = op2
            else:
                self.ip += 3
        elif opcode == 6:
            # Equal 0
            mode1 = (op//100) % 10
            mode2 = (op//1000) % 10
            op1 = self.get_value(self.ip + 1, mode1)
            op2 = self.get_value(self.ip + 2, mode2)
            if op1 == 0:
                self.ip = op2
            else:
                self.ip += 3
        elif opcode == 7:
            # Less than
            mode1 = (op//100) % 10
            mode2 = (op//1000) % 10
            op1 = self.get_value(self.ip + 1, mode1)
            op2 = self.get_value(self.ip + 2, mode2)
            op3 = opcodes[self.ip + 3]
            opcodes[op3] = int(op1 < op2)
            self.ip += 4
        elif opcode == 8:
            # Equal
            mode1 = (op//100) % 10
            mode2 = (op//1000) % 10
            op1 = self.get_value(self.ip + 1, mode1)
            op2 = self.get_value(self.ip + 2, mode2)
            op3 = opcodes[self.ip + 3]
            debug("Setting ", op1==op2, "at", op3)
            opcodes[op3] = int(op1 == op2)
            self.ip += 4
        elif opcode == 9:
            mode1 = (op//100) % 10
            op1 = self.get_value(self.ip + 1, mode1)
            self.relative_base += op1
            self.ip += 2
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

    output = []
    p = Program(program, input=[1], output=output)
    while p.step():
        pass
    print(output)

if __name__ == "__main__":
    main()
