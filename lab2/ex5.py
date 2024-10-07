def ex5(num: int) -> bool:
    num_str = str(num)
    while len(num_str) > 0:
        if num_str[0] != num_str[-1]:
            return False
        num_str = num_str[1:-1]
    return True


print(ex5(23132))
