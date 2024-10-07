
def ex8(text: str) -> int:
    count = 0
    trimmed_text = text.lstrip().rstrip()
    for i in range(len(trimmed_text)):
        if trimmed_text[i] == ' ':
            count += 1
    return count + 1


print(ex8(" hello world "))
