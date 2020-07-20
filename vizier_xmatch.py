from astroquery.xmatch import XMatch
from astropy import units as u

table_test = XMatch.query(cat1=open('alcala2017_halpha_ra_dec.csv'), cat2='vizier:II/332/c2d', max_distance=5 * u.arcsec, colRA1='RAJ2000', colDec1='DEJ2000')

type(table_test)

print(table_test)
