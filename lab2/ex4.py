def ex4(string: str) -> str:
    result = ''
    for idx, ch in enumerate(string):
        if str(ch).isupper():
            if idx != 0:
                result += '_'
            result += str(ch).lower()
        else:
            result += ch
    return result


print(ex4("HelloWorld"))
