# Script for producing color-color diagrams with photometric data for YSOs and background stars

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import os
from astropy import units as u

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
print(len(df_background_dropped))
df_background_grouped = df_background_dropped.groupby('sourceID')
print(len(df_background_grouped))
background_Ha_mag = u.Quantity(df_background_dropped['Hamag'].values, u.mag)
background_FIR1_Jy = u.Quantity(df_background_dropped['FIR1'].values, (10**(-3))*u.Jy)
background_FIR2_Jy = u.Quantity(df_background_dropped['FIR2'].values, (10**(-3))*u.Jy)
background_FIR3_Jy = u.Quantity(df_background_dropped['FIR3'].values, (10**(-3))*u.Jy)
background_FIR4_Jy = u.Quantity(df_background_dropped['FIR4'].values, (10**(-3))*u.Jy)
# For Alcala catalog, remove duplicate rows in xMatch table
df_yso_grouped = df_yso_dropped.groupby('Object')
# Then, extract photometry information
yso_FIR1_Jy = u.Quantity(df_yso_grouped['FIR1'].agg(np.mean), (10**(-3))*u.Jy)
yso_FIR2_Jy = u.Quantity(df_yso_grouped['FIR2'].agg(np.mean), (10**(-3))*u.Jy)
yso_FIR3_Jy = u.Quantity(df_yso_grouped['FIR3'].agg(np.mean), (10**(-3))*u.Jy)
yso_FIR4_Jy = u.Quantity(df_yso_grouped['FIR4'].agg(np.mean), (10**(-3))*u.Jy)
yso_FHa_flux = u.Quantity(df_yso_grouped['FHa'].agg(np.mean), (10**(-3))*u.W/u.meter**2)

# Convert H-alpha fluxes to average flux densities in mJy
## Divide H-alpha flux by frequency of H-alpha in Hz, multiply by factor of 10**(-26)
frequency_Ha = (6568.0 * u.AA).to(u.Hz, equivalencies=u.spectral()) # Used INT WFC H-alpha filter center wavelength from http://svo2.cab.inta-csic.es/theory/fps/index.php?id=INT/IPHAS.Ha&&mode=browse&gname=INT&gname2=IPHAS#filter
yso_FHa_Jy = (yso_FHa_flux/frequency_Ha).to(u.Jy) 

# Convert flux densities to magnitudes for background stars
## First, define Spitzer IRAC zero points from http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=Spitzer
FIR1_ZP_Jy = 277.2*u.Jy
FIR2_ZP_Jy = 179.0*u.Jy
FIR3_ZP_Jy = 113.8*u.Jy
FIR4_ZP_Jy = 62.0*u.Jy
Ha_ZP_Jy = 2659.39*u.Jy # VST H-alpha filter from http://svo2.cab.inta-csic.es/theory/fps/index.php?id=Paranal/OmegaCAM.Halpha&&mode=search&search_instrument=OmegaCAM#filter
background_FIR1_mag = -2.5*np.log10(background_FIR1_Jy/FIR1_ZP_Jy)*u.mag
background_FIR2_mag = -2.5*np.log10(background_FIR2_Jy/FIR2_ZP_Jy)*u.mag
background_FIR3_mag = -2.5*np.log10(background_FIR3_Jy/FIR3_ZP_Jy)*u.mag
background_FIR4_mag = -2.5*np.log10(background_FIR4_Jy/FIR4_ZP_Jy)*u.mag
# Do the same for Alcala catalog
yso_FIR1_mag = -2.5*np.log10(yso_FIR1_Jy/FIR1_ZP_Jy)*u.mag
yso_FIR2_mag = -2.5*np.log10(yso_FIR2_Jy/FIR2_ZP_Jy)*u.mag
yso_FIR3_mag = -2.5*np.log10(yso_FIR3_Jy/FIR3_ZP_Jy)*u.mag
yso_FIR4_mag = -2.5*np.log10(yso_FIR4_Jy/FIR4_ZP_Jy)*u.mag
yso_FHa_mag = -2.5*np.log10(yso_FHa_Jy/Ha_ZP_Jy)*u.mag

# Plot color-color diagrams
plt.figure(dpi = 100)
plt.grid()
plt.scatter(background_Ha_mag-background_FIR4_mag,background_FIR3_mag-background_FIR4_mag,label="background star",color='xkcd:black',alpha=0.5)
plt.scatter(yso_FHa_mag-yso_FIR4_mag,yso_FIR3_mag-yso_FIR4_mag,label="YSO",color='xkcd:azure',alpha=0.5)
plt.xlabel("H-alpha - [8.0]", size = 14)
plt.ylabel("[5.8] - [8.0]", size = 14)
plt.legend(loc="upper right")
plt.title("Color-color diagram for YSOs and background stars", size = 14)
plt.show()

