import itertools
import sys
from collections import defaultdict
from operator import itemgetter

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
        if opcode == 1:
            # Add
            mode1 = (op//100) % 10
            mode2 = (op//1000) % 10
            mode3 = (op//10000) % 10
            op1 = self.get_value(self.ip + 1, mode1)
            op2 = self.get_value(self.ip + 2, mode2)
            self.set_value(self.ip + 3, mode3, op1 + op2)
            self.ip += 4
        elif opcode == 2:
            # Mul
            mode1 = (op//100) % 10
            mode2 = (op//1000) % 10
            mode3 = (op//10000) % 10
            op1 = self.get_value(self.ip + 1, mode1)
            op2 = self.get_value(self.ip + 2, mode2)
            self.set_value(self.ip + 3, mode3, op1 * op2)
            self.ip += 4
        elif opcode == 3:
            # Input
            mode1 = (op//100) % 10
            self.set_value(self.ip + 1, mode1, self.input.read())
            self.ip += 2
        elif opcode == 4:
            # Output
            mode = (op//100) % 10
            val = self.get_value(self.ip + 1, mode)
            self.output.write(val)
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
            mode3 = (op//10000) % 10
            op1 = self.get_value(self.ip + 1, mode1)
            op2 = self.get_value(self.ip + 2, mode2)
            self.set_value(self.ip + 3, mode3, int(op1 < op2))
            self.ip += 4
        elif opcode == 8:
            # Equal
            mode1 = (op//100) % 10
            mode2 = (op//1000) % 10
            mode3 = (op//10000) % 10
            op1 = self.get_value(self.ip + 1, mode1)
            op2 = self.get_value(self.ip + 2, mode2)
            self.set_value(self.ip + 3, mode3, int(op1 == op2))
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

BLACK = 0
WHITE = 1

LEFT = 0
RIGHT = 1

PAINT = 0
TURN = 1
# current_dir -> (dir after left turn, dir after right turn)
DIR_TRANS = {
    (0,1): ((-1,0), (1,0)),
    (1,0): ((0,1), (0,-1)),
    (0,-1): ((1,0), (-1,0)),
    (-1,0): ((0,-1), (0,1))
}
class Hull:
    def __init__(self):
        self.hull = defaultdict(lambda: BLACK)
        self.robot_pos = (0, 0)
        self.robot_dir = (0, 1) # Facing up 
        self.mode = PAINT

    def read(self):
        return self.hull[self.robot_pos]

    def write(self, val):
        if self.mode == PAINT:
            self.hull[self.robot_pos] = val
            self.mode = TURN
        elif self.mode == TURN:
            self.robot_dir = DIR_TRANS[self.robot_dir][val]
            self.robot_pos = (self.robot_pos[0] + self.robot_dir[0], self.robot_pos[1] + self.robot_dir[1])
            self.mode = PAINT
        else:
            raise ValueError("Unknown val {:d}".format(val))

    def print(self):
        x_min = min(self.hull.keys(), key=itemgetter(0))[0]
        x_max = max(self.hull.keys(), key=itemgetter(0))[0]
        y_min = min(self.hull.keys(), key=itemgetter(1))[1]
        y_max = max(self.hull.keys(), key=itemgetter(1))[1]
        for y in range(y_max + 1, y_min - 2, -1):
            print(''.join("#" if self.hull[(x, y)]==BLACK else " " for x in range(x_min, x_max + 1)))
    

def main():
    infile = "input.txt"
    if len(sys.argv) > 1:
        infile = sys.argv[1]
    program = [int(op) for op in open(infile).read().replace('\n', '').split(",")]

    hull = Hull()
    p = Program(program, input=hull, output=hull)
    while p.step():
        pass
    print(len(hull.hull))
    hull = Hull()
    hull.hull[(0,0)] = WHITE
    p = Program(program, input=hull, output=hull)
    while p.step():
        pass
    hull.print()

if __name__ == "__main__":
    main()
