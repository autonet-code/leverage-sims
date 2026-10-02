# leverage-sims

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23111345.svg)](https://doi.org/10.5281/zenodo.23111345)

Code, data and results for the paper *Losing Leverage: A Game-Theoretic Simulation of Power After Full Automation* (Andrei Taranu, writing as Eight Rice, 2026).

The paper models what happens to a population's standing, and to its survival, once AI and robots make it economically and militarily unnecessary to the people who rule it. It combines three things:
- historical base rates;
- a game-theoretic Monte Carlo simulation of six world blocs from 2026 to 2075;
- a pre-specified cross-check against a calibrated judgment model.

All results are conditional on the assumptions stated in the paper.

## Layout

- `paper/`: the paper (`paper.md`), the full parameter list, the brake-search protocol and its results (with the Jev elicitation scripts in `paper/jev_brakes/`), and the citation checks.
- `models/`: simulation code.
  - `m8_v4.py`: the six-bloc model (GPU via PyTorch, CPU fallback).
  - `integrate_v4.py`: the integrated scenario tree, the main results and the structural variants.
  - `m9_lever.py`: the decentralized-network test grid.
  - `run_brakes.py` and `run_greenfield.py`: the brake variants and the matched comparison of the structural changes.
  - `check_brakes_identity.py` and `check_greenfield_identity.py`: check that the model is bit-identical when the new parts are switched off.
  - `run_v6_final.sh`: runs the full final configuration.
  - `m1` to `m7`: the upstream stage models whose outputs feed the scenario tree.
  - `jev_grid/`: the judgment-model elicitation.
- `results/`: output files.
  - Final model (brakes, dedicated core loop, compute feedback, wider physical floors): `integrated_v6_final.json`, `m8_v6_final.json`, `lever_grid_v6_final.json`, `greenfield_v6_matched.json`.
  - Earlier configurations kept for comparison: brakes only (`integrated_v5_brakes.json`, `brakes_v5_variants.json`, `lever_grid_brakes.json`, `m8_v5_brakes.json`) and no brakes (`integrated_v4.json`, `m8_v4.json`, `lever_grid.json`).
- `research/`: evidence notes behind the parameter priors.
- `figures/`: figures used in the paper.

## Reproducing

Requirements: Python 3.11 or later, numpy, scipy, matplotlib, and PyTorch (CUDA optional).

```
cd models
# final model (M8_FINAL=1): all runs in sequence
bash run_v6_final.sh
# brakes only
M8_BRAKES=final INT_OUT=integrated_v5_brakes.json python integrate_v4.py
M8_BRAKES=final LV_TAG=_brakes python m9_lever.py
# everything off (reproduces the earliest comparison results exactly)
python m8_v4.py
python integrate_v4.py
python m9_lever.py
```

The seed is fixed at 20260930. On a consumer GPU:
- the integrated run takes about 25 minutes;
- the network grid takes about 2 hours.

GPU and CPU runs agree within simulation error but not draw for draw, because their random streams differ.

## License

MIT. See `LICENSE`.

## Citation

Taranu, A. (Eight Rice) (2026). *Losing Leverage: A Game-Theoretic Simulation of Power After Full Automation* Zenodo. https://doi.org/10.5281/zenodo.23111345
