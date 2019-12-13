import sys
import re
import math

def add(vec1, vec2):
    return [v1 + v2 for v1, v2 in zip(vec1, vec2)]


def sub(vec1, vec2):
    return [v1 - v2 for v1, v2 in zip(vec1, vec2)]


def compare(vec1, vec2):
    res = []
    for v1, v2 in zip(vec1, vec2):
        if v1 < v2:
            res.append(1)
        elif v1 > v2:
            res.append(-1)
        else:
            res.append(0)
    return res


def energy(positions, velocities):
    total_energy = 0
    for pos, vel in zip(positions, velocities):
        total_energy += sum(abs(p) for p in pos) * sum(abs(v) for v in vel)
    return total_energy


def update_velocities(positions, velocities):
    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            p1 = positions[i]
            p2 = positions[j]
            diff = compare(p1, p2)
            velocities[i] = add(velocities[i], diff)
            velocities[j] = sub(velocities[j], diff)


def update_positions(positions, velocities):
    for i in range(len(positions)):
        positions[i] = add(positions[i], velocities[i])

def lcm(a, b):
    return (a * b) // math.gcd(a, b)

def main():
    infn = "input.txt"
    if len(sys.argv) > 1:
        infn = sys.argv[1]

    positions = []
    velocities = []
    for line in open(infn):
        numbers = [int(l) for l in re.findall("-?\d+", line)]
        positions.append(numbers[:3])
        velocities.append([0, 0, 0])

    step = 0
    repeats = [None, None, None]
    world = [set(), set(), set()]
    for i in (0,1,2):
        t = (tuple(p[i] for p in positions), tuple(v[i] for v in velocities))
        world[i].add(t)

    while True:
        update_velocities(positions, velocities)
        update_positions(positions, velocities)
        step += 1
        for i in (0,1,2):
            if repeats[i] is None:
                t = (tuple(p[i] for p in positions), tuple(v[i] for v in velocities))
                if t in world[i]:
                    print("repeat {:d}: {:d} ".format(i, step))
                    repeats[i] = step
                world[i].add(t)
        if not repeats[0] is None and not repeats[1] is None and not repeats[2] is None:
            break
        if step == 1000:
            print("Energy after 1000 steps: ", energy(positions, velocities))

    print(lcm(lcm(repeats[0], repeats[1]), repeats[2]))

if __name__ == "__main__":
    main()
