import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- Page Configuration ---
st.set_page_config(page_title="Sovereign Debt Stress-Test", layout="wide")

st.title("🏛️ Sovereign Debt High-Fidelity Simulator")
st.markdown("""
This model uses a **Recursive Stochastic Equation** with correlated shocks to evaluate debt sustainability.
Formula: $d_t = d_{t-1} \\frac{1 + \\bar{r} + \\epsilon_{r,t}}{1 + \\bar{g} + \\epsilon_{g,t}} - pb_t$
""")

# --- Sidebar: Correlated Scenarios ---
st.sidebar.header("Scenario Presets")

# Callback to update session state
def load_scenario(debt, growth, interest, corr):
    st.session_state.initial_debt = debt
    st.session_state.avg_growth = growth
    st.session_state.avg_interest = interest
    st.session_state.correlation = corr

# Scenario Buttons
col1, col2 = st.sidebar.columns(2)
if col1.button("Stable Economy"):
    load_scenario(60.0, 3.0, 2.0, 0.2)
if col2.button("Fiscal Crisis"):
    load_scenario(110.0, -1.5, 6.0, -0.7)

# --- Parameters ---
if 'initial_debt' not in st.session_state:
    load_scenario(110.0, 1.2, 3.0, -0.3)

initial_debt = st.sidebar.slider("Starting Debt-to-GDP (%)", 40.0, 160.0, st.session_state.initial_debt)
avg_growth = st.sidebar.slider("Mean GDP Growth (%)", -5.0, 7.0, st.session_state.avg_growth) / 100
avg_interest = st.sidebar.slider("Mean Interest Rate (%)", 0.0, 12.0, st.session_state.avg_interest) / 100
correlation = st.sidebar.slider("Growth-Interest Correlation (ρ)", -1.0, 1.0, st.session_state.correlation)
volatility = st.sidebar.slider("Economic Volatility (σ)", 0.5, 5.0, 1.5) / 100
primary_bal = st.sidebar.slider("Primary Balance/GDP (%)", -5.0, 5.0, -1.0) / 100

# --- Monte Carlo Engine with Multivariate Normal Shocks ---
years = 5
sims = 200
results = np.zeros((sims, years + 1))
results[:, 0] = initial_debt

# Define Covariance Matrix for Correlated Shocks
# Growth vol vs Interest rate vol (fixed at 1% for realism)
cov_matrix = [
    [volatility**2, correlation * volatility * 0.01],
    [correlation * volatility * 0.01, 0.01**2]
]

for i in range(sims):
    shocks = np.random.multivariate_normal([0, 0], cov_matrix, years)
    for t in range(years):
        g_t = avg_growth + shocks[t, 0]
        r_t = avg_interest + shocks[t, 1]
        
        # Recursive Equation
        results[i, t+1] = results[i, t] * ((1 + r_t) / (1 + g_t)) - (primary_bal * 100)

# --- Visualization ---
fig, ax = plt.subplots(figsize=(12, 6))
time_range = np.arange(years + 1)

# Plotting with a "Fan Chart" effect
for i in range(sims):
    ax.plot(time_range, results[i, :], color='royalblue', alpha=0.08)

# Highlight Statistics
median_path = np.median(results, axis=0)
ax.plot(time_range, median_path, color='navy', linewidth=3, label='Median Projection')
ax.axhline(y=120, color='crimson', linestyle='--', label='Critical Threshold (120%)')

ax.set_title("Stochastic Debt Trajectory (5-Year Horizon)", fontsize=14)
ax.set_ylabel("Debt-to-GDP Ratio (%)")
ax.set_xlabel("Years")
ax.legend(loc='upper left')
ax.grid(True, alpha=0.2)

# --- Output Layout ---
st.pyplot(fig)

risk_col, stats_col = st.columns(2)
final_debt = results[:, -1]
prob_stress = (final_debt > 120).sum() / sims * 100

with risk_col:
    st.metric("Sustainability Risk Score", f"{prob_stress:.1f}%")
    if prob_stress > 30:
        st.error("⚠️ HIGH RISK: High probability of insolvency.")
    else:
        st.success("✅ STABLE: Debt is likely sustainable.")

with stats_col:
    st.metric("Expected Debt Level", f"{np.mean(final_debt):.1f}%")
    st.write(f"95th Percentile (Worst Case): {np.percentile(final_debt, 95):.1f}%")
