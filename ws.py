import requests
import json
import pandas
url = "https://ukpolicedata.p.rapidapi.com/crimes-street/all-crime"



headers = {
    'x-rapidapi-key': "API",
    'x-rapidapi-host': "ukpolicedata.p.rapidapi.com"
    }

dates=["2020-10","2020-11","2020-12","2021-01","2021-02","2021-03","2021-04"]
frames=[]

for i in dates:
    querystring = {"date":i,"lat":"52.192001","lng":"-2.220000"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    jon = response.text
    jsn=json.loads(jon)
    frame=pandas.json_normalize(jsn)
    frames.append(frame)

jn = pandas.concat(frames)

#pandas.set_option("display.max_rows", None, "display.max_columns", None)
print(jn)
jn.drop(jn.columns[[1, 2, 3, 4, 5, 12]], axis = 1, inplace = True)
jn.rename(columns = {"location.latitude":"latitude", "location.street.id":"street_id", "location.street.name":"street_name", "location.longitude":"longitude",  "outcome_status.category":"outcome_status"
}, inplace = True)

print(jn)
#jn.to_excel (r'D:\proj\export_dataframen.xlsx', index = False, header=True)
#jn.to_csv(r'D:\proj\export_dataframen.csv', header=False, index=False)
