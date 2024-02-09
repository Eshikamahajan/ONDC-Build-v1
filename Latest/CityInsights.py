import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from wordcloud import WordCloud
warnings.filterwarnings("ignore")

pd.options.display.max_columns = None
pd.options.display.max_rows = None


@st.cache_data
def city_wise_df(Indian_df,city):
    name_df='df_'+str(city)
    name_df=Indian_df[Indian_df['City']==city]
    return name_df

@st.cache_data  
def flattened_list(sample_list):
    flattened_items_list = [items.strip() for items in sample_list for items in items.split(',')] # getting a flattened list of cuisines
    flattened_items_list=flattened_items_list
    #print(len(flattened_cuisine_list))
    return flattened_items_list

def remove_outliers(group):
    q_low = group.quantile(0.01)
    q_hi = group.quantile(0.99)
    return group[(group > q_low) & (group < q_hi)]

def remove_outliers_df(df):
    q_low = df['Average Cost for two'].quantile(0.01)
    q_hi = df['Average Cost for two'].quantile(0.99)
    return df[(df['Average Cost for two'] > q_low) & (df['Average Cost for two'] < q_hi)]


def full_graph(city_df_Cuisines_df,city_df_without_outliers):
    st.header("Analysis # 5")
    fig = px.bar(city_df_Cuisines_df.head(25), x="count", y="Cuisine", orientation='h', color='Cuisine', title='Different Cuisines served in the Selected City')
    st.plotly_chart(fig)

    st.header("Analysis # 6")
    fig = px.bar(city_df_without_outliers, x='Cuisines', y='Average Cost for two', title='Average Cost for Two in the Selected City',labels={'price': 'Price'})
    st.plotly_chart(fig)


def city_level_insights(Indian_df):

    City_list=Indian_df['City'].tolist()
    City_list=flattened_list(City_list)
    Unique_City_list=set(City_list)
    st.write("<h3> Let's Explore the data at City level</h3>",unsafe_allow_html=True )
    st.write(" ")
    city_option = st.selectbox( 'Select a city that you wish to analyse', Unique_City_list)
    text='You selected: '+ city_option
    st.header(text)
    st.write(" ")

    if city_option:
        city_df=city_wise_df(Indian_df,city_option)
        # st.write(city_df)
        #TOP 5 CUISINES in the business
        city_df_cuisines_list=city_df['Cuisines'].tolist()
        city_df_cuisines_list=flattened_list(city_df_cuisines_list)
        city_df_Cuisines_df=pd.DataFrame(city_df_cuisines_list, columns=['Cuisine'])
        city_df_Cuisines_df=city_df_Cuisines_df['Cuisine'].value_counts().reset_index()
        city_df_without_outliers = remove_outliers_df(city_df)

        if len(set(city_df_cuisines_list))>15:
            pass

        # st.warning("Since there are more than 15 Cuisines served in this city, Displaying results for top 10 served Cuisines")
        
        fig = px.bar(city_df_Cuisines_df.head(25), x="Cuisine", y="count", orientation='v', color='Cuisine', 
                        title='Famous Cuisines served in the Selected City', color_discrete_sequence=px.colors.sequential.Agsunset , width=1180, height=600)
        st.plotly_chart(fig)
        st.caption("<p style ='text-align:left'> Figure #6:Presenting Cuisines and the number of restaurant that serves that Cuisines in the selected city.  </p>",unsafe_allow_html=True )

        top_5_Cuisines=city_df_Cuisines_df.head(5)['Cuisine'].tolist()
        mask = city_df_without_outliers['Cuisines'].apply(lambda x: any(cuisine in x for cuisine in top_5_Cuisines))
        filtered_df = city_df_without_outliers[mask]
      
        fig = px.scatter(filtered_df.head(20), x='Cuisines', y='Average Cost for two', title='Average Cost for Two in the Selected City',
                        color_discrete_sequence=px.colors.sequential.Agsunset,labels={'price': 'Price'}, width=1180, height=600)
        st.plotly_chart(fig)
        st.caption("<p style ='text-align:left'> Figure #7:Presenting Average cost for two people per restraunt in the selected city and the famous cuisines served in the restaurants.</p>",unsafe_allow_html=True )

       