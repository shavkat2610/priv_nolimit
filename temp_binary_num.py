


# trays_score = 2

# n = 2048 / trays_score

# bin_string = ""

# curr = 1024

# for i in range(13):
#     if n>=curr:
#         bin_string += "1"
#         n -= curr
#     else:
#         bin_string += "0"
#     curr /= 2

# print(bin_string)

def bin_score(trays_score = 2):
    
    n = 2048 / trays_score

    bin_string = ""

    curr = 1024

    for i in range(13):
        if n>=curr:
            bin_string += "1"
            n -= curr
        else:
            bin_string += "0"
        curr /= 2

    print(bin_string)

    return bin_string

bin_score(2)