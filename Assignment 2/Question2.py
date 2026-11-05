# OTP Verification using while loop

correct_otp = "123456"
attempts = 0

while attempts < 3:
    otp = input("Enter OTP: ")

    if otp == "":
        print("Blank entry! Please enter OTP again.")
        continue

    if otp == correct_otp:
        print("OTP verified successfully!")
        break

    attempts += 1
    print("Wrong OTP! Attempts left:", 3 - attempts)

else:
    print("Account locked for 30 minutes.")