import cantera as ct
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


"""
Plot for stoichiometric and looking and pressures and temp combinations for methane yield. 
Equilibrium Calculations of the Sabatier Reaction
Objective: determine how equilibrium products vary depending on reactant molar ratio, temperature, and pressure. 
Reactants: CO2, H2
Products: CH4, H2O

Stoichiometric Coefficients:
1x CO2, 4x H2; 1x CH4, 2x H2O
"""

# Realistic Temp and Pressure domains
Tmin = 298  # K
Tmax = 338  # K
Pmin = 100000  # 100 kPa
Pmax = 5500000  # 5.5 MPa

T = np.linspace(Tmin, Tmax, 6) 
P = np.linspace(Pmin, Pmax, 50)  

# Stoichiometric ratio
X_CO2 = 0.2
X_H2 = 0.8

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

#methane yield for stoichiometric ratio across pressures and temps
methane_yield_stoich = np.zeros((len(T), len(P)))

for i, temp in enumerate(T):
    for j, pres in enumerate(P):
        methane_yield_stoich[i, j] = final_methane(mix, temp, pres, X_CO2, X_H2)

fig, ax = plt.subplots(figsize=(10, 6))
for i, temp in enumerate(T):
    ax.plot(P / 1e5, methane_yield_stoich[i], label=f"T={round(temp)}K")  # P in bar
formatter = ticker.FuncFormatter(lambda x, _: f"{x:.4e}") #set sig figs
ax.yaxis.set_major_formatter(formatter)
ax.grid(which='major', color='gray', linestyle='-', linewidth=0.8)
ax.grid(which='minor', color='gray', linestyle=':', linewidth=0.5)
ax.minorticks_on()
ax.set_xlabel('Pressure (bar)', fontsize=12)
ax.set_ylabel('Methane Yield (Mole Fraction)', fontsize=12)
ax.set_title(f'Methane Yield vs Pressure for Stoichiometric Ratio (CO2:H2 = 1:4)', fontsize=14)
ax.legend(fontsize=10, title="Temperature")
plt.tight_layout()
plt.show()
