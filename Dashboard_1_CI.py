import streamlit as st 
import pandas as pd
import plotly.express as px

# Load and filter data
@st.cache_data
def load_data():
    tpci = pd.read_csv('TalkpushCI_data_fetch.csv')
    tpci = tpci[tpci['CRMINSTANCE'].str.contains('dava', case=False, na=False)]
    tpci['INVITATIONDT'] = pd.to_datetime(tpci['INVITATIONDT'])
    return tpci

tpci = load_data()

# Function to get aggregated data
def get_aggregated_data(tpci, freq, period):
    lead_counts = (
        tpci.groupby(tpci['INVITATIONDT'].dt.to_period(freq))
        .agg({'RECORDID': 'count'})
        .reset_index()
    )
    lead_counts['INVITATIONDT'] = lead_counts['INVITATIONDT'].astype(str)
    
    if period:
        lead_counts = lead_counts.iloc[-period:]  # Keep only the last 'period' entries
    
    return lead_counts

# Streamlit app
st.title("Lead Count Trends Dashboard")

# Dropdown for time aggregation
view = st.selectbox("Select View", ["Daily", "Weekly", "Monthly", "All Time"])

# Set frequency and period based on selection
if view == "Daily":
    lead_counts = get_aggregated_data(tpci, "D", 30)
elif view == "Weekly":
    lead_counts = get_aggregated_data(tpci, "W", 12)
elif view == "Monthly":
    lead_counts = get_aggregated_data(tpci, "M", 12)
else:
    lead_counts = get_aggregated_data(tpci, "D", None)

# Plot the graph
fig = px.line(
    lead_counts, x='INVITATIONDT', y='RECORDID',
    title=f'Trend of Lead Counts ({view} View)',
    labels={'INVITATIONDT': 'Date', 'RECORDID': 'Lead Count'},
    markers=True
)
fig.update_xaxes(title_text='Date', tickangle=-45)
fig.update_yaxes(title_text='Lead Count')

st.plotly_chart(fig)
