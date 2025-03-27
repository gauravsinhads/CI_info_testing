import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
tpci = pd.read_excel("TalkpushCI_data_fetch.xlsx")
tpci['INVITATIONDT'] = pd.to_datetime(tpci['INVITATIONDT'])

# Define colors for graphs
colors = ["#001E44", "#F5F5F5", "#E53855", "#B4BBBE", "#2F76B9", "#3B9790", "#F5BA2E", "#6A4C93", "#F77F00"]

# Sidebar dropdown
st.sidebar.header("Select Time Period")
time_filter = st.sidebar.selectbox("Time Period", ["Last 30 days", "Last 12 Weeks", "Last 1 Year", "All Time"])

# Filter data based on selection
max_date = tpci['INVITATIONDT'].max()
if time_filter == "Last 30 days":
    filtered_data = tpci[tpci['INVITATIONDT'] >= max_date - pd.DateOffset(days=30)]
    date_freq = 'D'
elif time_filter == "Last 12 Weeks":
    filtered_data = tpci[tpci['INVITATIONDT'] >= max_date - pd.DateOffset(weeks=12)]
    date_freq = 'W'
elif time_filter == "Last 1 Year":
    filtered_data = tpci[tpci['INVITATIONDT'] >= max_date - pd.DateOffset(years=1)]
    date_freq = 'M'
else:
    filtered_data = tpci.copy()
    date_freq = 'M'

# Graph 1: Lead Count Trend
lead_trend = filtered_data.resample(date_freq, on='INVITATIONDT').count()
fig1 = px.line(lead_trend, x=lead_trend.index, y='RECORDID', title='Lead Count Trend', labels={'RECORDID': 'Counts'}, color_discrete_sequence=[colors[0]])
st.plotly_chart(fig1, use_container_width=True)

# Graph 2: Top 10 Campaign Titles
top_campaigns = filtered_data['CAMPAIGNTITLE'].value_counts().nlargest(10)
fig2 = px.bar(top_campaigns, x=top_campaigns.index, y=top_campaigns.values, title='Top 10 Campaign Titles', labels={'y': 'Counts'}, color_discrete_sequence=[colors[2]])
st.plotly_chart(fig2, use_container_width=True)

# Graph 3: Top 10 Source Counts
top_sources = filtered_data['SOURCE'].value_counts().nlargest(10)
fig3 = px.bar(top_sources, x=top_sources.index, y=top_sources.values, title='Top 10 Source Counts', labels={'y': 'Counts'}, color_discrete_sequence=[colors[3]])
st.plotly_chart(fig3, use_container_width=True)

# Graph 4: Top 10 Assigned Manager Counts
top_managers = filtered_data['ASSIGNEDMANAGER'].value_counts().nlargest(10)
fig4 = px.bar(top_managers, x=top_managers.index, y=top_managers.values, title='Top 10 Assigned Manager Counts', labels={'y': 'Counts'}, color_discrete_sequence=[colors[4]])
st.plotly_chart(fig4, use_container_width=True)

# Graph 5: Top 10 Folder Occurrences
top_folders = filtered_data['FOLDER'].value_counts().nlargest(10)
fig5 = px.bar(top_folders, x=top_folders.index, y=top_folders.values, title='Top 10 Folder Occurrences', labels={'y': 'Counts'}, color_discrete_sequence=[colors[5]])
st.plotly_chart(fig5, use_container_width=True)

# Graph 6: Top 5 Completion Methods
top_completion_methods = filtered_data['COMPLETIONMETHOD'].value_counts().nlargest(5)
fig6 = px.bar(top_completion_methods, x=top_completion_methods.index, y=top_completion_methods.values, title='Top 5 Completion Methods', labels={'y': 'Counts'}, color_discrete_sequence=[colors[6]])
st.plotly_chart(fig6, use_container_width=True)

# Graph 7: Repeat Application Counts
repeat_applications = filtered_data[filtered_data['REPEATAPPLICATION'] == 't'].resample(date_freq, on='INVITATIONDT').count()
fig7 = px.bar(repeat_applications, x=repeat_applications.index, y='REPEATAPPLICATION', title='Repeat Application Counts', labels={'REPEATAPPLICATION': "Counts-'REPEATAPPLICATION'"}, color_discrete_sequence=[colors[7]])
st.plotly_chart(fig7, use_container_width=True)

# Graph 8: Top 5 Campaign Type Occurrences
top_campaign_types = filtered_data['CAMPAIGN_TYPE'].value_counts().nlargest(5)
fig8 = px.bar(top_campaign_types, x=top_campaign_types.index, y=top_campaign_types.values, title='Top 5 Campaign Type Occurrences', labels={'y': 'Counts'}, color_discrete_sequence=[colors[8]])
st.plotly_chart(fig8, use_container_width=True)

# Graph 9: Lead Counts by Campaign Site
top_campaign_sites = filtered_data['CAMPAIGN_SITE'].value_counts().nlargest(5)
fig9 = px.bar(top_campaign_sites, x=top_campaign_sites.index, y=top_campaign_sites.values, title='Lead Counts by Campaign Site', labels={'y': 'Counts'}, color_discrete_sequence=[colors[0]])
st.plotly_chart(fig9, use_container_width=True)
