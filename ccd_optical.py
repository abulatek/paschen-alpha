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
YSO_type_str_list = ['YSOc', 'YSOc_PAH-em', 'YSOc_red', 'YSOc_star+dust(IR1)', 'YSOc_star+dust(IR2)', 'YSOc_star+dust(IR3)', 'YSOc_star+dust(IR4)', 'YSOc_star+dust(MP1)']
df_YSO = df_background_dropped.loc[df_background_dropped['OType'].isin(YSO_type_str_list)]

# Plot color-color diagrams
plt_type = 3

plt.figure(dpi = 150)
plt.grid()
if plt_type == 1:
        plt.scatter(Hamag - rmag, umag - gmag, marker='.', color='black', label='non-YSO', alpha=0.2)
        x_color = df_YSO['Hamag'].values - df_YSO['rmag'].values
        y_color = df_YSO['umag'].values - df_YSO['gmag'].values
        plt.scatter(x_color, y_color, marker='.', color='dodgerblue', label='YSO candidate')
        plt.ylabel("u - g", size = 14)
if plt_type == 2:
        plt.scatter(Hamag - rmag, gmag - rmag, marker='.', color='black', label='non-YSO', alpha=0.2)
        x_color = df_YSO['Hamag'].values - df_YSO['rmag'].values
        y_color = df_YSO['gmag'].values - df_YSO['rmag'].values
        plt.scatter(x_color, y_color, marker='.', color='dodgerblue', label='YSO candidate')
        plt.ylabel("g - r", size = 14)
if plt_type == 3:
        plt.scatter(Hamag - rmag, rmag - imag, marker='.', color='black', label='non_YSO', alpha=0.2)
        x_color = df_YSO['Hamag'].values - df_YSO['rmag'].values
        y_color = df_YSO['rmag'].values - df_YSO['imag'].values
        plt.scatter(x_color, y_color, marker='.', color='dodgerblue', label='YSO candidate')
        plt.ylabel("r - i", size = 14)
plt.xlabel("H-alpha - r", size = 14)
plt.legend(loc="upper right", fontsize = 6)
plt.title("VPHAS/c2d crossmatch color-color diagram", size = 14)
plt.show()
