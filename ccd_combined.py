# Script for producing color-color diagrams with photometric data for YSOs and background stars

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import os

# Import the relevant .csv files, turn them into dataframes
filepath_background = 'background_xmatch_test.csv'
filepath_yso = 'alcala_full_spec.csv'
df_background = pd.read_csv(filepath_background)
df_yso = pd.read_csv(filepath_yso)
#print(df_background)
#print(df_yso)

# For both catalogs, drop rows that have NaNs in any columns corresponding to fluxes
df_background_dropped = df_background.dropna(subset=['FIR1','FIR2','FIR3','FIR4','Hamag']) # Did not exclude MIPS NaNs
df_yso_dropped = df_yso.dropna(subset=['FIR1','FIR2','FIR3','FIR4','FHa']) # Did not exclude MIPS NaNs

# Get individual values for background stars
## Did not do any grouping here, so there might be duplicated sources (unlikely, though)
background_Ha_mag = df_background_dropped['Hamag'].values
background_FIR1_mJy = df_background_dropped['FIR1'].values
background_FIR2_mJy = df_background_dropped['FIR2'].values
background_FIR3_mJy = df_background_dropped['FIR3'].values
background_FIR4_mJy = df_background_dropped['FIR4'].values
# For Alcala catalog, remove duplicate rows in xMatch table
df_yso_grouped = df_yso_dropped.groupby('Object')
# Then, extract photometry information
yso_FIR1_mJy = df_yso_grouped['FIR1'].agg(np.mean)
yso_FIR2_mJy = df_yso_grouped['FIR2'].agg(np.mean)
yso_FIR3_mJy = df_yso_grouped['FIR3'].agg(np.mean)
yso_FIR4_mJy = df_yso_grouped['FIR4'].agg(np.mean)
yso_FHa_flux = df_yso_grouped['FHa'].agg(np.mean)

# Convert H-alpha fluxes to average flux densities in mJy
## Divide H-alpha flux by frequency of H-alpha in Hz, multiply by factor of 10**(-26)
yso_FHa_mJy = yso_FHa_flux*(10**(-26))/(4.565*(10**14)) # Used INT WFC H-alpha filter center wavelength

# Convert flux densities to magnitudes for background stars
## First, define Spitzer IRAC zero points
FIR1_ZP_Jy = 277.2
FIR2_ZP_Jy = 179.0
FIR3_ZP_Jy = 113.8
FIR4_ZP_Jy = 62.0
Ha_ZP_Jy = 2609.54 # INT WFC H-alpha filter
background_FIR1_mag = -2.5*np.log10(background_FIR1_mJy*(10**(-3))/FIR1_ZP_Jy)
background_FIR2_mag = -2.5*np.log10(background_FIR2_mJy*(10**(-3))/FIR2_ZP_Jy)
background_FIR3_mag = -2.5*np.log10(background_FIR3_mJy*(10**(-3))/FIR3_ZP_Jy)
background_FIR4_mag = -2.5*np.log10(background_FIR4_mJy*(10**(-3))/FIR4_ZP_Jy)
# Do the same for Alcala catalog
yso_FIR1_mag = -2.5*np.log10(yso_FIR1_mJy*(10**(-3))/FIR1_ZP_Jy)
yso_FIR2_mag = -2.5*np.log10(yso_FIR2_mJy*(10**(-3))/FIR2_ZP_Jy)
yso_FIR3_mag = -2.5*np.log10(yso_FIR3_mJy*(10**(-3))/FIR3_ZP_Jy)
yso_FIR4_mag = -2.5*np.log10(yso_FIR4_mJy*(10**(-3))/FIR4_ZP_Jy) 
yso_FHa_mag = -2.5*np.log10(yso_FHa_mJy*(10**(-3))/Ha_ZP_Jy)

# Plot color-color diagrams
plt.figure(dpi = 100)
plt.grid()
#plt.rc('font', family='serif')
plt.scatter(background_Ha_mag-background_FIR1_mag,background_FIR1_mag-background_FIR2_mag,label="background star",color='xkcd:black')
plt.scatter(yso_FHa_mag-yso_FIR1_mag,yso_FIR1_mag-yso_FIR2_mag,label="YSO",color='xkcd:azure')
plt.xlabel("H-alpha - [3.6]", size = 14)
#plt.xlabel(r"$H\alpha - [3.6]$", size = 14)
plt.ylabel("[3.6] - [4.5]", size = 14)
#plt.ylabel(r"$[3.6] - [4.5]$", size = 14)
#plt.xlim(0.7,4.2)
#plt.ylim(0,1)
plt.legend(loc="upper right")
plt.title("Color-color diagram for YSOs and background stars", size = 14)
#plt.savefig('test_ccd.png', transparent = False)
#, facecolor='none', edgecolor='none')
plt.show()
