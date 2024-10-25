import copy

list1 = [[1], [2], [3]]

list2 = copy.deepcopy(list1)

print(list1)
print(list2)
list2[0][0] = 10

print(list1)
print(list2)