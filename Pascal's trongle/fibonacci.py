
while True:
    lst = [1, 1]

    try:
        length = int(input("how long do you want your fibonacci sequence to be?"))

        if length < 2:
            print("Input a positive integer next time")

        elif length > 999:
            print("Maybe try a smaller number")

        # this is the actual fibonacci code part
        else:
            for i in range(2, length):
                lst.append(lst[i - 2] + lst[i - 1])

            print(lst)

    except ValueError:
        print("That's not a positive integer...")
