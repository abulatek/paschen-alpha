# Script for producing color-color diagrams with photometric data for YSOs and background stars

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import sys
from astropy import units as u

# Import the relevant .csv files, turn them into dataframes
filepath_background = 'background_xmatch_test.csv'
filepath_yso = 'alcala_full_spec_sptype.csv'
df_background = pd.read_csv(filepath_background)
df_yso = pd.read_csv(filepath_yso)
#print(df_background)
#print(df_yso)
print("Number of rows in current background catalog:",len(df_background))
print("Number of rows in current YSO catalog:",len(df_yso))

# For both catalogs, drop rows that have NaNs in any columns corresponding to fluxes
print("Dropping rows that have NaNs in any important columns.")
df_background_dropped = df_background.dropna(subset=['FIR1','FIR2','FIR3','FIR4','Hamag','FJ','FH','FKs','rmag','imag']) # Did not exclude MIPS NaNs
df_yso_dropped = df_yso.dropna(subset=['FIR1','FIR2','FIR3','FIR4','FHa','FJ','FH','FKs','rmag','imag']) # Did not exclude MIPS NaNs
print("Number of rows in current background catalog:",len(df_background_dropped),"-- dropped",len(df_background)-len(df_background_dropped))
print("Number of rows in current YSO catalog:",len(df_yso_dropped),"-- dropped",len(df_yso)-len(df_yso_dropped))

# Get individual values for background stars
## Did not do any grouping here, so there might be duplicated sources (unlikely, though)
background_FIR1_Jy = u.Quantity(df_background_dropped['FIR1'].values, (10**(-3))*u.Jy)
background_FIR2_Jy = u.Quantity(df_background_dropped['FIR2'].values, (10**(-3))*u.Jy)
background_FIR3_Jy = u.Quantity(df_background_dropped['FIR3'].values, (10**(-3))*u.Jy)
background_FIR4_Jy = u.Quantity(df_background_dropped['FIR4'].values, (10**(-3))*u.Jy)
background_FJ_Jy = u.Quantity(df_background_dropped['FJ'].values, (10**(-3))*u.Jy)
background_FH_Jy = u.Quantity(df_background_dropped['FH'].values, (10**(-3))*u.Jy)
background_FKs_Jy = u.Quantity(df_background_dropped['FKs'].values, (10**(-3))*u.Jy)
background_Ha_mag = u.Quantity(df_background_dropped['Hamag'].values, u.mag)
# For Alcala catalog, remove duplicate rows in xMatch table
df_yso_grouped = df_yso_dropped.groupby('Object')
print("After grouping, number of rows in current YSO catalog:",len(df_yso_grouped))
# Then, extract photometry information
yso_FIR1_Jy = u.Quantity(df_yso_grouped['FIR1'].agg(np.mean), (10**(-3))*u.Jy)
yso_FIR2_Jy = u.Quantity(df_yso_grouped['FIR2'].agg(np.mean), (10**(-3))*u.Jy)
yso_FIR3_Jy = u.Quantity(df_yso_grouped['FIR3'].agg(np.mean), (10**(-3))*u.Jy)
yso_FIR4_Jy = u.Quantity(df_yso_grouped['FIR4'].agg(np.mean), (10**(-3))*u.Jy)
yso_FJ_Jy = u.Quantity(df_yso_grouped['FJ'].agg(np.mean), (10**(-3))*u.Jy)
yso_FH_Jy = u.Quantity(df_yso_grouped['FH'].agg(np.mean), (10**(-3))*u.Jy)
yso_FKs_Jy = u.Quantity(df_yso_grouped['FKs'].agg(np.mean), (10**(-3))*u.Jy)
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
## Then, define 2MASS zero points from http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=2MASS
FJ_ZP_Jy = 1594.0*u.Jy
FH_ZP_Jy = 1024.0*u.Jy
FKs_ZP_Jy = 666.8*u.Jy
Ha_ZP_Jy = 2659.4*u.Jy # INT WFC H-alpha filter from http://svo2.cab.inta-csic.es/theory/fps/index.php?id=INT/IPHAS.Ha&&mode=browse&gname=INT&gname2=IPHAS#filter

# Testing for non-zero values within logarithm, prompted by error
'''
print(background_FIR1_Jy/FIR1_ZP_Jy)
print(background_FIR2_Jy/FIR2_ZP_Jy)
print(background_FIR3_Jy/FIR3_ZP_Jy)
print(background_FIR4_Jy/FIR4_ZP_Jy)
print(yso_FIR1_Jy/FIR1_ZP_Jy)
print(yso_FIR2_Jy/FIR2_ZP_Jy)
print(yso_FIR3_Jy/FIR3_ZP_Jy)
print(yso_FIR4_Jy/FIR4_ZP_Jy)
print(yso_FHa_Jy/Ha_ZP_Jy)
for array in [background_FIR1_Jy/FIR1_ZP_Jy,background_FIR2_Jy/FIR2_ZP_Jy,background_FIR3_Jy/FIR3_ZP_Jy,background_FIR4_Jy/FIR4_ZP_Jy,yso_FIR1_Jy/FIR1_ZP_Jy,yso_FIR2_Jy/FIR2_ZP_Jy,yso_FIR3_Jy/FIR3_ZP_Jy,yso_FIR4_Jy/FIR4_ZP_Jy,yso_FHa_Jy/Ha_ZP_Jy]:
	print(np.count_nonzero(array))
'''

# Get magnitudes
background_FIR1_mag = -2.5*np.log10(background_FIR1_Jy/FIR1_ZP_Jy)*u.mag
background_FIR2_mag = -2.5*np.log10(background_FIR2_Jy/FIR2_ZP_Jy)*u.mag
background_FIR3_mag = -2.5*np.log10(background_FIR3_Jy/FIR3_ZP_Jy)*u.mag
background_FIR4_mag = -2.5*np.log10(background_FIR4_Jy/FIR4_ZP_Jy)*u.mag
background_FJ_mag = -2.5*np.log10(background_FJ_Jy/FJ_ZP_Jy)*u.mag
background_FH_mag = -2.5*np.log10(background_FH_Jy/FH_ZP_Jy)*u.mag
background_FKs_mag = -2.5*np.log10(background_FKs_Jy/FKs_ZP_Jy)*u.mag
# Do the same for Alcala catalog
yso_FIR1_mag = -2.5*np.log10(yso_FIR1_Jy/FIR1_ZP_Jy)*u.mag
yso_FIR2_mag = -2.5*np.log10(yso_FIR2_Jy/FIR2_ZP_Jy)*u.mag
yso_FIR3_mag = -2.5*np.log10(yso_FIR3_Jy/FIR3_ZP_Jy)*u.mag
yso_FIR4_mag = -2.5*np.log10(yso_FIR4_Jy/FIR4_ZP_Jy)*u.mag
yso_FJ_mag = -2.5*np.log10(yso_FJ_Jy/FJ_ZP_Jy)*u.mag
yso_FH_mag = -2.5*np.log10(yso_FH_Jy/FH_ZP_Jy)*u.mag
yso_FKs_mag = -2.5*np.log10(yso_FKs_Jy/FKs_ZP_Jy)*u.mag
yso_FHa_mag = -2.5*np.log10(yso_FHa_Jy/Ha_ZP_Jy)*u.mag

# Looking at small group of background stars near the YSOs in the plot
'''
df_background_dropped['FIR3_mag'] = background_FIR3_mag
df_background_dropped['FIR4_mag'] = background_FIR4_mag
df_background_dropped['Ha_mag'] = background_Ha_mag
pd.set_option('max_columns', None)
print(df_background_dropped.loc[(df_background_dropped['Ha_mag']-df_background_dropped['FIR4_mag']>=9) & (df_background_dropped['FIR3_mag']-df_background_dropped['FIR4_mag']>=1)])
pd.reset_option('max_columns')
'''

# Perform "continuum subtraction" (sketchily) on the background H-alpha data
background_r_mag = u.Quantity(df_background_dropped['rmag'].values, u.mag)
background_r_ZP_Jy = 3086.72*u.Jy
background_r_flux = background_r_ZP_Jy*10**(-background_r_mag/(2.5*u.mag))
background_Ha_flux = Ha_ZP_Jy*10**(-background_Ha_mag/(2.5*u.mag))
background_Ha_contsub_flux = background_Ha_flux - background_r_flux
background_Ha_contsub_mag = -2.5*np.log10(background_Ha_contsub_flux/Ha_ZP_Jy)*u.mag

# Get i magnitude for background sources, and r and i mags for YSOs
background_i_mag = u.Quantity(df_background_dropped['imag'].values, u.mag)
yso_r_mag = u.Quantity(df_yso_dropped['rmag'].values, u.mag)
yso_i_mag = u.Quantity(df_yso_dropped['imag'].values, u.mag)

sys.exit()

# Get spectral type for YSOs
#yso_SpType = df_yso_grouped['SpType'].first()
#categories = set(yso_SpType)

# Plot color-color diagrams
plt.figure(dpi = 150)
plt.grid()

#plt.scatter(background_Ha_contsub_mag-background_FIR4_mag,background_FIR3_mag-background_FIR4_mag,label="background star",color='xkcd:black',marker="*",alpha=0.5) 
#plt.scatter(yso_FHa_mag-yso_FIR4_mag,yso_FIR3_mag-yso_FIR4_mag,label="YSO",color='xkcd:azure',marker="o",alpha=0.5)

plt.scatter(background_r_mag-background_i_mag,background_r_mag-background_Ha_contsub_mag,label="background star",color='xkcd:black',marker="o",alpha=0.5) 
plt.scatter(yso_r_mag-yso_i_mag,yso_r_mag-yso_FHa_mag,label="YSO",color='xkcd:azure',marker="o",alpha=0.5)

plt.xlabel('r - i', size = 14)
plt.ylabel('r - H-alpha', size = 14)

plt.legend(loc="upper right")
plt.title("Color-color diagram for YSOs and background stars", size = 14)
#plt.savefig('test_ccd.png', transparent = False, facecolor='none', edgecolor='none')
plt.show()

