# Produce a color-color diagram that shows the lack of separation between the YSOs with an excess and other YSO candidates/background sources. 
# Also, produce a color-color diagram that shows that H-alpha helps show this separation.
# Message: Spitzer alone is not able to identify accreting YSOs. Hydrogen recombination line photometry can help.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from astropy import units as u
from astropy import constants as const
import pylab as pl
import matplotlib as mpl
from adaptive_param_plot import *

plt.rcParams['text.latex.preamble'] = [r'\usepackage{gensymb}']

def import_csv(filename, columns, sourceName, drop_NaN=True):
    '''Import contents of a .csv file into a pandas dataframe, dropping NaNs when specified and grouping by specified unique identifier.'''
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

def filter_mag(df, e_mags, e_mag_lim):
    '''Perform signal-to-noise ratio cuts given a threshold and a list of magnitude errors.'''
    for e_mag in e_mags:
        df = df[df[e_mag] < e_mag_lim]
    return df

def convert_mag_to_mdot(Ha_minus_r_mag):
    '''Convert from H-alpha minus r color (H-alpha excess) to mass accretion rate.'''
    # Bandwidths below are FWHM values
    # VST r-band filter from http://svo2.cab.inta-csic.es/theory/fps/index.php?id=Paranal/OmegaCAM.r_SDSS&&mode=search&search_instrument=OmegaCAM#filter
    # VST H-alpha filter from http://svo2.cab.inta-csic.es/theory/fps/index.php?id=Paranal/OmegaCAM.Halpha&&mode=search&search_instrument=OmegaCAM#filter
    r_bandwidth_Hz, r_zero_point_Jy = (1362.89*u.AA).to(u.Hz,equivalencies=u.spectral()), 3094.61*u.Jy
    Ha_bandwidth_Hz, Ha_zero_point_Jy =	(102.69*u.AA).to(u.Hz,equivalencies=u.spectral()), 2659.39*u.Jy 
    M_r = 4.53 # Absolute magnitude of the Sun in the SDSS_r band, from https://iopscience.iop.org/article/10.3847/1538-4365/aabfdf
    L_r = 10**(-(M_r-4.77)/2.5)*u.Lsun # Get L_r estimate from absolute magnitude of Sun in the SDSS r band
    L_Ha = (Ha_zero_point_Jy/r_zero_point_Jy)*L_r*(r_bandwidth_Hz/Ha_bandwidth_Hz)*10**(-(Ha_minus_r_mag)/2.5)
    L_acc = (10**(1.13*np.log10(L_Ha.value)))*u.Lsun # Slope from Alcala+2017 table B.1, assuming log means log base 10 (they use ln elsewhere in their paper)
    R_star, M_star = (1.*u.Rsun).to(u.meter), (1.*u.Msun).to(u.kg) # Define average values for R_star and M_star, naively use solar values
    Mdot = ((1.25*L_acc.to(u.W)*R_star)/(const.G*M_star)).to(u.Msun/u.yr) # Calculate mass accretion rate from L_acc and defined values above
    return Mdot

def get_data(df, df_type):
    '''Get data from a given dataframe.'''
    if df_type=='SPICY':
        df_3p6, df_4p5, df_5p8, df_8p0, df_Halpha, df_rmag = df['mag3_6'].values, df['mag4_5'].values, df['mag5_8'].values, df['mag8_0'].values, df['Hamag'].values, df['rmag'].values
        return df_3p6, df_4p5, df_5p8, df_8p0, df_Halpha, df_rmag
    if df_type=='C2D':
        df_3p6, df_4p5, df_5p8, df_8p0, df_Halpha, df_rmag = df['FIR1_mag'].values, df['FIR2_mag'].values, df['FIR3_mag'].values, df['FIR4_mag'].values, df['Hamag'].values, df['rmag'].values
        return df_3p6, df_4p5, df_5p8, df_8p0, df_Halpha, df_rmag
    if df_type=='Alcala':
        df_3p6, df_4p5, df_5p8, df_8p0, df_Halpha = df['FIR1_mag'].values, df['FIR2_mag'].values, df['FIR3_mag'].values, df['FIR4_mag'].values, df['Hamag'].values
        return df_3p6, df_4p5, df_5p8, df_8p0, df_Halpha

def plot_contoured_ccd(yso_x, yso_y, exc_x, exc_y, x_lab, y_lab, bins, bgr_x=False, bgr_y=False, alcala_x=False, alcala_y=False):
    '''Plot a color-color diagram with contours in dense areas.'''
    plt.figure(dpi = 100)
    plt.grid(zorder=11)
    adaptive_param_plot(yso_x,yso_y,marker_color='#DE5F85',bins=bins,fill=False,alpha=1,threshold=3,cmap=None,colors='#DE5F85',label="SPICY young stellar objects",zorder=1)
    adaptive_param_plot(exc_x,exc_y,marker_color='orangered',bins=bins,fill=False,alpha=1,threshold=2,cmap=None,colors='orangered',label=r"SPICY YSOs with H$\mathrm{\alpha}$ excess",zorder=2)
    if bgr_x is not False:
        adaptive_param_plot(bgr_x,bgr_y,marker_color='#7AB648',bins=bins,fill=False,alpha=1,threshold=10,cmap=None,colors='#7AB648',label=r"Background sources",zorder=-1)
    if alcala_x is not False:
        adaptive_param_plot(alcala_x,alcala_y,marker='+',marker_color='#834187',bins=bins,fill=False,alpha=1,threshold=5,cmap=None,colors='#834187',label="Alcalá young stellar objects",zorder=10)
    plt.xlabel(x_lab)
    plt.ylabel(y_lab)
    plt.title(r"Young stellar objects and background sources ($Spitzer$ only)")
    plt.legend()
    plt.tight_layout()
    plt.savefig("ccd_spitzer_all_objects.png", dpi=250, facecolor='w', edgecolor='w')
    # plt.show()

def plot_contoured_ccd_w_mdot(yso_x, yso_y, exc_x, exc_y, x_lab, y_lab, bins, bgr_x=False, bgr_y=False, alcala_x=False, alcala_y=False):
    def convert_ax2_to_mdot(ax):
        '''Update second axis according with first axis.'''
        x1, x2 = ax.get_xlim()
        ax2.set_xlim(convert_mag_to_mdot(x1).value, convert_mag_to_mdot(x2).value)
        ax2.figure.canvas.draw()
    fig, ax1 = plt.subplots()
    ax1.set_xlabel(x_lab)
    ax1.set_ylabel(y_lab)
    ax1.set_xlim(-3.25, 0.75)
    adaptive_param_plot(yso_x,yso_y,marker_color='#DE5F85',bins=bins,fill=False,alpha=1,threshold=6,cmap=None,colors='#DE5F85',label="SPICY young stellar objects",axis=ax1)
    adaptive_param_plot(exc_x,exc_y,marker_color='orangered',bins=bins,fill=False,alpha=1,threshold=6,cmap=None,colors='orangered',label=r"SPICY YSOs with H$\mathrm{\alpha}$ excess",axis=ax1)
    if bgr_x is not False:
        adaptive_param_plot(bgr_x,bgr_y,marker_color='#7AB648',bins=bins,fill=False,alpha=1,threshold=10,cmap=None,colors='#7AB648',label=r"Background sources",axis=ax1)
    ax2 = ax1.twiny()
    ax2.set_xlabel(r"Mass accretion rate ($\log_{10}(\mathrm{M_{\odot}/yr}$))") # Would like to make the ticks match up...
    ax2.scatter(np.log10(convert_mag_to_mdot(yso_x).value),yso_y,marker='') # We want these points to be invisible
    ax2.set_xlim(np.log10(convert_mag_to_mdot(-3.25).value),np.log10(convert_mag_to_mdot(0.75).value))
    plt.title(r"Young stellar objects and background sources ($Spitzer$ and H$\mathrm{\alpha}$)")
    ax1.legend()
    ax1.grid()
    plt.tight_layout()
    plt.savefig("ccd_spitzer_all_objects_mdot.png", dpi=250, facecolor='w', edgecolor='w')
    # plt.show()

# Importing
df_yso = import_csv('xmatch_SPICY_VPHAS.csv',columns=['mag3_6','mag4_5','mag5_8','mag8_0','Hamag','rmag', 
                                                      'e_mag3_6', 'e_mag4_5','e_mag5_8','e_mag8_0','e_Hamag','e_rmag'],sourceName='SPICY')
df_bgr = import_csv('xmatch_c2d_VPHAS.csv',columns=['FIR1','FIR2','FIR3','FIR4','Hamag','rmag','e_Hamag','e_rmag'],sourceName='sourceID') # will not be able to filter IRAC, no errors provided
df_alc = import_csv('xmatch_alcala_c2d.csv',columns=['FIR1','FIR2','FIR3','FIR4','FHa','e_FHa'],sourceName='Object') # will not be able to filter IRAC fluxes or H-alpha flux, no errors provided

# Convert Alcala, background Spitzer flux densities to magnitudes
for df in [df_bgr, df_alc]:
    df['FIR1_mag'] = convert_flux_density_to_mag(df['FIR1'], 'FIR1')
    df['FIR2_mag'] = convert_flux_density_to_mag(df['FIR2'], 'FIR2')
    df['FIR3_mag'] = convert_flux_density_to_mag(df['FIR3'], 'FIR3')
    df['FIR4_mag'] = convert_flux_density_to_mag(df['FIR4'], 'FIR4')

# Convert Alcala H-alpha flux and error to magnitudes
df_alc['Hamag'] = convert_flux_to_mag(df_alc['FHa'], 'FHa')
# df_alc['e_Hamag'] = convert_flux_to_mag(df_alc['e_FHa'], 'FHa')

# Filtering
df_yso_filtered = filter_mag(df_yso,['e_mag3_6', 'e_mag4_5','e_mag5_8','e_mag8_0','e_Hamag','e_rmag'],0.1)
df_bgr_filtered = filter_mag(df_bgr,['e_Hamag','e_rmag'],0.1)
# Don't filter Alcala YSOs, since there are so few to begin with and I don't know how to convert flux error to mag error

# Creating another dataset, for a total of four 
df_yso_w_excess = df_yso_filtered[df_yso_filtered['Hamag'] - df_yso_filtered['rmag'] < -1.0]

# Retrieve data from each dataset
yso_3p6, yso_4p5, yso_5p8, yso_8p0, yso_Hamag, yso_rmag = get_data(df_yso_filtered, 'SPICY')
exc_3p6, exc_4p5, exc_5p8, exc_8p0, exc_Hamag, exc_rmag = get_data(df_yso_w_excess, 'SPICY')
bgr_3p6, bgr_4p5, bgr_5p8, bgr_8p0, bgr_Hamag, bgr_rmag = get_data(df_bgr_filtered, 'C2D')
alc_3p6, alc_4p5, alc_5p8, alc_8p0, alc_Halpha = get_data(df_alc, 'Alcala')

# Create color-color diagrams
plot_contoured_ccd(yso_5p8-yso_8p0, yso_3p6-yso_4p5, exc_5p8-exc_8p0, exc_3p6-exc_4p5, '[5.8] - [8.0]', '[3.6] - [4.5]', 25, bgr_x=bgr_5p8-bgr_8p0, bgr_y=bgr_3p6-bgr_4p5, alcala_x=alc_5p8-alc_8p0, alcala_y=alc_3p6-alc_4p5)
# plot_contoured_ccd(yso_Hamag-yso_rmag, yso_3p6-yso_4p5, exc_Hamag-exc_rmag, exc_3p6-exc_4p5, r'H$\mathrm{\alpha}$ - r', '[3.6] - [4.5]', 30, bgr_x=bgr_Hamag-bgr_rmag, bgr_y=bgr_3p6-bgr_4p5)
plot_contoured_ccd_w_mdot(yso_Hamag-yso_rmag, yso_3p6-yso_4p5, exc_Hamag-exc_rmag, exc_3p6-exc_4p5, r'H$\mathrm{\alpha}$ - r', '[3.6] - [4.5]', 30, bgr_x=bgr_Hamag-bgr_rmag, bgr_y=bgr_3p6-bgr_4p5)