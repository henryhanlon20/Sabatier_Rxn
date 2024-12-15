import cantera as ct
import numpy as np
import matplotlib.pyplot as plt

"""
Trying different molar ratios
Equilibrium Calculations of the Sabatier Reaction
Objective: determine how equilibrium products vary depending on reactant molar ratio, temperature, and pressure. 
Reactants: CO2, H2
Products: CH4, H2O

Stoichiometric Coefficients:
1x CO2, 4x H2; 1x CH4, 2x H2O
"""

# Realistic Temp and Pressure domains
Tmin = 298  # K
Tmax = 700  # K
Pmin = 100000  # 100 kPa
Pmax = 3000000  # 3 MPa
T = np.linspace(Tmin, Tmax, 6)  
P = np.linspace(Pmin, Pmax, 50)  

#range of molar ratios for CO2 and H2
molar_ratios = [
    (0.1, 0.9), 
    (0.15, 0.85),
    (0.2, 0.8),  
    (0.25, 0.75),  
    (0.33, 0.67), 
    (0.4, 0.6), 
]

mix = ct.Solution('gri30.yaml')

def final_methane(gas, temperature, pressure, mole_CO2, mole_H2):
    gas.TP = temperature, pressure
    mole_fractions = {'CO2': mole_CO2, 'H2': mole_H2}
    gas.X = mole_fractions
    # Allow solution to run to equilibrium
    gas.equilibrate('TP')
    methane_index = gas.species_index('CH4')
    X_CH4 = gas.X[methane_index]
    return X_CH4

rows = (len(molar_ratios)+2)// 3  #calc the display for 3 graphs per row
fig, axes = plt.subplots(rows, 3, figsize=(18, 6 * rows), constrained_layout=True)
axes = axes.flatten()

#looping over molar ratios and disp the plots
for idx, molar_ratio in enumerate(molar_ratios):
    X_CO2, X_H2 = molar_ratio
    methane_yield = np.zeros((len(T), len(P)))
    for i, temp in enumerate(T):
        for j, pres in enumerate(P):
            methane_yield[i, j] = final_methane(mix, T[i], P[j], X_CO2, X_H2)

    #plotting for the iterated molar ratio
    ax = axes[idx]
    for i, temp in enumerate(T):
        ax.plot(P / 1e5, methane_yield[i], label=f"T={round(temp)}K")  # Pressure in bar
    #plot settings
    ax.set_yscale("log")
    ax.set_xlabel('Pressure (bar)', fontsize=10)
    ax.set_ylabel('Methane Yield (Mole Fraction)', fontsize=10)
    ax.set_title(f'CO2:H2 = {X_CO2}:{X_H2}', fontsize=12)
    ax.legend(fontsize=8, title="Temperature")
    ax.grid(True)
plt.show()
