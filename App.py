import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from wordcloud import WordCloud
import constants 
import Latest.genAI as genAI
import Latest.apiKey

warnings.filterwarnings("ignore")
pd.options.display.max_columns = None
pd.options.display.max_rows = None

st.set_page_config(
    page_title="ONDC Hackathon Dashboard",
    page_icon="👩🏻‍💻" ,
    layout="wide", 
    initial_sidebar_state="collapsed",
)

import Latest.CityInsights as ct
import Latest.Logistics as lt

st.title('Build for Bharat: Data as a service 🇮🇳')

st.session_state.User=''

def creds_entered():
    if st.session_state.username == constants.USERNAME and st.session_state.password == constants.PASSWORD:
        st.session_state.User=constants.USERNAME
        st.session_state.logged_in = True

    elif st.session_state.username != constants.USERNAME or st.session_state.password != constants.PASSWORD:
        st.error("Incorrect Username or password ")
        st.session_state.logged_in = False
    else:
        pass


def LogIn(): 
    
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.write("Hello, 👋 Welcome to the dashboard by Dlayer team. Please login with your credentials to proceed with the data insights")
        username = st.text_input(label="Username",key="username")#,on_change=creds_entered)
        password = st.text_input("Password", key="password" ,type="password",on_change=creds_entered)
        
        return False
    else:
        if st.session_state.logged_in:
            return True
        else:
            st.write("Hello, 👋 Welcome to the dashboard by Dlayer team. Please login with your credentials to proceed with the data insights")
            username = st.text_input(label="Username",key="username")#,on_change=creds_entered)
            password = st.text_input("Password",  key="password", type="password",on_change=creds_entered)
           
            return False

@st.cache_data
def read_dataframe():
    Indian_df=pd.read_csv("../Zomato/Indian_zomato.csv", encoding='ISO-8859-1')
    print(Indian_df)
    ## RENAMING AND DROPPING THE COLUMNS
    Indian_df.rename(columns={'Unnamed: 0': 'ID'}, inplace=True)
    Indian_df.drop(['Restaurant ID','Country Code','Locality','Currency','Rating color','Switch to order menu'],axis=1,inplace=True)#df.drop(['C', 'D'], axis=1)
    return Indian_df

@st.cache_data
def read_logistics_dataframe():
    logistics_df=pd.read_csv("../Logistics/DeliveryPointsGenAI.csv")
    return logistics_df


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

#Initialise the key in session state
if 'clicked' not in st.session_state:
    st.session_state.clicked ={1:False}

#Function to udpate the value in session state
def clicked(button):
    st.session_state.clicked[button]= True


def GeneralInsights():
    col1, col2 = st.columns(2)

    with col1:
        
        #TOP 5 CITIES in the business
        city_counts = Indian_df['City'].value_counts().reset_index()
        fig = px.bar(city_counts.head(5), x="City", y="count", orientation='v',color='City', text='count' 
                     ,title='Top 5 Cities with Maximum number of Restraunts',color_discrete_sequence=px.colors.sequential.Agsunset
                     , height=480) #df.sort_values('count')
        st.plotly_chart(fig)
        st.caption("<p style ='text-align:left'> Figure #1:Presenting Top 5 cities where maximum number of Restraunts are present </p>",unsafe_allow_html=True)

    # fig = px.pie(city_counts.tail(7), values='count', names='City')
    # st.plotly_chart(fig)
    with col2:
        
        #TOP 5 CUISINES in the business
        Indian_df_cuisines_list=Indian_df['Cuisines'].tolist()
        Indian_df_cuisines_list=flattened_list(Indian_df_cuisines_list)
        Indian_df_Cuisines_df=pd.DataFrame(Indian_df_cuisines_list, columns=['Cuisine'])
        Indian_df_Cuisines_df=Indian_df_Cuisines_df['Cuisine'].value_counts().reset_index()
        
        fig = px.pie(Indian_df_Cuisines_df.head(5), values='count', names='Cuisine',title='Top 5 Famous Cuisines rated by Customers'
                     ,color_discrete_sequence=px.colors.sequential.Agsunset, width=620, height=480)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig)
        st.caption("<p style ='text-align:left'> Figure #2:Presenting top 5 Cuisines as preferred by the customers</p>",unsafe_allow_html=True )


    
    # Apply the function to each group (city)
    df_filtered = Indian_df.groupby('City')['Average Cost for two'].apply(remove_outliers).reset_index(name='Average Cost for two')
    # df_filtered.drop(['level_1'],axis=1,inplace=True)
    df_filtered.rename(columns={'level_1': 'Restaurant ID'}, inplace=True)
    # st.write(df_filtered)
    # print(df_filtered.columns)
    fig_scatter = px.scatter(df_filtered, x='City', y='Average Cost for two', color='City', title='Average Cost for Two People per Restraunts in Top 5 Cities with Maximum Restaurants', 
                             hover_data="Restaurant ID" ,labels={'price': 'Price'},color_discrete_sequence=px.colors.sequential.Agsunset , width=1180, height=600)
    st.plotly_chart(fig_scatter)
    st.caption("<p style ='text-align:left'> Figure #3:Presenting average cost for two people per restraunt in respective cities where every circle represents a restraunt in that city.</p>",unsafe_allow_html=True )
    
    col3,col4=st.columns(2)
    with col3:
        # st.caption("Figure # 4")
        # average cost for 2 in the top 5 cities
        popular_cities=city_counts.head(5).sort_values(by='City',ascending=False)
        top_5_cities=popular_cities['City'].tolist()
        top_5_cities_Indian_df = Indian_df[Indian_df['City'].isin(top_5_cities)]
        df_filtered_top_5_cities_Indian_df = top_5_cities_Indian_df.groupby('City')['Average Cost for two'].apply(remove_outliers).reset_index(name='Average Cost for two')

        # st.write(df_filtered_top_5_cities_Indian_df)
        # fig_scatter = px.scatter(df_filtered_top_5_cities_Indian_df, x='City', y='Average Cost for two', color='City', title='Average Cost for Two in Top 5 Cities with Maximum Restaurants', 
        #                          labels={'price': 'Price'},color_discrete_sequence=px.colors.sequential.Agsunset)
        fig_scatter = px.scatter(df_filtered_top_5_cities_Indian_df, x='City', y='Average Cost for two', color='City', title='Average Cost for Two People per Restraunts in Cities with Maximum Restaurants', 
                                labels={'price': 'Price'},color_discrete_sequence=px.colors.sequential.Agsunset, height=450)
        st.plotly_chart(fig_scatter)
        st.caption("<p style ='text-align:left'> Figure #4:Presenting average cost for two people in the top 5 cities restaurant wise.</p>",unsafe_allow_html=True )

    with col4:

        # st.caption("Figure # 5")  # famous cuisines in the top 5 cities with maximum restraunts
        top_5_cities_cuisines_list=top_5_cities_Indian_df['Cuisines'].tolist()
        top_5_cities_cuisines_list=flattened_list(top_5_cities_cuisines_list)
        top_5_cities_cuisines_df=pd.DataFrame(top_5_cities_cuisines_list, columns=['Cuisine'])
        top_5_cities_cuisines_df=top_5_cities_cuisines_df['Cuisine'].value_counts().reset_index()
        # st.write(top_5_cities_cuisines_df)
        fig = px.pie(top_5_cities_cuisines_df.head(10), values='count', names='Cuisine',title='Famous Cuisines served in the Cities having Maximum Restraunts'
                        ,color_discrete_sequence=px.colors.sequential.Agsunset, width=600, height=450)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig)
        st.caption("<p style ='text-align:left'> Figure #5:Presenting pie chart for the most preferred Cuisine in the top 5 cities restaurant wise.</p>",unsafe_allow_html=True )

    # with st.expander("Want to know something specific about the Analysis?Chat with our dashboard bot"):
    st.write('\n')
    st.write("<h3>Want to know something specific about the Analysis?Chat with our DashBot 🤖</h3>",unsafe_allow_html=True)
    text_entered=st.text_area("Enter your question to ask Dashboard bot")
    st.button("Search", on_click = clicked, args=[1])
    if st.session_state.clicked[1]:
        genAI.user_queries(text_entered)

        # st.markdown("**Integration with Generative AI bot in progress. Stay tuned...**")

# def LogIn():
#     st.session_state.username='admin'
#     return True
        
selectBox_font_css = """
<style>
div[class*="stSelectbox"] label {
  font-size: 55px !important;
}
</style>
"""

st.write(selectBox_font_css, unsafe_allow_html=True)

################################# UI BEGINS
if LogIn():
    st.session_state.username='admin'# st.session_state.User=constants.USERNAME
    st.write("Welcome to the Dashboard, ",st.session_state.username," !")
    Indian_df=read_dataframe()
    logistics_df=read_logistics_dataframe()
    col1,col2=st.columns(2)
    with col1:
        st.write(" ")
        # st.write(" ")
        st.write('<h4>Select your Industry from the dropdown menu</h4>',unsafe_allow_html=True)
    with col2:
        Industry_list=['Food and Beverages', 'Fashion','Agriculture','Beauty and Personal Care']
        Industry = st.selectbox(' ',Industry_list)

    if Industry:
        if Industry!='Food and Beverages':
            # st.write("We will be there soon...")
            st.write('<h4>We will be there soon</h4>',unsafe_allow_html=True)
            
        else:
            # st.write("Showing results for ",Industry)
            IndustrySelect='<h6>Showing results for '+Industry+' Industry. </h6>'
            # st.write(IndustrySelect,unsafe_allow_html=True)
            # st.write(Indian_df.head(2))
            font_css=''' <style> button[data-baseweb="tab"] { font-size: 24px; margin: 0; width: 100%; } </style>'''
            st.write(font_css,unsafe_allow_html=True)

            tab1, tab2, tab3 = st.tabs(["📊 General Pulse Check In", "📈 Know your City Better", "📦 Optimise your Logistics"])

            with tab1:
                GeneralInsights()

            with tab2:
                ct.city_level_insights(Indian_df)   

            with tab3:
                st.write("Logistics data goes here ")   
                lt.Logistics(logistics_df)
            
# st.divider()
# st.caption("<p style ='text-align:center'> Made with ❤️ by Eshika</p>",unsafe_allow_html=True )
