# Source Data

This folder contains the network initialization files and source data for the three main topics.

## Network Initialization

`Data_WS_2000/` contains the original network initialization files used by the simulation code:

- `edges.csv`: network edge list.
- `data_ID2Net_ID.csv`: mapping between data ids and network ids.
- `user_message_generate.json`: initial generated user messages.

## Topic Interaction Data

The three topic folders are:

- `Partisan Alignment/`
- `Gun Control/`
- `Abortion Ban/`

Each topic folder contains `epoch_run0.pkl` through `epoch_run40.pkl`.

## File Format

Each `epoch_run*.pkl` file is a pandas DataFrame. Each row is one directed interaction or edge from a source node to a target node at that epoch.

Columns:

- `source node Id`: id of the source node.
- `target node Id`: id of the target node.
- `source node state`: opinion state of the source node at that epoch.
- `target node state`: opinion state of the target node at that epoch.

Opinion states are coded as integers from `-2` to `2`.

## Metadata

`metadata.csv` summarizes each file with row counts, unique source/target node counts, unique edge counts, and observed state values.

Only the standard epoch files `epoch_run0.pkl` to `epoch_run40.pkl` are included. Temporary duplicate files such as `epoch_run40.pkl--` or `epoch_run40--.pkl` are excluded.
