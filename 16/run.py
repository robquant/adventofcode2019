from itertools import islice, repeat, chain, starmap, cycle

def fft(input, pattern):
    res = [None] * len(input)
    for i in range(len(input)):
        filter = chain.from_iterable(starmap(repeat, zip(cycle(pattern), repeat(i + 1))))
        next(filter)
        res[i] = abs(sum(a * b for a, b in zip(input, filter))) % 10
    return res

def main():
    input_list = list(int(el) for el in open("input.txt").readline().rstrip('\n'))
    test = 80871224585914546619083218645595
    test_result = 24176176
    pattern = [0, 1, 0, -1]
    test_list = [int(l) for l in str(test)]
    test_result_list = [int(l) for l in str(test_result)]
    for _ in range(100):
        test_list = fft(test_list, pattern)
        input_list = fft(input_list, pattern)
    assert test_list[:8] == test_result_list
    print(input_list[:8])

if __name__ == "__main__":
    main()
