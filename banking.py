import sqlite3
import random
import string


user = None
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()


def menu():
    print()
    print('1. Create an account')
    print('2. Log into account')
    print('0. Exit')


def generate_card():
    IIN = '400000'
    account_number = "".join(str(random.randint(0, 9)) for _ in range(9))
    card_number = IIN + account_number

    card_number += str(checksum(card_number))
    return card_number


def checksum(card_number):
    total = 0
    for i, digit in enumerate(card_number):
        digit = int(digit)
        if i % 2 == 0:
            digit *= 2
            total += digit if digit <= 9 else digit - 9
        else:
            total += digit

    return 10 - total % 10 if total % 10 != 0 else 0


def create_account():
    print('\nYour card has been created')

    # Generate a card number
    card_number = generate_card()
    print('Your card number:')
    print(card_number)

    # Generate a pin for the card
    print('Your card PIN:')
    pin = "".join(random.choice(string.digits) for _ in range(4))
    print(pin)

    # Insert card info to DB
    cur.execute('INSERT INTO card (number, pin) VALUES (?, ?);', (card_number, pin))
    conn.commit()


def login(card_info):
    global user
    user = card_info
    print('\nYou have successfully logged in!')
    dashboard()


def verification():
    global conn, cur
    print()
    print('Enter your card number:')
    card_number = input()
    print('Enter your PIN:')
    pin = input()

    # logging in the user by verifying info
    cur.execute('SELECT * FROM card WHERE number = ? and pin = ?;', (card_number, pin))

    data = cur.fetchone()

    if data:
        card_info = {
            'id': data[0],
            'balance': data[3],
        }
        login(card_info)
    else:
        print('\nWrong card number or PIN!')


def dashboard():
    while True:
        print()
        print('1. Balance')
        print('2. Log out')
        print('0. Exit')
        command = int(input())

        if command == 1:
            balance()
        elif command == 2:
            logout()
            return
        elif command == 0:
            bye()


def balance():
    print()
    global user
    print('Balance:', user.get('balance'))


def logout():
    global user
    user = None
    print()
    print('You have successfully logged out!')


def create_table():
    global conn, cur
    cur.execute('CREATE TABLE IF NOT EXISTS card ('
                'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                'number TEXT,'
                'pin TEXT,'
                'balance INTEGER DEFAULT 0'
                ');')
    conn.commit()


def cc_close():
    cur.close()
    conn.close()


def bye():
    print('Bye!')
    cc_close()
    exit(0)


def main():
    create_table()
    while True:
        menu()
        command = int(input())
        if command == 1:
            create_account()
        elif command == 2:
            verification()
        elif command == 0:
            bye()


if __name__ == '__main__':
    main()