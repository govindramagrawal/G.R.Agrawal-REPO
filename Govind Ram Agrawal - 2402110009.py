"""
Micro-Loan Ledger & EMI Tracker : Phase - 1 Submission
------  ------  -----  Govind Ram Agrawal - 2402110009
"""

loans = {}
borrowers = set()
payments = []
PASSWORD = "Namaste"
next_loan_id = 1
next_payment_id = 1

# ---------------- LOGIN ----------------
def login():
    print("\nWelcome to Micro-Loan Ledger & EMI Tracker")
    attempts = 3
    while attempts > 0:
        pwd = input("Enter password (or type 'exit' to quit): ").strip()
        if pwd.lower() == "exit":
            print("Exiting program. Namaste!")
            exit()
        else:
            if pwd == PASSWORD:
                print("\nLogin successful.")
                return
            else:
                attempts -= 1
                if attempts > 0:
                    print(f"Incorrect password. Attempts left: {attempts}")
                    print("")
                else:
                    print("Maximum attempts reached. Please restart the program to try again.")
                    exit()


# ---------------- EMI CALCULATION ----------------
def calculate_emi(principal, monthly_rate, term_months):
    if monthly_rate == 0:
        return principal / term_months
    emi = (principal * monthly_rate * (1 + monthly_rate) ** term_months) / ((1 + monthly_rate) ** term_months - 1)
    return round(emi, 2)


# ---------------- ADD NEW LOAN ----------------
def add_new_loan():
    global next_loan_id
    print("\n--- Add New Loan ---")
    name = input("Borrower name: ").strip()
    if name == "":
        print("Borrower name cannot be empty.")
        return

    try:
        principal = float(input("Principal amount: ").strip())
        rate = float(input("Monthly interest rate (e.g., 0.02 for 2%): ").strip())
        term = int(input("Term (in months): ").strip())
    except:
        print("Invalid input. Please enter numeric values for loan details.")
        return

    emi = calculate_emi(principal, rate, term)
    loans[next_loan_id] = (name, principal, rate, term, emi)
    borrowers.add(name)
    print(f"New loan successfully added. Assigned Loan ID: {next_loan_id} | EMI: {emi}")
    next_loan_id += 1


# ---------------- VIEW LOAN DETAILS ----------------
def view_loan_details():
    print("\n--- View Loan Details ---")
    if not loans:
        print("No loans available in the system.")
        return

    try:
        loan_id = int(input("Enter Loan ID: ").strip())
    except:
        print("Invalid input. Please enter a valid numeric Loan ID.")
        return

    if loan_id in loans:
        name, principal, rate, term, emi = loans[loan_id]
        print(f"\nLoan ID: {loan_id}")
        print(f"Borrower: {name}")
        print(f"Principal: {principal}")
        print(f"Monthly Rate: {rate}")
        print(f"Term (months): {term}")
        print(f"EMI: {emi}")

        total_paid = 0
        count_payments = 0
        for pay in payments:
            if pay[1] == loan_id:
                total_paid += pay[2]
                count_payments += 1

        remaining = round(principal - total_paid, 2)
        if remaining <= 0:
            remaining = 0.0
            print("Loan fully settled. Congratulations!")
        else:
            print(f"Payments made: {count_payments}")
            print(f"Total amount paid: {round(total_paid, 2)}")
            print(f"Outstanding balance: {remaining}")
    else:
        print("No active loan found with the provided Loan ID.")


# ---------------- MODIFY LOAN ----------------
def modify_loan():
    print("\n--- Modify Loan ---")
    if not loans:
        print("No loans available for modification.")
        return

    try:
        loan_id = int(input("Enter Loan ID to modify: ").strip())
    except:
        print("Invalid input. Please enter a valid Loan ID.")
        return

    if loan_id not in loans:
        print("No active loan found with the provided Loan ID.")
        return

    name, principal, rate, term, emi = loans[loan_id]
    print(f"Current Loan Details:\nBorrower: {name} | Principal: {principal} | Rate: {rate} | Term: {term} | EMI: {emi}")
    print("\n1. Update Interest Rate\n2. Update Term (months)\n3. Update Principal")
    choice = input("Select an option (or press Enter to cancel): ").strip()

    if choice == "1":
        try:
            rate = float(input("Enter new monthly rate: ").strip())
            print("Interest rate updated successfully.")
        except:
            print("Invalid rate entered. Update cancelled.")
            return
    elif choice == "2":
        try:
            term = int(input("Enter new term (in months): ").strip())
            print("Loan term updated successfully.")
        except:
            print("Invalid term entered. Update cancelled.")
            return
    elif choice == "3":
        try:
            principal = float(input("Enter new principal amount: ").strip())
            print("Principal amount updated successfully.")
        except:
            print("Invalid principal entered. Update cancelled.")
            return
    else:
        print("No changes were made.")
        return

    emi = calculate_emi(principal, rate, term)
    loans[loan_id] = (name, principal, rate, term, emi)
    print(f"Loan details updated successfully. Revised EMI: {emi}")


# ---------------- DELETE LOAN ----------------
def delete_loan():
    print("\n--- Delete Loan ---")
    if not loans:
        print("No loans available for deletion.")
        return

    try:
        loan_id = int(input("Enter the Loan ID to delete: ").strip())
    except:
        print("Invalid input. Please enter a valid Loan ID.")
        return

    if loan_id in loans:
        while True:
            confirm = input("Are you sure you want to permanently delete this loan? (yes/no): ").strip().lower()
            if confirm == "yes":
                borrower_name = loans[loan_id][0]
                del loans[loan_id]

                has_other_loans = any(l[0] == borrower_name for l in loans.values())
                if not has_other_loans and borrower_name in borrowers:
                    borrowers.remove(borrower_name)
                    print(f"Borrower '{borrower_name}' removed from active list.")

                global payments
                payments = [p for p in payments if p[1] != loan_id]

                print("Loan record and associated payment history deleted successfully.")
                break
            elif confirm == "no":
                print("Deletion cancelled. No changes made.")
                break
            else:
                print("Invalid choice. Please type 'yes' or 'no'.")
    else:
        print("No active loan found with the provided Loan ID.")


# ---------------- ADD PAYMENT ----------------
from datetime import datetime

def add_payment():
    global next_payment_id
    print("\n--- Record Loan Payment ---")
    if not loans:
        print("No active loans available. Please add a loan first.")
        return

    try:
        loan_id = int(input("Enter Loan ID: ").strip())
    except ValueError:
        print("Invalid input. Please enter a numeric Loan ID.")
        return

    if loan_id not in loans:
        print("No active loan found with the provided Loan ID.")
        return

    try:
        amount = float(input("Enter payment amount: ").strip())
        if amount <= 0:
            print("Payment amount must be positive.")
            return
    except ValueError:
        print("Invalid amount entered. Please enter a valid number.")
        return

    # Validating date format
    while True:
        date_input = input("Enter payment date (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(date_input, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date format. Please enter in YYYY-MM-DD format (e.g., 2025-10-28).")

    payments.append((next_payment_id, loan_id, amount, date_input))
    print(f"Payment recorded successfully. Payment ID: {next_payment_id}")
    next_payment_id += 1


# ---------------- PAYMENT HISTORY ----------------
def payment_history():
    print("\n--- Payment History ---")
    if not payments:
        print("No payment records available.")
        return

    try:
        loan_id = int(input("Enter Loan ID to view payments (or 0 to view all): ").strip())
    except:
        print("Invalid input. Please enter a numeric value.")
        return

    # If user wants all payments
    if loan_id == 0:
        print("\nDisplaying all payment records:")
        for p in payments:
            print(f"Payment ID: {p[0]} | Loan ID: {p[1]} | Amount: ₹{p[2]:.2f} | Date: {p[3]}")
        return

    # Checking if loan exists
    if loan_id not in loans:
        print("No active loan found with that Loan ID. Please check and try again.")
        return

    # Displaying payments for the loan
    found = False
    print(f"\nPayment records for Loan ID: {loan_id}")
    for p in payments:
        if p[1] == loan_id:
            print(f"Payment ID: {p[0]} | Amount: ₹{p[2]:.2f} | Date: {p[3]}")
            found = True

    if not found:
        print("No payments recorded for this loan yet.")

# ---------------- BORROWER REPORT ----------------
def borrower_report():
    print("\n--- Borrower Summary Report ---")
    if not borrowers:
        print("No borrowers currently registered.")
    else:
        print("List of Active Borrowers:")
        for borrower in borrowers:
            print("-", borrower)


# ---------------- LOAN REPORT ----------------
def loan_report():
    print("\n--- Loan Summary Report ---")
    if not loans:
        print("No loan records available.")
        return

    print("-" * 60)
    print(f"{'Loan ID':<8}{'Borrower':<20}{'Principal':<12}{'EMI':<10}{'Term':<8}")
    print("-" * 60)
    for loan_id, data in loans.items():
        name, principal, rate, term, emi = data
        print(f"{loan_id:<8}{name:<20}{principal:<12}{emi:<10}{term:<8}")
    print("-" * 60)


# ---------------- SEARCH LOAN ----------------
def search_loan():
    print("\n--- Search Loan by Borrower Name ---")
    key = input("Enter the borrower's name: ").strip().lower()
    found = False

    for loan_id, data in loans.items():
        if key == data[0].lower():
            print(f"Loan ID: {loan_id} | Borrower: {data[0]} | Principal: {data[1]} | EMI: {data[4]}")
            found = True

    if not found:
        print("No loan records found for the given borrower name.")

# ---------------- LOAN STATUS REPORT ----------------
def loan_status_report():
    print("\n--- Loan Status Report ---")

    if not loans:
        print("No loan records available.")
        return

    print(f"{'Loan ID':<8} {'Borrower':<20} {'Principal':<12} {'Total Paid':<12} {'Balance':<12} {'Status':<10}")
    print("-" * 80)

    for loan_id, details in loans.items():
        borrower, principal, rate, term, emi = details

        total_paid = sum(p[2] for p in payments if p[1] == loan_id)
        balance = principal - total_paid

        if balance <= 0:
            status = "Paid Off"
            balance = 0
        else:
            status = "Active"

        print(f"{loan_id:<8} {borrower:<20} ₹{principal:<10.2f} ₹{total_paid:<10.2f} ₹{balance:<10.2f} {status:<10}")

    print("-" * 80)
    print("Report generated successfully.")


# ---------------- EMI DUE REPORT ----------------
def emi_due_report():
    print("\n--- EMI Due Report ---")
    if not loans:
        print("No loans found in the system.")
        return

    today = datetime.today().date()
    overdue_found = False

    for loan_id, (name, principal, rate, term, emi) in loans.items():
        total_paid = sum(p[2] for p in payments if p[1] == loan_id)
        payments_made = sum(1 for p in payments if p[1] == loan_id)

        if payments_made < term:
            remaining_months = term - payments_made
            overdue_found = True
            print(f"Loan ID: {loan_id} | Borrower: {name} | Payments Done: {payments_made}/{term} | Remaining: {remaining_months} | EMI: ₹{emi}")

    if not overdue_found:
        print("All EMIs are up to date.")

# ---------------- MAIN MENU ----------------
def main_menu():
    while True:
        print("\n========== MICRO-LOAN LEDGER & EMI TRACKER ==========")
        print("1. Add New Loan")
        print("2. View Loan Details")
        print("3. Modify Loan")
        print("4. Delete Loan")
        print("5. Record Payment")
        print("6. View Payment History")
        print("7. Borrower Report")
        print("8. Loan Report")
        print("9. Search Loan by Borrower Name")
        print("10. Loan Status Report")
        print("11. EMI Due Report")
        print("0. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            add_new_loan()
        elif choice == "2":
            view_loan_details()
        elif choice == "3":
            modify_loan()
        elif choice == "4":
            delete_loan()
        elif choice == "5":
            add_payment()
        elif choice == "6":
            payment_history()
        elif choice == "7":
            borrower_report()
        elif choice == "8":
            loan_report()
        elif choice == "9":
            search_loan()
        elif choice == "10":
            loan_status_report()
        elif choice == "11":
            emi_due_report()
        elif choice == "0":
            print("Exiting program. Namaste!")
            break
        else:
            print("Invalid choice. Please try again.")
            continue

        # --- Asking user if they want to continue ---
        while True:
            cont = input("\nWould you like to return to the main menu? (y/n): ").strip().lower()
            if cont in ["y", "yes"]:
                break
            elif cont in ["n", "no"]:
                print("\nThank you for using the Micro-Loan Ledger. Namaste!")
                return
            else:
                print("Invalid input. Please type 'y' or 'n'.")

if __name__ == "__main__":
    login()
    main_menu()