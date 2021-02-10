import string
import random


# global variables
CARDS = []
user = {
    'info': {},
}


def menu():
    print()
    print('1. Create an account')
    print('2. Log into account')
    print('0. Exit')


def generate_card():
    IIN = '400000'
    account_number = "".join(random.choice(string.digits) for _ in range(9))
    checksum = '9'
    card_number = IIN + account_number + checksum
    return card_number


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
    card_info = {
        'card_number': card_number,
        'pin': pin,
        'balance': 0,
    }
    CARDS.append(card_info)


def login(card_info):
    user['info'] = card_info
    print('\nYou have successfully logged in!')
    dashboard()


def verification():
    print()
    print('Enter your card number:')
    card_number = input()
    print('Enter your PIN:')
    pin = input()

    # logging in the user by verifying info
    for card_info in CARDS:
        if card_info['card_number'] == card_number and card_info['pin'] == pin:
            login(card_info)
            return

    if not user['info']:
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
            print('Bye!')
            exit(0)


def balance():
    print()
    print('Balance:', user['info']['balance'])


def logout():
    user['info'] = {}
    print()
    print('You have successfully logged out!')


def main():
    while True:
        menu()
        command = int(input())
        if command == 1:
            create_account()
        elif command == 2:
            verification()
        elif command == 0:
            print('Bye!')
            exit(0)


if __name__ == '__main__':
    main()