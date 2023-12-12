# Task 1 - Make a function that accepts any parameters and computes the
# sum of the int and float parameters.

def calculate_sum_of_params(*args, **kwargs):
    sum_of_undefined_params = sum(argument for argument in args if isinstance(argument, (int, float)))
    return sum_of_undefined_params


# Examples of function calls
first_sum = calculate_sum_of_params(1, 5, -3, "abc", [12, 56, "cad"])
print(f"First function call result: {first_sum}")

second_sum = calculate_sum_of_params()
print(f"Second function call result: {second_sum}")

third_sum = calculate_sum_of_params(2, 4, 'abc', param_1=2)
print(f"Second function call result: {third_sum}")


# Task 2 - Define a recursive function that takes an in list as input and returns
# the total of all entries, the sum of odd elements, and the sum of even elements.

def sum_of_list_elements(input_list):
    if not input_list:
        return 0, 0, 0

    total_sum, even_sum, odd_sum = sum_of_list_elements(input_list[1:])
    current_element = input_list[0]

    total_sum += current_element

    if current_element % 2 == 0:
        even_sum += current_element
    else:
        odd_sum += current_element

    return total_sum, even_sum, odd_sum


# Example of list
list_of_integers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
result_total_sum, result_even_sum, result_odd_sum = sum_of_list_elements(list_of_integers)

print(f"Total sum result: {result_total_sum}")
print(f"Even elements sum result: {result_even_sum}")
print(f"Odd elements sum result: {result_odd_sum}")


# Task3 - Define a function that receives user input and tests to see
# whether it is an int number, then displays it; otherwise, return 0.

def read_user_integer():
    try:
        submitted_value = int(input("Please provide an integer number: "))
        return submitted_value
    except ValueError:
        print("Sorry but this is not an integer value! The default value was set to 0.")
        return 0


# Example of call
submitted_user_value = read_user_integer()
print(f"The integer value entered is: {submitted_user_value}")
