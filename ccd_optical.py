import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import sys
from astropy import units as u

# Import the relevant .csv files, turn them into dataframes
filepath_background = 'background_xmatch_test.csv'
df_background = pd.read_csv(filepath_background)

# Ignore objects that don't have H-alpha data
df_background_dropped = df_background.dropna(subset=['Hamag','rmag','imag'])

# Get magnitudes
umag = u.Quantity(df_background_dropped['umag'].values, u.mag)
gmag = u.Quantity(df_background_dropped['gmag'].values, u.mag)
rmag = u.Quantity(df_background_dropped['rmag'].values, u.mag)
r2mag = u.Quantity(df_background_dropped['r2mag'].values, u.mag)
imag = u.Quantity(df_background_dropped['imag'].values, u.mag)
Hamag = u.Quantity(df_background_dropped['Hamag'].values, u.mag)

# Get magnitudes for specific types of YSOs 
YSO_type_str_list = ['YSOc', 'YSOc_PAH-em', 'YSOc_red', 'YSOc_star+dust(IR1)', 'YSOc_star+dust(IR2)', 'YSOc_star+dust(IR3)', 'YSOc_star+dust(IR4)', 'YSOc_star+dust(MP1)']
df_YSO = df_background_dropped.loc[df_background_dropped['OType'].isin(YSO_type_str_list)]
#print(len(df_YSO))
#print(df_YSO[['sourceID', 'umag', 'gmag', 'r2mag', 'rmag', 'imag']])

# Check out what's up with possibly duplicate YSOs
#df_YSO = df_YSO.groupby('sourceID')
df_YSO = df_YSO.drop_duplicates()
df_YSO_sort = df_YSO.sort_values(by=['rmag'])
print(len(df_YSO_sort))
print(df_YSO_sort[['sourceID', 'umag', 'gmag', 'r2mag', 'rmag', 'imag']])

# Plot color-color diagrams
plt_type = 3

plt.figure(dpi = 150)
plt.grid()
if plt_type == 1:
	plt.scatter(umag - gmag, rmag - Hamag, marker='.', color='black', label='non-YSO', alpha=0.2)
	x_color = df_YSO['umag'].values - df_YSO['gmag'].values
	y_color = df_YSO['rmag'].values - df_YSO['Hamag'].values
	plt.scatter(x_color, y_color, marker='.', color='dodgerblue', label='YSO candidate')
	plt.xlabel("u - g", size = 14)
if plt_type == 2:
	plt.scatter(gmag - r2mag, rmag - Hamag, marker='.', color='black', label='non-YSO', alpha=0.2)
	x_color = df_YSO['gmag'].values - df_YSO['r2mag'].values
	y_color = df_YSO['rmag'].values - df_YSO['Hamag'].values
	plt.scatter(x_color, y_color, marker='.', color='dodgerblue', label='YSO candidate')
	plt.xlabel("g - r2", size = 14)
if plt_type == 3:
	plt.scatter(rmag - imag, rmag - Hamag, marker='.', color='black', label='non-YSO', alpha=0.2)
	x_color = df_YSO['rmag'].values - df_YSO['imag'].values
	y_color = df_YSO['rmag'].values - df_YSO['Hamag'].values
	#print(len(x_color),len(y_color))
	plt.scatter(x_color, y_color, marker='.', color='dodgerblue', label='YSO candidate')  
	plt.xlabel("r - i", size = 14)
plt.ylabel("r - H-alpha", size = 14)
plt.legend(loc="upper right", fontsize = 6)
plt.title("VPHAS/c2d crossmatch color-color diagram", size = 14)
plt.show()

