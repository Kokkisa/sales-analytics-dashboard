# sales-analytics-dashboard[README_project5.md](https://github.com/user-attachments/files/25725055/README_project5.md)
# 📊 Interactive Sales Analytics Dashboard

## Overview
A professional, interactive business intelligence dashboard built with Streamlit and Plotly. Enables stakeholders to explore sales data through dynamic filters, KPI cards, and multiple visualization types — no SQL or Python knowledge required to use.

**Built by:** Nithin Kumar Kokkisa — Senior Demand Planner with 12+ years in manufacturing operations & supply chain analytics.

---

## Live Demo
🔗 [View Dashboard](https://share.streamlit.io) *(deploy link — update after deployment)*

## Screenshots
*(Add screenshots after running the dashboard)*

---

## Features

### KPI Cards
- Total Sales, Profit, Orders, Profit Margin, Average Order Value
- All metrics update dynamically based on filter selections

### Interactive Filters (Sidebar)
- Year (multi-select)
- Region (multi-select)
- Category (multi-select)
- Segment (multi-select)

### Visualizations
- **Sales & Profit Trend** — Area chart with monthly revenue and profit over time
- **Category Breakdown** — Horizontal bar chart + donut chart for sales and profit distribution
- **Regional Performance** — Tabbed view with grouped bar chart, treemap, and profitability heatmap
- **Top Performers** — Top 10 products and customers by sales
- **Year-over-Year Comparison** — Annual sales and profit bars with growth rates
- **Monthly Seasonality** — Multi-year line chart showing seasonal patterns

### Technical Highlights
- `@st.cache_data` for performant data loading
- Plotly interactive charts (hover, zoom, download)
- Responsive layout with columns and tabs
- Clean, professional UI design

## Dataset
Superstore Sales — ~10,000 orders across 4 years covering furniture, office supplies, and technology sales across 4 US regions.

## Tech Stack
- **Streamlit** — Web application framework
- **Plotly** — Interactive visualizations
- **Pandas** — Data manipulation
- **Python** — Core language

## How to Run Locally
```bash
pip install streamlit plotly pandas numpy
streamlit run dashboard.py
```

## How to Deploy (Free)
1. Push code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Select `dashboard.py` as the main file
5. Deploy — get a public URL!

---

## About
Part of a **30-project data analytics portfolio**. See [GitHub profile](https://github.com/Kokkisa) for the full portfolio.

**Previous Projects:**
- [Project 1 — Demand Forecasting with Prophet](https://github.com/Kokkisa/demand-forecasting-prophet)
- [Project 2 — ARIMA vs Prophet vs ETS](https://github.com/Kokkisa/forecasting-model-comparison)
- [Project 3 — Customer Churn Prediction with SHAP](https://github.com/Kokkisa/customer-churn-prediction)
- [Project 4 — SQL Business Analytics](https://github.com/Kokkisa/sql-business-analytics)
