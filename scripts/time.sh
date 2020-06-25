#!/bin/bash
for f in *.csv; do 
  python3 timeFix.py "$f";
  newName="TF$f"
  rm "$f";
  mv -- "$newName" "${newName//TF/}" 2>/dev/null;
done