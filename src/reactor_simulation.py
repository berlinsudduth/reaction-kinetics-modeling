import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# --- 1. PHYSICAL CONSTANTS ---
R = 8.314  # Gas constant (J/mol*K)

# Reaction 1: A -> B (High Barrier, High Payoff)
A1 = 20000  # Pre-exponential factor (1/min)
Ea1 = 50000  # Activation Energy (J/mol)

# Reaction 2: B -> C (Lower Barrier, Waste)
A2 = 10000  # Pre-exponential factor (1/min)
Ea2 = 40000  # Activation Energy (J/mol)


# --- 2. THE DERIVATIVE FUNCTION (The "Engine") ---
def reactor_odes(concentrations, t, T):
    """
    Calculates the change in concentration (dC/dt) for A, B, and C.
    Arguments:
        concentrations: List [Ca, Cb, Cc]
        t: Time (minutes)
        T: Temperature (Kelvin) - Fixed for now
    """
    Ca, Cb, Cc = concentrations

    # Arrhenius Equation: k = A * exp(-Ea / RT)
    k1 = A1 * np.exp(-Ea1 / (R * T))
    k2 = A2 * np.exp(-Ea2 / (R * T))

    # Rate Laws (First Order)
    r1 = k1 * Ca  # Rate of A -> B
    r2 = k2 * Cb  # Rate of B -> C

    # Mass Balances (The Differential Equations)
    dCa_dt = -r1  # A is consumed
    dCb_dt = r1 - r2  # B is made by r1, consumed by r2
    dCc_dt = r2  # C is made by r2

    return [dCa_dt, dCb_dt, dCc_dt]


# --- 3. RUN THE SIMULATION ---
def run_simulation(T_kelvin, run_time_min=100):
    # Initial Conditions: Pure A at 1.0 mol/L
    y0 = [1.0, 0.0, 0.0]  # [Ca, Cb, Cc]

    # Time steps (0 to run_time)
    t = np.linspace(0, run_time_min, 100)

    # Solve the ODEs
    # args=(T_kelvin,) passes the temperature to the function
    solution = odeint(reactor_odes, y0, t, args=(T_kelvin,))

    return t, solution


# --- 4. VISUALIZATION ---
if __name__ == "__main__":
    # Let's test a "Cold" run and a "Hot" run
    temp_test = 420  # Kelvin (Try changing this!)

    time, data = run_simulation(temp_test)
    Ca = data[:, 0]
    Cb = data[:, 1]
    Cc = data[:, 2]

    # Find Max B (The Yield)
    max_B = np.max(Cb)
    time_at_max = time[np.argmax(Cb)]

    plt.figure(figsize=(10, 6))
    plt.plot(time, Ca, label='[A] Reactant', linestyle='--')
    plt.plot(time, Cb, label='[B] Product', linewidth=3, color='green')
    plt.plot(time, Cc, label='[C] Waste', color='red')

    plt.title(f"Batch Reactor Profile at {temp_test} K", fontsize=14)
    plt.xlabel("Time (minutes)")
    plt.ylabel("Concentration (mol/L)")
    plt.axvline(time_at_max, color='gray', linestyle=':', label=f'Max Yield ({max_B:.2f})')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

    print(f"✅ Simulation Complete at {temp_test} K")
    print(f"🏆 Maximum Yield of B: {max_B:.3f} mol/L at {time_at_max:.1f} minutes")