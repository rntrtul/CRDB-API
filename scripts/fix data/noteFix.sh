#!/bin/bash
for f in *-CR.csv; do 
  python3 fixNotes.py "$f";
  newName="LF$f"
  rm "$f";
  mv -- "$newName" "${newName//LF/}" 2>/dev/null;
done