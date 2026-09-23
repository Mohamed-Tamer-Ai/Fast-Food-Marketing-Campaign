# 🗄️ SQL Development Guide

> **File:** [`AB_Test_Queries.sql`](AB_Test_Queries.sql)  
> **Database:** SQLite · **Table:** `campaign`

---

## 📋 Queries at a Glance

| # | Query | Technique | Business Question |
|---|-------|-----------|-------------------|
| Q1 | Total & Avg Sales by Promotion | `GROUP BY` + aggregates | Which promo generated the most revenue? |
| Q2 | Sales by Promotion & Market Size | Multi-column `GROUP BY` | Does a promo only win in certain markets? |
| Q3 | Effectiveness by Store Age | CTE + `CASE WHEN` | Do newer stores respond differently? |
| Q4 | Rank Promos per Market | Window Function (`RANK`) | Who is #1 in each market tier? |

---

## 📊 Q1 — Total & Average Sales by Promotion

**🎯 Objective:** Identify the highest-grossing promotion overall.

- **Logic:** Group by `Promotion`, then compute `SUM()` and `AVG()` of `SalesInThousands`.
- **Why it matters:** This is the first number any stakeholder will ask for. It gives the absolute revenue each campaign produced.
- **⚠️ Caveat:** High total sales doesn't mean the difference is *statistically significant* — we validate that in the Python phase.

---

## 🏢 Q2 — Sales by Promotion & Market Size

**🎯 Objective:** Check if a promotion dominates only in certain market tiers (Small / Medium / Large).

- **Logic:** Add `MarketSize` to the `GROUP BY` so we get a cross-tabulation of performance.
- **Why it matters:** If Promo 3 wins in "Large" markets but loses in "Small" markets, a nationwide rollout would be a mistake. This query catches that.

---

## ⏳ Q3 — Promotion Effectiveness by Store Age

**🎯 Objective:** Determine if newer stores respond differently to promotions.

**Logic Breakdown:**
1. **CTE (`WITH AgeTiers AS …`)** — Classify `AgeOfStore` into 3 buckets:

   | Bucket | Rule |
   |--------|------|
   | `<5 years` | Brand-new locations |
   | `5-10 years` | Established mid-tier |
   | `10+ years` | Legacy / mature stores |

2. **Aggregation** — Group by `AgeTier` + `Promotion`, then compute `AVG()` and `SUM()`.

- **💡 Insight:** If younger stores respond better to a specific promo, the marketing team can segment their rollout strategy.

---

## ⭐ Q4 — Rank Promotions per Market (Window Function)

**🎯 Objective:** Rank promotion performance *within* each market size — no manual sorting needed.

**Key concepts:**
- **`RANK() OVER (PARTITION BY MarketSize ORDER BY TotalSales DESC)`**
  - `PARTITION BY` resets the rank counter for each market tier.
  - `ORDER BY … DESC` puts the highest sales at Rank 1.

**💼 Business value:** Stakeholders can instantly see: *"In Large markets, Promo 3 is #1. In Small markets, Promo 1 is #1."* — no pivot table required.

---

## 🚀 How to Run These Queries

```bash
# Option A — SQLite CLI
sqlite3 campaign_data.db < AB_Test_Queries.sql

# Option B — Python
import sqlite3, pandas as pd
conn = sqlite3.connect('campaign_data.db')
df = pd.read_sql('SELECT * FROM campaign LIMIT 5', conn)
```
