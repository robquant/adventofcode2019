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

def run(opcodes, input_val):
    ip = 0
    while opcodes[ip] != 99:
        op = opcodes[ip]
        opcode = opcodes[ip] % 100
        debug("Op: ", op)
        debug(opcodes)
        if opcode == 1:
            # Add
            assert opcodes[ip]//10000 == 0
            mode1 = (op//100) % 10
            mode2 = (op//1000) % 10
            mode3 = (op//10000) % 10
            assert mode3 == 0
            op1 = get_value(opcodes, ip + 1, mode1)
            op2 = get_value(opcodes, ip + 2, mode2)
            opcodes[opcodes[ip + 3]] = op1 + op2
            ip += 4
        elif opcode == 2:
            assert opcodes[ip]//10000 == 0
            mode1 = (op//100) % 10
            mode2 = (op//1000) % 10
            mode3 = (op//10000) % 10
            assert mode3 == 0
            op1 = get_value(opcodes, ip + 1, mode1)
            op2 = get_value(opcodes, ip + 2, mode2)
            opcodes[opcodes[ip + 3]] = op1 * op2
            ip += 4
        elif opcode == 3:
            # Input
            opcodes[opcodes[ip+1]] = input_val
            ip += 2
        elif opcode == 4:
            # Output
            mode = (op//100) % 10
            val = get_value(opcodes, ip + 1, mode)
            print('>>>', val)
            ip += 2
        elif opcode == 5:
            mode1 = (op//100) % 10
            mode2 = (op//1000) % 10
            op1 = get_value(opcodes, ip + 1, mode1)
            op2 = get_value(opcodes, ip + 2, mode2)
            if op1 != 0:
                ip = op2
            else:
                ip += 3
        elif opcode == 6:
            mode1 = (op//100) % 10
            mode2 = (op//1000) % 10
            op1 = get_value(opcodes, ip + 1, mode1)
            op2 = get_value(opcodes, ip + 2, mode2)
            if op1 == 0:
                ip = op2
            else:
                ip += 3
        elif opcode == 7:
            mode1 = (op//100) % 10
            mode2 = (op//1000) % 10
            op1 = get_value(opcodes, ip + 1, mode1)
            op2 = get_value(opcodes, ip + 2, mode2)
            op3 = opcodes[ip + 3]
            opcodes[op3] = int(op1 < op2)
            ip += 4
        elif opcode == 8:
            mode1 = (op//100) % 10
            mode2 = (op//1000) % 10
            op1 = get_value(opcodes, ip + 1, mode1)
            op2 = get_value(opcodes, ip + 2, mode2)
            op3 = opcodes[ip + 3]
            debug("Setting ", op1==op2, "at", op3)
            opcodes[op3] = int(op1 == op2)
            ip += 4
        else:
            raise RuntimeError("Unknown opcode %d at %d" % (opcode, ip))
    return opcodes[0]


def main():
    if len(sys.argv) > 1:
        program = [int(op) for op in open(sys.argv[1]).read().replace('\n', '').split(",")]
    else:
        program = [int(op) for op in open("input.txt").read().replace('\n', '').split(",")]

    print("Part 1")
    run(program[:], input_val=1)
    print("Part 2")
    run(program[:], input_val=5)


if __name__ == "__main__":
    main()
