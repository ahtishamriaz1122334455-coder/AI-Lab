#AI LAB class task 1 
print("Simple Dynamic Calculator")
print("Write any math question like: 2+3*4 or (5+6)/2")
print("Type exit to close")

while True:
    user_input = input("\nEnter your question: ")

    if user_input == "exit":
        print("Calculator closed")
        break

    try:
        result = eval(user_input)
        print("Answer =", result)
    except:
        print("Wrong input! Try again.")
