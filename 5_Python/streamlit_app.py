"""
Streamlit A/B Testing Dashboard
Fast Food Marketing Campaign Analysis
"""
import os

import pandas as pd
import plotly.express as px
import scipy.stats as stats
import streamlit as st
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# ──────────────────────────────────────────────
# Page Config
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Marketing A/B Test Dashboard",
    layout="wide",
    page_icon="🍔",
)

# ──────────────────────────────────────────────
# Data Loading
# ──────────────────────────────────────────────
from pathlib import Path

@st.cache_data
def load_data() -> pd.DataFrame:
    """Load cleaned dataset using robust relative pathing."""
    # Find the repository root dynamically based on this script's location
    # __file__ is .../5_Python/streamlit_app.py
    # .parent is .../5_Python/
    # .parent.parent is the repository root
    current_dir = Path(__file__).parent
    repo_root = current_dir.parent
    
    # The absolute path to the dataset, regardless of where Streamlit is executed from
    primary_path = repo_root / "1_Datasets" / "dataset_cleaned.csv"
    
    # Fallback strings just in case
    DATA_PATHS = [
        primary_path,
        "1_Datasets/dataset_cleaned.csv",      # If executing from repo root
        "../1_Datasets/dataset_cleaned.csv",   # If executing from 5_Python/
    ]
    
    for path in DATA_PATHS:
        if os.path.exists(path):
            return pd.read_csv(path)
            
    # If all paths fail, output the debugging info requested
    st.error("❌ Dataset not found. Check your GitHub repository and case sensitivity.")
    
    st.markdown("### 🐛 Path Debugging Information")
    st.write(f"**Current Working Directory (`os.getcwd()`):** `{os.getcwd()}`")
    st.write(f"**Script Location (`__file__`):** `{__file__}`")
    
    st.write("**Contents of Current Working Directory:**")
    st.json(os.listdir(os.getcwd()))
    
    # Also try to print the repo root if it exists
    if repo_root.exists():
        st.write(f"**Contents of Repo Root (`{repo_root}`):**")
        st.json(os.listdir(repo_root))
        
    st.stop()


df = load_data()

# ──────────────────────────────────────────────
# Sidebar – Filters & Controls
# ──────────────────────────────────────────────
st.sidebar.title("⚙️ Dashboard Controls")

selected_markets = st.sidebar.multiselect(
    "🏢 Market Size",
    options=sorted(df["MarketSize"].unique()),
    default=sorted(df["MarketSize"].unique()),
)
selected_promos = st.sidebar.multiselect(
    "🎯 Promotions",
    options=sorted(df["Promotion"].unique()),
    default=sorted(df["Promotion"].unique()),
)

st.sidebar.markdown("---")
st.sidebar.subheader("🧪 Statistical Parameters")
alpha = st.sidebar.slider(
    "Significance Level (α)",
    min_value=0.01,
    max_value=0.10,
    value=0.05,
    step=0.01,
    help="Lower α = stricter test. 0.05 is the industry standard.",
)

# Apply filters
mask = df["MarketSize"].isin(selected_markets) & df["Promotion"].isin(selected_promos)
filtered = df[mask].copy()

# ──────────────────────────────────────────────
# Header
# ──────────────────────────────────────────────
st.title("🍔 Fast Food Marketing Campaign — A/B Test Dashboard")
st.caption("Compare promotion performance with interactive charts and live statistical testing.")

if filtered.empty:
    st.warning("No data matches your filters. Adjust the sidebar selections.")
    st.stop()

# ──────────────────────────────────────────────
# KPI Cards
# ──────────────────────────────────────────────
promo_means = filtered.groupby("Promotion")["SalesInThousands"].mean()
best_promo = promo_means.idxmax()
best_avg = promo_means.max()

# % lift of the best promo vs the global Promo-1 baseline
baseline = df.loc[df["Promotion"] == 1, "SalesInThousands"].mean()
lift = ((best_avg - baseline) / baseline) * 100 if baseline else 0.0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Revenue (filtered)", f"${filtered['SalesInThousands'].sum():,.1f}k")
c2.metric("🏆 Best Promotion", f"Promo {best_promo}")
c3.metric("Best Avg Weekly Sales", f"${best_avg:.1f}k")
c4.metric("% Lift vs Promo 1", f"{lift:+.1f}%")

st.markdown("---")

# ──────────────────────────────────────────────
# Visualisation Tabs
# ──────────────────────────────────────────────
tab_dist, tab_trend, tab_market = st.tabs(
    ["📊 Distribution", "📈 Weekly Trend", "🏢 Market Breakdown"]
)

with tab_dist:
    st.subheader("Sales Distribution by Promotion")
    fig = px.violin(
        filtered,
        x="Promotion",
        y="SalesInThousands",
        color="Promotion",
        box=True,
        points="all",
        hover_data=["MarketSize", "AgeOfStore"],
        labels={"SalesInThousands": "Sales ($k)", "Promotion": "Promo"},
    )
    fig.update_layout(xaxis_type="category", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with tab_trend:
    st.subheader("Average Weekly Sales Over 4 Weeks")
    trend = (
        filtered.groupby(["week", "Promotion"], as_index=False)["SalesInThousands"]
        .mean()
        .rename(columns={"SalesInThousands": "AvgSales"})
    )
    fig = px.line(
        trend,
        x="week",
        y="AvgSales",
        color="Promotion",
        markers=True,
        labels={"AvgSales": "Avg Sales ($k)", "week": "Week"},
    )
    fig.update_layout(xaxis=dict(tickmode="linear", dtick=1))
    st.plotly_chart(fig, use_container_width=True)

with tab_market:
    st.subheader("Sales by Market Size & Promotion")
    market_data = (
        filtered.groupby(["MarketSize", "Promotion"], as_index=False)["SalesInThousands"]
        .mean()
        .rename(columns={"SalesInThousands": "AvgSales"})
    )
    fig = px.bar(
        market_data,
        x="MarketSize",
        y="AvgSales",
        color="Promotion",
        barmode="group",
        labels={"AvgSales": "Avg Sales ($k)"},
    )
    fig.update_layout(xaxis_type="category")
    st.plotly_chart(fig, use_container_width=True)

# ──────────────────────────────────────────────
# Statistical Testing
# ──────────────────────────────────────────────
st.markdown("---")
st.header("🧬 A/B Testing Engine")

if len(selected_promos) < 2:
    st.info("Select at least **two** promotions in the sidebar to run the ANOVA test.")
else:
    # Validate sample sizes
    group_sizes = filtered.groupby("Promotion").size()
    small_groups = group_sizes[group_sizes < 5]

    if not small_groups.empty:
        st.error(
            f"⚠️ Promotion(s) {list(small_groups.index)} have fewer than 5 observations. "
            "ANOVA results would be unreliable. Broaden your filters."
        )
    else:
        # One-Way ANOVA
        groups = [
            filtered.loc[filtered["Promotion"] == p, "SalesInThousands"]
            for p in selected_promos
        ]
        f_stat, p_value = stats.f_oneway(*groups)

        st.markdown(f"**Alpha:** `{alpha}` · **P-value:** `{p_value:.4e}` · **F-stat:** `{f_stat:.2f}`")

        if p_value < alpha:
            st.success(
                f"✅ **Significant** — The p-value ({p_value:.4e}) is below α ({alpha}). "
                "The promotions perform differently."
            )

            # Post-hoc: Tukey HSD
            st.subheader("Post-Hoc: Tukey HSD")
            tukey = pairwise_tukeyhsd(
                endog=filtered["SalesInThousands"],
                groups=filtered["Promotion"],
                alpha=alpha,
            )

            # Convert Tukey results to a clean DataFrame
            tukey_df = pd.DataFrame(
                data=tukey._results_table.data[1:],
                columns=tukey._results_table.data[0],
            )
            st.dataframe(tukey_df, use_container_width=True, hide_index=True)
        else:
            st.warning(
                f"❌ **Not significant** — The p-value ({p_value:.4e}) exceeds α ({alpha}). "
                "Observed differences are likely due to chance."
            )
