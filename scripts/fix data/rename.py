import csv
import os


FILETYPE = "CR"
CAMAPAIGN = "C1"
EXTENTION = ".csv"
SPLITTER = "-"

for dirpath,dirnmaes,files in os.walk('.'):
  files.sort()
  for file_name in files:
    if file_name.endswith('.csv') and file_name.startswith('Episode '):
      extenlessName = file_name[:-4]
      epNum= extenlessName[8:].zfill(3)
      newName = CAMAPAIGN + SPLITTER + "E"+ epNum + SPLITTER + FILETYPE + EXTENTION
      os.rename(file_name, newName)
      print(file_name + " will become: " + newName)
