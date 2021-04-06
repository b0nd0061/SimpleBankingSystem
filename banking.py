import random
import sys
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS card (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               number TEXT,
               pin TEXT,
               balance INTEGER DEFAULT 0);''')
conn.commit()


def gen_card():
    while True:
        card = '400000' + "".join([str(i) for i in random.sample(range(10), 10)])
        if luhn(card) is True:
            return card


def luhn(card_number):
    summa = 0
    num_digits = len(card_number)
    odd_even = num_digits & 1
    for count in range(0, num_digits):
        digit = int(card_number[count])
        if not ((count & 1) ^ odd_even):
            digit = digit * 2
        if digit > 9:
            digit = digit - 9
        summa = summa + digit
    if summa % 10 == 0:
        return True
    else:
        return False


def gen_pin():
    pin = "".join([str(i) for i in random.sample(range(10), 4)])
    return pin


def add_db():
    cur.execute(f'''INSERT INTO card (number,pin) VALUES ({gen_card()},{gen_pin()});''')
    conn.commit()


def get_db(param):
    cur.execute(f'SELECT {param} FROM card ORDER BY id DESC LIMIT 1;')
    return cur.fetchone()


def get_balance(number_card, pin):
    cur.execute(f'SELECT balance FROM card WHERE number={number_card} and pin = {pin};')
    return cur.fetchone()


def check_acc_db(number_card, pin):
    cur.execute(f'SELECT * FROM card WHERE number={number_card} and pin = {pin};')
    if cur.fetchone():
        return True


def check_card_db(number_card):
    cur.execute(f'SELECT number FROM card WHERE number = {number_card};')
    if not cur.fetchone():
        return False


def check_balance(number_card, pin, amount):
    cur.execute(f'SELECT balance FROM card WHERE number={number_card} and pin = {pin};')
    int_cur = int(''.join(map(str, cur.fetchone())))
    if int_cur >= int(amount):
        return True
    else:
        return False


def create_acc():
    add_db()
    print("Your card has been created")
    print("Your card number:")
    print(*get_db('number'))
    print("Your card PIN:")
    print(*get_db('pin'))


def del_acc_db(number_card, pin):
    cur.execute(f'DELETE FROM card WHERE number={number_card} and pin = {pin};')
    conn.commit()


def add_money(number_card, pin, num_money):
    cur.execute(f'''UPDATE card SET balance = balance + {num_money}
                    WHERE number={number_card} and pin = {pin};''')
    conn.commit()
    print('Income was added!')


def transaction_money(from_number_card, pin, to_number_card, amount):
    cur.execute(f'''UPDATE card SET balance = balance - {amount}
                    WHERE number={from_number_card} and pin = {pin};''')

    cur.execute(f'''UPDATE card SET balance = balance + {amount}
                    WHERE number={to_number_card};''')
    conn.commit()


def transfer_money(number_card, pin):
    print('Transfer')
    print('Enter card number:')
    to_card_number = input()
    if luhn(to_card_number) is False:
        print('Probably you made a mistake in the card number. Please try again!')
    elif check_card_db(to_card_number) is False:
        print('Such a card does not exist.')
    else:
        print('Enter how much money you want to transfer:')
        amount_money = int(input())
        if check_balance(number_card, pin, amount_money) is True:
            transaction_money(number_card, pin, to_card_number, amount_money)
            print('Success!')
        else:
            print('Not enough money!')


def after_check(number_card, pin):
    print("You have successfully logged in!")
    while True:
        print("1. Balance",
              "2. Add income",
              "3. Do transfer",
              "4. Close account",
              "5. Log out",
              "0. Exit", sep="\n")
        n = int(input())
        if n == 1:
            print("Balance:", *get_balance(number_card, pin))
        elif n == 2:
            num_money = input()
            add_money(number_card, pin, num_money)
        elif n == 3:
            transfer_money(number_card, pin)
        elif n == 4:
            del_acc_db(number_card, pin)
            print('The account has been closed!')
            break
        elif n == 5:
            print('You have successfully logged out!')
            break
        else:
            sys.exit()


def logg_acc():
    print("Enter your card number:")
    num_card = input()
    print("Enter your PIN:")
    num_pin = input()
    if check_acc_db(num_card, num_pin) is True:
        after_check(num_card, num_pin)
    else:
        print("Wrong card number or PIN!")


def main():
    print("1. Create an account", "2. Log into account", "0. Exit", sep="\n")
    n = int(input())
    if n == 1:
        create_acc()
    elif n == 2:
        logg_acc()
    else:
        print("Bye!")
        sys.exit()


while True:
    main()
