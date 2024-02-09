import os 
# from apiKey import apiKey
import streamlit as st
import pandas as pd
from langchain.llms import OpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from dotenv import load_dotenv, find_dotenv
import Latest.secretKey as secretKey

#OpenAIKey
os.environ['OPENAI_API_KEY'] = secretKey.apiKey
load_dotenv(find_dotenv())
llm = OpenAI(temperature = 0)

Indian_df=pd.read_csv("../Zomato/Indian_zomato.csv", encoding='ISO-8859-1')
Indian_df.rename(columns={'Unnamed: 0': 'ID'}, inplace=True) ## RENAMING AND DROPPING THE COLUMNS
Indian_df.drop(['Restaurant ID','Country Code','Locality','Currency','Rating color','Switch to order menu'],axis=1,inplace=True)#df.drop(['C', 'D'], axis=1)

pandas_agent = create_pandas_dataframe_agent(llm, Indian_df, verbose = True)

@st.cache_data
def function_question_dataframe(user_question_dataframe):
    dataframe_info = pandas_agent.run(user_question_dataframe)
    st.write(dataframe_info)
    return

def user_queries(user_question_variable):
    # user_question_variable = st.text_input('What variable are you interested in')
    if user_question_variable is not None and user_question_variable !="":
        st.write("Generating response")
        function_question_dataframe(user_question_variable)

