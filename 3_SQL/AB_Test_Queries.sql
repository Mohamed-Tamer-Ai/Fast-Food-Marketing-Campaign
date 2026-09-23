-- ============================================================================
-- Fast Food Marketing A/B Test — SQL Analysis
-- ============================================================================
-- Database: SQLite (ANSI-compatible)
-- Table:    campaign
-- Columns:  MarketID, MarketSize, LocationID, AgeOfStore,
--           Promotion, week, SalesInThousands
-- ============================================================================


-- --------------------------------------------------------------------------
-- Q1: Total & Average Sales by Promotion
-- Purpose: Quick KPI — which promotion generated the most revenue overall?
-- --------------------------------------------------------------------------
SELECT
    Promotion,
    COUNT(*)                              AS Weeks,
    ROUND(SUM(SalesInThousands), 2)       AS TotalSales,
    ROUND(AVG(SalesInThousands), 2)       AS AvgWeeklySales
FROM campaign
GROUP BY Promotion
ORDER BY TotalSales DESC;


-- --------------------------------------------------------------------------
-- Q2: Sales by Promotion AND Market Size
-- Purpose: Check whether a promotion only dominates in certain market tiers.
-- --------------------------------------------------------------------------
SELECT
    MarketSize,
    Promotion,
    ROUND(SUM(SalesInThousands), 2)       AS TotalSales,
    ROUND(AVG(SalesInThousands), 2)       AS AvgWeeklySales,
    COUNT(*)                              AS Weeks
FROM campaign
GROUP BY MarketSize, Promotion
ORDER BY MarketSize, TotalSales DESC;


-- --------------------------------------------------------------------------
-- Q3: Promotion Effectiveness by Store Age (CTE)
-- Purpose: Do newer stores respond differently to promotions?
-- Age buckets: <5 years | 5-10 years | 10+ years
-- --------------------------------------------------------------------------
WITH AgeTiers AS (
    SELECT
        Promotion,
        CASE
            WHEN AgeOfStore < 5             THEN '1. <5 years'
            WHEN AgeOfStore BETWEEN 5 AND 10 THEN '2. 5-10 years'
            ELSE                                  '3. 10+ years'
        END AS AgeTier,
        SalesInThousands
    FROM campaign
)
SELECT
    AgeTier,
    Promotion,
    ROUND(AVG(SalesInThousands), 2)       AS AvgWeeklySales,
    ROUND(SUM(SalesInThousands), 2)       AS TotalSales,
    COUNT(*)                              AS Weeks
FROM AgeTiers
GROUP BY AgeTier, Promotion
ORDER BY AgeTier, Promotion;


-- --------------------------------------------------------------------------
-- Q4: Rank Promotions Within Each Market Size (Window Function)
-- Purpose: Identify the #1 promotion per market tier without manual sorting.
-- --------------------------------------------------------------------------
WITH PromoMarketTotals AS (
    SELECT
        MarketSize,
        Promotion,
        ROUND(SUM(SalesInThousands), 2)   AS TotalSales
    FROM campaign
    GROUP BY MarketSize, Promotion
)
SELECT
    MarketSize,
    Promotion,
    TotalSales,
    RANK() OVER (
        PARTITION BY MarketSize
        ORDER BY TotalSales DESC
    ) AS Rank
FROM PromoMarketTotals
ORDER BY MarketSize, Rank;