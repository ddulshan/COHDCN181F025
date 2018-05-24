priceList = []
total = 0
discountValue = 0

while True:
        try:
                price = input("Enter item price : ")
                if not price:
                        if not total:
                                print("No values entered, exitting...")
                                quit()
                        break
                priceList.append(float(price))
                total += float(price)
        except ValueError:
                print("Invalid input")

if total > 5000:
        discountValue = 12
elif total >= 3000:
        discountValue = 10
elif total >= 1000:
        discountValue = 5

discountAmount = float(total * (discountValue/100.00))
netTotal = total - discountAmount
print("Total : Rs.", total, "\nDiscount : Rs. ", discountAmount, "\nNet total : Rs.", netTotal)

while True:
        try:
                file = open("bill.txt", "a")

        except IOError:
                print("Error creating/opening file")
                option = input("Enter any value to retry, Enter to exit without saving to file : ")
                if not option:
                        print("Error saving to file, exiting...")
                        quit()
                else:
                        continue
        break

for x in range (0, len(priceList)):
        if x == len(priceList)-1:
                file.write(str(priceList[x]) + "\n\n")
        else:
                file.write(str(priceList[x]) + "\n")
file.close()
        
