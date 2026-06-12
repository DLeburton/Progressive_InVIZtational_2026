# InVIZtational 2026 — Sprint Roadmap (v2)
## Stack: Python → SQLite → Streamlit → PowerPoint + README
### Last Updated: June 2026

---

## SUBMISSION PACKAGE (Final Deliverables)
```
InVIZtational_2026/
├── README.pdf                   ← How to interpret the project
├── InVIZtational_2026.pptx      ← Story narrative + Streamlit screenshots
├── pipeline/
│   ├── clean_data.py            ← Data cleaning + transformation
│   ├── load_db.py               ← Push cleaned data to SQLite
│   └── waymo_tnc.db             ← The database
├── streamlit_app/
│   └── app.py                   ← Interactive Streamlit dashboard
└── data/
    └── (original CSVs)          ← Raw source files
```

---

## ✅ COMPLETED (Previous Work)
- Story angle locked: "The Driverless TNC"
- 8-scene narrative structure defined
- All data analyzed — key numbers confirmed from CSVs
- TNC driver population research (800K CA, SFCTA data)
- TNC_Market_Context.csv built
- TNC_Driver_Population_Data.csv built
- Power BI exploration (data understanding only — not submitted)
- HTML prototypes built (trashed — visuals carried forward to PPT)

---

## SPRINT 1 — Python Data Pipeline
**Goal:** Clean raw CSVs, transform, load into SQLite
**Deliverable:** `clean_data.py` + `load_db.py` + `waymo_tnc.db`

### clean_data.py
- [ ] Load CSV1 (Miles) — rename columns, validate types
- [ ] Load CSV2 (Crashes) — parse dates, clean nulls, drop unused columns
- [ ] Load CSV3 (IPMM) — filter to non-Dynamic benchmark, All Crashes grouping
- [ ] Load TNC_Market_Context.csv — drop error rows (Fulton, DeKalb)
- [ ] Export 4 clean DataFrames ready for SQLite

### load_db.py
- [ ] Create SQLite database: `waymo_tnc.db`
- [ ] Create tables: `miles`, `crashes`, `ipmm`, `tnc_context`
- [ ] Load clean DataFrames into tables
- [ ] Verify row counts match expectations:
  - miles: 8 rows
  - crashes: 1,390 rows
  - ipmm: ~1,092 rows
  - tnc_context: 6 rows
- [ ] Write a simple query test to confirm data is queryable

---

## SPRINT 2 — Streamlit App
**Goal:** Interactive dashboard pulling from SQLite
**Deliverable:** `app.py` published to Streamlit Cloud

### Pages / Sections
- [ ] **Page 1 — The Safety Gap**
  - Bar chart: Waymo vs Human IPMM by severity
  - Filtered to All Locations, non-Dynamic, All Crashes
- [ ] **Page 2 — County Deep Dive**
  - Bar chart: Waymo vs Human IPMM by county
  - Slicer/filter for state
- [ ] **Page 3 — Crash Profile**
  - Donut: crash type breakdown
  - 5 KPI metrics: 282 / 127 / 49 / 3 / 2
- [ ] **Page 4 — Fleet Growth**
  - Line/bar: monthly crash volume over time
  - Annotation: volume grows with fleet, rate stays stable
- [ ] **Page 5 — The Scale**
  - 800K dot grid visual
  - KPI cards: 170.7M miles, 10,100 projected reduction
  - The underwriting question

### App Setup
- [ ] Connect to SQLite with sqlite3
- [ ] Dark theme styling to match story aesthetic
- [ ] Sidebar navigation between pages
- [ ] Deploy to Streamlit Cloud (free)
- [ ] Confirm public URL works
- [ ] Take final screenshots for PowerPoint

---

## SPRINT 3 — PowerPoint Narrative
**Goal:** Self-contained story deck that works without a presenter
**Deliverable:** `InVIZtational_2026.pptx`

### Slides
- [ ] Slide 1 — Title: "The Driverless TNC"
- [ ] Slide 2 — Hook: 800,000 TNC drivers in California
- [ ] Slide 3 — The Human Baseline (stats from Streamlit screenshot)
- [ ] Slide 4 — New Competitor Has Entered (Waymo intro)
- [ ] Slide 5 — Same Roads, Different Story (road comparison)
- [ ] Slide 6 — The Safety Gap (IPMM bar chart screenshot)
- [ ] Slide 7 — County by County (county deep dive screenshot)
- [ ] Slide 8 — The Scale (dot grid + projection screenshot)
- [ ] Slide 9 — The Underwriting Question + Streamlit URL
- [ ] Apply consistent dark theme across all slides
- [ ] Add source citations on every data slide
- [ ] Add "Explore the data: [Streamlit URL]" on final slide

---

## SPRINT 4 — README
**Goal:** Judge can understand the project cold with no context
**Deliverable:** `README.pdf`

- [ ] Section 1 — What This Project Is (2-3 sentences)
- [ ] Section 2 — The Story (plain English summary of the angle)
- [ ] Section 3 — The Data (what sources, what they show)
- [ ] Section 4 — The Technical Stack (Python → SQLite → Streamlit)
- [ ] Section 5 — How to Navigate (start with deck, explore with link)
- [ ] Section 6 — Data Limitations (honest caveats)
- [ ] Convert to PDF

---

## SPRINT 5 — Final Polish & Submission
**Goal:** Everything works, looks clean, submits as one package

- [ ] Run full pipeline end to end on clean machine (verify no broken paths)
- [ ] Confirm Streamlit URL is live and accessible
- [ ] Proofread all slides — no jargon a non-data person can't follow
- [ ] Proofread README
- [ ] Confirm all source citations are accurate
- [ ] Organize final submission folder structure
- [ ] Zip or package for submission
- [ ] Confirm submission format with InVIZtational committee

---

## OPEN QUESTIONS
- [ ] What is the submission deadline?
- [ ] What is the file size limit for submission?
- [ ] Is internal Progressive data allowed?
- [ ] Does Streamlit Cloud free tier stay live long enough for judging period?

---

## KEY NUMBERS (reference — do not change)
| Metric | Value | Source |
|--------|-------|--------|
| Total Waymo miles | 170.7M | CSV1 |
| Total crashes | 1,390 | CSV2 |
| Police-reported | 282 | CSV2 |
| Injury crashes | 127 | CSV2 |
| Airbag deployments | 49 | CSV2 |
| Serious injuries | 3 | CSV2 |
| Fatalities | 2 | CSV2 |
| Police IPMM — Waymo | 1.59 | CSV3 |
| Police IPMM — Human | 4.51 | CSV3 |
| Reduction — Police | 64.7% | CSV3 |
| Reduction — Airbag | 80.4% | CSV3 |
| Reduction — Serious | 90.0% | CSV3 |
| CA TNC drivers | 800,000 | AB 1340 (2024) |
| Projected crash reduction | ~10,100/yr | Derived |
