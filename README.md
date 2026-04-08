# 🏛️ Sovereign Risk Monte Carlo Simulator

An interactive **sovereign debt sustainability simulator** built using Monte Carlo methods.  
This model captures stochastic growth and interest rate dynamics with correlated shocks to evaluate fiscal risk and debt stability under different policy scenarios.

---

## 📊 Overview

This project simulates the evolution of a country’s **debt-to-GDP ratio** using a recursive macroeconomic framework:

d(t) = d(t-1) × (1 + r) / (1 + g) − pb

Where:
- \(d_t\): Debt-to-GDP ratio  
- \(r_t\): Interest rate  
- \(g_t\): GDP growth rate  
- \(pb_t\): Primary balance  

The model incorporates **correlated stochastic shocks**, allowing realistic crisis and stability scenarios.

---

## ⚙️ Features

- 📈 Monte Carlo simulation (200+ scenarios)
- 🔗 Correlated growth–interest rate shocks  
- 🎛️ Interactive controls via Streamlit  
- 🌪️ Fan chart visualization of debt trajectories  
- ⚠️ Probability-based fiscal stress indicator (>120% debt)  
- 📉 Scenario presets: Stable Economy vs Fiscal Crisis  

---
## 📷 Example Output

### 🔹 Interactive Dashboard
<img src="https://github.com/user-attachments/assets/c7d21f42-7de1-48a4-9b55-17fecbaf0b16" width="900"/>

### 🔹 Debt Trajectory & Risk Metrics
<img src="https://github.com/user-attachments/assets/43360658-604b-4bd8-9d2f-625ca939c270" width="900"/>

---
## 🚀 How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
