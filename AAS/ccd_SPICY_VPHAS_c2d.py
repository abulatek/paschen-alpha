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

def get_data(df, df_type):
    '''Get data from a given dataframe.'''
    if df_type=='yso':
        df_3p6, df_4p5, df_5p8, df_8p0, df_Halpha = df['mag3_6'], df['mag4_5'], df['mag5_8'], df['mag8_0'], df['Hamag']
    if df_type=='background':
        df_3p6, df_4p5, df_5p8, df_8p0, df_Halpha = df['FIR1_mag'], df['FIR2_mag'], df['FIR3_mag'], df['FIR4_mag'], df['Hamag']
    return df_3p6, df_4p5, df_5p8, df_8p0, df_Halpha

def plot_ccd(yso_IR_sw, yso_IR_lw, yso_Halpha, bg_IR_sw, bg_IR_lw, bg_Halpha, sw_str, lw_str):
    '''Plot a color-color diagram, given a dataframe.'''
    plt.figure(dpi = 100)
    plt.grid()
    plt.scatter(yso_Halpha-yso_IR_lw,yso_IR_sw-yso_IR_lw,marker='.',color='xkcd:teal',label="Young stellar objects",alpha=1.0)
    plt.scatter(bg_Halpha-bg_IR_lw,bg_IR_sw-bg_IR_lw,marker='.',color='xkcd:orange',label="Background stars",alpha=1.0)
    plt.xlabel(r"H$\mathrm{\alpha}$ - "+lw_str)
    plt.ylabel(sw_str+" - "+lw_str)
    plt.title("Color-color diagram for YSOs/background sources (SPICY YSOs)")
    plt.legend()
    plt.show()

def plot_binned_ccd(df_yso, df_back):
    return None

df_yso = import_csv('SPICY_VPHAS_xmatch.csv',columns=['mag3_6','mag4_5','mag5_8','mag8_0','Hamag'],sourceName='SPICY')
df_background = import_csv('c2d_VPHAS_xmatch.csv',columns=['FIR1','FIR2','FIR3','FIR4','Hamag'],sourceName='sourceID')

df_background['FIR1_mag'] = convert_flux_to_mag(df_background['FIR1'], 'FIR1')
df_background['FIR2_mag'] = convert_flux_to_mag(df_background['FIR2'], 'FIR2')
df_background['FIR3_mag'] = convert_flux_to_mag(df_background['FIR3'], 'FIR3')
df_background['FIR4_mag'] = convert_flux_to_mag(df_background['FIR4'], 'FIR4')

yso_3p6, yso_4p5, yso_5p8, yso_8p0, yso_Halpha = get_data(df_yso, 'yso')
bg_3p6, bg_4p5, bg_5p8, bg_8p0, bg_Halpha = get_data(df_background, 'background')

plot_ccd(yso_3p6, yso_4p5, yso_Halpha, bg_3p6, bg_4p5, bg_Halpha, '[3.6]', '[4.5]')
