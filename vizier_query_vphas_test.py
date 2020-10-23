from astroquery.vizier import Vizier

#vphas_coords = Vizier(columns=['RAJ2000','DEJ2000'], row_limit=-1).query_constraints(catalog='II/341/vphasp')[0]
#vphas_coords.write('vphas_coords_test_minus_one.csv')

vphas_coords = Vizier(columns=['RAJ2000','DEJ2000'], row_limit=319126837).query_constraints(catalog='II/341/vphasp')[0]
vphas_coords.write('vphas_coords_test_number.csv')
