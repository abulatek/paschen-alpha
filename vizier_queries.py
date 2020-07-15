from astroquery.vizier import Vizier
# Access all columns
alcala_all_tbl = Vizier(columns=['**']).query_constraints(catalog='J/A+A/561/A2/results')[0]
alcala_all_tbl.write('alcala_all.csv')
