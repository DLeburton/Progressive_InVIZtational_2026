import sqlite3
import os


#Load 4 functions from clean_data.py
from clean_data import BASE_DIR, clean_miles, clean_crashes, clean_ipmm, clean_tnc_context


#main block that calls all 4 clean functions. create table inside waymo_tnc.db
if __name__ == "__main__":
    DB_PATH = os.path.join(BASE_DIR, "waymo_tnc.db")
    comm = sqlite3.connect(DB_PATH)
    clean_miles_df = clean_miles()
    clean_crashes_df = clean_crashes()
    clean_ipmm_df = clean_ipmm()
    clean_tnc_context_df = clean_tnc_context()
    clean_miles_df.to_sql("cleaned_miles", comm, if_exists="replace", index=False)
    clean_crashes_df.to_sql("cleaned_crashes", comm, if_exists="replace", index=False)
    clean_ipmm_df.to_sql("cleaned_ipmm", comm, if_exists="replace", index=False)
    clean_tnc_context_df.to_sql("cleaned_tnc_context", comm, if_exists="replace", index=False)
    comm.close()    