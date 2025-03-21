import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# Load Data
tpci = pd.read_csv("TalkpushCI_data_fetch.csv")
tpci['INVITATIONDT'] = pd.to_datetime(tpci['INVITATIONDT'])

# Define Colors
colors = ["#001E44", "#F5F5F5", "#E53855", "#B4BBBE", "#2F76B9", "#3B9790", "#F5BA2E", "#6A4C93", "#F77F00"]

# Sidebar Dropdown
st.sidebar.header("Filter Options")
time_filter = st.sidebar.selectbox("Select Time Period", ["Last 30 days", "Last 12 Weeks", "Last 1 Year", "All Time"])

def filter_data(df, time_filter):
    today = datetime.today()
    if time_filter == "Last 30 days":
        start_date = today - timedelta(days=30)
        df = df[df['INVITATIONDT'] >= start_date]
    elif time_filter == "Last 12 Weeks":
        start_date = today - timedelta(weeks=12)
        df = df[df['INVITATIONDT'] >= start_date]
    elif time_filter == "Last 1 Year":
        start_date = today - timedelta(weeks=52)
        df = df[df['INVITATIONDT'] >= start_date]
    return df

filtered_data = filter_data(tpci, time_filter)

# Lead Count Trend Chart
def plot_lead_trend(df, time_filter):
    df['Date'] = df['INVITATIONDT'].dt.date
    if time_filter == "Last 30 days":
        trend_data = df.groupby('Date').size().reset_index(name='Count')
    elif time_filter == "Last 12 Weeks":
        df['Week'] = df['INVITATIONDT'].dt.to_period("W").astype(str)
        trend_data = df.groupby('Week').size().reset_index(name='Count')
    else:
        df['Month'] = df['INVITATIONDT'].dt.to_period("M").astype(str)
        trend_data = df.groupby('Month').size().reset_index(name='Count')
    
    fig = px.line(trend_data, x=trend_data.columns[0], y='Count', title='Lead Count Trend', markers=True, color_discrete_sequence=[colors[0]])
    return fig

st.plotly_chart(plot_lead_trend(filtered_data, time_filter))

# Top 10 Campaign Titles
def plot_top_campaigns(df):
    top_campaigns = df['CAMPAIGNTITLE'].value_counts().nlargest(10).reset_index()
    top_campaigns.columns = ['CAMPAIGNTITLE', 'Count']
    fig = px.bar(top_campaigns, x='CAMPAIGNTITLE', y='Count', title='Top 10 Campaign Titles', color='Count', color_continuous_scale='Blues')
    return fig

st.plotly_chart(plot_top_campaigns(filtered_data))
