# 📗 Excel Development Guide — Pivot Tables Analysis

> **File:** [`Marketing_AB_Test_Excel.xlsx`](Marketing_AB_Test_Excel.xlsx)  
> **Dataset columns:** `MarketID` · `MarketSize` · `LocationID` · `AgeOfStore` · `Promotion` · `week` · `SalesInThousands`

---

## 💡 1. Business Context

A fast-food chain tested **3 promotional campaigns** across Small, Medium, and Large markets for 4 weeks. Before running statistical tests in Python, we use **Excel Pivot Tables** to surface initial patterns that any stakeholder can explore — no code required.

**Our goal:** Build **5 Pivot Tables**, each answering a specific business question, then connect them into an interactive dashboard.

---

## 📋 2. Pivot Tables Overview

| # | Pivot Table | Business Question | Rows | Columns | Values |
|---|------------|-------------------|------|---------|--------|
| 1 | Sales by Promotion | Which promo generated the most revenue? | `Promotion` | — | `Sum of SalesInThousands` |
| 2 | Promotion × Market Size | Does a promo only win in certain markets? | `Promotion` | `MarketSize` | `Sum of SalesInThousands` |
| 3 | Weekly Trend | Is there Campaign Fatigue over the 4 weeks? | `week` | `Promotion` | `Average of SalesInThousands` |
| 4 | Store Age Analysis | Do newer stores respond differently? | `AgeOfStore` | `Promotion` | `Average of SalesInThousands` |
| 5 | Location Performance | Which individual locations are top/bottom? | `LocationID` | — | `Sum of SalesInThousands` |

---

## 🛠️ 3. Step-by-Step: Building Each Pivot Table

### 📌 Before You Start
1. Open `Marketing_AB_Test_Excel.xlsx`.
2. Go to the **Cleaned Data** sheet.
3. Click any cell inside the data (e.g., cell A1).
4. Make sure your data has **no blank rows** in the middle — Pivot Tables need a continuous range.

---

### Pivot 1 — Total Sales by Promotion

> **Question:** Which promotion generated the most total revenue?

**Build it:**
1. Click any cell in `Cleaned Data` → **Insert → PivotTable**.
2. In the dialog box, choose **New Worksheet** → click OK.
3. Rename the new sheet to `Pivot Analysis`.
4. In the **PivotTable Fields** pane on the right:

| Drag this field | To this area |
|----------------|--------------|
| `Promotion` | **Rows** |
| `SalesInThousands` | **Values** (it defaults to `Sum`) |

5. You should now see 3 rows (Promo 1, 2, 3) with their total sales.

**Format it:**
- Right-click any number → **Number Format** → Currency → `$#,##0` → OK.
- Click the `Sum of SalesInThousands` header → rename it to `Total Sales ($k)`.

**📊 Add a Chart:**
- Click inside the Pivot Table → **Insert → PivotChart → Clustered Bar Chart**.
- This instantly shows which promotion has the highest bar.

---

### Pivot 2 — Promotion × Market Size (Cross-Tab)

> **Question:** Does a promotion only dominate in certain market sizes?

**Build it:**
1. Click any cell in `Cleaned Data` → **Insert → PivotTable** → place in the **existing** `Pivot Analysis` sheet (choose a cell below Pivot 1, e.g., cell A10).
2. In the **PivotTable Fields** pane:

| Drag this field | To this area |
|----------------|--------------|
| `Promotion` | **Rows** |
| `MarketSize` | **Columns** |
| `SalesInThousands` | **Values** (`Sum`) |

3. You now see a **3×3 grid**: each Promotion's total sales broken down by Small, Medium, Large.

**💡 Why this matters:** If Promo 3 wins overall but only because of Large markets, a nationwide rollout would be risky. This pivot catches that.

**📊 Add a Chart:**
- Click inside → **Insert → PivotChart → Clustered Bar Chart**.
- Each market size gets its own color cluster, making comparison instant.

---

### Pivot 3 — Weekly Trend (Campaign Fatigue)

> **Question:** Does any promotion start strong but drop off over 4 weeks?

**Build it:**
1. **Insert → PivotTable** → place in `Pivot Analysis` sheet.
2. In the **PivotTable Fields** pane:

| Drag this field | To this area |
|----------------|--------------|
| `week` | **Rows** |
| `Promotion` | **Columns** |
| `SalesInThousands` | **Values** |

3. ⚠️ **Critical:** Click the dropdown on `Sum of SalesInThousands` in the Values area → **Value Field Settings** → change from `Sum` to `Average`. Click OK.
4. Rename the header to `Avg Weekly Sales ($k)`.

**💡 Why `Average` not `Sum`?** Because each week has a different number of stores reporting. Using Sum would make weeks with more stores look artificially higher. Average gives a fair comparison.

**📊 Add a Chart:**
- Click inside → **Insert → PivotChart → Line with Markers**.
- Each Promotion gets its own line. A downward slope = **Campaign Fatigue**.

---

### Pivot 4 — Store Age Analysis

> **Question:** Do newer stores respond to promotions differently than older stores?

**Build it:**
1. **Insert → PivotTable** → place in `Pivot Analysis` sheet.
2. In the **PivotTable Fields** pane:

| Drag this field | To this area |
|----------------|--------------|
| `AgeOfStore` | **Rows** |
| `Promotion` | **Columns** |
| `SalesInThousands` | **Values** (`Average`) |

3. **Group the ages into buckets** (so you don't get 20+ individual rows):
   - Right-click any value in the `AgeOfStore` column → **Group**.
   - Set: **Starting at:** `0`, **Ending at:** `30`, **By:** `5`.
   - This creates buckets: `0-4`, `5-9`, `10-14`, etc.

**💡 Why this matters:** If younger stores (<5 years) respond better to Promo 3, the marketing team can segment their rollout strategy by store maturity.

---

### Pivot 5 — Top & Bottom Locations

> **Question:** Which individual store locations are the best and worst performers?

**Build it:**
1. **Insert → PivotTable** → place in `Pivot Analysis` sheet.
2. In the **PivotTable Fields** pane:

| Drag this field | To this area |
|----------------|--------------|
| `LocationID` | **Rows** |
| `SalesInThousands` | **Values** (`Sum`) |

3. **Sort descending:** Click the dropdown arrow on `Row Labels` → **More Sort Options** → Descending by `Sum of SalesInThousands`.
4. **Show only Top 10:** Click the dropdown arrow on `Row Labels` → **Value Filters** → **Top 10** → OK.

**💡 Why this matters:** Identifies flagship locations that could serve as case studies, and underperforming locations that need investigation.

---

## 🧮 4. KPIs Sheet — Formulas Reference

Create a dedicated `KPIs` sheet with these formulas:

| Cell | Formula | What It Calculates |
|------|---------|-------------------|
| B2 | `=SUMIFS('Cleaned Data'!G:G, 'Cleaned Data'!E:E, 1)` | Total sales for **Promo 1** |
| B3 | `=SUMIFS('Cleaned Data'!G:G, 'Cleaned Data'!E:E, 2)` | Total sales for **Promo 2** |
| B4 | `=SUMIFS('Cleaned Data'!G:G, 'Cleaned Data'!E:E, 3)` | Total sales for **Promo 3** |
| C2 | `=AVERAGEIFS('Cleaned Data'!G:G, 'Cleaned Data'!E:E, 1)` | Avg weekly sales — **Promo 1** (baseline) |
| C3 | `=AVERAGEIFS('Cleaned Data'!G:G, 'Cleaned Data'!E:E, 2)` | Avg weekly sales — **Promo 2** |
| D3 | `=(C3-$C$2)/$C$2` | **% Lift** of Promo 2 vs Promo 1 |
| D4 | `=(C4-$C$2)/$C$2` | **% Lift** of Promo 3 vs Promo 1 |

> 💡 Use `$C$2` (absolute reference with dollar signs) so the baseline row stays locked when you drag the formula down.

---

## 🎛️ 5. Interactive Dashboard — Slicers & Report Connections

### Step A — Move Charts to Dashboard

1. Create a new sheet called `Dashboard`.
2. Go back to `Pivot Analysis`, click each PivotChart, press **Ctrl+X** (cut), then go to `Dashboard` and press **Ctrl+V** (paste).
3. Arrange them in a clean 2×2 or 3×1 layout.

### Step B — Add Slicers

1. Click any chart on the `Dashboard` sheet.
2. Go to **PivotChart Analyze → Insert Slicer**.
3. Check these fields: ✅ `MarketSize` ✅ `Promotion`.
4. Click OK — two slicer boxes appear.

### Step C — Connect Slicers to ALL Pivot Tables

> 🚨 **This is the step most people forget!** By default, a Slicer only controls the one Pivot Table it was created from. You must manually connect it to the others.

1. Right-click the **MarketSize** Slicer → **Report Connections**.
2. Check the boxes for **ALL** your Pivot Tables (Pivot 1, 2, 3, 4, 5).
3. Click OK.
4. Repeat for the **Promotion** Slicer.

**Result:** Now clicking "Large" on the MarketSize slicer filters every chart on the dashboard simultaneously. This is what makes it truly interactive.

---

## 🎨 6. Finishing Touches

| Technique | Where to Apply | Why |
|-----------|---------------|-----|
| **Conditional Formatting** → Color Scale (Green-Red) | `Cleaned Data` column G (`SalesInThousands`) | Instantly spot top/bottom weeks without reading numbers |
| **Currency format** (`$#,##0`) | All sales values in Pivots and KPIs | Executives expect clean dollar figures |
| **Slicer styling** | Right-click slicer → Slicer Settings → Style | Match your company brand colors |
| **Chart titles** | Double-click each chart title | Replace generic "Total" with descriptive titles like "Sales by Promotion & Market Size" |
| **Tab colors** | Right-click sheet tab → Tab Color | Color-code: Green for Dashboard, Blue for Pivots, Gray for raw data |

---

## 🚀 7. What You Should See When Done

Your `Dashboard` sheet should have:

- 📊 **Bar chart** showing total sales by Promotion (Pivot 1)
- 📊 **Grouped bar chart** showing Promotion × Market Size (Pivot 2)
- 📈 **Line chart** showing weekly trends (Pivot 3)
- 🎛️ **Two slicers** (MarketSize + Promotion) controlling everything
- Clicking any slicer button instantly updates all charts

> **Portfolio tip:** Take a screenshot of your finished dashboard with one slicer active (e.g., "Large" market selected) to include in your README or LinkedIn post. It demonstrates you can build interactive BI deliverables without Power BI.
