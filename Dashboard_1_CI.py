import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

# Define colors for graphs
colors = ["#001E44", "#F5F5F5", "#E53855", "#B4BBBE", "#2F76B9", 
          "#3B9790", "#F5BA2E", "#6A4C93", "#F77F00"]

# Load and cache data without UI components
@st.cache_data
def load_data():
    try:
        tpci = pd.read_csv('TalkpushCI_data_fetch.csv')
        
        # Date parsing with multiple fallbacks
        tpci['INVITATIONDT'] = pd.to_datetime(
            tpci['INVITATIONDT'],
            infer_datetime_format=True,
            errors='coerce',
            dayfirst=False  # Change to True if dates are DD/MM format
        )
        
        # Return data with parsing information
        null_dates = tpci['INVITATIONDT'].isnull().sum()
        bad_rows = tpci[tpci['INVITATIONDT'].isnull()]
        return {
            'data': tpci.dropna(subset=['INVITATIONDT']),
            'null_count': null_dates,
            'bad_rows': bad_rows,
            'error': None
        }
    
    except Exception as e:
        return {
            'data': pd.DataFrame(),
            'null_count': 0,
            'bad_rows': pd.DataFrame(),
            'error': str(e)
        }

# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False

# Load data
data_result = load_data()

# ======================
# Data Loading UI Section
# ======================
st.title("Talkpush CI Dashboard")

if data_result['error']:
    st.error(f"🚨 Critical Data Error: {data_result['error']}")
    st.stop()

if not data_result['data'].empty:
    st.session_state.data_loaded = True
    tpci = data_result['data']
    null_count = data_result['null_count']
    bad_rows = data_result['bad_rows']
    
    st.success(f"✅ Data loaded successfully ({len(tpci):,} valid records)")
    
    if null_count > 0:
        st.warning(f"⚠️ {null_count} records had invalid dates and were excluded")
        
        with st.expander("Show problematic records"):
            st.dataframe(bad_rows.head())
            
            csv = bad_rows.to_csv(index=False).encode()
            st.download_button(
                label="Download problematic records",
                data=csv,
                file_name="invalid_dates.csv",
                mime="text/csv"
            )
else:
    st.error("No valid data loaded - check your CSV file")
    st.stop()

# ===================
# Dashboard Controls
# ===================
st.sidebar.header("Filters")
time_period = st.sidebar.selectbox(
    "Time Period",
    ["Last 30 days", "Last 12 Weeks", "Last 1 Year", "All Time"],
    index=0
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

# Dynamic resampling
freq_mapping = {
    "Last 30 days": 'D',
    "Last 12 Weeks": 'W-MON',
    "Last 1 Year": 'M',
    "All Time": 'M'
}
freq = freq_mapping[time_period]

# =================
# Visualization
# =================
st.markdown("---")

# Lead Count Trend
try:
    st.subheader("Lead Count Trend")
    lead_count = filtered_data.set_index('INVITATIONDT').resample(freq).size().reset_index(name='Count')
    
    fig1 = px.line(
        lead_count,
        x='INVITATIONDT',
        y='Count',
        labels={'INVITATIONDT': 'Date', 'Count': 'Lead Count'},
        color_discrete_sequence=[colors[0]],
        template='plotly_white'
    )
    
    fig1.update_layout(
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        hovermode='x unified'
    )
    
    st.plotly_chart(fig1, use_container_width=True)
    
except Exception as e:
    st.error(f"Error generating trend chart: {str(e)}")

# Top Campaigns
try:
    st.subheader("Top 10 Campaign Titles")
    campaign_counts = filtered_data.groupby('CAMPAIGNTITLE').size().reset_index(name='Count')
    top_campaigns = campaign_counts.nlargest(10, 'Count').sort_values('Count', ascending=True)
    
    fig2 = px.bar(
        top_campaigns,
        x='Count',
        y='CAMPAIGNTITLE',
        orientation='h',
        labels={'Count': 'Lead Count', 'CAMPAIGNTITLE': 'Campaign Title'},
        color='Count',
        color_continuous_scale=px.colors.sequential.Blues_r
    )
    
    fig2.update_layout(
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        showlegend=False,
        template='plotly_white'
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
except Exception as e:
    st.error(f"Error generating campaign chart: {str(e)}")

# Footer
st.markdown("---")
st.markdown("Dashboard created using Streamlit | Data updated: {}".format(max_date.strftime('%Y-%m-%d')))
