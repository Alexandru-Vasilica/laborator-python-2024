def ex3(a: str, b: str) -> int:
    count = 0
    while len(b) >= len(a):
        if b[:len(a)] == a:
            count += 1
        b = b[1:]
    return count


print(ex3("ab", "babababaaba"))
