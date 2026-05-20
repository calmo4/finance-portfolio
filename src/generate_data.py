import numpy as np
import pandas as pd
#"random"
np.random.seed(42)

# -------------------------
# Spending model settings
# -------------------------
months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

# target monthly "typical" levels (roughly what you expect on average)
# will be used in our generations of distriibutions
target_monthly_mean = {
    "Payroll": 250_000,     # ~3M annually
    "Travel": 15_000,       # ~180k annually
    "Equipment": 25_000,    # ~300k annually
    "Operations": 12_000    # ~144k annually
}

# Variability controls (bigger = more volatile)
# - Payroll/Operations use normal standard deviations
#n(mu, sigma) aka n(0,1)
normal_sigma = {
    "Payroll": 5_000,
    "Operations": 1_200
}

# Buffers for annual budgets.
# finance-realistic:
#  build slack into volatile categories)
budget_buffer = {
    "Payroll": 0.03,
    "Travel": 0.15,
    "Equipment": 0.10,
    "Operations": 0.10
}

# -------------------------
# 2) Helper: parameters for Lognormal and Gamma
# -------------------------
#ln(X) ~ N(mu, variance ^2), can never be negative
#Good for modeling d
def lognormal_params_from_mean_cv(mean: float, cv: float):
    """
    Choose lognormal mu, sigma such that E[X]=mean and Coefficient of Variation=cv.
    cv = std/mean. Higher cv -> more right-tail.
    """
    sigma2 = np.log(1 + cv**2)
    sigma = np.sqrt(sigma2)
    mu = np.log(mean) - 0.5 * sigma2
    return mu, sigma

def gamma_params_from_mean_cv(mean: float, cv: float):
    """
    Choose gamma shape k and scale theta such that E[X]=mean and CV=cv.
    For Gamma(k, theta): mean = k*theta, var = k*theta^2 -> CV = 1/sqrt(k)
    """
    k = 1 / (cv**2)
    theta = mean / k
    return k, theta

# -------------------------
# 3) Build Budget table (auto-calculated)
# -------------------------
budget_rows = []
for cat, mean_m in target_monthly_mean.items():
    annual_expected = 12 * mean_m
    annual_budget = annual_expected * (1 + budget_buffer[cat])
    budget_rows.append({
        "Department": "CDSS - Academic & Administrative Support Unit",
        "Category": cat,
        "Annual_Budget": round(annual_budget, 2),
    })

budget = pd.DataFrame(budget_rows)
budget["Monthly_Allocation"] = (budget["Annual_Budget"] / 12).round(2)

# -------------------------
# 4) Generate Monthly Expenses (mixed distributions)
# -------------------------
rows = []
for m in months:
    # Payroll is Normal 
    payroll = np.random.normal(
        loc=target_monthly_mean["Payroll"],
        scale=normal_sigma["Payroll"]
    )
    payroll = max(0, payroll)

    # Travel: Lognormal right-skewed as it cn not be negative
    # CV ~ 0.45 gives occasional spikes but not insane
    travel_mu, travel_sigma = lognormal_params_from_mean_cv(
        mean=target_monthly_mean["Travel"],
        cv=0.45
    )
    travel = np.random.lognormal(mean=travel_mu, sigma=travel_sigma)

    # Equipment: Gamma distribution becuase purchases are expensive but not frequent
    # CV ~ 0.70 is fairly lumpy
    equip_k, equip_theta = gamma_params_from_mean_cv(
        mean=target_monthly_mean["Equipment"],
        cv=0.70
    )
    equipment = np.random.gamma(shape=equip_k, scale=equip_theta)

    # Operations: Normal distribution
    ops = np.random.normal(
        loc=target_monthly_mean["Operations"],
        scale=normal_sigma["Operations"]
    )
    ops = max(0, ops)

    rows.extend([
        {"Month": m, "Category": "Payroll", "Amount_Spent": round(payroll, 2)},
        {"Month": m, "Category": "Travel", "Amount_Spent": round(travel, 2)},
        {"Month": m, "Category": "Equipment", "Amount_Spent": round(equipment, 2)},
        {"Month": m, "Category": "Operations", "Amount_Spent": round(ops, 2)},
    ])

expenses = pd.DataFrame(rows)

# -------------------------
# 5) Save outputs
# -------------------------
budget.to_csv("budget_simulator/data/department_budget.csv", index=False)
expenses.to_csv("budget_simulator/data/monthly_expenses.csv", index=False)

print("CSV created (mixed distributions):")
print("- budget_simulator/data/department_budget.csv")
print("- budget_simulator/data/monthly_expenses.csv")

print("\nBudget preview:")
print(budget)

print("\nExpense preview:")
print(expenses.head(12))
