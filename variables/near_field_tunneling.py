#!/usr/bin/env python3
"""
The Carbon Exergy Matrix: Ambient Solid-State Harvesting
Track 2: All-Carbon Near-Field Thermophotovoltaic (TPV) Cells
Engine: variables/near_field_tunneling.py

Models sub-micron evanescent photon flux and Near-Field Radiative Heat Transfer 
(NFRHT) deviations from classical far-field blackbody limits (Planck's Law)
using a parameterized wave-vector (beta) transmission coupling engine.

Developed by Cheetah's Creations 🌻 | May 2026
License: CERN-OHL-S v2.0 (Strongly Reciprocal Open Hardware)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import h, c, k as k_B, pi

def calculate_near_field_flux(
    T_emitter=1773.15,    # High-density Graphite/CNT temperature (1500°C)
    T_receiver=298.15,   # Solid-state PV receiver temperature (25°C)
    gap_range=None,      # Vacuum gap distance array in meters
    omega_steps=300,     # Frequency resolution
    beta_steps=300       # Spatial wave-vector resolution
):
    """
    Simulates quantum evanescent photon coupling across sub-micron vacuum gaps.
    Compares the near-field exergy flux against classical far-field limits.
    """
    if gap_range is None:
        # Scan from 10 nanometers to 2 microns to visualize the near-field transition
        gap_range = np.logspace(-8, -6, 40)
        
    # 1. Fundamental Constants and Bandwidth Configuration
    # Focus on the near-infrared spectrum where CNT metamaterials emit strongly
    omega_min = 1e14      # Rad/s
    omega_max = 1.5e15    # Rad/s
    omega = np.linspace(omega_min, omega_max, omega_steps)
    
    # Calculate Far-Field Stefan-Boltzmann Baseline for comparison
    # q_far = sigma * (T_e^4 - T_r^4) where sigma = 5.670374e-8
    sigma = 5.670374419e-8
    q_far_field = sigma * (T_emitter**4 - T_receiver**4)
    
    # 2. Compute Mean Energy of Planck Oscillators (Theta)
    # Theta(omega, T) = (hbar * omega) / (exp(hbar * omega / k_B * T) - 1)
    hbar = h / (2.0 * pi)
    
    theta_emitter = (hbar * omega) / (np.exp((hbar * omega) / (k_B * T_emitter)) - 1.0)
    theta_receiver = (hbar * omega) / (np.exp((hbar * omega) / (k_B * T_receiver)) - 1.0)
    theta_delta = theta_emitter - theta_receiver  # Net exchange energy pool
    
    # 3. Near-Field Integration Loop over Vacuum Gap Distances
    q_near_field = np.zeros(len(gap_range))
    
    print("Initializing Near-Field Quantum Tunneling Engine...")
    print(f"Graphite Emitter Source: {T_emitter - 273.15:.1f}°C")
    print(f"Photovoltaic Receiver Sink: {T_receiver - 273.15:.1f}°C")
    print(f"Classical Far-Field Limit: {q_far_field / 1000:.2f} kW/m²")
    
    for g_idx, gap in enumerate(gap_range):
        total_flux = 0.0
        
        # Define parallel/spatial wave-vector scan (beta) normalized to free-space wave-vector k_0
        # For near-field tunneling, evanescent waves dominate where beta > k_0
        beta_min = 0.01
        beta_max = 10.0 / gap  # Evanescent domain expands exponentially as the gap narrows
        beta = np.linspace(beta_min, beta_max, beta_steps)
        d_beta = beta[1] - beta[0]
        
        for w_idx, w in enumerate(omega):
            k_0 = w / c
            
            # Parameterized Transmission Coefficient T_mu (wave coupling probability)
            # Models the evanescent decay and resonance match of aligned carbon nanotubes
            # Transmissivity peaks when beta >> k_0 and decays as exp(-2 * beta * gap)
            transmission = np.exp(-2.0 * beta * gap) * (beta**3 / (beta**3 + k_0**3))
            
            # Core Integrand: (beta / 4*pi^2) * Delta_Theta * Transmission
            integrand = (beta / (4.0 * pi**2)) * theta_delta[w_idx] * transmission
            
            # Trapezoidal integration step across spatial wave-vectors
            total_flux += np.sum(integrand) * d_beta
            
        # Frequency integration step
        d_omega = omega[1] - omega[0]
        q_near_field[g_idx] = total_flux * d_omega

    return gap_range, q_near_field, q_far_field

if __name__ == "__main__":
    # Execute the near-field simulation
    gaps, q_nf, q_ff = calculate_near_field_flux()
    
    # 4. Classical Deviation Multiplier
    enhancement_factor = q_nf / q_ff
    
    # 5. Visualization Suite
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
    fig.suptitle("The Carbon Exergy Matrix: Evanescent Photon Tunneling Sandbox\n(Cheetah's Creations 🌻)", fontsize=12, fontweight='bold')
    
    # Top Plot: Absolute Radiative Heat Flux vs Gap Distance
    ax1.loglog(gaps * 1e9, q_nf / 1000, color='#d35400', linewidth=2, label='Near-Field Flux (Quantum Tunneling)')
    ax1.axhline(q_ff / 1000, color='#7f8c8d', linestyle='--', linewidth=1.5, label='Classical Far-Field Limit (Planck/Stefan-Boltzmann)')
    ax1.set_ylabel("Net Heat Flux ($kW/m^2$)")
    ax1.grid(True, which="both", linestyle=':', alpha=0.6)
    ax1.legend(loc='lower left')
    ax1.set_title("Radiative Heat Transfer Scaling Beyond Classical Thresholds", fontsize=10)
    
    # Bottom Plot: Near-Field Enhancement Factor Multiplier
    ax2.loglog(gaps * 1e9, enhancement_factor, color='#2980b9', linewidth=2, label='Exergy Extraction Multiplier')
    ax2.axhline(1.0, color='#e74c3c', linestyle=':', alpha=0.7)
    ax2.set_xlabel("Vacuum Gap Distance (nanometers)")
    ax2.set_ylabel("Enhancement Factor ($q_{NF} / q_{FF}$)")
    ax2.grid(True, which="both", linestyle=':', alpha=0.6)
    ax2.legend(loc='lower left')
    ax2.set_title("Quantum Amplification Scale ($Bypassing\\ Planck's\\ Law$)", fontsize=10)
    
    plt.tight_layout()
    plt.show()
