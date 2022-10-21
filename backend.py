from datetime import datetime
from datetime import date
import pandas as pd
import streamlit as st


#data
@st.cache(allow_output_mutation=True)
def load_assets():
    assets = pd.read_excel("data.xlsx",
                    sheet_name = "Assets",
                    converters={"Next earnings": pd.to_datetime})
    return assets

@st.cache(allow_output_mutation=True)  
def load_stoxx600():
    stoxx600 = pd.read_excel("data.xlsx",
                    sheet_name = "stoxx600")
    return stoxx600

@st.cache(allow_output_mutation=True)
def load_stoxx50():
    stoxx50 = pd.read_excel("data.xlsx",
                    sheet_name = "stoxx50")
    return stoxx50

def margins_table(equities, financials, \
    selected_period, selected_indicators, \
        selected_period_types, selected_value_types):
    
    selected_indicators = selected_indicators
    selected_period_types = selected_period_types
    selected_value_types = selected_value_types

    margins = financials.query("Indicator in ['Revenue', 'EBITDA', 'EBITDA adjusted', 'EBITDA adjusted', 'EBIT', 'EBIT adjusted']")
    margins = margins.pivot_table(values = 'Value',
                        columns = 'Indicator',
                    index = ['Ticker', 'UOM', 'Period type', 'Value type', 'Date'])
    margins['EBIT margin'] = margins['EBIT'] / margins ['Revenue']
    margins['EBIT adjusted margin'] = margins['EBIT adjusted'] / margins ['Revenue']
    margins['EBITDA margin'] = margins['EBITDA'] / margins ['Revenue']
    margins['EBITDA adjusted margin'] = margins['EBITDA adjusted'] / margins ['Revenue']
    margins.drop(labels = ['Revenue', 'EBITDA', 'EBITDA adjusted', 'EBITDA adjusted', 'EBIT', 'EBIT adjusted'],
                axis = 1,
                inplace = True)
    margins = pd.melt(margins, value_vars = margins.columns, ignore_index = False, value_name = 'Value')
    margins.reset_index(inplace = True)
    margins.sort_index(axis = 1, inplace = True)


    financials = pd.concat(objs = [financials, margins])

#    indicators = financials["Indicator label"].unique()


    AY = datetime.strptime(selected_period, "%Y-%m-%d")


    PY = datetime(AY.year - 1, AY.month, AY.day)

    periods = pd.DataFrame(zip(["AY", "PY"],[AY, PY]), columns = ["Period label", "Date"])



    earnings = equities[["Ticker", "Name", "Sector", "Sub Industry"]]
    earnings = earnings.merge(financials, on = 'Ticker', how = 'left')
    earnings = earnings.merge(right = periods, on = "Date", how = 'inner')
    earnings = earnings.query(" `Indicator` in @selected_indicators \
                            and `Period type`  in @selected_period_types \
                            and `Value type` in @selected_value_types \
                            ")

    earnings = pd.pivot_table(data = earnings,
                index = ["Ticker", "Name", "Sector", "Sub Industry"],
                columns = ["Period label", "Period type", "Indicator"]
                )
    earnings.columns = earnings.columns.droplevel(0)


    YoY_rel = earnings['AY'] / earnings['PY'] - 1
    YoY_rel.style.format('{:.1%}', na_rep = '-')


    YoY_abs = earnings['AY'] - earnings['PY']
    YoY_abs.style.format('{:.3f}', na_rep = '-')


    YoY_abs["YTD"][["EBIT adjusted margin", 
                    "EBIT margin", "EBITDA adjusted margin", "EBITDA margin"]].style.format(
        '{:.2%}', na_rep = '-')

    cols = YoY_rel.columns.to_list()


    new_cols = []
    for col in cols:
        new_cols.append(('YoY, rel',) + col)
    new_cols


    YoY_rel.columns = pd.MultiIndex.from_tuples(new_cols)
    YoY_rel.style.format('{:.1%}', na_rep = '-')


    earnings = pd.concat([earnings, YoY_rel], axis = 1)


    styler = {}
    for i in earnings[['AY', 'PY']].columns:
        styler[i] = '{:,.2f}'
    for i in earnings[['YoY, rel']].columns:
        styler[i] = '{:.1%}'

#    df = earnings.style.format(formatter = styler, na_rep = '-')
    return earnings


#multiselect filter builder
def create_multiselect_filters(filters): 
    for k, v in filters.items():
        selection = st.sidebar.multiselect(
            label = k,
            options = filters[k]["Options"],
            default = filters[k]["Options"]
        )
        filters[k]["Selection"] = selection

#add filters with dynamic options
def build_filters(data, filtered_columns):
    filters = {}
    for column in filtered_columns:
        filters[column] = {"Selection": [""], "Options": [""]}

    filtered_data = data

    for column in filtered_columns:

        options = filtered_data[column].unique()

        selection = st.sidebar.multiselect(
            label = column,
            options = options,
            default = options
                )

        filters[column]["Selection"] = selection

        filtered_data = filtered_data[
                filtered_data[column].isin(filters[column]["Selection"])]

        for column in filtered_columns:
            options_updated = filtered_data[column].unique()
            filters[column]["Options"] = options_updated
    return filtered_data