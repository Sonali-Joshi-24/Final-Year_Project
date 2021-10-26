import re
import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
from sodapy import Socrata


client = Socrata("data.cityofnewyork.us", "3FziUOGS1PyhMLZdvPvlPlUfO")




results = client.get("5uac-w243", limit=204646)

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)
results_df=results_df.drop(['cmplnt_num','jurisdiction_code','parks_nm','housing_psa','station_name','transit_district','hadevelopt','geocoded_column'], axis = 1)
#pd.set_option("display.max_rows", None, "display.max_columns", None)
#print(results_df)
#for col in results_df.columns:
#    print(col)
#results_df.to_csv(r'E:\.py\crime\export_dataframen.csv', header=False, index=False)

###PREDICTION###
#'''
def prediction(results_df):
  p_df=results_df[['cmplnt_fr_dt','cmplnt_fr_tm','law_cat_cd','ofns_desc','latitude','longitude','boro_nm']]
  #p_df['cmplnt_fr_dt']=p_df['cmplnt_fr_dt'].apply(lambda x: pd.datetime.strptime(x, '%Y-%m-%dT%I:%M:%S') if type(x)==str else np.NaN)
  p_df['datetime']=pd.to_datetime(p_df['cmplnt_fr_dt'] + ' ' + p_df['cmplnt_fr_tm'],errors='coerce')
  p_df=p_df.drop(columns=['cmplnt_fr_dt','cmplnt_fr_tm'])
  p_df=p_df.sort_values(by='datetime',ascending=True) 

  #p_df=p_df.dropna(axis=0)
  #print(a_df.sample(5))
  '''
  '''
  #p_df['cmplnt_fr_dt'] = pd.to_datetime(p_df['cmplnt_fr_dt'])
  #p_df['cmplnt_fr_tm'] = pd.to_datetime(p_df['cmplnt_fr_tm'])

  p_df['year']=pd.DatetimeIndex(p_df['datetime']).year
  p_df['month'] = pd.DatetimeIndex(p_df['datetime']).month
  p_df['weekday'] = p_df['datetime'].dt.dayofweek

  #print(p_df["ofns_desc"].unique())

  #p_df['IsDay'] = 0
  #p_df.loc[ (p_df.datetime.dt.hour > 6) & (p_df.datetime.dt.hour < 18), 'IsDay' ] = 1
  p_df['Hour'] = p_df.datetime.dt.hour
  p_df['Minute'] = p_df.datetime.dt.minute
  p_df=p_df.drop(columns=['datetime'])
  global dict_law_cat_cd
  list_law_cat_cd=list(p_df['law_cat_cd'].unique())
  dict_law_cat_cd = {}
  for i in list_law_cat_cd:
    dict_law_cat_cd[i] = list_law_cat_cd.index(i)
  p_df['law_cat_cd']=p_df['law_cat_cd'].map(dict_law_cat_cd)

  od=list(p_df['ofns_desc'].unique())
  #fs=[i for i in range(47)]
  #dod={zip(od,range(47))}
  dict1 = {}
  for i in od:
    dict1[i] = od.index(i)
  p_df['ofns_desc']=p_df['ofns_desc'].map(dict1)

  p_df=p_df[p_df['year'].notna()]
  p_df=p_df.fillna("UNKNOWN")
  global dict_boro_nm
  dict_boro_nm = {'OTHERS':0,'BROOKLYN':1,'QUEENS':2,'BRONX':3,'MANHATTAN':4,'STATEN ISLAND':5}
  p_df['boro_nm']=p_df['boro_nm'].map(dict_boro_nm)
  p_df.to_csv(r'E:\.py\crime\p.csv', header=True, index=False)



###ANALYSIS###

#'''
def analysis(results_df):
  #a_df=results_df.dropna(axis=0)
  results_df=results_df[results_df['cmplnt_fr_dt'].notna()]
  a_df=results_df.fillna("UNKNOWN")
  a_df['datetime']=pd.to_datetime(a_df['cmplnt_fr_dt'] + ' ' + a_df['cmplnt_fr_tm'],errors='coerce')
  a_df=a_df.drop(columns=['cmplnt_fr_dt','cmplnt_fr_tm'])
  a_df=a_df.sort_values(by='datetime',ascending=True) 
  #a_df=results_df.replace(r'^\s*$', np.nan, regex=True)
  #'''

  a_df['year']=pd.DatetimeIndex(a_df['datetime']).year
  a_df['month'] = a_df['datetime'].dt.month_name()
  a_df['weekday'] = a_df['datetime'].dt.day_name()
  a_df['hour'] = a_df.datetime.dt.hour
  a_df['dayparting'] = "Night"
  a_df.loc[ (a_df['hour'] > 4) & (a_df['hour'] < 12), 'dayparting' ] = "Morning"
  a_df.loc[ (a_df['hour'] >= 12) & (a_df['hour'] < 16), 'dayparting' ] = "Afternoon"
  a_df.loc[ (a_df['hour'] >= 16) & (a_df['hour'] < 20), 'dayparting' ] = "Evening"
  
  a_df=a_df[a_df['year'].notna()]
  #'''
  #print(a_df.head())
  #b_df=a_df.sample(5)
  #b_df.to_csv(r'E:\.py\crime\export_dataframena5.csv', header=True, index=False)
  a_df.to_csv(r'E:\.py\crime\a.csv', header=True, index=False)

analysis(results_df)
prediction(results_df)