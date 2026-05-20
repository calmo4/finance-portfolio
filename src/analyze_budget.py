import pandas as pd
import matplotlib.pyplot as plt

# Load data
budget = pd.read_csv("data/raw/department_budget.csv")
expenses = pd.read_csv("data/raw/monthly_expenses.csv")
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


###################


###################

# Plot Budget vs Forecast

plt.figure(figsize=(8,5))

x = range(len(analysis["Category"]))
width = 0.4

plt.bar(
    [i - width/2 for i in x],
    analysis["Annual_Budget"],
    width=width,
    label="Budget"
)

plt.bar(
    [i + width/2 for i in x],
    analysis["Forecast_Annual_Spend"],
    width=width,
    label="Forecast"
)

plt.xticks(x, analysis["Category"], rotation=45)

plt.xlabel("Category")
plt.ylabel("Amount ($)")
plt.title("Budget vs Forecast by Category")

plt.legend()
plt.tight_layout()

# Save chart
plt.savefig("outputs/charts/budget_vs_forecast.png")

plt.show()

print("\nSaved chart to outputs/charts/budget_vs_forecast.png")


# Save processed analysis
analysis.to_csv("data/processed/budget_analysis.csv", index=False)

print("\nCool cool saved analysis to data/processed/budget_analysis.csv")