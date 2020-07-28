# Script for producing color-color diagrams with photometric data

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import os

# Run some things to get LaTeX font in plots
#plt.rc('text', usetex = True) # Use LaTeX font in plots
#plt.rcParams['text.latex.preamble'] = [r'\usepackage{gensymb}']
#                                       r'\usepackage{sansmath}',
#                                       r'\sansmath']

# Import the relevant .csv file, turn it into a dataframe
filepath = 'alcala_full_spec.csv'
df = pd.read_csv(filepath)
#print(df)

# Drop rows that have NaNs in any columns corresponding to fluxes
df_dropped = df.dropna(subset=['FIR1','FIR2','FIR3','FIR4','FHa']) # Did not exclude MIPS NaNs   

# Remove duplicate rows in xMatch table and extract photometry information
#print(df.groupby('Object').groups)

df_grouped = df_dropped.groupby('Object')

FIR1_mJy = df_grouped['FIR1'].agg(np.mean)
FIR2_mJy = df_grouped['FIR2'].agg(np.mean)
FIR3_mJy = df_grouped['FIR3'].agg(np.mean)
FIR4_mJy = df_grouped['FIR4'].agg(np.mean)
FHa_flux = df_grouped['FHa'].agg(np.mean)
#FHa_EW_nm = df_grouped['EWHa'].agg(np.mean)

# Convert H-alpha fluxes to average flux densities in mJy
## Divide H-alpha flux by frequency of H-alpha in Hz, multiply by factor of 10**(-26)
FHa_mJy = FHa_flux*(10**(-26))/(4.565*(10**14)) # Used INT WFC H-alpha filter center wavelength

# Convert flux densities to magnitudes
FIR1_ZP_Jy = 277.2
FIR1_mag = -2.5*np.log10(FIR1_mJy*(10**(-3))/FIR1_ZP_Jy)

FIR2_ZP_Jy = 179.0
FIR2_mag = -2.5*np.log10(FIR2_mJy*(10**(-3))/FIR2_ZP_Jy)

FIR3_ZP_Jy = 113.8
FIR3_mag = -2.5*np.log10(FIR3_mJy*(10**(-3))/FIR3_ZP_Jy)

FIR4_ZP_Jy = 62.0
FIR4_mag = -2.5*np.log10(FIR4_mJy*(10**(-3))/FIR4_ZP_Jy)

Ha_ZP_Jy = 2609.54 # INT WFC H-alpha filter 
FHa_mag = -2.5*np.log10(FHa_mJy*(10**(-3))/Ha_ZP_Jy)

# Plot color-color diagrams
plt.figure(dpi = 100)
plt.grid()
#plt.rc('font', family='serif')
plt.scatter(FHa_mag-FIR1_mag,FIR1_mag-FIR2_mag,color='xkcd:black')
plt.xlabel("H-alpha - [3.6]", size = 14)
#plt.xlabel(r"$H\alpha - [3.6]$", size = 14)
plt.ylabel("[3.6] - [4.5]", size = 14)
#plt.ylabel(r"$[3.6] - [4.5]$", size = 14)
#plt.xlim(0.7,4.2)
#plt.ylim(0,1)
plt.title("Color-color diagram for YSOs in Lupus from Alcala+2017", size = 14)
plt.savefig('test_ccd.png', transparent = False)
#, facecolor='none', edgecolor='none')
plt.show()
