def get_digits(n):
    d = []
    while n != 0:
        d.append(n%10)
        n = n // 10
    return d[::-1]

def get_diff(digits):
    return [a - b for a, b in zip(digits[1:], digits[:-1])]

def main():
    input = "145852-616942"
    start, end = (int(el) for el in input.split("-"))
    count1 = 0
    count2 = 0
    for n in range(start, end + 1):
        digits = get_digits(n)
        diff = get_diff(digits)
        if all(x>=0 for x in diff) and any(x == 0 for x in diff):
            count1 += 1
            padded = [99] + diff + [99]
            for i in [1,2,3,4,5]:
                digit = padded[i]
                if digit != 0:
                    continue
                if padded[i-1] > 0 and padded[i+1] > 0:
                    count2 += 1
                    break 
    print(count1, count2)


if __name__ == "__main__":
    main()