import csv
import sys

name = sys.argv[1]
newName = "LF" + name

with open(name, newline='') as myFile:
  reader = csv.reader(myFile)
  writer = csv.writer (open (newName, 'w'))

  header = next(reader)
  writer.writerow(header)
  for row in reader:
    newRow=[]

    for idx, col in enumerate(row):
      if idx == 9 or idx == 7 and '\n' in col:
        cleanedNote = col.replace("\n", "")
        newRow.append(cleanedNote)
      else:
        newRow.append(col)
    writer.writerow(newRow)
