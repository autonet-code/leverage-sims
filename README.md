# leverage-sims

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23111345.svg)](https://doi.org/10.5281/zenodo.23111345)

Code, data and results for the paper *Losing Leverage: A Game-Theoretic Simulation of Power After Full Automation* (Andrei Taranu, writing as Eight Rice, 2026).

The paper models what happens to a population's standing, and to its survival, once AI and robots make it economically and militarily unnecessary to the people who rule it. It combines three things:
- historical base rates;
- a game-theoretic Monte Carlo simulation of seventeen world actors from 2026 to 2075, with alliances between them;
- a pre-specified cross-check against a calibrated judgment model.

All results are conditional on the assumptions stated in the paper.

## Main findings

Under the paper's assumptions, in the order events unfold (version 7):
1. **Democracy erodes before work disappears.** In the US, democracy breaks down in 83% of runs by 2050, and in a fifth of all runs already by 2030.
2. **People stop being needed in the early-to-mid 2030s.** The leading actor's core supply chain runs on less than 20% of its 2026 human labor by a median year of 2034.
3. **Rights go within a few years.** The US or China public loses its rights in about 80% of runs, 68% of runs by 2040. Counting plain autocracy, it is disempowered in 94% by 2075.
4. **The outcome then rests on a few people.** What decides whether rulers escalate to mass killing is their own restraint, incentives and internal politics, and above all how much they fear what a surviving population could later become.
5. **Killing follows by escalation, mostly from the 2040s.** A deliberate loss of 10% or more of the US or China population reaches 50% of runs by 2075, and a loss of 99.9% or more reaches 42%.
6. **An income network outside state and corporate control changes the incentives.** At 50% of US economic activity by the early 2030s, it halves the near-total risk to 2050 and cuts it by more than a quarter by 2075.

These numbers show where the assumptions lead, not a forecast. Section 5.6 of the paper explains how much of the spread around them is chance and how much depends on inputs no one has measured.

The first publication (version 1.0, six blocs) is preserved in the repository history and on Zenodo.

A companion video essay tells the same scenario as a story, for a general audience. It narrates the scenario rather than reporting the results: [Automation and the RIGGED endgame](https://youtu.be/dPjT1uZc-pU).

## Layout

- `paper/`: the paper (`paper.md`), the full parameter list, the brake-search protocol and its results (with the Jev elicitation scripts in `paper/jev_brakes/`), and the citation checks.
- `models/`: simulation code.
  - `m8_v7.py`, `v7_actors.py`: the seventeen-actor model (version 7).
  - `integrate_v7.py`, `m9_lever_v7.py`: the integrated scenario tree and the network test for version 7.
  - `v7_variance.py`, `v7_extras.py`: the variance breakdown, the rights-loss timeline and the ideology sensitivity.
  - `run_v7_full.sh`: runs version 7 in full.
  - `m10_structure_diagram_v7.py`: the model structure figure.
  - `m8_v4.py`: the six-bloc model of the first publication (GPU via PyTorch, CPU fallback).
  - `integrate_v4.py`: the integrated scenario tree, the main results and the structural variants.
  - `m9_lever.py`: the decentralized-network test grid.
  - `run_brakes.py` and `run_greenfield.py`: the brake variants and the matched comparison of the structural changes.
  - `check_brakes_identity.py` and `check_greenfield_identity.py`: check that the model is bit-identical when the new parts are switched off.
  - `run_v6_final.sh`: runs the full final configuration.
  - `m1` to `m7`: the upstream stage models whose outputs feed the scenario tree.
  - `jev_grid/`: the judgment-model elicitation.
- `results/`: output files.
  - Version 7: `integrated_v7.json`, `m8_v7.json`, `lever_v7_grid_v7.json`, `v7_variance.json`, `v7_rights_timeline.json`, `v7_ideology_sensitivity.json`, `jev_ideology.json`.
  - First publication (six blocs; brakes, dedicated core loop, compute feedback, wider physical floors): `integrated_v6_final.json`, `m8_v6_final.json`, `lever_grid_v6_final.json`, `greenfield_v6_matched.json`.
  - Earlier configurations kept for comparison: brakes only (`integrated_v5_brakes.json`, `brakes_v5_variants.json`, `lever_grid_brakes.json`, `m8_v5_brakes.json`) and no brakes (`integrated_v4.json`, `m8_v4.json`, `lever_grid.json`).
- `research/`: evidence notes behind the parameter priors.
- `figures/`: figures used in the paper.

## Reproducing

Requirements: Python 3.11 or later, numpy, scipy, matplotlib, and PyTorch (CUDA optional).

```
cd models
# version 7 (M8_FINAL=1): all runs in sequence
sh run_v7_full.sh
# first publication, six blocs (M8_FINAL=1): all runs in sequence
bash run_v6_final.sh
# brakes only
M8_BRAKES=final INT_OUT=integrated_v5_brakes.json python integrate_v4.py
M8_BRAKES=final LV_TAG=_brakes python m9_lever.py
# everything off (reproduces the earliest comparison results exactly)
python m8_v4.py
python integrate_v4.py
python m9_lever.py
```

The seed is fixed at 20260930. On a consumer GPU, version 7 takes about 15 hours in all:
- the actor simulation and its variants take about 4.5 hours;
- the integrated run takes about 1 hour;
- the network grid takes about 9 hours.

GPU and CPU runs agree within simulation error but not draw for draw, because their random streams differ.

## License

MIT. See `LICENSE`.

## Citation

Taranu, A. (Eight Rice) (2026). *Losing Leverage: A Game-Theoretic Simulation of Power After Full Automation*. Zenodo. https://doi.org/10.5281/zenodo.23111345
