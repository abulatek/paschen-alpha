# Produce a color-color diagram with photometric data for YSOs (VPHAS and SPICY) and background sources (VPHAS and c2d)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
    mag = -2.5*np.log10(flux*(10**(-3))/FIR_ZP_Jy)
    return mag

def plot_ccd(df_yso, df_back):
    '''Plot a color-color diagram, given a dataframe.'''
    # Define variables
    yso_3p6, yso_4p5, yso_5p8, yso_8p0, yso_Halpha = df_yso['mag3_6'], df_yso['mag4_5'], df_yso['mag5_8'], df_yso['mag8_0'], df_yso['Hamag']
    back_3p6, back_4p5, back_5p8, back_8p0, back_Halpha = df_back['FIR1_mag'], df_back['FIR2_mag'], df_back['FIR3_mag'], df_back['FIR4_mag'], df_back['Hamag']
    # Plot a color-color diagram
    plt.figure(dpi = 100)
    plt.grid()
    plt.scatter(yso_Halpha-yso_8p0,yso_5p8-yso_8p0,color='xkcd:teal',label="Young stellar objects",alpha=0.5)
    plt.scatter(back_Halpha-back_8p0,back_5p8-back_8p0,color='xkcd:orange',label="Background stars",alpha=0.5)
    plt.xlabel(r"H$\mathrm{\alpha}$ - [8.0]")
    plt.ylabel("[5.8] - [8.0]")
    plt.title("Color-color diagram for YSOs/background sources (SPICY YSOs)")
    plt.legend()
    plt.show()

df_yso = import_csv('SPICY_VPHAS_xmatch.csv',columns=['mag3_6','mag4_5','mag5_8','mag8_0','Hamag'],sourceName='SPICY')
df_background = import_csv('c2d_VPHAS_xmatch.csv',columns=['FIR1','FIR2','FIR3','FIR4','Hamag'],sourceName='sourceID')

print(len(df_yso))
print(len(df_background))

df_background['FIR1_mag'] = convert_flux_to_mag(df_background['FIR1'], 'FIR1')
df_background['FIR2_mag'] = convert_flux_to_mag(df_background['FIR2'], 'FIR2')
df_background['FIR3_mag'] = convert_flux_to_mag(df_background['FIR3'], 'FIR3')
df_background['FIR4_mag'] = convert_flux_to_mag(df_background['FIR4'], 'FIR4')

plot_ccd(df_yso, df_background)
