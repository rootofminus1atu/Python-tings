
def find_max(lst):
    maxi = 0
    for i in lst:
        if i > maxi:
            maxi = i
    return maxi


numbs = [1, 5, 67, 3]
print(find_max(numbs))
