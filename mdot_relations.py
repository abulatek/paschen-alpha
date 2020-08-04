import numpy as np
from astropy import units as u
from astropy import constants

def lacc(mdot, rstar=u.R_sun, mstar=u.M_sun):
    return (mdot / 1.25 * constants.G * mstar / rstar).to(u.L_sun)

def log_pab(lacc):
    return 1/1.06 * np.log10(lacc/u.L_sun) - 2.76/1.06

def log_paa(lacc):
    return log_pab(lacc) + np.log10(2.86 * 0.336 / 0.347)

def L_paa(lacc):
    return 10**log_paa(lacc) * u.L_sun

def S_paa(lacc, distance=8*u.kpc):
    # I think this is wrong; I probably got a unit wrong above
    return (L_paa(lacc) / distance**2).to(u.erg/u.s/u.cm**2)

if __name__ == "__main__":

    import pylab as pl
    pl.ion()
    from astroquery.vizier import Vizier
    # Ekstrom 2012 evolutionary models; we'll use the age=10^6.5 for zero-age radii, lums
    tbl = Vizier(row_limit=1e7, columns=['**']).get_catalogs('J/A+A/537/A146/iso')[0]

    zeroage = tbl['logAge'] == 6.5
    masses = tbl['Mass'][zeroage].quantity
    radius = tbl['Rpol'][zeroage].quantity

    pl.clf()
    mdot = np.logspace(-9, -3)*u.M_sun/u.yr
    for mass, rad in list(zip(masses, radius))[::230]:
        acclum = lacc(mdot, rstar=rad, mstar=mass)
        paalum = S_paa(acclum)
        pl.loglog(mdot, paalum, label=f'R={rad.to(u.R_sun):0.1f} M={mass.to(u.M_sun):0.1f}')

    pl.legend(loc='best')
