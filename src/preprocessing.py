# src/preprocessing.py
import pandas as pd
import numpy as np
from scipy.stats import gmean

def load_and_preprocess():
    asv = pd.read_csv('../data/ibd_asv_table.txt', sep='\t', index_col=0)
    meta = pd.read_csv('../data/ibd_meta.csv', index_col=0)
    taxa = pd.read_csv('../data/ibd_taxa.txt', sep='\t', index_col=0)
    
    meta.index = meta.index.astype(str)
    asv = asv.drop(columns=['219659', '206768'])
    meta = meta.drop(index=['219659', '206768'])
    asv = asv[asv.sum(axis=1) > 1]
    
    min_samples = int(np.ceil(0.20 * asv.shape[1]))
    prevalence = (asv >= 4).sum(axis=1)
    asv = asv[prevalence >= min_samples]
    
    variance = asv.var(axis=1)
    asv = asv[variance > variance.quantile(0.10)]
    
    asv_pseudo = asv + 1
    geo_means = asv_pseudo.apply(gmean, axis=0)
    asv_clr = np.log(asv_pseudo.divide(geo_means, axis=1))
    
    return asv, asv_clr, meta, taxa