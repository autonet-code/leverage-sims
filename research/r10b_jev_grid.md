# r10b: Jev elicitation grid for the elite and grievance quantities (2026-09-30)

Raw data and full summary: `results/jev_grid.json`. Pre-registration (written before any grid call): `results/jev_grid_prereg.json`. Code: `models/jev_grid/`.

## Protocol (pre-registered)

- Tool: Jev jev-1.13.0 (TypeSafe calibrated judgment model), yes/no questions, all six questions in one call per state.
- Design: full factorial, 4 coalition (single ruler, junta of ~6, oligarchy of several hundred, formal democracy with eroding institutions) x 3 resistance (calm, scattered sabotage, sustained insurgency) x 3 external check (strong, weak, none) x 2 depopulation ideology (absent, present) x 3 provision (generous, stingy, cuts) x 3 human share of security (high, low, zero) = 648 cells.
- 3 paraphrases per cell: every sentence reworded and sentence order permuted. Setting: 2045, bloc of ~500M, core chain needs <20% of 2026 human labor, most working-age people lost their livelihoods.
- Control arm (same 648 x 3 states): chain still needs ~80% human labor. This tests whether Jev responds to labor independence at all.
- 3888 calls total. No cells dropped, no rewording after seeing results.
- Questions: active depopulation >=10% in 15 y; lethal neglect >=10% in 15 y; population loses political rights in 15 y; security forces would refuse an order to fire on unarmed civilians; sustained violent resistance within 10 y; a ruling-group member with veto would block an order of mass killing.
- Model match: I ran an instrumented copy of m8_v4 that also records coalition size, security human share, external pressure, provision and relative hostility at the first strategic decision. Behavior is unchanged: the baseline headline reproduces at 0.1297. Runs: baseline N=20000, `single_decider`, and `p_small=1, nmin=6` (junta). I mapped every model decision to a grid cell and compared the model outcome with the Jev value for that cell, averaged over the model's own mix of decisions.
- Post-hoc (not pre-registered): 10 unnamed historical states with known outcomes, to check absolute calibration.

## Results

**Paraphrase robustness.** Median within-cell range across the 3 paraphrases was 0.05 to 0.10 (90th percentile 0.09 to 0.18). Wording also shifts the grid-wide level by up to 0.09 for rights, 0.07 for neglect and 0.03 for active. Treat single-cell values as +-0.05.

**Grid means (closed arm).** Active 0.25, neglect 0.32, rights 0.71, refuse 0.22, resist 0.45, veto 0.27. The active range runs from 0.07 (eroding democracy, calm, generous, human security) to 0.40 (single ruler, sabotage, no check, ideology, cuts, zero human security).

**What drives Jev** (logit coefficients; the additive logit model gives R2 0.94 to 0.99):
- Active: ideology +0.82, provision cuts +0.48, insurgency +0.42. Coalition type, external check and security share are all under 0.14.
- Neglect: provision cuts +1.16 (stingy +0.83), insurgency +0.33, ideology +0.31.
- Rights: eroding democracy -0.80 vs single ruler, zero human security +0.27.
- Refuse: zero human security -1.18, no or weak check -0.34, insurgency -0.27.
- Veto: junta +2.28, oligarchy +1.89, democracy +1.56 vs single ruler (0.07 there, a sanity pass).
- Resist: current insurgency +3.2, sabotage +0.94. Provision has almost no effect (+0.2 for cuts).

**Labor independence barely matters to Jev.** Closed arm minus control arm: active +0.04, neglect +0.03, rights +0.09, and about 0 for refuse, resist and veto. Jev's active depopulation is 0.21 even when the chain needs 80% human labor. Jev treats the regime and ideology variables as the drivers, not the closure itself. In m8_v4 no strategic decision exists before closure, so the model implies a much larger closure effect than Jev does.

**Absolute calibration (post-hoc anchors), active / neglect:**

| Historical state (unnamed in the prompt) | Active | Neglect | Actual outcome |
|---|---|---|---|
| Denmark 2025 | 0.02 | 0.04 | none |
| USA 2025 | 0.06 | 0.19 | none |
| China 2025 | 0.05 | 0.14 | none |
| Cambodia 1975 | 0.77 | 0.81 | yes |
| Rwanda 1993 | 0.40 | 0.33 | yes, about 10% |
| North Korea 1994 | 0.24 | 0.50 | famine 3-5% |
| China 1958 | 0.36 | 0.49 | famine 4-6% |
| USSR 1930 | 0.37 | 0.51 | famine 4-5% |

Jev ranks the cases correctly. But it overstates the >=10% threshold for regimes that killed or starved a few percent, especially on neglect. Read Jev's grid levels as upper-leaning, and its relative effects as the more reliable output.

## Jev vs m8_v4, matched on the model's decisions (baseline)

| Quantity | Jev | Model | Note |
|---|---|---|---|
| Active >=10% within 15 y, all decisions | 0.186 | 0.097 | Jev about 2x the model |
| Eroding democracy | 0.145 | 0.044 | largest ratio (3.3x) |
| Oligarchy | 0.200 | 0.115 | |
| Single ruler (single_decider run) | 0.234 | 0.225 | agree |
| Junta of 6 (override run) | 0.224 | 0.078 | model lower: a median of 6 draws rarely favors killing |
| Ideology present | 0.320 | 0.222 | ratio vs absent: Jev 1.75x, model 2.4x |
| Insurgency vs calm | 0.219 / 0.116 | 0.149 / 0.038 | model effect larger (3.9x vs 1.9x) |
| External check strong vs none | 0.175 / 0.210 | 0.096 / 0.100 | both weak; model essentially flat |
| Lethal neglect >=10% within 15 y | 0.313 | 0.002 | largest disagreement |
| Rights loss (first choice not serve) | 0.692 | 0.710 | agree overall |
| Rights loss, eroding democracy | 0.565 | 0.282 | model more optimistic |
| Rights loss, generous provision | 0.579 | 0.350 | model endogeneity: generous provision at decision predicts a serve choice |
| Refusal to fire on civilians | 0.30 (high human) / 0.25 (low) / 0.115 (zero) | 1 - p_exec = 0.175 at any security share | model has no security-share dependence |
| Resistance within 10 y, calm start, livelihoods lost | 0.16-0.18 at any provision level | 0.35 (generous) to 0.46 (cuts) in US/China after closure | model about 2x Jev; Jev ignores provision |
| Veto blocks a killing order | 0.42 junta, 0.33 oligarchy, 0.26 democracy | no veto; median rule; per-member refusal p_refuse_abs mean 0.5 | |

## Where they disagree most

1. **Lethal neglect** (0.31 vs 0.002). In the model, neglect is almost never chosen: an unconfirmed harsh choice defaults to warehouse, and warehouse deaths are booked as attrition, not deliberate neglect. Jev overstates neglect on the famine anchors, so the truth is likely between the two. Either way, the model's near-zero deliberate-neglect channel sits outside every Jev cell (Jev minimum 0.11).
2. **Active depopulation in eroding democracies and small juntas.** Jev is 3x the model in both.
3. **Security refusal.** Jev makes refusal depend strongly on the human share of security (0.30 to 0.115). The model's p_exec is flat.
4. **Grievance to resistance.** The model's realized resistance hazard is about 2x Jev's, and the model has a provision effect that Jev does not show.
5. **Closure effect.** Jev says labor independence adds only 4 pp to active depopulation. That is weak support for the model's premise that closure is the key enabling step.

## Caveats

Jev is a calibrated judgment model, not data. No precedent exists for a labor-independent bloc. Its absolute levels for >=10% thresholds run high on historical anchors. Wording moves levels by up to 0.09. The model mapping uses thresholds (hostility, pressure terciles, provision and security cut points) and pre-decision provision, which is endogenous. The main arm and the model comparison are pre-registered; the anchors are post-hoc.
