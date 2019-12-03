def path(wire):
    DIR = dict(zip("RLUD", ((1,0), (-1,0), (0,1), (0,-1))))
    pos = (0,0)
    path = {}
    steps = 0
    for el in wire:
        dir = DIR[el[0]]
        length = int(el[1:])
        for _ in range(length):
            pos = (pos[0] + dir[0], pos[1] + dir[1])
            steps += 1
            if not pos in path:
                path[pos] = steps
    return path

def manhattan_dist(point):
    return abs(point[0]) + abs(point[1])

def main():
    w1, w2 = [line.rstrip('\n').split(",") for line in open("input.txt")]
    # lines = ["R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83"]
    # w1, w2 = [line.rstrip('\n').split(",") for line in lines]
    p1 = path(w1)
    p2 = path(w2)
    print(min(manhattan_dist(p) for p in p1.keys()&p2.keys()))
    print(min(p1[p]+p2[p] for p in p1.keys()&p2.keys()))

if __name__ == "__main__":
    main()