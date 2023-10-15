# import necessary libraries
import numpy as np
import pandas as pd

# Class to implement the algorithm to solve unit commitment for a single demand
class UnitCommitment:

    def __init__(self, demand, no_of_units, capacity, rate):
        try:
            self.demand = demand
            self.no_of_units = no_of_units
            self.capacity = capacity
            self.rate = rate
            self.cost = rate * capacity

            # Initialize a 2D DP table with zeros
            self.dp = []
            for i in range(no_of_units + 1):
                row = []
                for w in range(demand + 1):
                    row.append(0)
                self.dp.append(row)
        except Exception as e:
            print("An error occurred during initialization:", str(e))

    def solution(self):
        try:
            # Dynamic programming to solve the unit commitment problem
            for i in range(self.no_of_units + 1):
                for w in range(self.demand + 1):
                    if i == 0 or w == 0:
                        # Base case: no units or no demand
                        self.dp[i][w] = 0
                    elif self.capacity[i - 1] <= w:
                        # If the capacity of the current unit is less than or equal to the demand
                        self.dp[i][w] = max(
                            self.cost[i - 1] + self.dp[i - 1][w - self.capacity[i - 1]],
                            self.dp[i - 1][w]
                        )
                    else:
                        # If the capacity of the current unit is greater than the demand
                        self.dp[i][w] = self.dp[i - 1][w]
        except Exception as e:
            print("An error occurred during the solution phase:", str(e))

    def get_max_gen(self):
        try:
            # Return the maximum generation value found in the DP table
            return self.dp[self.no_of_units][self.demand]
        except Exception as e:
            print("An error occurred while getting the maximum generation:", str(e))

    def get_selected_items(self):
        try:
            # Find and return the selected generating units to meet the demand
            items = []
            i, w = self.no_of_units, self.demand

            while i > 0 and w > 0:
                if self.dp[i][w] != self.dp[i - 1][w]:
                    items.append(i - 1)
                    w -= self.capacity[i - 1]
                i -= 1

            return items
        except Exception as e:
            print("An error occurred while getting the selected items:", str(e))



class UnitCommitment24:
    
    def __init__(self, load_demand, no_of_units, capacity, rate):
        try:
            self.load_demand = load_demand
            self.no_of_units = no_of_units
            self.capacity = np.array(capacity)
            self.rate = np.array(rate)
        except Exception as e:
            print("An error occurred during initialization:", str(e))

    def solve(self):
        try:
            # Initialize variables
            total_cost = 0
            allocation = {}

            # Iterate through each hour's load demand
            for i in range(len(self.load_demand)):
                try:
                    # Create an instance of the UnitCommitment class for the current demand scenario
                    solution_solver = UnitCommitment(self.load_demand[i], self.no_of_units, self.capacity, self.rate)
                    solution_solver.solution()  # Solve the unit commitment problem
                    total_cost += solution_solver.get_max_gen()  # Accumulate the total cost
                    allocation[i] = solution_solver.get_selected_items()  # Store selected units
                except Exception as e:
                    print(f"An error occurred during hour {i}:", str(e))

            # Print the total cost of operation for 24 hours
            print("Total Cost of Operation for 24 hours is:", total_cost)

            # Create a DataFrame to represent the allocation of units for each hour
            allocation_df = pd.DataFrame({'Units': allocation})
            allocation_df.index.name = 'Hours'  # Set the index name

            print(allocation_df)  # Print the allocation DataFrame
        except Exception as e:
            print("An error occurred during the solution phase:", str(e))

"""
n= 4
rate = [10,10,10,10]
capacity = [70,55,60,90]
load_demand = [100, 120, 150, 170, 200, 230, 250, 270, 280, 290, 300, 310, 320, 330, 320, 310, 300, 280, 260, 240, 220, 200, 180, 150]
a = UnitCommitment24(load_demand,n, capacity, rate)
b = a.solve() """

try:
    n = int(input("Enter the total number of Generation Unit: "))
    rate = []
    capacity = []

    for i in range(n):
        r = int(input(f"Enter the Generating Capacity of Unit {i+1}: "))
        c = int(input(f"Enter the Rate of Generating single unit of Unit {i+1}: "))
        rate.append(r)
        capacity.append(c)

    load_demand = list(map(int, input("Enter load for 24 hours (comma-separated): ").split(",")))

except ValueError:
    print("An error occurred during input:")


# instances for unitCommitment24

instance1 = UnitCommitment24(load_demand,n, capacity, rate)
result = instance1.solve()   