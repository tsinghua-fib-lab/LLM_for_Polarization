# LLM for Polarization

Code and data for **A synthetic testbed of networked large language model agents for studying spontaneous opinion polarization**, in principle accepted by *Nature Communications*.

This repository contains the simulation code, source data, and curated figure data/code used for the main-text figures.

## Repository Structure

- `run.py`: example entry point for launching a simulation.
- `simulate.py`: baseline simulation code.
- `simulate_debiased.py`: self-regulated/debiased simulation code.
- `utils.py`: LLM prompting and simulation utilities.
- `source_data/`: network initialization files and source interaction data.
- `figures/figure1` to `figures/figure4`: main-text figure data and plotting notebooks.

## Source Data

`source_data/Data_WS_2000/` contains the original network initialization files used by the simulation code:

- `edges.csv`
- `data_ID2Net_ID.csv`
- `user_message_generate.json`

`source_data/Partisan Alignment/`, `source_data/Gun Control/`, and `source_data/Abortion Ban/` contain epoch-level interaction data for the three main topics. Each `epoch_run*.pkl` file is a pandas DataFrame where each row is a directed interaction with:

- `source node Id`
- `target node Id`
- `source node state`
- `target node state`

Opinion states are coded from `-2` to `2`. See `source_data/README.md` and `source_data/metadata.csv` for details.

## Figure Data and Code

Each figure folder includes a plotting notebook, minimal CSV data, and generated panel PDFs:

- `figures/figure1/figure1_codes.ipynb`
- `figures/figure2/figure2_codes.ipynb`
- `figures/figure3/figure3_codes.ipynb`
- `figures/figure4/figure4_codes.ipynb`

The notebooks are designed to be run from their own folders, reading local files from `data/` and writing PDFs to `output/`.

## Environment

The original simulation environment used:

```text
python == 3.8.11
numpy == 1.23.5
scipy == 1.10.1
scikit-learn == 1.2.2
matplotlib == 3.7.1
seaborn == 0.12.2
jupyter notebook == 6.4.8
openai == 0.28.0
```

For plotting the curated figure notebooks, a modern Python environment with `pandas`, `numpy`, `matplotlib`, and `seaborn` is sufficient.

## Installation

```bash
git clone https://github.com/tsinghua-fib-lab/LLM_for_Polarization.git
cd LLM_for_Polarization
pip install -r requirements.txt
```

To run simulations, configure your OpenAI API key and model settings in `utils.py`.

## Running the Demo Simulation

`run.py` provides an example configuration for the Partisan Alignment setting. By default, it uses:

```python
datasource = "source_data/Data_WS_2000"
topic = "Politics"
num_epoch = 2000
```

Run:

```bash
python run.py
```

For a network with around 4,000 relationships and 1,000 agents, a full simulation may take several hours depending on model latency and API tier.

## Drawing Main-Text Figures

Run a figure notebook from its folder. For example:

```bash
cd figures/figure1
jupyter notebook figure1_codes.ipynb
```

The same pattern applies to `figure2`, `figure3`, and `figure4`.

## License

This project is licensed under the MIT License. See `LICENSE` for details.
