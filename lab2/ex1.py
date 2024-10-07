def gcd(a: int, b: int):
    if b == 0:
        return a
    return gcd(b, a % b)


def ex1() -> int | None:
    print("Enter numbers separated by space: ")
    nums = input().split()
    if len(nums) < 0:
        return
    result = int(nums[0])
    for i in range(1, len(nums)):
        result = gcd(result, int(nums[i]))
    print(result)


ex1()
