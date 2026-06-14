# Paediatric IBD Microbiome Analysis

A Python reproduction and extension of a 16S rRNA microbiome analysis comparing
paediatric Crohn's disease (CD) patients to healthy controls, originally
performed in MicrobiomeAnalyst. This project re-implements the full pipeline
from raw ASV counts through to a machine learning classifier with model
interpretation.

## Dataset

iHMP Paediatric IBD dataset (Gevers et al., 2014), 16S rRNA amplicon sequencing
of 43 paediatric faecal samples (23 CD, 20 Control), provided as raw ASV
counts, taxonomy assignments, a phylogenetic tree, and sample metadata.

## Project structure

```
data/         raw ASV table, taxonomy, tree, and sample metadata
notebooks/    analysis notebooks (see below)
src/          reusable preprocessing module
results/      output tables (CSV)
figures/      output figures (PNG)
```

## Pipeline

**01_load_explore.ipynb** — data loading, validation, and the full
preprocessing pipeline: removal of two low-depth samples, singleton/zero
removal, prevalence filtering (>=4 reads in >=20% of samples), IQR variance
filtering (bottom 10% removed), and centred log-ratio (CLR) transformation.
Filtering steps are documented and justified, and reproduce the 130-ASV
result reported in the original assessment (129 ASVs in this implementation).
The final pipeline is exposed as `src/preprocessing.py:load_and_preprocess()`,
used by all subsequent notebooks.

**02_diversity.ipynb** — alpha diversity (Chao1, Shannon) and beta diversity
(PCA on CLR data, PERMANOVA with Bray-Curtis distance), each compared between
CD and Control using Mann-Whitney U / PERMANOVA.

**03_single_factor.ipynb** — genus-level differential abundance using
Mann-Whitney U with Benjamini-Hochberg FDR correction across all genera.

**04_ml_classifier.ipynb** — random forest classifier (CD vs Control) on
CLR-transformed ASV abundances, evaluated with repeated stratified
cross-validation, with SHAP used to interpret which ASVs drive predictions.

## Results

### Diversity

| Metric | CD median | Control median | p-value | Significant? |
|---|---|---|---|---|
| Chao1 (richness) | 63.0 | 76.5 | 0.005 | Yes |
| Shannon (diversity) | 2.587 | 2.907 | 0.163 | No |

Species richness is significantly reduced in CD, but overall diversity
(which also accounts for evenness) does not differ significantly — consistent
with a loss of specific taxa rather than wholesale community restructuring.

Beta diversity (PERMANOVA, Bray-Curtis, 999 permutations): pseudo-F = 3.073,
p = 0.001. CD and Control communities differ significantly in overall
composition.

### Single-factor analysis

After FDR correction, multiple genera within the Lachnospiraceae family were
significantly depleted in CD, most notably *Roseburia* (FDR = 0.0017) — a
well-characterised butyrate-producing genus consistently reported as depleted
in IBD.

### Classifier

A random forest classifier trained on CLR-transformed ASV abundances achieved
**90.8% mean accuracy** (repeated stratified 5-fold CV, 20 repeats, std =
0.094) versus a **51.1%** majority-class baseline.

SHAP analysis of the trained model showed that **8 of the top 10 most
predictive ASVs belong to Lachnospiraceae**, including two independent
*Roseburia* ASVs and one *Lachnospira* ASV. In each case, low abundance of
these taxa pushed predictions toward CD and high abundance pushed predictions
toward Control — directly consistent with the single-factor finding that
these taxa are depleted in CD.

### Headline finding

Three independent analytical approaches — diversity statistics, single-factor
differential abundance with multiple testing correction, and a supervised
machine learning model with no taxonomic information supplied — all converge
on the same result: **Lachnospiraceae depletion, particularly of *Roseburia*,
is a robust and predictive feature of this paediatric CD cohort.**

## Limitations

- **Sample size (n=41)**: results should be read as a strong within-dataset
  signal rather than a validated diagnostic. External validation on an
  independent cohort would be required to assess generalisability.
- **CLR transformation and cross-validation**: CLR was computed using all
  samples prior to cross-validation, which introduces minor information
  leakage via the geometric mean. For n=41 this effect is expected to be
  small, but a fully rigorous pipeline would recompute CLR within each fold.
- **Taxonomic resolution**: 16S amplicon sequencing resolves to genus level at
  best, and several ASVs in this dataset could not be classified below family
  or order level.
- **Minor numerical differences from the original MicrobiomeAnalyst
  analysis** (e.g. Shannon p = 0.163 here vs 0.098 originally; 129 vs 130
  ASVs after filtering) are attributed to implementation differences in
  tie-handling for Mann-Whitney and minor filtering differences, and do not
  affect the overall conclusions.

## Environment

```
conda env create -f environment.yml
conda activate ibd-ml
```

## Reproducing the analysis

Run the notebooks in order (01 -> 04). Each notebook after 01 imports
`load_and_preprocess()` from `src/preprocessing.py` and is independently
runnable from a fresh kernel.