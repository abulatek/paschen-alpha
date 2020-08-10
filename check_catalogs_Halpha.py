import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import sys
from astropy import units as u
from astropy.coordinates import SkyCoord

# Import the relevant .csv files, turn them into dataframes
filepath_background = 'background_xmatch_test.csv'
df_background = pd.read_csv(filepath_background)
#print(df_background)
#print("Number of rows in current background catalog:",len(df_background))

# Drop rows that have NaNs in any columns corresponding to fluxes
#print("Dropping rows that have NaNs in any important columns.")
df_background_dropped = df_background.dropna(subset=['FIR1','FIR2','FIR3','FIR4','Hamag','FJ','FH','FKs','rmag']) # Did not exclude MIPS NaNs
#print("Number of rows in current background catalog:",len(df_background_dropped),"-- dropped",len(df_background)-len(df_background_dropped))

#print(df_background_dropped)
background_RA = u.Quantity(df_background_dropped['RAJ2000_1'].values, u.deg)
background_DEC = u.Quantity(df_background_dropped['DEJ2000_1'].values, u.deg)
#print(background_RA)
#print(background_DEC)

c = SkyCoord(background_RA, background_DEC, frame='icrs')
#print(c)
c_gal = c.galactic
#print(c_gal)
background_l = (c_gal.l).to(u.deg)
background_b = (c_gal.b).to(u.deg)
#print(background_l)
#print(background_b)

# Try to determine whether we see H-alpha emitters in background stars
background_r_mag = u.Quantity(df_background_dropped['rmag'].values, u.mag)
background_r_ZP_Jy = 3086.72*u.Jy
background_r_flux = background_r_ZP_Jy*10**(-background_r_mag/(2.5*u.mag))
background_Ha_mag = u.Quantity(df_background_dropped['Hamag'].values, u.mag)
Ha_ZP_Jy = 2659.4*u.Jy # INT WFC H-alpha filter from http://svo2.cab.inta-csic.es/theory/fps/index.php?id=INT/IPHAS.Ha&&mode=browse&gname=INT&gname2=IPHAS#filter
background_Ha_flux = Ha_ZP_Jy*10**(-background_Ha_mag/(2.5*u.mag))

plt.figure(dpi = 150)
plt.grid()
plt.scatter(background_Ha_mag,background_Ha_mag - background_r_mag,color='xkcd:red',marker=".")
plt.plot(np.arange(-50,50,1),np.full(100,0),color='xkcd:black')
plt.xlabel('H-alpha mag', size = 10)
plt.ylabel('H-alpha mag minus r mag', size = 10)
plt.xlim(10,25)
#plt.ylim(10,25)
plt.title("Comparison of r-band and H-alpha magnitudes for c2d/VPHAS crossmatch", size = 10)
plt.show()
