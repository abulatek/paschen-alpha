import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import sys
from astropy import units as u

# Import the relevant .csv files, turn them into dataframes
filepath_background = 'background_xmatch_test.csv'
df_background = pd.read_csv(filepath_background)

# Drop rows that have NaNs in any columns corresponding to fluxes
#df_background_dropped = df_background.dropna(subset=['umag', 'gmag', 'rmag', 'imag', 'Hamag'])
df_background_dropped = df_background

# Get magnitudes
umag = u.Quantity(df_background_dropped['umag'].values, u.mag)
gmag = u.Quantity(df_background_dropped['gmag'].values, u.mag)
rmag = u.Quantity(df_background_dropped['rmag'].values, u.mag)
imag = u.Quantity(df_background_dropped['imag'].values, u.mag)
Hamag = u.Quantity(df_background_dropped['Hamag'].values, u.mag)

# Get magnitudes for specific types of YSOs 
df_YSOc = df_background_dropped.loc[df_background_dropped['OType'] == 'YSOc']
df_YSOc_PAH_em = df_background_dropped.loc[df_background_dropped['OType'] == 'YSOc_PAH-em']
df_YSOc_red = df_background_dropped.loc[df_background_dropped['OType'] == 'YSOc_red']
df_YSOc_star_dust_IR1 = df_background_dropped.loc[df_background_dropped['OType'] == 'YSOc_star+dust(IR1)']
df_YSOc_star_dust_IR2 = df_background_dropped.loc[df_background_dropped['OType'] == 'YSOc_star+dust(IR2)']
df_YSOc_star_dust_IR3 = df_background_dropped.loc[df_background_dropped['OType'] == 'YSOc_star+dust(IR3)']
df_YSOc_star_dust_IR4 = df_background_dropped.loc[df_background_dropped['OType'] == 'YSOc_star+dust(IR4)']
df_YSOc_star_dust_MP1 = df_background_dropped.loc[df_background_dropped['OType'] == 'YSOc_star+dust(MP1)']

# Plot color-color diagrams
plt_type = 1

YSO_type_list = ['YSO_c', 'YSOc_PAH-em', 'YSOc_red', 'YSOc_star+dust(IR1)', 'YSOc_star+dust(IR2)', 'YSOc_star+dust(IR3)', 'YSOc_star+dust(IR4)', 'YSOc_star+dust(MP1)']
color_list = ['red', 'orange', 'gold', 'limegreen', 'lightblue', 'dodgerblue', 'mediumorchid', 'deeppink']

plt.figure(dpi = 150)
plt.grid()
if plt_type == 1:
        plt.scatter(Hamag - rmag, umag - gmag, marker='.', color='black', label='non-YSO')
        i = 0
        for YSO_type in [df_YSOc, df_YSOc_PAH_em, df_YSOc_red, df_YSOc_star_dust_IR1, df_YSOc_star_dust_IR2, df_YSOc_star_dust_IR3, df_YSOc_star_dust_IR4, df_YSOc_star_dust_MP1]:
                x_color = YSO_type['Hamag'].values - YSO_type['rmag'].values
                y_color = YSO_type['umag'].values - YSO_type['gmag'].values
                plt.scatter(x_color, y_color, marker='.', color=color_list[i], label=YSO_type_list[i])
                i += 1
        plt.ylabel("u - g", size = 14)
if plt_type == 2:
        plt.scatter(Hamag - rmag, gmag - rmag, marker='.', color='xkcd:black', label='non-YSO')
        i = 0
        for YSO_type in [df_YSOc, df_YSOc_PAH_em, df_YSOc_red, df_YSOc_star_dust_IR1, df_YSOc_star_dust_IR2, df_YSOc_star_dust_IR3, df_YSOc_star_dust_IR4, df_YSOc_star_dust_MP1]:
                x_color = YSO_type['Hamag'].values - YSO_type['rmag'].values
                y_color = YSO_type['gmag'].values - YSO_type['rmag'].values
                plt.scatter(x_color, y_color, marker='.', color=color_list[i], label=YSO_type_list[i])
                i += 1
        plt.ylabel("g - r", size = 14)
if plt_type == 3:
        plt.scatter(Hamag - rmag, rmag - imag, marker='.', color='xkcd:black', label='non_YSO')
        i = 0
        for YSO_type in [df_YSOc, df_YSOc_PAH_em, df_YSOc_red, df_YSOc_star_dust_IR1, df_YSOc_star_dust_IR2, df_YSOc_star_dust_IR3, df_YSOc_star_dust_IR4, df_YSOc_star_dust_MP1]:
                x_color = YSO_type['Hamag'].values - YSO_type['rmag'].values
                y_color = YSO_type['rmag'].values - YSO_type['imag'].values
                plt.scatter(x_color, y_color, marker='.', color=color_list[i], label=YSO_type_list[i])
                i += 1
        plt.ylabel("r - i", size = 14)
plt.xlabel("H-alpha - r", size = 14)
plt.legend(loc="upper right", fontsize = 6)
plt.title("VPHAS/c2d crossmatch color-color diagram", size = 14)
plt.show()
