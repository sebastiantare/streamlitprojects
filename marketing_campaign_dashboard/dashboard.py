import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

df = pd.read_csv('https://raw.githubusercontent.com/sebastiantare/streamlitprojects/main/marketing_campaign_dashboard/data_for_dash.csv')
df['ACTIVITY_DATE'] = pd.to_datetime(df['ACTIVITY_DATE'])
df['ACTIVITY_DATE'] = df['ACTIVITY_DATE'].dt.date

tab1, tab2 = st.tabs(["Campaign Stats", "Other"])


@st.cache_data
def filter_data(start_date, end_date, sel_media_buyer, sel_campaign):
    filtered_by_date = df[(df['ACTIVITY_DATE'] >= start_date)
                          & (df['ACTIVITY_DATE'] <= end_date)]

    if sel_media_buyer != 'All':
        filtered_by_media_buyer = filtered_by_date[filtered_by_date['MEDIA_BUYER']
                                                   == sel_media_buyer]
    else:
        filtered_by_media_buyer = filtered_by_date

    if sel_campaign != 'All':
        filtered_by_campaign = filtered_by_media_buyer[filtered_by_media_buyer['CAMPAIGN'] == sel_campaign]
    else:
        filtered_by_campaign = filtered_by_media_buyer

    return filtered_by_campaign


with tab1:
    col1, col2, col3 = st.columns(3)

    with col1:
        min_date = df['ACTIVITY_DATE'].min()
        max_date = df['ACTIVITY_DATE'].max()
        start_date = st.date_input(
            'Start Date', value=min_date, min_value=min_date, max_value=max_date)
        end_date = st.date_input(
            'End Date', value=max_date, min_value=start_date, max_value=max_date)

    with col2:
        media_buyers = ['All'] + list(df['MEDIA_BUYER'].unique())
        sel_media_buyer = st.selectbox('Select a media buyer', media_buyers)

        campaigns = ['All'] + list(df['CAMPAIGN'].unique())
        sel_campaign = st.selectbox('Select a campaign', campaigns)

    filtered_df = filter_data(start_date, end_date,
                              sel_media_buyer, sel_campaign)

    # Plot 1
    total_profit_by_date = filtered_df.groupby('ACTIVITY_DATE')['DAILY_RETURN'].sum().reset_index()
    total_profit_by_date['COLOR'] = np.where(total_profit_by_date['DAILY_RETURN'] < 0, 'orangered', 'royalblue')

    fig = go.Figure()
    fig.add_trace(
        go.Bar(x=total_profit_by_date['ACTIVITY_DATE'],
               y=total_profit_by_date['DAILY_RETURN'],
               marker_color=total_profit_by_date['COLOR']))
    fig.update_layout(barmode='stack', title_text='Daily Return by Date')
    st.plotly_chart(fig)

    # Plot 2
    total_profit_by_date = filtered_df.groupby('ACTIVITY_DATE')['TOTAL_RETURN'].sum().reset_index()
    total_profit_by_date['COLOR'] = np.where(total_profit_by_date['TOTAL_RETURN'] < 0, 'orangered', 'royalblue')

    fig = go.Figure()
    fig.add_trace(
        go.Bar(x=total_profit_by_date['ACTIVITY_DATE'],
               y=total_profit_by_date['TOTAL_RETURN'],
               marker_color=total_profit_by_date['COLOR']))
    fig.update_layout(barmode='stack', title_text='Total Return by Date')
    st.plotly_chart(fig)

    # Plot 3
    total_profit_by_date = filtered_df.groupby('ACTIVITY_DATE')['DAILY_PROFIT'].sum().reset_index()
    total_profit_by_date['COLOR'] = np.where(total_profit_by_date['DAILY_PROFIT'] < 0, 'orangered', 'royalblue')

    fig = go.Figure()
    fig.add_trace(
        go.Bar(x=total_profit_by_date['ACTIVITY_DATE'],
               y=total_profit_by_date['DAILY_PROFIT'],
               marker_color=total_profit_by_date['COLOR']))
    fig.update_layout(barmode='stack', title_text='Daily Profit by Date')
    st.plotly_chart(fig)

    # Plot 4
    total_profit_by_date = filtered_df.groupby('ACTIVITY_DATE')['TOTAL_PROFIT'].sum().reset_index()
    total_profit_by_date['COLOR'] = np.where(total_profit_by_date['TOTAL_PROFIT'] < 0, 'orangered', 'royalblue')

    fig = go.Figure()
    fig.add_trace(
        go.Bar(x=total_profit_by_date['ACTIVITY_DATE'],
               y=total_profit_by_date['TOTAL_PROFIT'],
               marker_color=total_profit_by_date['COLOR']))
    fig.update_layout(barmode='stack', title_text='Total Profit by Date')
    st.plotly_chart(fig)

    # Plot 5
    total_spend_date = filtered_df.groupby('ACTIVITY_DATE')['SPEND'].sum().reset_index()
    total_revenue_date = filtered_df.groupby('ACTIVITY_DATE')['REVENUE'].sum().reset_index()

    fig = go.Figure(data=[
        go.Bar(name='SPEND', x=total_spend_date['ACTIVITY_DATE'], y=total_spend_date['SPEND'], marker_color='orangered'),
        go.Bar(name='REVENUE', x=total_revenue_date['ACTIVITY_DATE'], y=total_revenue_date['REVENUE'], marker_color='royalblue')
    ])

    fig.update_layout(barmode='group', title_text='Spend & Revenue by Date')
    st.plotly_chart(fig)

    st.write(filtered_df)
