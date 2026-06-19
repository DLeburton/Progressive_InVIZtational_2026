import streamlit as st
import pandas as pd
import sqlite3
import os
import plotly.express as px
import streamlit.components.v1 as components
import numpy as np


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
page = st.sidebar.radio("Navigation", ["Overview", "Safety Gap", "County Deep Dive", "Crash Profile", "The Scale Question", "Safety Trend", "Behind the Dashboard"])  

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
    st.markdown("<p style='font-size: 21px;'>Waymo has logged 170.7 million rider-only miles across five U.S. markets since September 2020— and in that time, reported 1,390 crashes. That number sounds large until you compare it to the rate. This dashboard explores what Waymo's safety record actually looks like, what it means relative to human TNC drivers, and why it matters for the future of ride-share insurance.</p>", unsafe_allow_html=True)
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

    #chart
    crash_type_counts = crashes_df['crash_type'].value_counts().reset_index()
    crash_type_counts.columns = ['crash_type', 'count']
    
    #change crash type naming
    label_map = {
    'V2V F2R':          'Rear-End',
    'V2V Lateral':      'Sideswipe',
    'V2V Backing':      'Backing',
    'V2V Head-on':      'Head-On',
    'V2V Intersection': 'Intersection',
    'Single Vehicle':   'Single Vehicle',
    'Secondary Crash':  'Secondary Crash',
    'All Others':       'All Others',
    'Motorcycle':       'Motorcycle Involved',
    'Cyclist':          'Cyclist Involved',
    'Pedestrian':       'Pedestrian Involved'
    }

    crash_type_counts['crash_type'] = crash_type_counts['crash_type'].map(label_map)
    crash_type_counts = crash_type_counts.sort_values('count', ascending=True)

    crash_type_counts = crash_type_counts.sort_values('count', ascending=True)

    fig = px.bar(
        crash_type_counts,
        x='count',
        y='crash_type',
        orientation='h',
        title="Distribution of Crash Types",
        labels={'count': 'Number of Crashes', 'crash_type': ''},
        color_discrete_sequence=['#00B4D8']
    )
    fig.update_traces(hovertemplate='<b>%{y}</b><br>Count: %{x}<extra></extra>')
    fig.update_layout(height=420)
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

#add page, CUSUM analysis

elif page == "Safety Trend":

    st.markdown("<h1 style='text-align: center; font-size: 52px;'>Safety Trend Analysis</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 21px;'>CUSUM (Cumulative Sum) analysis tests whether Waymo's crash injury rate shifted at any detectable point as the fleet scaled. Parameters: c = 0 to prioritize early detection— appropriate when delayed detection carries higher cost than a false positive.</p>", unsafe_allow_html=True)

    st.markdown("""
    <div style='background-color: #1F3347; border-left: 4px solid #00B4D8; padding: 16px 20px; border-radius: 6px; margin-bottom: 16px;'>
    <p style='font-size: 16px; color: #F0F4F8; margin: 0;'>
    <strong>How to read this: CUSUM works like a running scorecard. Each month Waymo's injury rate falls below the baseline average, points accumulate on the green line. When that line crosses the red dashed threshold, the improvement is statistically noticeable. The chart below shows the green line crossing in September 2024, signaling a genuine shift in Waymo's crash severity profile.
    </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<p style='font-size: 16px; color: #94A3B8;'>The formula behind the chart:</p>", unsafe_allow_html=True)

    st.latex(r"S_t = \max(0,\ S_{t-1} + (X_t - \mu - c))")

    #formula
    st.markdown("""
    <p style='font-size: 15px; color: #94A3B8; text-align: center;'>
    <strong style='color:#F0F4F8;'>X<sub>t</sub></strong> is the observed injury rate in month t &nbsp;·&nbsp; 
    <strong style='color:#F0F4F8;'>μ</strong> is the baseline mean (9.4%) &nbsp;·&nbsp; 
    <strong style='color:#F0F4F8;'>c = 0</strong> means maximum sensitivity<br>
    The statistic resets to zero when the rate rises above baseline, so only sustained improvements build toward a signal.
    </p>
    """, unsafe_allow_html=True)

    # Build monthly series from crashes_df
    cusum_df = crashes_df.groupby('year_month').agg(
        total=('sgo_report_id', 'count'),
        injuries=('is_any_injury_reported', 'sum')
    ).reset_index()
    cusum_df['injury_rate'] = cusum_df['injuries'] / cusum_df['total']
    cusum_df = cusum_df[cusum_df['total'] >= 20].reset_index(drop=True)
    cusum_df['date_label'] = pd.to_datetime(
        cusum_df['year_month'].astype(str), format='%Y%m'
    ).dt.strftime('%b %Y')

    # CUSUM parameters
    mu0   = cusum_df['injury_rate'].mean()
    sigma = cusum_df['injury_rate'].std()
    k     = 0.0
    h     = 3.0 * sigma

    # Compute two-sided CUSUM
    n = len(cusum_df)
    C_upper = np.zeros(n)
    C_lower = np.zeros(n)
    for i in range(1, n):
        x = cusum_df['injury_rate'].iloc[i]
        C_upper[i] = max(0, C_upper[i-1] + (x - mu0 - k))
        C_lower[i] = max(0, C_lower[i-1] + (mu0 - x - k))

    cusum_df['cusum_upper'] = C_upper
    cusum_df['cusum_lower'] = C_lower

    # Chart 1: Monthly injury rate
    fig1 = px.bar(
        cusum_df,
        x='date_label',
        y='injury_rate',
        title='Monthly Crash Injury Rate (months with n ≥ 20)',
        labels={'date_label': 'Month', 'injury_rate': 'Injury Rate'},
        color_discrete_sequence=['#00B4D8']
    )
    fig1.add_hline(
        y=mu0, line_dash='dash', line_color='#94A3B8',
        annotation_text=f'Baseline mean: {mu0:.1%}',
        annotation_position='top right'
    )
    fig1.update_traces(
        hovertemplate='<b>%{x}</b><br>Injury Rate: %{y:.1%}<extra></extra>'
    )
    fig1.update_layout(xaxis_tickangle=-45, height=380)
    st.plotly_chart(fig1, use_container_width=True)

    # Chart 2: CUSUM lower statistic
    fig2 = px.line(
        cusum_df,
        x='date_label',
        y='cusum_lower',
        title='CUSUM Lower Statistic — Detecting Safety Improvement',
        labels={'date_label': 'Month', 'cusum_lower': 'CUSUM Statistic'},
        color_discrete_sequence=['#3fb950']
    )
    fig2.add_hline(
        y=h, line_dash='dash', line_color='#f85149',
        annotation_text=f'Detection threshold (3σ = {h:.3f})',
        annotation_position='top right'
    )
    signal_rows = cusum_df[cusum_df['cusum_lower'] >= h]
    if not signal_rows.empty:
        signal_idx = signal_rows.index[0]
        fig2.add_annotation(
            x=cusum_df.loc[signal_idx, 'date_label'],
            y=cusum_df.loc[signal_idx, 'cusum_lower'],
            text="First signal: Sep 2024",
            showarrow=True,
            arrowhead=2,
            arrowcolor='#00B4D8',
            font=dict(color='#00B4D8', size=12),
            ax=40, ay=-40
        )
    fig2.update_traces(
        hovertemplate='<b>%{x}</b><br>CUSUM: %{y:.4f}<extra></extra>'
    )
    fig2.update_layout(xaxis_tickangle=-45, height=380)
    st.plotly_chart(fig2, use_container_width=True)

    # Finding callout
    st.divider()
    st.markdown("<h3 style='text-align: center;'>What CUSUM Found</h3>", unsafe_allow_html=True)

    
    st.markdown("""
    <div style='background-color: #1F3347; border-left: 4px solid #3fb950; padding: 16px 20px; border-radius: 6px; margin: 16px 0;'>
    <p style='font-size: 18px; color: #F0F4F8; margin: 0;'>
    <strong>Bottom line:</strong> Starting in September 2024, when Waymo got into a crash, 
    it was less likely to result in an injury. That pattern was consistent enough over the following 
    months to be statistically detectable. A late signal in November and December 2025 
    suggests the injury rate may be ticking back up, which is worth watching.
    </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("First Improvement Signal", "Sep 2024")
        st.markdown("<p style='font-size: 16px; color: #94A3B8;'>A statistically significant downward shift in crash injury rate— consistent with a system maturation event in Waymo's AV platform.</p>", unsafe_allow_html=True)
    with col2:
        st.metric("Late 2025 Signal", "Nov–Dec 2025 ↑")
        st.markdown("<p style='font-size: 16px; color: #94A3B8;'>An early upward signal in late 2025 suggests the injury rate may be trending back toward baseline. Continued monitoring warranted.</p>", unsafe_allow_html=True)

    st.markdown(
        "<p style='font-size: 13px; color: #94A3B8; text-align: center;'>"
        "<em>Parameters: c = 0 (prioritizes early detection; appropriate when delayed detection cost "
        "exceeds false positive cost), threshold h = 3σ. Methodology: Sokol, J.,Georgia Tech MSA. "
        "Only months with n ≥ 20 crash reports included.</em></p>",
        unsafe_allow_html=True
    )

#closing page

elif page == "Behind the Dashboard":
    st.markdown("<h1 style='text-align: center; font-size: 52px;'>Behind the Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 21px;'>This project is built on a fully reproducible data pipeline— raw Waymo safety CSVs cleaned with Python, loaded into SQLite, and served through a live Streamlit app deployed on Streamlit Cloud.</p>", unsafe_allow_html=True)
    img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_pipeline.png")
    st.image(img_path, use_container_width=True)
    st.markdown("<p style='font-size: 16px; color: #94A3B8;'><strong>clean_data.py</strong>: reads and standardizes raw Waymo CSVs into consistent dataframes<br><strong>load_db.py</strong>: loads cleaned data into a local SQLite database<br><strong>app.py</strong>: queries the database and renders all seven interactive pages</p>", unsafe_allow_html=True)