def even_bool(num):
    return num % 2 == 0


my_list = [1, 2, 3]
result = list(filter(even_bool, my_list))
print(result)


my_list1 = [1, 2, 3]
result1 = list(filter(lambda num: num % 2 != 0, my_list1))
print(result1)


if 1 in my_list:
    print(True)
else:
    print(False)