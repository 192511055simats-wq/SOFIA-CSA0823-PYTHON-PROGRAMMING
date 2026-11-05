# Vehicle Registration Number Validator
def normalise(text):
    text = text.strip()
    text = text.replace(" ", "")
    text = text.replace("-", "")
    return text.upper()
def is_valid(reg):
    if len(reg) != 9 and len(reg) != 10:
        return False
    state = reg[0:2]
    district = reg[2:4]
    series = reg[4:-4]
    number = reg[-4:]
    if (state.isalpha() and
        district.isdigit() and
        len(series) >= 1 and len(series) <= 2 and
        series.isalpha() and
        number.isdigit()):
        return True
    else:
        return False
def format_number(reg):
    if is_valid(reg):
        return reg[0:2] + " " + reg[2:4] + " " + reg[4:-4] + " " + reg[-4:]
    else:
        return "Invalid Number"
# Six test inputs
vehicles = [
    "tn 09 ab 1234",
    "KA-01-M-0007",
    "Tn09Ab1234",
    "TN 22 1234 AB",
    "MH-12-ABC-5678",
    "TN-9-AB-1234"
]
print("VEHICLE REGISTRATION VALIDATOR")
print("--------------------------------")
for raw in vehicles:
    reg = normalise(raw)
    if is_valid(reg):
        print(raw, "->", reg, "->", format_number(reg), "VALID")
    else:
        print(raw, "->", reg, "-> INVALID")