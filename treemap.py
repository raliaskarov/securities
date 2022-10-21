import streamlit as st
import plotly.express as px
import pandas as pd
from backend import *

def treemap():


    assets = load_assets()
    stoxx600 = load_stoxx600()
    stoxx50 = load_stoxx50()
            
    indices = {"stoxx600": stoxx600, "stoxx50": stoxx50}

    indices_keys = indices.keys()

    selected_index = st.sidebar.selectbox(
        label = "Select index",
        options = indices_keys,
        index = 0
        )

    index = indices[selected_index]

    data = pd.merge(
        left = index,
        right = assets,
        how = 'left',
        on = 'Ticker'
    )


    #set which columns to filter
    filtered_columns = ["Exchange", "Sector", "Sub Industry", "Ticker"]


    df = build_filters(data, filtered_columns)

    df["Index"] = selected_index

    df[["Index", "Sector", "Sub Industry", "Name"]] = \
        df[["Index", "Sector", "Sub Industry", "Name"]].fillna("-")

#    df.fillna("-", inplace=True)


    fig = px.treemap(
        df,
        path = ["Index", "Sector", "Sub Industry", "Name"],
        values = "Market Value",
        color_discrete_sequence=[
                                "#4AD24A", 
                                "#D3FD03", 
                                "#0374AD", 
                                "#A4E2FE", 
                                "#758735",
                                "#BECE84", 
                                "#76F0D9", 
                                "#B80088",
                                "#FF69D8"
                                ]
    )
    fig.update_traces(root_color="lightgrey")
    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    fig.update_layout(width = 1100)
    fig.update_layout(height = 600)

    st.markdown("**Composition of {} \
        (measured by market value as of Jun'2022)**".format(selected_index.upper()))
    st.write(fig)

    show_full_list = st.checkbox(
        label = "Show full list",
    )
    if show_full_list:
        st.dataframe(df)    
