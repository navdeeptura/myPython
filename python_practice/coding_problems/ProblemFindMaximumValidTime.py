"""
Problem 2: Find the Maximum Valid Time
Description: Given four digits, form the maximum valid 24-hour time (HH:MM).
If no valid time can be formed, return "NOT POSSIBLE".
Solution:
"""
from itertools import permutations

def max_time(A):
    max_time_str = ""

    # Generate all permutations of the four digits
    for perm in permutations(A):
        h1, h2, m1, m2 = perm
        hours = h1 * 10 + h2
        minutes = m1 * 10 + m2

        # Check if it's a valid time
        if 0 <= hours < 24 and 0 <= minutes < 60:
            time_str = f"{hours:02}:{minutes:02}"
            max_time_str = max(max_time_str, time_str)  # Keep the max valid time

    return max_time_str if max_time_str else "NOT POSSIBLE"

# Example Usage:
print(max_time([1, 9, 2, 3]))  # Output: "23:19"
#print(max_time([5, 5, 5, 5]))  # Output: "NOT POSSIBLE"