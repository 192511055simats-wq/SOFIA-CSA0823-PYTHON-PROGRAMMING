from decimal import Decimal, InvalidOperation
import csv
 
def calculate_hostel_bills(filename):
    total = Decimal("0.00")
    accepted = 0
    rejected = []
 
    try:
        with open(filename, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            for line_no, row in enumerate(reader, start=1):
                try:
                    if len(row) != 3:
                        raise ValueError("expected register_no, name, amount")
                    register_no, name, amount_text = [x.strip() for x in row]
 
                    if not register_no or not name:
                        raise ValueError("register number and name are required")
 
                    amount = Decimal(amount_text)
                    if not amount.is_finite() or amount < 0:
                        raise ValueError("amount must be a finite non-negative number")
 
                    total += amount
                    accepted += 1
                except (ValueError, InvalidOperation) as error:
                    rejected.append((line_no, row, str(error)))
 
        print(f"Accepted records: {accepted}")
        print(f"Total hostel bill: Rs. {total:.2f}")
        print(f"Rejected records: {len(rejected)}")
        for line_no, row, reason in rejected:
            print(f"Line {line_no}: {row} -> {reason}")
 
        return total, rejected
 
    except FileNotFoundError:
        print(f"Error: file not found: {filename}")
    except PermissionError:
        print(f"Error: permission denied: {filename}")
    except UnicodeDecodeError:
        print("Error: input file is not valid UTF-8 text.")
    except OSError as error:
        print(f"File system error: {error}")
 
    return None, []
 
if __name__ == "__main__":
    calculate_hostel_bills("hostel_bills.csv")
