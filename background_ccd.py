# Script for producing color-color diagrams with photometric data (background star edition)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import os

# Import the relevant .csv file, turn it into a dataframe
filepath = 'background_xmatch_test.csv'
df = pd.read_csv(filepath)
#print(df)

# Drop rows that have NaNs in any columns corresponding to fluxes
df_dropped = df.dropna(subset=['FIR1','FIR2','FIR3','FIR4','Hamag']) # Did not exclude MIPS NaNs

# Get individual values 
## Did not do any grouping here, so there might be duplicated sources (unlikely, though)
Ha_mag = df['Hamag'].values
FIR1_mJy = df['FIR1'].values
FIR2_mJy = df['FIR2'].values
FIR3_mJy = df['FIR3'].values
FIR4_mJy = df['FIR4'].values

# Convert flux densities to magnitudes
FIR1_ZP_Jy = 277.2
FIR1_mag = -2.5*np.log10(FIR1_mJy*(10**(-3))/FIR1_ZP_Jy)

FIR2_ZP_Jy = 179.0
FIR2_mag = -2.5*np.log10(FIR2_mJy*(10**(-3))/FIR2_ZP_Jy)

FIR3_ZP_Jy = 113.8
FIR3_mag = -2.5*np.log10(FIR3_mJy*(10**(-3))/FIR3_ZP_Jy)

FIR4_ZP_Jy = 62.0
FIR4_mag = -2.5*np.log10(FIR4_mJy*(10**(-3))/FIR4_ZP_Jy)

# Plot color-color diagrams
plt.figure(dpi = 100)
plt.grid()
#plt.rc('font', family='serif')
plt.scatter(Ha_mag-FIR1_mag,FIR1_mag-FIR2_mag,color='xkcd:black')
plt.xlabel("H-alpha - [3.6]", size = 14)
#plt.xlabel(r"$H\alpha - [3.6]$", size = 14)
plt.ylabel("[3.6] - [4.5]", size = 14)
#plt.ylabel(r"$[3.6] - [4.5]$", size = 14)
#plt.xlim(0.7,4.2)
#plt.ylim(0,1)
plt.title("Color-color diagram for background stars in c2d/VPHAS catalogs", size = 14)
plt.savefig('back_test_ccd.png', transparent = False)
#, facecolor='none', edgecolor='none')
plt.show()
