# Figure 1 Code and Data

This folder contains the data and code for the main-text Figure 1b, Figure 1c, and Figure 1d results.

## Files

- `data/figure1_node_state_proportions.csv`: aggregated node-state proportions for each topic, epoch, and state.
- `figure1_codes.ipynb`: notebook that reads the CSV and draws Figure 1b-d panels.
- `output/`: generated figure files from the notebook.

## Data Columns

- `topic`: original topic key used by the plotting code.
- `topic_title`: display title in the figure.
- `epoch`: simulation time step, 0-40.
- `state_order`: plotting order, matching the original color order.
- `state`: opinion state, from -2 to 2.
- `state_label`: readable state label.
- `count`: number of unique nodes in the state at the epoch.
- `total_nodes`: total number of unique nodes at the epoch.
- `proportion`: `count / total_nodes`.

The CSV was aggregated from the original `fig1/{Politics,Gun_Control,Abortion}_fix/epoch_run*.pkl` files using the same node-state extraction logic as `fig1/fig1.ipynb`.
