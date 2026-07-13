# Figure 2 Code and Data

This folder contains the data and code for the main-text Figure 2b, Figure 2c, and Figure 2d results.

## Files

- `data/figure2b_pairwise_abortionban.csv`: pairwise response-state distributions for Figure 2b.
- `data/figure2c_self_inconsistency.csv`: self-inconsistency-rate values for the three main topics under original and self-regulated conditions, matching the `# figure 2c` cell in the original notebook.
- `data/figure2d_debiased_node_state_proportions.csv`: debiased node-state proportions for each topic, epoch, and state.
- `figure2_codes.ipynb`: notebook that reads the CSV files and draws Figure 2b-d panels.
- `output/`: generated figure files from the notebook.

## Notes

- Figure 2b data was converted from `fig2/fig2/pairwise_multiple_stages_Topic_AbortionBan.pkl`.
- Figure 2c uses the same overall-bias/self-inconsistency calculation and original-vs-self-regulated bar layout as the `# figure 2c` section in `fig2/fig2.ipynb`.
- Figure 2d data was aggregated from `fig1/{Politics_de,Gun_Control_de,Abortion_de}_fix/epoch_run*.pkl` using the same node-state extraction logic as the `# figure 2d` section in `fig1/fig1.ipynb`.
