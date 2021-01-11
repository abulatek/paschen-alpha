# Produce a color-color diagram that shows the potential discovery space for PASHION

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from astropy import units as u
import pylab as pl
import matplotlib as mpl
from adaptive_param_plot import *

plt.rcParams['text.latex.preamble'] = [r'\usepackage{gensymb}']

def import_csv(filename, columns, sourceName, drop_NaN=True):
    '''Import contents of a .csv file into a pandas dataframe, dropping NaNs
    when specified and grouping by specified unique identifier.'''
    df = pd.read_csv(filename)
    if drop_NaN==True:
        df = df.dropna(subset=columns)
    df = df.groupby(sourceName).mean()
    return df

def get_data(df):
    '''Get data from a given dataframe.'''
    df_3p6, df_4p5, df_5p8, df_8p0 = df['mag3_6'].values, df['mag4_5'].values, df['mag5_8'].values, df['mag8_0'].values
    return df_3p6, df_4p5, df_5p8, df_8p0

def plot_contoured_ccd(total_x, total_y, subset_x, subset_y, x_lab, y_lab, bins):
    '''Plot a color-color diagram with contours in dense areas.'''
    plt.figure(dpi = 100)
    plt.grid()
    adaptive_param_plot(total_x,total_y,marker_color='#19967D',bins=bins,fill=False,alpha=1,threshold=10,cmap=None,colors='#19967D',label="Total SPICY sample")
    adaptive_param_plot(subset_x,subset_y,marker_color='#DE5F85',bins=bins,fill=False,alpha=1,threshold=10,cmap=None,colors='#DE5F85',label="SPICY/VPHAS cross-match")
    plt.xlabel(x_lab)
    plt.ylabel(y_lab)
    plt.title("SPICY YSOs covered by VPHAS")
    plt.legend()
    plt.tight_layout()
    plt.savefig("SPICY_YSOs_covered_by_VPHAS.png", dpi=250, facecolor='w', edgecolor='w')
    # plt.show()

total = import_csv('table1.csv',columns=['mag3_6','mag4_5','mag5_8','mag8_0'],sourceName='SPICY')
subset = import_csv('xmatch_SPICY_VPHAS.csv',columns=['mag3_6','mag4_5','mag5_8','mag8_0'],sourceName='SPICY')

total_3p6, total_4p5, total_5p8, total_8p0 = get_data(total)
subset_3p6, subset_4p5, subset_5p8, subset_8p0 = get_data(subset)

plot_contoured_ccd(total_5p8-total_8p0, total_3p6-total_4p5, subset_5p8-subset_8p0, subset_3p6-subset_4p5, '[5.8] - [8.0]', '[3.6] - [4.5]', 30)
