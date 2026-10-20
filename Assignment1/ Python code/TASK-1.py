farmers = []
n = int(input("Enter number of farmers: "))
for i in range(n):
    print("\nFarmer", i + 1)
    farmer_id = input("Enter Farmer ID: ")
    litres = float(input("Enter litres: "))
    fat = float(input("Enter fat percentage: "))
    snf = float(input("Enter SNF percentage: "))

    farmers.append((farmer_id, litres, fat, snf))

print("\nFarmer Records:")
for farmer in farmers:
    print(farmer)