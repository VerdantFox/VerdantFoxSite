def greedy(money):
    # Round money (for computer error with long strings of decimal).
    round(money)
    money *= 100

    hundred = money // 10000
    money %= 10000
    fifty = money // 5000
    money %= 5000
    twenty = money // 2000
    money %= 2000
    ten = money // 2000
    money %= 1000
    five = money // 500
    money %= 500
    one = money // 100
    money %= 100
    quarters = money // 25
    money %= 25
    dimes = money // 10
    money %= 10
    nickels = money // 5
    money %= 5
    pennies = money // 1

    # Add all stored coin amounts together and print as an integer
    print('\n' + str(int(hundred + fifty + twenty + five + one)) + " bills and " +
          str(int(quarters + dimes + nickels + pennies)) + " coins needed",
          end='\n\n')

    print("bills and coins to give: ")
    if hundred != 0:
        print("{} hundred dollar bills".format(int(hundred)))
    if fifty != 0:
        print("{} fifty dollar bills".format(int(fifty)))
    if twenty != 0:
        print("{} twenty dollar bills".format(int(twenty)))
    if ten != 0:
        print("{} ten dollar bills".format(int(ten)))
    if five != 0:
        print("{} five dollar bills".format(int(five)))
    if one != 0:
        print("{} one dollar bills".format(int(one)))
    if quarters != 0:
        print("{} quarters".format(int(quarters)))
    if dimes != 0:
        print("{} dimes".format(int(dimes)))
    if nickels != 0:
        print("{} nickels".format(int(nickels)))
    if pennies != 0:
        print("{} pennies".format(int(pennies)))


if __name__ == "__main__":
    while True:
        try:
            Money = float(input("Change: "))
            if Money >= 0:
                break
        except ValueError:
            print("Oops, need an int or float.")

    greedy(Money)
