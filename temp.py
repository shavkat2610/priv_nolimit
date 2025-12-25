import time
# from scripts.shavkats_functions import click_ok

# time.sleep(3)


holders = [ False, False, True, False, True, False, True, False]
def count_holders(holders = [ False, False, False, False, False, False, False, False]):
    i = 0
    for holder in holders:
        if holder == True:
            i += 1
    return i

print(count_holders())