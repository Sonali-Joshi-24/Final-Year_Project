import re
import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
from sodapy import Socrata


client = Socrata("data.cityofnewyork.us", "3FziUOGS1PyhMLZdvPvlPlUfO")


results = client.get("5uac-w243", limit=449506)

results_df = pd.DataFrame.from_records(results)
results_df=results_df.drop(['crm_atpt_cptd_cd','juris_desc','ky_cd','rpt_dt','x_coord_cd','y_coord_cd',':@computed_region_efsh_h5xi',':@computed_region_f5dn_yrer',':@computed_region_yeji_bk3q',':@computed_region_92fq_4b7q',':@computed_region_sbqj_enih','patrol_boro','pd_desc','cmplnt_to_dt','cmplnt_to_tm','cmplnt_num','jurisdiction_code','parks_nm','housing_psa','station_name','transit_district','hadevelopt','geocoded_column'], axis = 1)
results_df.to_csv(r'raw02.csv', header=True, index=False)



###PREDICTION###
def convertClassToNum(p_df):
  p_df['datetime']=pd.to_datetime(p_df['cmplnt_fr_dt'] + ' ' + p_df['cmplnt_fr_tm'],errors='coerce')
  p_df=p_df.drop(columns=['cmplnt_fr_dt','cmplnt_fr_tm'])
  p_df=p_df.sort_values(by='datetime',ascending=True) 

  p_df['year']=pd.DatetimeIndex(p_df['datetime']).year
  p_df['month'] = pd.DatetimeIndex(p_df['datetime']).month
  p_df['weekday'] = p_df['datetime'].dt.dayofweek
  p_df['Hour'] = p_df.datetime.dt.hour
  p_df['Minute'] = p_df.datetime.dt.minute
  p_df=p_df.drop(columns=['datetime'])

  list_law_cat_cd=list(p_df['law_cat_cd'].unique())
  global dict_law_cat_cd
  dict_law_cat_cd = {}
  for i in list_law_cat_cd:
    dict_law_cat_cd[i] = list_law_cat_cd.index(i)
  p_df['law_cat_cd']=p_df['law_cat_cd'].map(dict_law_cat_cd)
#     print(dict_law_cat_cd)

  list_ofns_desc=list(p_df['ofns_desc'].unique())
  global dict_ofns_desc
  dict_ofns_desc = {}
  for i in list_ofns_desc:
    dict_ofns_desc[i] = list_ofns_desc.index(i)
  p_df['ofns_desc']=p_df['ofns_desc'].map(dict_ofns_desc)
#     print(dict_ofns_desc)

  p_df=p_df[p_df['year'].notna()]
  p_df=p_df.fillna("OTHERS")
  global dict_boro_nm
  dict_boro_nm = {'OTHERS':0,'BROOKLYN':1,'QUEENS':2,'BRONX':3,'MANHATTAN':4,'STATEN ISLAND':5}
  p_df['boro_nm']=p_df['boro_nm'].map(dict_boro_nm)
#     print(dict_boro_nm)

  return p_df

def prediction(results_df):
  p_df=results_df[['cmplnt_fr_dt','cmplnt_fr_tm','law_cat_cd','ofns_desc','latitude','longitude','boro_nm']]
  p_df = convertClassToNum(p_df)
  ######## Rearrange Columns #######
  cols = p_df.columns.tolist()
  cols = cols[2:10] + cols[0:2]
  p_df = p_df[cols]
  p_df=p_df.fillna("UNKNOWN")
  Train = p_df.head(359598)
  Test = p_df.tail(89900)
  Train.to_csv(r'converted_traindata1.csv')
  Test.to_csv(r'converted_testdata1.csv')




###ANALYSIS###


def analaysis(results_df):

  a_df=results_df.fillna("UNKNOWN")
  a_df['datetime']=pd.to_datetime(a_df['cmplnt_fr_dt'] + ' ' + a_df['cmplnt_fr_tm'],errors='coerce')
  a_df=a_df.drop(columns=['cmplnt_fr_dt','cmplnt_fr_tm'])
  a_df=a_df.sort_values(by='datetime',ascending=True) 

  a_df['year']=pd.DatetimeIndex(a_df['datetime']).year
  a_df['month'] = a_df['datetime'].dt.month_name()
  a_df['weekday'] = a_df['datetime'].dt.day_name()
  a_df['hour'] = a_df.datetime.dt.hour
  a_df['dayparting'] = "Night"
  a_df.loc[ (a_df['hour'] > 4) & (a_df['hour'] < 12), 'dayparting' ] = "Morning"
  a_df.loc[ (a_df['hour'] >= 12) & (a_df['hour'] < 16), 'dayparting' ] = "Afternoon"
  a_df.loc[ (a_df['hour'] >= 16) & (a_df['hour'] < 20), 'dayparting' ] = "Evening"
  
  a_df=a_df[a_df['year'].notna()]
  
  a_df.to_csv(r'analysis_data.csv', header=True, index=False)
 
  # a_df1 = a_df.iloc[:224506,:]
  # a_df2 = a_df.iloc[224506:,:]
  # a_df1.to_csv(r'analysis_data1.csv', header=True, index=False)
  # a_df2.to_csv(r'analysis_data2.csv', header=True, index=False)
  


analaysis(results_df)
prediction(results_df)