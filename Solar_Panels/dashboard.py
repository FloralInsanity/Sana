# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 00:05:47 2023

@author: crike
"""

import pandas as pd # data manipulation
import streamlit as st # hosting dashboard

# define functions
def style_negative(v, props = ''):
    # styling negative values in the data frame
    try:
        return props if  v < 0 else None
    except:
        pass

def style_positive(v, props = ''):
    # styling positive values in the data frame
    try:
        return props if  v > 0 else None
    except:
        pass

def display(df):
    # creating a copy of the dataframe
    df_copy = df.copy()
    df_copy = df_copy.apply(lambda x: pd.to_numeric(x, errors='coerce') if x.name not in ['Site', 'Date', 'Month', 'Time', 'Hour', 'WindDir', 'HiDir', 'THSWIndex'] else x)
    # writing to streamlit
    st.write('Past Month Mean Values (Per Half Hour)')
    # metrics that will be displayed
    df_sigma = df_copy[['Date', 'SolarRad', 'SolarEnergy', 'TempOut', 'InTemp', 'OutHum', 'InHum', 'DewPt', 'InDew', 'WindSpeed', 'WindRun', 'HeatIndex', 'Rain']]
    #df_max = df_sigma.max(numeric_only = True)
    #df_median = df_sigma.median(numeric_only = True)
    #df_mean = df_sigma.mean(numeric_only = True)
    df_1m = df_sigma['Date'].max() - pd.DateOffset(months = 1)
    df_2m = df_sigma['Date'].max() - pd.DateOffset(months = 2)
    # mean at 1 month and 2 months
    df_1m_mean = df_sigma[df_sigma['Date'] >= df_1m].mean(numeric_only = True)
    df_2m_mean = df_sigma[df_sigma['Date'] >= df_2m].mean(numeric_only = True)
    # organising columns in rows
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    columns = [col1, col2, col3, col4, col5, col6]
    # for loop which organises each metric nicely
    count = 0
    for i in df_1m_mean.index:
        with columns[count]:
            delta = (df_1m_mean[i] - df_2m_mean[i]) / df_2m_mean[i]
            st.metric(label = i, value = round(df_1m_mean[i], 1), delta = "{:.2%}".format(delta))
            count += 1
            if count >= 6:
                count = 0
    # temp: creating the table
    #del after 
    df_copy = df_er.copy()
    #del after 
    df_copy = df_copy.apply(lambda x: pd.to_numeric(x, errors='coerce') if x.name not in ['Site', 'Date', 'Month', 'Time', 'Hour', 'WindDir', 'HiDir', 'THSWIndex'] else x)
    
    df_final = df_copy[['Date', 'Time', 'SolarRad', 'SolarEnergy', 'TempOut', 'InTemp', 
                        'OutHum', 'InHum', 'DewPt', 'InDew', 'WindSpeed', 'WindRun', 
                        'HeatIndex', 'Rain']]
    # convert the 'Date' column to a datetime data type
    df_final['Date'] = pd.to_datetime(df_final['Date'])
    # format the dates in the desired format ("dd/mm/yyyy")
    df_final['Date'] = df_final['Date'].dt.strftime('%d/%m/%Y')
    
    # group rows by date, sum the values of values, and find the mean
    df_grouped = df_final.groupby(['Date']).agg({'SolarRad': 'sum', 'SolarEnergy': 'sum', 'TempOut' : 'sum', 'InTemp' : 'sum', 'OutHum' : 'sum', 'InHum' : 'sum', 'DewPt' : 'sum', 'InDew' : 'sum', 'WindSpeed' : 'sum', 'WindRun' : 'sum', 'HeatIndex' : 'sum', 'Rain' : 'sum', }).reset_index()
    df_grouped['SolarRad'] = df_grouped['SolarRad'] / df_final.groupby('Date').size().values
    df_grouped['SolarEnergy'] = df_grouped['SolarEnergy'] / df_final.groupby('Date').size().values
    df_grouped['TempOut'] = df_grouped['TempOut'] / df_final.groupby('Date').size().values
    df_grouped['InTemp'] = df_grouped['InTemp'] / df_final.groupby('Date').size().values
    df_grouped['OutHum'] = df_grouped['OutHum'] / df_final.groupby('Date').size().values
    df_grouped['InHum'] = df_grouped['InHum'] / df_final.groupby('Date').size().values
    df_grouped['DewPt'] = df_grouped['DewPt'] / df_final.groupby('Date').size().values
    df_grouped['InDew'] = df_grouped['InDew'] / df_final.groupby('Date').size().values
    df_grouped['WindSpeed'] = df_grouped['WindSpeed'] / df_final.groupby('Date').size().values
    df_grouped['WindRun'] = df_grouped['WindRun'] / df_final.groupby('Date').size().values
    df_grouped['HeatIndex'] = df_grouped['HeatIndex'] / df_final.groupby('Date').size().values
    df_grouped['Rain'] = df_grouped['Rain'] / df_final.groupby('Date').size().values

    # changing the values into percentages
    df_grouped_numeric_list = df_grouped.median(numeric_only = True).index.tolist()
    df_grouped_dictionary = {}
    for i in df_grouped_numeric_list:
        df_grouped_dictionary[i] = '{:.1%}'.format
    # adding to streamlit
    st.write('Comparing to Average Each Day')
    st.dataframe(df_grouped.style.applymap(style_negative, props = 'color:red;').applymap(style_positive, props = 'color:green;').format(df_grouped_dictionary))
    
# loads already cleaned data
@st.cache_data
def load_data():
    df = pd.read_excel('/Sana/Solar_Panels/solar_data.xlsx', sheet_name = 0)
    # Filter the dataset to create a sub dataset with rows that contain the site keyword 
    df_er = df[df['Site'].str.contains('Easthill Road')]
    df_ec = df[df['Site'].str.contains('Elm Crescent')]
    df_fr = df[df['Site'].str.contains('Forest Road')]
    df_md = df[df['Site'].str.contains('Maple Drive East')]
    df_ym = df[df['Site'].str.contains('YMCA')]
    return df, df_er, df_ec, df_fr, df_md, df_ym

# creates a data frame from the function
df, df_er, df_ec, df_fr, df_md, df_ym = load_data()

# build the dashboard
add_sidebar = st.sidebar.selectbox('Site', ('Easthill Road', 'Elm Crescent', 'Forest Road', 'Maple Drive East', 'YMCA'))

# all coming together
if (add_sidebar == 'Easthill Road'):
    display(df_er)
    
if (add_sidebar == 'Elm Crescent'):
    display(df_ec)

if (add_sidebar == 'Forest Road'):
    display(df_fr)

if (add_sidebar == 'Maple Drive East'):
    display(df_md)

if (add_sidebar == 'YMCA'):
    display(df_ym)




