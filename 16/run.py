from itertools import islice, repeat, chain, starmap, cycle
import time

def fft(input, pattern):
    res = [None] * len(input)
    for i in range(len(input)):
        filter = chain.from_iterable(starmap(repeat, zip(cycle(pattern), repeat(i + 1))))
        next(filter)
        res[i] = abs(sum(a * b for a, b in zip(input, filter))) % 10
    return res

def fft2(input, pattern):
    return [abs(sum(input[i] * pattern[((i+1)//(index+1))%4] for i in range(index, len(input)))) % 10 for index in range(len(input))]

def main():
    start = time.time()
    input_list = list(int(el) for el in open("input.txt").readline().rstrip('\n'))
    
    target_part2 = int(''.join(str(el) for el in input_list[:7]))
    input_part2 = (input_list*10000)[target_part2:]

    test = 80871224585914546619083218645595
    test_result = 24176176
    pattern = [0, 1, 0, -1]
    test_list = [int(l) for l in str(test)]
    test_result_list = [int(l) for l in str(test_result)]
    for _ in range(100):
        # test_list = fft2(test_list, pattern)
        input_list = fft2(input_list, pattern)
    # assert test_list[:8] == test_result_list
    print(input_list[:8])

    N = len(input_part2)
    for _ in range(100):
        for i in range(N-2, -1, -1):
            input_part2[i] = (input_part2[i + 1] + input_part2[i]) % 10
    print(input_part2[:8])

    print(time.time() - start)

if __name__ == "__main__":
    main()
