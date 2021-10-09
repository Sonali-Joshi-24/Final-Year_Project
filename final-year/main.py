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


    # st.subheader('')
    fig = px.histogram(x, x='month', color='dayparting', width=800, height=600, title="Crime Frequency by Month...")
    st.plotly_chart(fig)

    # plot charts
    fig = px.pie(x, names='susp_race', title='Criminal analysis on race', hole=.3, width=800, height=600)
    st.plotly_chart(fig)

    # plot charts
    fig = px.pie(x, names='weekday', title='Crime Count on each day', hole=.3, width= 600 , height=600)
    st.plotly_chart(fig)

    # to check the offence active
    # st.subheader('Analyze The Number Of Crime In Total')
    # select_crime = data['ofns_desc'].drop_duplicates()
    # y = list(select_crime)
    # make_decs = st.selectbox('CRIME TYPE: ', y)
    # # st.write(data[data['ofns_desc'] == make_decs])
    # # st.write(f"The dataset registers {data.shape[0]} entries for {make_decs} in total")
    # filter_data =  data[data.ofns_desc.str.contains(make_decs)]
    # st.subheader(f"The dataset registers {filter_data.shape[0]} entries for {make_decs} in total")


   
    # analys by gender
    # st.subheader('Crime Analysis By Gender')
    fig = px.histogram(x, x = 'vic_sex',color = 'vic_sex',width = 800, height = 600, title ="Crime victims by gender")
    st.plotly_chart(fig)

    fig = px.histogram(x, x = 'vic_age_group',color = 'vic_age_group',width = 800, height = 600, title ="Crime victims by age group")
    st.plotly_chart(fig)

    fig = px.box(x, x = 'susp_race', y = 'ofns_desc', color = 'susp_race', width = 1200, height = 900, title= "Crime done on basis of race")
    # fig.update_traces(quartilemethod ="exclusive")
    st.plotly_chart(fig)

    fig = px.pie(x, names='law_cat_cd', title='Determining level of offense',width= 600 , height=600, hole=.3, color_discrete_sequence=px.colors.sequential.RdBu,)
    st.plotly_chart(fig)


    # map for analysis

    st.subheader("MAP FOR ANALYSIS")

    m = folium.Map(location=[40.712776 ,-74.005974], zoom_start=16, width= 1000, height = 700)


    def circle_marker(x):
        folium.CircleMarker(location=[x[0],x[1]], radius=2, popup="Crime description: {}".format(x[3]),color = 'red', fill = 'True').add_to(m)

    x[['latitude','longitude','pd_cd','ofns_desc']].apply(lambda x:circle_marker(x), axis = 1)
    folium_static(m)




# def map_analysis():

#     data = pd.read_csv("crime_analysis.csv", low_memory=False)
#     # st.subheader('Select The City To View Analysis')
#     # make = data['boro_nm'].drop_duplicates()  # Droping Duplicates Values
#     # x = list(make)
#     # makeChoices = st.selectbox('Select Boro Name', x)  # Adding value selected from select box
#     # st.write(data[data['boro_nm'] == makeChoices])
    

#     st.subheader("MAP FOR ANALYSIS")

#     m = folium.Map(location=[40.712776 ,-74.005974], zoom_start=16, width= 1000, height = 700)


#     def circle_marker(x):
#         folium.CircleMarker(location=[x[0],x[1]], radius=2, popup="Crime description: {}".format(x[3]),color = 'red', fill = 'True').add_to(m)

#     data[['latitude','longitude','pd_cd','ofns_desc']].apply(lambda x:circle_marker(x), axis = 1)
#     folium_static(m)



def crime_prediction():
    st.title("Welcome to prediction!")


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
    st.title("Hello")


def main():
    st.sidebar.image("logo.jpg")
    st.sidebar.title("Crime Prediction System")
    nav = ['About Us', 'Crime Analysis', 'Prediction','User Review','View Reviews']
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