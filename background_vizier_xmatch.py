from astroquery.xmatch import XMatch
from astropy import units as u

# RA and dec for both catalogs should already be in decimal degrees.
result = XMatch.query(cat1='vizier:II/341/vphasp', cat2='vizier:II/332/c2d', max_distance=1 * u.arcsec, colRA1='RAJ2000', colDec1='DEJ2000', colRA2='RAJ2000', colDec2='DEJ2000')

type(result)
print(result)

# Write result to a .csv file (can also use a VOTable file):
result.write('/blue/adamginsburg/abulatek/project_paschen_alpha/background_xmatch_test.csv')
