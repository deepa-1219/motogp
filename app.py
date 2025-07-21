import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Page settings
st.set_page_config(page_title="MotoGP Rider Analysis", layout="wide")

st.title("🏍️ MotoGP Rider Circuit Direction Analysis")
st.markdown("""
Analyze **MotoGP riders' wins** across clockwise and anticlockwise circuits.  
**Filters** below let you explore by class, season, and compare multiple riders.
""")

# Load data
@st.cache_data
@st.cache_data
def load_data():
    import os
    import pandas as pd

    # Load circuits with corner info
    df_circuits = pd.read_csv('data/circuit_data.csv', usecols=['Name', 'Right Corners','Left Corners'])

    # Load original races
    df_races_original = pd.read_csv('data/grand-prix-race-winners.csv')

    # Load mock 2024–2025 races
    df_races_2024_2025 = pd.read_csv('data/motogp-mock-wins-2024-2025.csv')

    # Combine race data
    df_races = pd.concat([df_races_original, df_races_2024_2025], ignore_index=True)

    # Load rider season info
    df_seasons = pd.read_csv('data/active_years_per_category.csv')

    return df_circuits, df_races, df_seasons


df_circuits, df_races, df_active_seasons = load_data()

# Add direction info
df_circuits['Direction'] = ['Clockwise' if r > l else 'Anticlockwise'
                            for r, l in zip(df_circuits['Right Corners'], df_circuits['Left Corners'])]
df_dir = df_circuits[['Name', 'Direction']]
merged_df = pd.merge(df_dir, df_races, left_on='Name', right_on='Circuit')
merged_df = merged_df[['Circuit', 'Direction', 'Class', 'Rider', 'Season']]

# Sidebar filters
st.sidebar.header("🔍 Filters")

# Rider filter
rider_list = df_active_seasons['rider_name'].dropna().unique().tolist()
selected_riders = st.sidebar.multiselect("Select Rider(s)", sorted(rider_list), default=["Valentino Rossi"])

# Class filter
class_list = merged_df['Class'].unique().tolist()
selected_classes = st.sidebar.multiselect("Select Class(es)", sorted(class_list), default=["MotoGP™"])

# Season filter
min_year = merged_df['Season'].min()
max_year = merged_df['Season'].max()
selected_years = st.sidebar.slider("Select Season Range", min_year, max_year, (1996, 2020))

# Filter data
filtered_df = merged_df[
    (merged_df['Rider'].isin(selected_riders)) &
    (merged_df['Class'].isin(selected_classes)) &
    (merged_df['Season'] >= selected_years[0]) &
    (merged_df['Season'] <= selected_years[1])
]

# Overview
st.subheader("📊 Summary by Rider and Direction")
summary = filtered_df.groupby(['Rider', 'Direction']).size().unstack(fill_value=0)
summary['Total Wins'] = summary.sum(axis=1)
summary['Win % Clockwise'] = round((summary['Clockwise'] / summary['Total Wins']) * 100, 2)
summary['Win % Anticlockwise'] = round((summary['Anticlockwise'] / summary['Total Wins']) * 100, 2)
st.dataframe(summary)

# Plot comparison chart
st.subheader("🏁 Win Direction Breakdown (Bar Chart)")
fig1, ax1 = plt.subplots(figsize=(10, 5))
direction_counts = filtered_df.groupby(['Rider', 'Direction']).size().unstack(fill_value=0)
direction_counts.plot(kind='bar', stacked=True, ax=ax1)
ax1.set_ylabel("Number of Wins")
ax1.set_title("Wins by Rider and Circuit Direction")
st.pyplot(fig1)

# Optional: Show data table
if st.checkbox("📄 Show Raw Filtered Data Table"):
    st.write(filtered_df.sort_values(by=["Rider", "Season"]))

# Optional: Download CSV
st.download_button(
    label="💾 Download Filtered Data as CSV",
    data=filtered_df.to_csv(index=False),
    file_name='filtered_motogp_data.csv',
    mime='text/csv'
)
