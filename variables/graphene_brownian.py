#!/usr/bin/env python3
"""
The Carbon Exergy Matrix: Ambient Solid-State Harvesting
Track 1: Freestanding Graphene Fluctuation Harvesters (Brownian Kinetic DC)
Engine: variables/graphene_brownian.py

Simulates the bistable out-of-plane buckling dynamics of a freestanding graphene
membrane domain under ambient thermal noise, using numerical integration of the
non-linear Ito-Langevin equation, and calculates the resulting displacement current.

Developed by Cheetah's Creations 🌻 | May 2026
License: CERN-OHL-S v2.0 (Strongly Reciprocal Open Hardware)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import k as k_B

def simulate_graphene_harvester(
    T_ambient=298.15,    # Ambient temperature in Kelvin (25°C)
    t_max=1e-9,          # Maximum simulation time (1 nanosecond sandbox)
    dt=1e-14,            # Time step (10 femtoseconds for integration stability)
    mass_eff=1.5e-22,    # Effective mass of vibrating graphene domain (kg)
    gamma=2.5e-12,       # Intrinsic damping coefficient (kg/s)
    barrier_height=1e-20,# Intrinsic potential energy barrier height (Joules)
    z_0=0.5e-9,          # Bistable potential minimum positions (±0.5 nm)
    electrode_gap=2e-9,  # Distance to fixed asymmetric sub-micron electrode (meters)
    electrode_area=1e-14,# Effective capacitive coupling surface area (m^2)
    V_bias=1.0           # Applied bias voltage across the vacuum gap (Volts)
):
    """
    Numerically integrates the non-linear stochastic differential equation of 
    the graphene membrane domain and extracts the raw capacitive displacement current.
    """
    # 1. Initialize Time and Arrays
    num_steps = int(t_max / dt)
    time_array = np.linspace(0, t_max, num_steps)
    
    z = np.zeros(num_steps)      # Out-of-plane displacement (meters)
    v = np.zeros(num_steps)      # Particle velocity (m/s)
    
    # Initial state: start at one of the buckled minimums with zero velocity
    z[0] = z_0
    v[0] = 0.0
    
    # 2. Physics Parameter Derivations
    # Bistable potential: V(z) = A*z^4 - B*z^2
    # Setting potential minimum at ±z_0 and barrier height at z=0 yields:
    A = barrier_height / (z_0**4)
    B = 2.0 * barrier_height / (z_0**2)
    
    # Stochastic forcing scale (Fluctuation-Dissipation Theorem)
    # Thermal force variance: 2 * gamma * k_B * T
    stochastic_scale = np.sqrt(2.0 * gamma * k_B * T_ambient / dt)
    
    # Permittivity of vacuum (F/m)
    epsilon_0 = 8.8541878128e-12 
    
    print("Initializing Carbon Exergy Matrix Simulation...")
    print(f"Ambient Temperature: {T_ambient - 273.15:.2f}°C")
    print(f"Stochastic Thermal Force Scale: {stochastic_scale:.3e} N")
    
    # 3. Euler-Maruyama Integration Loop
    for t in range(0, num_steps - 1):
        # Calculate non-linear restoring force from bistable potential: F = -dV/dz
        # dV/dz = 4*A*z^3 - 2*B*z
        force_potential = -(4.0 * A * (z[t]**3) - 2.0 * B * z[t])
        
        # Calculate intrinsic damping force (viscous drag of atomic structure)
        force_damping = -gamma * v[t]
        
        # Sample stochastic Gaussian white noise
        xi = np.random.normal(0.0, 1.0)
        force_thermal = stochastic_scale * xi
        
        # Net acceleration
        acceleration = (force_potential + force_damping + force_thermal) / mass_eff
        
        # Step velocity and position
        v[t+1] = v[t] + acceleration * dt
        z[t+1] = z[t] + v[t] * dt
        
    # 4. Transduction Profile: Capacitance & Displacement Current Calculation
    # C(t) = (epsilon_0 * Area) / (electrode_gap - z(t))
    # As the membrane ripples, the changing gap modulates the capacitance.
    capacitance = (epsilon_0 * electrode_area) / (electrode_gap - z)
    
    # Numerical derivative of capacitance: dC/dt
    dC_dt = np.diff(capacitance) / dt
    # Pad end to maintain matching array dimensions
    dC_dt = np.append(dC_dt, dC_dt[-1])
    
    # Displacement Current: I(t) = V_bias * (dC/dt)
    current_displacement = V_bias * dC_dt
    
    return time_array, z, current_displacement

if __name__ == "__main__":
    # Execute the 1ns simulation sandbox
    time, displacement, current = simulate_graphene_harvester()
    
    # 5. Visualization Suite
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    fig.suptitle("The Carbon Exergy Matrix: Graphene Fluctuation Sandbox\n(Cheetah's Creations 🌻)", fontsize=12, fontweight='bold')
    
    # Top Plot: Atomic Displacement showing bistable buckling jumps
    ax1.plot(time * 1e9, displacement * 1e9, color='#2c3e50', linewidth=1.5, label='Membrane Position')
    ax1.axhline(0.5, color='#e74c3c', linestyle='--', alpha=0.5, label='Stable Buckle Minimums')
    ax1.axhline(-0.5, color='#e74c3c', linestyle='--', alpha=0.5)
    ax1.set_ylabel("Displacement (nm)")
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.legend(loc='upper right')
    ax1.set_title("Atomic Domain Brownian Dynamics (Out-of-Plane Ripple Phase)", fontsize=10)
    
    # Bottom Plot: Generated Raw Transduction Current
    ax2.plot(time * 1e9, current * 1e6, color='#27ae60', linewidth=1.2, label='Raw Displacement Current')
    ax2.set_xlabel("Time (nanoseconds)")
    ax2.set_ylabel("Current (μA)")
    ax2.grid(True, linestyle=':', alpha=0.6)
    ax2.legend(loc='upper right')
    ax2.set_title("Induced Displacement Current Across Asymmetric Sub-Micron Electrode", fontsize=10)
    
    plt.tight_layout()
    plt.show()
