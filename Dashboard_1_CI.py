import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

# Define colors for graphs
colors = ["#001E44", "#F5F5F5", "#E53855", "#B4BBBE", "#2F76B9", 
          "#3B9790", "#F5BA2E", "#6A4C93", "#F77F00"]

# Load and cache data without any UI components
@st.cache_data
def load_data():
    try:
        tpci = pd.read_csv('TalkpushCI_data_fetch.csv')
        
        # Improved datetime conversion
        tpci['INVITATIONDT'] = pd.to_datetime(
            tpci['INVITATIONDT'],
            infer_datetime_format=True,
            errors='coerce',
            dayfirst=False
        )
        
        # Return both data and parsing info
        null_dates = tpci['INVITATIONDT'].isnull().sum()
        bad_dates = tpci[tpci['INVITATIONDT'].isnull()]
        return {
            'data': tpci.dropna(subset=['INVITATIONDT']),
            'null_count': null_dates,
            'bad_rows': bad_dates
        }
    
    except Exception as e:
        return {'error': str(e)}

# Load data
data_result = load_data()

# Handle errors and display UI components outside the cached function
if 'error' in data_result:
    st.error(f"Error loading data: {data_result['error']}")
    st.stop()

tpci = data_result['data']
null_count = data_result['null_count']
bad_dates = data_result['bad_rows']

# Show data quality warnings
if null_count > 0:
    st.warning(f"⚠️ Could not parse {null_count} date entries. Showing partial data.")
    
    with st.expander("Show problematic rows"):
        st.dataframe(bad_dates.head())
    
    # Create download button for problematic data
    csv = bad_dates.to_csv(index=False).encode()
    st.download_button(
        label="Download problematic rows as CSV",
        data=csv,
        file_name="unparsed_dates.csv",
        mime="text/csv"
    )

# Show data loading status
st.success(f"✅ Data loaded successfully ({len(tpci)} valid records)")

# Rest of the code remains the same from previous version...
# [Include the time period selection and visualization code here]
