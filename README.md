# Bank Account Management System

A menu-driven **Bank Account Management System developed using Python** that demonstrates Object-Oriented Programming (OOP) concepts. The application allows users to create bank accounts, deposit money, withdraw money, check account balances, maintain transaction history, and save account data using CSV files.

## Features

- **Create Accounts:** Create savings accounts with a unique account number and account holder name.
- **Deposit Money:** Deposit money into an existing account.
- **Withdraw Money:** Withdraw money while checking for sufficient balance.
- **Check Balance:** Display account details and current balance.
- **Transaction History:** View recorded transactions for a particular account.
- **Save Account Data:** Store account information in a CSV file.
- **Load Account Data:** Automatically load saved accounts when the program starts.
- **Transaction Logging:** Maintain a history of account creation, deposits, and withdrawals.
- **Input Validation:** Validate monetary amounts and prevent invalid transactions.
- **Exception Handling:** Handle invalid inputs, duplicate account numbers, insufficient balance, and file errors.

## Technologies Used

- **Programming Language:** Python 3
- **Programming Paradigm:** Object-Oriented Programming (OOP)
- **Data Storage:** CSV (Comma-Separated Values)
- **Python Modules:** `csv`, `os`, `abc`, `decimal`, and `datetime`

## OOP Concepts Implemented

This project demonstrates the following six concepts:

1. **Classes and Objects:** Uses `BankAccount`, `SavingsAccount`, and `BankManager` classes.
2. **Encapsulation:** Uses private attributes such as `__account_number`, `__holder_name`, and `__balance`.
3. **Inheritance:** The `SavingsAccount` class inherits from the abstract `BankAccount` class.
4. **Abstraction:** Uses the `ABC` module and an abstract `account_type()` method.
5. **File Handling:** Reads and writes account data and transaction history using CSV files.
6. **Exception Handling:** Handles invalid amounts, insufficient balance, and file-related errors.

## Project Structure

```text
BankManagementSystem/
├── main.py
├── accounts.csv
├── transactions.csv
└── README.md
```

- `main.py` — Contains the complete Python application.
- `accounts.csv` — Stores account numbers, holder names, account types, and balances.
- `transactions.csv` — Stores transaction dates, account numbers, transaction types, and amounts.
- `README.md` — Contains project documentation.

**Note:** The CSV files are created automatically when the program saves account or transaction data. Keep existing CSV files when restarting the application so previously saved data remains available.

## Requirements

- Python 3 installed on your system.
- A code editor such as Visual Studio Code.

No external Python packages are required.

## Installation and Setup

### 1. Clone the repository

If the project is hosted on GitHub, clone it using:

```bash
git clone YOUR_REPOSITORY_URL
```

Replace `YOUR_REPOSITORY_URL` with your actual GitHub repository URL.

### 2. Open the project folder

```bash
cd BankManagementSystem
```

### 3. Run the application

On macOS or Linux:

```bash
python3 main.py
```

On Windows:

```bash
python main.py
```

## How to Use

When the program starts, it displays the following menu:

```text
======= BANK ACCOUNT MANAGEMENT SYSTEM =======
1. Create Account
2. Deposit Money
3. Withdraw Money
4. Check Balance
5. Transaction History
6. Save Account Data
7. Exit

Enter your choice (1-7):
```

Enter the number corresponding to the operation you want to perform.

### Example: Creating an Account

```text
Enter your choice (1-7): 1
Enter account number: 1001
Enter account holder name: Rahul Sharma

Account created successfully!
```

### Example: Depositing Money

```text
Enter your choice (1-7): 2
Enter account number: 1001
Enter deposit amount: Rs. 5000

Deposit successful!
New balance: Rs. 5000.00
```

### Example: Withdrawing Money

```text
Enter your choice (1-7): 3
Enter account number: 1001
Enter withdrawal amount: Rs. 1200

Withdrawal successful!
Remaining balance: Rs. 3800.00
```

### Example: Checking Balance

```text
Enter your choice (1-7): 4
Enter account number: 1001

========== ACCOUNT DETAILS ==========
Account Number : 1001
Account Holder : Rahul Sharma
Account Type   : Savings
Current Balance: Rs. 3800.00
=====================================
```

## Data Storage

### accounts.csv

Stores account information using the following fields:

| Field | Description |
|---|---|
| `account_number` | Unique account identifier |
| `holder_name` | Account holder's name |
| `account_type` | Account type |
| `balance` | Current account balance |

### transactions.csv

Stores transaction history using the following fields:

| Field | Description |
|---|---|
| `date` | Transaction date and time |
| `account_number` | Account associated with the transaction |
| `type` | Account creation, deposit, or withdrawal |
| `amount` | Transaction amount |

The application loads saved account data and transaction history when it starts.

## Learning Objectives

This project helps demonstrate:

- Practical implementation of OOP principles in Python.
- Creating abstract classes and derived classes.
- Applying encapsulation, inheritance, and abstraction.
- Implementing deposit and withdrawal operations.
- Performing monetary calculations with Python's `Decimal` class.
- Reading and writing CSV files.
- Maintaining transaction history.
- Validating user input and handling exceptions.

## Future Enhancements

Possible improvements include:

- A graphical user interface using Tkinter.
- Database integration using SQLite or MySQL.
- PIN-based authentication and secure login.
- Multiple account types, such as savings and current accounts.
- Fund transfers between accounts.
- Monthly transaction statements.
- Account closure and customer management.
- More robust transaction processing and audit logging.

## Security Disclaimer

This is an educational console application, not a production banking system. It does not implement user authentication, authorization, encryption, or secure banking infrastructure. CSV files are not suitable for storing real customer financial data.

## Author

**Your Name:** Vishal Bagdi

## License

This project is intended for educational and learning purposes. You may modify and extend it for your own use.