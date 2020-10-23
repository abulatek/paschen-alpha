import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
from astropy.table import Table

# Example fileame:
# ADP.2020-02-12T10:26:23.730.fits

filename = "/orange/adamginsburg/adhoc/ADP.2020-02-12T10:26:23.730.fits"

hdul = fits.open(filename)
#hdul.info()
#print(repr(hdul[0].header))

#print(hdul[-1].columns)
print(hdul[4].data)

#catalog1 = Table.read("/orange/adamginsburg/adhoc/ADP.2020-02-12T10:26:23.730.fits")

hdul.close()

