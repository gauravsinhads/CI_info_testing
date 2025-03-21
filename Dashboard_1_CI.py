import streamlit as st
import pandas as pd
import plotly.express as px

# Load and filter data
@st.cache_data
def load_data():
    try:
        # Load the CSV file
        tpci = pd.read_csv('TalkpushCI_data_fetch.csv')
        
        # Filter rows where CRMINSTANCE contains 'dava' (case-insensitive)
        tpci = tpci[tpci['CRMINSTANCE'].str.contains('dava', case=False, na=False)]
        
        # Convert INVITATIONDT to datetime safely
        tpci['INVITATIONDT'] = pd.to_datetime(tpci['INVITATIONDT'], errors='coerce')
        
        # Drop rows where INVITATIONDT is NaT (invalid dates)
        tpci = tpci.dropna(subset=['INVITATIONDT'])
        
    except FileNotFoundError:
        st.error("The file 'TalkpushCI_data_fetch.csv' was not found. Please upload the correct file.")
        return pd.DataFrame()  # Return an empty DataFrame if file is missing
    
    except Exception as e:
        st.error(f"An error occurred while loading the data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame if any other error occurs
    
    return tpci

# Load the data
tpci = load_data()

# Function to get aggregated data
def get_aggregated_data(tpci, freq, period):
    if tpci.empty:
        return pd.DataFrame(columns=['INVITATIONDT', 'RECORDID'])  # Return an empty DataFrame if no data
    
    # Group by the specified frequency and count RECORDID
    lead_counts = (
        tpci.groupby(tpci['INVITATIONDT'].dt.to_period(freq))
        .agg({'RECORDID': 'count'})
        .reset_index()
    )
    
    # Convert INVITATIONDT back to string for plotting
    lead_counts['INVITATIONDT'] = lead_counts['INVITATIONDT'].astype(str)
    
    # Keep only the last 'period' entries if a period is specified
    if period:
        lead_counts = lead_counts.iloc[-period:]
    
    return lead_counts

# Streamlit app title
st.title("Lead Count Trends Dashboard")

# Dropdown for time aggregation view
view = st.selectbox("Select View", ["Daily", "Weekly", "Monthly", "All Time"])

# Set frequency and period based on the selected view
if view == "Daily":
    lead_counts = get_aggregated_data(tpci, "D", 30)  # Last 30 days
elif view == "Weekly":
    lead_counts = get_aggregated_data(tpci, "W", 12)  # Last 12 weeks
elif view == "Monthly":
    lead_counts = get_aggregated_data(tpci, "M", 12)  # Last 12 months
else:
    lead_counts = get_aggregated_data(tpci, "D", None)  # All time

# Check if there is data to plot
if not lead_counts.empty:
    # Create a line plot with Plotly Express
    fig = px.line(
        lead_counts, x='INVITATIONDT', y='RECORDID',
        title=f'Trend of Lead Counts ({view} View)',
        labels={'INVITATIONDT': 'Date', 'RECORDID': 'Lead Count'},
        markers=True
    )
    
    # Customize axes for better readability
    fig.update_xaxes(title_text='Date', tickangle=-45)
    fig.update_yaxes(title_text='Lead Count')
    
    # Display the plot in Streamlit
    st.plotly_chart(fig)
else:
    st.warning("No data available to display. Please check your filters or data source.")
