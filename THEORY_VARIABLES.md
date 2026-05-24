# Allotrope Parametric Mapping & Theory Variables

Developed by **Cheetah's Creations** 🌻  
*Published May 2026 | Analytical Document Version: 1.0.0*

This document outlines the strict physical-to-code variable mapping used across **The Carbon Exergy Matrix** simulation engines. To ensure flawless open-source reproducibility, all Python variables in `variables/graphene_brownian.py` and `variables/near_field_tunneling.py` are bound directly to established quantum and thermodynamic principles.

---

## 📂 Track 1 Mapping: `graphene_brownian.py`
This module tracks the stochastic out-of-plane buckling of freestanding monolayer graphene membranes under ambient thermal excitation ($\Delta T = 0$).

### 1. Script Parameters vs. Physical Boundary Constraints

| Python Variable | Physical Property Represented | Baseline Value | Structural Significance |
| :--- | :--- | :--- | :--- |
| `T_ambient` | Ambient Thermal Pool ($T$) | `298.15 K` ($25^\circ\text{C}$) | Governs the magnitude of the stochastic white noise forcing term via the Fluctuation-Dissipation Theorem. |
| `mass_eff` | Effective Domain Mass ($m_{eff}$) | `1.5e-22 kg` | The localized mass of a coherent graphene ripple cluster ($\approx 45,000$ carbon atoms vibrating in phase). |
| `gamma` | Intrinsic Structural Damping ($\gamma$) | `2.5e-12 kg/s` | Models the internal visco-elastic resistance and phononic dissipation within the crystalline carbon lattice. |
| `barrier_height` | Potential Energy Barrier ($E_b$) | `1.0e-20 J` | The activation energy required for a buckled graphene domain to snap/invert into its mirrored configuration. |
| `z_0` | Bistable Spatial Minimums ($\pm z_0$) | `0.5e-9 m` | The physical apex displacement ($\pm 0.5\text{ nm}$) of the naturally buckled pristine graphene sheet. |
| `electrode_gap` | Vacuum Cavity Clearance ($d_0$) | `2.0e-9 m` | The sub-micron distance separating the neutral graphene plane from the fixed asymmetric metal electrode collector. |
| `V_bias` | Electrostatic Bias Field ($V_b$) | `1.0 V` | Establishes the static voltage gradient across the gap required to convert variable capacitance into displacement current. |

### 2. Derived Mechanical-to-Electrical Transduction Equations
The instantaneous capacitance $C(t)$ of the shifting vacuum cavity behaves as a non-linear function of the atomic displacement variable $z(t)$:

$$C(t) = \frac{\varepsilon_0 \cdot A_{electrode}}{d_0 - z(t)}$$

Because the mechanical ripple shifts $z(t)$ dynamically, the resulting electrical displacement current $I(t)$ driven across the asymmetric collection boundary tracks the time-derivative of the capacitance matrix:

$$I(t) = V_{bias} \cdot \frac{dC(t)}{dt} = V_{bias} \cdot \left[ \frac{\varepsilon_0 \cdot A_{electrode}}{(d_0 - z(t))^2} \cdot \frac{dz(t)}{dt} \right]$$

---

## 📂 Track 2 Mapping: `near_field_tunneling.py`
This module simulates the near-field radiative heat transfer (NFRHT) and evanescent photon tunneling across a sub-micron vacuum gap separating an aligned carbon nanotube (CNT) emitter from a solid-state PV receiver.

### 1. Script Parameters vs. Physical Boundary Constraints

| Python Variable | Physical Property Represented | Baseline Value | Structural Significance |
| :--- | :--- | :--- | :--- |
| `T_emitter` | High-Density Carbon Core ($T_H$) | `1773.15 K` ($1500^\circ\text{C}$) | The thermal storage pool temperature (graphite block core). Governs the peak frequency of the emission spectrum. |
| `T_receiver` | Photovoltaic Sink ($T_C$) | `298.15 K` ($25^\circ\text{C}$) | The operating temperature of the static PV semiconductor layer. |
| `gap_range` | Sub-Wavelength Vacuum Gap ($d$) | `10e-9` to `2e-6 m` | Scans the spatial boundary domain from extreme near-field wave coupling ($10\text{ nm}$) out to classical far-field limits ($2\mu\text{m}$). |
| `omega` | Angular Photon Frequency ($\omega$) | `1e14` to `1.5e15 rad/s` | Constrains the simulation focus to the near-infrared band matching the structural bandgap of low-index PV substrates. |
| `transmission` | Evanescent Modal Coupling ($\mathcal{T}_\mu$) | Parameterized Curve | Computes the probability of surface plasmon-phonon polariton waves successfully tunneling across the vacuum gap before decaying. |

### 2. Quantum Amplification Variables
Classical far-field radiation is strictly capped by the Stefan-Boltzmann law, which assumes surface waves propagate out into space as free photons:

$$q_{Far-Field} = \sigma \cdot \left( T_{emitter}^4 - T_{receiver}^4 \right)$$

When the simulation gap parameter falls below the dominant thermal wavelength ($d < \lambda_{thermal}$), the near-field flux $q_{Near-Field}$ scales inversely with the gap distance ($q_{NF} \propto 1/d^2$ for surface modes). The transmission variable integrates the high spatial-frequency parallel wave-vectors ($\beta$) that are physically trapped on the carbon nanotube surface boundaries in a traditional far-field configuration:

$$\mathcal{T}_{evanescent}(\omega, \beta; d) \approx \exp(-2\beta d)$$

---

## 🛠️ Calibration & Optimization Protocols
When tuning this codebase for advanced hardware sandboxing, engineers must observe the following parametric sensitivities:

1. **Numerical Stability Thresholds (`dt`):** The integration time-step `dt` in `graphene_brownian.py` must remain at least two orders of magnitude smaller than the natural oscillation period of the carbon lattice ($\tau \approx \sqrt{m_{eff} / k_{elastic}}$). If `dt` exceeds `1e-13s`, the Euler-Maruyama algorithm will experience numerical divergence due to extreme non-linear forces at the potential boundary walls.
2. **Vacuum Gap Tolerances (`gap`):** In `near_field_tunneling.py`, as the gap parameter approaches the $10\text{ nm}$ limit, non-local quantum effects and electron tunneling begin to interface with photon transport. This model assumes a perfect macro-vacuum isolation profile across the spatial boundary matrix.
