def ex6(text: str) -> int | None:
    num = None
    for ch in text:
        if ch.isdigit():
            if num is None:
                num = 0
            num = num * 10 + int(ch)
        elif num is not None:
            return num
    return num


print(ex6("hello123asda"))
