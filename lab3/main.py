from collections import defaultdict


def ex1(n: int):
    # Write a function to return a list of the first n numbers in the Fibonacci string.
    a = 1
    b = 0
    nums = []
    for i in range(n):
        nums.append(a)
        a, b = a + b, a
    return nums


print(ex1(10))


def _is_prime(n: int):
    if n < 2:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True


def ex2(n: list[int]):
    # Write a function that receives a list of numbers and returns a list of the prime numbers found in it.
    return [x for x in n if _is_prime(x)]


print(ex2([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))


def ex3(a: list[int], b: list[int]):
    # Write a function that receives as parameters two lists a and b and returns: (a intersected with b, a reunited with b, a - b, b - a)
    set_a = set(a)
    set_b = set(b)
    return set_a & set_b, set_a | set_b, set_a - set_b, set_b - set_a


print(ex3([1, 2, 3, 4, 5], [3, 4, 5, 6, 7]))


def ex4(notes: list[str], positions: list[int], start: int):
    # Write a function that receives as a parameters a list of musical notes (strings), a list of moves (integers) and a start position (integer). The function will return the song composed by going though the musical notes beginning with the start position and following the moves given as parameter.
    song = []
    current_note = start
    song.append(notes[current_note])
    for i in positions:
        current_note = (current_note + i) % len(notes)
        song.append(notes[current_note])
    return song


print(ex4(["do", "re", "mi", "fa", "sol"], [1, -3, 4, 2], 2))


def ex5(matrix: list[list[int]]):
    # Write a function that receives as parameter a matrix and will return the matrix obtained by replacing all the elements under the main diagonal with 0 (zero).
    result = []
    for row in range(len(matrix)):
        result.append([])
        for col in range(len(matrix[row])):
            if row > col:
                result[row].append(0)
            else:
                result[row].append(matrix[row][col])
    return result


print(ex5([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))


def ex6(x: int, *lists):
    # Write a function that receives as a parameter a variable number of lists and a whole number x. Return a list containing the items that appear exactly x times in the incoming lists.
    appearances = defaultdict(int)
    for l in lists:
        for item in l:
            appearances[item] += 1
    return [item for item, count in appearances.items() if count == x]


print(ex6(2, [1, 2, 3], [2, 3, 4], [4, 5, 6], [4, 1, "test"]))


def _is_palindrome(n: int):
    return str(n) == str(n)[::-1]


def ex7(nums: list[int]):
    # Write a function that receives as parameter a list of numbers (integers) and will return a tuple with 2 elements. The first element of the tuple will be the number of palindrome numbers found in the list and the second element will be the greatest palindrome number.
    palindromes = [x for x in nums if _is_palindrome(x)]
    return len(palindromes), max(palindromes)


print(ex7([121, 123, 1331, 12321, 12345]))


def ex8(x: int = 1, strs: list[str] = [], flag: bool = True):
    # Write a function that receives as parameters 3 whole numbers. Return a list containing the numbers received as parameters sorted in ascending order.
    results = []
    for str in strs:
        if flag:
            results.append([ch for ch in str if ord(ch) % x == 0])
        else:
            results.append([ch for ch in str if ord(ch) % x != 0])
    return results


print(ex8(2, ["test", "hello", "lab002"], False))


def ex9(seats: list[list[int]]):
    # Write a function that receives as paramer a matrix which represents the heights of the spectators in a stadium and will return a list of tuples (line, column) each one representing a seat of a spectator which can't see the game. A spectator can't see the game if there is at least one taller spectator standing in front of him. All the seats are occupied. All the seats are at the same level. Row and column indexing starts from 0, beginning with the closest row from the field.
    results = []
    for j, col in enumerate(zip(*seats)):
        in_front = 0
        for i, h in enumerate(col):
            if h <= in_front:
                results.append((i, j))
            else:
                in_front = h
    return results


print(ex9([[1, 2, 3, 2, 1, 1],
           [2, 4, 4, 3, 7, 2],
           [5, 5, 2, 5, 6, 4],
           [6, 6, 7, 6, 7, 5]]))


def ex10(*lists):
   #Write a function that receives a variable number of lists and returns a list of tuples as follows: the first tuple contains the first items in the lists, the second element contains the items on the position 2 in the lists, etc.
    return list(zip(*lists))

print(ex10([1,2,3], [5,6,7], ["a", "b", "c"]))


def ex11(tuples: list[tuple[str, str]]):
    # Write a function that will order a list of string tuples based on the 3rd character of the 2nd element in the tuple.
    return sorted(tuples, key=lambda x: x[1][2])

print(ex11([('abc', 'bcd'), ('abc', 'zza')]))


def ex12(words:list[str]):
    #Write a function that will receive a list of words as parameter and will return a list of lists of words, grouped by rhyme. Two words rhyme if both of them end with the same 2 letters.
    rhymes = defaultdict(list)
    for word in words:
        rhymes[word[-2:]].append(word)
    return list(rhymes.values())

print(ex12(['ana', 'banana', 'carte', 'arme', 'parte']))

