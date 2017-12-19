def change_function(cost, paid):
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

    # Add all stored coin amounts together and print as an integer
    bills_statement = str(str(int(hundred + fifty + twenty + ten + five + one)))
    coins_statement = str(int(quarters + dimes + nickels + pennies))
    change_list = []

    if hundred != 0:
        change_list.append((int(hundred), "hundred dollar bill"))
    if fifty != 0:
        change_list.append((int(fifty), "fifty dollar bill"))
    if twenty != 0:
        change_list.append((int(twenty), "twenty dollar bill"))
    if ten != 0:
        change_list.append((int(ten), "ten dollar bill"))
    if five != 0:
        change_list.append((int(five), "five dollar bill"))
    if one != 0:
        change_list.append((int(one), "one dollar bill"))
    if quarters != 0:
        change_list.append((int(quarters), "quarter"))
    if dimes != 0:
        change_list.append((int(dimes), "dime"))
    if nickels != 0:
        change_list.append((int(nickels), "nickel"))
    if pennies != 0:
        change_list.append((int(pennies), "penn"))

    return bills_statement, coins_statement, change_list


if __name__ == "__main__":
    Cost = float(input("item cost? "))
    Paid = float(input("Amount paid? "))
    print(change_function(Cost, Paid))
