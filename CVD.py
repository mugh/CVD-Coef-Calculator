# Author: Mughni Yumashar
# Contact: mughnimail@gmail.com
# Any non-commercial usage shall include credit to the author.
# Commercial usages are prohibited without consent from the author.

import numpy as np

def main():
    # Get the number of data points with error handling
    while True:
        try:
            n = int(input("Enter the number of calibration data points (do not include the resistance at 0°C, will be asked later): "))
            if n <= 0:
                raise ValueError("The number of data points must be a positive integer.")
            break
        except ValueError as e:
            print(f"Invalid input: {e}. Please enter a valid number.")

    # Initialize arrays for temperatures and resistances
    temperatures = np.zeros(n)
    resistances = np.zeros(n)
    
    # Input data from the user
    print(f"")
    print("Enter the temperatures and corresponding resistances:")
    print(f"")
    for i in range(n):
        while True:
            try:
                temp, res = input(f"Data point {i+1} (temperature resistance): ").split()
                temperatures[i] = float(temp)
                resistances[i] = float(res)
                break
            except ValueError:
                print("Invalid input. Please enter the temperature and resistance separated by a space. Decimal value separated using point (.)")

    # Manually input R0, the resistance at 0°C
    while True:
        try:
            R0 = float(input("Enter the resistance at 0°C (R0): "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid number for R0.")

    # Normalize the resistance values
    r = resistances / R0
    
    # Prepare the matrix of independent variables
    X = np.column_stack([
        np.ones(n),  # for the constant term
        temperatures,                # T
        temperatures**2,             # T^2
    ])
    
    # Check for temperatures below 0°C
    if np.any(temperatures < 0):
        # Add the cubic term only for temperatures below 0°C
        cubic_terms = (temperatures - 100) * temperatures**3
        cubic_terms[temperatures >= 0] = 0  # Set cubic term to 0 for T >= 0
        X = np.column_stack([X, cubic_terms])
    else:
        print("Warning: No temperatures below 0°C. Cubic term will be omitted.")

    try:
        # Perform the linear regression using the normal equation: (X^T X)^-1 X^T y
        coefficients = np.linalg.inv(X.T @ X) @ X.T @ r

        # Extract coefficients
        A = coefficients[1]  # Coefficient A
        B = coefficients[2]  # Coefficient B
        C = coefficients[3] if X.shape[1] > 3 else None  # Coefficient C if it exists

        # Print the coefficients
        print(f"")
        print(f"R0: {R0}")
        print(f"Coefficient A: {A}")
        print(f"Coefficient B: {B}")
        if C is not None:
            print(f"Coefficient C: {C}")

    except np.linalg.LinAlgError:
        print("Error: The matrix is singular and cannot be inverted. Please check your input data.")

    print(f"")
    print(f"Please copy or write the coefficient")
    print(f"")
    print(f"Author: Mughni Yumashar")
    print(f"Contact: mughnimail@gmail.com")
    print(f"Any non-commercial usage shall include credit to the author.")
    print(f"Commercial usages are prohibited without consent from the author.")

    # Pause the console window so it doesn't close immediately
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()