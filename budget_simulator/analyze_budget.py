import pandas as pd
# Load data
budget = pd.read_csv("budget_simulator/data/department_budget.csv")
expenses = pd.read_csv("budget_simulator/data/monthly_expenses.csv")

# Total spent per category (sum of 12 months)
total_spent = expenses.groupby("Category")["Amount_Spent"].sum().reset_index()

# Merge with budget
analysis = budget.merge(total_spent, on="Category")

# Calculate remaining + variance
analysis["Remaining_Budget"] = analysis["Annual_Budget"] - analysis["Amount_Spent"]
analysis["Variance"] = analysis["Amount_Spent"] - analysis["Annual_Budget"]

print("\n=== Budget vs Actual Analysis ===\n")
print(analysis)
##############################



##############################




# ---- Year-End Forecast ----

# Average monthly spend per category
monthly_avg = expenses.groupby("Category")["Amount_Spent"].mean().reset_index()
monthly_avg.rename(columns={"Amount_Spent": "Avg_Monthly_Spend"}, inplace=True)

# Merge with analysis table
analysis = analysis.merge(monthly_avg, on="Category")

# Forecast annual spend (based on average monthly)
analysis["Forecast_Annual_Spend"] = analysis["Avg_Monthly_Spend"] * 12

# Forecast variance
analysis["Forecast_Variance"] = analysis["Forecast_Annual_Spend"] - analysis["Annual_Budget"]

# Forecast overspend flag
analysis["Forecast_Overspend"] = analysis["Forecast_Variance"] > 0

print("\n=== Forecast Analysis ===\n")
print(analysis[[
    "Category",
    "Annual_Budget",
    "Forecast_Annual_Spend",
    "Forecast_Variance",
    "Forecast_Overspend"
]])
###################


###################

print("\n=== Executive Financial Summary ===\n")

for _, row in analysis.iterrows():
    if row["Forecast_Overspend"]:
        print(f"{row['Category']}: Projected to exceed budget by ${row['Forecast_Variance']:.2f}. Review spending controls.")
    else:
        print(f"{row['Category']}: On track. Projected underspend of ${abs(row['Forecast_Variance']):.2f}.")
