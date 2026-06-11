# ibd-microbiome-ml
Reproducing and extending paediatric IBD microbiome analysis in Python with ML classification
# Paediatric IBD Microbiome Analysis

Reproducing and extending a 16S rRNA microbiome analysis of paediatric 
Crohn's disease vs healthy controls, originally performed in MicrobiomeAnalyst.

## Project structure
- `data/` — OTU abundance table and sample metadata
- `notebooks/` — analysis notebooks (01_load_explore, 02_diversity, 03_ml_classifier)
- `src/` — reusable utility functions
- `results/` — processed outputs
- `figures/` — saved plots

## Environment setup
conda env create -f environment.yml
conda activate ibd-ml

## Data
iHMP Paediatric IBD dataset (Gevers et al. 2014), downloaded from MicrobiomeAnalyst.

## Analysis overview
1. Data loading, filtering and CLR normalisation
2. Alpha and beta diversity analysis
3. Random forest classification of CD vs control with SHAP interpretation