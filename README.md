# leverage-sims

Code, data and results for the paper *Losing Leverage: A Game-Theoretic Simulation of Power After Full Automation* (Eight Rice, 2026).

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
  - `run_brakes.py`: the brake variants.
  - `check_brakes_identity.py`: checks that the model is bit-identical when the brakes are off.
  - `m1` to `m7`: the upstream stage models whose outputs feed the scenario tree.
  - `jev_grid/`: the judgment-model elicitation.
- `results/`: output files.
  - Final model, brakes on: `integrated_v5_brakes.json`, `brakes_v5_variants.json`, `lever_grid_brakes.json`, `m8_v5_brakes.json`.
  - The same model without brakes, kept for comparison: `integrated_v4.json`, `m8_v4.json`, `lever_grid.json`.
- `research/`: evidence notes behind the parameter priors.
- `figures/`: figures used in the paper.

## Reproducing

Requirements: Python 3.11 or later, numpy, scipy, matplotlib, and PyTorch (CUDA optional).

```
cd models
# final model (evidence-based brakes on)
M8_BRAKES=final python m8_v4.py        # writes results/m8_v4.json; the published copy is m8_v5_brakes.json
M8_BRAKES=final INT_OUT=integrated_v5_brakes.json python integrate_v4.py
M8_BRAKES=final LV_TAG=_brakes python m9_lever.py
# brakes off (reproduces the comparison results exactly)
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
