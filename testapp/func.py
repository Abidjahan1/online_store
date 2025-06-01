

def my_func(n):
    return lambda b: n % b


multiplication = my_func(5)

print(multiplication(3))