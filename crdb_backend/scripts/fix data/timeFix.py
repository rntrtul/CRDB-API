import sys
import csv
import re
from datetime import datetime
from time import strptime

date = re.compile(r"^...\s...\s\d{2}\s\d{4}")
stdTime = datetime(year = 1899, month = 12, day = 30, hour = 0)
name = sys.argv[1]
newName = "TF" + name

with open(name, newline='') as myFile:
  reader = csv.reader(myFile)
  writer = csv.writer (open (newName, 'w'))
  for row in reader:
    newRow = []
    for col in row:
      if date.match(col):
        currTime= datetime(year = int(col[10:15]), month = strptime(col[4:7],'%b').tm_mon,day = int(col[8:10]),
                           hour = int(col[16:18]), minute = int(col[19:21]), second=int(col[22:24]))

        diff = currTime - stdTime
        newRow.append(diff.total_seconds())
        #newRow.append(currTime.strftime("%Y/%m/%d"))
      else:
        newRow.append(col)
    writer.writerow(newRow)