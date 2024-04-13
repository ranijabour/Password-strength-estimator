import os
import ESrank

"""
 Retrieve L1 and L2 values from the country's data using the algorithm specified in the ESrank module.
 """


def to_num(file_name):
    float_numbers = []
    with open(file_name, 'r') as file:
        for line in file:
            # Split the line into sub-password and distribution parts, and then select the last part.
            number_str = line.split()[-1]
            float_numbers.append(float(number_str))
    result = sorted(float_numbers, reverse=True)
    return result


def main(country):
    P_main = []

    # Iterate through dimensions from 1 to 5 (1, d+1)
    for dim in range(1, 6):
        # Generate the file path based on the country and dimension
        file_name = os.path.join(os.getcwd(), f"{country}_{dim}.txt")

        # Extract and append sorted data from the file to the list
        sorted_data = to_num(file_name)
        P_main.append(sorted_data)

    # Call the ESrank module's main1 function with the sorted data and parameters
    L1, L2 = ESrank.main1(P_main, 5, 1.09, 14)


    return L1, L2
