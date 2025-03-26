"""Problem 1: Interleaving Two Numbers
Description: Given two integers A and 𝐵, interleave their digits alternately.
If one number has more digits, append the remaining digits at the end.
If the resulting number exceeds 100,000,000, return -1.
Solution (already provided by you, slightly optimized):
"""
# my code
# you can write to stdout for debugging purposes, e.g.
# print("this is a debug message")
from measure_latency import measure_latency

#w@measure_latency
def my_solution(A, B):
    # Implement your solution here
    string_A, string_B = str(A), str(B)
    array_C = []

    if len(string_A) < len(string_B):
        loop_count = len(string_A)
        string_to_append = string_B
    else:
        loop_count = len(string_B)
        string_to_append = string_A

    for i in range(loop_count):
        array_C.append(string_A[i])
        array_C.append(string_B[i])

    array_C.extend(string_to_append[loop_count:])

    C = int("".join(array_C))

    C = C if C < 100000000 else -1 #condition if C exceeds 100000000

    return C

A, B = 456, 12624
print (f"The Output is : {my_solution(A,B)}")