import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.title("Academic Budget Forecasting Dashboard")

# Load data
analysis = pd.read_csv("data/processed/budget_analysis.csv")
expenses = pd.read_csv("data/raw/monthly_expenses.csv")

# Category filter
category_options = ["All"] + list(analysis["Category"].unique())

selected_category = st.selectbox(
    "Select a budget category",
    category_options
)

if selected_category != "All":
    analysis = analysis[analysis["Category"] == selected_category]
    expenses = expenses[expenses["Category"] == selected_category]

# Scenario simulation sliders
st.sidebar.header("Scenario Simulation")

payroll_adjustment = st.sidebar.slider("Payroll Adjustment (%)", -20, 20, 0)
travel_adjustment = st.sidebar.slider("Travel Adjustment (%)", -20, 20, 0)
equipment_adjustment = st.sidebar.slider("Equipment Adjustment (%)", -20, 20, 0)
operations_adjustment = st.sidebar.slider("Operations Adjustment (%)", -20, 20, 0)

adjustments = {
    "Payroll": payroll_adjustment,
    "Travel": travel_adjustment,
    "Equipment": equipment_adjustment,
    "Operations": operations_adjustment
}

analysis["Adjusted_Forecast"] = analysis.apply(
    lambda row: row["Forecast_Annual_Spend"] * (1 + adjustments[row["Category"]] / 100),
    axis=1
)

analysis["Adjusted_Variance"] = analysis["Adjusted_Forecast"] - analysis["Annual_Budget"]
analysis["Adjusted_Overspend"] = analysis["Adjusted_Variance"] > 0

# KPI calculations
total_budget = analysis["Annual_Budget"].sum()
total_spent = analysis["Amount_Spent"].sum()
forecast_spend = analysis["Adjusted_Forecast"].sum()
remaining_budget = total_budget - forecast_spend

# KPI cards
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Budget", f"${total_budget:,.0f}")
col2.metric("Amount Spent", f"${total_spent:,.0f}")
col3.metric("Adjusted Forecast", f"${forecast_spend:,.0f}")
col4.metric("Projected Remaining", f"${remaining_budget:,.0f}")

# Main chart
st.subheader("Budget vs Adjusted Forecast")

budget_fig = go.Figure()

budget_fig.add_trace(go.Bar(
    x=analysis["Category"],
    y=analysis["Annual_Budget"],
    name="Budget"
))

budget_fig.add_trace(go.Bar(
    x=analysis["Category"],
    y=analysis["Adjusted_Forecast"],
    name="Adjusted Forecast"
))

budget_fig.update_layout(
    barmode="group",
    xaxis_title="Category",
    yaxis_title="Amount ($)"
)

st.plotly_chart(budget_fig, use_container_width=True)

# Executive summary
st.subheader("Executive Summary")

for _, row in analysis.iterrows():
    if row["Adjusted_Overspend"]:
        st.warning(
            f"{row['Category']} is projected to exceed budget by "
            f"${row['Adjusted_Variance']:,.0f}."
        )
    else:
        st.success(
            f"{row['Category']} is projected to finish under budget by "
            f"${abs(row['Adjusted_Variance']):,.0f}."
        )

# Monthly spending trend
st.subheader("Monthly Spending Trend")

monthly_summary = expenses.groupby("Month")["Amount_Spent"].sum().reset_index()

trend_fig = go.Figure()

trend_fig.add_trace(go.Scatter(
    x=monthly_summary["Month"],
    y=monthly_summary["Amount_Spent"],
    mode="lines+markers",
    name="Monthly Spend"
))

trend_fig.update_layout(
    xaxis_title="Month",
    yaxis_title="Amount ($)"
)

st.plotly_chart(trend_fig, use_container_width=True)

# Data table
st.subheader("Budget Analysis Table")
st.dataframe(analysis)
