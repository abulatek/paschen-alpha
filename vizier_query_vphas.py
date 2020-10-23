from astroquery.vizier import Vizier
import astropy.units as u
import astropy.coordinates as coord

Vizier.ROW_LIMIT = -1

#catalogs = Vizier.get_catalogs("II/341/vphasp")
#print(catalogs)

# Query VPHAS in a large area in c2d fields
result = Vizier.query_region(coordinates = coord.SkyCoord(ra=235, dec=-34, unit=(u.deg, u.deg), frame='icrs'), width="30m", catalog="II/341/vphasp")[0]

print(result)
#result.write('vphas_test.csv")
