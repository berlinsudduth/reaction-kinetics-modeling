import numpy as np
import matplotlib.pyplot as plt
from reactor_simulation import run_simulation


def generate_yield_surface():
    # 1. Define the Grid
    # We test Temperatures from 300K to 500K
    T_range = np.linspace(300, 500, 50)
    # We test Batch Times from 0 to 100 minutes
    time_range = np.linspace(0, 100, 50)

    # Create empty matrix to store Yield results
    yield_matrix = np.zeros((len(T_range), len(time_range)))

    print("🗺️  Mapping the Yield Surface (Running 2,500 simulations)...")

    # 2. Run the Grid Search (Nested Loop)
    for i, T in enumerate(T_range):
        for j, t_stop in enumerate(time_range):
            # Run simulation at this Temp
            # We run long enough (100 min) to cover all time points
            # But efficiently, we can just run ONCE per Temp and slice the data
            pass

            # Optimization: Instead of running odeint 50 times inside the inner loop,
        # we run it ONCE per Temperature for the full 100 mins.
        t_sim, sol_sim = run_simulation(T, run_time_min=100)
        Cb_sim = sol_sim[:, 1]

        # Interpolate to find exact yields at our specific grid times
        # (This aligns the data perfectly to our heatmap grid)
        yield_matrix[i, :] = np.interp(time_range, t_sim, Cb_sim)

    # 3. Create the Heatmap
    plt.figure(figsize=(10, 8))

    # Contour Plot
    # X=Time, Y=Temp, Z=Yield
    X, Y = np.meshgrid(time_range, T_range)
    cp = plt.contourf(X, Y, yield_matrix, levels=20, cmap='viridis')
    plt.colorbar(cp, label='Concentration of B (mol/L)')

    # Add the "Optimal Point" marker (from your previous script)
    plt.scatter(60, 398.56, color='red', s=100, label='Optimal Setpoint (60min, 398K)', edgecolors='white')

    plt.title("Reactor Operating Map: The 'Sweet Spot'", fontsize=14)
    plt.xlabel("Batch Time (minutes)")
    plt.ylabel("Temperature (K)")
    plt.axvline(60, color='white', linestyle='--', alpha=0.5, label='Shift Change Constraint')
    plt.legend()
    plt.savefig('../images/yield_heatmap.png', dpi=300)
    print("📸 Saved heatmap to images/yield_heatmap.png")
    plt.show()


if __name__ == "__main__":
    generate_yield_surface()