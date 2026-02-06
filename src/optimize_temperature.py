import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar
from reactor_simulation import run_simulation  # Reuse our engine!


# --- 1. DEFINE THE OBJECTIVE ---
# The solver tries to find 'T' that makes this function return the Smallest number.
# Since we want Maximum Yield, we return (-1 * Yield).
def objective_function(T_kelvin):
    # Constraint: We assume a fixed batch time of 60 minutes
    fixed_time = 60

    # Run the simulation
    # We only need the final point, so we ask for the value at t=60
    # Note: run_simulation returns (time_array, concentration_matrix)
    t, solution = run_simulation(T_kelvin, run_time_min=fixed_time)

    # Get the FINAL concentration of B (at 60 mins)
    # solution is [Ca, Cb, Cc], so index 1 is Cb. -1 is the last time step.
    final_Cb = solution[-1, 1]

    # Return negative because 'minimize' searches for lows
    return -1.0 * final_Cb


# --- 2. RUN THE OPTIMIZER ---
if __name__ == "__main__":
    print("🤖 Starting Optimizer: Searching for Best Temperature (Fixed Time = 60 min)...")

    # minimize_scalar uses the "Brent" method to find the minimum of our function
    # bounds=[300, 500] tells it to only look between 300K and 500K
    result = minimize_scalar(objective_function, bounds=(300, 500), method='bounded')

    optimal_T = result.x
    max_yield = -1.0 * result.fun  # Flip the sign back to positive

    print(f"\n✅ Optimization Complete!")
    print(f"   Optimal Temperature: {optimal_T:.2f} K")
    print(f"   Predicted Yield at 60 min: {max_yield:.4f} mol/L")

    # --- 3. VERIFICATION PLOT ---
    # Let's prove it by plotting the profile at this exact temperature
    t_opt, sol_opt = run_simulation(optimal_T, run_time_min=60)
    Cb_opt = sol_opt[:, 1]  # Product B curve

    plt.figure(figsize=(10, 6))
    plt.plot(t_opt, Cb_opt, label=f'Optimal Run ({optimal_T:.1f} K)', color='green', linewidth=3)
    plt.title(f"Optimized Process: Peak hits exactly at Shift Change", fontsize=14)
    plt.xlabel("Time (minutes)")
    plt.ylabel("Concentration B (mol/L)")
    plt.axvline(60, color='red', linestyle='--', label='Shift Change (60 min)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()