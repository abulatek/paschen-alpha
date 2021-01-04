# Cross-match SPICY (Spitzer/IRAC) data on YSO candidates with VPHAS and/or IPHAS (H-alpha)

from astroquery.xmatch import XMatch
from astropy import units as u
from astropy import table, coordinates

def read_table(filename, coord_convert_deg=False):
    '''Read in table to be crossmatched as an astropy table.'''
    print("Reading in table")
    tbl = table.Table.read(filename)
    if coord_convert_deg==True:
        print("Converting coordinates to decimal form")
        tbl.add_column(name='ra', col=coordinates.SkyCoord(tbl['RAJ2000'], tbl['DEJ2000'], frame='fk5', unit=(u.h, u.deg)).ra)
        tbl.add_column(name='dec', col=coordinates.SkyCoord(tbl['RAJ2000'], tbl['DEJ2000'], frame='fk5', unit=(u.h, u.deg)).dec)
    print("Returning table")
    return tbl

tbl = read_table('table1.csv', coord_convert_deg=False)
result = XMatch.query(cat1=tbl, cat2='vizier:II/341/vphasp', max_distance=1*u.arcsec, colRA1='ra', colDec1='dec', colRA2='RAJ2000', colDec2='DEJ2000')
result.write('SPICY_VPHAS_xmatch.csv')