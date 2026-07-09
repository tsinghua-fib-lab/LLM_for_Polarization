# Figure 4 Code and Data

This folder contains the data and code for the main-text Figure 4b, Figure 4c, Figure 4d, Figure 4e, and Figure 4f results.

## Files

- `data/figure4_polarization_after_intervention.csv`: polarization levels after intervention for Figure 4b-f.
- `data/figure4_homophily_after_intervention.csv`: homophilic interaction levels after intervention for Figure 4b-f.
- `figure4_codes.ipynb`: notebook that reads the CSV files and draws Figure 4b-f panels.
- `output/`: generated figure files from the notebook.

## Notes

- The data was aggregated from `fig5/Echo_vis/Politics_de_fix/epoch_run*.pkl` and `fig5/Echo_vis/intv/{random,no_extreme,selective,no_confirmation,KOL}_fix/epoch_run*.pkl`.
- Each panel compares the original condition with one intervention over timesteps 35-40, matching the plotting cells in `fig5/Echo_vis/intervention_experiments.ipynb`.
