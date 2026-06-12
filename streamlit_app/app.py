import streamlit as st
import pandas as pd
import sqlite3
import os
import plotly.express as px


st.set_page_config(page_title="Progressive InVIZtational 2026", layout="wide")

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
page = st.sidebar.radio("Navigation", ["Overview", "Safety Gap", "County Deep Dive", "Crash Profile", "The Scale Question"])    

#4 pages: Overview - show the miles_df with st.dataframe and a brief description of the data
if page == "Overview":

    #3 side by side, use st.columns(3) to create 3 columns first, 
    # then place one metric in each hardcode the values directly
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Miles", "170.7M")
    with col2:
        st.metric("Total Crashes", "1,390")
    with col3:
        st.metric("Police-Reported", "282")

    st.title("Overview")
    st.write("This dashboard presents an analysis of Waymo's safety performance in relation to its miles driven, crash data, and context of operations. The data is sourced from Waymo's 2022 benchmark report, which includes detailed information on miles driven, crashes, and various contextual factors.")
    #st.subheader("Miles Driven Data")
    #st.dataframe(miles_df)
    #st.write("The 'Miles Driven Data' table shows the total miles driven by Waymo in millions, broken down by county. This data is crucial for understanding the scale of Waymo's operations and serves as a baseline for analyzing safety performance in relation to miles driven.")   

elif page == "Safety Gap":  
    st.title("Safety Gap Analysis")
    st.write("In this section, we analyze the safety gap between Waymo's performance and the benchmark. The safety gap is calculated as the difference in crash rates between Waymo and the benchmark, normalized by miles driven. A positive safety gap indicates that Waymo has a higher crash rate than the benchmark, while a negative safety gap indicates that Waymo has a lower crash rate than the benchmark.")
    
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
    fig = px.bar(
        ipmm_df_filtered,
        x="benchmark_comparison",
        y=["waymo_ipmm", "benchmark_ipmm"],
        barmode="group",
        labels={"benchmark_comparison": "Benchmark Comparison", "value": "IPMM"},
        title="Waymo IPMM vs Benchmark IPMM"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.write("The 'Safety Gap Data' table shows the crash rates for Waymo and the benchmark, along with the calculated safety gap. This data allows us to assess how Waymo's safety performance compares to the benchmark and identify areas for improvement.")     

elif page == "County Deep Dive":
    st.title("County Deep Dive")
    st.write("This section provides a detailed analysis of Waymo's safety performance at the county level. We examine the crash data for each county, including the types of crashes, severity, and contributing factors. This analysis helps us understand the specific challenges and opportunities for improving safety in different operational contexts.")
    st.subheader("County Crash Data")
    #st.dataframe(crashes_df)
    #st.write("The 'County Crash Data' table shows detailed information about crashes that occurred in each county, including the type of crash, severity, and contributing factors. This data allows us to identify patterns and trends in crash occurrences across different counties.")

    #bar chart comparing waymo_ipmm_police vs benchmark_ipmm_police for each county
    fig = px.bar(
        tnc_context_df,
        x="county",
        y=["waymo_ipmm_police", "benchmark_ipmm_police"],
        barmode="group",
        labels={"county": "County", "value": "IPMM (Police-Reported)"},
        title="Waymo IPMM (Police-Reported) vs Benchmark IPMM (Police-Reported) by County"
    )
    st.plotly_chart(fig, use_container_width=True)  
    

elif page == "Crash Profile":
    st.title("Crash Profile")
    st.write("In this section, we profile the crashes that occurred during Waymo's operations. We analyze the types of crashes, their severity, and the circumstances under which they occurred. This profiling helps us understand the nature of crashes and identify potential areas for safety improvements.")
    st.subheader("Crash Profile Data")
    #st.dataframe(crashes_df)
    #st.write("The 'Crash Profile Data' table provides detailed information about each crash, including the type of crash, severity, and contributing factors. This data allows us to create a comprehensive profile of crashes and identify common characteristics that may inform safety strategies.") 

    #pie/donut chart showing the distribution of crash types in crashes_df
    crash_type_counts = crashes_df['crash_type'].value_counts().reset_index()
    crash_type_counts.columns = ['crash_type', 'count']
    fig = px.pie(
        crash_type_counts,
        names='crash_type',
        values='count',
        title="Distribution of Crash Types"
    )
    st.plotly_chart(fig, use_container_width=True)

elif page == "The Scale Question":
    st.title("The Scale Question")
    st.write("This section addresses the question of scale in relation to Waymo's safety performance. We analyze how the scale of Waymo's operations, as measured by miles driven, impacts its safety performance. We also explore the implications of scaling up operations for safety and identify potential strategies for managing safety at scale.")
    st.subheader("Scale and Safety Data")
    #st.dataframe(miles_df)
    #st.dataframe(ipmm_df)
    #st.write("The 'Scale and Safety Data' tables show the relationship between miles driven and safety performance. By analyzing these tables, we can assess how scaling up operations may impact safety and identify strategies for managing safety as operations grow.")

    #3 KPI cards side by side: CA TNC Annual Miles — 3.5B, Crashes at Human Rate — 20,650/yr,Crashes at Waymo Rate — 5,600/yr
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("CA TNC Annual Miles", "3.5B")
    with col2:
        st.metric("Crashes at Human Rate", "20,650/yr")
    with col3:
        st.metric("Crashes at Waymo Rate", "5,600/yr")  

    #KPI card full width, Projected Fewer Crashes/Year: ~10,100,wrap it in a single column that spans the full width, px.bar()
        
    st.markdown("### Projected Fewer Crashes/Year")
    st.markdown("# ~10,100")    
    fig = px.bar(
        x=["Crashes at Human Rate", "Crashes at Waymo Rate"],
        y=[20650, 5600],
        labels={"x": "Scenario", "y": "Annual Crashes"},
        title="Projected Annual Crashes: Human Rate vs Waymo Rate"
    )
    st.plotly_chart(fig, use_container_width=True)  