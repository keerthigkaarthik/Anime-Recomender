import csv
import re
file = open("anime_names.csv")
csvreader = csv.reader(file)
header = next(csvreader)
print(header)
rows = []
for row in csvreader:
    new_row = re.sub('_',' ', row[1])
    rows.append(new_row)
file.close()
for i in rows:
    print (i)