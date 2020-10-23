from astroquery.vizier import Vizier
from astropy.table import join
from astropy.table import Table
from astropy.table import QTable

# Access all columns from the Alcala+2014 survey
#alcala2014_all_tbl = Vizier(columns=['**']).query_constraints(catalog='J/A+A/561/A2/results')[0]
#alcala2014_all_tbl.write('alcala2014_all.csv')

# Access all columns from the Alcala+2017 survey (across different tables)
alcala2017_ra_dec_tbl = Vizier(columns=['**'], row_limit=-1).query_constraints(catalog='J/A+A/600/A20/table1')[0] # includes RA/dec for each source (57 rows)
alcala2017_tbl1 = Vizier(columns=['**']).query_constraints(catalog='J/A+A/600/A20/tablee1')[0] # includes H-alpha data (46 rows)
#alcala2017_tbl2 = Vizier(columns=['**']).query_constraints(catalog='J/A+A/600/A20/tablee2')[0]
#alcala2017_tbl3 = Vizier(columns=['**']).query_constraints(catalog='J/A+A/600/A20/tablee3')[0]
#alcala2017_tbl4 = Vizier(columns=['**']).query_constraints(catalog='J/A+A/600/A20/tablee4')[0]
#alcala2017_tbl5 = Vizier(columns=['**']).query_constraints(catalog='J/A+A/600/A20/tablee5')[0]

# Remove final four rows of RA and dec table (rejected as Lupus members)
alcala2017_ra_dec_tbl.remove_rows([-1, -2, -3, -4])

# Export tables individually as .csv files
#alcala2017_ra_dec_tbl.write('alcala2017_ra_dec.csv')
#alcala2017_tbl1.write('alcala2017_1.csv')
#alcala2017_tbl2.write('alcala2017_2.csv')
#alcala2017_tbl3.write('alcala2017_3.csv')
#alcala2017_tbl4.write('alcala2017_4.csv')
#alcala2017_tbl5.write('alcala2017_5.csv')

# Make a table that includes both Halpha data and RA/dec for sources in Alcala+2017
alcala2017_halpha_ra_dec_tbl = join(alcala2017_ra_dec_tbl, alcala2017_tbl1) # Matches based on common columns
alcala2017_halpha_ra_dec_tbl.write('alcala2017_halpha_ra_dec.csv')

# Access accretion information from Alcala+2017 survey
#alcala2017_acc_tbl = Vizier(columns=['**']).query_constraints(catalog='J/A+A/600/A20/tablea23')[0]
#alcala2017_acc_tbl.write('alcala2017_acc.csv')

