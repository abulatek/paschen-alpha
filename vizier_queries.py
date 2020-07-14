# Access all columns
alcala_all_tbl = Vizier(columns=['**']).query_constraints(catalog='J/A+A/561/A2/results')[0]
alcala_all_tbl.write('alcala_all.csv')

# Access only Spitzer/WISE fluxes and hydrogen spectral line intensities, along with limit flags and uncertainties
#columns_photom = ['Name', 'RAJ2000', 'DEJ2000', 
                    'l_F3.4', 'F3.4', 'e_F3.4', 
                    'l_F3.6', 'F3.6', 'e_F3.6',
                    'l_F4.5', 'F4.5', 'e_F4.5',
                    'l_F4.6', 'F4.6', 'e_F4.6',
                    'l_F5.8', 'F5.8', 'e_F5.8',
                    'l_F8.0', 'F8.0', 'u_F8.0', 'e_F8.0',
                    'l_F12.8', 'F12.8', 'e_F12.8',
                    'l_F22.4', 'F22.4', 'e_F22.4',
                    'l_F24', 'F24', 'u_F24', 'e_F24',
                    'l_F70', 'F70', 'e_F70',
                    'F_Ha_', 'e_F_Ha_', 'W_Ha_', 'e_W_Ha_',
                    'F_Hb_', 'e_F_Hb_', 'W_Hb_', 'e_W_Hb_',
                    'F_Hg_', 'e_F_Hg_', 'W_Hg_', 'e_W_Hg_',
                    'F_Hd_', 'e_F_Hd_', 'W_Hd_', 'e_W_Hd_',
                    'F_He_', 'f_F_He_', 'e_F_He_', 'W_He_', 'e_W_He_',
                    'F_H8_', 'e_F_H8_', 'W_H8_', 'e_W_H8_',
                    'F_H9_', 'e_F_H9_', 'W_H9_', 'e_W_H9_',
                    'l_F_H10_', 'F_H10_', 'e_F_H10_', 'W_H10_', 'e_W_H10_',
                    'l_F_H11_', 'F_H11_', 'e_F_H11_', 'W_H11_', 'e_W_H11_',
                    'l_F_H12_', 'F_H12_', 'e_F_H12_', 'W_H12_', 'e_W_H12_',
                    'l_F_H13_', 'F_H13_', 'e_F_H13_', 'W_H13_', 'e_W_H13_',
                    'l_F_H14_', 'F_H14_', 'e_F_H14_', 'W_H14_', 'e_W_H14_',
                    'l_F_H15_', 'F_H15_', 'e_F_H15_', 'W_H15_', 'e_W_H15_',
                    'l_F_Pab_', 'F_Pab_', 'e_F_Pab_', 'W_Pab_', 'e_W_Pab_',
                    'l_F_Pag_', 'F_Pag_', 'e_F_Pag_', 'W_Pag_', 'e_W_Pag_',
                    'l_F_Pad_', 'F_Pad_', 'e_F_Pad_', 'W_Pad_', 'e_W_Pad_',
                    'l_F_Pa8_', 'F_Pa8_', 'e_F_Pa8_', 'W_Pa8_', 'e_W_Pa8_',
                    'l_F_Pa9_', 'F_Pa9_', 'e_F_Pa9_', 'W_Pa9_', 'e_W_Pa9_',
                    'l_F_Pa10_', 'F_Pa10_', 'e_F_Pa10_', 'W_Pa10_', 'e_W_Pa10_',
                    'l_F_Brg_', 'F_Brg_', 'e_F_Brg_', 'W_Brg_', 'e_W_Brg_',
                    'l_F_Br8_', 'F_Br8_', 'e_F_Br8_', 'W_Br8_', 'e_W_Br8_']
#alcala_photom_tbl = Vizier(columns=columns_photom).query_constraints(catalog='J/A+A/561/A2/results')[0]
#alcala_photom_tbl.write('alcala_photom.csv')
