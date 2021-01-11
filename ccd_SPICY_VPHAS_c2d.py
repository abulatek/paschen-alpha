# Produce a color-color diagram with photometric data for YSOs (VPHAS and SPICY) and background sources (VPHAS and c2d)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from astropy import units as u
import pylab as pl
import matplotlib as mpl
from adaptive_param_plot import *

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
        print(FHa_Jy)
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

def get_data(df, df_type):
    '''Get data from a given dataframe.'''
    if df_type=='ysoA':
        df_3p6, df_4p5, df_5p8, df_8p0, df_Halpha, df_rmag, df_r2mag = df['FIR1_mag'].values, df['FIR2_mag'].values, df['FIR3_mag'].values, df['FIR4_mag'].values, df['Hamag'].values, df['rmag'].values, df['r2mag'].values
    if df_type=='yso':
        df_3p6, df_4p5, df_5p8, df_8p0, df_Halpha, df_rmag, df_r2mag = df['mag3_6'].values, df['mag4_5'].values, df['mag5_8'].values, df['mag8_0'].values, df['Hamag'].values, df['rmag'].values, df['r2mag'].values
    if df_type=='background':
        df_3p6, df_4p5, df_5p8, df_8p0, df_Halpha, df_rmag, df_r2mag = df['FIR1_mag'].values, df['FIR2_mag'].values, df['FIR3_mag'].values, df['FIR4_mag'].values, df['Hamag'].values, df['rmag'].values, df['r2mag'].values
    return df_3p6, df_4p5, df_5p8, df_8p0, df_Halpha, df_rmag, df_r2mag

def plot_ccd(yso_IR_sw, yso_IR_lw, yso_Halpha, bg_IR_sw, bg_IR_lw, bg_Halpha, sw_str, lw_str):
    '''Plot a color-color diagram, given a dataframe.'''
    plt.figure(dpi = 100)
    plt.grid()
    plt.plot(yso_Halpha-yso_IR_lw,yso_IR_sw-yso_IR_lw,marker='.',linestyle='',color='xkcd:teal',label="Young stellar objects",alpha=1.0)
    plt.plot(bg_Halpha-bg_IR_lw,bg_IR_sw-bg_IR_lw,marker='.',linestyle='',color='xkcd:orange',label="Background sources",alpha=1.0)
    plt.xlabel(r"H$\mathrm{\alpha}$ - "+lw_str)
    plt.ylabel(sw_str+" - "+lw_str)
    plt.title("Color-color diagram for YSOs/background sources (SPICY YSOs)")
    plt.legend()
    plt.show()

def plot_contoured_ccd(yso_x, yso_y, bg_x, bg_y, x_lab, y_lab, bins):
    '''Plot a color-color diagram with contours in dense areas.'''
    plt.figure(dpi = 100)
    plt.grid()
    adaptive_param_plot(yso_x,yso_y,marker_color='xkcd:teal',bins=bins,fill=False,alpha=1,threshold=10,cmap=None,colors='xkcd:teal',label="Young stellar objects")
    adaptive_param_plot(bg_x,bg_y,marker_color='xkcd:orange',bins=bins,fill=False,alpha=1,threshold=10,cmap=None,colors='xkcd:orange',label='Background sources')
    plt.xlabel(x_lab)
    plt.ylabel(y_lab)
    plt.title("Color-color diagram for YSOs/background sources (SPICY YSOs)")
    plt.legend()
    plt.show()

# df_ysoA = import_csv('alcala_full_spec.csv',columns=['FIR1','FIR2','FIR3','FIR4','FHa'],sourceName='Object')
df_yso = import_csv('SPICY_VPHAS_xmatch.csv',columns=['mag3_6','mag4_5','mag5_8','mag8_0','Hamag'],sourceName='SPICY')
df_background = import_csv('c2d_VPHAS_xmatch.csv',columns=['FIR1','FIR2','FIR3','FIR4','Hamag'],sourceName='sourceID')

# df_ysoA['Hamag'] = convert_flux_to_mag(df_ysoA['FHa'], 'FHa')
# df_ysoA['FIR1_mag'] = convert_flux_density_to_mag(df_ysoA['FIR1'], 'FIR1')
# df_ysoA['FIR2_mag'] = convert_flux_density_to_mag(df_ysoA['FIR2'], 'FIR2')
# df_ysoA['FIR3_mag'] = convert_flux_density_to_mag(df_ysoA['FIR3'], 'FIR3')
# df_ysoA['FIR4_mag'] = convert_flux_density_to_mag(df_ysoA['FIR4'], 'FIR4')
df_background['FIR1_mag'] = convert_flux_density_to_mag(df_background['FIR1'], 'FIR1')
df_background['FIR2_mag'] = convert_flux_density_to_mag(df_background['FIR2'], 'FIR2')
df_background['FIR3_mag'] = convert_flux_density_to_mag(df_background['FIR3'], 'FIR3')
df_background['FIR4_mag'] = convert_flux_density_to_mag(df_background['FIR4'], 'FIR4')

# ysoA_3p6, ysoA_4p5, ysoA_5p8, ysoA_8p0, ysoA_Halpha, ysoA_rmag, ysoA_r2mag = get_data(df_ysoA, 'ysoA')
yso_3p6, yso_4p5, yso_5p8, yso_8p0, yso_Halpha, yso_rmag, yso_r2mag = get_data(df_yso, 'yso')
bg_3p6, bg_4p5, bg_5p8, bg_8p0, bg_Halpha, bg_rmag, bg_r2mag = get_data(df_background, 'background')

# plot_ccd(yso_3p6, yso_4p5, yso_Halpha, bg_3p6, bg_4p5, bg_Halpha, '[3.6]', '[4.5]')

plot_contoured_ccd(yso_5p8-yso_8p0, yso_3p6-yso_4p5, bg_5p8-bg_8p0, bg_3p6-bg_4p5, '[5.8] - [8.0]', '[3.6] - [4.5]', 20)

#### Trying to plot all three together (don't have r-band for Alcala though)
# bins=20
# plt.figure(dpi = 100)
# plt.grid()

# # adaptive_param_plot(ysoA_Halpha-ysoA_rmag,ysoA_5p8-ysoA_8p0,marker_color='xkcd:azure',bins=bins,fill=False,alpha=1,threshold=10,cmap=None,colors='xkcd:azure',label="Young stellar objects (Alcala)")
# adaptive_param_plot(yso_3p6-yso_4p5,yso_5p8-yso_8p0,marker_color='xkcd:teal',bins=bins,fill=False,alpha=1,threshold=10,cmap=None,colors='xkcd:teal',label="Young stellar objects (SPICY)")
# adaptive_param_plot(bg_3p6-bg_4p5,bg_5p8-bg_8p0,marker_color='xkcd:orange',bins=bins,fill=False,alpha=1,threshold=10,cmap=None,colors='xkcd:orange',label='Background sources')
# # plt.xlabel(r"H$\mathrm{\alpha}$ - R")
# plt.xlabel(r"[3.6] - [4.5]")
# plt.ylabel(r"[5.8] - [8.0]")
# plt.title("Color-color diagram for YSOs/background sources (SPICY YSOs)")
# plt.legend()
# plt.show()