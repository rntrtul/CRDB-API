from episodes.models import Episode, VodLinks, VodType
from campaigns.models import Campaign
import json


C1VOD = "/home/lightbulb/CritRoleDB/zdata/C1/ytvods.json"
C2VOD = "/home/lightbulb/CritRoleDB/zdata/C2/vodlinks.json"

with open(C2VOD) as f:
  data = json.load(f)


count = 0
yt = VodType.objects.get(name="YouTube")
c1 = Campaign.objects.get(num=2)
for things in data['entries']:
  idx = things['title'].find("Episode")
  num = things['title'][idx+8:]
  
  if num.find('-') != -1:
    num = num.split(' ')[0]
  elif num.find('w/') != -1:
    num = num.split(' ')[0]
  elif num.find('p') != -1:
    num = num.split(',')[0]
  
  try:
    ep = Episode.objects.get(num=num, campaign=c1)
    vl = VodLinks.objects.get_or_create(episode = ep, vod_type=yt,link_key=things['id'])
    if vl[1]:
      print("CREATED: ", ep.title, 'link:', 'https://www.youtube.com/watch?v=' + things['id'] )
      count+= 1
  except:
    print("NOT FOUND", things['title'])

print(count)