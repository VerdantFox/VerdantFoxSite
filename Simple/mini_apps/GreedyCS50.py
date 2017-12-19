def greedy(cost, paid):
    # Round money (for computer error with long strings of decimal).
    change = int(paid * 100) - int(cost * 100)
    round(change)

    hundred = change // 10000
    change %= 10000
    fifty = change // 5000
    change %= 5000
    twenty = change // 2000
    change %= 2000
    ten = change // 1000
    change %= 1000
    five = change // 500
    change %= 500
    one = change // 100
    change %= 100
    quarters = change // 25
    change %= 25
    dimes = change // 10
    change %= 10
    nickels = change // 5
    change %= 5
    pennies = change // 1

    print(str(int(quarters + dimes + nickels + pennies)))
    # Add all stored coin amounts together and print as an integer
    statement = str(str(int(hundred + fifty + twenty + ten + five + one))
                    + " bills and " + str(int(quarters + dimes + nickels + pennies))
                    + " coins needed")
    change_list = ["bills and coins to give: "]

    if hundred != 0:
        change_list.append("{} hundred dollar bill".format(int(hundred)))
    if fifty != 0:
        change_list.append("{} fifty dollar bill".format(int(fifty)))
    if twenty != 0:
        change_list.append("{} twenty dollar bill".format(int(twenty)))
    if ten != 0:
        change_list.append("{} ten dollar bill".format(int(ten)))
    if five != 0:
        change_list.append("{} five dollar bill".format(int(five)))
    if one != 0:
        change_list.append("{} one dollar bill".format(int(one)))
    if quarters != 0:
        change_list.append("{} quarter".format(int(quarters)))
    if dimes != 0:
        change_list.append("{} dime".format(int(dimes)))
    if nickels != 0:
        change_list.append("{} nickel".format(int(nickels)))
    if pennies != 0:
        change_list.append("{} penny".format(int(pennies)))

    return statement, change_list


if __name__ == "__main__":
    Cost = float(input("item cost? "))
    Paid = float(input("Amount paid? "))
    print(greedy(Cost, Paid))
