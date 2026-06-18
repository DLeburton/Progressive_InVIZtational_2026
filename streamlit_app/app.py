import streamlit as st
import pandas as pd
import sqlite3
import os
import plotly.express as px
import streamlit.components.v1 as components


st.set_page_config(page_title="Progressive InVIZtational 2026", layout="wide")

#CSS block for navigation panel
st.markdown("""
<style>
[data-testid="stSidebar"] [data-testid="stRadio"] label > div:first-child {
    display: none !important;
    width: 0 !important;
    height: 0 !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label {
    color: #F0F4F8;
    font-size: 15px;
    padding: 8px 12px;
    border-radius: 6px;
    display: flex;
    cursor: pointer;
    gap: 0;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background-color: #1F3347;
}
</style>
""", unsafe_allow_html=True)

#connects to waymo_tnc.db and loads each table into a DataFrame
@st.cache_data
def load_data():    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DB_PATH = os.path.join(BASE_DIR, "waymo_tnc.db")
    comm = sqlite3.connect(DB_PATH)
    miles_df = pd.read_sql_query("SELECT * FROM cleaned_miles", comm)
    crashes_df = pd.read_sql_query("SELECT * FROM cleaned_crashes", comm)
    ipmm_df = pd.read_sql_query("SELECT * FROM cleaned_ipmm", comm)
    tnc_context_df = pd.read_sql_query("SELECT * FROM cleaned_tnc_context", comm)
    comm.close()
    return miles_df, crashes_df, ipmm_df, tnc_context_df


#Call load_data() and unpack the 4 DataFrames into variables
miles_df, crashes_df, ipmm_df, tnc_context_df = load_data()

#Add a sidebar with st.sidebar and st.selectbox to select which DataFrame to display
#st.sidebar.radio("label", [list of options])
page = st.sidebar.radio("Navigation", ["Overview", "Safety Gap", "County Deep Dive", "Crash Profile", "The Scale Question", "Behind the Dashboard"])  

#4 pages: Overview - show the miles_df with st.dataframe and a brief description of the data
if page == "Overview":

    #3 side by side, use st.columns(3) to create 3 columns first, 
    # then place one metric in each hardcode the values directly

    
    st.markdown("""
    <style>
    [data-testid="stMetric"] {
        border: 1px solid #00B4D8;
        border-radius: 8px;
        padding: 16px;
        text-align: center;
    }
    [data-testid="stMetricLabel"] {
        justify-content: center;
    }
    [data-testid="stMetricValue"] {
        justify-content: center;
    }
    </style>
    """, unsafe_allow_html=True)

    #animation
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "road_intro.html"), "r") as f:
        road_html = f.read()
    components.html(road_html, height=600, scrolling=False)

    st.markdown("<h1 style='text-align: center; font-size: 52px;'>Overview</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 21px;'>Waymo has logged 170.7 million rider-only miles across five U.S. markets since September 2020 — and in that time, reported 1,390 crashes. That number sounds large until you compare it to the rate. This dashboard explores what Waymo's safety record actually looks like, what it means relative to human TNC drivers, and why it matters for the future of ride-share insurance.</p>", unsafe_allow_html=True)
    #st.subheader("Miles Driven Data")
    #st.dataframe(miles_df)
    #st.write("The 'Miles Driven Data' table shows the total miles driven by Waymo in millions, broken down by county. This data is crucial for understanding the scale of Waymo's operations and serves as a baseline for analyzing safety performance in relation to miles driven.")   
    #st.image("streamlit_app/road_scene.png", use_container_width=True)
    img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "road_scene.png")

    

    st.image(img_path, use_container_width=True)

elif page == "Safety Gap":  
    st.title("Safety Gap Analysis")
    #st.write("In this section, we analyze the safety gap between Waymo's performance and the benchmark. The safety gap is calculated as the difference in crash rates between Waymo and the benchmark, normalized by miles driven. A positive safety gap indicates that Waymo has a higher crash rate than the benchmark, while a negative safety gap indicates that Waymo has a lower crash rate than the benchmark.")
    st.markdown("<p style='font-size: 21px;'>Waymo produces 65–90% fewer crashes per million miles than human TNC drivers across every outcome category. Waymo's incident rate (IPMM) plotted against the non-dynamic human driver benchmark.</p>", unsafe_allow_html=True)

    #Filter ipmm_df to rows where county_name == "All Locations (mileage blended)"
    ipmm_df_filtered = ipmm_df[ipmm_df['county_name'] == "All Locations (mileage blended)"]
    
    st.subheader("Safety Gap Data")

    #remove the st.dataframe() and replace it with a chart
    #st.dataframe(ipmm_df_filtered)
    #st.bar_chart(ipmm_df_filtered[["waymo_ipmm", "benchmark_ipmm"]].set_index(ipmm_df_filtered["benchmark_comparison"]))
    
    #create the chart. px.bar() needs:
    # data_frame — your filtered DataFrame
    # x — the outcome column
    # y — a list of both IPMM columns
    # barmode — set to "group" for side-by-side bars
    # Then display it with st.plotly_chart().
    
       
    #hover plotly bar
    fig = px.bar(
        ipmm_df_filtered,
        x="benchmark_comparison",
        y=["waymo_ipmm", "benchmark_ipmm"],
        barmode="group",
        labels={
            "benchmark_comparison": "Outcome",
            "value": "IPMM",
            "variable": "Driver Type"
        },
        title="Waymo IPMM vs Benchmark IPMM",
        color_discrete_map={"waymo_ipmm": "#00B4D8", "benchmark_ipmm": "#94A3B8"}
    )

    fig.for_each_trace(lambda t: t.update(
        name="Waymo" if t.name == "waymo_ipmm" else "Human Benchmark",
        hovertemplate="<b>%{x}</b><br>IPMM: %{y:.3f}<extra>%{fullData.name}</extra>"
    ))

    fig.update_layout(xaxis_tickangle=-35)

    st.plotly_chart(fig, use_container_width=True)
  
    
   
elif page == "County Deep Dive":
    st.title("County Deep Dive")
    st.markdown("<p style='font-size: 21px;'>The safety advantage holds at the local level. Police-reported IPMM by county, comparing Waymo's rate against the human TNC benchmark in each market. San Francisco, Los Angeles, Phoenix, Austin, and Atlanta all tell the same story.</p>", unsafe_allow_html=True)
    
    fig = px.bar(
        tnc_context_df,
        x="county",
        y=["waymo_ipmm_police", "benchmark_ipmm_police"],
        barmode="group",
        labels={
            "county": "County",
            "value": "IPMM (Police-Reported)",
            "variable": "Driver Type"
        },
        title="Waymo vs Human Benchmark — Police-Reported IPMM by County",
        color_discrete_map={"waymo_ipmm_police": "#00B4D8", "benchmark_ipmm_police": "#94A3B8"}
    )

    fig.for_each_trace(lambda t: t.update(
        name="Waymo" if t.name == "waymo_ipmm_police" else "Human Benchmark",
        hovertemplate="<b>%{x}</b><br>IPMM: %{y:.3f}<extra>%{fullData.name}</extra>"
    ))

    fig.update_layout(xaxis_tickangle=0)

    st.plotly_chart(fig, use_container_width=True)
    

elif page == "Crash Profile":
    st.title("Crash Profile")
    st.markdown("<p style='font-size: 21px;'>Not all crashes are equal. This page breaks down Waymo's 1,390 reported incidents by crash type— showing what kinds of contact actually occur, how often they result in injury, and how rarely they involve serious outcomes. The profile reflects a vehicle that crashes differently than a human driver.</p>", unsafe_allow_html=True)

    crash_type_counts = crashes_df['crash_type'].value_counts().reset_index()
    crash_type_counts.columns = ['crash_type', 'count']
    
    fig = px.pie(
        crash_type_counts,
        names='crash_type',
        values='count',
        title="Distribution of Crash Types",
        color_discrete_sequence=["#00B4D8", "#94A3B8", "#1F3347", "#0D7A94", "#F0F4F8"]
    )

    fig.update_traces(
        hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Share: %{percent}<extra></extra>"
    )
    fig.update_layout(
        height=800
    )

    st.plotly_chart(fig, use_container_width=True)


elif page == "The Scale Question":
    st.title("The Scale Question")
    st.markdown("<p style='font-size: 21px;'>Waymo currently operates at a fraction of TNC market scale. In California alone, the TNC market generates roughly 3.5 billion miles per year. If Waymo's crash rate were applied at that scale instead of the human rate, the math suggests approximately 15,000 fewer crashes annually.</p>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("CA TNC Annual Miles", "3.5B")
    with col2:
        st.metric("Crashes at Human Rate", "20,650/yr")
    with col3:
        st.metric("Crashes at Waymo Rate", "5,600/yr")
    with col4:
        st.metric("Projected Fewer Crashes/Year", "~15,050")

    #st.markdown("### Projected Fewer Crashes/Year")
    #st.markdown("# ~15,050")

    fig = px.bar(
        x=["Human Rate", "Waymo Rate"],
        y=[20650, 5600],
        labels={"x": "Scenario", "y": "Annual Crashes"},
        title="Projected Annual Crashes: Human Rate vs Waymo Rate",
        color=["Human Rate", "Waymo Rate"],
        color_discrete_map={"Human Rate": "#94A3B8", "Waymo Rate": "#00B4D8"}
    )

    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>Projected Crashes: %{y:,}<extra></extra>"
    )

    fig.update_layout(
        showlegend=False,
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.markdown("<h3 style='text-align: center;'>What This Means for Progressive</h3>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 21px; text-align: center;'>Progressive has written 1.5 million TNC policies and generated $1.5 billion in TNC premium over the last 10 years. As autonomous vehicles enter the same permit class, the question isn't whether this affects our book— it's how we model it.</p>", unsafe_allow_html=True)

    
    st.markdown("<p style='font-size: 13px; color: #94A3B8; text-align: center;'><em>Source: California Air Resources Board, Clean Miles Standard (2021). CA TNC VMT estimated at 4.3B miles/year (2018); analysis uses 3.5B as conservative baseline.</em></p>", unsafe_allow_html=True)

elif page == "Behind the Dashboard":
    st.markdown("<h1 style='text-align: center; font-size: 52px;'>Behind the Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 21px;'>This project is built on a fully reproducible data pipeline— raw Waymo safety CSVs cleaned with Python, loaded into SQLite, and served through a live Streamlit app deployed on Streamlit Cloud.</p>", unsafe_allow_html=True)
    img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_pipeline.png")
    st.image(img_path, use_container_width=True)
    st.markdown("<p style='font-size: 16px; color: #94A3B8;'><strong>clean_data.py</strong>: reads and standardizes raw Waymo CSVs into consistent dataframes<br><strong>load_db.py</strong>: loads cleaned data into a local SQLite database<br><strong>app.py</strong>: queries the database and renders all five interactive pages</p>", unsafe_allow_html=True)