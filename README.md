# The Driverless TNC — Progressive InVIZtational 2026

**Live Dashboard**: [progressiveinviztational2026-5pfedegdmgjfycvuybaeyd.streamlit.app](https://progressiveinviztational2026-5pfedegdmgjfycvuybaeyd.streamlit.app/)

---

## What This Project Asks

When a licensed TNC produces 65–90% fewer crashes than the fleets you already insure— how does that change the way you price commercial auto risk?

Waymo holds the same California CPUC TNC permit as every Uber and Lyft driver in Progressive's book. This project analyzes Waymo's published safety record across 170.7 million rider-only miles and benchmarks it against human TNC drivers — then asks what it means at scale.

---

## The Data

- **Source**: Waymo Safety Impact Data Hub (March 2026 release)
- **Coverage**: 170.7 million rider-only miles · Sep 2020–Dec 2025
- **Markets**: San Francisco, Los Angeles, Phoenix, Austin, Atlanta
- **Benchmark**: Human-driven vehicles, same county, same road type · peer-reviewed (Journal of Safety Research, 2025)

---

## Stack

| Layer | Tool |
|-------|------|
| Raw data | 4 Waymo CSVs |
| Cleaning | Python · Pandas |
| Storage | SQLite |
| Dashboard | Streamlit · Plotly |
| Deployment | Streamlit Cloud |

---

## Key Files

- `clean_data.py`: reads and standardizes raw Waymo CSVs into consistent dataframes
- `load_db.py`: loads cleaned data into a local SQLite database (`waymo_tnc.db`)
- `streamlit_app/app.py`: 6-page interactive dashboard
- `streamlit_app/road_intro.html`: animated road scene intro (canvas-based)

---

## Dashboard Pages

1. **Overview** — cinematic road animation + project context
2. **Safety Gap** — Waymo IPMM vs. human benchmark across all outcome categories
3. **County Deep Dive** — police-reported IPMM by market
4. **Crash Profile** — breakdown of Waymo's 1,390 reported incidents by type
5. **The Scale Question** — projected impact if Waymo replaced CA TNC fleet
6. **Behind the Dashboard** — data pipeline and methodology
