import itertools
import sys
from collections import defaultdict
from operator import itemgetter


def debug(*args):
    if DEBUG:
        print(*args)

DEBUG = False
VISUAL = False

if VISUAL:
    import colorama
    import time


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

    def set_value(self, ip, mode, value):
        assert mode != 1
        if mode == 0:
            self.opcodes[self.opcodes[ip]] = value
        elif mode == 2:
            self.opcodes[self.relative_base + self.opcodes[ip]] = value
        else:
            raise ValueError("Unknown mode {}".format(mode))

    def step(self):
        if self.stopped:
            return False
        opcodes = self.opcodes
        op = opcodes[self.ip]
        opcode = op % 100
        debug("Op: ", op)
        mode1 = (op//100) % 10
        mode2 = (op//1000) % 10
        mode3 = (op//10000) % 10
        if opcode == 1:
            # Add
            op1 = self.get_value(self.ip + 1, mode1)
            op2 = self.get_value(self.ip + 2, mode2)
            self.set_value(self.ip + 3, mode3, op1 + op2)
            self.ip += 4
        elif opcode == 2:
            # Mul
            op1 = self.get_value(self.ip + 1, mode1)
            op2 = self.get_value(self.ip + 2, mode2)
            self.set_value(self.ip + 3, mode3, op1 * op2)
            self.ip += 4
        elif opcode == 3:
            # Input
            self.set_value(self.ip + 1, mode1, self.input.read())
            self.ip += 2
        elif opcode == 4:
            # Output
            val = self.get_value(self.ip + 1, mode1)
            self.output.write(val)
            self.ip += 2
        elif opcode == 5:
            # Not equal 0
            op1 = self.get_value(self.ip + 1, mode1)
            op2 = self.get_value(self.ip + 2, mode2)
            if op1 != 0:
                self.ip = op2
            else:
                self.ip += 3
        elif opcode == 6:
            # Equal 0
            op1 = self.get_value(self.ip + 1, mode1)
            op2 = self.get_value(self.ip + 2, mode2)
            if op1 == 0:
                self.ip = op2
            else:
                self.ip += 3
        elif opcode == 7:
            # Less than
            op1 = self.get_value(self.ip + 1, mode1)
            op2 = self.get_value(self.ip + 2, mode2)
            self.set_value(self.ip + 3, mode3, int(op1 < op2))
            self.ip += 4
        elif opcode == 8:
            # Equal
            op1 = self.get_value(self.ip + 1, mode1)
            op2 = self.get_value(self.ip + 2, mode2)
            self.set_value(self.ip + 3, mode3, int(op1 == op2))
            self.ip += 4
        elif opcode == 9:
            op1 = self.get_value(self.ip + 1, mode1)
            self.relative_base += op1
            self.ip += 2
        elif opcode == 99:
            self.stopped = True
            return False
        else:
            raise RuntimeError("Unknown opcode %d at %d" % (opcode, self.ip))
        return True

class Field:
    def __init__(self):
        self.out = []
        self.input_request = False
        self.field = None
        self.ballx = -1
        self.paddlex = -1
        self.points = 0

    def read(self):
        self.input_request = True
        if self.field is not None:
            self.update_field()
        if self.ballx < self.paddlex:
            return -1
        elif self.ballx > self.paddlex:
            return 1
        return 0
        # inp = readchar.readchar()
        # return {b"a": -1, b"l": 1, b" ": 0}[inp]

    def write(self, val):
        self.out.append(val)

    def __str__(self):
        return '\n'.join(''.join(line) for line in self.field)

    def update_field(self):
        for chunk in chunker(self.out, 3):
            if chunk[0] == -1 and chunk[1] == 0:
                self.points = chunk[2]
                continue
            elif chunk[2] == BALL:
                self.ballx = chunk[0]
            elif chunk[2] == PADDLE:
                self.paddlex = chunk[0]
            symbol = SYMBOLS[chunk[2]]
            self.field[chunk[1]][chunk[0]] = symbol
        self.out.clear()


def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4


def main():
    infile = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    program = [int(op) for op in open(infile).read().replace('\n', '').split(",")]

    field = Field()
    p = Program(program, input=field, output=field)
    while p.step():
        if field.input_request:
            break

if __name__ == "__main__":
    main()
