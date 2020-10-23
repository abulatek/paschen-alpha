from astroquery.vizier import Vizier
from astropy import table
from astropy.table import join

# Readd in table to be xMatched
tbl = table.Table.read('alcala_full_spec.csv')
# Retrieve spectral type data from Alcala catalog
alcala2017_sptype_tbl = Vizier(columns=['**'], row_limit=-1).query_constraints(catalog='J/A+A/600/A20/tablea23')[0] # includes spectral type for many sources (81 rows)

# Join full table with spectral type table based on common columns 
alcala_full_spec_sptype = join(tbl, alcala2017_sptype_tbl, keys='Object') # Matches based on common columns specified in 'keys' parameter

# Write result to a .csv file (can also use a VOTable file)
alcala_full_spec_sptype.write('alcala_full_spec_sptype.csv')
