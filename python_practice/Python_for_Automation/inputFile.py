#open the inputFile with the intention of reading it
input_file = open("Ex_Files/inputFile.txt", "r")

# open passFile and FailFile to write all Pass and Fail entries
pass_file = open("Ex_Files/passFile.txt", "w")
fail_file = open("Ex_Files/failFile.txt", "w")

#loop through each line of inputFile and print first 5 values to passFile or failFile
pass_counter = 0
fail_counter = 0

for line in input_file:
    line_split = line.split()
    if line_split[2] == "P":
        if pass_counter < 5:
            pass_file.write(line)
            pass_counter += 1
    else:
        if fail_counter < 5:
            fail_file.write(line)
            fail_counter += 1
    if pass_counter >= 5 and fail_counter >= 5:
        break

#close inputFile, passFile, failFile
input_file.close()
pass_file.close()
fail_file.close()

"""
print_counter_2 = 0

with open("Ex_Files\\inputFile.txt", "r") as input_file_2:
    while print_counter_2 >= 5:
        line_2 = input_file_2.readline()
        if not line_2:
            break

        line_split_2 = line_2.split()
        if int(line_split_2[2]) > 30:
            print (line_2)
            print_counter_2 += 1
"""