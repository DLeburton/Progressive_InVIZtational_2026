import os
import pandas as pd

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR   = os.path.dirname(SCRIPT_DIR)  
DATA_DIR   = os.path.join(BASE_DIR, "2026")


#Function 1: reads and cleans CSV1

def clean_miles():
    df = pd.read_csv(os.path.join(DATA_DIR, "CSV1 - RO Miles per Location 202009-202512-2022benchmark.csv"))
    df.columns = ["county_name", "waymo_miles_millions"]
    df["waymo_miles_millions"] = pd.to_numeric(df["waymo_miles_millions"], errors="coerce")
    return df

#test it in isolation
#if __name__ == "__main__":
#    df = clean_miles()
#    print(df)
#    print(df.dtypes)


#Function 2: reads and cleans CSV2

def clean_crashes():
    
    df = pd.read_csv(os.path.join(DATA_DIR, "CSV2 - Crashes with SGO ID and Group Membership 202009-202512-2022benchmark.csv"))
    
    #debug
    #print(df["Is Police-Reported"].unique())

    #rename columns and clean data types
    df.columns = [
        "sgo_report_id", "sgo_report_version", "sgo_amendment", "year_month",
        "state", "county", "road_type", "crash_type",
        "is_nhtsa_reportable", "is_nhtsa_delta_v_lt1", "is_police_reported",
        "is_any_injury_reported", "is_any_airbag_deployment", "is_ego_airbag_deployment",
        "is_suspected_serious_injury_plus", "is_any_fatal_injury",
        "incident_date", "location_description", "zip_code",
    ]
    
    bool_cols = [
        "is_nhtsa_reportable", "is_nhtsa_delta_v_lt1", "is_police_reported",
        "is_any_injury_reported", "is_any_airbag_deployment", "is_ego_airbag_deployment",
        "is_suspected_serious_injury_plus", "is_any_fatal_injury",
    ]
    for col in bool_cols:
        #df[col] = df[col].map({"True": True, "False": False})
        df[col] = df[col].astype(bool)
    
    df["incident_date"] = pd.to_datetime(df["incident_date"], errors="coerce")
    df["year_month"] = df["year_month"].astype(str)
    df["zip_code"] = df["zip_code"].astype(str).str.strip()
    
    return df


#test it in isolation
#if __name__ == "__main__":
#    df = clean_crashes()
#    print(f"Rows: {len(df)}")
#    print(f"Date range: {df['incident_date'].min().date()} → {df['incident_date'].max().date()}")
#    print(f"States: {sorted(df['state'].dropna().unique())}")
#    print(f"Police-reported: {df['is_police_reported'].sum()}")
#    print(df.dtypes)


#Function 3: reads CSV3, filters to non-Dynamic + All Crashes, returns the analysis-ready rows
#clean_ipmm(). read and column rename, 
# then apply those 3 filters. The CSV has 21 columns 

def clean_ipmm():
    df = pd.read_csv(os.path.join(DATA_DIR, "CSV3 - Collision Counts and Comparison to Benchmarks 202009-202512-2022benchmark.csv"))
    
    df.columns = [
        "outcome", "benchmark_comparison", "county_name", "grouping_type", "conflict_partner_type_group", "waymo_count", "delta_v_less_than_1_mph_percent", "waymo_ipmm", "waymo_ipmm_ci_lower", "waymo_ipmm_ci_upper", "benchmark_ipmm", "benchmark_ipmm_ci_lower", "benchmark_ipmm_ci_upper", "predicted_benchmark_count", "waymo_count_reduction", "waymo_percent_reduction", "waymo_percent_reduction_ci_lower", "waymo_percent_reduction_ci_upper", "waymo_rate_ratio", "waymo_rate_ratio_ci_lower", "waymo_rate_ratio_ci_upper"
    ]
    
    #filter to non-Dynamic + All Crashes
    df = df[df["benchmark_comparison"].str.contains("non-Dynamic")]
    df = df[(df["grouping_type"] == "All Crashes") & (df["conflict_partner_type_group"] == "All Crashes")]
    
    #add pd.to_numeric on the numeric columns 
    numeric_cols = [
        "waymo_count", "delta_v_less_than_1_mph_percent", "waymo_ipmm", "waymo_ipmm_ci_lower", "waymo_ipmm_ci_upper", "benchmark_ipmm", "benchmark_ipmm_ci_lower", "benchmark_ipmm_ci_upper", "predicted_benchmark_count", "waymo_count_reduction", "waymo_percent_reduction", "waymo_percent_reduction_ci_lower", "waymo_percent_reduction_ci_upper", "waymo_rate_ratio", "waymo_rate_ratio_ci_lower", "waymo_rate_ratio_ci_upper"
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    
    #print df.dtypes to confirm those numeric columns are float64
    #print(df.dtypes)

    return df


#test it in isolation
#call clean_ipmm() and print the row count and the unique values of benchmark_comparison and county_name
#if __name__ == "__main__":
#    df = clean_ipmm()
#    print(f"Rows: {len(df)}")
#    print(f"Benchmark Comparison: {df['benchmark_comparison'].unique()}")
#    print(f"County Name: {df['county_name'].unique()}")


#Function 4:clean_tnc_context(). 
#reads TNC_Market_Context.csv from BASE_DIR (not DATA_DIR). 
#8 rows but need to drop Fulton and DeKalb, leaving 6 clean rows.
#main challenge is the Reduction_Pct and CA_TNC_Trip_Share_Est columns 
#% and ~ symbols that need to be stripped before converting to numeric. 

def clean_tnc_context():
    df = pd.read_csv(os.path.join(BASE_DIR, "TNC_Market_Context.csv"))
    
    #drop Fulton and DeKalb
    df = df[~df["County"].isin(["Fulton", "DeKalb"])]
    
    #clean the Reduction_Pct and CA_TNC_Trip_Share_Est columns
    df.columns = [
        "county","state","waymo_miles_millions","waymo_crashes_total","waymo_police_reported","waymo_ipmm_police","benchmark_ipmm_police","reduction_pct","ca_tnc_trip_share_est", "notes"
    ]
    
    for col in ["reduction_pct", "ca_tnc_trip_share_est"]:
        df[col] = df[col].astype(str).str.replace("%", "").str.replace("~", "").str.strip()
        df[col] = pd.to_numeric(df[col], errors="coerce")
    
    #print df.dtypes to confirm those numeric columns are float64
    print(df.dtypes)

    return df


#test it in isolation
#call clean_tnc_context() and print the row count and the unique values of county and state
#if __name__ == "__main__":
#    df = clean_tnc_context()
#    print(f"Rows: {len(df)}")
#    print(f"County: {df['county'].unique()}")
#    print(f"State: {df['state'].unique()}")

#__main__ block to call all 4 functions and print the row count for each
if __name__ == "__main__":
    miles_df = clean_miles()
    print(f"Miles DataFrame Rows: {len(miles_df)}")
    
    crashes_df = clean_crashes()
    print(f"Crashes DataFrame Rows: {len(crashes_df)}")
    
    ipmm_df = clean_ipmm()
    print(f"IPMM DataFrame Rows: {len(ipmm_df)}")
    
    tnc_context_df = clean_tnc_context()
    print(f"TNC Context DataFrame Rows: {len(tnc_context_df)}")