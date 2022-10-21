import streamlit as st
from backend import *


#load data

def startpage():
    equities = pd.read_excel("data.xlsx",
                sheet_name = "Assets")

    financials = pd.read_excel("data.xlsx ",
                            sheet_name = "Financials")
    financials.sort_index(axis = 1, inplace = True)

    #set parameters
    selected_period = "2022-06-30"
    selected_indicators = ["Revenue", "EBIT adjusted", "EBITDA adjusted", "EBIT adjusted margin", "EBITDA adjusted margin", "EBITDA margin", "EBIT", "EBIT margin"]
    selected_period_types = ["YTD"]
    selected_value_types = ["Actual"]

    df = margins_table(equities, financials, \
    selected_period, selected_indicators, \
        selected_period_types, selected_value_types)
    
    st.write(df)