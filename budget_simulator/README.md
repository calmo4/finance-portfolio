# Academic Unit Budget Simulation & Forecasting (CDSS)

Simulated end-to-end financial planning workflow for a mid-size university unit (~$3–4M annual operating budget). The project generates realistic monthly expenditures using mixed probability distributions, then produces budget vs. actual variance reporting and a year-end forecast with executive-style narrative output.

## Why this project
This mirrors higher education finance workflows: budgeting, expenditure monitoring, burn-rate forecasting, and communicating results clearly for decision-making.

## What it does
1. **Generates data (simulated)**
   - Creates a budget by category with built-in buffers for volatility
   - Generates monthly “actuals” using mixed distributions:
     - **Payroll:** Normal (stable)
     - **Travel:** Lognormal (right-skew; occasional spikes)
     - **Equipment:** Gamma (lumpy purchases)
     - **Operations:** Normal (moderately stable)

2. **Analyzes and reports**
   - Budget vs. Actual variance by category
   - Remaining budget and overspend flags
   - Forecast annual spend from average monthly burn rate
   - Prints an executive summary for finance leadership

## Files
- `generate_data.py` — creates:
  - `data/department_budget.csv`
  - `data/monthly_expenses.csv`
- `analyze_budget.py` — creates:
  - `data/budget_analysis_report.csv` (plus printed tables + executive summary)

## How to run
From the project root (`finance_portfolio`):

```bash
python3 budget_simulator/generate_data.py
python3 budget_simulator/analyze_budget.py
