from collections import defaultdict


def ex1(a: list, b: list):
    # Write a function that receives as parameters two lists a and b and returns a list of sets containing: (a intersected with b, a reunited with b, a - b, b - a)
    set_a = set(a)
    set_b = set(b)
    return [set_a & set_b, set_a | set_b, set_a - set_b, set_b - set_a]


print(ex1([1, 2, 3, 4], [3, 4, 5, 6]))


def ex2(text: str):
    # Write a function that receives a string as a parameter and returns a dictionary in which the keys are the characters in the character string and the values are the number of occurrences of that character in the given text. Example: For string "Ana has apples." given as a parameter the function will return the dictionary:
    appearances = defaultdict(int)
    for ch in text:
        appearances[ch] += 1
    return appearances


print(ex2("Ana has apples."))


def ex3(a: dict, b: dict):
    # Compare two dictionaries without using the operator "==" returning True or False. (Attention, dictionaries must be recursively covered because they can contain other containers, such as dictionaries, lists, sets, etc.)
    if len(a) != len(b):
        return False
    for key in a:
        if key not in b:
            return False
        if type(a[key]) != type(b[key]):
            return False
        if isinstance(a[key], dict):
            if not ex3(a[key], b[key]):
                return False
        elif a[key] != b[key]:
            return False
    return True


print(ex3({1: {"a": [1, 2, 3]}, 3: 4}, {1: {"a": [1, 2, 3]}, 3: 4}))


def build_xml_element(tag: str, content: str, **kwargs):
    # The build_xml_element function receives the following parameters: tag, content, and key-value elements given as name-parameters. Build and return a string that represents the corresponding XML element
    xml = f"<{tag}"
    for key, value in kwargs.items():
        xml += f' {key}="{value}"'
    xml += f">{content}</{tag}>"
    return xml


print(build_xml_element("a", "Hello there", href=" http://python.org ", _class=" my-link ", id=" someid "))


def validate_dict(rules: set[tuple], target: dict):
    # The validate_dict function that receives as a parameter a set of tuples ( that represents validation rules for a dictionary that has strings as keys and values) and a dictionary. A rule is defined as follows: (key, "prefix", "middle", "suffix"). A value is considered valid if it starts with "prefix", "middle" is inside the value (not at the beginning or end) and ends with "suffix". The function will return True if the given dictionary matches all the rules, False otherwise.
    if len(rules) != len(target):
        return False
    for key, prefix, middle, suffix in rules:
        if key not in target:
            return False
        if not target[key].startswith(prefix):
            return False
        if not target[key].endswith(suffix):
            return False
        if not middle in target[key][1:-1]:
            return False
    return True


print(validate_dict({("key1", "", "inside", ""), ("key2", "start", "middle", "winter")},
                    {"key1": "come inside, it's too cold out", "key3": "this is not valid"}))


def ex6(list: list):
    # Write a function that receives as a parameter a list and returns a tuple (a, b), a representing the number of unique elements in the list, and b representing the number of duplicate elements in the list
    a = len(set(list))
    b = len(list) - a
    return a, b


print(ex6([1, 2, 3, 4, 1, 2, 3, 4, 5]))


def ex7(*sets):
    # Write a function that receives a variable number of sets and returns a dictionary with the following operations from all sets two by two: reunion, intersection, a-b, b-a. The key will have the following form: "a op b", where a and b are two sets, and op is the applied operator: |, &, -.
    results = {}
    for idx, set1 in enumerate(sets):
        for set2 in sets[idx + 1:]:
            results[f"{set1} | {set2}"] = set1 | set2
            results[f"{set1} & {set2}"] = set1 & set2
            results[f"{set1} - {set2}"] = set1 - set2
            results[f"{set2} - {set1}"] = set2 - set1
    return results


print(ex7({1, 2, 3}, {3, 4, 5}, {5, 6, 7}))


def ex8(mapping: dict):
    # Write a function that receives a single dict parameter named mapping. This dictionary always contains a string key "start". Starting with the value of this key you must obtain a list of objects by iterating over mapping in the following way: the value of the current key is the key for the next value, until you find a loop (a key that was visited before). The function must return the list of objects obtained as previously described
    result = []
    visited = {'start'}
    current = mapping['start']
    while current not in visited:
        visited.add(current)
        result.append(current)
        current = mapping[current]
    return result


print(ex8({'start': 'a', 'b': 'a', 'a': '6', '6': 'z', 'x': '2', 'z': '2', '2': '2', 'y': 'start'}))


def ex9(*args, **kwargs):
    # Write a function that receives a variable number of positional arguments and a variable number of keyword arguments adn will return the number of positional arguments whose values can be found among keyword arguments values.
    return len([arg for arg in args if arg in kwargs.values()])


print(ex9(1, 2, 3, 4, x=1, y=2, z=3, w=5))
