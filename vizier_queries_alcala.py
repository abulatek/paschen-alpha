from astroquery.vizier import Vizier
from astropy.table import join

# Access all columns from the Alcala+2014 survey
alcala2014_all_tbl = Vizier(columns=['**']).query_constraints(catalog='J/A+A/561/A2/results')[0]
alcala2014_all_tbl.write('alcala2014_all.csv')

# Access all columns from the Alcala+2017 survey (across different tables)
alcala2017_ra_dec_tbl = Vizier(columns=['**']).query_constraints(catalog='J/A+A/600/A20/table1')[0]
alcala2017_tbl1 = Vizier(columns=['**']).query_constraints(catalog='J/A+A/600/A20/tablee1')[0]
alcala2017_tbl2 = Vizier(columns=['**']).query_constraints(catalog='J/A+A/600/A20/tablee2')[0]
alcala2017_tbl3 = Vizier(columns=['**']).query_constraints(catalog='J/A+A/600/A20/tablee3')[0]
alcala2017_tbl4 = Vizier(columns=['**']).query_constraints(catalog='J/A+A/600/A20/tablee4')[0]
alcala2017_tbl5 = Vizier(columns=['**']).query_constraints(catalog='J/A+A/600/A20/tablee5')[0]

alcala2017_ra_dec_tbl.write('alcala2017_ra_dec.csv') # ended up removing the final 4 rows -- should look up why there isn't spectral line data for those sources
alcala2017_tbl1.write('alcala2017_1.csv')
alcala2017_tbl2.write('alcala2017_2.csv')
alcala2017_tbl3.write('alcala2017_3.csv')
alcala2017_tbl4.write('alcala2017_4.csv')
alcala2017_tbl5.write('alcala2017_5.csv')

## Make a table that includes both Halpha data and RA/dec for sources in Alcala+2017
alcala2017_halpha_ra_dec_tbl = join(alcala2017_ra_dec_tbl, alcala2017_tbl1)
alcala2017_halpha_ra_dec_tbl.write('alcala2017_halpha_ra_dec.csv')
