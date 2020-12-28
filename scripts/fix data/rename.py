import os
import re
import sys

FILETYPE = sys.argv[1]
CAMAPAIGN = "C2"
EXTENTION = ".csv"
SPLITTER = "-"

for dirpath, dirnmaes, files in os.walk('.'):
    files.sort()
    for file_name in files:
        if file_name.endswith('.csv'):
            extenlessName = file_name[:-4]
            epNum = re.search(r'\d+$', extenlessName)
            epNum = epNum.group().zfill(3)
            newName = CAMAPAIGN + SPLITTER + "E" + epNum + SPLITTER + FILETYPE + EXTENTION
            os.rename(file_name, newName)
            print(file_name + " will become: " + newName)
