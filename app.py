import streamlit as st
import pandas as pd
import plotly.express as px
from io import StringIO
from datetime import datetime

# ─── Constants & Configuration ────────────────────────────────────────────────
TEAM = ["Student Name 1", "Student Name 2", "Student Name 3", "Student Name 4"]

# Chart configuration
CHART_CONFIG = {
    "line_height": 320,
    "bar_height": 320,
    "dept_height": 360,
    "scatter_height": 350,
    "margin": dict(t=20, b=30),
    "dept_margin": dict(t=40, b=30),
}

# Color scheme
COLORS = {
    "retention": "#1f77b4",
    "satisfaction": "#2ca02c",
    "applications": "#1f77b4",
    "enrolled": "#ff7f0e",
    "spring": "#9467bd",
    "fall": "#e377c2",
    "correlation": "#d62728",
}

# Required columns for validation
REQUIRED_COLUMNS = [
    "Year", "Term", "Applications", "Admitted", "Enrolled",
    "Retention Rate (%)", "Student Satisfaction (%)",
    "Engineering Enrolled", "Business Enrolled", "Arts Enrolled", "Science Enrolled"
]

DEPARTMENT_COLUMNS = {
    "Engineering": "Engineering Enrolled",
    "Business": "Business Enrolled",
    "Arts": "Arts Enrolled",
    "Science": "Science Enrolled",
}

# Data
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

#Page Config
st.set_page_config(
    page_title="University Student Dashboard",
    page_icon="🎓",
    layout="wide",
)

#Data Loading & Validation
@st.cache_data
def load_data():
    """
    Load and validate university enrollment data from CSV.
    
    Returns:
        pd.DataFrame: Validated enrollment data
        
    Raises:
        ValueError: If data is empty or missing required columns
    """
    try:
        df = pd.read_csv(StringIO(DATA_CSV))
        
        # Validate data is not empty
        if df.empty:
            raise ValueError("No data loaded from CSV")
        
        # Validate required columns exist
        missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {', '.join(missing_cols)}")
        
        # Convert Year to integer for proper sorting
        df["Year"] = df["Year"].astype(int)
        
        return df
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        st.stop()


df = load_data()

#Sidebar Configuration
st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Escudo_CUC.png/200px-Escudo_CUC.png",
    width=80
)
st.sidebar.title("🎓 Filters")

# Year filter
years = sorted(df["Year"].unique())
selected_years = st.sidebar.multiselect(
    "Year(s)",
    years,
    default=years,
    help="Select one or more years to display"
)

# Term filter
terms = sorted(df["Term"].unique())
selected_terms = st.sidebar.multiselect(
    "Term(s)",
    terms,
    default=terms,
    help="Select Spring, Fall, or both"
)

# Department filter
selected_depts = st.sidebar.multiselect(
    "Department(s)",
    list(DEPARTMENT_COLUMNS.keys()),
    default=list(DEPARTMENT_COLUMNS.keys()),
    help="Select departments to analyze"
)

# Sidebar info
st.sidebar.markdown("---")
st.sidebar.markdown("**👥 Team Members**")
for name in TEAM:
    st.sidebar.markdown(f"- {name}")
st.sidebar.markdown("---")
st.sidebar.caption("Universidad de la Costa · Data Mining")

#Data Filtering & Validation
if not selected_years or not selected_terms:
    st.warning("⚠️ Please select at least one year and term in the filters.")
    st.stop()

filtered = df[
    (df["Year"].isin(selected_years)) & 
    (df["Term"].isin(selected_terms))
]

if filtered.empty:
    st.warning(
        "⚠️ No data matches the selected filters. Please adjust your selection."
    )
    st.stop()

#Helper Functions for Charts
def create_line_chart(data, x, y, color, title, height=320):
    """
    Create a standardized line chart with markers.
    
    Args:
        data: DataFrame with data to plot
        x: Column name for x-axis
        y: Column name for y-axis
        color: Hex color code
        title: Chart title
        height: Chart height in pixels
        
    Returns:
        plotly.graph_objects.Figure: Configured line chart
    """
    fig = px.line(
        data,
        x=x,
        y=y,
        markers=True,
        color_discrete_sequence=[color],
        title=title
    )
    fig.update_layout(height=height, margin=CHART_CONFIG["margin"])
    return fig


def create_bar_chart(data, x, y, color=None, height=320, barmode="group", **kwargs):
    """
    Create a standardized bar chart.
    
    Args:
        data: DataFrame with data to plot
        x: Column name for x-axis
        y: Column name(s) for y-axis
        color: Column to color by (optional)
        height: Chart height in pixels
        barmode: "group" or "stack"
        **kwargs: Additional plotly express parameters
        
    Returns:
        plotly.graph_objects.Figure: Configured bar chart
    """
    fig = px.bar(data, x=x, y=y, color=color, barmode=barmode, **kwargs)
    fig.update_layout(height=height, margin=CHART_CONFIG["margin"])
    return fig


def create_scatter_chart(data, x, y, title, height=350):
    """
    Create a scatter plot with OLS trendline.
    
    Args:
        data: DataFrame with data to plot
        x: Column name for x-axis
        y: Column name for y-axis
        title: Chart title
        height: Chart height in pixels
        
    Returns:
        plotly.graph_objects.Figure: Configured scatter chart
    """
    fig = px.scatter(
        data,
        x=x,
        y=y,
        text="Year",
        trendline="ols",
        size_max=12,
        color_discrete_sequence=[COLORS["correlation"]],
        title=title
    )
    fig.update_traces(textposition="top center")
    fig.update_layout(height=height, margin=CHART_CONFIG["margin"])
    return fig


#Calculate KPIs
@st.cache_data
def calculate_kpis(data):
    """
    Calculate key performance indicators from filtered data.
    
    Args:
        data: Filtered DataFrame
        
    Returns:
        dict: Dictionary with KPI values
    """
    return {
        "avg_applications": int(data["Applications"].mean()),
        "avg_enrolled": int(data["Enrolled"].mean()),
        "avg_retention": round(data["Retention Rate (%)"].mean(), 1),
        "avg_satisfaction": round(data["Student Satisfaction (%)"].mean(), 1),
        "admission_rate": round((data["Admitted"] / data["Applications"]).mean() * 100, 1),
    }


#Header
st.title("🎓 University Student Analytics Dashboard")
st.caption("Data Mining Activity I · Universidad de la Costa")
st.markdown("---")

#KPI Cards
st.subheader("Key Performance Indicators")

kpis = calculate_kpis(filtered)

k1, k2, k3, k4, k5 = st.columns(5)

k1.metric("Avg Applications", f"{kpis['avg_applications']:,}")
k2.metric("Avg Enrolled", f"{kpis['avg_enrolled']:,}")
k3.metric("Avg Retention", f"{kpis['avg_retention']}%")
k4.metric("Avg Satisfaction", f"{kpis['avg_satisfaction']}%")
k5.metric("Admission Rate", f"{kpis['admission_rate']}%")

st.markdown("---")

#Line Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Retention Rate Over Time")
    ret_df = filtered.groupby("Year")["Retention Rate (%)"].mean().reset_index()
    fig1 = create_line_chart(
        ret_df,
        x="Year",
        y="Retention Rate (%)",
        color=COLORS["retention"],
        title="",
        height=CHART_CONFIG["line_height"]
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Student Satisfaction by Year")
    sat_df = filtered.groupby("Year")["Student Satisfaction (%)"].mean().reset_index()
    fig2 = create_line_chart(
        sat_df,
        x="Year",
        y="Student Satisfaction (%)",
        color=COLORS["satisfaction"],
        title="",
        height=CHART_CONFIG["line_height"]
    )
    st.plotly_chart(fig2, use_container_width=True)

#Bar Charts
col3, col4 = st.columns(2)

with col3:
    st.subheader("Applications vs Enrolled by Year")
    bar_df = filtered.groupby("Year")[["Applications", "Enrolled"]].mean().reset_index()
    fig3 = create_bar_chart(
        bar_df,
        x="Year",
        y=["Applications", "Enrolled"],
        color_discrete_sequence=[COLORS["applications"], COLORS["enrolled"]],
        height=CHART_CONFIG["bar_height"]
    )
    fig3.update_layout(legend_title="Metric")
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("Spring vs Fall — Avg Enrolled")
    term_df = filtered.groupby("Term")["Enrolled"].mean().reset_index()
    fig4 = create_bar_chart(
        term_df,
        x="Term",
        y="Enrolled",
        color="Term",
        color_discrete_sequence=[COLORS["spring"], COLORS["fall"]],
        height=CHART_CONFIG["bar_height"]
    )
    fig4.update_layout(showlegend=False)
    fig4.update_traces(text=fig4.data[0].y.round(0), textposition='auto', texttemplate='%{text}')
    st.plotly_chart(fig4, use_container_width=True)

#Department Breakdown
st.markdown("---")
st.subheader("Enrollment by Department")

selected_cols = [
    DEPARTMENT_COLUMNS[dept]
    for dept in selected_depts
    if dept in DEPARTMENT_COLUMNS
]

col5, col6 = st.columns(2)

with col5:
    if selected_cols:
        st.subheader("Enrollment Trend by Department", divider=False)
        dept_trend = filtered.groupby("Year")[selected_cols].sum().reset_index()
        dept_trend_melt = dept_trend.melt(
            "Year",
            var_name="Department",
            value_name="Enrolled"
        )
        dept_trend_melt["Department"] = dept_trend_melt["Department"].str.replace(
            " Enrolled",
            ""
        )
        fig5 = px.line(
            dept_trend_melt,
            x="Year",
            y="Enrolled",
            color="Department",
            markers=True
        )
        fig5.update_layout(height=CHART_CONFIG["dept_height"], margin=CHART_CONFIG["dept_margin"])
        st.plotly_chart(fig5, use_container_width=True)
    else:
        st.info("Select at least one department to view enrollment trends.")

with col6:
    if selected_cols:
        st.subheader("Department Share (Selected Period)", divider=False)
        totals = filtered[selected_cols].sum()
        totals.index = [col.replace(" Enrolled", "") for col in totals.index]
        fig6 = px.pie(
            values=totals.values,
            names=totals.index,
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig6.update_layout(height=CHART_CONFIG["dept_height"], margin=CHART_CONFIG["dept_margin"])
        st.plotly_chart(fig6, use_container_width=True)
    else:
        st.info("Select at least one department to view enrollment distribution.")

#Correlation Analysis
st.markdown("---")
st.subheader("Satisfaction vs Retention Correlation")

scatter_df = filtered.groupby("Year")[
    ["Retention Rate (%)", "Student Satisfaction (%)"]
].mean().reset_index()

fig7 = create_scatter_chart(
    scatter_df,
    x="Retention Rate (%)",
    y="Student Satisfaction (%)",
    title="",
    height=CHART_CONFIG["scatter_height"]
)
st.plotly_chart(fig7, use_container_width=True)

#Data Export Section
st.markdown("---")
st.subheader("Export Data")

col_exp1, col_exp2 = st.columns(2)

with col_exp1:
    # Export filtered data as CSV
    csv = filtered.to_csv(index=False)
    st.download_button(
        label="Download Filtered Data (CSV)",
        data=csv,
        file_name=f"university_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        help="Download the filtered dataset in CSV format"
    )

with col_exp2:
    # Export summary statistics
    summary_stats = {
        "Metric": ["Avg Applications", "Avg Enrolled", "Avg Retention %", 
                   "Avg Satisfaction %", "Admission Rate %"],
        "Value": [
            kpis['avg_applications'],
            kpis['avg_enrolled'],
            kpis['avg_retention'],
            kpis['avg_satisfaction'],
            kpis['admission_rate']
        ]
    }
    summary_df = pd.DataFrame(summary_stats)
    csv_summary = summary_df.to_csv(index=False)
    st.download_button(
        label="Download Summary Stats (CSV)",
        data=csv_summary,
        file_name=f"summary_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        help="Download summary statistics in CSV format"
    )
