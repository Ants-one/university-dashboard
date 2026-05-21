import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from io import StringIO

# ─── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="University Student Dashboard",
    page_icon="🎓",
    layout="wide",
)

# ─── Team members ────────────────────────────────────────────────────────────
TEAM = ["Student Name 1", "Student Name 2", "Student Name 3", "Student Name 4"]

# ─── Data ────────────────────────────────────────────────────────────────────
DATA_CSV = """Year,Term,Applications,Admitted,Enrolled,Retention Rate (%),Student Satisfaction (%),Engineering Enrolled,Business Enrolled,Arts Enrolled,Science Enrolled
2015,Spring,2500,1500,600,85,78,200,150,125,125
2015,Fall,2500,1500,600,85,78,200,150,125,125
2016,Spring,2600,1550,625,86,79,210,160,130,125
2016,Fall,2600,1550,625,86,79,210,160,130,125
2017,Spring,2700,1600,650,87,80,225,165,135,125
2017,Fall,2700,1600,650,87,80,225,165,135,125
2018,Spring,2800,1650,675,86,82,235,175,140,125
2018,Fall,2800,1650,675,86,82,235,175,140,125
2019,Spring,3000,1750,700,88,83,250,185,145,120
2019,Fall,3000,1750,700,88,83,250,185,145,120
2020,Spring,2900,1700,690,85,81,240,180,140,130
2020,Fall,2900,1700,690,85,81,240,180,140,130
2021,Spring,3100,1800,725,87,84,260,195,150,120
2021,Fall,3100,1800,725,87,84,260,195,150,120
2022,Spring,3250,1900,750,88,85,275,200,160,115
2022,Fall,3250,1900,750,88,85,275,200,160,115
2023,Spring,3350,2000,775,89,86,285,210,165,115
2023,Fall,3350,2000,775,89,86,285,210,165,115
2024,Spring,3500,2100,800,90,88,300,225,175,100
2024,Fall,3500,2100,800,90,88,300,225,175,100
"""

@st.cache_data
def load_data():
    df = pd.read_csv(StringIO(DATA_CSV))
    return df

df = load_data()

# ─── Sidebar filters ─────────────────────────────────────────────────────────
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Escudo_CUC.png/200px-Escudo_CUC.png", width=80)
st.sidebar.title("🎓 Filters")

years = sorted(df["Year"].unique())
selected_years = st.sidebar.multiselect("📅 Year(s)", years, default=years)

terms = df["Term"].unique().tolist()
selected_terms = st.sidebar.multiselect("📆 Term(s)", terms, default=terms)

departments = ["Engineering", "Business", "Arts", "Science"]
selected_depts = st.sidebar.multiselect("🏫 Department(s)", departments, default=departments)

st.sidebar.markdown("---")
st.sidebar.markdown("**👥 Team Members**")
for name in TEAM:
    st.sidebar.markdown(f"- {name}")
st.sidebar.markdown("---")
st.sidebar.caption("Universidad de la Costa · Data Mining")

# ─── Filter data ─────────────────────────────────────────────────────────────
filtered = df[df["Year"].isin(selected_years) & df["Term"].isin(selected_terms)]

if filtered.empty:
    st.warning("No data matches the selected filters. Please adjust your selection.")
    st.stop()

# ─── Header ──────────────────────────────────────────────────────────────────
st.title("🎓 University Student Analytics Dashboard")
st.caption("Data Mining Activity I · Universidad de la Costa")
st.markdown("---")

# ─── KPI Cards ───────────────────────────────────────────────────────────────
st.subheader("📊 Key Performance Indicators")
k1, k2, k3, k4, k5 = st.columns(5)

avg_apps    = int(filtered["Applications"].mean())
avg_enroll  = int(filtered["Enrolled"].mean())
avg_ret     = round(filtered["Retention Rate (%)"].mean(), 1)
avg_sat     = round(filtered["Student Satisfaction (%)"].mean(), 1)
admit_rate  = round((filtered["Admitted"] / filtered["Applications"]).mean() * 100, 1)

k1.metric("Avg Applications", f"{avg_apps:,}")
k2.metric("Avg Enrolled",     f"{avg_enroll:,}")
k3.metric("Avg Retention",    f"{avg_ret}%")
k4.metric("Avg Satisfaction", f"{avg_sat}%")
k5.metric("Admission Rate",   f"{admit_rate}%")

st.markdown("---")

# ─── Row 1: Line charts ───────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Retention Rate Over Time")
    ret_df = filtered.groupby("Year")["Retention Rate (%)"].mean().reset_index()
    fig1 = px.line(ret_df, x="Year", y="Retention Rate (%)",
                   markers=True, color_discrete_sequence=["#1f77b4"],
                   labels={"Retention Rate (%)": "Retention Rate (%)"})
    fig1.update_layout(height=320, margin=dict(t=20, b=30))
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("😊 Student Satisfaction by Year")
    sat_df = filtered.groupby("Year")["Student Satisfaction (%)"].mean().reset_index()
    fig2 = px.line(sat_df, x="Year", y="Student Satisfaction (%)",
                   markers=True, color_discrete_sequence=["#2ca02c"],
                   labels={"Student Satisfaction (%)": "Satisfaction (%)"})
    fig2.update_layout(height=320, margin=dict(t=20, b=30))
    st.plotly_chart(fig2, use_container_width=True)

# ─── Row 2: Bar charts ────────────────────────────────────────────────────────
col3, col4 = st.columns(2)

with col3:
    st.subheader("📊 Applications vs Enrolled by Year")
    bar_df = filtered.groupby("Year")[["Applications", "Enrolled"]].mean().reset_index()
    fig3 = px.bar(bar_df, x="Year", y=["Applications", "Enrolled"],
                  barmode="group",
                  color_discrete_sequence=["#1f77b4", "#ff7f0e"])
    fig3.update_layout(height=320, margin=dict(t=20, b=30), legend_title="Metric")
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("🌸 Spring vs Fall — Avg Enrolled")
    term_df = filtered.groupby("Term")["Enrolled"].mean().reset_index()
    fig4 = px.bar(term_df, x="Term", y="Enrolled",
                  color="Term", color_discrete_sequence=["#9467bd", "#e377c2"],
                  text_auto=True)
    fig4.update_layout(height=320, margin=dict(t=20, b=30), showlegend=False)
    st.plotly_chart(fig4, use_container_width=True)

# ─── Row 3: Department breakdown ─────────────────────────────────────────────
st.markdown("---")
st.subheader("🏫 Enrollment by Department")

dept_col_map = {
    "Engineering": "Engineering Enrolled",
    "Business":    "Business Enrolled",
    "Arts":        "Arts Enrolled",
    "Science":     "Science Enrolled",
}
selected_cols = [dept_col_map[d] for d in selected_depts if d in dept_col_map]

col5, col6 = st.columns(2)

with col5:
    if selected_cols:
        dept_trend = filtered.groupby("Year")[selected_cols].sum().reset_index()
        dept_trend_melt = dept_trend.melt("Year", var_name="Department", value_name="Enrolled")
        dept_trend_melt["Department"] = dept_trend_melt["Department"].str.replace(" Enrolled", "")
        fig5 = px.line(dept_trend_melt, x="Year", y="Enrolled", color="Department",
                       markers=True, title="Enrollment Trend by Department")
        fig5.update_layout(height=360, margin=dict(t=40, b=30))
        st.plotly_chart(fig5, use_container_width=True)

with col6:
    if selected_cols:
        totals = filtered[selected_cols].sum()
        totals.index = [c.replace(" Enrolled", "") for c in totals.index]
        fig6 = px.pie(values=totals.values, names=totals.index,
                      title="Department Share (selected period)",
                      hole=0.4, color_discrete_sequence=px.colors.qualitative.Set2)
        fig6.update_layout(height=360, margin=dict(t=40, b=30))
        st.plotly_chart(fig6, use_container_width=True)

# ─── Row 4: Satisfaction vs Retention scatter ────────────────────────────────
st.markdown("---")
st.subheader("🔍 Satisfaction vs Retention Correlation")
scatter_df = filtered.groupby("Year")[["Retention Rate (%)", "Student Satisfaction (%)"]].mean().reset_index()
fig7 = px.scatter(scatter_df, x="Retention Rate (%)", y="Student Satisfaction (%)",
                  text="Year", size_max=12,
                  trendline="ols",
                  color_discrete_sequence=["#d62728"])
fig7.update_traces(textposition="top center")
fig7.update_layout(height=350, margin=dict(t=20, b=30))
st.plotly_chart(fig7, use_container_width=True)

# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption("📌 Universidad de la Costa · Department of Computer Science and Electronics · Data Mining · Prof. José Escorcia-Gutierrez, Ph.D.")
