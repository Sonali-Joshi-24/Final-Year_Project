from logging import Filter
from re import T
from altair.vegalite.v4.schema.channels import Color, Tooltip
from matplotlib.pyplot import axes, axis, fill, tick_params, title, winter
import streamlit as st
import pandas as pd
import numpy as np
import folium
import plotly.express as px
from streamlit_folium import folium_static
import sqlite3

conn = sqlite3.connect('data.db')
c = conn.cursor()


# Functions
def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS blogtable(author TEXT,title TEXT,article TEXT,postdate DATE)')

def add_data(author, title, article, postdate):
    c.execute('INSERT INTO blogtable(author, title, article, postdate) VALUES (?,?,?,?)', (author, title, article, postdate))
    conn.commit()

def view_all_notes():
    c.execute('SELECT * FROM blogtable')
    data = c.fetchall()
    return data


# st.set_page_config(layout="wide")



# Layout Template
title_temp = """
<div style = "background-color:#464e5f;overflow-x:auto;padding:10px;border-radius:5px;margin:10px;">
<h4 style="color:white; text-align:center;">Title: {}</h4>
<h4 style="color:white; text-align:center;">Author: {}</h4>
</br>
<p style="text-align:justify">{}</p>
</br>
<h6 style="color:white; text-align:justify;">Post Date: {}</h6>

</div>
"""

st.title("Crime Prediction System")

def crime_analysis():
    st.header('NYC crime dataset')
    st.text('A view of this dataset on crime prediction...')
    data = pd.read_csv("crime_analysis.csv")
    st.write(data.head(5))

    st.subheader('New-York city name distribution on the NYC Crime dataset')
    city_name = pd.DataFrame(data['boro_nm'].value_counts())
    st.bar_chart(city_name)

    # the code for selecting individual city to display analysis
    st.subheader('Select The City To View Analysis')
    # make = data['boro_nm'].drop_duplicates()  # Droping Duplicates Values
    # x = list(make)
    # makeChoices = st.selectbox('Select Boro Name', x)  # Adding value selected from select box
    # st.write(data[data['boro_nm'] == makeChoices])
    def filter_data(data):
        make = data['boro_nm'].drop_duplicates() 
        y = list(make)
        makeChoices = st.selectbox('Select Boro Name', y) 

        
        filtered_data = (data[data['boro_nm'] == makeChoices])
        return filtered_data
        
    x = filter_data(data)
    st.write(x)



    st.header(f"Generating Analysis")
    st.subheader("Crime Frequency by Month")
    st.write("The below analysis display the crime frequency with respect to dayparting over a month!")

    fig = px.histogram(x, x='month', color='dayparting', width=800, height=600)
    fig.update_layout(xaxis = dict(showline = True, showgrid = False), yaxis = dict(showgrid =False, showline = True))
    st.plotly_chart(fig)

    # plot charts
    st.subheader("Criminal analysis based on race")
    st.write("The below plot display the crime rate with respect to the race of suspect performing crime!")
    fig = px.pie(x, names='susp_race',hole=.3, width=800, height=600)
    st.plotly_chart(fig)

    # plot charts
    st.subheader('Crime Count on each day')
    st.write('The below plot display the percentage of crime occuring each day!')
    fig = px.pie(x, names='weekday', hole=.3, width= 600 , height=600)
    st.plotly_chart(fig)

   
    # analys by gender
    st.subheader('Victim by Gender')
    fig = px.histogram(x, x = 'vic_sex',color = 'vic_sex',width = 800, height = 600)
    fig.update_layout(xaxis = dict(showline = True, showgrid = False), yaxis = dict(showgrid =False, showline = True))
    st.plotly_chart(fig)

    st.subheader("Crime victims by age group")
    fig = px.histogram(x, x = 'vic_age_group',color = 'vic_age_group',width = 800, height = 600)
    fig.update_layout(xaxis = dict(showline = True, showgrid = False), yaxis = dict(showgrid =False, showline = True))
    st.plotly_chart(fig)

    st.subheader("Crime done on basis of race of Suspect")
    fig = px.box(x, x = 'susp_race', y = 'ofns_desc', color = 'susp_race', width = 1200, height = 900)
    fig.update_layout(xaxis = dict(showline = True, showgrid = False), yaxis = dict(showgrid =False, showline = True))
    # fig.update_traces(quartilemethod ="exclusive")
    st.plotly_chart(fig)

    st.subheader("Determining level of offense")
    fig = px.pie(x, names='law_cat_cd',width= 600 , height=600, hole=.3, color_discrete_sequence=px.colors.sequential.RdBu,)
    st.plotly_chart(fig)

# newly added from here
    # st.write("Now lets have a look on crime using time series analysis")
    

    
    # Number_crimes_days = x['weekday'].value_counts()
    # days = pd.DataFrame(data=Number_crimes_days.index, columns=["weekday"])
    # days['values'] = Number_crimes_days.values
    # fig = px.histogram(x, y="weekday",color="weekday")
    # fig.update_layout(xaxis = dict(showline = True, showgrid = False), yaxis = dict(showgrid =False, showline = True))
    # fig.update_layout(title_text='Crime count on each day', xaxis_title_text='Day',yaxis_title_text='Crimes Count', bargap=0.2, bargroupgap=0.1)
    # st.plotly_chart(fig)


   
    st.subheader("Crime count on each Hour")
    fig = px.histogram(x, x = 'hour',color = 'hour',width = 800, height = 600)
    fig.update_layout(bargap=0.2)
    fig.update_layout(xaxis = dict(showline = True, showgrid = False), yaxis = dict(showgrid =False, showline = True))
    st.plotly_chart(fig)

    # plot
    st.subheader("Crime count per Category on each Year")
    fig = px.histogram(x, x = 'law_cat_cd',color = 'year',width = 800, height = 600)
    fig.update_layout(xaxis = dict(showline = True, showgrid = False), yaxis = dict(showgrid =False, showline = True))
    fig.update_layout(bargap=0.2)
    st.plotly_chart(fig)

     # plot
    st.subheader("Crimes Count per day")
    fig = px.histogram(x, x = 'weekday',color = 'hour',width = 800, height = 600)
    fig.update_layout(bargap=0.2)
    fig.update_layout(xaxis = dict(showline = True, showgrid = False), yaxis = dict(showgrid =False, showline = True))
    st.plotly_chart(fig)

# histogram(data,"DAY_OF_WEEK","HOUR",'Crime count per Day on each Hour','Day','Crimes Count on each Hour')



    #  map for analysis

    st.subheader("MAP FOR ANALYSIS")

    m = folium.Map(location=[40.712776 ,-74.005974], zoom_start=16)


    def circle_marker(x):
        folium.CircleMarker(location=[x[0],x[1]], radius=2, popup="Crime description: {}".format(x[3]),color = 'red', fill = 'True').add_to(m)

    x[['latitude','longitude','pd_cd','ofns_desc']].apply(lambda x:circle_marker(x), axis = 1)
    folium_static(m)
    
    folium.TileLayer('Stamen Terrain').add_to(m)
    folium.TileLayer('Stamen Toner').add_to(m)
    folium.TileLayer('Stamen Water Color').add_to(m)
    folium.TileLayer('cartodbpositron').add_to(m)
    folium.TileLayer('cartodbdark_matter').add_to(m)
    folium.LayerControl().add_to(m)


    st.subheader("The following map shows crime are index vise i.e pin code vise")
    st.write("The data maped here is according tp their index i.e pin code, hence it maps the similar crime happning it thoes cluster.")

    newyork_map = folium.Map(location=[40.668583957,-73.9269799319999],zoom_start=11,tiles="CartoDB dark_matter")
    locations = x.groupby('addr_pct_cd').first()
    new_locations = locations.loc[:, ['latitude','longitude', 'prem_typ_desc', 'law_cat_cd']]
    popup_text = """Community Index : {}<br
                Arrest : {}<br>
                Location Description : {}<br>"""
    for i in range(len(new_locations)):
        lat = new_locations.iloc[i][0]
        long = new_locations.iloc[i][1]
        popup_text = """Community Index : {}<br>
                    Arrest : {}<br>
                    Location Description : {}<br>"""
        popup_text = popup_text.format(new_locations.index[i],
                                new_locations.iloc[i][-1],
                                new_locations.iloc[i][-2]
                                )
        folium.CircleMarker(location = [lat, long], popup= popup_text, fill = True).add_to(newyork_map)

    
    folium.TileLayer('Stamen Terrain').add_to(newyork_map)
    folium.TileLayer('Stamen Toner').add_to(newyork_map)
    folium.TileLayer('Stamen Water Color').add_to(newyork_map)
    folium.TileLayer('cartodbpositron').add_to(newyork_map)
    folium.TileLayer('cartodbdark_matter').add_to(newyork_map)
    folium.LayerControl().add_to(newyork_map)
    folium_static(newyork_map)



    st.subheader("The Below result create cluster of area that have more no.of crime!")
    st.write("The Circle in Red indicates more no.of.crime region")

    # code for second analysis
    unique_locations = x['lat_lon'].value_counts()
    # unique_locations.index
    CR_index = pd.DataFrame({"Raw_String" : unique_locations.index, "ValueCount":unique_locations})
    CR_index.index = range(len(unique_locations))
    # CR_index.head()
    def Location_extractor(Raw_Str):
        preProcess = Raw_Str[1:-1].split(',')
        lat =  preProcess[0][13:-1]
        long = preProcess[1][15:-1]
        return (lat, long)
    CR_index['LocationCoord'] = CR_index['Raw_String'].apply(Location_extractor)
    CR_index  = CR_index.drop(columns=['Raw_String'], axis = 1)

    # %%time

    newyork_map_crime = folium.Map(location=[40.668583957,-73.9269799319999],
                            zoom_start=13,
                            tiles="CartoDB dark_matter")

    for i in range(500):
        lat = CR_index['LocationCoord'].iloc[i][0]
        long = CR_index['LocationCoord'].iloc[i][1]
        radius = CR_index['ValueCount'].iloc[i] / 45
        
        if CR_index['ValueCount'].iloc[i] > 200:
            color = "#FF4500"
        else:
            color = "#008080"
        
        popup_text = """Latitude : {}<br>
                    Longitude : {}<br>
                    Criminal Incidents : {}<br>"""
        popup_text = popup_text.format(lat,
                                long,
                                CR_index['ValueCount'].iloc[i]
                                )
        folium.CircleMarker(location = [lat, long], popup= popup_text,radius = radius, color = color, fill = True).add_to(newyork_map_crime)
    folium.TileLayer('Stamen Terrain').add_to(newyork_map_crime)
    folium.TileLayer('Stamen Toner').add_to(newyork_map_crime)
    folium.TileLayer('Stamen Water Color').add_to(newyork_map_crime)
    folium.TileLayer('cartodbpositron').add_to(newyork_map_crime)
    folium.TileLayer('cartodbdark_matter').add_to(newyork_map_crime)
    folium.LayerControl().add_to(newyork_map_crime)
    folium_static(newyork_map_crime)

    

        





def crime_prediction():
    # st.set_page_config(layout="wide")

    st.title("Welcome to prediction!")
    data = pd.read_csv("finalOutput.csv")



 

    def filter_data(data):
        make = data['boro_nm'].drop_duplicates() 
        y = list(make)
        makeChoices = st.selectbox('Select City Name to view prediction', y) 

        
        filtered_data = (data[data['boro_nm'] == makeChoices])
        return filtered_data
        
    x = filter_data(data)
    st.write(x)

    newyork = [40.712776 ,-74.005974]
    m = folium.Map(newyork, zoom_start = 13)

    st.subheader("Map For Displaying Prediction Results")
    st.write("The red spots in map displays the crime description")

    def circle_marker(x):
        folium.CircleMarker(location =[x[0],x[1]], radius=2,
                        popup = 'Crime description: {}'.format(x[3]),color = 'red', fill = True).add_to(m)
    x[['latitude','longitude','law_cat_cd_pred','ofns_desc_pred']].apply(lambda x:circle_marker(x), axis = 1)

    folium.TileLayer('Stamen Terrain').add_to(m)
    folium.TileLayer('Stamen Toner').add_to(m)
    folium.TileLayer('Stamen Water Color').add_to(m)
    folium.TileLayer('cartodbpositron').add_to(m)
    folium.TileLayer('cartodbdark_matter').add_to(m)
    folium.LayerControl().add_to(m)

    folium_static(m)

    st.subheader("Map For Displaying one offense type in area")
    st.write("The blue spots in map displays the clusters formed indicating offense severity")
    # second map
    new_york = folium.Map(location=[40.712776 ,-74.005974],
                        zoom_start=11,)
    locations = x.groupby('ofns_desc_pred').first()
    new_locations = locations.loc[:, ['latitude', 'longitude', 'law_cat_cd_pred', 'month']]
    for i in range(len(new_locations)):
        lat = new_locations.iloc[i][0]
        long = new_locations.iloc[i][1]
        popup_text = """Law Category : {}<br>
                    Month : {}<br>
                    Category Prediction : {}<br>"""
        popup_text = popup_text.format(new_locations.index[i],
                                new_locations.iloc[i][-1],
                                new_locations.iloc[i][-2]
                                )
        folium.CircleMarker(location = [lat, long], popup= popup_text, fill = True).add_to(new_york)
    folium.TileLayer('Stamen Terrain').add_to(new_york)
    folium.TileLayer('Stamen Toner').add_to(new_york)
    folium.TileLayer('Stamen Water Color').add_to(new_york)
    folium.TileLayer('cartodbpositron').add_to(new_york)
    folium.TileLayer('cartodbdark_matter').add_to(new_york)
    folium.LayerControl().add_to(new_york)
    folium_static(new_york)


    st.markdown(""" ### 1. Here the month are indicated in form of numbers
    ### 2. The number range from 1 to 12 where 1 indicates January and 12 indicates December """)
    



def user_review():  
    add_blog = st.beta_container()
    # view_blog = st.beta_container()

    with add_blog:
        st.title("Welcome to Review Page !")
        st.markdown("### You can add your review here")

        st.subheader("ADD POST")
        create_table()
        blog_author = st.text_input("Enter your name", max_chars=50)
        blog_title = st.text_input("Enter Post Title")
        blog_article = st.text_area("Post Article here",height=150)
        blog_post_date = st.date_input("Date")

        if st.button("ADD"):
            add_data(blog_author,blog_title,blog_article,blog_post_date)
            st.success("Post:{} saved".format(blog_title))

    # with view_blog:
    #     result = view_all_notes()
    #     st.write(result)
def view_review():
    st.subheader("View Post Here!")
    result = view_all_notes()
    # st.write(result)
    for i in result:
        b_author = i[0]
        b_title = i[1]
        b_article = i[2]
        b_post_date = i[3]
        st.markdown(title_temp.format(b_title,b_author,b_article,b_post_date), unsafe_allow_html=True)

        # st.write(i)







def about_us():
  
    st.title("Members")
    col1, col2, col3, col4 = st.beta_columns(4)
    col1.subheader("Team Members:")
    col2.subheader("Sonali Joshi") 
    col3.subheader("Robin Lobo")
    col4.subheader("Joel Fernandes")

    col5,col6 = st.beta_columns(2)
    col5.subheader("Project Guide:")
    col6.subheader("Prof. Prajakta Bhagale")

    st.title("Project Abstract")
    st.write("To implement and design a system that assists in preserving crime statistics of a city by analyzing past records and predicting the crime of that specific city, Depending on the depth of the security aspects.")


def main():
    st.sidebar.image("logo.jpg")
    st.sidebar.title("Crime Prediction System")
    nav = ['About Us', 'Crime Analysis', 'Prediction','User Review','View Reviews',]
    choice =  st.sidebar.selectbox('Navigation', nav)
      
    if choice == 'Crime Analysis':
        crime_analysis()
    elif choice == 'Prediction':
       crime_prediction()
    elif choice == 'User Review':   
        user_review() 
    elif choice == 'View Reviews':
        view_review()
    # elif choice == 'Map Analysis':
    #     map_analysis()
    elif choice == 'About Us':
        about_us()



    
main()