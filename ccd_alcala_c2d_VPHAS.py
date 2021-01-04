# Produce a color-color diagram with photometric data for YSOs (Alcala and c2d) and background sources (VPHAS and c2d)

import pandas as pd
import numpy as np
from astropy import units as u
import matplotlib.pyplot as plt
from matplotlib import rc

plt.rcParams['text.latex.preamble'] = [r'\usepackage{gensymb}']

def import_csv(filename, columns, sourceName, drop_NaN=True):
    '''Import contents of a .csv file into a pandas dataframe, dropping NaNs
    when specified and grouping by specified unique identifier.'''
    df = pd.read_csv(filename)
    if drop_NaN==True:
        df = df.dropna(subset=columns)
    df = df.groupby(sourceName).mean()
    return df

def convert_flux_to_mag(flux, filter):
    '''Convert H-alpha fluxes to average flux densities in mJy.'''
    if filter=='FHa':
        FHa_flux = u.Quantity(flux, (10**(-3))*u.W/u.meter**2) # Give flux units that match catalog units
        frequency_Ha = (6568.0 * u.AA).to(u.Hz, equivalencies=u.spectral()) # Used INT WFC H-alpha filter center wavelength from http://svo2.cab.inta-csic.es/theory/fps/index.php?id=INT/IPHAS.Ha&&mode=browse&gname=INT&gname2=IPHAS#filter
        FHa_Jy = (FHa_flux/frequency_Ha).to(u.Jy) # Divide H-alpha flux by frequency of H-alpha in Hz
        Ha_ZP_Jy = 2659.39*u.Jy # VST H-alpha filter from http://svo2.cab.inta-csic.es/theory/fps/index.php?id=Paranal/OmegaCAM.Halpha&&mode=search&search_instrument=OmegaCAM#filter
        mag = -2.5*np.log10(FHa_Jy/Ha_ZP_Jy)
    return mag

def convert_flux_density_to_mag(flux_density, filter):
    '''Convert flux densities to magnitudes using correct zero points. 
    From http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=Spitzer'''
    if filter=='FIR1':
        FIR_ZP_Jy = 277.2
    if filter=='FIR2':
        FIR_ZP_Jy = 179.0
    if filter=='FIR3':
        FIR_ZP_Jy = 113.8
    if filter=='FIR4':
        FIR_ZP_Jy = 62.0
    mag = -2.5*np.log10(flux_density*(10**(-3))/FIR_ZP_Jy)
    return mag

def plot_ccd(df_yso, df_back):
    '''Plot a color-color diagram, given a dataframe.'''
    # Define variables
    yso_3p6, yso_4p5, yso_5p8, yso_8p0, yso_Halpha = df_yso['FIR1_mag'], df_yso['FIR2_mag'], df_yso['FIR3_mag'], df_yso['FIR4_mag'], df_yso['Ha_mag']
    back_3p6, back_4p5, back_5p8, back_8p0, back_Halpha = df_back['FIR1_mag'], df_back['FIR2_mag'], df_back['FIR3_mag'], df_back['FIR4_mag'], df_back['Hamag']
    # Plot a color-color diagram
    plt.figure(dpi = 100)
    plt.grid()
    plt.scatter(back_Halpha-back_8p0,back_5p8-back_8p0,color='xkcd:orange',label="Background stars",alpha=0.5)
    plt.scatter(yso_Halpha-yso_8p0,yso_5p8-yso_8p0,color='xkcd:azure',label="Young stellar objects",alpha=0.5)
    plt.xlabel(r"H$\mathrm{\alpha}$ - [8.0]")
    plt.ylabel("[5.8] - [8.0]")
    plt.title("Color-color diagram for YSOs/background sources")
    plt.legend()
    plt.show()

df_yso = import_csv('alcala_full_spec.csv',columns=['FIR1','FIR2','FIR3','FIR4','FHa'],sourceName='Object')
df_background = import_csv('background_xmatch_test.csv',columns=['FIR1','FIR2','FIR3','FIR4','Hamag'],sourceName='sourceID')

df_yso['Ha_mag'] = convert_flux_to_mag(df_yso['FHa'], 'FHa')
df_yso['FIR1_mag'] = convert_flux_density_to_mag(df_yso['FIR1'], 'FIR1')
df_yso['FIR2_mag'] = convert_flux_density_to_mag(df_yso['FIR2'], 'FIR2')
df_yso['FIR3_mag'] = convert_flux_density_to_mag(df_yso['FIR3'], 'FIR3')
df_yso['FIR4_mag'] = convert_flux_density_to_mag(df_yso['FIR4'], 'FIR4')
df_background['FIR1_mag'] = convert_flux_density_to_mag(df_background['FIR1'], 'FIR1')
df_background['FIR2_mag'] = convert_flux_density_to_mag(df_background['FIR2'], 'FIR2')
df_background['FIR3_mag'] = convert_flux_density_to_mag(df_background['FIR3'], 'FIR3')
df_background['FIR4_mag'] = convert_flux_density_to_mag(df_background['FIR4'], 'FIR4')

plot_ccd(df_yso, df_background)