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
#Optimal Mole Fractions
opt_X_CO2=0.2
opt_X_H2=1-opt_X_CO2

# Define a color dictionary for consistent color mapping
color_dict = {
    'H2': 'purple',
    'CO2': 'green',
    'CH4': 'red',
    'H2O': 'blue'
    # Add more species and their corresponding colors
}

#Varied Temperature Range (used with constant P and Xs)
Tmin = 298  # K
Tmax = 700  # K
Ts= np.linspace(Tmin, Tmax, 6)  

#Varied Pressure Range (used with constant T and Xs)
Pmin = 100000  # 1 bar
Pmax = 2000000 # 20 bar
Ps = np.linspace(Pmin, Pmax, 10)  

#Varied Mole Fraction Range (used with constant T and P)
X_CO2min=0.05
X_CO2max=0.35
X_CO2s=np.linspace(X_CO2min,X_CO2max,7)
print(X_CO2s)
X_H2s=np.ones_like(X_CO2s)
X_H2s-=X_CO2s

mix = ct.Solution('gri30.yaml')

#Vary Temperature, Constant P and Constant Xs
combined_species_data_T = {}
mole_fractions={'CO2':opt_X_CO2,'H2':opt_X_H2}
mix.X=mole_fractions
for i in range(len(Ts)):
    mix.TP=Ts[i],P_opt
    mix.equilibrate('TP')
    species_names = mix.species_names 
    mole_fractions = mix.X
    filtered_species = {species_names[i]: mole_fractions[i] for i in range(len(species_names)) if mole_fractions[i] > 0.01}
    for species, mole_fraction in filtered_species.items():
        if species not in combined_species_data_T:
            combined_species_data_T[species] = {'temperature': [], 'mole_fraction': []}
        combined_species_data_T[species]['temperature'].append(Ts[i])
        combined_species_data_T[species]['mole_fraction'].append(mole_fraction)

#Vary Pressure, Constant T and Constant Xs
combined_species_data_P = {}
p_mole_fractions={'CO2':opt_X_CO2,'H2':opt_X_H2}
mix.X=p_mole_fractions
for i in range(len(Ps)):
    mix.TP=T_opt,Ps[i]
    mix.equilibrate('TP')
    p_species_names = mix.species_names 
    p_mole_fractions = mix.X
    p_filtered_species = {p_species_names[i]: p_mole_fractions[i] for i in range(len(p_species_names)) if p_mole_fractions[i] > 0.01}
    for species, mole_fraction in p_filtered_species.items():
        if species not in combined_species_data_P:
            combined_species_data_P[species] = {'pressure': [], 'mole_fraction': []}
        combined_species_data_P[species]['pressure'].append(Ps[i])
        combined_species_data_P[species]['mole_fraction'].append(mole_fraction)

#Vary Mole Fraction, Constant T and Constant P
combined_species_data_X = {}
mix.TP=T_opt,P_opt

for i in range(len(X_CO2s)):
    x_mole_fractions={'CO2':X_CO2s[i],'H2':X_H2s[i]}
    mix.X=x_mole_fractions
    mix.equilibrate('TP')
    x_species_names = mix.species_names 
    x_mole_fractions = mix.X
    x_filtered_species = {x_species_names[i]: x_mole_fractions[i] for i in range(len(x_species_names)) if x_mole_fractions[i] > 0.01}
    for species, mole_fraction in x_filtered_species.items():
        if species not in combined_species_data_X:
            combined_species_data_X[species] = {'starting mole fraction': [], 'mole_fraction': []}
        combined_species_data_X[species]['starting mole fraction'].append(X_CO2s[i])
        combined_species_data_X[species]['mole_fraction'].append(mole_fraction)

# Plot the results
plt.figure(1)
for species, data in combined_species_data_T.items():
    plt.plot(data['temperature'], data['mole_fraction'], label=species,color=color_dict.get(species, 'black'))
plt.xlabel('Temperature (K)')
plt.ylabel('Mole Fraction')
plt.title('At constant pressure (5 bar), and starting molar ratio of 1:4',fontsize=10)
plt.suptitle('Mole Fractions of Major Species (>1%) vs. Various Temperatures',fontsize=12)
plt.legend(loc='lower left')
plt.grid(True)

plt.figure(2)
for species, data in combined_species_data_P.items():
    plt.plot(data['pressure'], data['mole_fraction'], label=species,color=color_dict.get(species, 'black'))
plt.xlabel('Pressure (Pa)')
plt.ylabel('Mole Fraction')
plt.title('At constant temperature (673k) and starting molar ratio of 1:4',fontsize=10)
plt.suptitle('Mole Fractions of Major Species (>1%) vs. Various Pressures',fontsize=12)
plt.legend(loc='upper right')
plt.grid(True)

plt.figure(3)
for species, data in combined_species_data_X.items():
    plt.plot(data['starting mole fraction'], data['mole_fraction'], label=species,color=color_dict.get(species, 'black'))
plt.xlabel('Reactant Mole Fraction of CO2')
plt.ylabel('Product Mole Fractions')
plt.title('At constant temperature (673k), and constant pressure (5 bar)',fontsize=8)
plt.suptitle('Mole Fractions of Major Species (>1%) vs. Various Starting Mole Fractions of CO2',fontsize=10)
plt.legend(loc='upper right')
plt.grid(True)


plt.show()





