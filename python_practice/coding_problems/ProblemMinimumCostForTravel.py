"""
Problem 3: Minimum Cost for Travel
Description:
You are given a list of days when you need to travel.
You can purchase travel passes:
1-day pass costs 2
7-day pass costs 7
30-day pass costs 25
The goal is to find the minimum cost to cover all travel days.
"""


def min_cost_travel(days):
    cost_per_day = {1: 2, 7: 7}
    travel_days = set(days)  # Convert list to set for quick lookup
    max_day = max(days)  # Last travel day

    # DP array to store the minimum cost up to each day
    dp = [0] * (max_day + 1)
    len(dp)

    for day in range(1, max_day + 1):
        if day not in travel_days:
            dp[day] = dp[day - 1]  # If no travel, cost remains same
        else:
            # Compute the minimum cost considering all pass options
            dp[day] = min(
                dp[max(0, day - 1)] + cost_per_day[1],  # 1-day pass
                dp[max(0, day - 7)] + cost_per_day[7]  # 7-day pass
            )

    return dp[max_day]


# Example Usage
print(min_cost_travel([1, 4, 6, 7, 8, 20]))  # Expected Output: Minimum cost
print(min_cost_travel([1, 2, 3, 4, 5, 6, 7]))  # Expected: 7
print(min_cost_travel([1, 8, 15, 22]))  # Expected: 8
