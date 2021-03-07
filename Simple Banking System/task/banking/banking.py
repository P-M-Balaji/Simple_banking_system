import sqlite3
import random

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
conn.commit()


class CardDB:
    def __init__(self):
        self.pin_num_ = 0
        self.balance_ = 0
        self.card_number = ""

    def get_card(self, card_num_):
        cur.execute("SELECT number FROM card WHERE number = {};".format(card_num_))
        self.card_number = cur.fetchone()
        return self.card_number

    def get_pin(self, card_num_):
        cur.execute("SELECT pin FROM card WHERE number = {};".format(card_num_))
        self.pin_num_ = cur.fetchone()
        return self.pin_num_

    def get_balance_(self, card_num_):
        cur.execute("SELECT balance FROM card WHERE number = {};".format(card_num_))
        self.balance_ = cur.fetchone()
        return str(self.balance_)[1:-2]


class Card:
    def __init__(self):
        self.choice2 = 1
        self.codeword_ = ""
        self.codeword_list = []
        self.sum = 0
        self.code_ = "400000" + str(f"{random.randint(0, 999999999):09d}")
        self.checksum_ = self.checksum(self.code_)
        self.balance_ = 0
        self.pin = f"{random.randint(0, 9999):04d}"
        self.get_balance_ = 0
        self.card_db = CardDB()

    def checksum(self, codeword_):
        self.codeword_ = codeword_
        self.codeword_list = list(map(int, self.codeword_))
        for x in self.codeword_list[::2]:
            index_ = self.codeword_list.index(x)
            self.codeword_list[index_] = x * 2
            if self.codeword_list[index_] > 9:
                self.codeword_list[index_] -= 9
        self.sum = 0
        for x in self.codeword_list:
            self.sum += x
        return 10 - (self.sum % 10) if self.sum % 10 != 0 else 0

    def create_code(self, count_):
        self.code_ = "400000" + str(f"{random.randint(0, 999999999):09d}")
        self.checksum_ = self.checksum(self.code_)
        cur.execute(f'UPDATE card SET number = {self.code_ + str(self.checksum_)} WHERE id = {count_};')
        conn.commit()
        return self.code_ + str(self.checksum_)

    def create_pin(self, count_):
        self.pin = f"{random.randint(0, 9999):04d}"
        cur.execute(f'UPDATE card SET pin = {self.pin} WHERE id = {count_};')
        conn.commit()
        return self.pin

    def create_balance(self, count_):
        self.balance_ = 0
        cur.execute(f'UPDATE card SET balance = {self.balance_} WHERE id = {count_};')
        conn.commit()
        return self.balance_

    def login(self, card_num_, pin_num_):
        if card_num_ in str(self.card_db.get_card(card_num_)) and str(pin_num_) in str(self.card_db.get_pin(card_num_)):
            print("You have successfully logged in!")
            while True:
                print("1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit\n")
                self.choice2 = int(input())
                if self.choice2 == 1:
                    print("\nBalance:", self.get_balance(card_num_))
                    continue
                if self.choice2 == 2:
                    credit = int(input("Enter income:"))
                    self.balance_ = int(self.get_balance(card_num_))
                    self.balance_ = self.balance_ + credit
                    cur.execute(f'UPDATE card SET balance = {self.balance_} WHERE number = {card_num_};')
                    conn.commit()
                    print("Income was added!")
                    continue
                if self.choice2 == 3:
                    print("\nTransfer")
                    card_no = input("Enter card number:")
                    if card_no in str(self.card_db.get_card(card_no)):
                        transfer = int(input("Enter how much money you want to transfer:"))
                        if transfer < self.balance_:
                            balance_ = self.get_balance(card_num_) - transfer
                            cur.execute(f'UPDATE card SET balance = {balance_} WHERE number = {card_num_};')
                            conn.commit()
                            balance_ = self.get_balance(card_no) + transfer
                            cur.execute(f'UPDATE card SET balance = {balance_} WHERE number = {card_no};')
                            conn.commit()
                            print("Success!")
                            continue
                        else:
                            print("Not enough money!")
                            continue
                    elif self.checksum(card_no[0:-1]) != card_no[-1] and card_no[:6] == "400000":
                        print("Probably you made a mistake in the card number. Please try again!")
                        continue
                    else:
                        print("Such a card does not exist.")
                        continue
                if self.choice2 == 4:
                    conn.execute(f'DELETE FROM card WHERE number = {card_num_};')
                    conn.commit()
                    print("\nThe account has been closed!")
                    break
                if self.choice2 == 5:
                    print("You have successfully logged out!")
                    break
                else:
                    print("Bye!")
                    cur.close()
                    exit(0)
        else:
            print("Wrong card number or PIN!")

    def get_balance(self, card_num__):
        self.get_balance_ = self.card_db.get_balance_(card_num__)
        return int(self.get_balance_)


count = 1
while 1:
    print("1. Create an account")
    print("2. Log into account")
    print("0. Exit")
    choice1 = int(input())
    if choice1 == 1:
        card_ = Card()
        cur.execute('INSERT INTO card (id, number, pin, balance) VALUES ({},NULL,NULL,0);'.format(count))
        conn.commit()
        card_number = card_.create_code(count)
        print("Your card has been created\nYour card number:")
        print(card_number)
        pin_number = card_.create_pin(count)
        print("Your card PIN:")
        print(pin_number)
        balance = card_.create_balance(count)
        count += 1
        continue
    if choice1 == 2:
        card_ = Card()
        card_num = input("\nEnter your card number:")
        pin_num = int(input("Enter your PIN:"))
        card_.login(card_num, pin_num)
    else:
        print("Bye!")
        cur.close()
        exit(0)
