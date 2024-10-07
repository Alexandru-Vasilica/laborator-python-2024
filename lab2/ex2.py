vowels = ['a', 'e', 'i', 'o', 'u']


def ex2(string: str) -> int:
    count = 0
    for ch in string:
        if ch in vowels:
            count += 1
    return count


print(ex2("hello"))
