import json
import os
import getpass
from datetime import datetime

ACCOUNTS_FILE = "accounts.json"

def load_accounts():
    if not os.path.exists(ACCOUNTS_FILE):
        demo = {
            "1001": {"name": "Harsha", "pin": "1234", "balance": 50000.0, "history": []},
            "1002": {"name": "Ravi", "pin": "4321", "balance": 15000.0, "history": []}
        }
        save_accounts(demo)
        return demo
    with open(ACCOUNTS_FILE, "r") as f:
        return json.load(f)

def save_accounts(accounts):
    with open(ACCOUNTS_FILE, "w") as f:
        json.dump(accounts, f, indent=2)

def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def append_history(account, desc, amount, accounts):
    entry = {"time": timestamp(), "desc": desc, "amount": float(amount), "balance": float(accounts[account]["balance"])}
    accounts[account].setdefault("history", []).append(entry)

def check_balance(acc_id, accounts):
    print(f"\nAvailable balance: ₹{accounts[acc_id]['balance']:.2f}\n")

def withdraw(acc_id, accounts):
    try:
        amt = float(input("Enter withdrawal amount: ₹"))
    except ValueError:
        print("Invalid amount")
        return
    if amt <= 0 or amt > accounts[acc_id]["balance"]:
        print("Invalid or insufficient balance")
        return
    accounts[acc_id]["balance"] -= amt
    append_history(acc_id, "Withdrawal", -amt, accounts)
    save_accounts(accounts)
    print(f"Please collect your cash: ₹{amt:.2f}")

def fast_cash(acc_id, accounts):
    options = [100, 500, 1000, 2000, 5000]
    for i, o in enumerate(options, start=1):
        print(f" {i}. ₹{o}")
    choice = input("Choose option: ")
    if not choice.isdigit() or int(choice) not in range(1, len(options)+1):
        print("Invalid selection")
        return
    amt = options[int(choice)-1]
    if amt > accounts[acc_id]["balance"]:
        print("Insufficient balance")
        return
    accounts[acc_id]["balance"] -= amt
    append_history(acc_id, f"Fast Cash ₹{amt}", -amt, accounts)
    save_accounts(accounts)
    print(f"Dispensed: ₹{amt}")

def deposit(acc_id, accounts):
    try:
        amt = float(input("Enter deposit amount: ₹"))
    except ValueError:
        print("Invalid amount")
        return
    if amt <= 0:
        print("Amount must be greater than 0")
        return
    accounts[acc_id]["balance"] += amt
    append_history(acc_id, "Cash Deposit", amt, accounts)
    save_accounts(accounts)
    print(f"₹{amt:.2f} deposited successfully")

def transfer_funds(acc_id, accounts):
    to_acc = input("Enter beneficiary account number: ")
    if to_acc not in accounts or to_acc == acc_id:
        print("Invalid beneficiary account")
        return
    try:
        amt = float(input("Enter transfer amount: ₹"))
    except ValueError:
        print("Invalid amount")
        return
    if amt <= 0 or amt > accounts[acc_id]["balance"]:
        print("Invalid or insufficient balance")
        return
    accounts[acc_id]["balance"] -= amt
    accounts[to_acc]["balance"] += amt
    append_history(acc_id, f"Transfer to {to_acc}", -amt, accounts)
    append_history(to_acc, f"Transfer from {acc_id}", amt, accounts)
    save_accounts(accounts)
    print("Transfer successful")

def mini_statement(acc_id, accounts, limit=10):
    history = accounts[acc_id].get("history", [])[-limit:]
    if not history:
        print("No transactions yet")
        return
    for entry in history:
        print(f"{entry['time']} | {entry['desc']} | ₹{entry['amount']:.2f} | Bal: ₹{entry['balance']:.2f}")

def change_pin(acc_id, accounts):
    cur = input("Enter current PIN: ")
    if cur != accounts[acc_id]["pin"]:
        print("Incorrect PIN")
        return
    new = input("Enter new 4-digit PIN: ")
    if len(new) != 4 or not new.isdigit():
        print("PIN must be 4 digits")
        return
    accounts[acc_id]["pin"] = new
    save_accounts(accounts)
    print("PIN changed successfully")

def authenticate(accounts):
    acc_id = input("Enter account number: ")
    if acc_id not in accounts:
        print("Account not found")
        return None
    for _ in range(3):
        pin = input("Enter PIN: ")
        if pin == accounts[acc_id]["pin"]:
            return acc_id
        print("Incorrect PIN")
    return None

def main_menu(acc_id, accounts):
    while True:
        print("\n1. Balance Enquiry\n2. Withdrawal\n3. Fast Cash\n4. Cash Deposit\n5. Transfer Funds\n6. Mini Statement\n7. Change PIN\n8. Logout")
        choice = input("Choice: ")
        if choice == "1": check_balance(acc_id, accounts)
        elif choice == "2": withdraw(acc_id, accounts)
        elif choice == "3": fast_cash(acc_id, accounts)
        elif choice == "4": deposit(acc_id, accounts)
        elif choice == "5": transfer_funds(acc_id, accounts)
        elif choice == "6": mini_statement(acc_id, accounts)
        elif choice == "7": change_pin(acc_id, accounts)
        elif choice == "8": break
        else: print("Invalid choice")

if __name__ == "__main__":
    accounts = load_accounts()
    while True:
        print("\n--- ATM System ---\n1. Login\n2. Exit")
        choice = input("Choice: ")
        if choice == "1":
            acc = authenticate(accounts)
            if acc: main_menu(acc, accounts)
        elif choice == "2": break
        else: print("Invalid choice")
