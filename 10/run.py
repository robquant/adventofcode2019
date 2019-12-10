import sys
import math

def count_visible(space, pos):
    posx, posy = pos
    angles = set()
    for y in range(len(space)):
        for x in range(len(space[0])):
            if space[y][x] == ".":
                continue
            if posx == x and posy == y:
                continue
            angles.add(math.atan2(posy - y, posx - x))
    return len(angles)

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
            count = count_visible(space, (x, y))
            if count > max_asteroids:
                max_asteroids = count
                bestpos = (x,y)
    print(max_asteroids, bestpos)

if __name__ == "__main__":
    main()