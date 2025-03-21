import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

# Define colors for graphs
colors = ["#001E44", "#F5F5F5", "#E53855", "#B4BBBE", "#2F76B9", 
          "#3B9790", "#F5BA2E", "#6A4C93", "#F77F00"]

# Load and cache data with robust date parsing
@st.cache_data
def load_data():
    try:
        tpci = pd.read_csv('TalkpushCI_data_fetch.csv')
        
        # Improved datetime conversion with multiple fallbacks
        tpci['INVITATIONDT'] = pd.to_datetime(
            tpci['INVITATIONDT'],
            infer_datetime_format=True,
            errors='coerce',
            dayfirst=False  # Set to True if dates are DD/MM format
        )
        
        # Check for parsing failures
        null_dates = tpci['INVITATIONDT'].isnull().sum()
        if null_dates > 0:
            st.warning(f"⚠️ Could not parse {null_dates} date entries. Showing partial data.")
            
            # Show problematic rows
            bad_dates = tpci[tpci['INVITATIONDT'].isnull()]
            st.write("Problematic rows with unparsed dates:")
            st.dataframe(bad_dates.head())
            
            # Create download button for problematic data
            csv = bad_dates.to_csv(index=False).encode()
            st.download_button(
                label="Download problematic rows as CSV",
                data=csv,
                file_name="unparsed_dates.csv",
                mime="text/csv"
            )
        
        return tpci.dropna(subset=['INVITATIONDT'])
    
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()  # Return empty dataframe to prevent crashes

tpci = load_data()

# Show data loading status
if not tpci.empty:
    st.success(f"✅ Data loaded successfully ({len(tpci)} records)")
else:
    st.stop()  # Stop execution if no data

# Sidebar - Time Period Selection
time_period = st.sidebar.selectbox(
    "Select Time Period",
    ["Last 30 days", "Last 12 Weeks", "Last 1 Year", "All Time"]
)

# Date filtering logic
max_date = tpci['INVITATIONDT'].max()
date_ranges = {
    "Last 30 days": max_date - pd.DateOffset(days=30),
    "Last 12 Weeks": max_date - pd.DateOffset(weeks=12),
    "Last 1 Year": max_date - pd.DateOffset(years=1),
    "All Time": tpci['INVITATIONDT'].min()
}

filter_date = date_ranges[time_period]
filtered_data = tpci[tpci['INVITATIONDT'] >= filter_date]

# Dynamic resampling frequency
freq_mapping = {
    "Last 30 days": 'D',
    "Last 12 Weeks": 'W-MON',
    "Last 1 Year": 'M',
    "All Time": 'M'
}
freq = freq_mapping[time_period]

# --- Graph 1: Lead Count Trend ---
st.subheader('Lead Count Trend')

try:
    lead_count = filtered_data.set_index('INVITATIONDT').resample(freq).size().reset_index(name='Count')
    
    fig1 = px.line(
        lead_count,
        x='INVITATIONDT',
        y='Count',
        labels={'INVITATIONDT': 'Date', 'Count': 'Lead Count'},
        color_discrete_sequence=[colors[0]]
    )
    
    fig1.update_layout(
        xaxis=dict(showgrid=False, title='Date'),
        yaxis=dict(showgrid=False, title='Number of Leads'),
        hovermode='x unified',
        plot_bgcolor='white'
    )
    
    st.plotly_chart(fig1, use_container_width=True)

except Exception as e:
    st.error(f"Error generating lead count trend: {str(e)}")

# --- Graph 2: Top 10 Campaign Titles ---
st.subheader('Top 10 Campaign Titles')

try:
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
        xaxis=dict(showgrid=False, title='Number of Leads'),
        yaxis=dict(showgrid=False, title='Campaign Title'),
        plot_bgcolor='white'
    )
    
    st.plotly_chart(fig2, use_container_width=True)

except Exception as e:
    st.error(f"Error generating campaign titles chart: {str(e)}")

# Add some spacing at the bottom
st.markdown("<br><br>", unsafe_allow_html=True)
