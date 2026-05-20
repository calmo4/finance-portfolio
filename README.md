## Live Demo

https://academic-dashboard-budget.streamlit.app/




# Academic Budget Forecasting Dashboard

Interactive financial planning dashboard for a simulated academic unit operating budget of approximately **$3.8M**. The project generates synthetic monthly expense data, analyzes budget variance, forecasts year-end spending, and provides scenario simulation through a Streamlit dashboard.

## Why this project

This project mirrors real finance and operations workflows: budget tracking, burn-rate forecasting, scenario planning, and executive reporting. It is designed to show how data can support financial decision-making for departments, nonprofits, or academic units.

## Features

- Generates simulated monthly expense data across Payroll, Travel, Equipment, and Operations
- Models realistic spending patterns using normal, lognormal, and gamma distributions
- Calculates budget vs. actual variance by category
- Forecasts year-end spending based on monthly burn rate
- Provides interactive category filtering
- Includes scenario sliders for adjusted spending assumptions
- Displays KPI cards, dynamic charts, and executive-style summaries

## Project Structure

```text
budget_forecasting_dashboard/
├── app/
│   └── dashboard.py
├── data/
│   ├── raw/
│   │   ├── department_budget.csv
│   │   └── monthly_expenses.csv
│   └── processed/
│       └── budget_analysis.csv
├── outputs/
│   └── charts/
│       └── budget_vs_forecast.png
├── src/
│   ├── generate_data.py
│   └── analyze_budget.py
├── README.md
└── requirements.txt


****How to run****

Install dependencies:

pip3 install -r requirements.txt

Generate the simulated data:

python3 src/generate_data.py

Run the budget analysis pipeline:

python3 src/analyze_budget.py

Launch the dashboard:

python3 -m streamlit run app/dashboard.py
Tech Stack
Python
pandas
matplotlib
Plotly
Streamlit
Dashboard Overview

This dashboard includes:

Total budget, amount spent, adjusted forecast, and projected remaining budget
Budget vs. adjusted forecast comparison
Scenario simulation sliders for category-level spending changes
Monthly spending trends
Executive summaries showing projected underspend or overspend
Detailed analysis table

Key Takeaways

This project demonstrates an end-to-end analytics workflow: data generation, processing, forecasting, visualization, and interactive dashboard!!!!!