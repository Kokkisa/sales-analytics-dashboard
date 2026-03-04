#!/usr/bin/env python
# coding: utf-8

# =============================================================================
# PROJECT 5: INTERACTIVE SALES DASHBOARD WITH STREAMLIT
# =============================================================================
# Author: Nithin Kumar Kokkisa
# Purpose: Build a professional interactive dashboard that business stakeholders
#          can use to explore data, filter by dimensions, and get insights.
#
# WHY THIS PROJECT:
# - Data scientists don't just build models — they COMMUNICATE results
# - Stakeholders want dashboards, not Jupyter notebooks
# - Streamlit is the fastest way to build ML/data apps in Python
# - Shows you can go from data → insight → PRODUCT
#
# DATASET: Superstore Sales (popular Kaggle dataset, ~10,000 orders)
# - Sales, profit, quantity across categories, regions, segments
# - Date range: 4 years of order history
# - Perfect for business intelligence dashboards
#
# NEW CONCEPTS YOU'LL LEARN:
# - Streamlit framework (interactive web apps in Python)
# - KPI cards (key performance indicators)
# - Interactive filters (sidebar dropdowns, date ranges)
# - Multiple chart types (line, bar, pie, heatmap, treemap)
# - Plotly for interactive charts (hover, zoom, click)
# - Page layout (columns, tabs, expanders)
# - Caching for performance
#
# ESTIMATED TIME: 2-3 hours
#
# HOW TO RUN:
# 1. Save this file as dashboard.py
# 2. Open Command Prompt, navigate to the file location
# 3. Run: streamlit run dashboard.py
# 4. Browser opens automatically at localhost:8501
# =============================================================================


# =============================================================================
# STEP 1: IMPORTS AND PAGE CONFIG
# =============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page configuration — MUST be the first Streamlit command
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="\U0001F4CA",
    layout="wide",           # Use full screen width
    initial_sidebar_state="expanded"
)

# WHAT THIS DOES:
# set_page_config controls the browser tab title, favicon, and layout.
# layout="wide" uses the full browser width instead of a narrow centered column.
# This MUST be the very first st.xxx command — before any other Streamlit call.


# =============================================================================
# STEP 2: LOAD AND PREPARE DATA
# =============================================================================

@st.cache_data
def load_data():
    """Load and prepare the Superstore dataset."""
    url = "https://community.tableau.com/s/question/0D54T00000CWeX8SAL/sample-superstore-sales-excelxls"
    
    # Try multiple sources
    urls = [
        "https://raw.githubusercontent.com/jdwittenauer/dataset-collection/master/SampleSuperstore.csv",
        "https://raw.githubusercontent.com/dsrscientist/dataset1/master/superstore.csv",
    ]
    
    df = None
    for u in urls:
        try:
            df = pd.read_csv(u, encoding='windows-1252')
            break
        except:
            try:
                df = pd.read_csv(u)
                break
            except:
                continue
    
    if df is None:
        # Generate sample data if all URLs fail
        np.random.seed(42)
        n = 5000
        dates = pd.date_range('2020-01-01', '2023-12-31', periods=n)
        categories = np.random.choice(['Furniture', 'Office Supplies', 'Technology'], n, p=[0.3, 0.4, 0.3])
        regions = np.random.choice(['East', 'West', 'Central', 'South'], n)
        segments = np.random.choice(['Consumer', 'Corporate', 'Home Office'], n, p=[0.5, 0.3, 0.2])
        
        sub_cats = {
            'Furniture': ['Chairs', 'Tables', 'Bookcases', 'Furnishings'],
            'Office Supplies': ['Paper', 'Binders', 'Art', 'Storage', 'Labels'],
            'Technology': ['Phones', 'Accessories', 'Machines', 'Copiers']
        }
        
        sub_category = [np.random.choice(sub_cats[c]) for c in categories]
        sales = np.random.exponential(250, n).round(2)
        profit = (sales * np.random.uniform(-0.2, 0.4, n)).round(2)
        quantity = np.random.randint(1, 10, n)
        
        df = pd.DataFrame({
            'Order ID': [f'ORD-{i:05d}' for i in range(n)],
            'Order Date': dates,
            'Ship Date': dates + pd.to_timedelta(np.random.randint(1, 7, n), unit='D'),
            'Customer Name': [f'Customer_{np.random.randint(1,300)}' for _ in range(n)],
            'Segment': segments,
            'Region': regions,
            'Category': categories,
            'Sub-Category': sub_category,
            'Product Name': [f'{s}_{np.random.randint(1,20)}' for s in sub_category],
            'Sales': sales,
            'Profit': profit,
            'Quantity': quantity,
        })
    
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Ship Date'] = pd.to_datetime(df['Ship Date'])
    df['Year'] = df['Order Date'].dt.year
    df['Month'] = df['Order Date'].dt.month
    df['Month_Name'] = df['Order Date'].dt.strftime('%b')
    df['Quarter'] = df['Order Date'].dt.quarter
    df['Year_Month'] = df['Order Date'].dt.to_period('M').astype(str)
    df['Profit_Margin'] = (df['Profit'] / df['Sales'] * 100).round(1)
    
    return df

# Load the data
df = load_data()

# @st.cache_data EXPLAINED:
# Without caching: every time you click a filter, Streamlit reruns the ENTIRE script.
# That means reloading the CSV every single time — slow!
# @st.cache_data caches the result: load once, reuse on every rerun.
# The cache invalidates when the function code or inputs change.


# =============================================================================
# STEP 3: SIDEBAR FILTERS
# =============================================================================

st.sidebar.title("\U0001F50D Filters")
st.sidebar.markdown("---")

# Year filter
all_years = sorted(df['Year'].unique())
selected_years = st.sidebar.multiselect(
    "Select Year(s)",
    options=all_years,
    default=all_years
)

# Region filter
all_regions = sorted(df['Region'].unique())
selected_regions = st.sidebar.multiselect(
    "Select Region(s)",
    options=all_regions,
    default=all_regions
)

# Category filter
all_categories = sorted(df['Category'].unique())
selected_categories = st.sidebar.multiselect(
    "Select Category(ies)",
    options=all_categories,
    default=all_categories
)

# Segment filter
all_segments = sorted(df['Segment'].unique())
selected_segments = st.sidebar.multiselect(
    "Select Segment(s)",
    options=all_segments,
    default=all_segments
)

# Apply filters
filtered_df = df[
    (df['Year'].isin(selected_years)) &
    (df['Region'].isin(selected_regions)) &
    (df['Category'].isin(selected_categories)) &
    (df['Segment'].isin(selected_segments))
]

# Show filter summary
st.sidebar.markdown("---")
st.sidebar.metric("Filtered Orders", f"{len(filtered_df):,}")
st.sidebar.metric("Total Orders", f"{len(df):,}")

# WHAT THIS DOES:
# st.sidebar puts widgets in the left sidebar (not the main page).
# multiselect lets users pick one or more options from a list.
# default=all_years means everything is selected initially.
# The filtered_df applies ALL selected filters using .isin() with AND logic.
# st.sidebar.metric shows a nice KPI card in the sidebar.


# =============================================================================
# STEP 4: HEADER AND KPI CARDS
# =============================================================================

# Main title
st.title("\U0001F4CA Sales Analytics Dashboard")
st.markdown("Interactive business intelligence dashboard for Superstore sales data")
st.markdown("---")

# Calculate KPIs
total_sales = filtered_df['Sales'].sum()
total_profit = filtered_df['Profit'].sum()
total_orders = filtered_df['Order ID'].nunique()
avg_profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
avg_order_value = total_sales / total_orders if total_orders > 0 else 0

# Display KPIs in columns
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="\U0001F4B0 Total Sales",
        value=f"${total_sales:,.0f}",
    )
with col2:
    st.metric(
        label="\U0001F4C8 Total Profit",
        value=f"${total_profit:,.0f}",
    )
with col3:
    st.metric(
        label="\U0001F4E6 Total Orders",
        value=f"{total_orders:,}",
    )
with col4:
    st.metric(
        label="\U0001F3AF Profit Margin",
        value=f"{avg_profit_margin:.1f}%",
    )
with col5:
    st.metric(
        label="\U0001F6D2 Avg Order Value",
        value=f"${avg_order_value:,.0f}",
    )

st.markdown("---")

# WHAT THIS DOES:
# st.columns(5) creates 5 equal-width columns.
# st.metric shows a KPI card with label and value.
# The "with col1:" syntax puts content into that specific column.
# These KPIs update AUTOMATICALLY when filters change!


# =============================================================================
# STEP 5: SALES TREND OVER TIME
# =============================================================================

st.subheader("\U0001F4C8 Sales & Profit Trend")

# Monthly aggregation
monthly = filtered_df.groupby('Year_Month').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Order ID': 'nunique'
}).reset_index()
monthly.columns = ['Month', 'Sales', 'Profit', 'Orders']
monthly = monthly.sort_values('Month')

# Create dual-axis chart
fig_trend = go.Figure()

fig_trend.add_trace(go.Scatter(
    x=monthly['Month'], y=monthly['Sales'],
    name='Sales', line=dict(color='#2E86C1', width=2),
    fill='tozeroy', fillcolor='rgba(46,134,193,0.1)'
))

fig_trend.add_trace(go.Scatter(
    x=monthly['Month'], y=monthly['Profit'],
    name='Profit', line=dict(color='#28B463', width=2),
    fill='tozeroy', fillcolor='rgba(40,180,99,0.1)'
))

fig_trend.update_layout(
    height=400,
    hovermode='x unified',
    plot_bgcolor='white',
    xaxis=dict(showgrid=False, tickangle=-45, dtick=3),
    yaxis=dict(title='Amount ($)', gridcolor='#f0f0f0'),
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
)

st.plotly_chart(fig_trend, use_container_width=True)

# WHAT THIS DOES:
# go.Figure() creates a Plotly chart (interactive — hover, zoom, download).
# add_trace adds a line/area to the chart.
# fill='tozeroy' fills area from line down to zero (area chart).
# hovermode='x unified' shows all values when hovering over any point.
# use_container_width=True stretches chart to full page width.
# The chart is INTERACTIVE — users can hover, zoom, pan, and download.


# =============================================================================
# STEP 6: CATEGORY BREAKDOWN (Two columns)
# =============================================================================

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("\U0001F4CA Sales by Category")
    
    cat_sales = filtered_df.groupby('Category')['Sales'].sum().reset_index()
    cat_sales = cat_sales.sort_values('Sales', ascending=True)
    
    fig_cat = px.bar(
        cat_sales, x='Sales', y='Category',
        orientation='h',
        color='Category',
        color_discrete_sequence=['#2E86C1', '#28B463', '#E74C3C'],
        text=cat_sales['Sales'].apply(lambda x: f'${x:,.0f}')
    )
    fig_cat.update_layout(
        height=350, showlegend=False,
        plot_bgcolor='white',
        xaxis=dict(title='Sales ($)', gridcolor='#f0f0f0'),
        yaxis=dict(title='')
    )
    fig_cat.update_traces(textposition='auto')
    st.plotly_chart(fig_cat, use_container_width=True)

with col_right:
    st.subheader("\U0001F4B0 Profit by Category")
    
    cat_profit = filtered_df.groupby('Category')['Profit'].sum().reset_index()
    
    fig_profit = px.pie(
        cat_profit, values='Profit', names='Category',
        color_discrete_sequence=['#2E86C1', '#28B463', '#E74C3C'],
        hole=0.4  # Donut chart
    )
    fig_profit.update_layout(height=350)
    fig_profit.update_traces(textinfo='label+percent', textfont_size=14)
    st.plotly_chart(fig_profit, use_container_width=True)


# =============================================================================
# STEP 7: REGIONAL PERFORMANCE
# =============================================================================

st.subheader("\U0001F30E Regional Performance")

tab1, tab2, tab3 = st.tabs(["Sales by Region", "Sub-Category Analysis", "Profitability Heatmap"])

with tab1:
    region_data = filtered_df.groupby('Region').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Order ID': 'nunique'
    }).reset_index()
    region_data.columns = ['Region', 'Sales', 'Profit', 'Orders']
    region_data['Profit_Margin'] = (region_data['Profit'] / region_data['Sales'] * 100).round(1)
    
    fig_region = px.bar(
        region_data, x='Region', y=['Sales', 'Profit'],
        barmode='group',
        color_discrete_sequence=['#2E86C1', '#28B463'],
        text_auto='.2s'
    )
    fig_region.update_layout(
        height=400, plot_bgcolor='white',
        yaxis=dict(title='Amount ($)', gridcolor='#f0f0f0'),
        legend=dict(orientation='h', yanchor='bottom', y=1.02)
    )
    st.plotly_chart(fig_region, use_container_width=True)
    
    # Region metrics table
    st.dataframe(
        region_data.style.format({
            'Sales': '${:,.0f}',
            'Profit': '${:,.0f}',
            'Orders': '{:,}',
            'Profit_Margin': '{:.1f}%'
        }),
        use_container_width=True,
        hide_index=True
    )

with tab2:
    subcat_sales = filtered_df.groupby(['Category', 'Sub-Category']).agg({
        'Sales': 'sum',
        'Profit': 'sum'
    }).reset_index()
    
    fig_treemap = px.treemap(
        subcat_sales,
        path=['Category', 'Sub-Category'],
        values='Sales',
        color='Profit',
        color_continuous_scale='RdYlGn',
        color_continuous_midpoint=0,
        title='Sales Volume (size) vs Profitability (color)'
    )
    fig_treemap.update_layout(height=500)
    st.plotly_chart(fig_treemap, use_container_width=True)

with tab3:
    heatmap_data = filtered_df.groupby(['Region', 'Category'])['Profit_Margin'].mean().reset_index()
    heatmap_pivot = heatmap_data.pivot(index='Region', columns='Category', values='Profit_Margin')
    
    fig_heat = px.imshow(
        heatmap_pivot,
        color_continuous_scale='RdYlGn',
        color_continuous_midpoint=0,
        text_auto='.1f',
        labels=dict(color='Profit Margin %'),
        aspect='auto'
    )
    fig_heat.update_layout(height=400)
    st.plotly_chart(fig_heat, use_container_width=True)


# WHAT THIS DOES:
# st.tabs creates clickable tabs within the same section.
# Treemap: box SIZE = sales volume, box COLOR = profit (red=loss, green=profit).
#   Great for spotting categories that sell a lot but lose money.
# Heatmap: shows profit margin by Region × Category.
#   Quickly spot which region-category combos are most/least profitable.
# st.dataframe shows an interactive table with sorting and searching.


# =============================================================================
# STEP 8: TOP PRODUCTS & CUSTOMERS
# =============================================================================

st.subheader("\U0001F3C6 Top Performers")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Top 10 Products by Sales**")
    top_products = filtered_df.groupby('Product Name')['Sales'].sum().nlargest(10).reset_index()
    top_products['Sales'] = top_products['Sales'].apply(lambda x: f'${x:,.0f}')
    st.dataframe(top_products, use_container_width=True, hide_index=True)

with col2:
    st.markdown("**Top 10 Customers by Sales**")
    top_customers = filtered_df.groupby('Customer Name').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Order ID': 'nunique'
    }).nlargest(10, 'Sales').reset_index()
    top_customers.columns = ['Customer', 'Sales', 'Profit', 'Orders']
    top_customers['Sales'] = top_customers['Sales'].apply(lambda x: f'${x:,.0f}')
    top_customers['Profit'] = top_customers['Profit'].apply(lambda x: f'${x:,.0f}')
    st.dataframe(top_customers, use_container_width=True, hide_index=True)


# =============================================================================
# STEP 9: YEAR-OVER-YEAR COMPARISON
# =============================================================================

st.subheader("\U0001F4C5 Year-over-Year Comparison")

yearly = filtered_df.groupby('Year').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Order ID': 'nunique',
    'Customer Name': 'nunique'
}).reset_index()
yearly.columns = ['Year', 'Sales', 'Profit', 'Orders', 'Customers']

# Calculate YoY growth
yearly['Sales_Growth'] = yearly['Sales'].pct_change() * 100
yearly['Profit_Growth'] = yearly['Profit'].pct_change() * 100

col1, col2 = st.columns(2)

with col1:
    fig_yoy_sales = px.bar(
        yearly, x='Year', y='Sales',
        text=yearly['Sales'].apply(lambda x: f'${x/1000:.0f}K'),
        color_discrete_sequence=['#2E86C1']
    )
    fig_yoy_sales.update_layout(
        title='Annual Sales',
        height=350, plot_bgcolor='white',
        yaxis=dict(title='Sales ($)', gridcolor='#f0f0f0')
    )
    fig_yoy_sales.update_traces(textposition='outside')
    st.plotly_chart(fig_yoy_sales, use_container_width=True)

with col2:
    fig_yoy_profit = px.bar(
        yearly, x='Year', y='Profit',
        text=yearly['Profit'].apply(lambda x: f'${x/1000:.0f}K'),
        color_discrete_sequence=['#28B463']
    )
    fig_yoy_profit.update_layout(
        title='Annual Profit',
        height=350, plot_bgcolor='white',
        yaxis=dict(title='Profit ($)', gridcolor='#f0f0f0')
    )
    fig_yoy_profit.update_traces(textposition='outside')
    st.plotly_chart(fig_yoy_profit, use_container_width=True)

# YoY Growth Table
st.markdown("**Year-over-Year Growth**")
display_yearly = yearly.copy()
display_yearly['Sales'] = display_yearly['Sales'].apply(lambda x: f'${x:,.0f}')
display_yearly['Profit'] = display_yearly['Profit'].apply(lambda x: f'${x:,.0f}')
display_yearly['Sales_Growth'] = display_yearly['Sales_Growth'].apply(
    lambda x: f'{x:+.1f}%' if pd.notna(x) else 'Base Year')
display_yearly['Profit_Growth'] = display_yearly['Profit_Growth'].apply(
    lambda x: f'{x:+.1f}%' if pd.notna(x) else 'Base Year')
st.dataframe(display_yearly, use_container_width=True, hide_index=True)


# =============================================================================
# STEP 10: MONTHLY SEASONALITY PATTERN
# =============================================================================

st.subheader("\U0001F4C6 Monthly Seasonality Pattern")

monthly_pattern = filtered_df.groupby(['Year', 'Month', 'Month_Name']).agg({
    'Sales': 'sum'
}).reset_index()

fig_season = px.line(
    monthly_pattern, x='Month', y='Sales', color='Year',
    markers=True,
    color_discrete_sequence=['#AED6F1', '#5DADE2', '#2E86C1', '#1A5276'],
    labels={'Month': 'Month', 'Sales': 'Sales ($)'}
)
fig_season.update_layout(
    height=400, plot_bgcolor='white',
    xaxis=dict(
        tickmode='array',
        tickvals=list(range(1, 13)),
        ticktext=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
        gridcolor='#f0f0f0'
    ),
    yaxis=dict(title='Sales ($)', gridcolor='#f0f0f0'),
    legend=dict(orientation='h', yanchor='bottom', y=1.02)
)
st.plotly_chart(fig_season, use_container_width=True)


# =============================================================================
# STEP 11: FOOTER
# =============================================================================

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #888; font-size: 14px;'>
        Built by Nithin Kumar Kokkisa | 
        <a href='https://github.com/Kokkisa'>GitHub</a> | 
        Data: Superstore Sales Dataset
    </div>
    """,
    unsafe_allow_html=True
)


# =============================================================================
# CONGRATULATIONS! YOU COMPLETED PROJECT #5
# =============================================================================
#
# WHAT YOU BUILT:
# ✅ Professional interactive dashboard
# ✅ 5 KPI cards with dynamic metrics
# ✅ 4 sidebar filters (year, region, category, segment)
# ✅ Sales & profit trend line chart
# ✅ Category breakdown (bar chart + donut chart)
# ✅ Regional performance with tabs (bar, treemap, heatmap)
# ✅ Top products & customers tables
# ✅ Year-over-year comparison with growth rates
# ✅ Monthly seasonality pattern by year
#
# HOW TO RUN:
# 1. Save as dashboard.py
# 2. pip install streamlit plotly pandas
# 3. streamlit run dashboard.py
#
# HOW TO DEPLOY (free):
# 1. Push to GitHub repo
# 2. Go to share.streamlit.io
# 3. Connect your GitHub repo
# 4. Deploy — get a public URL anyone can access!
#
# UPLOAD TO GITHUB:
# 1. New repo: sales-analytics-dashboard
# 2. Upload: dashboard.py + requirements.txt + README
# 3. Add screenshots of the dashboard
#
# NEXT: Project #6 — NLP / Text Analytics
# =============================================================================
