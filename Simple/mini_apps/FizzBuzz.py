while True:
    try:
        variableCount = int(input(
            "How many variables would you like to input? "))
        if 0 < variableCount < 6:
            break
        else:
            print("Please input an integer between 1 and 5 for variables. \n")
    except ValueError:
        print("Please input an integer between 1 and 5 for variables. \n")

variables = {}
for i in range(variableCount):
    while True:
        tempVarName = input(
            "Give me a variable name for variable {}: ".format(i+1))
        try:
            tempVarMultiple = int(input(
                "What multiple should {} appear on? (1-10) "
                .format(tempVarName)))
            if 0 < tempVarMultiple < 11:
                variables[tempVarName] = tempVarMultiple
                break
            else:
                print("Try again, this time with multiplier as integer between"
                      "1 and 10 \n")
        except ValueError:
            print("Try again, this time with multiplier as integer between"
                  "1 and 10 \n")

while True:
    try:
        countTo = int(input("What should I count up to? (1-1000 please) "))
        if 0 < countTo < 1001:
            break
        else:
            print("Please input an integer between 1 and 1000. \n")
    except ValueError:
        print("Please input an integer between 1 and 1000. \n")

while True:
    try:
        multiplier = int(input("Count in multiples of what? "))
        if 0 < multiplier < 11:
            break
        else:
            print("Please input an integer between 1 and 10. \n")
    except ValueError:
        print("Please input an integer between 1 and 10. \n")

print(variableCount, countTo, variables)

equalsNumber = False
for i in range(multiplier, countTo + 1, multiplier):
    for variable in variables:
        if i % variables[variable] == 0:
            print(variable, end=" ")
            equalsNumber = True
    if equalsNumber is False:
        print(i)
    else:
        print()
    equalsNumber = False
