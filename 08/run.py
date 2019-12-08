import numpy as np
import sys

def main():
    inp = [int(el) for el in open("input.txt").readline()]
    nx = 25
    ny = 6
    nlayer = 100
    array = np.reshape(inp, (nlayer, ny, nx))
    zeros_per_layer = np.sum(np.sum(array==0, axis=1), axis=1)
    minlayer = array[np.argmin(zeros_per_layer), :, :]
    print(np.sum(minlayer==1) * np.sum(minlayer==2))
    for y in range(ny):
        for x in range(nx):
            for l in range(nlayer):
                p = array[l, y, x]
                if p == 0:
                    sys.stdout.write(" ")
                    break
                if p == 1:
                    sys.stdout.write("#")
                    break
        sys.stdout.write('\n')
            

if __name__ == "__main__":
    main()