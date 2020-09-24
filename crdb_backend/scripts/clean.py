from characters.models import StatSheet 

def weaponsClean(sheets):
  import re
  count = 0 

  for sheet in sheets:

    #if '0 0 0' in sheet.weapons:
      #count+= 1
      zero_less_wpn = re.sub('0 0 0', '', sheet.weapons)
      unique_wpns = set(map(lambda wpn: wpn.strip(), zero_less_wpn.split('\n')))
      unique_wpns.discard(' ')
      unique_wpns.discard('')
      cleaned_wpn = "\n".join(unique_wpns)

      #sheet.weapons = cleaned_wpn
      #sheet.save()
      print('Original:' ,sheet.weapons)
      print("Updated to:" , cleaned_wpn)
  print("Updated", count, "stat sheets weapons")

def ftClean(sheets):
  import re
  count = 0

  for sheet in sheets:
    
    #if '\\n' in sheet.features_traits:
      #clean = ""
      #clean = re.sub("\\n", '\n', sheet.features_traits)
      #count +=1
      #sheet.features_traits = clean

    if re.findall(r',(?:,+|\s\s+-)', sheet.features_traits) :
      count += 1
      clean = ""
      stripped = sheet.features_traits.strip()
      prev = 0

      for match in re.finditer(r',(?:,+|\s\s+-)', stripped):
        clean += stripped[prev:match.span()[0]] + '\n'
        prev = match.span()[1]
        if match.group().endswith('-'):
          prev -= 1
        
      print("ORIGINAL:")
      print(stripped)
      print ("CLEANED:")
      print(clean)

      sheet.features_traits = clean
      sheet.save()

  print("Cleaned %d feats and traits" % (count))


sheets = StatSheet.objects.all()
weaponsClean(sheets)
#ftClean(sheets)
