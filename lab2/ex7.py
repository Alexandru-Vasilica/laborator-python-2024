def ex7(num: int) -> int:
    count = 0
    while num > 0:
        count += num & 1
        num = num >> 1
    return count


print(ex7(24))
