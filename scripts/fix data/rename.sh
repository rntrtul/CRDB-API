#!/bin/bash
for f in *.csv; do 
  updated="${f//C1/C1-}";
  updated="${updated//SC/-SC}";
  mv -- "$f" "$updated" 2>/dev/null;
done

#for f in {1..99}; do 
# mv -- "$f" `printf C2-E%03d-DT.csv ${f#.csv}`;
#done