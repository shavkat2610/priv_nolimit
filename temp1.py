from pokerkit import *
import time

# Load hand
with open("C:/Users/shavk/Desktop/phh-dataset-main/data/wsop/2023/43/5/00-02-07.phh", "rb") as file:
    hh = HandHistory.load(file)

# Iterate through each action step
for state in hh:
    print()
    print()
    print()
    print(state)
    print()
    print()
    print()
    time.sleep(10)  # Pause for 1 second between steps

print(hh)





