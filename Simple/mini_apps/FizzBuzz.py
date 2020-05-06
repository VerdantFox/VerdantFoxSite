def fizz_buzz(count_to, multiplier, variables):
    list_count = []
    equals_number = False
    for i in range(multiplier, count_to + 1, multiplier):
        row = []
        for variable in variables:
            if i % variables[variable] == 0:
                row.append(variable)
                equals_number = True
        if equals_number is False:
            row.append(i)
        else:
            pass
        equals_number = False
        list_count.append(row)
    return list_count


def create_variables(
    var_1_name, var_1_mult, var_2_name, var_2_mult, var_3_name, var_3_mult
):

    var_dict = {var_1_name: var_1_mult}
    if var_2_name:
        var_dict[var_2_name] = var_2_mult
    if var_3_name:
        var_dict[var_3_name] = var_3_mult

    return var_dict


if __name__ == "__main__":
    while True:
        try:
            variableCount = int(input("How many Variables would you like to input? "))
            if 0 < variableCount < 6:
                break
            else:
                print("Please input an integer between 1 and 5 for Variables. \n")
        except ValueError:
            print("Please input an integer between 1 and 5 for Variables. \n")

    Variables = {}
    for i in range(variableCount):
        while True:
            tempVarName = input(
                "Give me a variable name for variable {}: ".format(i + 1)
            )
            try:
                tempVarMultiple = int(
                    input(
                        "What multiple should {} appear on? (1-10) ".format(tempVarName)
                    )
                )
                if 0 < tempVarMultiple < 11:
                    Variables[tempVarName] = tempVarMultiple
                    break
                else:
                    print(
                        "Try again, this time with multiplier as integer "
                        "between 1 and 10 \n"
                    )
            except ValueError:
                print(
                    "Try again, this time with multiplier as integer between"
                    "1 and 10 \n"
                )

    while True:
        try:
            CountTo = int(input("What should I count up to? (1-1000 please) "))
            if 0 < CountTo < 1001:
                break
            else:
                print("Please input an integer between 1 and 1000. \n")
        except ValueError:
            print("Please input an integer between 1 and 1000. \n")

    while True:
        try:
            Multiplier = int(input("Count in multiples of what? "))
            if 0 < Multiplier < 11:
                break
            else:
                print("Please input an integer between 1 and 10. \n")
        except ValueError:
            print("Please input an integer between 1 and 10. \n")

    print(variableCount, CountTo, Variables)

    fizzbuzz(CountTo, Multiplier, Variables)
