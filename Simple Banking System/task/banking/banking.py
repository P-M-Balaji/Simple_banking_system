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
        return str(self.balance_)[1]


class Card:
    def __init__(self):
        self.choice2 = 1
        self.codeword_ = ""
        self.codeword_list = []
        self.sum = 0
        self.code_ = "400000" + str(random.randint(100000000, 999999999))
        self.checksum_ = self.checksum(self.code_)
        self.balance_ = 0
        self.pin = random.randint(1000, 9999)
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
        self.code_ = "400000" + str(random.randint(100000000, 999999999))
        self.checksum_ = self.checksum(self.code_)
        cur.execute('UPDATE card SET number = {} WHERE id = {}'.format(self.code_ + str(self.checksum_), count_))
        conn.commit()
        return self.code_ + str(self.checksum_)

    def create_pin(self, count_):
        self.pin = random.randint(1000, 9999)
        cur.execute('UPDATE card SET pin = {} WHERE id = {}'.format(self.pin, count_))
        conn.commit()
        return self.pin

    def create_balance(self, count_):
        self.balance_ = 0
        cur.execute('UPDATE card SET balance = {} WHERE id = {}'.format(self.balance_, count_))
        conn.commit()
        return self.balance_

    def login(self, card_num_, pin_num_):
        if card_num_ in str(self.card_db.get_card(card_num_)) and str(pin_num_) in str(self.card_db.get_pin(card_num_)):
            print("You have successfully logged in!")
            while True:
                self.choice2 = int(input("1. Balance\n2. Log out\n0. Exit\n"))
                if self.choice2 == 1:
                    print("\nBalance:", self.get_balance(card_num_))
                    continue
                if self.choice2 == 2:
                    print("You have successfully logged out!")
                    break
                else:
                    print("Bye!")
                    exit(0)
        else:
            print("Wrong card number or PIN!")

    def get_balance(self, card_num__):
        self.get_balance_ = str(self.card_db.get_balance_(card_num__))
        return self.get_balance_


count = 1
while 1:
    print("1. Create an account")
    print("2. Log into account")
    print("0. Exit")
    choice1 = int(input())
    if choice1 == 1:
        card_ = Card()
        cur.execute('INSERT INTO card (id, number, pin, balance) VALUES ({},NULL,NULL,0)'.format(count))
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
        exit(0)
