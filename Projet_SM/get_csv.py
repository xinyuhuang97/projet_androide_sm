import json
import urllib
import requests

where = urllib.parse.quote_plus("""
{
    "Gender": "male"
}
""")
url = 'https://parseapi.back4app.com/classes/Complete_List_Names?limit=250000&order=Name&where=%s' % where
headers = {
    'X-Parse-Application-Id': 'zsSkPsDYTc2hmphLjjs9hz2Q3EXmnSxUyXnouj1I', # This is the fake app's application id
    'X-Parse-Master-Key': '4LuCXgPPXXO2sU5cXm6WwpwzaKyZpo3Wpj4G4xXK' # This is the fake app's readonly master key
}
data = json.loads(requests.get(url, headers=headers).content.decode('utf-8')) # Here you have the data that you need
#print(json.dumps(data, indent=2))
with open('name_male.json', 'w', encoding='utf-8') as f:
    json.dump(data['results'], f, ensure_ascii=False, indent=4)

"""
Other methode
text = json.loads(resp)
csvFile = open('output.csv','w')
csvwriter = csv.writer(csvFile, delimiter=',')
line = text["drivers"]
csvwriter.writerow(["id","groupId","vehicleId","currentVehicleId","username","name"])
for l in line:
    csvwriter.writerow([l["id"],l["groupId"],l["vehicleId"],l["currentVehicleId"],l["username"],l["name"]])
csvFile.close()
"""

import pandas as pd
df_m=pd.read_json(r'./name_male.json')
df_m.to_csv(r'./name_male.csv',index=None)

where = urllib.parse.quote_plus("""
{
    "Gender": "female"
}
""")
url = 'https://parseapi.back4app.com/classes/Complete_List_Names?limit=250000&order=Name&where=%s' % where
headers = {
    'X-Parse-Application-Id': 'zsSkPsDYTc2hmphLjjs9hz2Q3EXmnSxUyXnouj1I', # This is the fake app's application id
    'X-Parse-Master-Key': '4LuCXgPPXXO2sU5cXm6WwpwzaKyZpo3Wpj4G4xXK' # This is the fake app's readonly master key
}
data = json.loads(requests.get(url, headers=headers).content.decode('utf-8')) # Here you have the data that you need
#print(json.dumps(data, indent=2))
with open('name_female.json', 'w', encoding='utf-8') as f:
    json.dump(data['results'], f, ensure_ascii=False, indent=4)

df_m=pd.read_json(r'./name_female.json')
df_m.to_csv(r'./name_female.csv',index=None)
