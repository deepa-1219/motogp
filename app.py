import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="MotoGP Rider Summary", layout="wide")
st.title("🏍️ MotoGP Rider Career Dashboard")

# Upload data
@st.cache_data
def load_data():
    return pd.read_csv("RidersSummary.csv")

df = load_data()

# Sidebar filters
st.sidebar.header("🎯 Filters")
riders = df['rider_name'].unique().tolist()
selected_rider = st.sidebar.selectbox("Select Rider", sorted(riders))

classes = df['class'].unique().tolist()
selected_classes = st.sidebar.multiselect("Select Class", sorted(classes), default=classes)

min_year = int(df['season'].min())
max_year = int(df['season'].max())
selected_years = st.sidebar.slider("Select Season Range", min_year, max_year, (min_year, max_year))

# Filter data
filtered = df[
    (df['rider_name'] == selected_rider) &
    (df['class'].isin(selected_classes)) &
    (df['season'] >= selected_years[0]) &
    (df['season'] <= selected_years[1])
]

# Summary
st.subheader(f"📊 Stats Summary for {selected_rider}")
st.dataframe(filtered)

# Pie Charts
st.markdown("### 🥧 Career Pie Charts")
col1, col2, col3 = st.columns(3)
with col1:
    fig1, ax1 = plt.subplots()
    ax1.pie([filtered['wins'].sum(), filtered['races_participated'].sum() - filtered['wins'].sum()],
            labels=['Wins', 'No Wins'], autopct='%1.1f%%', colors=['#4CAF50', '#FFC107'])
    ax1.set_title("Wins Distribution")
    st.pyplot(fig1)

with col2:
    fig2, ax2 = plt.subplots()
    ax2.pie([filtered['podium'].sum(), filtered['races_participated'].sum() - filtered['podium'].sum()],
            labels=['Podiums', 'No Podium'], autopct='%1.1f%%', colors=['#2196F3', '#E0E0E0'])
    ax2.set_title("Podium Distribution")
    st.pyplot(fig2)

with col3:
    fig3, ax3 = plt.subplots()
    ax3.pie([filtered['world_championships'].sum(), 
             filtered['races_participated'].sum()], 
            labels=['Championships', 'Other Races'],
            autopct='%1.1f%%', colors=['#9C27B0', '#BDBDBD'])
    ax3.set_title("Championship Wins")
    st.pyplot(fig3)

# Bar Chart - Points per Season
st.markdown("### 📊 Points Scored per Season")
fig4, ax4 = plt.subplots(figsize=(10, 4))
ax4.bar(filtered['season'], filtered['points'], color='#00BCD4')
ax4.set_xlabel("Season")
ax4.set_ylabel("Points")
ax4.set_title(f"{selected_rider} - Points by Season")
st.pyplot(fig4)

# Line Graph - Placement over time
st.markdown("### 📈 Rider Placement Trend (Lower is Better)")
fig5, ax5 = plt.subplots(figsize=(10, 4))
ax5.plot(filtered['season'], filtered['placed'], marker='o', color='#FF5722')
ax5.invert_yaxis()  # Better placements (1st) appear at the top
ax5.set_xlabel("Season")
ax5.set_ylabel("Placement")
ax5.set_title(f"{selected_rider} - Yearly Placement")
st.pyplot(fig5)
