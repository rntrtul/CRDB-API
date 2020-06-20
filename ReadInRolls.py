from rolls.models import Rolls, RollType
import sys
import csv
import re

#date = re.compile(r"^...\s...\s\d{2}\s\d{4}")
#stdTime = datetime(year = 1899, month = 12, day = 30, hour = 0)
#name = sys.argv[1]
name = "C1-E001-CR.csv"

Rolls.objects.all().delete()
with open(name, newline='') as myFile:
  reader = csv.reader(myFile)
  next(reader)
  for row in reader:
    timeStamp = int(float(row[1]))
    type, created = RollType.objects.get_or_create(name=row[3])
    totalVal = 0
    if row[4] == "Nat1":
       totalVal = 1
    elif row[4] == "Nat20": 
      totalVal = 20
    elif row[4] != "Unknown": 
      totalVal = int(row[4])

    natVal = 0
    if row[5] != "Unknown" and row[5] != '':
      natVal = int(row[5])

    notes= row[9]

    roll, created = Rolls.objects.get_or_create(timeStamp=timeStamp,rollType=type,finalValue=totalVal, naturalValue=natVal, notes=notes)
    if created == False:
      print("duplicate roll, did not add to DB")

#delete these after testing views and stuff
#as reading in rolls will create a new rolltype, episode, character name if not found 

