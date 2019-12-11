import sys
import math
from collections import defaultdict
from operator import itemgetter

def count_visible(space, pos):
    posx, posy = pos
    angles = defaultdict(list)
    for y in range(len(space)):
        for x in range(len(space[0])):
            if space[y][x] == ".":
                continue
            if posx == x and posy == y:
                continue
            # Angle to neg y-axis in [0, 2 * pi]
            angles[math.fmod(math.atan2(posx - x, posy - y) + math.tau, math.tau)].append((x,y))
    return len(angles), angles

def distsq(pos1, pos2):
    return (pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2

def main():
    infn = "input.txt"
    if len(sys.argv) > 1:
        infn = sys.argv[1]
    
    space = [list(line.rstrip('\n')) for line in open(infn)]
    
    max_asteroids = 0
    bestpos = (0,0)
    for y in range(len(space)):
        for x in range(len(space[0])):
            if space[y][x] == ".":
                continue
            count, _ = count_visible(space, (x, y))
            if count > max_asteroids:
                max_asteroids = count
                bestpos = (x,y)
    print(max_asteroids, bestpos)

    _, angles = count_visible(space, bestpos)
    angles = list(sorted(angles.items(), key=itemgetter(0)))
    for _, asteroids in angles:
        asteroids.sort(key= lambda a: distsq(bestpos, a))
    vaporized = 0
    i = 0
    while vaporized < 200:
        if angles[i]:
            vaporized += 1
            print(vaporized, angles[i][1][0])
            angles[i][1].pop(0)
        i = (i - 1) % len(angles)

if __name__ == "__main__":
    main()