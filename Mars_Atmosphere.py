import cantera as ct
import numpy as np
import matplotlib.pyplot as plt
"""
In this script, we will generate plots of the minor species vs temperature, vs pressure, 
and vs mole fraction. There will be 3 constant values that we will use for 2 of the properties
when we are varying the 3rd. These will be the optimal RXN characteristics. 
"""
#Optimal Temperature 
T_opt=673.15

#Optimal Pressure
P_opt=500000

#Varied Mole Fraction Range (used with constant T and P)
X_H2min=0.05
X_H2max=0.95
X_H2s=np.linspace(X_H2min,X_H2max,50)
X_CO2=np.zeros_like(X_H2s)
X_N2=np.zeros_like(X_H2s)
X_AR=np.zeros_like(X_H2s)
X_O2=np.zeros_like(X_H2s)
X_H2O=np.zeros_like(X_H2s)
X_mars=np.zeros_like(X_H2s)

mars_CO2=0.9532
mars_N2=0.027
mars_AR=0.016
mars_O2=0.013
mars_H2O=0.03

for i in range(len(X_H2s)):
    X_mars[i]=1-X_H2s[i]
    X_CO2[i]=mars_CO2*X_mars[i]
    X_N2[i]=mars_N2*X_mars[i]
    X_AR[i]=mars_AR*X_mars[i]
    X_O2[i]=mars_O2*X_mars[i]
    X_H2O[i]=mars_H2O*X_mars[i]


mix = ct.Solution('gri30.yaml')

#Vary Mole Fraction, Constant T and Constant P
combined_species_data_X = {}
mix.TP=T_opt,P_opt

for i in range(len(X_H2s)):
    x_mole_fractions={'CO2':X_CO2[i],'H2':X_H2s[i],'O2': X_O2[i], 'H2O': X_H2O[i], 'Ar': X_AR[i], 'N2': X_N2[i]}
    mix.X=x_mole_fractions
    mix.equilibrate('TP')
    x_species_names = mix.species_names 
    x_mole_fractions = mix.X
    x_filtered_species = {x_species_names[i]: x_mole_fractions[i] for i in range(len(x_species_names)) if x_mole_fractions[i] > 0.00001}
    for species, mole_fraction in x_filtered_species.items():
        if species not in combined_species_data_X:
            combined_species_data_X[species] = {'starting mole fraction': [], 'mole_fraction': []}
        combined_species_data_X[species]['starting mole fraction'].append(X_H2s[i])
        combined_species_data_X[species]['mole_fraction'].append(mole_fraction)

# Plot the results
plt.figure(1)
for species, data in combined_species_data_X.items():
    plt.plot(data['starting mole fraction'], data['mole_fraction'], label=species)
plt.xlabel('Reactant Mole Fraction of H2')
plt.ylabel('Product Mole Fractions')
plt.yscale('log')
plt.title('At constant temperature (673K) and constant pressure (5 bar)',fontsize=8)
plt.suptitle('Mole Fractions of Major Species (>1%) at Various Starting Mole Fractions of H2',fontsize=10)
plt.legend(loc='upper left')
plt.grid(True)

plt.figure(2)
for species, data in combined_species_data_X.items():
    plt.plot(data['starting mole fraction'], data['mole_fraction'], label=species)
plt.xlabel('Reactant Mole Fraction of H2')
plt.ylabel('Product Mole Fractions')
plt.title('At constant temperature (673K) and constant pressure (5 bar)',fontsize=8)
plt.suptitle('Mole Fractions of Major Species (>1%) at Various Starting Mole Fractions of H2',fontsize=10)
plt.legend(loc='upper left')
plt.grid(True)

plt.show()