try:
    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))
    sum = num1 + num2
    print(sum)
except ValueError:
    print("Invalid input. Please enter numbers only.")