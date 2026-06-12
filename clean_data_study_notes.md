# Study Notes: clean_data.py
### Progressive InVIZtational 2026 — Sprint 1

---

## What clean_data.py does

`clean_data.py` is a **module** — a file that holds reusable functions. It doesn't run anything on its own. It defines 4 functions, one per data source, that each:
1. Read a raw CSV file
2. Rename the columns
3. Fix data types
4. Return a clean DataFrame

The next file (`load_db.py`) will import and call these functions to load the data into SQLite.

---

## What is snake_case and why does it matter?

**snake_case** is a naming convention where all words are lowercase and separated by underscores. Examples:
- `waymo_miles_millions`
- `is_police_reported`
- `benchmark_ipmm_police`

The raw CSV headers use mixed formats like:
- `"Is Police-Reported"` — has a hyphen and mixed case
- `"Waymo IPMM CI Lower"` — has spaces
- `"CA_TNC_Trip_Share_Est"` — inconsistent capitalization

**Why we rename everything to snake_case:**

1. **Consistency** — every table in the database uses the same naming style. You never have to remember if it's `"Is Police-Reported"` or `"is_police_reported"` or `"IsPoliceReported"`.
2. **Python compatibility** — column names with spaces or hyphens cause errors when you try to access them using dot notation (e.g., `df.is_police_reported` works; `df.Is Police-Reported` does not).
3. **SQL compatibility** — SQLite column names with spaces require special quoting. snake_case avoids that entirely.
4. **Streamlit** — when you build charts later, these column names become axis labels and filter keys. Clean names = less cleanup work.

**Rule of thumb:** Rename columns at the top of every function, right after `pd.read_csv`. Everything downstream uses the new names.

---

## Errors we hit and how to read them

### 1. UnboundLocalError

**What you saw:**
```
UnboundLocalError: cannot access local variable 'df' where it is not associated with a value
```

**What it means:**
You tried to use a variable (`df`) before it was created. In Python, variables only exist after the line that assigns them has run. If your code tries to reference `df` on line 5 but `df = pd.read_csv(...)` is on line 8, Python has no idea what `df` is yet.

**How to spot it:**
Look at the line number in the error. Then look at your code — is the variable being used *before* it's assigned?

**How to fix it:**
Always make sure assignment (`df = ...`) comes before usage (`df["column"]`). Order of execution matters.

---

### 2. KeyError

**What you saw:**
```
KeyError: 'is_police_reported'
```

**What it means:**
You tried to access a column that doesn't exist in the DataFrame at that point in the code. This happens because:
- You referenced the new snake_case name before the rename had run
- You referenced the old original name after the rename had run
- There was a typo in the column name

**How to spot it:**
The error tells you exactly which column name it couldn't find. Compare that name against your `df.columns` list character by character — capitalization, hyphens, and spaces all matter.

**How to fix it:**
Check where in the function the error line falls relative to your `df.columns = [...]` rename. If the rename already ran, use the new name. If not, use the original name.

---

### 3. The .map() that did nothing (silent bug)

**What happened:**
The boolean columns stayed as `object` dtype and the police-reported count was 0, even though `.map({"True": True, "False": False})` looked correct.

**Why it failed:**
The values in the CSV were already Python booleans (`True`/`False`), not the strings `"True"`/`"False"`. The `.map()` was looking for string keys that didn't exist, so every row returned `NaN`.

**Why this is dangerous:**
There was no error message. The code ran fine and returned results — just wrong ones. This is a **silent bug** — harder to catch than a crash because you have to know what the right answer should be to notice something is wrong.

**How to spot silent bugs:**
Always validate your output against a known value. We knew from Power BI that police-reported should be 282. When it came back as 0, that was the signal something was wrong.

**How to fix it:**
Use `df["column"].unique()` to inspect the raw values before transforming. Once you see what's actually in the column, you can choose the right conversion method.

**Lesson learned:** Before writing any transformation, always check what the raw data actually looks like. Don't assume.

---

### 4. .str.contains() vs ==

**The situation:**
Filtering CSV3 to keep only non-Dynamic benchmark rows.

**Wrong approach:**
```python
df = df[df["benchmark_comparison"] == "non-Dynamic"]
```
This checks for an exact match. The actual values look like `"Police-reported (non-Dynamic)"` — non-Dynamic is a substring, not the full value. This filter returns zero rows.

**Right approach:**
```python
df = df[df["benchmark_comparison"].str.contains("non-Dynamic")]
```
`.str.contains()` checks whether the substring appears anywhere in the string.

**Rule of thumb:**
- Use `==` when you know the exact, complete value
- Use `.str.contains()` when you're matching a pattern or partial value

---

## Key pandas methods used in clean_data.py

| Method | What it does |
|---|---|
| `pd.read_csv()` | Reads a CSV file into a DataFrame |
| `df.columns = [...]` | Renames all columns at once |
| `pd.to_numeric(..., errors="coerce")` | Converts to number; bad values become NaN |
| `.astype(bool)` | Converts column to boolean type |
| `pd.to_datetime(..., errors="coerce")` | Parses dates; bad values become NaT |
| `.str.contains("text")` | Returns True where substring is found |
| `.str.replace("x", "y")` | Replaces characters in a string column |
| `.isin([...])` | Returns True where value is in a list |
| `~` (tilde) | Negates a boolean condition (NOT) |
| `.unique()` | Returns all distinct values in a column |
| `.sum()` | Sums a column (True counts as 1 for booleans) |

---

## Final row counts (validation reference)

| Table | Rows | Notes |
|---|---|---|
| miles | 8 | All Waymo locations including blended total |
| crashes | 1,390 | Sep 2020 – Dec 2025, 4 states |
| ipmm | 46 | Filtered: non-Dynamic, All Crashes grouping |
| tnc_context | 6 | Fulton + DeKalb removed (no IPMM data) |
