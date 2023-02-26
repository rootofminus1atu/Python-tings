
length = 6

lst = [1]

for i in range(length):
    print(" ".join(map(str, lst)))
    temp = list(lst)
    for j in range(i):
        lst[j+1] = temp[j] + temp[j+1]
    lst.append(1)
