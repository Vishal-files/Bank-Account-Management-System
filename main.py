import csv
import os
from decimal import Decimal, InvalidOperation
from datetime import datetime
from abc import ABC, abstractmethod


# Abstract Base Class

class BankAccount(ABC):

    def __init__(self, account_number, holder_name, balance=0):
        self.__account_number = int(account_number)
        self.__holder_name = holder_name.strip()
        self.__balance = self.validate_money(balance)

        if not self.__account_number:
            raise ValueError("Account number cannot be empty.")

        if not self.__holder_name:
            raise ValueError("Account holder name cannot be empty.")

        if self.__balance < 0:
            raise ValueError("Balance cannot be negative.")

    @staticmethod
    def validate_money(amount):
        try:
            value = Decimal(str(amount))

            if not value.is_finite():
                raise ValueError("Enter a valid monetary amount.")

            if value.as_tuple().exponent < -2:
                raise ValueError("Maximum two decimal places allowed.")

            return value.quantize(Decimal("0.01"))

        except (InvalidOperation, TypeError):
            raise ValueError("Enter a valid monetary amount.")

    @property
    def account_number(self):
        return self.__account_number

    @property
    def holder_name(self):
        return self.__holder_name

    @property
    def balance(self):
        return self.__balance

    def deposit(self, amount):
        amount = self.validate_money(amount)

        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")

        self.__balance += amount

    def withdraw(self, amount):
        amount = self.validate_money(amount)

        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")

        if amount > self.__balance:
            raise ValueError("Insufficient balance.")

        self.__balance -= amount

    @abstractmethod
    def account_type(self):
        pass

    def display_details(self):
        print("-" * 48)
        print("Account Number :", self.account_number)
        print("Holder Name    :", self.holder_name)
        print("Account Type   :", self.account_type())
        print(f"Balance        : Rs. {self.balance:.2f}")
        print("-" * 48)


# SavingsAccount

class SavingsAccount(BankAccount):

    def account_type(self):
        return "Savings"


# BankManager

class BankManager:

    ACCOUNT_FILE = "Bank-Account-Management-System/accounts.csv"
    TRANSACTION_FILE = "Bank-Account-Management-System/transactions.csv"

    def __init__(self):
        self.__accounts = {}
        self.__transactions = []

        self.load_accounts()
        self.load_transactions()

    def create_account(self):
        try:
            account_number = int(input("Enter account number: "))

            if not account_number:
                raise ValueError("Account number cannot be empty.")

            if account_number in self.__accounts:
                raise ValueError("Account number already exists.")

            holder_name = str(input("Enter account holder name: "))

            account = SavingsAccount(
                account_number,
                holder_name,
                Decimal("0.00")
            )

            self.__accounts[account_number] = account

            try:
                self.save_accounts()
            except OSError:
                del self.__accounts[account_number]
                raise

            self.record_transaction(
                account_number, "ACCOUNT CREATED", Decimal("0.00")
            )

            print("Account created successfully!")

        except ValueError as error:
            print("Invalid input:", error)
        except OSError as error:
            print("File error:", error)

    def find_account(self, account_number):
        account = self.__accounts.get(account_number)

        if account is None:
            print("Account not found.")

        return account

    def deposit_money(self):
        account_number = int(input("Enter account number: "))
        account = self.find_account(account_number)

        if account is None:
            return

        try:
            amount = int(input("Enter deposit amount: Rs. "))
            amount = BankAccount.validate_money(amount)

            old_balance = account.balance
            account.deposit(amount)

            try:
                self.save_accounts()
            except OSError:
                account.withdraw(amount)
                raise

            try:
                self.record_transaction(account_number, "DEPOSIT", amount)
            except OSError as error:
                print("Transaction log could not be saved:", error)

            print(f"Deposit successful! Balance: Rs. {account.balance:.2f}")

        except ValueError as error:
            print("Transaction failed:", error)
        except OSError as error:
            print("File error:", error)

    def withdraw_money(self):
        account_number = int(input("Enter account number: "))
        account = self.find_account(account_number)

        if account is None:
            return

        try:
            amount = int(input("Enter withdrawal amount: Rs. "))
            amount = BankAccount.validate_money(amount)

            account.withdraw(amount)

            try:
                self.save_accounts()
            except OSError:
                account.deposit(amount)
                raise

            try:
                self.record_transaction(account_number, "WITHDRAWAL", amount)
            except OSError as error:
                print("Transaction log could not be saved:", error)

            print(f"Withdrawal successful! Balance: Rs. {account.balance:.2f}")

        except ValueError as error:
            print("Transaction failed:", error)
        except OSError as error:
            print("File error:", error)

    def check_balance(self):
        account_number = int(input("Enter account number: "))
        account = self.find_account(account_number)

        if account:
            account.display_details()

    def show_transactions(self):
        account_number = int(input("Enter account number: "))

        if account_number not in self.__accounts:
            print("Account not found.")
            return

        history = [
            transaction for transaction in self.__transactions
            if transaction["account_number"] == account_number
        ]

        if not history:
            print("No transactions found.")
            return

        print("\n========== TRANSACTION HISTORY ==========")
        print(
            f"{'Date and Time':<22}"
            f"{'Type':<18}"
            f"{'Amount (Rs.)':>14}"
        )
        print("-" * 56)

        for transaction in history:
            print(
                f"{transaction['date']:<22}"
                f"{transaction['type']:<18}"
                f"{Decimal(transaction['amount']):>14.2f}"
            )

    def record_transaction(self, account_number, kind, amount):
        transaction = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "account_number": account_number,
            "type": kind,
            "amount": f"{amount:.2f}"
        }

        with open( self.TRANSACTION_FILE, "a", newline="", encoding="utf-8" ) as file:
            writer = csv.writer(file)

            if file.tell() == 0:
                writer.writerow([
                    "date", "account_number", "type", "amount"
                ])

            writer.writerow([
                transaction["date"],
                transaction["account_number"],
                transaction["type"],
                transaction["amount"]
            ])

        self.__transactions.append(transaction)

    def save_accounts(self):
        with open( self.ACCOUNT_FILE, "w", newline="", encoding="utf-8" ) as file:
            writer = csv.writer(file)

            writer.writerow([
                "account_number",
                "holder_name",
                "account_type",
                "balance"
            ])

            for account in self.__accounts.values():
                writer.writerow([
                    account.account_number,
                    account.holder_name,
                    account.account_type(),
                    f"{account.balance:.2f}"
                ])

    def load_accounts(self):
        if not os.path.exists(self.ACCOUNT_FILE):
            return

        try:
            with open( self.ACCOUNT_FILE, "r", newline="", encoding="utf-8" ) as file:
                reader = csv.DictReader(file)

                required = {"account_number", "holder_name", "account_type", "balance"}

                if not reader.fieldnames or not required.issubset(
                    reader.fieldnames
                ):
                    raise ValueError("Invalid accounts CSV format.")

                for row in reader:
                    if row["account_type"] != "Savings":
                        raise ValueError("Unknown account type.")

                    account = SavingsAccount(
                        row["account_number"],
                        row["holder_name"],
                        row["balance"]
                    )

                    if account.account_number in self.__accounts:
                        raise ValueError("Duplicate account number.")

                    self.__accounts[account.account_number] = account

        except (OSError, ValueError, KeyError, csv.Error) as error:
            self.__accounts.clear()
            print("Could not load accounts:", error)

    def load_transactions(self):
        if not os.path.exists(self.TRANSACTION_FILE):
            return

        try:
            with open( self.TRANSACTION_FILE, "r", newline="", encoding="utf-8" ) as file:
                reader = csv.DictReader(file)

                required = {"date", "account_number", "type", "amount"}

                if not reader.fieldnames or not required.issubset(
                    reader.fieldnames
                ):
                    raise ValueError("Invalid transaction CSV format.")

                for row in reader:
                    amount = BankAccount.validate_money(row["amount"])

                    if row["account_number"] not in self.__accounts:
                        raise ValueError(
                            "Transaction references an unknown account."
                        )

                    self.__transactions.append({
                        "date": row["date"],
                        "account_number": row["account_number"],
                        "type": row["type"],
                        "amount": f"{amount:.2f}"
                    })

        except (OSError, ValueError, KeyError, csv.Error) as error:
            self.__transactions.clear()
            print("Could not load transaction history:", error)


# MAIN PROGRAM

def main():
    bank = BankManager()

    while True:
        print("\n======= BANK ACCOUNT MANAGEMENT SYSTEM =======")
        print("1. For Create Account -> press 1")
        print("2. For Deposit Money -> press 2")
        print("3. For Withdraw Money -> press 3")
        print("4. For Check Balance -> press 4")
        print("5. For Transaction History -> press 5")
        print("6. For Save Account Data -> press 6")
        print("7. For Exit -> press 7\n")

        choice = int(input(" ✹ Enter your choice (1-7): "))

        try:
            if choice == 1:
                bank.create_account()

            elif choice == 2:
                bank.deposit_money()

            elif choice == 3:
                bank.withdraw_money()

            elif choice == 4:
                bank.check_balance()

            elif choice == 5:
                bank.show_transactions()

            elif choice == 6:
                bank.save_accounts()
                print("Account data saved successfully!")

            elif choice == 7:
                bank.save_accounts()
                print("Account data saved. Goodbye!")
                break

            else:
                print("Invalid choice. Please enter 1-7.")

        except OSError as error:
            print("File operation failed:", error)


if __name__ == "__main__":
    main()
