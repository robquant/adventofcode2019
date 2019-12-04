import itertools

def run(opcodes):
    ip = 0
    while opcodes[ip] != 99:
        if opcodes[ip] == 1:
            op1 = opcodes[opcodes[ip+1]]
            op2 = opcodes[opcodes[ip+2]]
            opcodes[opcodes[ip+3]] = op1 + op2
        elif opcodes[ip] == 2:
            op1 = opcodes[opcodes[ip+1]]
            op2 = opcodes[opcodes[ip+2]]
            opcodes[opcodes[ip+3]] = op1 * op2
        else:
            raise RuntimeError("Unknown opcode %d at %d"%(opcodes[ip],ip))
        ip += 4
    return opcodes[0]

def init(orig, noun, verb):
    opcodes = orig[:]
    opcodes[1] = noun
    opcodes[2] = verb
    return opcodes

def main():
    opcodes_orig = [int(op) for op in open("input.txt").readline().split(",")]

    # Part 1
    program = init(opcodes_orig, 12, 2)
    print(run(program))

    # Part 2
    target = 19690720
    for noun, verb in itertools.product(range(0, 100), range(0, 100)):
        program = init(opcodes_orig, noun, verb)
        if run(program) == target:
            print(100 * noun + verb)
            break

if __name__ == "__main__":
    main()
