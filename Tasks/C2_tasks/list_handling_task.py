"""
    Solution for tasks in course 2 GAD - week 2
"""

# Declaration of list
starting_list = [7, 8, 9, 2, 3, 1, 4, 10, 5, 6]
print(f"Input list: {starting_list}")

# Sorting list in ascending order
ascending_list = sorted(starting_list)
print(f"List sorted in ascending order: {ascending_list}")

# Sorting list in descending order
descending_list = sorted(starting_list, reverse=True)
print(f"List sorted in descending order: {descending_list}")

# List of all numbers with even indexes
even_indexes_list = starting_list[::2]
print(f"List of elements with even indexes: {even_indexes_list}")

# List of all numbers with odd indexes
odd_indexes_list = starting_list[1::2]
print(f"List of elements with odd indexes: {odd_indexes_list}")

# List with all multiples of 3 from input list
multiples_of_three_list = [element for element in starting_list if element % 3 == 0]
print(f"List of multiples of three: {multiples_of_three_list}")
