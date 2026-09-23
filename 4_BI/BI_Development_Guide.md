# 📊 Power BI Development Guide — Marketing A/B Test Dashboard

> **Source file:** `../1_Datasets/dataset_raw.csv`  
> **Approach:** Import the raw CSV into Power BI, clean it with Power Query, build a Star Schema, create advanced DAX measures, and design an interactive dashboard.

---

## 📋 Full Workflow Overview

| Phase | What You Do | Where in Power BI |
|-------|------------|-------------------|
| 1 | Import raw data | Home → Get Data |
| 2 | Clean & validate | Power Query Editor |
| 3 | Build Star Schema (Fact + Dim) | Power Query Editor |
| 4 | Create relationships | Model View |
| 5 | Write DAX measures | Data View / Report View |
| 6 | Build core visualizations | Report View |
| 7 | Implement advanced BI features| Report View |

---

## 🛠️ Phase 1 — Import the Raw Data

1. Open **Power BI Desktop**.
2. **Home → Get Data → Text/CSV**.
3. Navigate to `1_Datasets/dataset_raw.csv` → click **Open**.
4. A preview window appears — click **Transform Data**.
   > ⚠️ Click **Transform Data**, NOT Load. This opens Power Query Editor to clean the data.

---

## 🧹 Phase 2 — Data Cleaning in Power Query

1. **Rename the Query:** Right-click `dataset_raw` → **Rename** to `Cleaned_Data`.
2. **Verify Types:** Ensure `SalesInThousands` is Decimal Number, `MarketSize` is Text, and the rest are Whole Numbers.
3. **Trim Whitespace:** Select `MarketSize` → **Transform → Format → Trim**.
4. **Standardize Text:** Select `MarketSize` → **Transform → Format → Capitalize Each Word**.
5. **Check Nulls:** Use **View → Column Quality** to verify 0% Empty and 0% Error across all columns.
6. **Remove Duplicates:** Select ALL columns (Ctrl+A) → **Home → Remove Rows → Remove Duplicates**.
7. **Add Label:** Add a Custom Column named `Promo_Label` with:
   ```
   if [Promotion] = 1 then "Promo 1" else if [Promotion] = 2 then "Promo 2" else "Promo 3"
   ```

---

## 🌟 Phase 3 — Build Star Schema in Power Query

### Step 1 — Create Fact Table
1. Right-click `Cleaned_Data` → **Reference**. Name it `Fact_Sales`.
2. Select `LocationID`, `Promotion`, `week`, `SalesInThousands`.
3. Right-click selected columns → **Remove Other Columns**.

### Step 2 — Create Dimension Table
1. Right-click `Cleaned_Data` → **Reference**. Name it `Dim_Store`.
2. Select `LocationID`, `MarketID`, `MarketSize`, `AgeOfStore`.
3. Right-click selected columns → **Remove Other Columns**.
4. Select `LocationID` → **Home → Remove Rows → Remove Duplicates**.

### Step 3 — Disable Original Table
1. Right-click `Cleaned_Data` → uncheck **Enable Load**.
2. Click **Close & Apply**.

---

## 🔗 Phase 4 — Create the Relationship

1. Switch to **Model View**.
2. Drag `LocationID` from **Dim_Store** onto `LocationID` in **Fact_Sales**.
3. Verify it is a **One-to-Many (1:*)** relationship, Single direction, Active.

---

## 🧮 Phase 5 — DAX Measures

Create a Measures Table: **Home → Enter Data** → name it `_Measures` → **Load**.

### Core KPIs

```dax
Total Sales = SUM(Fact_Sales[SalesInThousands])

Avg Weekly Sales = AVERAGE(Fact_Sales[SalesInThousands])

Total Transactions = COUNTROWS(Fact_Sales)
```

### Dynamic % Lift vs Baseline (Advanced)

We want to dynamically calculate how much better/worse a selected promotion is compared to Promotion 1 (our baseline).

```dax
Avg Sales Promo 1 = 
CALCULATE(
    [Avg Weekly Sales],
    REMOVEFILTERS(Fact_Sales[Promotion]),
    Fact_Sales[Promotion] = 1
)

% Lift vs Baseline = 
VAR _baseline = [Avg Sales Promo 1]
RETURN
    DIVIDE(
        [Avg Weekly Sales] - _baseline,
        _baseline,
        0
    )
```
> **Formatting:** Select the `% Lift vs Baseline` measure → **Modeling → Format → Percentage**.

---

## 📊 Phase 6 — Core Visualizations

Build the following visuals on your main dashboard page:

### 1. Avg Weekly Sales by Promotion
* **Visual:** Clustered Column Chart
* **X-axis:** `Promotion`
* **Y-axis:** `Avg Weekly Sales`
* **Purpose:** Identifies the overall winning campaign.

### 2. Weekly Campaign Trend
* **Visual:** Line Chart
* **X-axis:** `week`
* **Y-axis:** `Avg Weekly Sales`
* **Legend:** `Promotion`
* **Purpose:** Tracks campaign fatigue over the 4-week period.

### 3. Store Age Analysis (Bins)
* **Setup:** In the Fields pane, right-click `AgeOfStore` → **New Group**. Set **Bin size** to 5. This creates 5-year age buckets.
* **Visual:** Clustered Column Chart
* **X-axis:** `AgeOfStore (bins)`
* **Y-axis:** `Avg Weekly Sales`
* **Legend:** `Promotion`
* **Purpose:** Reveals if older vs newer stores respond differently to campaigns.

### 4. Top Performing Locations
* **Visual:** Clustered Bar Chart
* **Y-axis:** `LocationID`
* **X-axis:** `Total Sales`
* **Filter:** Drag `LocationID` to the Filters pane → Filter type: **Top N** → Top 5 By `Total Sales`.
* **Purpose:** Highlights flagship locations.

### 5. Market Size Distribution
* **Visual:** Donut Chart
* **Legend:** `MarketSize`
* **Values:** `Total Sales`
* **Purpose:** Shows revenue composition across market sizes.

---

## ⭐ Phase 7 — Advanced BI Features & UX

### 1️⃣ KPI Cards
Add top-level KPI cards for:
* **Total Sales**
* **Total Transactions**
* **Avg Weekly Sales**
> **Formatting:** Select the Card → **Format visual → Callout value → Display units** → set to Thousands or Millions for a clean executive look.

### 2️⃣ Dropdown Slicers
1. Add **Slicers** for `MarketSize` and `Promotion`.
2. Select the slicer → **Format visual → Slicer settings → Style** → Change from "Vertical list" to **"Dropdown"**.
> **Why:** Saves valuable canvas space while keeping the dashboard interactive.

### 3️⃣ Report Page Tooltips
Instead of generic text tooltips, show a mini trend chart on hover:
1. Create a new page → rename it `Trend Tooltip`.
2. **Format page → Page information → Allow use as tooltip** → Turn On.
3. **Canvas settings → Type** → Select **Tooltip**.
4. Add a Line Chart on this small page (X = `week`, Y = `Avg Weekly Sales`).
5. Go to your main dashboard page, select the "Avg Weekly Sales by Promotion" Column Chart.
6. **Format visual → General → Tooltips** → Set Page to `Trend Tooltip`.

### 4️⃣ Drill-Through Pages
Allow users to drill down from a high-level Market Size into specific Store Details:
1. Create a new page → rename it `Store Details`.
2. Add a **Table** visual: `LocationID`, `AgeOfStore`, `Total Sales`.
3. In the **Format** pane for the page, under **Drill through**, drag `MarketSize` and `Promotion` into the drill-through fields well.
4. On your main dashboard, right-click any slice of the Market Size Donut Chart → **Drill through → Store Details**.

### 5️⃣ Page & Title Cleanup
* **Clean Titles:** Double-click the auto-generated visual titles (like "Avg Weekly Sales by Promotion and Promotion") and manually type clean, business-friendly titles (e.g., "Weekly Sales by Promo").
* **Hide Utility Pages:** Right-click the `Trend Tooltip` and `Store Details` page tabs at the bottom and select **Hide Page**. 
> **Why:** This ensures end-users only navigate via the main dashboard interface and drill-through actions, rather than stumbling onto utility pages.
