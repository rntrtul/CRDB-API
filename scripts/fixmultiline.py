import csv
import sys

def appendAsCols(row, appendTo):
  for col in row:
    appendTo.append(col)
  
  return appendTo

name = sys.argv[1]
newName = "LF" + name
print(name)
with open(name, newline='') as myFile:
  reader = csv.reader(myFile)
  writer = csv.writer (open (newName, 'w'))

  
  prevLine = next(reader)
  for row in reader:
    currHasTime = True
    if not row:
      continue

    if len(row) == 1:
      prevLine[9] += ''.join(row)
      print(prevLine[9] + ''.join(row))
    elif not row[1].endswith('.0'):
      try:
        prevLine[9] += ''.join(row)
        print(prevLine[9] + ''.join(row))
      except:
        prevLine[7] += ''.join(row)
        print(prevLine[7] + ''.join(row))
      
      currHasTime = False
    elif len(row) < 9 and not currHasTime:
      prevLine[9] += ''.join(row)
      print(prevLine[9] + ''.join(row))
    else:
        writer.writerow(prevLine)
        prevLine = row
  
  writer.writerow(prevLine)
