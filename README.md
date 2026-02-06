# Reaction Kinetics Modeling & Optimization

**Project Status:** Active | **Type:** First-Principles Simulation

## 1. Overview
This project simulates a **Series Reaction (A -> B -> C)** in a batch reactor to solve a classic chemical engineering optimization problem: maximizing yield under conflicting kinetic constraints.

Unlike "Black Box" machine learning models, this project uses **First-Principles Modeling** (Arrhenius equations & Differential Equations) to determine the optimal operating conditions.

## 2. The Engineering Problem
We are optimizing the production of **Product B** in the following pathway:
$$A \xrightarrow{k_1} B \xrightarrow{k_2} C$$

* **Reaction 1 (A->B):** High Activation Energy ($E_a = 50,000$ J/mol). Favored by High Temp.
* **Reaction 2 (B->C):** Lower Activation Energy ($E_a = 40,000$ J/mol). Represents thermal degradation (Waste).
* **Constraint:** Batch time is fixed at **60 minutes** (shift change).

## 3. Key Results
Using `scipy.optimize` and `odeint`, we determined the global maximum:

* **Optimal Temperature:** **398.6 K** (125.4 °C)
* **Predicted Yield:** **0.78 mol/L**
* **Sensitivity Analysis:** The process is **highly sensitive to Temperature** (narrow operating window) but robust to Time variations, suggesting that capital investment should focus on precise Temperature Control Units (TCUs) rather than automated timing systems.

## 4. Tech Stack
* **Python 3.14**
* **Scipy (odeint, minimize_scalar):** For solving differential equations and optimization.
* **Numpy & Matplotlib:** For vector calculus and surface mapping.

## 5. Usage
1. **Run the Simulation:** `python src/reactor_simulation.py`
2. **Find Optimal Temp:** `python src/optimize_temperature.py`
3. **Generate Heatmap:** `python src/yield_heatmap.py`