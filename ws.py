import requests
import json
import pandas
url = "https://ukpolicedata.p.rapidapi.com/crimes-street/all-crime"

querystring = {"lat":"52.192001","lng":"-2.220000"}

headers = {
    'x-rapidapi-key': "6220239fd6msh64cd8258f025bacp1d5d3djsn5dd21e702f98",
    'x-rapidapi-host': "ukpolicedata.p.rapidapi.com"
    }

response = requests.request("GET", url, headers=headers, params=querystring)
#print(response.text)
jon = response.text
jsn=json.loads(jon)
jn=pandas.json_normalize(jsn)
print(jn)
#pandas.set_option("display.max_rows", None, "display.max_columns", None)
#jn.to_excel (r'D:\proj\export_dataframe.xlsx', index = False, header=True)