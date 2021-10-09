#!/usr/bin/env python
# coding: utf-8

# In[1]:


import folium


# In[26]:


m = folium.Map(location = [40.668583957,-73.9269799319999])


# In[31]:


folium.Circle(location = [40.668583957,-73.9269799319999],radius = 1000, color = 'red', fill = True, popup = "Brooklyn {}".format("motor crime")).add_to(m)


# In[32]:


m


# ## The complete analysis

# In[1]:


import numpy as np
import pandas as pd


# In[2]:


data = pd.read_csv("crime_analysis.csv")
data


# In[3]:


# # function to sort data set according to input
# # def filter_data(data, user_input = None):
# filtered_data = data[data['boro_nm'].str.contains('BROOKLYN')]
# filtered_data
# # user_input = input("Enter boron name: ")
# # print(user_input)
# # x = filtered_data(data, user_input)
# # x


# In[ ]:





# In[4]:


def filter_data(data, user_input = None):
    if user_input == None:
        return data
    else:
        filtered_data = data[data['boro_nm'].str.contains(user_input)]
        return filtered_data
        print(user_input)
user_input = input("Enter boron name: ")
print(user_input)
x = filter_data(data, user_input)
x
    


# In[ ]:





# In[5]:


import plotly.express as px
fig = px.histogram(x, x='month', color='dayparting', width=800, height=600, 
                   title="Crime Frequency")
fig.show()


# In[6]:


fig = px.pie(x, names='susp_race', title='Criminal analysis on race', hole=.3)
fig.show()


# In[7]:


'''
Plotly Pie chart for day which crime occur
'''

fig = px.pie(x, names='weekday', title='Crime Count on each day', hole=.3)
fig.show()


# In[8]:


data_x = x
fig = px.bar(data_x, x='ofns_desc', y='weekday',
             hover_data=['ofns_desc', 'hour','loc_of_occur_desc'],color = 'weekday',
             labels={'hour':'Time series'}, height=400)
fig.show()




# In[9]:


fig = px.bar(x, x="susp_sex", y="dayparting", color='dayparting')
fig.show()


# In[ ]:





# In[ ]:





# In[10]:


# fuction to determine specific crime entries
def determine_entries(x, user_input= None):
    if user_input == None:
        return x
    else:
        filter_data =  x[x.ofns_desc.str.contains(user_input)]
        return f"The dataset registers {filter_data.shape[0]} entries for {user_input} in total"
data = x
user_input = input("Enter the Specific Crime:  ")
y = determine_entries(data, user_input)
y

        


# In[ ]:





# In[ ]:





# In[11]:


# Analyzing victims
fig = px.histogram(x, x = 'vic_sex',color = 'vic_sex',width = 800, height = 600, title ="Crime victims by gender")
fig.show()


# In[12]:


# removing percentage
vic_sex_per = x['vic_sex'].value_counts() / x['vic_sex'].shape[0] *100
print(vic_sex_per)


# In[13]:


fig = px.histogram(x, x = 'vic_age_group',color = 'vic_age_group',width = 800, height = 600, title ="Crime victims by age group")
fig.show()


# In[14]:


vic_age_per = x['vic_age_group'].value_counts().iloc[[0,1,2,4,5]] /x['vic_age_group'].shape[0] *100
print(vic_age_per)
print("the max age is: ")
print(max(vic_age_per))


# In[21]:


fig = px.box(x, x = 'susp_race', y = 'ofns_desc', color = 'susp_race', width = 2000, height = 900)
# fig.update_traces(quartilemethod ="exclusive")
fig.show()


# In[15]:


# determining level of offense
fig = px.pie(x, names='law_cat_cd', title='Determining level of offense', hole=.3, color_discrete_sequence=px.colors.sequential.RdBu)
fig.show()


# In[ ]:



          


# In[ ]:





# In[ ]:





# ## STARTING MAPS ANALYSIS

# In[16]:


import folium


# In[45]:


newyork = [40.712776 ,-74.005974]
m = folium.Map(newyork, zoom_start = 13)


# In[46]:


def circle_marker(x):
    folium.CircleMarker(location =[x[0],x[1]], radius=2,
                 popup = 'Crime description: {}'.format(x[3]),color = 'red', fill = True).add_to(m)


# In[50]:


x[['latitude','longitude','pd_cd','ofns_desc']].apply(lambda x:circle_marker(x), axis = 1)


# In[48]:


m


# In[69]:


newyork = [40.712776 ,-74.005974]
map = folium.Map(newyork, zoom_start = 5)
map


# In[72]:



m2=folium.Map(location=[40.712776 ,-74.005974])
folium.TileLayer('Stamen Terrain').add_to(m2)
folium.TileLayer('Stamen Toner').add_to(m2)
folium.TileLayer('Stamen Water Color').add_to(m2)
folium.TileLayer('cartodbpositron').add_to(m2)
folium.TileLayer('cartodbdark_matter').add_to(m2)
folium.LayerControl().add_to(m2)
m2


# In[ ]:




