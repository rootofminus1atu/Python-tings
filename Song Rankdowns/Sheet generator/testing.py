numberrr = 11
colooors = ['red', 'orange', 'yellow', 'green']
speciaaals = ['bronze', 'silver', 'gold']


def get_color_ranges(length, colors):
    colors_copy = colors.copy()
    colors_copy.reverse()
    color_list = []
    for i in range(length):
        color_list.append(colors_copy[i % len(colors_copy)])

    final_list = []
    jumpy_index = 0
    tracker = 0
    for i in range(length):
        if jumpy_index >= length:
            tracker += 1
            jumpy_index = tracker 

        final_list.append(color_list[jumpy_index])

        jumpy_index += len(colors_copy)

    final_list.reverse()
    return final_list

"""
sonnum = 18
print(get_color_ranges(sonnum - 3, colooors) + speciaaals)
"""



