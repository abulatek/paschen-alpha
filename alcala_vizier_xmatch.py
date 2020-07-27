from astroquery.xmatch import XMatch
from astropy import units as u
from astropy import table, coordinates

# VizieR's xMatch service only accepts coordinates in degrees (this is true for browser version too). Need to convert.
## Read in table to be xMatch-ed as an astropy table:
tbl = table.Table.read('alcala2017_halpha_ra_dec.csv')
## Calculate and add new RA column in degrees: (written by Adam)
tbl.add_column(name='ra', col=coordinates.SkyCoord(tbl['RAJ2000'], tbl['DEJ2000'], frame='fk5', unit=(u.h, u.deg)).ra)
## Calculate and add new dec column in degrees: (written by Adam)
tbl.add_column(name='dec', col=coordinates.SkyCoord(tbl['RAJ2000'], tbl['DEJ2000'], frame='fk5', unit=(u.h, u.deg)).dec)
# Use new table to xMatch with VizieR catalog (here, c2d):
## Make sure you specify what the names of the RA and dec columns are in each catalog.
result = XMatch.query(cat1=tbl, cat2='vizier:II/332/c2d', max_distance=1 * u.arcsec, colRA1='ra', colDec1='dec', colRA2='RAJ2000', colDec2='DEJ2000')

type(result)
print(result)

# Write result to a .csv file (can also use a VOTable file):
result.write('/blue/adamginsburg/abulatek/project_paschen_alpha/xmatch_test.csv')
