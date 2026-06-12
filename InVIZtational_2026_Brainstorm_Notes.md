# InVIZtational 2026 — Brainstorm Notes
**Date:** May 26, 2026  
**Dataset:** Waymo Autonomous Vehicle Safety Impact Data (Sep 2020 – Dec 2025)

---

## The Competition
Progressive's 7th annual internal data visualization competition. Entries due **June 25**. Main event **July 9**. Open to individuals or small teams. All tools supported within Progressive are fair game — not Tableau-only. Winner chosen by a panel of judges.

Key rule: The Waymo dataset is required. Supplemental data is allowed but must be **non-proprietary**. *(Still need to confirm whether internal Progressive data is permissible — email inviztational@progressive.com.)*

---

## The Dataset — What's in It
Four CSVs covering **170.7 million rider-only miles** across 4 states from September 2020 through December 2025.

| File | Contents |
|------|----------|
| CSV1 | Miles driven per county |
| CSV2 | 1,390 individual crash records with date, location, type, severity |
| CSV3 | Waymo vs. human benchmark IPMM by outcome, crash type, and county |
| CSV4 | Granular geographic data (S2 cell level) with benchmark crash counts |

**Operating markets:** San Francisco, Los Angeles, San Mateo, Santa Clara (CA) · Maricopa/Phoenix (AZ) · Travis/Austin (TX) · Fulton & DeKalb/Atlanta (GA)

**The headline numbers (vs. human driver benchmark):**
- Police-reported crashes: **−65–71%**
- Any injury: **−73–82%**
- Any airbag deployment: **−80–83%**
- Serious injury: **−90–92%**
- 2 fatalities in 170.7M miles

**Key insight:** The worse the severity, the bigger Waymo's advantage. It's not just avoiding fender-benders — it's especially good at preventing the crashes that actually hurt people.

**Time frame note:** Meaningful operational data really starts in **2024–2025**. Pre-2023 data is very sparse and reflects a small SF pilot. The benchmark comparisons in CSV3 use the full blended period, which is the most statistically defensible approach.

---

## Story Angles Explored

**1. "The Safety Ladder"** — Severity tells the real story. The more serious the crash outcome, the bigger Waymo's advantage. Counterintuitive and compelling.

**2. "Who Does Waymo Protect Most?"** — Focus on pedestrian, cyclist, and motorcycle crashes — the most emotionally resonant outcomes.

**3. "City by City"** — Geographic comparison across SF, Phoenix, LA, Austin. Does the safety advantage hold everywhere, or does it vary?

**4. "The Long Road"** — Time-series showing crash rates as Waymo's technology matures from 2020 to 2025.

**5. "Commercial Lines Lens"** — Waymo is essentially a TNC (robotaxi = same category as Uber/Lyft from an insurance standpoint). The data is a preview of what a fully autonomous commercial fleet looks like from a risk pricing perspective. Frequency drops, severity drops even more — and liability shifts toward other drivers. Directly relevant to Progressive's commercial book.

---

## The TNC Data Investigation

**The idea:** Supplement the Waymo data with public TNC (Uber/Lyft) crash data from the same geographies for a true apples-to-apples comparison — same use case, same roads, same cities.

**Findings after reviewing all four state crash databases:**

| State | System | TNC Flag? | Notes |
|-------|--------|-----------|-------|
| California | CCRS (CHP) | ❌ No | Party type field doesn't capture TNC trip status |
| Texas | CRIS (TxDOT) | ❌ No | TNC regulated by TDLR separately — no link to crash data |
| Georgia | GDOT-523 | ⚠️ Maybe | "Vehicle Class 10 = Passenger Service Vehicle (Taxi)" could include TNCs, but inconsistently applied |
| Arizona | ADOT ACIS | ❌ No TNC — but **✅ AV field** | Form has "Autonomous Veh Control: Man / AV / Unkn" |

**Conclusion:** No state has a reliable, public TNC-specific crash field. Officers record what's observable at a scene — not the commercial nature of the trip.

---

## Key Discovery — Arizona AV Field

Arizona's crash report form includes a field for **Autonomous Vehicle Control status: Manual / AV / Unknown**.

This means Waymo vehicles in Maricopa County are likely coded as **"AV"** in Arizona's public crash data (ADOT ACIS), allowing a direct **AV vs. human driver comparison using independent government data** — not Waymo's own numbers.

**Why this matters:**
- Validates Waymo's self-reported safety figures with a third-party source
- Maricopa is Waymo's **largest market by miles driven** (68.6M miles — 40% of their total)
- Adds credibility and a "trust but verify" dimension to the story
- Could be a differentiator — no other competition entry is likely pulling this

**Potential path forward:** Pull Maricopa County AV-flagged crashes from ADOT ACIS for 2024–2025, compare severity outcomes to human-driver crashes in the same county, and layer against Waymo's own CSV3 benchmark numbers.

---

## Next Steps / Open Questions
- [ ] Confirm with InVIZtational committee whether internal Progressive data is allowed
- [ ] Explore Arizona ADOT ACIS data — can the AV control field be filtered in public extract?
- [ ] Decide on primary story angle
- [ ] Confirm submission format requirements (coming soon per competition email)
