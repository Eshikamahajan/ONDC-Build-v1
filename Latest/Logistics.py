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
def wordcloud(sample_list):
    wordcloud = WordCloud(width=700, height=400, background_color='white', normalize_plurals=False).generate(' '.join(sample_list))
    fig, ax = plt.subplots(figsize = (12, 8))
    ax.imshow(wordcloud)
    plt.gca().add_patch(plt.Rectangle((0, 0), 800, 400, linewidth=2, edgecolor='g', facecolor='none'))
    plt.axis("off")
    st.pyplot(fig)

@st.cache_data  
def flattened_list(sample_list):
    flattened_cuisine_list = [Cuisines.strip() for Cuisines in sample_list for Cuisines in Cuisines.split(',')] # getting a flattened list of cuisines
    flattened_cuisine_list=flattened_cuisine_list
    #print(len(flattened_cuisine_list))
    return flattened_cuisine_list

def Logistics(logistics_df):

    # st.write("<h3> Let's Explore the Logistics Data in Delhi</h3>",unsafe_allow_html=True )
    st.write(" ")
    logistics_df['DeliveryRating']=logistics_df['DeliveryRating'].apply(lambda x: round(x,2) )
    logistics_df['AverageDeliveryTime']=logistics_df['AverageDeliveryTime'].apply(lambda x: round(x,2) )
    logistics_df['DeliveryCharges']=logistics_df['DeliveryCharges'].apply(lambda x: round(x,2) )
    # st.write(logistics_df)
    Agencies=logistics_df['AgencyName'].tolist()
    agencies_list=flattened_list(Agencies)
    Unique_agencies_list=set(agencies_list)

    # wordcloud(Unique_agencies_list)

    # Combine "Destination" and "City" into a new column "FullDestination"
    logistics_df['FullDestination'] = logistics_df['Destination'] + ', ' + logistics_df['City']


    destination_analysis = logistics_df.groupby('Destination').agg({
        'AverageDeliveryTime': 'mean',
        'DeliveryRating': 'mean',
        'DeliveryCharges': 'mean'
    }).reset_index()
    
    destination_analysis = destination_analysis.round(2)
    

    agency_analysis = logistics_df.groupby('AgencyName').agg({
        'AverageDeliveryTime': 'mean',
        'DeliveryRating': 'mean',
        'DeliveryCharges': 'mean'
    }).reset_index()
    
    agency_analysis = agency_analysis.round(2)
    

    col1,col2=st.columns(2)
    with col1:
        st.write("\nAgency-wise Analysis:")
        st.write(agency_analysis)
    with col2:
        st.write("\nDestination-wise Analysis:")
        st.write(destination_analysis)

    col3,col4=st.columns(2)
    with col3:

        logistics_agencies=logistics_df['AgencyName'].value_counts().reset_index()
        # st.write(top_5_cities_cuisines_df)
        fig = px.pie(logistics_agencies.head(10), values='count', names='AgencyName',title='Logistic Agencies in your network'
                        ,color_discrete_sequence=px.colors.sequential.Agsunset,width=550, height=500)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig)
        st.caption("<p style ='text-align:left'> Figure#8:Presenting pie chart comprising of different logistics agencies in the network.</p>",unsafe_allow_html=True )
        st.write(" ")
    
    with col4:
        agencies_rating=agency_analysis['DeliveryRating']
        # st.write(top_5_cities_cuisines_df)
        fig = px.pie(agency_analysis, values='DeliveryRating', names='AgencyName',title='Logistic Agencies Rating in your network'
                        ,color_discrete_sequence=px.colors.sequential.Agsunset, width=550,height=500)
        fig.update_traces(textposition='inside', textinfo='label+value')
        st.plotly_chart(fig)
        st.caption("<p style ='text-align:left'> Figure#9:Presenting pie chart comprising of diferent logistic agencies in the network and their respective average rating.</p>",unsafe_allow_html=True )
        st.write(" ")


    col1,col2=st.columns(2)

    with col1:
        # 1. Bar plot for Average Delivery Time, Rating, and Charges
        fig = px.bar(logistics_df, x='AgencyName', y='AverageDeliveryTime', title='Average Delivery Time - Agency Wise',color='Destination',color_discrete_sequence=px.colors.sequential.Agsunset,width=550, height=450)
        st.plotly_chart(fig)
        st.caption("<p style ='text-align:left'> Figure#10:Presenting a comparison of average delivery time taken by logistics agencies for different destinations in the city. </p>",unsafe_allow_html=True )
        st.write(" ")
    with col2:
       
        fig = px.bar(logistics_df, x='AgencyName', y='DeliveryRating', title='Average Delivery Rating - Agency Wise',color='Destination',color_discrete_sequence=px.colors.sequential.Agsunset ,width=570, height=450 )
        st.plotly_chart(fig)
        st.caption("<p style ='text-align:left'> Figure#11:Presenting a comparison of average delivery rating of logistics agencies for different destinations in the city.</p>",unsafe_allow_html=True )
        st.write(" ")

    col3,col4=st.columns(2)
    
    with col3:
       
        fig = px.bar(logistics_df, x='AgencyName', y='DeliveryCharges', title='Average Delivery Charges - Agency Wise',color='Destination',color_discrete_sequence=px.colors.sequential.Agsunset ,width=570, height=450)
        st.plotly_chart(fig)
        st.caption("<p style ='text-align:left'> Figure#12:Presenting a comparison of average delivery prices charged by logistics agencies for different destinations in the city. </p>",unsafe_allow_html=True )
        st.write(" ")

    with col4:
  
        fig = px.bar(destination_analysis, x='Destination', y='AverageDeliveryTime', title='Average Delivery Time by Destination',color='Destination',color_discrete_sequence=px.colors.sequential.Agsunset ,width=570, height=450)
        st.plotly_chart(fig)
        st.caption("<p style ='text-align:left'> Figure#13:Presnting average delivery time taken to deliver to the respective destinations in the city. </p>",unsafe_allow_html=True )
        st.write(" ")

    col5,col6=st.columns(2)
    with col5:
       
        fig = px.bar(destination_analysis, x='Destination', y='DeliveryRating', title='Average Delivery Rating by Destination',color='Destination',color_discrete_sequence=px.colors.sequential.Agsunset ,width=570, height=450)
        st.plotly_chart(fig)
        st.caption("<p style ='text-align:left'> Figure#14:Presnting average delivery rating for respective destinations as per delivery system in the city.  </p>",unsafe_allow_html=True )
        st.write(" ")

    with col6:
  
        fig = px.bar(destination_analysis, x='Destination', y='DeliveryCharges', title='Average Delivery Charges by Destination',color='Destination',color_discrete_sequence=px.colors.sequential.Agsunset ,width=570, height=450)
        st.plotly_chart(fig)
        st.caption("<p style ='text-align:left'> Figure#15:Presnting average delivery prices charged by different logistics agency for respective destinations in the city. </p>",unsafe_allow_html=True )
        st.write(" ")


    # st.divider()
    # st.caption("<p style ='text-align:left'> Made with ❤️ by Eshika</p>",unsafe_allow_html=True )

# Basic Analysis Examples:

    # 1. Average Delivery Time Analysis
    # average_delivery_time = logistics_df['AverageDeliveryTime'].mean()
    # st.write("\nAverage Delivery Time across all agencies:", average_delivery_time)

    # # 2. Delivery Rating Analysis
    # average_delivery_rating = logistics_df['DeliveryRating'].mean()
    # st.write("Average Delivery Rating across all agencies:", average_delivery_rating)

    # # 3. Delivery Charges Analysis
    # average_delivery_charges = logistics_df['DeliveryCharges'].mean()
    # st.write("Average Delivery Charges across all agencies:", average_delivery_charges)

    # 4. Destination-wise Analysis