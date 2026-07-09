# Figure 3 Code and Data

This folder contains the data and code for the main-text Figure 3a, Figure 3c, Figure 3d, Figure 3e, Figure 3f, and Figure 3g results.

## Files

- `data/figure3a_homophily.csv`: homophilic interaction proportions over time for Figure 3a.
- `data/figure3cd_interaction_effects.csv`: interaction-level effect data for Figure 3c and Figure 3d bar plots.
- `data/figure3efg_polarization_bar_data.csv`: bar-plot data for Figure 3e, Figure 3f, and Figure 3g.
- `figure3_codes.ipynb`: notebook that reads the CSV files and draws Figure 3a/c/d/e/f/g panels.
- `output/`: generated figure files from the notebook.

## Notes

- Figure 3a/c/d data was aggregated from `fig5/Echo_vis/{Politics,Gun_Control,Abortion}_de_fix/epoch_run*.pkl`.
- Figure 3e/f/g data was aggregated from the Figure 4 parameter and control-run files used by `fig4/fig4.ipynb`.
- For Figure 3e/f/g, only the bar-plot data is included; the line-plot data from the original cells is omitted.
