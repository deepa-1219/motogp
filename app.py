import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="MotoGP 2024–2025 Analysis", layout="wide")
st.title("🏍️ MotoGP Rider Performance Comparison (2024 vs 2025)")

# File uploads
st.sidebar.header("📁 Upload MotoGP CSV Files")
file_2024 = st.sidebar.file_uploader("Upload 2024 Standings CSV", type="csv")
file_2025 = st.sidebar.file_uploader("Upload 2025 Standings CSV", type="csv")

if file_2024 and file_2025:
    df_2024 = pd.read_csv(motogp2024.csv)
    df_2025 = pd.read_csv(motogp2025.csv)

    # Merge on Rider name
    merged = pd.merge(df_2024, df_2025, on="Rider", suffixes=("_2024", "_2025"))

    # Select metric
    metric = st.selectbox("📊 Select Metric to Compare", ['Race Pts', 'Qual Pts', 'Wup Pts', 'Sprint Pts'])

    # Filter by rider
    all_riders = merged['Rider'].tolist()
    selected_riders = st.multiselect("🎯 Select Riders to Display", all_riders, default=all_riders)

    filtered = merged[merged['Rider'].isin(selected_riders)]

    st.markdown("### 📈 Bar Chart Comparison")
    fig_bar, ax = plt.subplots(figsize=(12, 6))
    ax.bar(filtered['Rider'], filtered[f'{metric}_2024'], label='2024', width=0.4, align='edge')
    ax.bar(filtered['Rider'], filtered[f'{metric}_2025'], label='2025', width=-0.4, align='edge')
    ax.set_title(f"{metric} Comparison (2024 vs 2025)")
    ax.set_ylabel(metric)
    ax.set_xticklabels(filtered['Rider'], rotation=45, ha='right')
    ax.legend()
    st.pyplot(fig_bar)

    # Line chart toggle
    if st.checkbox("📉 Show Line Chart"):
        st.markdown(f"### 📊 Line Chart for {metric}")
        fig_line, ax_line = plt.subplots(figsize=(12, 5))
        ax_line.plot(filtered['Rider'], filtered[f'{metric}_2024'], marker='o', label='2024')
        ax_line.plot(filtered['Rider'], filtered[f'{metric}_2025'], marker='o', label='2025')
        ax_line.set_ylabel(metric)
        ax_line.set_title(f"{metric} Trend Line by Rider")
        ax_line.set_xticklabels(filtered['Rider'], rotation=45, ha='right')
        ax_line.legend()
        st.pyplot(fig_line)

    # Pie chart toggle
    if st.checkbox("🥧 Show Pie Chart Distributions"):
        col1, col2 = st.columns(2)
        with col1:
            fig_pie1, ax1 = plt.subplots()
            ax1.pie(filtered[f'{metric}_2024'], labels=filtered['Rider'], autopct='%1.1f%%')
            ax1.set_title(f"{metric} Distribution - 2024")
            st.pyplot(fig_pie1)
        with col2:
            fig_pie2, ax2 = plt.subplots()
            ax2.pie(filtered[f'{metric}_2025'], labels=filtered['Rider'], autopct='%1.1f%%')
            ax2.set_title(f"{metric} Distribution - 2025")
            st.pyplot(fig_pie2)

    # Downloadable chart as PNG
    from io import BytesIO
    buf = BytesIO()
    fig_bar.savefig(buf, format="png")
    st.download_button("💾 Download Bar Chart as PNG", data=buf.getvalue(), file_name="motogp_comparison.png", mime="image/png")

else:
    st.info("👈 Please upload both 2024 and 2025 MotoGP CSVs from the sidebar to begin.")
