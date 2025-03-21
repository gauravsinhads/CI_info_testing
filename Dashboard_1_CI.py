import streamlit as st
import pandas as pd
import plotly.express as px

# Define colors for graphs
colors = ["#001E44", "#F5F5F5", "#E53855", "#B4BBBE", "#2F76B9", 
          "#3B9790", "#F5BA2E", "#6A4C93", "#F77F00"]

# Load and cache data
@st.cache_data
def load_data():
    tpci = pd.read_csv('TalkpushCI_data_fetch.csv')
    tpci['INVITATIONDT'] = pd.to_datetime(tpci['INVITATIONDT'])
    return tpci

tpci = load_data()

# Sidebar - Time Period Selection
time_period = st.sidebar.selectbox(
    "Select Time Period",
    ["Last 30 days", "Last 12 Weeks", "Last 1 Year", "All Time"]
)

# Calculate date range based on selection
max_date = tpci['INVITATIONDT'].max()
start_date = max_date

if time_period == "Last 30 days":
    start_date = max_date - pd.DateOffset(days=30)
elif time_period == "Last 12 Weeks":
    start_date = max_date - pd.DateOffset(weeks=12)
elif time_period == "Last 1 Year":
    start_date = max_date - pd.DateOffset(years=1)
else:
    start_date = None

# Filter data based on selected time period
if start_date is not None:
    filtered_data = tpci[tpci['INVITATIONDT'] >= start_date]
else:
    filtered_data = tpci.copy()

# Determine frequency for resampling
if time_period == "Last 30 days":
    freq = 'D'
elif time_period == "Last 12 Weeks":
    freq = 'W'
else:  # For "Last 1 Year" and "All Time"
    freq = 'M'

# Graph 1: Lead Count Trend
st.subheader('Lead Count Trend')
lead_count = filtered_data.set_index('INVITATIONDT').resample(freq).size().reset_index(name='Count')

fig1 = px.line(
    lead_count, 
    x='INVITATIONDT', 
    y='Count',
    labels={'INVITATIONDT': 'Date', 'Count': 'Lead Count'},
    color_discrete_sequence=[colors[0]]
)
fig1.update_layout(
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False),
    plot_bgcolor='white'
)
st.plotly_chart(fig1, use_container_width=True)

# Graph 2: Top 10 Campaign Titles
st.subheader('Top 10 Campaign Titles')
campaign_counts = filtered_data.groupby('CAMPAIGNTITLE').size().reset_index(name='Count')
top_campaigns = campaign_counts.nlargest(10, 'Count').sort_values('Count', ascending=True)

fig2 = px.bar(
    top_campaigns,
    x='Count',
    y='CAMPAIGNTITLE',
    orientation='h',
    labels={'Count': 'Lead Count', 'CAMPAIGNTITLE': 'Campaign Title'},
    color_discrete_sequence=colors
)
fig2.update_layout(
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False),
    plot_bgcolor='white'
)
st.plotly_chart(fig2, use_container_width=True)

# Add some spacing between components
st.markdown("<br><br>", unsafe_allow_html=True)
