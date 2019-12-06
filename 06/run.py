import sys

def path_to(orbits, object, central):
    path = [object]
    while object != central:
        object = orbits[object]
        path.append(object)
    return path

def pathlength_to(orbits, object, central):
    count = 0
    while object != central:
        count += 1
        object = orbits[object]
    return count

def main():
    infile = "input.txt"
    if len(sys.argv) > 1:
        infile = sys.argv[1]
    input = [line.rstrip('\n').split(')') for line in open(infile)]
    orbits = {satellite:central for central, satellite in input}
    total = sum(pathlength_to(orbits, satellite, "COM") for satellite in orbits.keys())
    print(total)
    you_to_com = path_to(orbits, "YOU", "COM")
    san_to_com = path_to(orbits, "SAN", "COM")
    com_to_you = list(reversed(you_to_com))
    com_to_san = list(reversed(san_to_com))
    i = 0
    while com_to_san[i] == com_to_you[i]:
        i += 1
    i -= 1
    transfers = len(com_to_you) - i - 1 + len(com_to_san) - i - 1 - 2
    print(transfers)
         

if __name__ == "__main__":
    main()