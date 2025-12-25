import csv


# with open('Giants.csv', mode ='w')as file:
#   csvFile = csv.reader(file, delimiter=";")
#   for lines in csvFile:
#         print(lines)




import csv
from io import StringIO

# data = "name\nEmil\nTobias"
# r = csv.reader(StringIO(data))

# for row in r:
with open('csv_s/turnModel.csv','a', newline='') as fd:
    writer = csv.writer(fd, delimiter=";")
    writer.writerow(["probability_1_1", "potheight", "average_pot_2", "average_pot_3", "average_pot_5", "average_pot_7", "average_pot_9", "average_pot_11", "average_pot_13", "average_pot_16", "average_pot_20", "average_pot_30", "average_pot_50", "to_call", "hand_score", "output"]) 
  


