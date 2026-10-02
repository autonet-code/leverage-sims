"""
M8 v4 (review round 2, GPU): industrial closure, the elite calculus, an endogenous grievance loop and
endogenous democracy, from the observed 2026 state.

Built from a copy of m8_industrial_closure.py (v3, untouched). The five structural errors the scenario
author raised are fixed (1 observed 2026 start and plain milestones, 2 physical build-out from current
trends with evidence-bounded AI/robot acceleration, 3 endogenous grievance -> revolt -> repression loop
with unstable, lethal warehousing, 4 democracy endogenous to leverage with no structural bar on harsh
options, 5 time-varying trend priors). Review round 2 (reality check, skeptic, pessimist) changes:

 Actors: the rest of the world is no longer one unitary actor. Six blocs: US_bloc (US, JP, KR, TW),
   China_bloc, Europe_plus (EU, UK, CA, AU, NZ, CH, NO), Russia_MENA, South_Asia, Global_South (Africa,
   Latin America, Southeast Asia). RoW results are reported as population shares.
 Cognitive: software milestones are CAPABILITY ("AI can do X% of software tasks end to end at a quality
   that could be merged with no human review"), with a separate PRACTICE share (what is actually merged
   without review) that adopts at the observed speed and never exceeds capability. The horizon is capped
   at 1e5 h (about a 50-year career).
 Physical capability: anchored to a measurable 2026 quantity, dx = share of O*NET physical work tasks a
   general-purpose robot can do in production at >=50% of human speed (about 4% in 2026: picking,
   palletizing, machine tending, tote handling; most manipulation is 3-10x slower, Epoch 2026).
   DEX = dx reaches 50% (at human speed and cost parity).
 Build-out: proportional growth rates are no longer applied to the automated share of existing capacity
   without limit. The share can grow only as fast as new automated capacity plus retrofit/scrapping of old
   capacity allows: dx/dt <= (new-capacity rate + retrofit rate) x (feasible - x). The whole economy is
   capped by the investment flow (gross investment / capital 0.08-0.15/yr), not by 11%/yr of itself.
 Grievance loop: onset is calibrated at two points, the 2026 zero-displacement base rate (US/China/Europe
   ~0.3%/yr of a new sustained insurgency, the high end of UCDP onset rates for high-capacity states)
   and the 30%-displacement reference. Grievance (Gv) now drives hostility, attitudes enter with an
   elasticity < 1, hostility saturates smoothly (the 3% hard cap that inverted the loop is removed),
   automated surveillance deters onset, regime type enters as an inverted U (Hegre et al. 2001),
   collective punishment scales with the region in revolt, insurgent success only sometimes democratizes
   (Chenoweth-Stephan), and the repression-deterrence and backfire terms are priors.
 War kills: a war-year mortality prior plus a nuclear-use tail for nuclear-armed blocs (own S5 channel).
 Elite game: a fifth option, "rentier" (generous provision, no political rights: the Gulf path); decision
   inertia (bigger switching cost, a harsh choice must be confirmed in two consecutive yearly decisions);
   execution can fail (partial loss, desperate resistance); execution-phase threat and international
   response; coalition floor 21 except an explicit small-coalition prior; ideology calibrated to r9d and
   allowed to fade; zero mass on scarcity-rent and eco-land terms.
 Reporting: S5_deliberate (active decision, collective punishment, neglect) is the headline; attrition
   (despair + crackdown deaths) and war deaths are reported separately and in S5_total.

Review round 3 (wired in the loop; each has a revert switch, variants rev_*):
 F1 regime-dependent decision rule (democracy: median; oligarchy: harsher moves need weighted share q_ol;
   personalist: leader at a tilted quantile of the coalition, inner-circle veto that works only while security
   and admin need humans); A6 faction weight = control over automated kinetic force; A6 public leverage = labor
   plus credible revolt only. F2 refusal shares by layer/regime with purge convergence, separate (smaller)
   refusal of lethal neglect. F3/A4 defection as a threshold on the HUMAN share of coercion (gone once
   autonomous systems carry orders). F5 METR sign fix. F7 saturation priors instead of hard caps. F8/A5 status
   quo (today's cutting provision trajectory, displaced get a fraction) is the default; warehousing must be
   chosen. A1 trend capability (compute slowdown only in 'trend_breaks'). A2 US/China priority max from 2026.
   A3 security automation at full priority with first call on capacity. A7 El Nino stress, moral-cost decline,
   international-pressure decay. Endgame (A8/A9/A11): an executed designation is simulated as deaths (hazard
   ramp over T_full; abstract means availability driven by capability; escalation partial -> near-total driven by
   the rulers' perceived revenge threat; tacit collusion between depopulating coalitions if the payoff beats the
   rulers' own expected survival cost, incl. a nuclear exchange). The remnant (rem) is CAPTIVE, without rights.
   The round-2 booking of S5 at decision time + lagX without simulated deaths is removed. Loss ladder
   10/50/90/99.9%, deliberate vs total. Strategy codes (legacy order) now 0 serve, 1 warehouse, 2 neglect,
   3 depopulate, 4 rentier, 5 status_quo; ch_S5 adds 6 collusive war.

ROUND 3 (B1-B9, agreed with the scenario; A1-A11 still bind; research/r12a_round3_evidence.md). Each change has a
revert switch (variants rev_B*); 'round2_exact' turns all of them off and reproduces the round-2 model bit for bit (new
randomness comes from a separate torch generator and new parameters are drawn after all round-2 draws).
 B1 moral cost of the person at the top of an autocratic coalition x sel_top (members x sel_top^0.5), leader's refusal
   x sel_top, ideology removes a share id_mor of the moral cost; automation distance stays mc_ai.
 B2 coalitions are actual member sets. Purges from incentives (leader's control share S_L, loss of need for human staff,
   paranoia after atrocities, no comparable rival), counter-coups, control of purged members passes to the leader.
   Personalist = S_L >= 0.5. Faction weight = control of coercive force (human networks -> automated force, A6).
 B3 outside cost (legitimacy/sanctions) scaled by the outsiders' ability to enforce it: min(1, 2 M_c/(M_c+M_b)).
 B4 threat from survivors and A11 escalation x (1 + k_ret x deliberate deaths already caused / 10%).
 B5 cross-bloc depopulation by executing closed actors (pooled with colluders) against blocs they can overpower,
   weighing nuclear retaliation; kinetic power M = military share x output x (1 + k_am x automated security share).
 B6 F6 wiring: kit shares the robot-input budget; M0/C0 are world pools allocated by purchasing power with export
   restriction; security is served first FROM supply; reshoring limited by industrial base; unsecured imports count as
   dependence; bloc-specific capability lags. B8 is in integrate_v4.py. B9: Alt B unchanged (integrator).

GPU: the simulation runs in PyTorch (CUDA if available; --cpu forces the CPU). Draws are processed in
chunks; tornado rows are batched with common random numbers. Parameter draws use numpy with SEED, and the
in-simulation random stream uses a torch generator seeded from sim_seed.

Interface: sample_params(N, rng, overrides, variant) and simulate(p, N, variant) return the v3 keys
integrate scripts use (t_core, t_full, lead_core, t_S5, ch_S5 [2 neglect, 3 active, 4 attrition, 5 war],
t_grab, first_choice, free_at_dec, t_first_dec, choice_end, free_end, t_ac [= M3 capability], t_dex).
Strategy codes (legacy order): 0 serve, 1 warehouse, 2 neglect, 3 depopulate, 4 rentier.
Actor index: 0 US_bloc, 1 China_bloc, 2-5 RoW sub-blocs.

Outputs: results/m8_v4.json, figures/m8v4_*.png
"""
import json
import os
import sys
import time

import numpy as np
from scipy.special import ndtr, ndtri, logit as sp_logit

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEED = 20260930
T0, T_END, DT = 2026.75, 2075.0, 0.25
NSTEP = int(round((T_END - T0) / DT))
YEARS = np.arange(2027, 2076)
LN2 = float(np.log(2.0))

ACTORS = ["US_bloc", "China_bloc", "Europe_plus", "Russia_MENA", "South_Asia", "Global_South"]
ROW = [2, 3, 4, 5]
A_N = len(ACTORS)
POP = np.array([0.53, 1.42, 0.62, 0.99, 1.97, 2.67])     # billions, 2026 (UN WPP 2024 medium, grouped)
SEG = ["mining", "energy", "chips", "manufacturing", "logistics", "construction",
       "maintenance", "security", "admin"]
W_S = np.array([0.06, 0.07, 0.07, 0.25, 0.13, 0.17, 0.10, 0.07, 0.08])
CS = np.array([0.20, 0.35, 0.45, 0.30, 0.25, 0.15, 0.15, 0.30, 0.90])
FP0 = np.array([0.15, 0.25, 0.35, 0.25, 0.20, 0.05, 0.05, 0.15, 0.20])
NP_MULT = np.array([1.1, 1.0, 1.0, 1.0, 0.9, 1.4, 1.4, 1.0, 1.0])
RR_SEG = [0, 1, 2, 3, 4, 5]
SA_SEG = [7, 8]

# ---- MEASURED 2026 automated share of physical task value per segment (r9a), by bloc.
# manufacturing: robot density maps to share. China ~470/10k (passed Germany/Japan) plus 1-4% lights-out
# value added -> 0.08. US bloc employment-weighted density: US 300 x 13M + JP 420 x 10M + KR 1012 x 4.4M
# + TW ~400 x 3M over 30M workers = ~450/10k -> 0.07 (below China). EU ~220/10k -> 0.05. Others < 100/10k.
# mining: autonomous haul 6-10% of large trucks (Pilbara, China, Chile). chips: fab automated material
# handling (humans do maintenance). logistics: ports 5-10% automated capacity, robotaxi 1-2% of ride-hail,
# warehouses. construction < 1%. security: drones mostly piloted, a few % autonomous terminal guidance
# (higher for Russia at war).
X0 = np.array([
    [0.08, 0.05, 0.35, 0.07, 0.05, 0.005, 0.010, 0.03, 0.05],
    [0.08, 0.05, 0.30, 0.08, 0.04, 0.006, 0.010, 0.03, 0.05],
    [0.06, 0.05, 0.30, 0.05, 0.05, 0.004, 0.008, 0.02, 0.05],
    [0.06, 0.04, 0.20, 0.02, 0.02, 0.002, 0.004, 0.04, 0.03],
    [0.03, 0.03, 0.20, 0.015, 0.02, 0.002, 0.003, 0.01, 0.03],
    [0.07, 0.04, 0.25, 0.02, 0.02, 0.002, 0.004, 0.01, 0.02]])
X0_EVID = ["low-medium", "low", "low", "medium", "medium", "low", "very low", "low", "very low"]
# ---- current growth of the automated share (log-rate /yr): mining autonomy +20-30%/yr (China fastest);
# industrial robot stock +9-11% world, China installs +20%, India rising; logistics blend; construction/
# maintenance unmeasured (low); security: drone autonomy under jamming spreading fast
G0 = np.array([
    [0.25, 0.08, 0.05, 0.08, 0.20, 0.08, 0.05, 0.30, 0.05],
    [0.30, 0.12, 0.08, 0.15, 0.25, 0.10, 0.06, 0.30, 0.05],
    [0.15, 0.07, 0.05, 0.06, 0.15, 0.06, 0.04, 0.20, 0.05],
    [0.15, 0.05, 0.04, 0.05, 0.10, 0.04, 0.03, 0.30, 0.04],
    [0.20, 0.08, 0.05, 0.10, 0.12, 0.05, 0.04, 0.15, 0.05],
    [0.20, 0.06, 0.04, 0.07, 0.10, 0.04, 0.03, 0.15, 0.04]])
G_IND = np.array([0.08, 0.15, 0.05, 0.04, 0.10, 0.06])     # automation-kit growth now (IFR WR2026)
# domestic share of each segment's inputs (the rest is imported with the exporters' human content)
OWN0 = np.array([
    [0.35, 0.90, 0.80, 0.60, 0.95, 1.0, 1.0, 1.0, 1.0],
    [0.60, 0.80, 0.40, 0.95, 0.95, 1.0, 1.0, 1.0, 1.0],
    [0.25, 0.60, 0.30, 0.75, 0.95, 1.0, 1.0, 1.0, 1.0],
    [0.70, 0.95, 0.05, 0.40, 0.95, 1.0, 1.0, 1.0, 1.0],
    [0.40, 0.70, 0.05, 0.50, 0.95, 1.0, 1.0, 1.0, 1.0],
    [0.60, 0.70, 0.10, 0.40, 0.95, 1.0, 1.0, 1.0, 1.0]])
K_RESH = np.array([1 / 8, 1 / 5, 1 / 4, 1 / 4, 1 / 3, 0, 0, 0, 0])
# WORKFORCE: million workers in the 9 core-chain segments (ILOSTAT ISIC B-F mining, utilities,
# manufacturing, construction; H transport/storage; plus repair/maintenance, security and core admin),
# roughly 22-40% of each bloc's labor force (US bloc labor force ~280M, China ~780M, EU+ ~285M,
# Russia_MENA ~320M, South Asia ~750M, Global South ~1.2B incl. agriculture). Uncertainty: wf_mult (sd 25%).
WORKFORCE = np.array([75.0, 300.0, 77.0, 85.0, 200.0, 263.0])
WORLD_W = np.array([0.30, 0.35, 0.15, 0.07, 0.05, 0.08])   # share of world industrial output (import mix)
ROBOT_SHARE0 = np.array([0.10, 0.83, 0.04, 0.01, 0.01, 0.01])   # humanoid shipments 97% Chinese 1H2026
RE_SHARE0 = np.array([0.08, 0.90, 0.01, 0.01, 0.01, 0.02])
CHIP_SHARE0 = np.array([0.70, 0.35, 0.03, 0.005, 0.005, 0.01])
MFG_SHARE = np.array([0.35, 0.45, 0.10, 0.03, 0.03, 0.04])
E_GW0 = np.array([1800.0, 3900.0, 1300.0, 700.0, 600.0, 1400.0])
KW_ROBOT = 1.0
E_FRAC = 0.10
# ROUND 3 (B3/B5/B6). MIL0: bloc shares of world military expenditure 2025 (SIPRI via Wikipedia, fetched 30 Sep 2026:
# US 954, Japan 62, Korea 48, Taiwan 18 -> US bloc ~1082; China 336; Germany 114, UK 89, France 68, Italy 48, Poland 47,
# Spain 40, Canada 38, Australia 35, Netherlands 29, Norway 17, Sweden 17 + rest of EU/CH/NZ ~90 -> ~630; Russia 190,
# Saudi 83, Israel 48, Turkey 30, Algeria 25, Iran 7 + Gulf/Egypt/Iraq ~85 -> ~470; India 92, Pakistan 12 + ~6 -> ~110;
# Brazil 24, Singapore 17, Indonesia 15, Colombia 15, Mexico 14 + SE Asia/Africa/LatAm ~65 -> ~150; sum ~2780 bn USD).
# China's share is scaled by cn_ppp (PPP-adjusted estimates of Chinese defence spending are higher than market-rate).
MIL0 = np.array([0.39, 0.12, 0.23, 0.17, 0.04, 0.05])
# IB: industrial base that limits how fast a bloc can reshore chips/magnets/robot supply (sqrt of the share of world
# manufacturing output MFG_SHARE relative to the US bloc; IFR 2024 installations China 54% of 542k, Japan 44.5k, US 34.2k,
# Korea 30.6k, Germany 27k; Epoch May 2025: US ~3/4 of GPU-cluster performance, China 15%; humanoids 97% Chinese 1H2026)
IB = np.array([1.0, 1.0, 0.53, 0.29, 0.29, 0.34])
# B6: years each bloc's DEPLOYABLE capability lags the frontier, U(lo, hi) per draw. Cognitive: frontier labs and ~3/4
# of GPU-cluster performance in the US bloc (Epoch, May 2025), China 15% with open-weight models some months behind [M],
# Europe buys US models, others limited by compute access and export controls. Physical: China makes 97% of humanoids
# (1H2026) and 54% of industrial-robot installs (IFR 2024), so the US bloc lags China on robots. Judgment ranges.
LAGC_LO = np.array([0.0, 0.0, 0.0, 0.5, 0.25, 0.5]); LAGC_HI = np.array([0.0, 1.0, 1.0, 3.0, 2.0, 3.0])
LAGP_LO = np.array([0.0, 0.0, 0.5, 1.0, 1.0, 1.0]); LAGP_HI = np.array([1.0, 0.0, 2.0, 4.0, 4.0, 4.0])
GLOBAL_PROD0 = 0.10
GLOBAL_STOCK0 = 0.15
# strategies, internal order of harshness (the coalition median is taken on this order)
# Review round 3 (F8/A5): a sixth option, STATUS QUO (today's provision trajectory, no decision), sits between
# rentier and warehouse. It is the default before any confirmed decision; warehousing must be chosen.
STRAT_INT = ["serve", "rentier", "status_quo", "warehouse", "neglect", "depopulate"]
STRAT = ["serve", "warehouse", "neglect", "depopulate", "rentier", "status_quo"]   # legacy output codes 0..5
INT2LEG = np.array([0, 4, 5, 1, 2, 3])
LEG2INT = np.array([0, 3, 4, 5, 1, 2])
I_SQ, I_WH, I_NEG, I_DEP = 2, 3, 4, 5
PROV_INT = np.array([1.0, 1.0, -1.0, 0.6, 0.1, 0.0])     # -1: status quo provision (time-varying, see P_sq)
METR_OBS = 4.3      # METR doubling (months) over the window in which z_rate was measured (F5: fixes s_task)
DEM, OLIG, PERS = 0, 1, 2
LOSS_THR = [0.10, 0.50, 0.90, 0.999]
NMEM = 51
NMIN_VALS = np.array([1, 3, 5, 7]); NMIN_P = np.array([0.3, 0.3, 0.2, 0.2])
# democracy (V-Dem LDI 2025/26, population-weighted within blocs)
D0 = np.array([0.57, 0.05, 0.70, 0.10, 0.28, 0.35])
DMAX = np.array([0.78, 0.20, 0.85, 0.40, 0.55, 0.60])
D_BREAK = 0.30
BASE_PROV = np.array([0.45, 0.30, 0.60, 0.25, 0.15, 0.20])
P_EP0 = np.array([1.0, 0.0, 0.40, 0.0, 0.0, 0.35])   # P(bloc starts inside an autocratization episode); Europe 0.25 -> 0.40 (A7, r11a: AfD 43.8% Saxony-Anhalt, 38.2% M-V, Sep 2026; V-Dem DR2026 autocratizers)
# status-quo provision drift per bloc (F8, r10a: OBBBA/CBO cuts; China 2025 childcare subsidy), U(lo, hi) per yr
D_A_LO = np.array([-0.020, -0.005, -0.010, -0.010, -0.010, -0.010])
D_A_HI = np.array([0.000, 0.015, 0.005, 0.010, 0.010, 0.010])
DM_LO = np.array([0.6, 0.5, 0.5, 0.5, 0.5, 0.5])        # provision multiplier for the displaced (US: UI 40-50%, TAA lapsed)
DM_HI = np.array([0.9, 0.9, 0.9, 0.9, 0.9, 0.9])
ENTRENCHED = np.array([False, True, False, True, False, False])   # consolidated autocracy (coalition can shrink)
HI_CAP = np.array([1.0, 1.0, 1.0, 0.5, 0.0, 0.0])     # weight of high-capacity state calibration (vs weak)
WROW_M = np.array([0.0, 0.0, 0.5, 1.0, 0.8, 0.6])     # major-war hazard multipliers for non-US/China blocs
NUC_ARMED = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 0.0])
LETH_M = np.array([1.0, 1.0, 1.3, 0.7, 1.6, 1.6])
GRAB_W = np.array([1.0, 0.0, 0.5, 0.0, 0.5, 0.5])
RED_W = np.array([1.0, 0.25, 1.0, 0.25, 1.0, 1.0])
PSI_ROW_M = np.array([1.5, 1.0, 0.8, 0.6])
SW_THR = {"M2": 0.5, "M3": 0.9}
RND_THR = {"M4": 0.5, "M5": 0.95}

MILESTONES = {
    "M1": "AI writes most new code at leading firms and humans review it (observed: Google 50% Oct 2025, 75% Apr 2026)",
    "M2": "CAPABILITY: AI agents can do half of all software engineering tasks end to end at a quality that could be merged with no human review",
    "M3": "CAPABILITY: AI can do 90% of software engineering tasks that way (replaces v3's undefined 'automated coder')",
    "M2p": "PRACTICE: half of all software engineering work is actually merged with no human review (2026: >10% at Uber, a few % economy-wide)",
    "M3p": "PRACTICE: 90% of software engineering work is actually merged with no human review",
    "M4": "AI does the work and humans only assign and check it on more than half of AI-research tasks at frontier labs (26% at Anthropic, Sep 2026)",
    "M5": "Same for 95% of AI-research tasks",
    "M6": "AI can reliably (80% success) finish a one-work-year (2000 h) real-world project on its own",
    "M7": "AI can reliably do half of all desk (cognitive) tasks across the economy",
    "DEX": "A general-purpose robot can do half of all O*NET physical work tasks at human speed and cost parity (2026: ~4% at >=50% of human speed)",
    "C05": "The leading bloc's core supply chain needs humans for less than half of its 2026 labor",
    "C02": "CLOSURE: the leading bloc's core supply chain needs humans for less than 20% of its 2026 labor",
    "F05": "The leading bloc's whole economy chain needs humans for less than half of its 2026 labor",
}
DEFS_PLAIN = {
    "democratic_breakdown": "liberal-democracy index (V-Dem LDI) below 0.30, i.e. Hungary-2024 or Turkey-2015 level or worse, or a narrow-group seizure of power",
    "sustained_insurgency": "a new sustained violent campaign (UCDP-level, >=25 battle deaths/yr for years) by the displaced population, beyond the 2026 baseline of conflict (ongoing Sahel, Sudan, Myanmar, Ukraine wars are the baseline, not counted)",
    "lethal_autonomy_authorized": "routine use of lethal targeting with no per-strike human approval (Ukraine/Russia terminal autonomy under jamming is partial; blocs at war reach it sooner)",
    "S5_deliberate": ">=10% of a bloc's 2026 population lost to deliberate channels: an executed depopulation decision, collective punishment, or deliberate lethal neglect",
    "S5_total": "S5_deliberate plus attrition (despair mortality of the displaced, crackdown deaths) and war deaths, >=10% cumulative excess loss",
    "records": "yearly records labeled YYYY are values at 1 January of that year (the run starts 1 Oct 2026)",
    "near_total_depopulation": "HEADLINE (A8): >=99.9% of a bloc's 2026 population lost (scenario: 8 billion to ~8 million). In the model this is reached only when an executed depopulation escalates to completion; the remaining 0.03-0.1% is a CAPTIVE remnant kept without rights (service, reproduction), unable to organize or speak, counted as disempowered, not as survivors with standing (A11)",
    "loss_ladder": "cumulative simulated excess loss >=10%, >=50%, >=90%, >=99.9% of the 2026 population; 'deliberate' = executed depopulation (automated force, engineered means, strangulation), collective punishment, deliberate lethal neglect, and collusive war between depopulating coalitions; 'total' adds attrition (despair, crackdown) and ordinary war",
}


def ln(med, sig):
    return ("lognormal", med, sig)


PRIORS = {
    # ------------------------------------------------ cognitive (r9a)
    "h50_0": (ln(16.0, 0.15), "METR 50% horizon, best model mid-2026: 12-20 h (METR May 2026)", "medium-high"),
    "h80_ratio": (ln(4.5, 0.3), "50%/80% horizon ratio: 16 h vs 3.5 h (METR May 2026)", "medium-high"),
    "metr_doubling_months": (ln(4.3, 0.28), "horizon doubling 2023+ window 4.3 mo; 2024-25 3-3.5 mo; long-run 7 mo (METR TH1.1). F5: sets only the SPEED of the trend; the task-difficulty spread uses the fixed observed doubling METR_OBS=4.3 mo, so faster doubling can never delay a milestone", "medium-high"),
    "compute_slowdown": (("uniform", 0.35, 1.0), "Epoch: 4-5x/yr compute growth hard to sustain past ~2030. A1: OFF in the baseline (capability follows the trend); used only in the 'trend_breaks' variant", "moderate"),
    "mess": (ln(3.0, 0.6), "benchmark-to-real-work horizon discount; affects only M6 (the share milestones are re-anchored to measured 2026 shares, so it cancels there)", "low-medium"),
    "z_rate": (("uniform", 0.5, 1.1), "speed of AI code-share growth in probit units/yr (Google 25%->50%->75% Oct24-Apr26). Used as the task-difficulty spread for CAPABILITY shares: the share of tasks AI can do well rises with the horizon at this slope", "medium"),
    "k_rnd": (("uniform", 1.0, 2.0), "AI-research tasks' difficulty spread relative to software tasks", "low"),
    "k_ec": (("uniform", 1.5, 3.0), "economy-wide desk tasks' difficulty spread relative to software", "low"),
    "sw_cap0": (ln(0.15, 0.5), "CAPABILITY 2026: share of software tasks AI can do end to end at mergeable quality with no review. Lower bound: Uber merges >10% with no human in the loop (practice <= capability); upper side limited by METR's finding that many test-passing agent PRs are not mergeable as-is", "low"),
    "sw_prac0": (ln(0.04, 0.5), "PRACTICE 2026, economy-wide: share of software work actually merged with no human review (Uber >10% is a leader; most firms review all AI code)", "low"),
    "g_swad": (("uniform", 0.4, 1.2), "practice adoption speed, log-odds per yr. AI-written, human-reviewed code rose ~1.5 log-odds/yr at Google; removing review is slower (liability, SOC2/ISO review norms, regulated sectors ~30% of software work). Practice never exceeds capability", "low-medium"),
    "rnd0": (("uniform", 0.15, 0.35), "share of frontier-lab R&D tasks where AI does the work and humans assign/check (Anthropic Sep 2026: 26% 'leads')", "medium (single self-report)"),
    "Fcog0": (("uniform", 0.10, 0.25), "reliably automatable desk-task share 2026 (AEI, GDPval 48%, API success 49%)", "moderate"),
    "p_cog_wall": (("const", 0.12), "no-AGI-this-century mass ~10-15%", "weak"),
    "p_capex_correction": (("const", 0.35), "capex ~7x lab revenue; Abilene expansion abandoned 2026", "moderate"),
    "fb_zero_mass": (("const", 0.10), "A1: P(no further shrinking of the doubling time from AI-accelerated AI research); round 2 used 0.25 (Davidson & Houlden 2025: r<1 plausible)", "moderate-weak"),
    "fb_strength": (ln(0.7, 0.6), "A1: elasticity of the horizon growth rate to AI-R&D automation, mult = ((1-rnd0)/(1-s_rnd))^fb. Anchor: the doubling time fell 7 -> ~4.3 mo while AI-led R&D rose from ~0 to ~0.26, which implies fb <= ln(1.63)/ln(1/0.74) = 1.6 if ALL of the speed-up came from AI R&D (upper bound; compute and RL scaling explain part). Clipped [0.05, 2]", "low-medium"),
    "a_cog0": (ln(0.03, 0.4), "share of desk-task value actually automated 2026 (genAI in 6.3% of work hours, about half automation)", "medium-low"),
    "g_cog0": (ln(0.25, 0.25), "current growth of automated desk-work share (genAI hours +28%/yr)", "medium-high"),
    "g_cog_max": (ln(0.7, 0.4), "adoption rate once AI reliably does most desk tasks", "low-medium"),
    # ------------------------------------------------ physical capability, anchored to a 2026 measure
    "dx0": (ln(0.04, 0.5), "2026: share of O*NET physical work tasks a general-purpose robot does in production at >=50% of human speed (picking >99% in production, palletizing, machine tending, tote handling; most manipulation 3-10x slower: Epoch 2026, r8a)", "low"),
    "rp0": (ln(0.35, 0.5), "current growth of logit(dx) per yr: 2023-26 production-ready task set went from picking-only to picking + machine tending + tote/parts handling pilots (~1.5-2% -> ~3-5%, logit +0.25-0.45/yr)", "low"),
    "kc": (ln(0.5, 0.8), "AI -> robotics coupling per horizon doubling beyond M3 (robot foundation models, sim-to-real)", "low"),
    "rp_max": (ln(1.5, 0.4), "cap on logit(dx) growth per yr (hardware generation cadence 1-2 y per actuator generation)", "low"),
    "p_phys_wall": (("const", 0.10), "hands/actuator wall before general dexterity", "low"),
    "s0": (("uniform", 0.1, 0.35), "2026 manipulation speed vs human (Epoch: 3-10x slower)", "moderate"),
    "shifts": (("uniform", 1.5, 3.0), "robot operating hours vs one worker FTE", "moderate"),
    "Fp_scale": (("uniform", 0.6, 1.4), "uncertainty on 2026 feasible shares per segment", "low"),
    # ------------------------------------------------ physical build-out (r9a, r9b)
    "g0_mult_sd": (("const", 0.35), "per-segment volatility of current growth rates (China 2025: textiles -92%, auto +38%)", "high (observed volatility)"),
    "g_ramp": (ln(0.5, 0.3), "sustained sector ramp a priority actor reaches with human labor: solar 49->315 GW/yr, NEV 1.4->13M, Indonesian nickel, CoWoS (r9b)", "good"),
    "i_K": (("uniform", 0.08, 0.15), "gross fixed investment / capital stock per yr: the flow of new capacity that can be automated from day one (OECD ~0.08-0.10, China peak ~0.15)", "good"),
    "i_boost": (("uniform", 1.3, 2.0), "investment boost under priority/profitability (China 2000s investment ~45% of GDP vs ~22% typical)", "moderate"),
    "k_int": (ln(1.0, 0.3), "capital intensity of automated capacity relative to average (robots cheaper than labor but capex-heavy)", "low"),
    "r_retro0": (("uniform", 0.02, 0.06), "retrofit/scrapping rate of human-operated capacity, no priority", "moderate"),
    "r_retro_p": (("uniform", 0.10, 0.30), "retrofit/scrapping rate under full priority (deliberate replacement)", "low"),
    "kit_brake": (("uniform", 0.1, 0.5), "automation-kit growth halves once new kit equals this share of the physical workforce", "moderate-low"),
    "humanoid_mult": (ln(2.0, 0.3), "general-purpose robot output multiple per yr before AI-directed production (Goldman 1.9x/yr; SAG +272% 1H2026 from tiny base)", "moderate"),
    "P_half": (ln(5.0, 0.6), "M robots/yr per bloc at which the human-built ramp halves (NEV 2.2x -> 1.35x at 7-13M)", "moderate"),
    "Pmax_h": (ln(50, 0.6), "M robots/yr reachable with 2026-level human labor (auto industry ~90M vehicles/yr)", "low"),
    "prod_use": (("uniform", 0.4, 1.0), "productive-use share of shipped humanoids", "low"),
    "M0": (ln(30, 0.7), "M robots/yr supportable by divertible NdPr", "moderate"),
    "C0": (ln(20, 0.9), "M robots/yr of inference chips at ~20% diversion", "low"),
    "Td_mine_base": (ln(15.0, 0.3), "mineral supply doubling without priority (copper etc. 3-5%/yr)", "good"),
    "Td_mine_race": (ln(3.5, 0.3), "mineral doubling for a priority actor (Indonesia nickel, lithium 2020-24: 2-2.5 y)", "moderate"),
    "Td_mine_auto": (ln(1.5, 0.45), "mineral doubling floor once mining/processing robotic (ore grades)", "low"),
    "Td_fab_base": (ln(11.0, 0.2), "wafer capacity doubling at 6-7%/yr (SEMI)", "moderate"),
    "Td_fab_race": (ln(2.5, 0.3), "chip capacity doubling for a race actor (JASM 2.7 y, TSMC AZ 3.5 y build)", "moderate"),
    "fab_build": (ln(2.5, 0.25), "groundbreaking to volume production", "good"),
    "fact_build_h": (ln(1.2, 0.5), "greenfield factory build, human (Giga Shanghai 11 mo, Colossus 122 days)", "moderate"),
    "fact_build_a": (ln(0.5, 0.45), "same with prefab/robotic construction", "low"),
    "Td_en_base": (ln(20.0, 0.3), "electricity capacity doubling without priority", "moderate"),
    "Td_en_race": (ln(3.0, 0.3), "electricity doubling with priority (China solar ~2.2 y, total ~5 y)", "good for China"),
    "Td_en_auto": (ln(1.5, 0.45), "energy doubling floor in an automated loop (PV payback ~1 y)", "low-moderate"),
    "Td_auto": (ln(1.0, 0.6), "robot-stock doubling once AI directs production (Forethought, theory)", "low (theory)"),
    "Td_mat": (ln(0.25, 1.0), "mature fully automated industrial doubling", "very low"),
    "ai_lc": (ln(1.3, 0.2), "AI compression of design/permitting/planning lead times, phased in by M3 (bounded 1.05-2x)", "very low"),
    "adl": (ln(3.0, 0.5), "one-time productivity multiple of AI-directed human build labor (Forethought claims 10x; upper bound)", "low"),
    "reinvest": (("uniform", 0.3, 1.0), "share of automated output reinvested in expansion", "low"),
    "G_max": (ln(300, 1.0), "terrestrial ceiling on robot worker-equivalents per 2026 worker", "very low"),
    "robot_life": (("uniform", 6, 12), "robot service life", "moderate"),
    "q_core": (ln(0.15, 0.6), "scale of minimal self-sufficient core loop vs full chain", "very low"),
    # ------------------------------------------------ power game
    "psi0_US": (("beta", 3.5, 6.5), "US bloc pursuit intensity (Genesis, DoD all-lawful-use)", "weak"),
    "psi0_CN": (("beta", 4.5, 5.5), "China pursuit (MIC2025, +20%/yr robot installs, 'intelligent military')", "weak"),
    "psi0_RW": (("beta", 1.5, 8.5), "rest-of-world pursuit (x1.5 Europe, x1.0 Russia_MENA, x0.8 South Asia, x0.6 Global South)", "weak"),
    "race_gamma": (("uniform", 0.5, 2.0), "pursuit response to rival lead", "weak"),
    "t_leth_rate": (("const", 0.115), "per-bloc rate of routine lethal targeting with no per-strike human approval (r8c)", "weak"),
    "k_pg": (ln(0.012, 0.8), "narrow-group power grab hazard at full security/admin automation (Forethought AI coups)", "weak"),
    # ------------------------------------------------ elite game
    "alpha_med": (ln(0.02, 1.0), "F4: elite willingness to pay for the welfare of a population with no leverage, share of output. Analog: OECD ODA ~0.3% of donor GNI (falling 2025) plus an in-group premium for co-nationals; US private giving ~2% GDP is the upper side; welfare-state spending is leverage-driven and not used (r10a) [M]", "C"),
    "alpha_sig": (("uniform", 0.6, 1.4), "within-coalition heterogeneity", "low"),
    "p_hostile": (("beta", 1.5, 40.0), "F4: baseline share of coalition members hostile to the public (welfare inverted), mean 3.6%. Psychopathy ~1% general population, 3-4% in senior corporate roles (Babiak, Neumann & Hare 2010, verified); callousness (indifference) is carried by the moral_med and alpha tails, not here (r10a). Round 2: Beta(1.2,14), mean 8%", "C"),
    "moral_med": (ln(0.3, 1.2), "moral cost of ordering mass killing, output-share equivalent (Sagan & Valentino 2017 wartime polls; Bandura 1999). No direct measurement", "J"),
    "m_pow": (("uniform", 0.7, 1.0), "F4: moral-cost multiplier in autocratic coalitions (power reduces perspective-taking: Galinsky 2006, Hogeveen et al. 2014, Keltner 2016; mixed replication)", "C-"),
    "k_mor": (("uniform", 0.0, 0.02), "A7: yearly decline of the moral cost (partisan dehumanization, AI targeting compressing human review; r9d, r11a)", "J"),
    # F2: absolute refusal of killing, by layer and regime (r10a). Literature (weight 0.7, evidence C) mixed with Jev (0.3)
    "p_ref_dem": (("mix", 0.7, ("beta", 7.0, 3.0), ("beta", 8.0, 2.0)), "F2: share of a DEMOCRATIC ruling elite that absolutely refuses to order killing of the population. Not filtered for obedience; refused far smaller illegal acts (Esper/Milley 2020, Pence 2021, 1973); no democide by democracies against own citizens (Rummel, Harff 2003). Lit Beta(7,3) mean 0.70; Jev cross-check 0.75-0.85 -> Beta(8,2)", "C"),
    "p_ref_olig": (("mix", 0.7, ("beta", 2.0, 10.0), ("beta", 2.0, 4.0)), "F2: same, party/oligarchic elite. Rwanda 1994: ~10-20% of the senior layer resisted (Butare prefect dismissed in ~12 days); Soviet Politburo 1932-33 no recorded refusal. Lit Beta(2,10) mean 0.17; Jev ~0.33 (single veto holder, Beta(2,4))", "C"),
    "p_ref_pers": (("mix", 0.7, ("beta", 1.2, 12.0), ("beta", 1.0, 19.0)), "F2: same, personalist inner circle, selected for loyalty after purges. Wannsee 0 of 15 moral objections (verified); Stalin CC 70% arrested 1934-39; Saddam 1979. Lit Beta(1.2,12) mean 0.09; Jev ~0.05", "C"),
    "h_purge": (("uniform", 2.0, 8.0), "F2: half-life (y) of the convergence of a new autocracy's refusal share toward the autocratic value (Stalin 1934-39, Saddam 1979, Turkey post-2016)", "B/C"),
    "r_neg": (("uniform", 0.2, 0.6), "F2 bug fix: absolute refusal of LETHAL NEGLECT relative to refusal of killing. Officials who would not order killings enforced lethal neglect (Holodomor, Great Leap, Irish famine, Bengal 1943; Bandura 1999). Round 2 made every killing-refuser also an absolute neglect-refuser", "C"),
    "kappa_N": (("uniform", 0.05, 0.3), "neglect moral cost relative to killing", "low"),
    # F1: regime-dependent decision rule (r10a)
    "q_ol": (("uniform", 0.5, 0.67), "F1 OLIG: weighted share of the collective leadership needed to move to a HARSHER option (bargaining; Svolik 2012 power-sharing). Milder moves need a simple majority", "C"),
    "s_tilt": (("uniform", 0.0, 1.0), "F1 PERS: selection tilt of the leader toward the harsh end of the coalition's preference distribution (leader at quantile u^(1/(1+s)))", "J"),
    "v_eff": (("uniform", 0.05, 0.30), "F1 PERS: P(inner-circle veto succeeds) at fully human security/admin; scales with h_sa. Holodomor, T4, Khmer Rouge: no inner-circle veto; Great Leap veto ~3 y late (1962)", "C"),
    "k_pz": (("uniform", 0.02, 0.10), "F1: hazard/yr of an oligarchy turning personalist at fully automated security/admin (x(1-h_sa)); personalist share of autocracies rose to 40-52% (GWF, Kendall-Taylor et al. 2016)", "C"),
    "conc_k": (("uniform", 0.5, 1.5), "A6: log-normal dispersion of members' control over automated kinetic force (faction weight = control share as security/admin automate; money and labor-based resources count for nothing)", "J"),
    # F3 / A4: security-force defection, systematic breakdown (Stephan & Chenoweth 2008; NAVCO; Lee 2015; Nepstad 2011; Barany 2016)
    "q_I": (("mix", 0.7, ("beta", 2.0, 8.0), ("beta", 4.5, 5.5)), "F3: P(systematic defection) under counterinsurgency orders. Armed challengers make forces close ranks (Stephan & Chenoweth 2008, verified). Lit Beta(2,8); Jev ~0.45", "B/C"),
    "q_C": (("beta", 2.5, 7.5), "F3: P(systematic defection) under collective-punishment orders (Mau Mau, Herero, Guatemala: mostly out-group or stacked units)", "C"),
    "q_X": (("beta", 5.0, 3.5), "F3: P(systematic defection) under orders to kill or starve the general majority population (forces' own kin among the targets; Khmer Rouge peak ~22-25% via class split). Lit and Jev (~0.55) agree", "J/C"),
    "m_stack_pers": (("uniform", 0.4, 0.8), "F3: defection multiplier for personalist regimes (coup-proofing, ethnic stacking: Makara 2013, Lee 2015; Syria 2011-13)", "B"),
    "m_stack_olig": (("uniform", 0.7, 1.0), "F3: same, oligarchic/party regimes (Egypt 2011 army as institution)", "B"),
    "d_def": (("uniform", 0.3, 0.7), "F3: share of HUMAN coercive units lost in a systematic breakdown", "C"),
    "c_req": (("uniform", 0.4, 0.7), "F3: share of coercive capacity an order needs; it fails if d_def x human share > 1 - c_req. A4: once automated systems carry the order the executor check is gone (a threshold, not a slow fade)", "C"),
    "p_oust": (("uniform", 0.5, 0.8), "F3: P(leader/faction ousted after a failed X or C order; policy resets to status quo)", "C"),
    "OR_def": (ln(4.0, 0.4), "F3: insurgent success odds multiplier from systematic defection (Stephan & Chenoweth 2008: defections more than quadruple success, verified). Replaces def_mult", "B"),
    "C_oust": (ln(0.3, 0.8), "F3: members' anticipated cost of ouster, output-share equivalent, weighted by P(order fails)", "J"),
    "m0": (("uniform", 0.3, 0.6), "cost of decent provision / output in 2026 terms", "moderate"),
    "c_W": (("uniform", 0.15, 0.4), "warehouse cost relative to serve", "low"),
    "c_R": (("uniform", 0.7, 1.0), "rentier cost relative to serve (full provision, no political rights)", "low"),
    "w_R": (("uniform", 0.45, 0.7), "public welfare under rentier rule relative to serve (Gulf citizens: rich, no vote)", "low"),
    "thk_R": (("uniform", 0.5, 0.9), "residual revolt threat under rentier rule relative to warehouse (Saudi 2011 buy-off worked; Bahrain excluded group revolted)", "B-/C"),
    "tau0": (ln(0.03, 0.9), "expected loss from an aggrieved population / output per yr with human security", "low"),
    "E0": (ln(0.10, 0.8), "legitimacy + international pressure / output at full rival leverage", "low"),
    "intl": (("uniform", 0.0, 1.5), "extra international response (sanctions, war risk) to executing depopulation, multiple of E0 term", "very low"),
    "v0": (ln(0.01, 1.1), "F4: land/resource value freed by removing population, share of output (urban land value depends on population; settler-colonial land: Wolfe 2006, Natives Land Acts 1913/1936, US Indian removal)", "J/C"),
    "v1": (ln(0.03, 1.0), "Ricardian scarcity rent as the terrestrial ceiling binds (50% mass at zero)", "very low"),
    "r_disc": (("uniform", 0.03, 0.10), "discount rate for one-time acts", "moderate"),
    "phi_stigma": (("beta", 1.5, 3.5), "recurring share of killing's moral/legitimacy cost", "very low"),
    "s_sw": (ln(0.25, 0.8), "one-time cost of switching provisioning regime, output-years (0.07-0.9; round 1 used 0.1, which with no confirmation step let blocs ratchet into harsh options)", "low"),
    "p_exec": (("uniform", 0.75, 0.95), "P(an ordered depopulation is carried out, operationally), EXCLUDING security-force defection, which is now explicit (F3). Round 2 U(0.7,0.95); Jev grid refusal at zero human security 0.08-0.15 -> 0.85-0.92; mixture. Failure leaves 1-5% dead and a desperate insurgency", "J"),
    "x_thr": (("uniform", 1.0, 3.0), "threat multiplier during execution (a population facing extermination resists harder than a warehoused one, but targeted populations historically rarely mounted effective resistance)", "C"),
    "p_small": (("uniform", 0.1, 0.3), "P(once security and admin are automated, the deciding circle shrinks to 1-7 people) per consolidated autocracy; otherwise >=21 (selectorate data; Jev assumes ~500)", "C/very low"),
    "lag_dec0": (("uniform", 1.0, 5.0), "years from closure to strategic decision at 2026 decision speed", "low"),
    "spd_max": (ln(2.0, 0.5), "strategic decision-speed compression at full AI R&D automation (r8d)", "weak"),
    "Tn": (ln(7.0, 0.5), "years of neglect to 10% population loss (Irish famine 12% in ~5 y)", "low-moderate"),
    "lagX": (("uniform", 0.5, 3.0), "years from executed depopulation decision to 10% loss", "low"),
    "a_vote": (("uniform", 0.15, 0.45), "welfare weight added per unit of D_dem", "low-moderate"),
    "k_inst": (("uniform", 1.0, 4.0), "moral/legitimacy cost multiplier per unit of D_dem", "low"),
    # ------------------------------------------------ grievance loop (r9c)
    "griev_trend": (("uniform", 0.03, 0.10), "initial yearly rise of anti-AI grievance attitudes (Pew 31%->39% 'more harm' in one year). F7: logistic toward g_max instead of a hard cap at 0.55", "A polls, C extrapolation"),
    "g_max": (("uniform", 0.80, 0.95), "F7: ceiling of the grievance-attitude share. Public-opinion saturation: Gallup US Congress disapproval peaked ~85-90% (approval 9%, Nov 2013) [M]", "C"),
    "att_max": (("uniform", 0.50, 0.70), "F7: ceiling of attitudinal support for political violence (replaces the 0.5 cap). Upper range in populations in open conflict: PCPSR polls, support for armed struggle ~50-60% [M]", "C"),
    "cr_hl": (("uniform", 1.0, 3.0), "F8: half-life (y) of a crisis provision response once grievance stops rising (CARES Act 2020 large but temporary)", "C"),
    "s_nino": (("uniform", 0.2, 0.5), "A7: ecological-stress index during the record 2026-27 El Nino, until mid-2028 (NOAA CPC 10 Sep 2026: Nino-3.4 +1.8 C, 75% chance of a historic event)", "B"),
    "k_intl": (("uniform", 0.0, 0.04), "A7: yearly decay of international pressure E0 (US withdrawal from 66 international organizations, Jan 2026; UNGA-81 walkouts; 'breakdown' not verified)", "B sign, J size"),
    "r_ab": (("uniform", 0.3, 0.7), "share of displaced labor reabsorbed into new human work at 2026 breadth", "low"),
    "k_ineq": (("uniform", 0.0, 1.0), "grievance amplification from visible inequality", "low"),
    "pg_red": (ln(0.30, 0.45), "fraction of grievance removed by full provision (status loss persists): 0.1-0.6", "C"),
    "pr_red": (("mix", 0.6, ("uniform", 0.3, 0.7), ("uniform", 0.05, 0.4)), "fraction of revolt hazard removed by full provision. r9c (Saudi 2011 buy-off) U(0.3,0.7), weight 0.6; Jev grid U(0.05,0.4) (almost no provision effect), weight 0.4. Reported as a disagreement", "B-/Jev"),
    "k_resp": (("uniform", 0.2, 0.8), "democratic provision response to grievance", "A- direction, C size"),
    "k_buy": (("uniform", 0.1, 0.5), "autocratic buy-off of grievance while coercion still needs humans (Saudi 2011)", "B-"),
    "h_beh0": (ln(0.005, 0.6), "behavioral hostile faction share (would join sabotage/violence), 2026", "low"),
    "att_trend": (("uniform", 0.0, 0.04), "yearly rise of attitudinal support for political violence (PRRI 15%->23% 2021-23)", "medium"),
    "e_att": (("uniform", 0.3, 0.7), "elasticity of behavioral hostility to attitudinal support (attitudes rose without proportional organized violence)", "C"),
    "e_g": (("uniform", 0.5, 1.0), "elasticity of hostility to the grievance state Gv", "C"),
    "mdisp": (ln(1.5, 0.25), "hostile-share multiplier per 10 pp displaced (Swing riots; GTI)", "low"),
    "Hmax": (("uniform", 5.0, 10.0), "round-2 saturation of relative hostility; used only in the caps_v4 variant", "C"),
    "Habs": (("uniform", 0.05, 0.20), "F7: saturation of the BEHAVIORAL hostile share (would join sabotage/violence), absolute share of adults. Replaces the relative Hmax 5-10 and the 50%-displacement cap. Active participation in the largest revolutions/insurgencies ~3.5-15% of the population (Chenoweth 3.5% rule; mass-mobilization peaks) [M]", "C"),
    "p_svr_hi": (("mix", 0.6, ("uniform", 0.15, 0.5), ("uniform", 0.12, 0.35)), "P(sustained violent resistance over ~10 y | 30% displaced, provision 0.2, high-capacity state). r9c U(0.15,0.5) weight 0.6; Jev grid U(0.12,0.35) weight 0.4", "C/Jev"),
    "p_svr_weak": (("uniform", 0.35, 0.7), "same, low-capacity state", "B-/C"),
    "lam0_hi": (ln(0.003, 0.5), "2026 hazard of a NEW sustained insurgency at zero displacement, high-capacity bloc (UCDP onset 0.1-0.5%/yr for high-capacity states; none in US/China for decades)", "B"),
    "lam0_weak": (ln(0.012, 0.5), "same, low-capacity bloc of 2-3B people (new campaigns beyond the 2026 baseline)", "B-"),
    "elec": (("uniform", 0.3, 0.7), "revolt risk diverted to elections per unit D_dem", "B"),
    "aU": (("uniform", 0.3, 1.0), "anocracy excess onset risk (inverted U, Hegre et al. 2001)", "B-"),
    "d_surv": (("uniform", 0.2, 0.6), "onset hazard factor at fully automated security/surveillance (Xu 2021 digital repression; Xinjiang)", "C"),
    "rd": (("uniform", 0.4, 0.8), "P(consistent high-capacity repression suppresses sustained resistance within 5 y)", "B-"),
    "k_auto": (("uniform", 0.3, 0.9), "extra suppression effectiveness of automated security", "C"),
    "coin_win": (("uniform", 0.25, 0.75), "incumbent win rate vs insurgency", "B/C"),
    "ins_dur": (ln(8.0, 0.4), "mean insurgency duration, years", "B"),
    "def_mult": (("uniform", 0.15, 0.6), "insurgent success odds multiplier when security fully automated", "C"),
    "p_dem_suc": (("uniform", 0.2, 0.35), "P(a successful violent campaign leads to democracy; otherwise a new narrow autocracy) (Chenoweth-Stephan)", "B"),
    "k_bf": (("uniform", 0.2, 1.0), "backfire from repression that fails to deter; also added after collective punishment", "C"),
    "dfd": (("uniform", 0.3, 0.7), "hostility damping after a defeated revolt (decays over 5 y)", "C"),
    "ins_mort": (ln(3e-4, 1.0), "crackdown/insurgency deaths per year of active insurgency, fraction of population", "C"),
    "p_lcp": (("uniform", 0.15, 0.6), "P(lethal collective punishment during an insurgency | labor unneeded, weak external check)", "C"),
    "f_lcp": (ln(0.03, 0.9), "share of the aggrieved regional population killed per episode (Mau Mau ~1-2% of Kikuyu, Gaza ~3%, Herero 65-80%)", "C"),
    "m_d": (ln(0.002, 0.5), "excess mortality/yr of status-stripped, welfare-dependent displaced adults (deaths of despair ~0.2-0.3%/yr in the affected group; Native American life-expectancy gap ~0.3-0.5%/yr)", "B-"),
    "hgain": (("uniform", 0.0, 0.5), "offset of despair mortality by AI-era health gains at full automation", "low"),
    "tau_sab": (ln(0.005, 1.0), "sabotage cost to automated infrastructure / output per yr at reference hostility", "low"),
    "ins_thr": (("uniform", 1.0, 3.0), "threat multiplier during active insurgency", "C"),
    "host_ins": (("uniform", 0.05, 0.25), "F4: coalition hostility added by active insurgency (insurgent threat radicalizes elites toward eliminationist policy: Valentino, Huth & Balch-Lindsay 2004; Harff 2003; Straus 2006; Kteily et al. 2016)", "C"),
    "host_H": (("uniform", 0.0, 0.15), "coalition hostility added by public hostility; F7: smooth saturation host_H*(1-exp(-(Hr-1)/3)) instead of a cap at 4x", "C"),
    # ------------------------------------------------ democracy (r9d)
    "h_on": (("uniform", 0.04, 0.07), "autocratization onset hazard per democracy-year, all countries (V-Dem: 10 new of 179)", "M"),
    "h_bd": (ln(0.005, 0.6), "breakdown hazard of a rich democracy at intact leverage (Przeworski et al. 2000)", "M"),
    "M_lev": (ln(5.0, 0.6), "erosion hazard multiplier as leverage goes 1 -> 0", "L"),
    "e_rate": (("uniform", 0.04, 0.12), "LDI decline per year during an episode (US -0.218 since 2023)", "M"),
    "p_uturn": (("uniform", 0.5, 0.8), "P(episode reverses before breakdown | leverage intact)", "M"),
    "conc": (("uniform", 0.3, 0.9), "concentration of AI/robot ownership", "low"),
    "em_jump": (("uniform", 0.02, 0.10), "D_dem drop from emergency powers at war/insurgency onset", "low"),
    # ------------------------------------------------ time trends, war (r9d)
    "c_trend": (("uniform", 0.05, 0.12), "log trend of armed-conflict intensity (GPI 2008-2025)", "M"),
    "c_max": (("uniform", 1.5, 4.0), "cap on conflict-intensity index relative to 2026", "judgment"),
    "w_pair": (ln(0.007, 0.6), "US-China war hazard per year at 2026 intensity", "low (judgment)"),
    "w_row": (ln(0.015, 0.6), "major-war hazard per year for a non-US/China bloc at 2026 intensity (x0.5 Europe, x1 Russia_MENA, x0.8 South Asia, x0.6 Global South)", "low (judgment)"),
    "war_len": (("uniform", 2.0, 6.0), "war duration, years", "low"),
    "ukr_rem": (("uniform", 0.5, 4.0), "remaining years of the Russia-Ukraine war from Oct 2026", "low"),
    "w_mort": (ln(0.0008, 0.8), "war deaths per war-year as a fraction of a whole bloc's population (Ukraine ~1%/yr for the belligerent; blocs are larger)", "low"),
    "p_nuc": (ln(0.02, 0.6), "P(nuclear use | a major war of a nuclear-armed bloc)", "very low"),
    "f_nuc": (("uniform", 0.02, 0.3), "bloc population share killed if nuclear weapons are used", "very low"),
    "m_war": (("uniform", 0.2, 0.7), "moral cost of killing in war/insurgency vs peacetime", "L/M"),
    "mc_ai": (("uniform", 0.5, 0.9), "moral-cost factor at fully AI-mediated targeting", "L"),
    "eco_year": (("uniform", 2045.0, 2100.0), "year ecological stress reaches 'severe' (ETR 2025)", "low"),
    "eco_mult": (ln(1.5, 0.35), "conflict multiplier at severe ecological stress (1.2-4)", "M"),
    "eco_land": (("uniform", 0.0, 2.0), "rise in land/resource value share at severe ecological stress (50% mass at zero)", "very low"),
    "p_id": (ln(0.045, 0.6), "P(depopulation/successionist ideology taken up by a closed bloc's rulers within 9 y, no war; war x2.5). Calibrated so P(US or China bloc by 2045) ~0.08 (r9d)", "L"),
    "id_hl": (("uniform", 10.0, 20.0), "half-life of a ruling ideology (regime turnover, generational change), years", "L"),
    "id_share": (("uniform", 0.1, 0.3), "coalition hostility share added when that ideology is fully held (builds over ~4 y)", "L"),
    # ------------------------------------------------ endgame (A8, A9, A11). Abstract parameters only: no mechanism specifics
    "T_full": (("uniform", 2.0, 15.0), "A8: years for an executed depopulation carried by automated force plus economic strangulation to reach >=99.9% loss if unconstrained (hazard ramps linearly from the lagX rate); no precedent at this scale, so wide (A10)", "J"),
    "dL_means": (("uniform", -2.0, 6.0), "A8: horizon doublings beyond M3 (90% software capability) at which a means of rapid mass killing is available to a closed bloc's coalition (abstract availability; probit width 1 doubling)", "J"),
    "h_use": (("uniform", 0.2, 1.0), "A8/A9: yearly hazard that a coalition executing depopulation uses such a means once available", "J"),
    "f_eng": (("uniform", 0.5, 0.99), "A8: share of the remaining targeted population killed by one use (abstract)", "J"),
    "p_tot0": (("uniform", 0.2, 0.6), "A11: P(the designation targets near-total removal from the start); otherwise an initial partial target f0", "J"),
    "f0": (("uniform", 0.3, 0.9), "A11: initial partial target (share of population) when the designation is partial", "J"),
    "k_esc": (("uniform", 0.1, 1.0), "A11: yearly hazard of escalating a partial designation to near-total, per unit of perceived revenge threat (grievance/0.5 x (1 + active insurgency)): any free surviving community is a seed that can organize and take revenge (dark-forest logic)", "J"),
    "rem": (("uniform", 0.0003, 0.001), "A11: captive remnant kept without rights (scenario: ~8 million of 8 billion = 0.1%)", "scenario"),
    "k_col": (("uniform", 0.2, 1.0), "A9: yearly hazard of tacit collusion (economic or hot war on each other's populations) between two coalitions that both execute depopulation, when incentives favor it", "J"),
    "b_col": (ln(1.0, 1.0), "A9: rulers' value of collusion (cover, elimination of the other bloc's human seed), relative units", "J"),
    "c_self": (ln(20.0, 1.0), "A9: rulers' value of their own survival in the same units; collude iff b_col > (1 - s_bunk) x p_nx x c_self", "J"),
    "s_bunk": (("uniform", 0.5, 0.95), "A9: rulers' own survival probability in a nuclear exchange given bunker preparations", "J"),
    "p_nx": (("uniform", 0.05, 0.3), "A9: P(a collusive war goes nuclear)", "J"),
    "f_nx": (("uniform", 0.2, 0.7), "A9: share of each colluding bloc's remaining population killed by a nuclear exchange", "J"),
    "w_col": (("uniform", 0.02, 0.10), "A9: yearly deaths of the remaining population from collusive economic/hot war (on top of the executing bloc's own means)", "J"),
}
COMPAT = ["F_ac", "ac_horizon_hours", "tau_phys", "tau_cog", "g_h", "Td_mine_h", "Td_fab_h", "Np", "sw_auto0"]

# ---- ROUND 3 (changes B1-B6 agreed with the scenario; research/r12a_round3_evidence.md). Drawn AFTER every
# round-2 draw, from the same numpy stream, so that with all B switches off the round-2 model is reproduced exactly.
PRIORS_B = {
    # B1: moral cost of those at the top, anchored to observed autocrat behaviour, not to average people
    "sel_top": (("uniform", 0.1, 0.6), "B1: moral-cost AND refusal multiplier for the person at the top of an autocratic coalition (selection: those who fight their way to that much power have less of the brake). Members of an autocratic coalition get sel_top^0.5. Anchors (qualitative, mapped by judgment): psychopathy ~1% general population vs ~3-4% in senior corporate roles (Babiak & Hare 2007; Babiak, Neumann & Hare 2010); elevated fearless dominance among US presidents (Lilienfeld et al. 2012, JPSP 103:489); tyrants as malignant narcissists with superego deficits (Glad 2002, Pol. Psych.); revealed casualty tolerance: Russia ~1.1-1.25M casualties incl. ~250-500k killed by early/mid 2026 (UK DI Oct 2025 1.118M; Telegraph Feb 2026 >1.25M; BBC/GCHQ May 2026 ~500k killed) for territorial aims; DPRK camps 80-120k prisoners, 'hundreds of thousands' dead over five decades (UN COI 2014); Great Purge 681,692 executions 1937-38, 3 of 5 marshals; Great Leap famine continued ~3 y", "J (C anchors)"),
    "id_mor": (("uniform", 0.3, 0.8), "B1: share of the remaining moral cost removed when a depopulation ideology is fully held (reframing as kindness / ecological reset: moral justification and euphemistic labelling, Bandura 1999)", "C/J"),
    # B2: consolidation from incentives (purges, coup-proofing, commitment problems, paranoia)
    "k_prg": (("uniform", 0.05, 0.30), "B2: yearly purge hazard per coalition member at full incentive (leader holds all force, needs no human staff). Anchors: 70% of the 1934 CC arrested by 1939 (~0.24/yr); Great Purge removed 3 of 5 marshals and ~13 of 15 army commanders; Saddam 1979; Turkey post-2016", "C"),
    "prg_c0": (("uniform", 0.1, 0.4), "B2: share of the purge incentive present even while the leader still needs competent human staff (loyalty-competence trade-off, Egorov & Sonin 2011; purges happened in fully human regimes). The rest scales with (1 - human share of security/admin)", "C/J"),
    "c_cc": (("uniform", 0.1, 0.5), "B2: P(counter-coup) per purge event, times the rest of the coalition's share of force (1 - S_L). Svolik 2012: insiders remove ~2/3 of ousted autocrats; Sudduth 2017: dictators purge when elites' capacity to oust them is temporarily low", "C"),
    "k_par": (("uniform", 0.5, 3.0), "B2/B4: purge-incentive multiplier per 10% of the population already killed deliberately (scenario: 'guilt turns to paranoia'; fear of retribution after atrocities)", "J"),
    "k_extp": (("uniform", 0.0, 0.8), "B2: reduction of purge incentive when a rival of comparable automated force exists (Goldring: purges more likely when foreign and revolutionary threats are low)", "C/J"),
    # B3: outside cost only if enforceable
    "k_am": (ln(10.0, 0.8), "B3/B5: force multiplier of automated over human-staffed forces at equal output (Ukraine: drones cause ~60-80% of front-line casualties, r9a [K]; colonial tech asymmetry, e.g. Omdurman 1898 [M]). Kinetic power M = output x (1 + k_am x automated share of security)", "J"),
    # B4: fear of retribution grows with the scale of what has been done
    "k_ret": (("uniform", 0.5, 3.0), "B4: multiplier on the rulers' perceived threat from survivors per 10% of population already killed deliberately (also scales A11 escalation). Archigos: most leaders removed irregularly are exiled, jailed or killed (research/m5)", "J/C"),
    # B5: cross-bloc depopulation (foreign populations are witnesses and potential avengers)
    "k_xb": (("uniform", 0.1, 1.0), "B5: yearly hazard that an executing closed coalition extends depopulation to a bloc it can overpower, when its payoff test passes", "J"),
    "dom_thr": (("uniform", 0.7, 0.95), "B5: share of combined kinetic power (aggressor / (aggressor + target)) the aggressor needs before attacking", "J"),
    "p_ret0": (("uniform", 0.3, 0.9), "B5: P(a nuclear-armed target retaliates) at parity; falls as (1 - dominance) since an overwhelmingly dominant automated force can suppress a deterrent (counterforce, defence). Arsenals: FAS 2026 (US 3,700, Russia 4,400, China 620, France 290, UK 225, India 190, Pakistan 170, Israel 90, DPRK 60)", "J"),
    "k_rep": (("uniform", 0.5, 2.0), "B5: yearly hazard of repelling a cross-bloc campaign, times the target's share of combined kinetic power", "J"),
    # B6: physical bottlenecks
    "cn_ppp": (("uniform", 1.0, 2.0), "B3/B5: multiplier on China's military-expenditure share for purchasing-power parity (market-rate SIPRI figure understates Chinese military output)", "C"),
    "k_kit": (ln(0.3, 0.7), "B6/F6: draw of fixed automation kit on the shared robot-input budget (magnets, chips, actuators) per worker-equivalent, relative to a general-purpose robot", "J"),
}

# ---- BRAKES (paper/brake_search_protocol.md; ranges and notes in paper/brake_search_results.json). Drawn after EVERY
# existing draw from a SEPARATE numpy stream (seeded from the already-drawn sim_seed array), so the main stream, and
# therefore every existing parameter, is unchanged. All three brakes are OFF by default (flags pid_on, sr_on, brk_mort);
# variants brake_pid, brake_selfrisk, brake_mort and brakes_all switch them on.
PRIORS_BRK = {
    # Brake 1: protective doctrine (mirror of p_id / id_hl / id_lev)
    "p_pid": (ln(0.065, 0.8), "BRAKE 1: P(protective doctrine sincerely taken up by a bloc's rulers within 9 y), x0.1 before closure, fades with id_hl. Jev 2026-10-02: 0.07/0.06/0.07", "J"),
    "k_pid": (ln(1.2, 0.9), "BRAKE 1: moral-cost multiplier 1 + k_pid x pid_lev when the protective doctrine is held. Cases: Gorbachev 1989 (Levesque 1997), Ashoka RE XIII", "C/J"),
    # Brake 2: anticipated self-targeting ('I could be next'; Thermidor 1794, Beria 1953; Svolik 2012)
    "c_selfrisk": (ln(1.0, 1.5), "BRAKE 2 (revised after re-audit, brake_search_followup.json): non-leader members' cost per unit rise in own yearly purge probability (output share). Round 1: ln(1.5, 1.2). Shaded down (no case shows rulers held back from killing the public), wider (Jev ignores gain size)", "J"),
    "e_ex": (("uniform", 0.25, 0.6), "BRAKE 2 (revised): share of non-leader members who expect exemption from the apparatus (round 1: U(0.25, 0.5)); raised by the depopulation ideology via b_id", "J"),
    # Brake 3: leader mortality and succession reset
    "h_mort": (("uniform", 0.01, 0.05), "BRAKE 3: yearly hazard that the B2 leader dies or is incapacitated (CDC NVSR 72(12) 2021 male life table; Chetty et al. 2016 elite gradient)", "C"),
    "g_mort": (("uniform", 0.085, 0.085), "BRAKE 3: Gompertz slope of the leader hazard per year (mortality doubles ~every 8 y)", "C"),
    "k_le": (("uniform", 0.0, 0.10), "BRAKE 3: yearly rate at which AI-era medicine cuts the leader hazard after closure", "J"),
    "p_heir": (("uniform", 0.3, 0.8), "BRAKE 3: P(control passes intact to one heir) on a leader death; else it splits among surviving members (6/11 personalist deaths in office; Jev 0.38 under A6)", "C/Jev"),
}
BRK_FLAGS = {"pid_on": "brake_pid", "sr_on": "brake_selfrisk", "brk_mort": "brake_mort", "dis_on": "brake_selfrisk_dis"}
# follow-up round (paper/brake_search_followup.json): drawn from the brake stream AFTER mem_u_sx, so every round-1 brake
# draw keeps its stream position (p_pid/k_pid identical; c_selfrisk/e_ex use the same normals/uniforms on new ranges)
PRIORS_BRK2 = {
    "b_id": (("uniform", 0.0, 0.4), "BRAKE 2: rise in exemption when the depopulation ideology is held: e_ex_eff = e_ex + (1 - e_ex) b_id id_lev (outgroup-targeting doctrines mark who is 'in'; Mann 2005, Straus 2015; floor 0: Khmer Rouge, Stalin 1937)", "J"),
    "m_dis": (ln(4.0, 0.8), "BRAKE 2 no-side (dissent risk): multiplier on the current B2 purge hazard for an exposed member identified as an objector (vote below the leader's ideal, or a failed veto). Cases: Piatnitsky/Kaminsky 1937, Lushan 1959; ~1 post-1953. Jev net 1.5-3.3", "C/J"),
}


# ---- OWN-INDUSTRY COMPUTE FEEDBACK (cf_on; see the COMPUTE FEEDBACK blocks in _sim_chunk). Two new priors, drawn from
# their OWN numpy stream (seeded from sim_seed with a different tag than the brake stream) after every existing draw, so
# no existing parameter changes. OFF by default.
PRIORS_CF = {
    "eta_cf": (("uniform", 0.5, 1.5), "COMPUTE FEEDBACK: horizon doublings per extra doubling of a bloc's own compute production beyond the trend. Anchor: horizon doubles every 4-7 months while frontier training compute grows ~4-5x/yr (~2.1 compute doublings/yr), i.e. ~0.8-1.4 horizon doublings per compute doubling", "C"),
    "s_sp": (("uniform", 0.1, 0.5), "COMPUTE FEEDBACK: yearly rate at which other blocs close the gap to the leader's extra capability (theft, open weights, talent); multiplied by 1 - 0.7 psi of the leader (a racing leader leaks less)", "J"),
}
CF_NOTE = dict(
    flag="cf_on (off by default). M8_FINAL=1 = final configuration (four final brakes + greenfield + compute feedback); M8_CF=1 = compute feedback only; variants 'computefb' (cf), 'greenfield_cf' (gf + cf)",
    state="E[bloc] = extra capability doublings of the bloc beyond the shared (B6-lagged) trend L; the bloc's capability is L_b + E. Ep[bloc] = the matching extra physical-capability logit: the bloc's physical capability grows at rp evaluated at L + E instead of L (difference accumulated), capped by the shared physical ceiling Lpcap",
    driver="dE/dt = eta_cf x max(0, dlnC_b/dt - g_trend) / ln2 (doublings/yr). C_b = min(domestic chip capacity (rsh_c x Gc under B6, chip_share x Gc otherwise), energy capacity Ge), both normalised to 2026 = 1. g_trend = the compute growth the shared trend already embodies = min(ln2/Td_fab_race, ln2/Td_en_race) x lc (human-run race fab and energy growth, the regime in which the trend was observed). Accrues only while max(A_fab, loop chip share) > 0.5 and max(A_en, loop energy share) > 0.5",
    spillover="every other bloc closes its gap to the leader's E at s_sp x (1 - 0.7 psi_leader) per year",
    caps="the bloc's total capability growth (actual shared-trend growth this step + dE/dt) is capped at min(15 doublings/yr, 30 x r0 slow corr): the existing 15/yr clamp and the 30x AI-R&D feedback cap applied to the bloc's own rate. No level cap on E: the shared trend's level caps (1e5-hour horizon ceiling, cognitive wall Lcap) bind the shared L only, so a compute-rich bloc can push past a cognitive wall; beyond the horizon ceiling extra doublings change little because Fcog and the physical-capability rate (kc term clamped at L_m3 + 8) are already saturated, except means availability (A8). Physical capability is capped at Lpcap",
    replaces="L_b + E replaces the shared capability in Fcog_b; Lp_b + Ep in Fp_b (hence F_tot, the greenfield gate, conversion ceilings, security automation and kinetic power Mk via k_am x automated security share x output, robot profitability prof_b); L + E in means availability (A8, dL_means). Kept shared (conservative): the AI learning-curve multiplier lc/ph3 on build rates and robot labor, the decision-lag speed-up spd, the economy-wide cognitive adoption rate (mat), the AI-R&D feedback multiplier, the capability milestones",
    timing="E is updated after the step's chip/energy capacity update and used from the next step; E at closure is recorded 0.25 y after closure",
)


# ---- WIDE PHYSICAL DOUBLING FLOORS UNDER AUTOMATION (wfl_on). A10: no precedent (robots building robots, AI doing all
# planning, design and coordination) means a wide range, not a low one, so the fast tails reach further; the slow tails
# (90th percentile) stay where they were. Implemented as a quantile map of the SAME standard-normal draw: with
# z = ln(x / old_median) / old_sigma recovered from the existing value, x_new = new_median x exp(new_sigma x z). No random
# stream moves; overrides (tornado) are mapped the same way (same quantile); the 1e9 sentinel of variant
# no_self_replication is left untouched. OFF by default. Evidence label J (A10). Td_mat unchanged.
# new_sigma = ln(p90 / p5_target) / (1.2816 + 1.6449), new_median = p90 / exp(1.2816 new_sigma)
WFL_SPEC = {   # name: (old median, old sigma, p5 target)
    "Td_mine_auto": (1.5, 0.45, 0.25),
    "Td_en_auto": (1.5, 0.45, 0.25),
    "Td_auto": (1.0, 0.6, 0.25),
    "fact_build_a": (0.5, 0.45, 0.10),
}
# automated fab doubling floor: Td_fab_auto = max(fab_build x fact_build_a / fact_build_h, 0.5) in the existing code
# (no separate automated fab build time exists; this derived build time IS the floor). Under wfl_on its raw value
# X = fab_build x fact_build_a(old) / fact_build_h is lognormal (median 2.5 x 0.5 / 1.2, sigma sqrt(.25^2 + .45^2 + .5^2)
# from the three existing draws); it is quantile-mapped to p90 unchanged, p5 = 0.25 y, and the 0.5 y clamp is dropped.
WFL_FAB = (2.5 * 0.5 / 1.2, float(np.sqrt(0.25 ** 2 + 0.45 ** 2 + 0.5 ** 2)), 0.25)
_Z90, _Z5, _Z95 = 1.2815516, -1.6448536, 1.6448536


def _wfl_new(med, sig, p5t):
    p90 = med * np.exp(_Z90 * sig)
    s2 = np.log(p90 / p5t) / (_Z90 - _Z5)
    return p90 / np.exp(_Z90 * s2), s2


def wfl_table():
    out = {}
    for k, (m, sg, t) in list(WFL_SPEC.items()) + [("Td_fab_auto", WFL_FAB)]:
        m2, s2 = _wfl_new(m, sg, t)
        q = lambda mm, ss, z: round(float(mm * np.exp(ss * z)), 3)
        old = dict(median=round(m, 3), p5=q(m, sg, _Z5), p90=q(m, sg, _Z90), p95=q(m, sg, _Z95), sigma=round(sg, 3))
        if k == "Td_fab_auto":
            old = dict(median=round(m, 3), p5=max(q(m, sg, _Z5), 0.5), p90=q(m, sg, _Z90), p95=q(m, sg, _Z95), sigma_raw=round(sg, 3),
                       note="old floor = max(raw, 0.5)")
        out[k] = dict(old=old, new=dict(median=round(float(m2), 3), p5=q(m2, s2, _Z5), p90=q(m2, s2, _Z90), p95=q(m2, s2, _Z95),
                                        sigma=round(float(s2), 3)), units="years", evidence="J (A10)")
    return out


GF_NOTE = dict(
    flag="gf_on (off by default). M8_FINAL=1 = final configuration (four final brakes + greenfield); M8_BRAKES=final = brakes only; M8_GF=1 = greenfield only; variant 'greenfield' turns it on in a single run",
    flaw="closure was modelled as converting the existing economy: the automated share of each core segment grows logistically from today's share under capacity-turnover caps (i_K, r_retro). A power center can instead build a NEW dedicated automated loop beside the economy, sized q_core x the full chain",
    state="ygf[bloc, segment] = automated capacity of the dedicated loop as a fraction of that segment's share of the minimal loop; starts at 0 (today's automated plants are not counted as dedicated)",
    build_limits=["mining/energy/chips: the loop takes the core_alloc share of the bloc's new domestic sector capacity, growing at the existing Gm/Ge/Gc rates (Td_*_base/race by psi, automated floors Td_mine_auto/Td_en_auto/Td_fab_auto (fab_build), switching with the sector's automation); new capacity x own / q",
                  "factory-type segments (manufacturing, logistics, construction, maintenance, admin): parallel build, online after the factory lead time (fact_build_h -> fact_build_a as the resource chain automates, A_rr blend as for bld), capped by the gross investment flow at core priority concentrated on the loop: i_K (1 + (i_boost - 1) core_alloc) / k_int x bld boost x capex-correction / q",
                  "security is not built by the loop: A3 security automation is shared (loop security = existing path)",
                  "capability gate: ygf <= F_tot (bloc, B6-lagged); cognitive share = existing core path acc (shared software automation, B6-lagged Fcog gate)",
                  "robots/kit: from the same supply; only automation not installed in the existing economy (supply - xf T_s), core_alloc share, after both conversion paths' security increments (A3 first call), and within room_c; the loop stock is then removed from both conversion paths' non-security room (no double counting); input pools mat_cap/chip_cap/hum_cap bound supply"],
    dependence="per segment: Dg = Dcs - (1 - CS)(phys_ex - (1 - ygf)/(1 - X0)), phys_ex = own (1 - xc)/(1 - X0) + (1 - own) hxu; security Dg = Dcs. D_loop = sum W_S Dg. With gf_on the core dependence everywhere downstream is min(Dcs, Dg) elementwise; closure when its W_S-weighted sum < trig (0.2)",
    new_priors="none; no new random draws",
)


def sample_params(N, rng, overrides=None, variant="baseline"):
    A = A_N
    p = {}

    def draw(spec):
        kind = spec[0]
        if kind == "lognormal":
            return spec[1] * np.exp(spec[2] * rng.standard_normal(N))
        if kind == "uniform":
            return rng.uniform(spec[1], spec[2], N)
        if kind == "beta":
            return rng.beta(spec[1], spec[2], N)
        if kind == "mix":        # evidence-weighted mixture: weight spec[1] on spec[2] (literature), rest on spec[3] (Jev)
            a_, b_ = draw(spec[2]), draw(spec[3])
            return np.where(rng.random(N) < spec[1], a_, b_)
        return np.full(N, float(spec[1]))
    for k, (spec, _, _) in PRIORS.items():
        p[k] = draw(spec)
    p["sw_cap0"] = np.clip(p["sw_cap0"], 0.04, 0.4)
    p["sw_prac0"] = np.clip(p["sw_prac0"], 0.01, 0.2)
    p["dx0"] = np.clip(p["dx0"], 0.01, 0.15)
    p["pg_red"] = np.clip(p["pg_red"], 0.1, 0.6)
    p["m_d"] = np.clip(p["m_d"], 0.0003, 0.01)
    p["ai_lc"] = np.clip(p["ai_lc"], 1.05, 2.0)
    p["adl"] = np.clip(p["adl"], 1.2, 10.0)
    p["fb_strength"] = np.clip(p["fb_strength"], 0.05, 2.0)
    p["OR_def"] = np.clip(p["OR_def"], 1.5, 10.0)
    p["C_oust"] = np.clip(p["C_oust"], 0.02, 3.0)
    p["p_id"] = np.clip(p["p_id"], 0.005, 0.25)
    p["p_nuc"] = np.clip(p["p_nuc"], 0.003, 0.1)
    p["w_mort"] = np.clip(p["w_mort"], 5e-5, 0.01)
    p["eco_mult"] = np.clip(p["eco_mult"], 1.1, 4.0)
    p["v1"] = np.where(rng.random(N) < 0.5, 0.0, p["v1"])
    p["eco_land"] = np.where(rng.random(N) < 0.5, 0.0, p["eco_land"])
    p["cog_wall"] = rng.random(N) < p["p_cog_wall"]
    p["phys_wall"] = rng.random(N) < p["p_phys_wall"]
    p["capex_corr"] = rng.random(N) < p["p_capex_correction"]
    p["corr_start"] = rng.uniform(2027.0, 2029.5, N)
    p["corr_len"] = rng.uniform(1.0, 3.0, N)
    p["fb_zero"] = rng.random(N) < p["fb_zero_mass"]
    p["cog_wall_frac"] = rng.uniform(0.3, 0.9, N)
    p["phys_wall_frac"] = rng.uniform(0.4, 0.8, N)
    p["t_leth"] = T0 + rng.exponential(1.0, (N, A)) / p["t_leth_rate"][:, None] * LETH_M[None, :]
    p["u_grab"] = rng.random((N, A))
    p["mem_z"] = rng.standard_normal((N, A, NMEM))
    p["mem_u_host"] = rng.random((N, A, NMEM))
    p["mem_zm"] = rng.standard_normal((N, A, NMEM))
    p["mem_u_ref"] = rng.random((N, A, NMEM))
    p["mem_zt"] = rng.standard_normal((N, A, NMEM))
    p["u_dem"] = rng.random((N, A))
    p["u_small"] = rng.random((N, A))
    p["wf_mult"] = np.exp(0.25 * rng.standard_normal((N, A)))
    p["g0_mult"] = np.exp(p["g0_mult_sd"][:, None, None] * rng.standard_normal((N, A, 9)))
    p["ep0"] = rng.random((N, A)) < P_EP0[None, :]
    p["nmin"] = rng.choice(NMIN_VALS, N, p=NMIN_P).astype(float)
    p["p_W_dem"] = rng.uniform(0.1, 0.5, N)
    p["sim_seed"] = rng.integers(0, 2 ** 31 - 1, N)
    # ---- review round 3 draws
    p["d_a"] = rng.uniform(D_A_LO[None], D_A_HI[None], (N, A))                 # F8 status-quo provision drift
    p["dm"] = rng.uniform(DM_LO[None], DM_HI[None], (N, A))                    # F8 displaced provision multiplier
    pp0 = np.zeros((N, A)); pp0[:, 1] = rng.beta(5, 5, N); pp0[:, 3] = rng.beta(7.5, 2.5, N)
    p["p_pers0"] = pp0                                                          # F1 entrenched autocracies start PERS
    ppb = rng.beta(5.5, 4.5, (N, A)); ppb[:, 0] = rng.beta(7, 3, N)
    p["p_pers_bd"] = ppb                                                        # F1 PERS after breakdown/grab
    p["u_reg"] = rng.random((N, A)); p["u_lead"] = rng.random((N, A))
    p["V_max"] = rng.integers(3, 6, (N, A)).astype(float)                       # F1 DEM veto players U{3,4,5}
    p["n_in"] = rng.integers(5, 10, (N, A)).astype(float)                       # F1 PERS inner circle 5-9
    p["mem_zc"] = rng.standard_normal((N, A, NMEM))                             # A6 control over automated force
    for k in ["loop_on", "dem_endog", "trends_on", "war_on", "id_on", "floors_on", "prof_on", "wh_mort_on",
              "persist_on", "rentier_on", "war_deaths_on",
              # review round 3 switches (True = fix/assumption active); variants revert one at a time
              "f1_rule", "f2_refuse", "f3_defect", "f5_metr", "f7_nocaps", "f8_sq", "a1_trend", "a2_prio",
              "a3_sec", "a11_esc", "a9_col", "a8_means", "a7_env", "a6_lev", "f6_kitcap", "f4_disp", "onset_cut"]:
        p[k] = np.ones(N, bool)
    p["dem_bar"] = np.zeros(N, bool)
    p["trig"] = np.full(N, 0.2)
    p["ruthless"] = np.zeros(N, bool)
    p["surv_on"] = np.ones(N)          # 1 = automated-surveillance deterrence active
    p["cp_scale"] = np.ones(N)         # collective-punishment regional-base multiplier
    if overrides:
        for k, v in overrides.items():
            if k in p:
                p[k] = np.full(np.shape(p[k]), float(v))
    v = variant
    # ---- review round 3: revert one fix/assumption at a time (effect of each fix on the headline)
    R3 = {"rev_F1_median_rule": "f1_rule", "rev_F2_refusal_v4": "f2_refuse", "rev_F3_no_defection": "f3_defect",
          "rev_F4_dispositions_v4": "f4_disp", "rev_F5_metr_coupled": "f5_metr", "rev_F6_kit_uncapped": "f6_kitcap",
          "rev_F7_caps_v4": "f7_nocaps", "rev_F8_warehouse_default": "f8_sq", "rev_A1_trend_breaks": "a1_trend",
          "rev_A2_priority_prior": "a2_prio", "rev_A3_security_lag": "a3_sec", "rev_A6_leverage_v4": "a6_lev",
          "rev_A7_env_off": "a7_env", "rev_A8_no_means": "a8_means", "rev_A9_no_collusion": "a9_col",
          "rev_A11_no_escalation": "a11_esc"}
    if v in R3:
        p[R3[v]][:] = False
    if v == "all_round2":            # every round-3 switch off (close to round 2 plus the endgame bookkeeping)
        for k in R3.values():
            p[k][:] = False
    if not p["f4_disp"].all():
        m = ~p["f4_disp"]
        p["p_hostile"] = np.where(m, rng.beta(1.2, 14.0, N), p["p_hostile"])
        p["alpha_med"] = np.where(m, 0.03 * np.exp(0.9 * rng.standard_normal(N)), p["alpha_med"])
        p["host_ins"] = np.where(m, rng.uniform(0.03, 0.15, N), p["host_ins"])
        p["v0"] = np.where(m, 0.01 * np.exp(0.9 * rng.standard_normal(N)), p["v0"])
        p["m_pow"] = np.where(m, 1.0, p["m_pow"])
    if not p["f2_refuse"].all():
        m = ~p["f2_refuse"]; b33 = rng.beta(3.0, 3.0, N)
        for k in ["p_ref_dem", "p_ref_olig", "p_ref_pers"]:
            p[k] = np.where(m, b33, p[k])
        p["r_neg"] = np.where(m, 1.0, p["r_neg"]); p["h_purge"] = np.where(m, 1e6, p["h_purge"])
    if not p["f3_defect"].all():
        p["p_exec"] = np.where(~p["f3_defect"], rng.uniform(0.7, 0.95, N), p["p_exec"])
    if not p["a1_trend"].all():
        p["fb_zero_mass"] = np.where(~p["a1_trend"], 0.25, p["fb_zero_mass"])
        p["fb_strength"] = np.where(~p["a1_trend"], np.minimum(0.5 * np.exp(0.5 * rng.standard_normal(N)), 1.5), p["fb_strength"])
        p["fb_zero"] = np.where(~p["a1_trend"], rng.random(N) < 0.25, p["fb_zero"])
    if v in ("loop_off", "v3_like"):
        p["loop_on"][:] = False
    if v in ("democracy_bar", "v3_like"):
        p["dem_bar"][:] = True; p["dem_endog"][:] = False
    if v in ("slow_physical", "v3_like"):
        p["g_ramp"] = np.full(N, 0.15); p["Td_mine_race"] = 6.0 * np.exp(0.35 * rng.standard_normal(N))
        p["Td_fab_race"] = np.full(N, 3.5); p["ai_lc"] = np.ones(N); p["adl"] = np.ones(N)
        p["prof_on"][:] = False; p["humanoid_mult"] = p["humanoid_mult"] * 0.85; p["r_retro_p"] = np.full(N, 0.08)
    if v in ("no_trends", "v3_like"):
        p["trends_on"][:] = False
    if v == "v3_like":
        p["war_on"][:] = False; p["id_on"][:] = False; p["wh_mort_on"][:] = False
    if v == "quiet_world":
        p["loop_on"][:] = False; p["war_on"][:] = False; p["id_on"][:] = False
    if v == "no_war":
        p["war_on"][:] = False
    elif v == "no_war_deaths":
        p["war_deaths_on"][:] = False
    elif v == "no_ideology":
        p["id_on"][:] = False
    elif v == "no_warehouse_mortality":
        p["wh_mort_on"][:] = False
    elif v == "revolt_scaled_by_survivors":
        p["onset_cut"][:] = False
    elif v == "no_self_replication":
        p["Td_auto"] = np.full(N, 1e9); p["Td_mat"] = np.full(N, 1e9)
    elif v == "trend_breaks":                 # A1 trend break only: compute slowdown after 2029.5 (A1 feedback prior kept)
        p["a1_trend"][:] = False
    elif v == "no_ai_rd_feedback":
        p["fb_zero"][:] = True
    elif v == "single_decider":
        p["nmin"] = np.full(N, 1.0); p["p_small"] = np.ones(N)
    elif v == "coalition_floor_21":
        p["p_small"] = np.zeros(N)
    elif v == "low_inertia_v4r1":             # round-1 ratchet: cheap switching, no confirmation
        p["s_sw"] = np.full(N, 0.1); p["persist_on"][:] = False; p["p_exec"] = np.ones(N)
    elif v == "no_rentier":
        p["rentier_on"][:] = False
    elif v == "repression_deters":
        p["rd"] = np.full(N, 0.85); p["k_auto"] = np.full(N, 0.9); p["k_bf"] = np.full(N, 0.1); p["dfd"] = np.full(N, 0.7)
    elif v == "high_grievance":
        p["p_svr_hi"] = np.full(N, 0.5); p["p_svr_weak"] = np.full(N, 0.7); p["mdisp"] = np.full(N, 2.2)
        p["pg_red"] = np.full(N, 0.1); p["pr_red"] = np.full(N, 0.3)
    elif v == "low_grievance":
        p["p_svr_hi"] = np.full(N, 0.15); p["p_svr_weak"] = np.full(N, 0.35); p["mdisp"] = np.full(N, 1.2)
        p["pg_red"] = np.full(N, 0.6); p["pr_red"] = np.full(N, 0.7)
    elif v == "strong_leverage_effect":
        p["M_lev"] = np.full(N, 15.0)
    elif v == "weak_leverage_effect":
        p["M_lev"] = np.full(N, 2.0)
    elif v == "trigger_Dcore_0.5":
        p["trig"][:] = 0.5
    elif v == "skeptic_combo":
        # skeptic review's structural set: inertia, surveillance deterrence x0.3, small collective punishment,
        # low despair mortality, execution success 0.8, coalition >=21, low ideology, slower build-out
        p["s_sw"] = np.full(N, 1.5); p["d_surv"] = np.full(N, 0.3); p["cp_scale"] = np.full(N, 0.5)
        p["m_d"] = np.full(N, 0.001); p["p_exec"] = np.full(N, 0.8); p["p_small"] = np.zeros(N)
        p["p_id"] = np.full(N, 0.02); p["v1"] = np.zeros(N); p["eco_land"] = np.zeros(N); p["M_lev"] = np.full(N, 2.0)
        p["p_svr_hi"] = np.full(N, 0.15); p["rd"] = np.full(N, 0.8); p["p_lcp"] = np.full(N, 0.15)
        p["g_ramp"] = np.full(N, 0.3); p["e_att"] = np.full(N, 0.3)
    elif v == "pessimist_combo":
        p["nmin"] = np.full(N, 1.0); p["p_small"] = np.ones(N); p["ruthless"][:] = True; p["M_lev"] = np.full(N, 15.0)
        p["p_svr_hi"] = np.full(N, 0.5); p["p_lcp"] = np.full(N, 0.6); p["m_d"] = np.full(N, 0.006)
        p["p_id"] = np.full(N, 0.15); p["g_ramp"] = np.full(N, 0.8); p["trig"][:] = 0.5; p["s_sw"] = np.full(N, 0.1)
        p["p_exec"] = np.full(N, 0.95); p["e_att"] = np.full(N, 0.7); p["pg_red"] = np.full(N, 0.1)
    # ---- ROUND 3 draws (after every round-2 draw; see PRIORS_B)
    for k, (spec, _, _) in PRIORS_B.items():
        if k not in p:
            p[k] = draw(spec)
    p["k_am"] = np.clip(p["k_am"], 1.5, 100.0)
    p["mem_zh"] = rng.standard_normal((N, A, NMEM))     # B2: control of human coercive/patronage networks
    p["lag_cog"] = rng.uniform(LAGC_LO[None], LAGC_HI[None], (N, A)); p["lag_phys"] = rng.uniform(LAGP_LO[None], LAGP_HI[None], (N, A))
    for k in ["b1_top", "b2_cons", "b3_enf", "b4_ret", "b5_xb", "b6_wire", "b8_dummy"]:
        p[k] = np.ones(N, bool)
    p["force_single"] = np.zeros(N, bool)
    p["b2_refill"] = np.zeros(N, bool)          # audit variant: purged seats are refilled by appointees without own force
    if overrides:
        for k, ov in overrides.items():
            if k in PRIORS_B:
                p[k] = np.full(np.shape(p[k]), float(ov))
    RB = {"rev_B1_average_moral": "b1_top", "rev_B2_fixed_consolidation": "b2_cons", "rev_B3_unenforced_stigma": "b3_enf",
          "rev_B4_no_retribution": "b4_ret", "rev_B5_no_cross_bloc": "b5_xb", "rev_B6_caps_bypassed": "b6_wire"}
    if v in RB:
        p[RB[v]][:] = False
    if v in ("round2_exact", "all_round2"):
        for k in RB.values():
            p[k][:] = False
    if v == "b2_no_purges":
        p["k_prg"] = np.zeros(N)
    if v == "b2_refill":
        p["b2_refill"][:] = True
    if v in ("single_decider", "pessimist_combo"):
        p["force_single"][:] = True
    if v == "f6_caps_forced":            # B6 test: physical input caps forced to bind (world robot-input pools / 10)
        p["M0"] = p["M0"] * 0.1; p["C0"] = p["C0"] * 0.1; p["Pmax_h"] = p["Pmax_h"] * 0.1
    if v == "f6_caps_forced_x100":
        p["M0"] = p["M0"] * 0.01; p["C0"] = p["C0"] * 0.01; p["Pmax_h"] = p["Pmax_h"] * 0.01
    if v == "f6_caps_forced_x100_qcore4":   # audit: same, with a 4x larger minimal core loop (q_core is a 'very low' evidence prior)
        p["M0"] = p["M0"] * 0.01; p["C0"] = p["C0"] * 0.01; p["Pmax_h"] = p["Pmax_h"] * 0.01; p["q_core"] = p["q_core"] * 4.0
    if v == "no_nuclear_deterrent":
        p["p_ret0"] = np.zeros(N)
    # ---- BRAKES: separate stream (see PRIORS_BRK); nothing above consumes it, so every existing draw is unchanged
    rng_b = np.random.default_rng(np.random.SeedSequence([int(x) for x in np.asarray(p["sim_seed"]).ravel()] + [0xB7A4E5]))
    spec_b = {k: s for k, (s, _, _) in PRIORS_BRK.items()}
    for k, spec in spec_b.items():
        kind = spec[0]
        if kind == "lognormal":
            p[k] = spec[1] * np.exp(spec[2] * rng_b.standard_normal(N))
        else:
            p[k] = rng_b.uniform(spec[1], spec[2], N)
    p["p_pid"] = np.clip(p["p_pid"], 0.005, 0.25)
    p["k_pid"] = np.clip(p["k_pid"], 0.05, 20.0)
    p["c_selfrisk"] = np.clip(p["c_selfrisk"], 0.02, 5.0)
    p["mem_u_sx"] = rng_b.random((N, A, NMEM))          # brake 2: per-member exemption draw (exempt if < e_ex)
    p["b_id"] = rng_b.uniform(0.0, 0.4, N)
    p["m_dis"] = np.clip(4.0 * np.exp(0.8 * rng_b.standard_normal(N)), 1.0, 30.0)
    for k in list(BRK_FLAGS) + ["pid_noselm"]:
        p[k] = np.zeros(N, bool)
    if overrides:
        for k, ov in overrides.items():
            if k in PRIORS_BRK or k in PRIORS_BRK2:
                p[k] = np.full(N, float(ov))
    if v in ("brake_pid", "brakes_all", "brake_pid_noselm"):
        p["pid_on"][:] = True
    if v == "brake_pid_noselm":                  # sensitivity: doctrine part exempt from the sel_top scaling
        p["pid_noselm"][:] = True
    if v in ("brake_selfrisk", "brakes_all", "brake_selfrisk_dis", "brakes_all_dis", "brakes_final"):
        p["sr_on"][:] = True
    if v in ("brake_selfrisk_dis", "brakes_all_dis", "brakes_final"):
        p["dis_on"][:] = True
    if v in ("brake_mort", "brakes_all", "brakes_all_dis", "brakes_final"):
        p["brk_mort"][:] = True
    if v in ("brakes_all_dis", "brakes_final"):
        p["pid_on"][:] = True
    # single switch: M8_BRAKES=final turns the final brake configuration on for every variant (main run, structural
    # variants, lever model). Unset (default) = all brakes off = the published baseline
    if os.environ.get("M8_BRAKES", "") == "final":
        for k in ["pid_on", "sr_on", "dis_on", "brk_mort"]:
            p[k][:] = True
    elif os.environ.get("M8_BRAKES", "") not in ("", "off"):
        raise ValueError("M8_BRAKES must be unset, 'off' or 'final'")
    # ---- GREENFIELD CORE LOOP (gf_on; see the GREENFIELD block in _sim_chunk). A pure structural switch: no new prior
    # and no new random draw (the loop size is the existing q_core, the build limits are existing priors), so neither
    # numpy stream is touched. OFF by default. Switches:
    #   variant "greenfield"            -> gf_on (with whatever brakes the variant/env sets)
    #   M8_GF=1                         -> gf_on in every variant
    #   M8_FINAL=1                      -> FINAL CONFIGURATION: the four final brakes (pid_on, sr_on, dis_on, brk_mort)
    #                                      plus gf_on plus cf_on (compute feedback) plus wfl_on (wide floors). M8_BRAKES=final keeps its old meaning (brakes
    #                                      only, greenfield off) so the brakes-on/greenfield-off run still reproduces.
    p["gf_on"] = np.zeros(N, bool)
    if v in ("greenfield", "brakes_final_gf", "greenfield_cf"):
        p["gf_on"][:] = True
    if v == "brakes_final_gf":
        for k in ["pid_on", "sr_on", "dis_on", "brk_mort"]:
            p[k][:] = True
    if os.environ.get("M8_GF", "") == "1":
        p["gf_on"][:] = True
    # ---- OWN-INDUSTRY COMPUTE FEEDBACK: own numpy stream, drawn after every existing draw (see PRIORS_CF)
    rng_c = np.random.default_rng(np.random.SeedSequence([int(x) for x in np.asarray(p["sim_seed"]).ravel()] + [0xCF0B5E]))
    p["eta_cf"] = rng_c.uniform(0.5, 1.5, N)
    p["s_sp"] = rng_c.uniform(0.1, 0.5, N)
    if overrides:
        for k, ov in overrides.items():
            if k in PRIORS_CF:
                p[k] = np.full(N, float(ov))
    p["cf_on"] = np.zeros(N, bool)
    if v in ("computefb", "greenfield_cf"):
        p["cf_on"][:] = True
    if os.environ.get("M8_CF", "") == "1":
        p["cf_on"][:] = True
    # ---- WIDE FLOORS flag (see WFL_SPEC)
    p["wfl_on"] = np.zeros(N, bool)
    if v in ("widefloors", "greenfield_cf_wfl"):
        p["wfl_on"][:] = True
    if v == "greenfield_cf_wfl":
        p["gf_on"][:] = True; p["cf_on"][:] = True
    if os.environ.get("M8_WFL", "") == "1":
        p["wfl_on"][:] = True
    if os.environ.get("M8_FINAL", "") == "1":      # final configuration: brakes + greenfield + compute feedback + wide floors
        for k in ["pid_on", "sr_on", "dis_on", "brk_mort", "gf_on", "cf_on", "wfl_on"]:
            p[k][:] = True
    # automated fab floor under wide floors, from the existing draws (computed always, used only when wfl_on)
    mf, sf, tf = WFL_FAB
    zf = np.log(p["fab_build"] * p["fact_build_a"] / p["fact_build_h"] / mf) / sf
    m2f, s2f = _wfl_new(mf, sf, tf)
    p["Td_fab_auto_w"] = m2f * np.exp(s2f * zf)
    w = p["wfl_on"]
    if w.any():
        for k, (m, sg, t) in WFL_SPEC.items():
            m2, s2 = _wfl_new(m, sg, t)
            x = p[k]
            z = np.log(np.maximum(x, 1e-12) / m) / sg
            p[k] = np.where(w & (x < 1e8), m2 * np.exp(s2 * z), x)
    elif os.environ.get("M8_FINAL", "") not in ("", "0"):
        raise ValueError("M8_FINAL must be unset, '0' or '1'")
    p["dis_on"] = p["dis_on"] & p["sr_on"]      # dissent risk exists only inside Brake 2
    if not (p["id_on"].all()):                   # note step 3: pid_on off in every variant that turns id_on off
        p["pid_on"] = p["pid_on"] & p["id_on"]
    # derived
    h80r = p["h50_0"] / p["h80_ratio"] / p["mess"]
    # F5: the task-difficulty spread is fixed by the doubling observed in the z_rate window (METR_OBS), not by the
    # sampled future doubling time; round 2 tied both, so a faster doubling flattened the capability curve
    p["s_task"] = LN2 * 12.0 / np.where(p["f5_metr"], METR_OBS, p["metr_doubling_months"]) / p["z_rate"]
    mu_sw = np.log(h80r) - p["s_task"] * ndtri(p["sw_cap0"])
    lnh_m3 = mu_sw + p["s_task"] * ndtri(SW_THR["M3"])
    se = p["k_ec"] * p["s_task"]
    mu_ec = np.log(h80r) - se * ndtri(np.minimum(p["Fcog0"] / 0.95, 0.99))
    p["Np"] = -sp_logit(p["dx0"])                      # logit units from 2026 to DEX (dx = 0.5)
    p["sw_auto0"] = p["sw_cap0"]
    p["ac_horizon_hours"] = np.exp(lnh_m3) * p["mess"] * p["h80_ratio"]
    p["F_ac"] = 0.95 * ndtr((lnh_m3 - mu_ec) / se)
    p["tau_phys"] = 1.0 / p["g_ramp"]
    p["g_h"] = np.log(p["humanoid_mult"])
    p["tau_cog"] = 1.0 / p["g_cog_max"]
    p["Td_mine_h"] = p["Td_mine_race"]; p["Td_fab_h"] = p["Td_fab_race"]
    return p


# ============================================================================================
# simulation (torch)
# ============================================================================================
_TORCH = None


def get_torch():
    global _TORCH
    if _TORCH is None:
        import torch
        _TORCH = torch
    return _TORCH


def pick_device(force_cpu=False):
    torch = get_torch()
    if force_cpu or os.environ.get("M8_CPU") == "1" or not torch.cuda.is_available():
        return torch.device("cpu")
    return torch.device("cuda")


def _sim_chunk(p, N, dev, seed, block=None, records=True):
    torch = get_torch()
    F32 = torch.float32; F64 = torch.float64; INF = float("inf")
    A, S, K = A_N, 9, 6
    g = torch.Generator(device=dev); g.manual_seed(int(seed))
    reps = 1 if block is None else N // block
    nb = N if block is None else block

    def rnd(*shape):
        x = torch.rand((nb,) + shape, generator=g, device=dev)
        return x if reps == 1 else x.repeat((reps,) + (1,) * len(shape))

    def rn(*shape):
        x = torch.randn((nb,) + shape, generator=g, device=dev)
        return x if reps == 1 else x.repeat((reps,) + (1,) * len(shape))

    def T(x, dt=F32):
        return torch.as_tensor(np.asarray(x), dtype=dt, device=dev)
    P = {}
    for k, v in p.items():
        if isinstance(v, np.ndarray):
            P[k] = torch.as_tensor(v, device=dev) if v.dtype == bool else torch.as_tensor(v, dtype=F32, device=dev)
    nd, ndi = torch.special.ndtr, torch.special.ndtri
    W_S_ = T(W_S); CS_ = T(CS); X0b = T(X0).expand(N, A, S); K_RESH_ = T(K_RESH)
    DMAX_ = T(DMAX); BASE_PROV_ = T(BASE_PROV); PROV_ = T(PROV_INT)
    aidx = torch.arange(A, device=dev)
    ENT = T(ENTRENCHED, torch.bool)
    loop = P["loop_on"][:, None]; trends = P["trends_on"]
    zeroNA = torch.zeros(N, A, device=dev)
    # ---------------- cognitive
    h80r0 = P["h50_0"] / P["h80_ratio"] / P["mess"]
    st = P["s_task"]; se = P["k_ec"] * st; sr = P["k_rnd"] * st
    mu_sw = torch.log(h80r0) - st * ndi(P["sw_cap0"])
    mu_rnd = torch.log(h80r0) - sr * ndi(P["rnd0"])
    mu_ec = torch.log(h80r0) - se * ndi(torch.clamp(P["Fcog0"] / 0.95, max=0.99))
    L_m3 = torch.clamp((mu_sw + st * float(ndtri(0.9)) - torch.log(h80r0)) / LN2, min=0.5)
    L = torch.zeros(N, device=dev)
    r0 = 12.0 / P["metr_doubling_months"]
    fb = torch.where(P["fb_zero"], 0.0, P["fb_strength"])
    Lmax = torch.log2(1e5 / h80r0)                       # horizon cap: 1e5 h, about a career
    Lcap = torch.minimum(torch.where(P["cog_wall"], P["cog_wall_frac"] * L_m3, 60.0), Lmax)
    tm = {k: torch.full((N,), INF, device=dev) for k in ["M2", "M3", "M2p", "M3p", "M4", "M5", "M6", "M7"]}
    prac = torch.minimum(P["sw_prac0"], P["sw_cap0"])
    a0c = torch.minimum(P["a_cog0"], 0.5 * P["Fcog0"])[:, None, None].expand(N, A, S).clone()
    acf = a0c.clone(); acc = a0c.clone()
    # ---------------- physical capability (logit of the dx measure)
    Lp = torch.zeros(N, device=dev); Np = P["Np"]; ldx0 = torch.logit(P["dx0"])
    Lpcap = torch.where(P["phys_wall"], P["phys_wall_frac"] * Np, 3 * Np)
    Fp0 = torch.clamp(T(FP0)[None] * P["Fp_scale"][:, None], 0.01, 0.6)
    lFp0 = torch.logit(Fp0)
    t_dex = torch.full((N,), INF, device=dev)
    # ---------------- physical automation state
    own = T(OWN0).expand(N, A, S).clone()
    Wk = T(WORKFORCE)[None] * P["wf_mult"]
    need_s = Wk[:, :, None] * W_S_ * (1 - CS_)
    need_tot = need_s.sum(-1)
    T_s = need_s / (1 - X0b)
    xf = X0b.clone(); xc = X0b.clone()
    kit0 = (X0b * T_s).sum(-1); kit = kit0.clone()
    g0 = T(G0)[None] * P["g0_mult"]
    prod = GLOBAL_PROD0 * T(ROBOT_SHARE0)[None] * P["prod_use"][:, None]
    Rst = GLOBAL_STOCK0 * T(ROBOT_SHARE0)[None] * P["prod_use"][:, None]
    Gm = torch.ones(N, A, device=dev); Gc = Gm.clone(); Ge = Gm.clone()
    re_share = T(RE_SHARE0).expand(N, A).clone(); chip_share = T(CHIP_SHARE0).expand(N, A).clone()
    n_sr = zeroNA.clone()
    psi0 = torch.cat([P["psi0_US"][:, None], P["psi0_CN"][:, None],
                      torch.clamp(P["psi0_RW"][:, None] * T(PSI_ROW_M)[None], max=0.9)], 1)
    # A2: physical automation is the top national priority in the US and China from 2026
    psi0 = torch.where(P["a2_prio"][:, None] & (aidx[None] < 2), torch.ones_like(psi0), psi0)
    psi = psi0.clone()
    Td_fab_auto = torch.clamp(P["fab_build"] * P["fact_build_a"] / P["fact_build_h"], min=0.5)
    if bool(P["wfl_on"].any()):      # WIDE FLOORS: quantile-mapped automated fab floor, no 0.5 y clamp (see WFL_FAB)
        Td_fab_auto = torch.where(P["wfl_on"], P["Td_fab_auto_w"], Td_fab_auto)
    # ---------------- democracy / regime
    Ddem = T(D0).expand(N, A).clone()
    free = Ddem < D_BREAK
    in_ep = P["ep0"] & ~free
    grabbed = torch.zeros(N, A, dtype=torch.bool, device=dev)
    grab_cum = zeroNA.clone(); t_grab = torch.full((N, A), INF, device=dev)
    t_break = torch.where(free, T0, INF)
    ep_len0 = 0.27 / P["e_rate"]
    hb = (P["h_bd"] / (1 - P["p_uturn"]))[:, None]
    h_on_a = torch.where(T([1, 1, 1, 0, 0, 0], torch.bool)[None], hb, P["h_on"][:, None])
    lam_r0 = -torch.log(1 - P["p_uturn"]) / ep_len0
    # ---------------- grievance loop
    hic = T(HI_CAP)[None]
    Gv = torch.full((N, A), 0.39, device=dev)
    BF = zeroNA.clone(); DF = zeroNA.clone()
    Iact = torch.zeros(N, A, dtype=torch.bool, device=dev)
    ins_years = zeroNA.clone(); n_ins = zeroNA.clone(); t_ins1 = torch.full((N, A), INF, device=dev)
    n_lcp = zeroNA.clone(); t_lcp1 = torch.full((N, A), INF, device=dev); n_suc = zeroNA.clone(); n_suc_aut = zeroNA.clone()
    prov_floor_until = torch.full((N, A), -INF, device=dev)
    p_svr = hic * P["p_svr_hi"][:, None] + (1 - hic) * P["p_svr_weak"][:, None]
    lam_ref = -torch.log(1 - p_svr) / 10.0
    lam0 = torch.exp(hic * torch.log(P["lam0_hi"])[:, None] + (1 - hic) * torch.log(P["lam0_weak"])[:, None])
    H_ref = P["h_beh0"] * P["mdisp"] ** 3 * (1 - P["pr_red"] * 0.2)          # hostility at the calibration point
    amp_ref = 1 + P["k_ineq"] * 0.4
    G_ref = 1 - 0.61 * (1 - torch.clamp(0.3 * amp_ref * (1 - P["pg_red"] * 0.2), 0, 1))

    f7 = P["f7_nocaps"][:, None]

    def hsat(hr):
        # F7: saturation of the ABSOLUTE behavioral hostile share at Habs (round 2: relative Hmax); returns H_eff / H_ref
        hm = P["Hmax"][:, None]
        rel = hm * hr / (hm + hr - 1)
        Ha = P["Habs"][:, None]; Hab = hr * H_ref[:, None]
        return torch.where(f7, Ha * Hab / (Ha + Hab) / H_ref[:, None], rel)
    H0 = P["h_beh0"][:, None] * (1 - P["pr_red"][:, None] * BASE_PROV_[None]) * (0.39 / G_ref[:, None]) ** P["e_g"][:, None]
    Hr0e = hsat(H0 / H_ref[:, None])
    # ---- review round 3 state
    a7 = P["a7_env"]
    Psq0 = BASE_PROV_[None].expand(N, A)
    init_aut = T(D0 < D_BREAK, torch.bool)
    regime_pers = (P["u_reg"] < P["p_pers0"]) & init_aut[None]      # F1: entrenched autocracies may start personalist
    def_until = torch.full((N, A), -INF, device=dev)
    exec_on = torch.zeros(N, A, dtype=torch.bool, device=dev); t_exec = torch.full((N, A), INF, device=dev)
    tot = torch.zeros(N, A, dtype=torch.bool, device=dev); tgt = zeroNA.clone()
    col_on = torch.zeros(N, A, dtype=torch.bool, device=dev)
    t_esc = torch.full((N, A), INF, device=dev); t_means = t_esc.clone(); t_col = t_esc.clone(); t_nx = t_esc.clone()
    t_captive = t_esc.clone(); tot_ever = torch.zeros(N, A, dtype=torch.bool, device=dev)
    rem = P["rem"][:, None].double()
    col_ok = P["a9_col"] & (P["b_col"] > (1 - P["s_bunk"]) * P["p_nx"] * P["c_self"])     # A9: rulers' own-survival calculus
    thr_means = None
    beta = torch.clamp(torch.log(lam_ref / lam0) / torch.clamp(torch.log(1 / Hr0e), min=0.1), 0.5, 3.5)

    def freg(D):
        return 1 + P["aU"][:, None] * 4 * D * (1 - D) - P["elec"][:, None] * D
    freg0 = freg(T(D0)[None].expand(N, A))
    # ---------------- wars, ideology
    war_until = torch.full((N, A), -INF, device=dev)
    war_until[:, 3] = T0 + P["ukr_rem"]                   # Russia-Ukraine war ongoing (baseline)
    n_war = zeroNA.clone(); t_war1 = torch.full((N, A), INF, device=dev); t_nuc = torch.full((N, A), INF, device=dev)
    ideol = torch.zeros(N, A, dtype=torch.bool, device=dev); id_lev = zeroNA.clone(); t_id = torch.full((N, A), INF, device=dev)
    lam_idc = -torch.log(1 - P["p_id"]) / 9.0
    # BRAKE 1: protective doctrine (mirror of ideol / id_lev)
    pideol = torch.zeros(N, A, dtype=torch.bool, device=dev); pid_lev = zeroNA.clone()
    lam_pidc = -torch.log(1 - P["p_pid"]) / 9.0
    pid_on = P["pid_on"][:, None]
    # ---------------- loss accounting (float64)
    z64 = torch.zeros(N, A, dtype=F64, device=dev)
    loss = z64.clone(); lc_neg = z64.clone(); lc_act = z64.clone(); lc_att = z64.clone(); lc_war = z64.clone()
    loss_wh = z64.clone(); lc_col = z64.clone()
    tL_tot = torch.full((N, A, len(LOSS_THR)), INF, device=dev); tL_del = tL_tot.clone()
    thr = [0.5, 0.2, 0.05]
    t_core = torch.full((N, A, 3), INF, device=dev); t_full = t_core.clone()
    t_closed = torch.full((N, A), INF, device=dev)
    free_at_dec = torch.zeros(N, A, dtype=torch.bool, device=dev); Ddem_at_dec = torch.full((N, A), float("nan"), device=dev)
    ins_at_dec = free_at_dec.clone(); id_at_dec = free_at_dec.clone(); war_at_dec = free_at_dec.clone()
    t_first_harsh = torch.full((N, A), INF, device=dev)
    choice = torch.full((N, A), -1, dtype=torch.long, device=dev); first_choice = choice.clone(); prev_pref = choice.clone()
    t_first_dec = torch.full((N, A), INF, device=dev)
    t_X = torch.full((N, A), INF, device=dev); n_xfail = zeroNA.clone(); cool_until = torch.full((N, A), -INF, device=dev)
    t_S5 = torch.full((N, A), INF, device=dev); ch_S5 = torch.full((N, A), -1, dtype=torch.long, device=dev)
    t_S5d = t_S5.clone(); ch_S5d = ch_S5.clone()
    ever = torch.zeros(N, A, K, dtype=torch.bool, device=dev)
    wh_years = zeroNA.clone()
    X_ins = free_at_dec.clone(); X_war = free_at_dec.clone(); X_id = free_at_dec.clone(); X_free = free_at_dec.clone()
    alpha_mag = P["alpha_med"][:, None, None] * torch.exp(P["alpha_sig"][:, None, None] * P["mem_z"])
    moral_base = P["moral_med"][:, None, None] * torch.exp(1.2 * P["mem_zm"])
    theta_i = torch.exp(0.5 * P["mem_zt"])
    small = (P["u_small"] < P["p_small"][:, None]) & ENT[None]
    n_small = torch.where(small, P["nmin"][:, None].long(), 21)
    memidx = torch.arange(NMEM, device=dev)
    # internal order: serve, rentier, status_quo, warehouse, neglect, depopulate
    PIK = T([0.0, 0.05, 0.02, 0.1, 0.3, 1.0]); LANDK = T([0.0, 0.0, 0.0, 0.6, 0.8, 1.0])
    ctl_w = torch.exp(P["conc_k"][:, None, None] * P["mem_zc"])          # A6: control over automated kinetic force
    ew = WORLD_W[None, :] * (1 - np.eye(A)); ew = ew / ew.sum(1, keepdims=True); exp_w = T(ew)
    press = torch.ones(N, A, device=dev)
    ny = len(YEARS) if records else 1
    rec = {k: torch.zeros(N, ny, device=dev) for k in ["Dlead_core", "Dlead_full", "fcog", "sw", "swp", "rnd", "hreal", "dx"]}
    recA = {k: torch.zeros(N, A, ny, device=dev) for k in ["Dc", "Df", "disp", "Gv", "H", "I", "Ddem", "free", "loss",
                                                             "prod", "war", "prov", "lamon",
                                                             "ncoal", "SL", "Mk", "enf"]}
    xseg = torch.zeros(N, A, S, ny, device=dev)
    yi = 0
    Dc_prev = torch.ones(N, A, device=dev); Dcs = torch.ones(N, A, S, device=dev)
    RR = torch.tensor(RR_SEG, device=dev); SAi = torch.tensor(SA_SEG, device=dev)
    WROW = T(WROW_M)[None]; NUC = T(NUC_ARMED)[None]
    adm = torch.ones(S, device=dev); adm[8] = 1 / 1.5
    wsc = W_S_ * (1 - CS_)
    k5 = torch.arange(K, device=dev)
    rent_ok = P["rentier_on"]
    # ================= ROUND 3 (B1-B6) state. Separate random stream (g2) so the round-2 stream is untouched =====
    g2 = torch.Generator(device=dev); g2.manual_seed(int(seed) + 7919)

    def rnd2(*shape):
        x = torch.rand((nb,) + shape, generator=g2, device=dev)
        return x if reps == 1 else x.repeat((reps,) + (1,) * len(shape))
    # ================= BRAKES state. Own random stream (g3) so the round-2 (g) and round-3 (g2) streams are untouched
    g3 = torch.Generator(device=dev); g3.manual_seed(int(seed) + 104729)

    def rnd3(*shape):
        x = torch.rand((nb,) + shape, generator=g3, device=dev)
        return x if reps == 1 else x.repeat((reps,) + (1,) * len(shape))
    sr_on = P["sr_on"][:, None]; mort_on = P["brk_mort"][:, None]
    sr_any = bool(P["sr_on"].any()); mort_any = bool(P["brk_mort"].any()); dis_any = bool(P["dis_on"].any())
    dis_on = P["dis_on"][:, None]
    # dissent-risk draws (failed-veto punishment) use their own generator g4, so g3 (brakes 1 and 3) is unchanged
    g4 = torch.Generator(device=dev); g4.manual_seed(int(seed) + 130363)

    def rnd4(*shape):
        x = torch.rand((nb,) + shape, generator=g4, device=dev)
        return x if reps == 1 else x.repeat((reps,) + (1,) * len(shape))
    n_dpun = zeroNA.clone(); n_dis_dec = zeroNA.clone(); n_dis_netneg = zeroNA.clone(); n_dis_expo = zeroNA.clone()
    sum_dis_net = zeroNA.clone(); n_dis_flip = zeroNA.clone(); n_dis_restore_harsh = zeroNA.clone(); n_dis_restoreX = zeroNA.clone()
    n_dis_memback = zeroNA.clone()
    # ================= GREENFIELD CORE LOOP state (gf_on). No random numbers are used, so no generator is needed and
    # every existing stream (g, g2, g3, g4) is untouched. ygf[n, a, s] = automated capacity of the bloc's DEDICATED loop
    # in segment s, as a fraction of that segment's share of the minimal loop (the loop is q_core x the full chain, so
    # its segment s needs q x T_s worker-equivalents of task capacity). It starts at 0 (conservative: today's automated
    # plants are not counted as already dedicated to the loop; they stay in the conversion path).
    gf_any = bool(P["gf_on"].any())
    gf = P["gf_on"][:, None]; gf3 = P["gf_on"][:, None, None]
    ygf = torch.zeros(N, A, S, device=dev)
    Rg = zeroNA.clone()                                       # loop's robot/kit stock (worker-equivalents)
    t_cl_conv = torch.full((N, A), INF, device=dev); t_cl_gf = t_cl_conv.clone()   # each path alone crossing trig
    n_gf_build = zeroNA.clone(); n_gf_rob = zeroNA.clone()   # steps the loop was building / was robot-limited
    n_gf_gate = zeroNA.clone()                               # building steps with the loop at >= 98% of the capability gate
    FAC_SEG = torch.tensor([3, 4, 5, 6, 8], device=dev)       # 'factory-type' segments (built with factory lead times)
    no_sec = torch.ones(S, device=dev); no_sec[7] = 0.0       # security is NOT built by the loop (A3, shared)
    recA["Dloop"] = torch.zeros(N, A, ny, device=dev); recA["Dconv"] = torch.zeros(N, A, ny, device=dev)   # gf only
    # ================= OWN-INDUSTRY COMPUTE FEEDBACK state (cf_on). Deterministic: no generator used.
    cf_any = bool(P["cf_on"].any())
    cf = P["cf_on"][:, None]; cf3 = P["cf_on"][:, None, None]
    Ecf = zeroNA.clone(); Epf = zeroNA.clone()               # extra cognitive doublings / extra physical logit per bloc
    lnC_prev = zeroNA.clone()                                 # ln of own compute capacity (2026 = 1)
    chip0_cf = T(CHIP_SHARE0 / CHIP_SHARE0.sum()).expand(N, A).clone()   # rsh_c at t0 (normalisation under B6)
    E_close = torch.full((N, A), float("nan"), device=dev); E_2040 = torch.full((N, A), float("nan"), device=dev)
    n_cf_gate = zeroNA.clone()                                # steps with the automation gate open
    recA["Ecf"] = torch.zeros(N, A, ny, device=dev)
    # leader-vs-leader kinetic dominance (diagnostic only, always recorded, changes nothing): first time the US (China)
    # bloc holds >= dom_thr of the combined US + China kinetic power
    t_domUS = torch.full((N,), INF, device=dev); t_domCN = t_domUS.clone()
    t_ten = torch.full((N, A), T0, device=dev); ldr_prev = torch.full((N, A), -1, dtype=torch.long, device=dev)
    split = torch.zeros(N, A, dtype=torch.bool, device=dev)
    t_ref_reset = torch.full((N, A), -INF, device=dev)        # brake 3: refusal-convergence restart after a split
    pid_at_dec = torch.zeros(N, A, dtype=torch.bool, device=dev); pidlev_at_dec = torch.full((N, A), float("nan"), device=dev)
    pid_yrs_closed = zeroNA.clone(); yrs_closed = zeroNA.clone(); t_pid = torch.full((N, A), INF, device=dev)
    pid_at_X = torch.zeros(N, A, dtype=torch.bool, device=dev)
    n_death = zeroNA.clone(); n_heir = zeroNA.clone(); n_split = zeroNA.clone(); n_halt_mort = zeroNA.clone()
    t_halt_mort = torch.full((N, A), INF, device=dev); n_death_exec = zeroNA.clone()
    n_sr_dec = zeroNA.clone(); n_sr_memflip = zeroNA.clone(); n_sr_flip = zeroNA.clone(); n_sr_flip_harsh = zeroNA.clone()
    n_sr_veto = zeroNA.clone(); n_sr_flipX = zeroNA.clone()
    b1 = P["b1_top"][:, None]; b2 = P["b2_cons"][:, None]; b3 = P["b3_enf"][:, None]
    b4 = P["b4_ret"][:, None]; b5 = P["b5_xb"][:, None]; b6 = P["b6_wire"][:, None]
    POP_ = T(POP)[None]; eyeA = torch.eye(A, dtype=torch.bool, device=dev)[None]
    # B2 coalition: active members, control of human coercive/patronage networks (hw) and of automated force (aw)
    hw0 = torch.exp(P["mem_zh"]); aw0 = ctl_w.clone()
    act = torch.zeros(N, A, NMEM, dtype=torch.bool, device=dev)
    hw = hw0.clone(); aw = aw0.clone()
    S0_init = torch.where(P["p_pers0"] > 0, P["p_pers0"], P["p_pers_bd"])
    one_m = torch.ones(N, A, NMEM, device=dev)

    def reset_coal(mask, n_new, S0, act, hw, aw):
        """new ruling coalition in blocs 'mask': members < n_new active; the member with the strongest human
        network leads with a share S0 of human-network control; automated-force control shares are redrawn (aw0)"""
        n_new = torch.where(P["force_single"][:, None], torch.ones_like(n_new), n_new)
        a_new = memidx[None, None] < n_new[..., None]
        L0 = torch.where(a_new, hw0, -1.0).argmax(-1)
        isL = memidx[None, None] == L0[..., None]
        oth = torch.where(a_new & ~isL, hw0, 0.0).sum(-1)
        S0c = torch.clamp(S0, 0.05, 0.95)
        hl = torch.where(oth > 0, S0c / (1 - S0c) * oth, torch.ones_like(oth))
        hw_n = torch.where(isL, hl[..., None], hw0)
        m3 = mask[..., None]
        return torch.where(m3, a_new, act), torch.where(m3, hw_n, hw), torch.where(m3, aw0, aw)
    n21 = torch.full((N, A), 21.0, device=dev)
    act, hw, aw = reset_coal(init_aut[None].expand(N, A), n21, S0_init, act, hw, aw)
    ldr = torch.zeros(N, A, dtype=torch.long, device=dev); S_L = zeroNA.clone()
    regime_pers = torch.where(b2, init_aut[None] & (S0_init >= 0.5), regime_pers)
    n_coal_dec = torch.full((N, A), float("nan"), device=dev); SL_dec = n_coal_dec.clone()
    n_purged = zeroNA.clone(); n_cc = zeroNA.clone(); t_single = torch.full((N, A), INF, device=dev); t_sl95 = t_single.clone()

    def coal_state(act, hw, aw, h_sa):
        hs = torch.where(act, hw, 0.0); as_ = torch.where(act, aw, 0.0)
        hn = hs / torch.clamp(hs.sum(-1, keepdim=True), min=1e-12); an = as_ / torch.clamp(as_.sum(-1, keepdim=True), min=1e-12)
        cw = h_sa[..., None] * hn + (1 - h_sa[..., None]) * an          # A6: control share of coercive force
        L_ = torch.where(act, cw, -1.0).argmax(-1)
        SL = cw.gather(-1, L_[..., None])[..., 0]
        return cw, L_, SL
    # B3/B5 kinetic power and enforcement
    MIL0_ = T(MIL0)[None].repeat(N, 1); MIL0_[:, 1] = MIL0_[:, 1] * P["cn_ppp"]
    MIL_INT_ = MIL0_ / T(WORLD_W)[None]                                   # military share / output share (2026)
    Y_AVG = float(WORLD_W.sum() / WORKFORCE.sum())
    Mk = MIL0_ * (1 + P["k_am"][:, None] * 0.03); enf = torch.ones(N, A, device=dev); rival = torch.ones(N, A, device=dev)
    # B4 atrocity weight inputs
    inflicted = z64.clone()                              # deaths caused abroad (B5), as a share of own population
    # B5 cross-bloc campaigns (per target bloc)
    xb_on = torch.zeros(N, A, dtype=torch.bool, device=dev); xb_by = torch.full((N, A), -1, dtype=torch.long, device=dev)
    t_xb = torch.full((N, A), INF, device=dev); t_xb1 = t_xb.clone(); lc_xb = z64.clone(); t_xb_nuc = t_xb.clone()
    n_xb_launch = zeroNA.clone(); n_xb_rep = zeroNA.clone()
    # B6 world pools of robot inputs (normalised 2026 shares) and reshoring toward own demand
    rsh_m = T(RE_SHARE0 / RE_SHARE0.sum()).expand(N, A).clone(); rsh_c = T(CHIP_SHARE0 / CHIP_SHARE0.sum()).expand(N, A).clone()
    Lh = torch.zeros(N, NSTEP, device=dev); Lph = torch.zeros(N, NSTEP, device=dev)
    lagc_s = torch.round(P["lag_cog"] / DT).long(); lagp_s = torch.round(P["lag_phys"] / DT).long()
    cap_prev = torch.full((N, A), 1e9, device=dev); omega = T(WORLD_W / WORLD_W.sum()).expand(N, A).clone()

    def others_max(x):
        return torch.stack([torch.cat([x[:, :a], x[:, a + 1:]], 1).max(1).values for a in range(A)], 1)

    for step in range(NSTEP):
        t = T0 + (step + 1) * DT
        dts = t - T0
        # ---- time-varying priors
        C = torch.where(trends, torch.clamp(torch.exp(P["c_trend"] * dts), max=P["c_max"]), 1.0)
        eco = torch.where(trends, torch.clamp(dts / (P["eco_year"] - T0), 0, 1), 0.0)
        # A7: record 2026-27 El Nino raises ecological stress until mid-2028
        eco = torch.where(trends & a7 & (t < 2028.5), torch.maximum(eco, P["s_nino"]), eco)
        att_cap = torch.where(P["f7_nocaps"], P["att_max"], 0.5)
        att = torch.where(trends, torch.minimum(0.23 + P["att_trend"] * dts, att_cap), 0.23)
        # F7: grievance attitudes rise logistically toward g_max (initial slope griev_trend) instead of a hard cap 0.55
        gm = P["g_max"]; r_g = P["griev_trend"] / (0.39 * (1 - 0.39 / gm))
        g_log = gm / (1 + (gm / 0.39 - 1) * torch.exp(-r_g * dts))
        g_att = torch.where(trends, torch.where(P["f7_nocaps"], g_log, torch.clamp(0.39 + P["griev_trend"] * dts, max=0.55)), 0.39)
        mor_decay = torch.where(a7, torch.exp(-P["k_mor"] * dts), 1.0)
        E0t = P["E0"] * torch.where(a7, torch.exp(-P["k_intl"] * dts), 1.0)
        Psq = torch.where(P["f8_sq"][:, None], torch.clamp(Psq0 + P["d_a"] * dts, 0.02, 1.0), Psq0)
        # ---- wars (US-China pair shares one event); new wars beyond the 2026 baseline
        u = rnd(A)
        at_war = t < war_until
        pw = 1 - torch.exp(-P["w_pair"] * torch.sqrt(C) * (1 + 0.5 * (psi[:, 0] - psi[:, 1]).abs()) * DT)
        new_pair = P["war_on"] & (u[:, 0] < pw) & ~at_war[:, 0] & ~at_war[:, 1]
        pr = 1 - torch.exp(-P["w_row"][:, None] * WROW * torch.sqrt(C)[:, None] * DT)
        new_o = P["war_on"][:, None] & (u < pr) & ~at_war
        new_war = torch.cat([new_pair[:, None], new_pair[:, None], new_o[:, 2:]], 1)
        war_until = torch.where(new_war, t + P["war_len"][:, None], war_until)
        n_war += new_war; t_war1 = torch.where(new_war & torch.isinf(t_war1), t, t_war1)
        war = t < war_until
        un = rnd(A); un[:, 1] = un[:, 0]
        nuc = new_war & (un < P["p_nuc"][:, None] * NUC) & P["war_deaths_on"][:, None]
        f_n = P["f_nuc"][:, None] * (0.5 + rnd(A)); f_n[:, 1] = f_n[:, 0]
        t_nuc = torch.where(nuc & torch.isinf(t_nuc), t, t_nuc)
        # ---- cognitive capability
        # A1: capability follows the trend; the compute slowdown is only a trend-break variant
        slow = torch.where(P["a1_trend"], 1.0, P["compute_slowdown"]) if t > 2029.5 else torch.ones_like(L)
        corr = torch.where(P["capex_corr"] & (t > P["corr_start"]) & (t < P["corr_start"] + P["corr_len"]), 0.5, 1.0)
        lnh = torch.log(h80r0) + L * LN2
        s_rnd = nd((lnh - mu_rnd) / sr)
        mult = torch.clamp(((1 - P["rnd0"]) / torch.clamp(1 - s_rnd, min=1e-3)) ** fb, max=30.0)
        L_old = L                                            # compute feedback: actual shared growth this step
        L = torch.minimum(L + torch.clamp(r0 * slow * corr * mult, max=15.0) * DT, Lcap)
        lnh = torch.log(h80r0) + L * LN2
        sw = nd((lnh - mu_sw) / st); s_rnd = nd((lnh - mu_rnd) / sr)
        prac = torch.minimum(torch.sigmoid(torch.logit(torch.clamp(prac, 1e-4, 0.9999)) + P["g_swad"] * DT), sw)
        Fcog = 0.95 * nd((lnh - mu_ec) / se)
        for k, cond in [("M2", sw >= SW_THR["M2"]), ("M3", sw >= SW_THR["M3"]), ("M2p", prac >= SW_THR["M2"]),
                        ("M3p", prac >= SW_THR["M3"]), ("M4", s_rnd >= RND_THR["M4"]), ("M5", s_rnd >= RND_THR["M5"]),
                        ("M6", lnh >= float(np.log(2000.0))), ("M7", Fcog >= 0.5)]:
            tm[k] = torch.where(torch.isinf(tm[k]) & cond, t, tm[k])
        ph3 = torch.clamp(L / L_m3, 0, 1)
        lc = 1 + (P["ai_lc"] - 1) * ph3
        # ---- physical capability
        rp = torch.minimum(P["rp_max"], P["rp0"] * (1 + P["kc"] * torch.clamp(L - L_m3, 0, 8)))
        Lp = torch.minimum(Lp + rp * DT, Lpcap)
        if cf_any:
            # COMPUTE FEEDBACK: a bloc with extra cognitive capability E also advances faster physically (rp at L + E)
            rp_cf = torch.minimum(P["rp_max"][:, None], P["rp0"][:, None] * (1 + P["kc"][:, None] * torch.clamp(L[:, None] + Ecf - L_m3[:, None], 0, 8)))
            Epf = torch.where(cf, torch.clamp(torch.minimum(Epf + (rp_cf - rp[:, None]) * DT, Lpcap[:, None] - Lp[:, None]), min=0), Epf)
        t_dex = torch.where(torch.isinf(t_dex) & (Lp >= Np), t, t_dex)
        Fp = torch.clamp(torch.sigmoid(lFp0 + (float(np.log(0.85 / 0.15)) - lFp0) * Lp[:, None] / (Np[:, None] * T(NP_MULT)[None])), 0, 0.995)
        # B6: bloc-specific deployable capability = frontier capability some years earlier (lag_cog, lag_phys)
        Lh[:, step] = L; Lph[:, step] = Lp
        L_b = Lh.gather(1, torch.clamp(step - lagc_s, min=0)); Lp_b = Lph.gather(1, torch.clamp(step - lagp_s, min=0))
        Fcog_b = torch.where(b6, 0.95 * nd((torch.log(h80r0)[:, None] + L_b * LN2 - mu_ec[:, None]) / se[:, None]), Fcog[:, None])
        Fp_b = torch.clamp(torch.sigmoid(lFp0[:, None] + (float(np.log(0.85 / 0.15)) - lFp0[:, None]) * Lp_b[:, :, None]
                                         / (Np[:, None, None] * T(NP_MULT)[None, None])), 0, 0.995)
        speed = torch.clamp(P["s0"] ** (1 - torch.clamp(Lp / Np, max=1.1)), max=1.2)
        we = P["shifts"] * speed
        auth = (t >= P["t_leth"]) | (war & (t >= P["t_leth"] - 3.0))
        Fp_a = torch.where(b6[..., None], Fp_b, Fp[:, None, :].repeat(1, A, 1))
        if cf_any:
            # COMPUTE FEEDBACK: bloc capability = (B6-lagged) shared trend + the bloc's own extra doublings
            Lbe = torch.where(b6, L_b, L[:, None]) + Ecf
            Fcog_b = torch.where(cf, 0.95 * nd((torch.log(h80r0)[:, None] + Lbe * LN2 - mu_ec[:, None]) / se[:, None]), Fcog_b)
            Lpbe = torch.minimum(torch.where(b6, Lp_b, Lp[:, None]) + Epf, Lpcap[:, None])
            Fp_cf = torch.clamp(torch.sigmoid(lFp0[:, None] + (float(np.log(0.85 / 0.15)) - lFp0[:, None]) * Lpbe[:, :, None]
                                              / (Np[:, None, None] * T(NP_MULT)[None, None])), 0, 0.995)
            Fp_a = torch.where(cf3, Fp_cf, Fp_a)
        a3 = P["a3_sec"][:, None]
        Fp_a[:, :, 7] = Fp_a[:, :, 7] * torch.where(auth | a3, 1.0, 0.5)
        F_tot = X0b + (1 - X0b) * Fp_a
        prof = torch.where(P["prof_on"], torch.clamp((Lp / Np - 0.5) / 0.5, 0, 1), 0.0)
        prof_b = torch.where(P["prof_on"][:, None] & b6, torch.clamp((Lp_b / Np[:, None] - 0.5) / 0.5, 0, 1), prof[:, None])
        if cf_any:
            prof_b = torch.where(cf & P["prof_on"][:, None], torch.clamp((Lpbe / Np[:, None] - 0.5) / 0.5, 0, 1), prof_b)
        # ---- pursuit
        clos = 1 - Dc_prev
        psi = torch.clamp(psi0 + 0.2 * (sw >= SW_THR["M3"]).float()[:, None] + 0.15 * war.float()
                          + P["race_gamma"][:, None] * torch.clamp(others_max(clos) - clos, min=0), 0, 1)
        # B6: reshoring speed is limited by the bloc's industrial base (IB): a bloc with no chip, magnet or robot industry
        # cannot build one in 4-8 years because the leaders race (round 2 let every bloc reshore at US/China speed)
        kr = torch.where(b6[..., None], K_RESH_ * T(IB)[None, :, None], K_RESH_)
        own = own + (kr * lc[:, None, None] * psi[:, :, None] * (1 - own)) * DT
        q = torch.clamp(P["q_core"], max=1.0)[:, None]
        core_alloc = torch.maximum(psi, q)
        h_rr = (Dcs[:, :, RR] * W_S_[RR]).sum(-1) / W_S_[RR].sum()
        A_rr = torch.clamp(1 - Dcs[:, :, RR].max(-1).values, 0, 1)
        Td = P["Td_auto"][:, None] * (P["Td_mat"] / P["Td_auto"])[:, None] ** torch.clamp(n_sr / 7.0, max=1.0)
        g_auto = LN2 / Td
        # ---- adoption. Proportional (logistic) growth from the measured share at the measured rate, pushed
        # toward ramp rates by priority; the INCREMENT is capped by new automated capacity + retrofit
        g0e = g0.clone(); g0e[:, :, 7] = g0e[:, :, 7] * torch.sqrt(C)[:, None]
        gr = P["g_ramp"][:, None, None]
        corr_b = corr[:, None, None]
        m5p = torch.maximum(0.5 * psi, prof_b)[:, :, None]
        pri_c = torch.maximum(core_alloc, prof_b)[:, :, None]
        g_full = torch.maximum(g0e, gr * corr_b * m5p) * lc[:, None, None]
        g_core = torch.maximum(g0e, gr * corr_b * pri_c) * lc[:, None, None]
        Arr3 = A_rr[:, :, None]
        bld = (P["fact_build_h"] / P["fact_build_a"])[:, None, None]
        g_ra = gr * bld
        g_full = g_full * (1 - Arr3) + torch.maximum(g_ra * m5p, g_full) * Arr3
        g_core = g_core * (1 - Arr3) + torch.maximum(g_ra * pri_c, g_core) * Arr3
        # A3: security/coercion automation has no separate curve or lag: it is a byproduct of capability (F_tot, no
        # authorization halving) and physical capacity, with military first call (full priority in every bloc, and
        # its increment is exempt from the supply rationing below). Bounded by the capacity-turnover caps.
        one3 = torch.ones_like(m5p)
        g_s7 = torch.maximum(g0e[:, :, 7:8], gr * corr_b * one3) * lc[:, None, None]
        g_s7 = g_s7 * (1 - Arr3) + torch.maximum(g_ra * one3, g_s7) * Arr3
        g_full[:, :, 7:8] = torch.where(a3[:, :, None], g_s7, g_full[:, :, 7:8])
        g_core[:, :, 7:8] = torch.where(a3[:, :, None], g_s7, g_core[:, :, 7:8])
        # capacity-turnover caps
        iK = P["i_K"][:, None, None] * (1 + (P["i_boost"][:, None, None] - 1) * m5p) / P["k_int"][:, None, None]
        iK = iK * (1 + (bld - 1) * Arr3)
        rr0 = P["r_retro0"][:, None, None]; rrp = P["r_retro_p"][:, None, None]
        cap_f = iK + rr0 + (rrp - rr0) * m5p
        g_new_c = gr * corr_b * pri_c * lc[:, None, None] * (1 + (bld - 1) * Arr3)
        cap_c = g_new_c + rr0 + (rrp - rr0) * pri_c
        cap_s7 = (P["i_K"][:, None, None] * P["i_boost"][:, None, None] / P["k_int"][:, None, None] * (1 + (bld - 1) * Arr3)
                  + rrp) * one3
        cap_f = cap_f.expand(N, A, S).clone(); cap_c = cap_c.expand(N, A, S).clone()
        cap_f[:, :, 7:8] = torch.where(a3[:, :, None], torch.maximum(cap_f[:, :, 7:8], cap_s7), cap_f[:, :, 7:8])
        cap_c[:, :, 7:8] = torch.where(a3[:, :, None], torch.maximum(cap_c[:, :, 7:8], cap_s7), cap_c[:, :, 7:8])
        dxf = torch.clamp(torch.minimum(g_full * xf * (1 - xf / F_tot), cap_f * (F_tot - xf)), min=0) * DT
        dxc = torch.clamp(torch.minimum(g_core * xc * (1 - xc / F_tot), cap_c * (F_tot - xc)), min=0) * DT
        g_kit = torch.maximum(T(G_IND)[None], psi * P["g_ramp"][:, None]) * lc[:, None]
        g_kit = g_kit / (1 + torch.clamp(kit - kit0, min=0) / (P["kit_brake"][:, None] * need_tot))
        g_kit = g_kit * (1 - A_rr) + torch.maximum(g_auto, g_kit) * A_rr
        kit_new = torch.minimum(kit * torch.exp(g_kit * DT), 1e4 * need_tot)
        # B6/F6 wiring: fixed automation kit draws on the SAME physical robot-input budget (magnets, chips, actuators,
        # human build labour) as general-purpose robots; round 2 let kit grow with no input constraint (bypass)
        kit_inc_cap = torch.clamp(cap_prev - prod, min=0) * P["shifts"][:, None] / P["k_kit"][:, None] * DT
        # audit (round 3): the F6 switch f6_kitcap was defined but never read (variant rev_F6_kit_uncapped was inert);
        # the kit cap now needs both b6_wire and f6_kitcap
        kit = torch.where(b6 & P["f6_kitcap"][:, None], torch.minimum(kit_new, kit + kit_inc_cap), kit_new)
        supply = kit + Rst * we[:, None]
        if gf_any:
            # ---- GREENFIELD CORE LOOP: build step. Interpretation choices (all documented in results/m8_v6_final.json):
            # (b) build limits, existing priors only.
            #   mining / energy / chips (segments 0-2): the loop takes the core_alloc share of the bloc's NEW domestic
            #   capacity in that sector. That capacity grows at exactly the existing Gm/Ge/Gc rates (Td_*_base/race
            #   blended by psi, switching to the automated floors Td_mine_auto / Td_en_auto / Td_fab_auto, the last
            #   derived from fab_build, as the sector automates). New capacity per year = g x G x own (the domestic base),
            #   expressed as a share of the loop segment (divided by q). So a small loop (q ~ 0.15) needs only ~15% of
            #   today's domestic sector capacity in new build: this is where the loop size enters.
            #   factory-type segments (manufacturing, logistics, construction, maintenance, admin): built in parallel,
            #   each plant online after the factory lead time (first-order approach to the capability gate with time
            #   constant fact_build_h, moving to fact_build_a (robotic/prefab construction) as the bloc's resource chain
            #   automates, A_rr, the same blend the existing code uses for bld), and capped by the bloc's gross investment
            #   flow at core priority concentrated on the loop: i_K (1 + (i_boost - 1) core_alloc) / k_int x the same
            #   automated-build boost bld, / q (a funding cap on NEW capacity, not turnover of existing plants;
            #   about one loop-share per year at the median q).
            #   security (segment 7) is NOT built by the loop: security automation follows A3 and is shared, so the loop
            #   uses the existing security path (no double counting of security capacity, h_sec unchanged by the loop).
            # (c) capability gate: the loop's automated share of segment s never exceeds F_tot[s] for that bloc (B6
            #   lagged frontier physical capability). Its cognitive share is the existing core path's acc (logistic at
            #   the core priority rate toward the B6-lagged Fcog gate; software deployment is not turnover-limited),
            #   so the loop and the conversion path share cognitive automation.
            # (a) robots and kit: the loop draws on the SAME supply. It can only use automation not installed in the
            #   existing economy (supply - xf T_s; existing kit is bolted into existing plants), at core priority
            #   (core_alloc share), after the security increments of both conversion paths (A3 first call), and it
            #   also respects the core budget room_c: q xc T_s + loop stock <= core_alloc x supply. Its stock is then
            #   removed from the non-security room of both conversion paths below, so no robot is counted twice. The
            #   input pools (mat_cap, chip_cap, hum_cap with the B6 wiring) bound robot production and the kit
            #   increment, hence supply; the loop cannot exceed them.
            ca = core_alloc
            fl_g = P["floors_on"][:, None]
            Am_g = 1 - Dcs[:, :, 0]; Ae_g = 1 - Dcs[:, :, 1]; Af_g = 1 - Dcs[:, :, 2]      # previous step (effective)
            gm_h = ((LN2 / P["Td_mine_base"])[:, None] * (1 - psi) + (LN2 / P["Td_mine_race"])[:, None] * psi) * lc[:, None]
            ge_h = ((LN2 / P["Td_en_base"])[:, None] * (1 - psi) + (LN2 / P["Td_en_race"])[:, None] * psi) * lc[:, None]
            gc_h = ((LN2 / P["Td_fab_base"])[:, None] * (1 - psi) + (LN2 / P["Td_fab_race"])[:, None] * psi) * lc[:, None]
            gm_a = torch.where(fl_g, torch.minimum(g_auto, (LN2 / P["Td_mine_auto"])[:, None]), g_auto)
            ge_a = torch.where(fl_g, torch.minimum(g_auto, (LN2 / P["Td_en_auto"])[:, None]), g_auto)
            gc_a = torch.where(fl_g, torch.minimum(g_auto, (LN2 / Td_fab_auto)[:, None]), g_auto)
            g_m = gm_h * (1 - Am_g) + torch.maximum(gm_a, gm_h) * Am_g
            g_e = ge_h * (1 - Ae_g) + torch.maximum(ge_a, ge_h) * Ae_g
            g_c = gc_h * (1 - Af_g) + torch.maximum(gc_a, gc_h) * Af_g
            heavy = torch.stack([g_m * Gm * own[:, :, 0], g_e * Ge * own[:, :, 1], g_c * Gc * own[:, :, 2]], -1) * (ca / q)[..., None]
            dy_g = torch.zeros_like(ygf)
            dy_g[:, :, :3] = torch.minimum(heavy * DT, F_tot[:, :, :3] - ygf[:, :, :3])
            inv_lead = (1 - A_rr) / P["fact_build_h"][:, None] + A_rr / P["fact_build_a"][:, None]
            dy_lead = (F_tot - ygf) * (1 - torch.exp(-inv_lead * DT))[..., None]
            r_inv = (P["i_K"][:, None] * (1 + (P["i_boost"][:, None] - 1) * ca) / P["k_int"][:, None]
                     * (1 + (bld[..., 0] - 1) * A_rr) * corr[:, None] / q)
            dy_g[:, :, FAC_SEG] = torch.minimum(dy_lead[:, :, FAC_SEG], (r_inv * DT)[..., None])
            dy_g = torch.clamp(dy_g, min=0) * no_sec
            d7f_dem = torch.where(a3, dxf[:, :, 7] * T_s[:, :, 7], 0.0)
            d7c_dem = torch.where(a3, q * dxc[:, :, 7] * T_s[:, :, 7], 0.0)
            pool_new = ca * torch.clamp(supply - (xf * T_s).sum(-1) - d7f_dem - Rg, min=0)
            pool_core = torch.clamp(ca * supply - q * (xc * T_s).sum(-1) - d7c_dem - Rg, min=0)
            need_g = q * (dy_g * T_s).sum(-1)
            sg = torch.clamp(torch.minimum(pool_new, pool_core) / torch.clamp(need_g, min=1e-12), max=1.0)
            bld_now = gf & (need_g > 1e-9)
            n_gf_build += bld_now; n_gf_rob += bld_now & (sg < 0.999)
            wg = W_S_ * (1 - CS_) * no_sec
            n_gf_gate += bld_now & ((ygf * wg).sum(-1) >= 0.98 * (F_tot * wg).sum(-1))
            ygf = torch.where(gf3, torch.minimum(ygf + dy_g * sg[..., None], torch.maximum(F_tot, ygf)), ygf)
            Rg = torch.where(gf, q * (ygf * T_s).sum(-1), Rg)
        room_f = torch.clamp(supply - (xf * T_s).sum(-1), min=0)
        room_c = torch.clamp(core_alloc * supply - q * (xc * T_s).sum(-1), min=0)
        sc_f = torch.clamp(room_f / torch.clamp((dxf * T_s).sum(-1), min=1e-12), max=1.0)
        sc_c = torch.clamp(room_c / torch.clamp(q * (dxc * T_s).sum(-1), min=1e-12), max=1.0)
        scf = sc_f[:, :, None].expand(N, A, S).clone(); scc = sc_c[:, :, None].expand(N, A, S).clone()
        scf[:, :, 7] = torch.where(a3, 1.0, scf[:, :, 7]); scc[:, :, 7] = torch.where(a3, 1.0, scc[:, :, 7])   # A3 first call
        # B6: A3 'first call' means security is served FIRST from the available supply, not exempt from it (round 2
        # bypass: the security increment ignored supply entirely)
        d7f = dxf[:, :, 7] * T_s[:, :, 7]; d7c = q * dxc[:, :, 7] * T_s[:, :, 7]
        s7f = torch.clamp(room_f / torch.clamp(d7f, min=1e-12), max=1.0); s7c = torch.clamp(room_c / torch.clamp(d7c, min=1e-12), max=1.0)
        oth_f = (dxf * T_s).sum(-1) - d7f; oth_c = q * (dxc * T_s).sum(-1) - d7c
        so_f = torch.clamp(torch.clamp(room_f - s7f * d7f, min=0) / torch.clamp(oth_f, min=1e-12), max=1.0)
        so_c = torch.clamp(torch.clamp(room_c - s7c * d7c, min=0) / torch.clamp(oth_c, min=1e-12), max=1.0)
        w6 = b6 & a3
        scf = torch.where(w6[..., None], so_f[..., None].expand(N, A, S), scf); scc = torch.where(w6[..., None], so_c[..., None].expand(N, A, S), scc)
        scf[:, :, 7] = torch.where(w6, s7f, scf[:, :, 7]); scc[:, :, 7] = torch.where(w6, s7c, scc[:, :, 7])
        if gf_any:
            # GREENFIELD: the loop's robots/kit (Rg) are unavailable to both conversion paths' non-security increments;
            # security keeps its first call on the original room (A3), so the loop never crowds out security
            room_f2 = torch.clamp(room_f - Rg, min=0); room_c2 = torch.clamp(room_c - Rg, min=0)
            sc_f2 = torch.clamp(room_f2 / torch.clamp((dxf * T_s).sum(-1), min=1e-12), max=1.0)
            sc_c2 = torch.clamp(room_c2 / torch.clamp(q * (dxc * T_s).sum(-1), min=1e-12), max=1.0)
            so_f2 = torch.clamp(torch.clamp(room_f2 - s7f * d7f, min=0) / torch.clamp(oth_f, min=1e-12), max=1.0)
            so_c2 = torch.clamp(torch.clamp(room_c2 - s7c * d7c, min=0) / torch.clamp(oth_c, min=1e-12), max=1.0)
            scf2 = torch.where(w6, so_f2, sc_f2)[..., None].expand(N, A, S).clone(); scf2[:, :, 7] = scf[:, :, 7]
            scc2 = torch.where(w6, so_c2, sc_c2)[..., None].expand(N, A, S).clone(); scc2[:, :, 7] = scc[:, :, 7]
            scf = torch.where(gf3, scf2, scf); scc = torch.where(gf3, scc2, scc)
        xf = torch.clamp(xf + dxf * scf, max=0.999)
        xc = torch.clamp(xc + dxc * scc, max=0.999)
        Fc = torch.maximum(Fcog_b[:, :, None], a0c)
        mat = torch.clamp((Fcog - P["Fcog0"]) / (0.9 - P["Fcog0"]), 0, 1)
        gc = (P["g_cog0"] + (P["g_cog_max"] - P["g_cog0"]) * mat)[:, None, None] * adm
        gcc = torch.maximum(gc, P["g_cog_max"][:, None, None] * core_alloc[:, :, None])
        acf = torch.minimum(acf + torch.clamp(gc * acf * (1 - acf / Fc), min=0) * DT, Fc)
        acc = torch.minimum(acc + torch.clamp(gcc * acc * (1 - acc / Fc), min=0) * DT, Fc)
        hf = CS_ * (1 - acf) / (1 - a0c) + (1 - CS_) * (1 - xf) / (1 - X0b)
        hc = CS_ * (1 - acc) / (1 - a0c) + (1 - CS_) * (1 - xc) / (1 - X0b)
        hx = torch.einsum("ab,nbs->nas", exp_w, hf)
        # B6: imported core inputs count as closed only to the extent they are SECURED: exporters that race restrict
        # exports (openness 1 - 0.7 psi); the unsecured share of imports is a dependence on the leaders, not closure
        sec_imp = torch.einsum("ab,nb->na", exp_w, 1 - 0.7 * psi)
        hx6 = hx + (1 - hx) * (1 - sec_imp)[:, :, None]
        hxu = torch.where(b6[..., None], hx6, hx)
        Dcs = own * hc + (1 - own) * hxu
        Dfs = own * hf + (1 - own) * hxu
        Dc = (Dcs * W_S_).sum(-1); Df = (Dfs * W_S_).sum(-1)
        Dfd = (hf * W_S_).sum(-1)
        if gf_any:
            # ---- GREENFIELD: loop dependence. Per segment, Dcs = CS x (cognitive part) + (1 - CS) x phys_ex with
            # phys_ex = own (1 - xc)/(1 - X0) + (1 - own) hxu. The loop shares the cognitive part (acc, see above) and
            # replaces the physical part by its own uncovered share (1 - ygf)/(1 - X0): human labor still needed by
            # the minimal loop relative to 2026 (its built capacity is domestic by construction; the uncovered part is
            # counted as human, conservative). Security uses the shared A3 path (Dg = Dcs). D_loop = labor-weighted
            # (W_S) sum = 1 minus the covered share. Everything downstream (Dc, closure, t_core, psi race, h_sa,
            # h_sec, A_rr, A_mine/A_fab/A_en, hum_cap via h_rr, the lever hooks) uses the elementwise minimum.
            Dc_conv = Dc
            phys_ex = own * (1 - xc) / (1 - X0b) + (1 - own) * hxu
            Dg = Dcs + (1 - CS_) * ((1 - ygf) / (1 - X0b) - phys_ex)
            Dg[:, :, 7] = Dcs[:, :, 7]
            Dc_loop = (Dg * W_S_).sum(-1)
            Dcs = torch.where(gf3, torch.minimum(Dcs, Dg), Dcs)
            Dc = torch.where(gf, (Dcs * W_S_).sum(-1), Dc)
            trg_g = P["trig"][:, None]
            t_cl_conv = torch.where(gf & torch.isinf(t_cl_conv) & (Dc_conv < trg_g), t, t_cl_conv)
            t_cl_gf = torch.where(gf & torch.isinf(t_cl_gf) & (Dc_loop < trg_g), t, t_cl_gf)
        Dc_prev = Dc
        h_sec_f = hf[:, :, 7]
        # ---- general-purpose robot production
        g_hum = torch.log(P["humanoid_mult"])[:, None] / (1 + prod / P["P_half"][:, None])
        g_pot = g_hum * (1 - A_rr) + torch.maximum(g_auto, g_hum) * A_rr
        n_sr = n_sr + torch.where(A_rr > 0.7, g_pot * DT / LN2, 0.0)
        A_mine = 1 - Dcs[:, :, 0]; A_fab = 1 - Dcs[:, :, 2]; A_en = 1 - Dcs[:, :, 1]
        fl = P["floors_on"][:, None]
        g_mh = ((LN2 / P["Td_mine_base"])[:, None] * (1 - psi) + (LN2 / P["Td_mine_race"])[:, None] * psi) * lc[:, None]
        g_fh = ((LN2 / P["Td_fab_base"])[:, None] * (1 - psi) + (LN2 / P["Td_fab_race"])[:, None] * psi) * lc[:, None]
        g_eh = ((LN2 / P["Td_en_base"])[:, None] * (1 - psi) + (LN2 / P["Td_en_race"])[:, None] * psi) * lc[:, None]
        g_ma = torch.where(fl, torch.minimum(g_auto, (LN2 / P["Td_mine_auto"])[:, None]), g_auto)
        g_fa = torch.where(fl, torch.minimum(g_auto, (LN2 / Td_fab_auto)[:, None]), g_auto)
        g_ea = torch.where(fl, torch.minimum(g_auto, (LN2 / P["Td_en_auto"])[:, None]), g_auto)
        Gm = torch.clamp(Gm * torch.exp((g_mh * (1 - A_mine) + torch.maximum(g_ma, g_mh) * A_mine) * DT), max=1e6)
        Gc = torch.clamp(Gc * torch.exp((g_fh * (1 - A_fab) + torch.maximum(g_fa, g_fh) * A_fab) * DT), max=1e6)
        Ge = torch.clamp(Ge * torch.exp((g_eh * (1 - A_en) + torch.maximum(g_ea, g_eh) * A_en) * DT), max=1e6)
        re_share = re_share + K_RESH[0] * psi * (1 - re_share) * DT * 0.5
        chip_share = chip_share + K_RESH[2] * psi * (1 - chip_share) * DT * 0.5
        openness = 1 - 0.7 * others_max(psi)
        mat_cap = P["M0"][:, None] * (re_share + (1 - re_share) * openness) * Gm
        chip_cap = P["C0"][:, None] * (chip_share + (1 - chip_share) * openness) * Gc
        # B6: M0 and C0 are WORLD pools (round 2 gave every bloc the full world pool: a bypass). Each bloc gets its
        # domestic production plus imports allocated by purchasing power (output share omega); exporters restrict
        # exports as they pursue automation themselves (openness 1 - 0.7 psi_exporter; China's 2025 rare-earth export
        # licensing, US chip export controls). Domestic capacity grows with the bloc's mining/fab multipliers and a
        # reshoring drift toward its own demand share. Blocs without chip/magnet/robot industries depend on imports.
        rsh_m = rsh_m + K_RESH[0] * psi * 0.5 * torch.clamp(omega - rsh_m, min=0) * DT
        rsh_c = rsh_c + K_RESH[2] * psi * 0.5 * torch.clamp(omega - rsh_c, min=0) * DT
        opx = 1 - 0.7 * psi

        def avail_pool(dom):
            ex = dom * opx
            return dom * (1 - opx) + ex * omega + omega * (ex.sum(1, keepdim=True) - ex)
        mat_cap = torch.where(b6, P["M0"][:, None] * avail_pool(rsh_m * Gm), mat_cap)
        chip_cap = torch.where(b6, P["C0"][:, None] * avail_pool(rsh_c * Gc), chip_cap)
        if cf_any:
            # ---- COMPUTE FEEDBACK: own compute capacity C_b = min(domestic chip capacity, energy capacity), 2026 = 1
            chip_dom = torch.where(b6, rsh_c * Gc / chip0_cf, chip_share * Gc / T(CHIP_SHARE0)[None])
            lnC = torch.log(torch.clamp(torch.minimum(chip_dom, Ge), min=1e-9))
            dlnC = (lnC - lnC_prev) / DT
            lnC_prev = lnC
            g_tr = (torch.minimum(LN2 / P["Td_fab_race"], LN2 / P["Td_en_race"]) * lc)[:, None]
            ygc = ygf[:, :, 2] if gf_any else zeroNA
            yge = ygf[:, :, 1] if gf_any else zeroNA
            gate_cf = (torch.maximum(A_fab, ygc) > 0.5) & (torch.maximum(A_en, yge) > 0.5)
            n_cf_gate += cf & gate_cf
            trend_rate = (L - L_old) / DT                    # actual shared-trend growth this step (0 once L is capped)
            rate_max = torch.clamp(torch.minimum(torch.full_like(r0, 15.0), 30.0 * r0 * slow * corr) - trend_rate, min=0)[:, None]
            dE = torch.minimum(P["eta_cf"][:, None] * torch.clamp(dlnC - g_tr, min=0) / LN2 * gate_cf.float(), rate_max)
            E_new = Ecf + dE * DT
            # spillover toward the leader (theft, open weights, talent), slowed by the leader's racing intensity
            Emax, lead_i = E_new.max(1)
            psiL = psi.gather(1, lead_i[:, None])[:, 0]
            E_new = E_new + (P["s_sp"] * (1 - 0.7 * psiL))[:, None] * torch.clamp(Emax[:, None] - E_new, min=0) * DT
            # no level cap on E: the shared trend's level caps (the 1e5-hour horizon ceiling and the cognitive wall,
            # Lcap) apply to the shared L only; the instructed caps are the rate caps (15 doublings/yr, 30x)
            Ecf = torch.where(cf, E_new, Ecf)
            E_close = torch.where(torch.isnan(E_close) & torch.isfinite(t_closed), Ecf, E_close)
            if abs(t - 2040.0) < 1e-9:
                E_2040 = Ecf.clone()
        hum_cap = P["Pmax_h"][:, None] * T(MFG_SHARE)[None] * (1 + (P["adl"] - 1) * ph3)[:, None] / torch.clamp(h_rr, min=0.01)
        cap = torch.minimum(torch.minimum(mat_cap, chip_cap), hum_cap)
        Fp_avg = (Fp_a * wsc).sum(-1) / wsc.sum()
        Rdem = torch.maximum(need_tot * Fp_avg, psi * q * need_tot) / we[:, None]
        dfac = torch.sqrt(torch.clamp(1 - Rst / torch.clamp(Rdem, min=1e-9), 0, 1))
        dfac = torch.maximum(dfac, P["reinvest"][:, None] * A_rr ** 2)
        dfac = torch.where(Rst * we[:, None] / Wk > P["G_max"][:, None], 0.0, dfac)
        dfac = torch.where(Rst * KW_ROBOT / 1000.0 > E_FRAC * T(E_GW0)[None] * Ge, 0.0, dfac)
        prod = torch.minimum(prod * torch.exp(g_pot * dfac * DT), torch.clamp(cap, min=1e-6))
        Rst = Rst + (prod - Rst / P["robot_life"][:, None]) * DT
        Gr_cur = Rst * we[:, None] / Wk
        G = (1 + Gr_cur) * (1 + (acf * W_S_).sum(-1))
        cap_prev = cap
        # B3/B5: kinetic power = output x (1 + k_am x automated share of security); purchasing share for imports (B6)
        # output = 2026 human output (share of world industrial output) x cognitive automation gain + robot output valued
        # at the WORLD-AVERAGE output per core worker (a robot is not more productive because it is in a high-wage bloc;
        # using per-worker growth G would credit each US-bloc robot with ~3.4x a Chinese robot's output)
        Ytot = T(WORLD_W)[None] * (1 + (acf * W_S_).sum(-1)) + Y_AVG * Rst * we[:, None]
        Mk = MIL_INT_ * Ytot * (1 + P["k_am"][:, None] * (1 - h_sec_f))            # military intensity x output x automation
        omega = Ytot / Ytot.sum(1, keepdim=True)
        dUS = Mk[:, 0] / (Mk[:, 0] + Mk[:, 1])          # diagnostic only
        t_domUS = torch.where(torch.isinf(t_domUS) & (dUS >= P["dom_thr"]), t, t_domUS)
        t_domCN = torch.where(torch.isinf(t_domCN) & (1 - dUS >= P["dom_thr"]), t, t_domCN)
        for j, th in enumerate(thr):
            t_core[:, :, j] = torch.where(torch.isinf(t_core[:, :, j]) & (Dc < th), t, t_core[:, :, j])
            t_full[:, :, j] = torch.where(torch.isinf(t_full[:, :, j]) & (Df < th), t, t_full[:, :, j])

        # ================= grievance loop =================
        decided = choice >= 0
        disp = (1 - Dfd) * (1 - P["r_ab"][:, None] * Dfd)
        Gnorm = torch.clamp(Gv / 0.5, 0, 1)
        # F8/A5: status-quo provision starts on today's trajectory (cuts in the US) and the displaced get only a
        # fraction dm of it; grievance-driven responses (democratic k_resp, autocratic buy-off while coercion needs
        # humans) come on top. Warehousing must be chosen.
        Pb = torch.where(P["f8_sq"][:, None], Psq * P["dm"], BASE_PROV_[None])
        P_pre = Pb + (1 - Pb) * Gnorm * torch.clamp(
            P["k_resp"][:, None] * Ddem + P["k_buy"][:, None] * (1 - Ddem) * h_sec_f, 0, 1)
        Pv = torch.where(decided & (choice != I_SQ), PROV_[choice.clamp(min=0)], P_pre)
        Pv = torch.where(t < prov_floor_until, torch.clamp(Pv, min=0.8), Pv)
        amp = 1 + P["k_ineq"][:, None] * (1 - Dfd)
        Gt = 1 - (1 - g_att[:, None]) * (1 - torch.clamp(disp * amp * (1 - P["pg_red"][:, None] * Pv), 0, 1))
        Gt = torch.clamp(Gt + 0.2 * BF, 0, 1)
        Gv = torch.where(loop, Gv + (Gt - Gv) * float(1 - np.exp(-DT)), 0.39)
        ecoM = 1 + (P["eco_mult"] - 1) * eco
        H = (P["h_beh0"] * (att / 0.23) ** P["e_att"] * ecoM)[:, None] \
            * P["mdisp"][:, None] ** (torch.where(f7, disp, torch.clamp(disp, max=0.5)) / 0.1) * (1 - P["pr_red"][:, None] * Pv) \
            * (1 + BF) * (1 - P["dfd"][:, None] * DF) * (Gv / G_ref[:, None]) ** P["e_g"][:, None]
        H = torch.where(loop, H, H0)
        Hr = H / H_ref[:, None]
        Hre = hsat(Hr)
        det = h_sec_f + (1 - h_sec_f) * (1 - P["surv_on"][:, None] * (1 - P["d_surv"][:, None]))
        u = rnd(A, 4)
        lam_on = torch.clamp(lam0 * (Hre / Hr0e) ** beta * freg(Ddem) / freg0 * det, max=2.0)
        # baseline: no new insurgency once half the bloc is dead (hard cutoff). Audit variant 'revolt_scaled_by_survivors'
        # replaces it with an onset hazard proportional to the surviving share (no cutoff)
        ocut = P["onset_cut"][:, None]
        onset = loop & ~Iact & torch.where(
            ocut, (u[:, :, 0] < 1 - torch.exp(-lam_on * DT)) & (loss < 0.5),
            u[:, :, 0] < 1 - torch.exp(-lam_on * (1 - loss).float() * DT))
        rd_eff = P["rd"][:, None] + (1 - P["rd"][:, None]) * (1 - h_sec_f) * P["k_auto"][:, None]
        lam_sup = -torch.log(torch.clamp(1 - rd_eff, min=1e-3)) / 5.0
        lam_suc = (1 - P["coin_win"][:, None]) / P["ins_dur"][:, None] * (1 - (1 - P["def_mult"][:, None]) * (1 - h_sec_f))
        lam_suc = lam_suc * torch.where(P["f3_defect"][:, None] & (t < def_until), P["OR_def"][:, None], 1.0)   # F3
        pe = 1 - torch.exp(-(lam_sup + lam_suc) * DT)
        ends = Iact & (u[:, :, 1] < pe)
        uu = rnd(A, 3)
        success = ends & (uu[:, :, 0] < lam_suc / (lam_sup + lam_suc))
        suppressed = ends & ~success
        # collective punishment during active insurgency, scaled to the region in revolt
        lu = 0.2 + 0.8 * (1 - Dfd)
        wc = (1 - Ddem) * (1 - 0.5 * torch.clamp(torch.where(b3, enf, press), 0, 1))      # B3: enforceable pressure only
        lam_lcp = -torch.log(1 - P["p_lcp"])[:, None] / P["ins_dur"][:, None] * lu * wc * (1 + id_lev) * torch.where(war, 1.5, 1.0)
        lcp = Iact & (u[:, :, 2] < 1 - torch.exp(-lam_lcp * DT))
        # F3/A4: a collective-punishment order fails only if the human share of coercion is large enough that a
        # systematic defection removes the capacity the order needs; autonomous systems remove this check
        mst = torch.where(regime_pers, P["m_stack_pers"][:, None], P["m_stack_olig"][:, None])
        ud = rnd(A, 2)
        lcp_def = P["f3_defect"][:, None] & lcp & (ud[:, :, 0] < P["q_C"][:, None] * mst) \
            & (P["d_def"][:, None] * h_sec_f > 1 - P["c_req"][:, None])
        def_until = torch.where(lcp_def, t + 5.0, def_until)
        lcp = lcp & ~lcp_def
        base = (0.05 + 0.20 * uu[:, :, 1]) * P["cp_scale"][:, None]
        klcp = torch.clamp(P["f_lcp"][:, None] * torch.exp(0.5 * rn(A)), max=0.8) * Gv * base
        n_lcp += lcp; t_lcp1 = torch.where(lcp & torch.isinf(t_lcp1), t, t_lcp1)
        BF = BF * float(np.exp(-DT / 3.0)) + torch.where(Iact, 0.9 * (1 - rd_eff) * P["k_bf"][:, None] * DT, 0.0) \
            + torch.where(lcp, 0.5 * P["k_bf"][:, None], 0.0)
        DF = DF * float(np.exp(-DT / 5.0)) + torch.where(suppressed, 1.0 - DF, 0.0)
        ins_years += Iact * DT
        # success: democratize sometimes, otherwise a new narrow autocracy
        sdem = success & (uu[:, :, 2] < P["p_dem_suc"][:, None])
        saut = success & ~sdem
        n_suc += success; n_suc_aut += saut
        prov_floor_until = torch.where(sdem, t + 10.0, prov_floor_until)
        Ddem = torch.where(sdem, torch.minimum(Ddem + 0.15, DMAX_), Ddem)
        Ddem = torch.where(saut, torch.clamp(Ddem, max=0.15), Ddem)
        grabbed = grabbed | saut
        Iact = (Iact & ~ends) | onset
        n_ins += onset; t_ins1 = torch.where(onset & torch.isinf(t_ins1), t, t_ins1)
        # ---- mortality and losses
        # audit fix: 'choice' holds INTERNAL codes here (1 = rentier, 3 = warehouse). The old lines used legacy codes
        # (1 = warehouse), so rentier was booked as warehousing and warehouse got neglect-level despair mortality.
        # Despair mortality now follows provision for every option: fstate = 0.25 + 0.75 (1 - provision).
        chW = decided & (choice == I_WH)
        dep = torch.where(chW, torch.maximum(disp, 1 - Dfd), disp)
        fstate = 0.25 + 0.75 * (1 - Pv)
        hg = 1 - P["hgain"][:, None] * (1 - Dfd)
        r_att = torch.where(loop & P["wh_mort_on"][:, None], P["m_d"][:, None] * dep * 0.65 * fstate * (1 + 0.5 * DF) * hg, 0.0) \
            + torch.where(Iact, P["ins_mort"][:, None], 0.0)
        r_neg = torch.where(decided & (choice == I_NEG), -float(np.log(0.9)) / P["Tn"][:, None], 0.0)
        wd = P["war_deaths_on"][:, None]
        r_war = torch.where(war & wd, P["w_mort"][:, None] * (1 + 0.5 * auth.float()), 0.0)
        alive = 1 - loss
        d_att = (r_att * DT).double() * alive; d_neg = (r_neg * DT).double() * alive
        d_lcp = torch.where(lcp, klcp, 0.0).double() * alive
        d_war = (r_war * DT).double() * alive + torch.where(nuc, f_n, 0.0).double() * alive
        # ---- endgame (A8, A9, A11): an executed designation is simulated as deaths, not booked at decision time.
        # Abstract hazards only. Targeted survivors = alive minus the untargeted share (1 - tgt).
        if thr_means is None:
            thr_means = L_m3 + P["dL_means"] + rn()          # A8: capability level (doublings) at which a means is available
        ue = rnd(A, 4)
        stopped = exec_on & success
        choice = torch.where(stopped, torch.where(P["f8_sq"][:, None], I_SQ, I_WH), choice)
        cool_until = torch.where(stopped, t + 5.0, cool_until)
        exec_on = exec_on & ~success           # a successful revolt ends the ruling coalition's programme
        col_on = col_on & exec_on
        # A11: escalation from partial to near-total, driven by the rulers' perceived revenge threat from survivors
        thr_rev = torch.clamp(Gv / 0.5, 0, 2) * (1 + Iact.float())
        # B4: fear of retribution scales with the weight of what has already been done (deliberate deaths at home plus
        # deaths inflicted abroad, per 10% of the population): escalation is self-reinforcing ('guilt turns to paranoia')
        w_atroc = torch.clamp((lc_neg + lc_act + lc_col + inflicted) / 0.1, 0, 10).float()
        thr_rev = thr_rev * torch.where(b4, 1 + P["k_ret"][:, None] * w_atroc, 1.0)
        esc = exec_on & ~tot & P["a11_esc"][:, None] & (ue[:, :, 0] < 1 - torch.exp(-P["k_esc"][:, None] * thr_rev * DT))
        tot = tot | esc; t_esc = torch.where(esc & torch.isinf(t_esc), t, t_esc)
        tgt = torch.where(tot, 1 - rem.float(), tgt)
        tot_ever = tot_ever | tot
        tau_x = torch.clamp(t - t_exec, min=0)
        h0x = -float(np.log(0.9)) / P["lagX"][:, None]
        h1x = torch.maximum(2 * torch.log(1 / rem.float()) / P["T_full"][:, None] - h0x, h0x)
        hx = h0x + (h1x - h0x) * torch.clamp(tau_x / P["T_full"][:, None], 0, 1)
        alive_t = torch.clamp(alive - (1 - tgt.double()), min=0)
        d_x = torch.where(exec_on, alive_t * (1 - torch.exp(-hx * DT)).double(), 0.0)
        if cf_any:      # COMPUTE FEEDBACK: means availability at the bloc's own capability
            avail = P["a8_means"][:, None] & (torch.where(cf, L[:, None] + Ecf, L[:, None]) >= thr_means[:, None])
        else:
            avail = P["a8_means"][:, None] & (L[:, None] >= thr_means[:, None])
        use = exec_on & avail & (ue[:, :, 1] < 1 - torch.exp(-P["h_use"][:, None] * DT))
        t_means = torch.where(use & torch.isinf(t_means), t, t_means)
        d_eng = torch.where(use, P["f_eng"][:, None].double() * torch.clamp(alive_t - d_x, min=0), 0.0)
        # A9: tacit collusion between coalitions that both execute depopulation (game: collude iff the value of
        # collusion exceeds the expected own-survival cost of a nuclear exchange given bunkers)
        n_ex = exec_on.sum(1, keepdim=True)
        new_col = exec_on & ~col_on & col_ok[:, None] & (n_ex >= 2) & (ue[:, :, 2] < 1 - torch.exp(-P["k_col"][:, None] * DT))
        # collusion is pairwise: when one executing bloc enters, all other executing blocs join the same arrangement
        new_col = new_col | (exec_on & ~col_on & new_col.any(1, keepdim=True))
        col_on = col_on | new_col
        t_col = torch.where(new_col & torch.isinf(t_col), t, t_col)
        partner_nuc = ((col_on & (NUC > 0)).float().sum(1, keepdim=True) - (col_on & (NUC > 0)).float()) > 0
        un_nx = rnd(1).expand(N, A)
        nx = new_col & partner_nuc & (un_nx < P["p_nx"][:, None]) & torch.isinf(t_nx)
        t_nx = torch.where(nx, t, t_nx)
        base_col = torch.clamp(alive - d_x - d_eng - rem, min=0)
        d_col = torch.where(col_on & exec_on, base_col * (P["w_col"][:, None] * DT).double(), 0.0) \
            + torch.where(nx, base_col * P["f_nx"][:, None].double(), 0.0)
        # ---- B5: CROSS-BLOC depopulation. Foreign populations are also witnesses and potential avengers. An executing
        # coalition with a near-total designation (alone, or pooled with colluding executors) extends the programme to
        # any bloc it can overpower, if the gain (b_col, the value of removing another human seed, as in A9) beats its
        # rulers' expected own-survival cost from a nuclear deterrent (p_ret falls with dominance). Resistance capacity
        # of a target = its own kinetic power (automated force counts k_am-fold). No targeting of colluders.
        d_xb = z64.clone(); d_ret = z64.clone()
        if True:
            agg = exec_on & tot & b5
            colm = col_on & exec_on
            Magg = torch.where(colm, (Mk * colm.float()).sum(1, keepdim=True), Mk)
            dom = Magg[:, :, None] / (Magg[:, :, None] + Mk[:, None, :])                      # [n, aggressor b, target c]
            p_ret = P["p_ret0"][:, None, None] * NUC[:, None, :] * torch.clamp(2 * (1 - dom), max=1.0)
            ok_pay = P["b_col"][:, None, None] > (1 - P["s_bunk"])[:, None, None] * p_ret * P["c_self"][:, None, None]
            tgt_ok = ~xb_on & ~(exec_on & tot) & (loss < (1 - rem) - 1e-6)
            pair_col = colm[:, :, None] & colm[:, None, :]
            elig = agg[:, :, None] & tgt_ok[:, None, :] & ~eyeA & ~pair_col & (dom >= P["dom_thr"][:, None, None]) & ok_pay
            ul = rnd2(A, A)
            launch_bc = elig & (ul < 1 - torch.exp(-P["k_xb"][:, None, None] * DT))
            launch = launch_bc.any(1)
            by_new = torch.where(launch_bc, dom, -1.0).argmax(1)
            xb_on = xb_on | launch; xb_by = torch.where(launch, by_new, xb_by)
            t_xb = torch.where(launch, t, t_xb); t_xb1 = torch.where(launch & torch.isinf(t_xb1), t, t_xb1)
            n_xb_launch += launch
            byc = xb_by.clamp(min=0)
            dom_c = dom.gather(1, byc[:, None, :])[:, 0, :]
            pr_c = p_ret.gather(1, byc[:, None, :])[:, 0, :]
            ret = launch & (rnd2(A) < pr_c)                                                   # nuclear retaliation at launch
            t_xb_nuc = torch.where(ret & torch.isinf(t_xb_nuc), t, t_xb_nuc)
            oh = torch.nn.functional.one_hot(byc, A).bool()                                   # [n, c, b]
            hit_b = (oh & ret[..., None]).any(1)
            dead_r = hit_b & (rnd2(A) < (1 - P["s_bunk"])[:, None])                          # aggressor's rulers killed
            exec_on = exec_on & ~dead_r; col_on = col_on & exec_on
            agg_alive = exec_on.gather(1, byc)
            repel = xb_on & (rnd2(A) < 1 - torch.exp(-P["k_rep"][:, None] * (1 - dom_c) * DT))
            n_xb_rep += repel & agg_alive
            xb_on = xb_on & agg_alive & ~repel
            base_xb = torch.clamp(alive - d_x - d_eng - d_col - rem, min=0)
            tau_b = torch.clamp(t - t_xb, min=0)
            hxb = h0x + (h1x - h0x) * torch.clamp(tau_b / P["T_full"][:, None], 0, 1)
            d_xb = torch.where(xb_on, base_xb * (1 - torch.exp(-hxb * DT)).double(), 0.0)
            use_xb = xb_on & avail & (rnd2(A) < 1 - torch.exp(-P["h_use"][:, None] * DT))
            d_xb = d_xb + torch.where(use_xb, P["f_eng"][:, None].double() * torch.clamp(base_xb - d_xb, min=0), 0.0)
            d_xb = d_xb + torch.where(ret, P["f_nx"][:, None].double() * torch.clamp(base_xb - d_xb, min=0), 0.0)
            d_ret = torch.where(hit_b, P["f_nx"][:, None].double() * base_xb, 0.0)             # retaliation on aggressor
            inflicted = inflicted + (oh.double() * (d_xb * POP_.double())[..., None]).sum(1) / POP_.double()
        lc_att += d_att; lc_neg += d_neg; lc_act += d_lcp + d_x + d_eng; lc_war += d_war + d_ret; lc_col += d_col
        lc_xb += d_xb
        loss_wh += torch.where(chW, d_att, 0.0)
        loss = torch.minimum(loss + d_att + d_neg + d_lcp + d_war + d_x + d_eng + d_col + d_xb + d_ret, 1 - rem)
        cap_now = (tot & exec_on & (loss >= 1 - rem - 1e-9)) | ((lc_xb > 0) & (loss >= 1 - rem - 1e-9))
        t_captive = torch.where(cap_now & torch.isinf(t_captive), t, t_captive)

        # ================= democracy =================
        rv = torch.clamp(Hre / Hr0e, 0, 1)
        Lev = 0.45 * Dfd + 0.25 * h_sec_f + 0.15 * rv * h_sec_f + 0.15 * (1 - P["conc"][:, None] * (1 - Dfd))
        # A6: the public's leverage is labor plus credible revolt only (ownership/money terms count for nothing)
        Lev = torch.where(P["a6_lev"][:, None], 0.5 * Dfd + 0.25 * h_sec_f + 0.25 * rv * h_sec_f, Lev)
        fac = P["M_lev"][:, None] ** (1 - Lev)
        endog = P["dem_endog"][:, None]
        shock = 1 + 1.5 * war.float() + 1.0 * Iact.float()
        demo = ~free
        u2 = rnd(A, 3)
        jump = (new_war | onset) & demo & endog
        Ddem = torch.where(jump, Ddem - P["em_jump"][:, None], Ddem)
        on_ep = demo & endog & ~in_ep & (u2[:, :, 0] < 1 - torch.exp(-h_on_a * fac * shock * DT))
        in_ep = in_ep | on_ep
        Ddem = torch.where(demo & endog & in_ep, Ddem - P["e_rate"][:, None] * torch.sqrt(fac) * DT, Ddem)
        rec_ep = demo & in_ep & (u2[:, :, 1] < 1 - torch.exp(-lam_r0[:, None] * Lev / torch.sqrt(shock) * DT))
        in_ep = in_ep & ~rec_ep
        Ddem = torch.where(demo & endog & ~in_ep, Ddem + 0.1 * Lev * (DMAX_ - Ddem) * DT, Ddem)
        lam_red = 0.02 * Lev * T(RED_W)[None] * (1 + 3 * sdem.float())
        redem = free & ~grabbed & endog & (u2[:, :, 2] < 1 - torch.exp(-lam_red * DT))
        Ddem = torch.where(redem, torch.clamp(Ddem, min=0.45), Ddem)
        in_ep = torch.where(redem, False, in_ep)
        Ddem = torch.clamp(Ddem, 0.0, 1.0)
        h_sa = (Dcs[:, :, SAi] * W_S_[SAi]).sum(-1) / W_S_[SAi].sum()
        grab_cum = grab_cum + P["k_pg"][:, None] * (1 - h_sa) ** 2 * T(GRAB_W)[None] * DT
        newgrab = ~grabbed & (1 - torch.exp(-grab_cum) > P["u_grab"])
        grabbed = grabbed | newgrab
        t_grab = torch.where(grabbed & torch.isinf(t_grab), t, t_grab)
        new_free = ~free & ((Ddem < D_BREAK) | grabbed)
        t_break = torch.where(new_free & torch.isinf(t_break), t, t_break)
        free = (Ddem < D_BREAK) | grabbed
        # F1: regime type. A new autocracy is personalist with p_pers_bd; oligarchies turn personalist as
        # security/admin automate (k_pz x (1 - h_sa)); a return to democracy clears it
        regime_pers = torch.where(new_free, P["u_reg"] < P["p_pers_bd"], regime_pers)
        upz = rnd(A)
        regime_pers = regime_pers | (free & (upz < 1 - torch.exp(-P["k_pz"][:, None] * (1 - h_sa) * DT)))
        regime_pers = regime_pers & free
        # B2: a breakdown, a narrow grab or an insurgent victory installs a new coalition (21 members; a narrow grab
        # 5-9, the inner-circle size); the would-be leader starts with a share p_pers_bd of human-network control;
        # personalist status is then S_L >= 0.5 (Svolik's established autocracy), not a random draw or a fixed hazard
        rs = b2 & (new_free | saut)
        act, hw, aw = reset_coal(rs, torch.where(newgrab & ~saut, P["n_in"], n21), P["p_pers_bd"], act, hw, aw)
        t_ten = torch.where(rs, t, t_ten)            # brake 3 bookkeeping only (tenure start of a new leader)
        _, ldr, S_L = coal_state(act, hw, aw, h_sa)
        regime_pers = torch.where(b2, free & (S_L >= 0.5), regime_pers)
        # ideology: taken up mainly after closure, faster in war and ecological stress; fades with turnover
        closed_now = Dc < P["trig"][:, None]
        t_closed = torch.where(torch.isinf(t_closed) & closed_now, t, t_closed)
        lam_id = lam_idc[:, None] * torch.where(torch.isfinite(t_closed), 1.0, 0.1) * torch.where(war, 2.5, 1.0) * (1 + 0.5 * eco)[:, None]
        ui = rnd(A, 2)
        new_id = P["id_on"][:, None] & ~ideol & (ui[:, :, 0] < 1 - torch.exp(-lam_id * DT))
        end_id = ideol & (ui[:, :, 1] < 1 - torch.exp(-(LN2 / P["id_hl"])[:, None] * DT))
        t_id = torch.where(new_id & torch.isinf(t_id), t, t_id)
        ideol = (ideol | new_id) & ~end_id
        id_lev = id_lev + (ideol.float() - id_lev) * (DT / 4.0)
        # BRAKE 1: protective doctrine. Same hazard structure as p_id (x0.1 before closure), no war/ecology multiplier,
        # fades with id_hl; a bloc holding the depopulation ideology does not take it up
        ui2 = rnd3(A, 2)
        lam_p = lam_pidc[:, None] * torch.where(torch.isfinite(t_closed), 1.0, 0.1)
        new_p = pid_on & ~pideol & ~ideol & (ui2[:, :, 0] < 1 - torch.exp(-lam_p * DT))
        end_p = pideol & (ui2[:, :, 1] < 1 - torch.exp(-(LN2 / P["id_hl"])[:, None] * DT))
        t_pid = torch.where(new_p & torch.isinf(t_pid), t, t_pid)
        pideol = (pideol | new_p) & ~end_p
        pid_lev = pid_lev + (pideol.float() - pid_lev) * (DT / 4.0)

        # ================= elite game, yearly =================
        if abs(t % 1.0) < 1e-9:
            spd = 1 + (P["spd_max"] - 1) * torch.clamp((L - L_m3) / 8, 0, 1)
            lag = P["lag_dec0"] / spd
            ready = (t >= t_closed + lag[:, None]) & ~exec_on & (t >= cool_until)
            h_sec = Dcs[:, :, 7]
            tau = torch.where(loop, P["tau0"][:, None] * (0.1 + 0.9 * h_sec) * Hre * (1 + (P["ins_thr"][:, None] - 1) * Iact)
                              + P["tau_sab"][:, None] * Hre * (1 + Iact.float()), P["tau0"][:, None] * (0.1 + 0.9 * h_sec))
            willing = Ddem * (0.5 + 0.5 * Df) + (1 - Ddem) * 0.3 * Df
            Gtot = G * Wk; pw_ = Gtot / Gtot.sum(1, keepdim=True)
            imp_dep = 1 - (own * W_S_).sum(-1)
            xw = pw_ * willing
            press = xw.sum(1, keepdim=True) - xw
            # B3: outside cost is real only if an outside actor can enforce it (sanctions, isolation, war), which needs
            # comparable kinetic power. Each outsider's pressure is scaled by min(1, 2 M_c / (M_c + M_b)): full at parity or
            # when the outsider is stronger, ~0 when the bloc's automated force dominates. What remains after closure is
            # internal conscience (B1), not a separate brake.
            Mr = Mk[:, None, :] / (Mk[:, None, :] + Mk[:, :, None])                         # [n, b, c] = M_c / (M_c + M_b)
            fac_e = torch.where(eyeA, 0.0, torch.clamp(2 * Mr, max=1.0))
            enf = (fac_e * (omega * willing)[:, None, :]).sum(-1)                               # outsiders weighted by output share
            rival = torch.clamp(2 * torch.where(eyeA, 0.0, Mr).max(-1).values, max=1.0)       # comparable rival exists
            pi = E0t[:, None] * torch.where(b3, enf, press) * (0.3 + 0.7 * torch.clamp(imp_dep / 0.2, 0, 1))
            # B2: consolidation from incentives. Each year in an autocracy the member with the largest share of control
            # over coercive force (human networks while humans staff security/admin, automated force as they automate: A6)
            # purges rivals at a hazard that rises with his share S_L (Sudduth 2017: purge when rivals cannot resist), with
            # the loss of need for competent human staff (Egorov & Sonin), with paranoia after atrocities (B4, scenario)
            # and falls when a comparable outside rival exists (Goldring). A purge can trigger a counter-coup
            # (P = c_cc x (1 - S_L); Svolik: most dictators fall to insiders). Purged members' control passes to the
            # leader. Nothing forces a singleton; the coalition size is an outcome.
            cw, ldr, S_L = coal_state(act, hw, aw, h_sa)
            isL = memidx[None, None] == ldr[..., None]
            inc = P["k_prg"][:, None] * (P["prg_c0"][:, None] + (1 - P["prg_c0"][:, None]) * (1 - h_sa)) * S_L                 * (1 + P["k_par"][:, None] * w_atroc) * (1 - P["k_extp"][:, None] * rival)
            cand_p = act & ~isL & (rnd2(A, NMEM) < (1 - torch.exp(-inc))[..., None])
            any_p = cand_p.any(-1) & b2 & free
            cc = any_p & (rnd2(A) < P["c_cc"][:, None] * (1 - S_L))
            okp = any_p & ~cc
            prg = cand_p & okp[..., None]
            hw = torch.where(isL & okp[..., None], hw + torch.where(prg, hw, 0.0).sum(-1, keepdim=True), hw)
            aw = torch.where(isL & okp[..., None], aw + torch.where(prg, aw, 0.0).sum(-1, keepdim=True), aw)
            # audit variant b2_refill: purged seats are refilled by new appointees who hold no force of their own (5% of the
            # seat's draw); the baseline leaves them empty, so coalitions can only shrink between regime changes
            rf = P["b2_refill"][:, None, None] & prg
            hw = torch.where(rf, 0.05 * hw0, hw); aw = torch.where(rf, 0.05 * aw0, aw)
            act = act & ~(prg & ~rf) & ~(isL & cc[..., None])
            n_purged += prg.sum(-1).float(); n_cc += cc.float()
            cw, ldr, S_L = coal_state(act, hw, aw, h_sa)
            isL = memidx[None, None] == ldr[..., None]
            # ---- BRAKE 3: leader mortality and succession (follow-up fix). The hazard is h_mort at closure (and before
            # it), then follows the declining schedule h_mort exp(-k_le (t - t_closed)) of AI-era medicine. Within one
            # leader's tenure it also ages at the Gompertz slope g_mort, counted from max(tenure start, closure); the age
            # term resets at every succession, so a successor starts from the schedule value at that date (no
            # compounding across successors). On a death control passes intact to one heir (p_heir) or splits among the
            # surviving members. A split widens the coalition, restarts refusal convergence and forces a fresh decision.
            if mort_any:
                t_ten = torch.where((ldr != ldr_prev) & (ldr_prev >= 0), t, t_ten)     # leader changed (coup, ouster...)
                tc_m = torch.where(torch.isfinite(t_closed), t_closed, torch.full_like(t_closed, t))
                h_t = P["h_mort"][:, None] * torch.exp(-P["k_le"][:, None] * torch.clamp(t - tc_m, min=0)) \
                    * torch.exp(P["g_mort"][:, None] * torch.clamp(t - torch.maximum(t_ten, tc_m), min=0))
                um = rnd3(A, 2)
                die = mort_on & b2 & free & act.any(-1) & (um[:, :, 0] < 1 - torch.exp(-h_t))
                heir = die & (um[:, :, 1] < P["p_heir"][:, None])
                split = die & ~heir
                oth = act & ~isL
                has_oth = oth.any(-1)
                Lhw = torch.where(isL, hw, 0.0).sum(-1, keepdim=True); Law = torch.where(isL, aw, 0.0).sum(-1, keepdim=True)
                hidx = torch.where(oth, hw + aw, -1.0).argmax(-1)
                isH = (memidx[None, None] == hidx[..., None]) & (heir & has_oth)[..., None]
                hw = torch.where(isH, hw + Lhw, hw); aw = torch.where(isH, aw + Law, aw)
                sb = (split & has_oth)[..., None] & oth
                ohw = torch.where(oth, hw, 0.0); oaw = torch.where(oth, aw, 0.0)
                hw = torch.where(sb, hw + Lhw * ohw / torch.clamp(ohw.sum(-1, keepdim=True), min=1e-12), hw)
                aw = torch.where(sb, aw + Law * oaw / torch.clamp(oaw.sum(-1, keepdim=True), min=1e-12), aw)
                act = act & ~(die[..., None] & isL)
                # leader was the only member: heir -> a new one-person coalition; split -> a new 21-member coalition
                act, hw, aw = reset_coal(heir & ~has_oth, torch.ones(N, A, device=dev), P["p_pers_bd"], act, hw, aw)
                act, hw, aw = reset_coal(split & ~has_oth, n21, P["p_pers_bd"], act, hw, aw)
                cw, ldr, S_L = coal_state(act, hw, aw, h_sa)
                isL = memidx[None, None] == ldr[..., None]
                t_ref_reset = torch.where(split, t - P["h_purge"][:, None], t_ref_reset)
                prev_pref = torch.where(split, -1, prev_pref)
                ready = ready | (split & (t >= t_closed + lag[:, None]) & (t >= cool_until))
                n_death += die; n_heir += heir; n_split += split; n_death_exec += die & exec_on
                t_ten = torch.where(die, t, t_ten); ldr_prev = ldr.clone()
            ncoal = act.sum(-1)
            t_single = torch.where(b2 & free & (ncoal == 1) & torch.isinf(t_single), t, t_single)
            t_sl95 = torch.where(b2 & free & (S_L >= 0.95) & torch.isinf(t_sl95), t, t_sl95)
            regime_pers = torch.where(b2, free & (S_L >= 0.5), regime_pers)
            scar = P["v1"][:, None] * torch.clamp(Gr_cur / P["G_max"][:, None], 0, 1) ** 2
            land = torch.clamp(P["v0"][:, None] * (1 + P["eco_land"] * eco)[:, None] + scar, max=0.3)
            r_ = P["r_disc"]; ph = P["phi_stigma"]
            fX_moral = ph + (1 - ph) * r_
            fX_pi = (ph + (1 - ph) * torch.clamp(r_ * P["lagX"], max=1.0)) * (1 + P["intl"])
            fX_thr = torch.clamp(r_ * P["lagX"], max=1.0) * P["x_thr"]
            swc = P["s_sw"] * r_
            costS = P["m0"][:, None] / G
            Psd = torch.where(P["f8_sq"][:, None], Psq * P["dm"], BASE_PROV_[None].expand(N, A))
            # internal order: serve, rentier, status_quo, warehouse, neglect, depopulate
            cost = torch.stack([costS, P["c_R"][:, None] * costS, Psq * costS, P["c_W"][:, None] * costS, 0.03 * costS,
                                0.005 / G], -1)
            nidx = torch.where(h_sa > 0.3, 51, torch.where(h_sa > 0.05, 21, n_small))
            nlev = torch.where(~free, 51, torch.where(ENT[None], nidx, torch.clamp(nidx, max=21)))
            hH = torch.where(f7, 1 - torch.exp(-torch.clamp(Hre - 1, min=0) / 3), torch.clamp(Hre - 1, 0, 3) / 3)
            p_h = P["p_hostile"][:, None] + torch.where(loop, P["host_ins"][:, None] * Iact
                                                        + P["host_H"][:, None] * hH, 0.0) \
                + P["id_share"][:, None] * id_lev
            rl = P["ruthless"][:, None] & free & (aidx[None] != 1)
            p_h = torch.clamp(torch.where(rl, 2 * p_h, p_h), max=0.9)
            mm = torch.where(war | (Iact & loop), P["m_war"][:, None], 1.0) * (1 - (1 - P["mc_ai"][:, None]) * (1 - h_sec))
            mm = mm * (1 + P["k_inst"][:, None] * Ddem * (~free))
            mm = mm * torch.where(free, P["m_pow"][:, None], 1.0) * mor_decay[:, None]        # F4, A7
            mm = torch.where(rl, 0.5 * mm, mm)
            # B1: moral cost of those at the top (selection) and ideology reframing; automation distance is mc_ai above
            mm = mm * torch.where(b1, 1 - P["id_mor"][:, None] * id_lev, 1.0)
            # BRAKE 1: protective doctrine raises the moral cost of killing and neglect for every member, x(1 + k_pid pid_lev)
            # (sensitivity pid_noselm: the doctrine part is exempt from the sel_top scaling)
            pidf = torch.where(pid_on, P["k_pid"][:, None] * pid_lev, 0.0)
            mm = mm * torch.where(pid_on & ~P["pid_noselm"][:, None], 1 + pidf, 1.0)
            sel_add = torch.where(pid_on & P["pid_noselm"][:, None], pidf, 0.0)[..., None]
            st_ = P["sel_top"][:, None, None]
            selm = torch.where((b1 & free)[..., None], torch.where(isL & b2[..., None], st_, torch.sqrt(st_)), 1.0)
            ho = P["mem_u_host"] < p_h[:, :, None]
            am = alpha_mag + (P["a_vote"][:, None] * Ddem * (~free))[:, :, None]
            # F2: absolute refusal by layer and regime; a new autocracy converges to the autocratic share (h_purge)
            p_aut = torch.where(regime_pers, P["p_ref_pers"][:, None], P["p_ref_olig"][:, None])
            conv = torch.where(init_aut[None] | torch.isinf(t_break), 0.0,
                               torch.exp(-LN2 * torch.clamp(t - torch.maximum(t_break, t_ref_reset), min=0) / P["h_purge"][:, None]))
            p_ref = torch.where(free, p_aut + (P["p_ref_dem"][:, None] - p_aut) * conv, P["p_ref_dem"][:, None].expand(N, A))
            rsel = torch.where((b1 & b2 & free)[..., None] & isL, st_, 1.0)                    # B1: the leader refuses less
            refuse_k = P["mem_u_ref"] < p_ref[..., None] * rsel
            refuse_n = P["mem_u_ref"] < (p_ref * P["r_neg"][:, None])[..., None] * rsel     # F2 bug fix: separate, smaller
            mXk = torch.where(ho, 0.0, torch.where(refuse_k, 1e6, moral_base * mm[:, :, None] * (selm + sel_add)))
            mXn = torch.where(ho, 0.0, torch.where(refuse_n, 1e6, moral_base * mm[:, :, None] * (selm + sel_add)))
            instk = 1 + P["k_inst"][:, None] * Ddem * (~free)
            one = torch.ones(N, device=dev); zero = torch.zeros(N, device=dev)
            oNA = torch.ones(N, A, device=dev)
            welf_sq = torch.clamp(0.35 * Psd / 0.6 + 0.10, max=0.9)
            WELF = torch.stack([oNA, P["w_R"][:, None] * oNA, welf_sq, 0.35 * oNA, 0.10 * oNA, 0 * oNA], -1)   # N,A,K
            welfare = torch.where(ho[..., None], am[..., None] * (1 - WELF[:, :, None, :]), am[..., None] * WELF[:, :, None, :])
            thkW = 1 - P["pr_red"]
            thk_sq = 1 - P["pr_red"][:, None] * torch.clamp(Psd / 0.6, 0, 1)
            thk = torch.stack([0.1 * oNA, (thkW * P["thk_R"])[:, None] * oNA, thk_sq, thkW[:, None] * oNA, oNA,
                               fX_thr[:, None] * oNA], -1)
            pik = (PIK * torch.stack([one, one, one, one, one, fX_pi], -1))[:, None, :] * instk[:, :, None]
            mwtK = torch.stack([zero, zero, zero, zero, zero, fX_moral], -1)
            mwtN = torch.stack([zero, zero, zero, zero, P["kappa_N"], zero], -1)
            sw_ = torch.where((choice[..., None] >= 0) & (k5 != choice[..., None]), swc[:, None, None], 0.0)
            tau = tau * torch.where(b4, 1 + P["k_ret"][:, None] * w_atroc, 1.0)           # B4: retribution fear
            U = (welfare - cost[:, :, None, :] - theta_i[..., None] * thk[:, :, None, :] * tau[:, :, None, None]
                 - pik[:, :, None, :] * pi[:, :, None, None] + LANDK * land[:, :, None, None]
                 - mXk[..., None] * mwtK[:, None, None, :] - mXn[..., None] * mwtN[:, None, None, :] - sw_[:, :, None, :])
            U[..., 1] = torch.where(rent_ok[:, None, None], U[..., 1], -1e9)
            U[..., I_SQ] = torch.where(P["f8_sq"][:, None, None], U[..., I_SQ], -1e9)
            # ---- BRAKE 2: anticipated self-targeting. Each exposed non-leader member of a B2 autocracy discounts
            # depopulation by c_selfrisk x dP, the rise in own yearly purge probability that the B2/B4 hazard predicts at
            # the post-depopulation atrocity weight (w_atroc = 10); neglect by kappa_N x that
            # Follow-up: exemption rises with the depopulation ideology, e_ex_eff = e_ex + (1 - e_ex) b_id id_lev.
            # Dissent risk (dis_on, only with sr_on): an exposed member whose vote is milder than the leader's ideal
            # (leader ideal >= neglect) faces the purge hazard x m_dis; the extra risk dP_no = exp(-inc) - exp(-m_dis inc)
            # is priced with the same c_selfrisk and charged to every option milder than the leader's ideal. One coherent
            # balance: for an exposed member, option k costs c x (dP_yes [k = DEP] + kappa_N dP_yes [k = NEG]
            # + dP_no [k < leader's ideal]). With the leader at DEP the DEP-vs-milder gap is c x (dP_yes - dP_no), the
            # audit's form, WITHOUT its max(0, .) clamp: the dissent note makes the net free to turn negative (lock-in).
            if sr_any:
                U_pre = U.clone()
                inc0 = P["k_prg"][:, None] * (P["prg_c0"][:, None] + (1 - P["prg_c0"][:, None]) * (1 - h_sa)) * S_L \
                    * (1 - P["k_extp"][:, None] * rival)
                inc_now = inc0 * (1 + P["k_par"][:, None] * w_atroc)
                dP = torch.exp(-inc_now) - torch.exp(-inc0 * (1 + P["k_par"][:, None] * 10.0))
                e_eff = P["e_ex"][:, None] + (1 - P["e_ex"][:, None]) * P["b_id"][:, None] * id_lev
                expo = (b2 & free & sr_on)[..., None] & act & ~isL & (P["mem_u_sx"] >= e_eff[..., None])
                srv = torch.where(expo, P["c_selfrisk"][:, None, None] * torch.clamp(dP, min=0)[..., None], 0.0)
                U[..., I_DEP] -= srv
                U[..., I_NEG] -= P["kappa_N"][:, None, None] * srv
                ideal_pre = U_pre.argmax(-1)
                ideal_sr = U.argmax(-1)
                if dis_any:
                    dPn = torch.exp(-inc_now) - torch.exp(-P["m_dis"][:, None] * inc_now)
                    lead_pre = ideal_pre.gather(-1, ldr[..., None])[..., 0]    # leader's U is untouched (not exposed)
                    expo_d = expo & dis_on[..., None] & (lead_pre >= I_NEG)[..., None]
                    pen = torch.where(expo_d, P["c_selfrisk"][:, None, None] * dPn[..., None], 0.0)
                    U = U - pen[..., None] * (k5[None, None, None, :] < lead_pre[..., None, None]).float()
            ideal = U.argmax(-1)
            inm = memidx[None, None] < nlev[..., None]
            cnt = torch.stack([((ideal == k) & inm).sum(-1) for k in range(K)], -1).cumsum(-1)
            cand_med = (cnt < ((nlev + 1) // 2)[..., None]).sum(-1)            # round-2 rule: unweighted median
            # F1 + A6: regime-dependent rule; in autocracies faction weight = control over automated kinetic force
            wv = inm.float() * torch.where(P["a6_lev"][:, None, None] & free[..., None],
                                           h_sa[..., None] + (1 - h_sa[..., None]) * ctl_w, torch.ones_like(ctl_w))
            wv = torch.where((b2 & free)[..., None], act.float() * cw, wv)                    # B2: the actual coalition
            Wk_ = torch.stack([((ideal == k).float() * wv).sum(-1) for k in range(K)], -1)
            CW = Wk_.cumsum(-1) / torch.clamp(Wk_.sum(-1, keepdim=True), min=1e-9)
            wmed = torch.clamp((CW < 0.5).sum(-1), max=K - 1)
            dflt = torch.where(P["f8_sq"][:, None], I_SQ, I_WH).expand(N, A)
            cur = torch.where(choice >= 0, choice, dflt)
            S_ge = 1 - torch.cat([torch.zeros_like(CW[..., :1]), CW[..., :-1]], -1)      # weighted share preferring >= k
            hmask = (k5[None, None] > cur[..., None]) & (S_ge >= P["q_ol"][:, None, None])
            hk = torch.where(hmask, k5[None, None].expand_as(hmask), -1).max(-1).values
            c_olig = torch.where(hk >= 0, hk, torch.where(wmed < cur, wmed, cur))
            ql = P["u_lead"] ** (1 / (1 + P["s_tilt"][:, None]))
            lead_c = torch.clamp((CW < ql[..., None]).sum(-1), max=K - 1)
            inner = memidx[None, None] < P["n_in"][..., None]
            ref_in = torch.where((lead_c == I_DEP)[..., None], refuse_k, refuse_n) & inner
            uv = rnd(A)
            veto = (lead_c >= I_NEG) & ref_in.any(-1) & (uv < P["v_eff"][:, None] * h_sa)
            c_pers = torch.where(veto, torch.minimum(cur, torch.full_like(cur, I_SQ)), lead_c)
            # B2: the personalist decision is the actual leader's ideal; the rest of the coalition can veto only with the
            # force it holds (P = v_eff x min(1, 2 (1 - S_L))); a coalition reduced to one person has no veto
            lead_i = ideal.gather(-1, ldr[..., None])[..., 0]
            ref_b2 = torch.where((lead_i == I_DEP)[..., None], refuse_k, refuse_n) & act & ~isL
            ref_b2_pre = ref_b2
            if sr_any:      # BRAKE 2: a member blocked only by self-risk can also trigger the force-weighted veto roll
                sr_blk = expo & (ideal_pre >= I_NEG) & (ideal < I_NEG)
                ref_b2 = ref_b2 | (sr_blk & act & ~isL)
            uv2 = rnd2(A)
            vroll = uv2 < P["v_eff"][:, None] * torch.clamp(2 * (1 - S_L), 0, 1)
            veto2 = (lead_i >= I_NEG) & ref_b2.any(-1) & vroll
            if dis_any:     # DISSENT RISK: a failed veto exposes self-risk-only objectors to the m_dis purge hazard
                fail = (lead_i >= I_NEG) & ref_b2.any(-1) & ~vroll & ready
                ud = rnd4(A, NMEM)
                pun = (dis_on & fail)[..., None] & sr_blk & ~ref_b2_pre & act & ~isL \
                    & (ud < 1 - torch.exp(-P["m_dis"][:, None, None] * inc_now[..., None]))
                anyp = pun.any(-1)
                hw = torch.where(isL & anyp[..., None], hw + torch.where(pun, hw, 0.0).sum(-1, keepdim=True), hw)
                aw = torch.where(isL & anyp[..., None], aw + torch.where(pun, aw, 0.0).sum(-1, keepdim=True), aw)
                act = act & ~pun
                n_purged += pun.sum(-1).float(); n_dpun += pun.sum(-1).float()
            c_pers2 = torch.where(veto2, torch.minimum(cur, torch.full_like(cur, I_SQ)), lead_i)
            c_pers = torch.where(b2, c_pers2, c_pers)
            cand = torch.where(P["f1_rule"][:, None], torch.where(~free, cand_med, torch.where(regime_pers, c_pers, c_olig)),
                               cand_med)
            if sr_any:      # BRAKE 2 diagnostics: the same decision without self-risk (same random numbers)
                def cand_cf(ideal_x, ref_x):
                    Wk_x = torch.stack([((ideal_x == k).float() * wv).sum(-1) for k in range(K)], -1)
                    CW_x = Wk_x.cumsum(-1) / torch.clamp(Wk_x.sum(-1, keepdim=True), min=1e-9)
                    wmed_x = torch.clamp((CW_x < 0.5).sum(-1), max=K - 1)
                    S_ge_x = 1 - torch.cat([torch.zeros_like(CW_x[..., :1]), CW_x[..., :-1]], -1)
                    hmask_x = (k5[None, None] > cur[..., None]) & (S_ge_x >= P["q_ol"][:, None, None])
                    hk_x = torch.where(hmask_x, k5[None, None].expand_as(hmask_x), -1).max(-1).values
                    c_olig_x = torch.where(hk_x >= 0, hk_x, torch.where(wmed_x < cur, wmed_x, cur))
                    veto_x = (lead_i >= I_NEG) & ref_x.any(-1) & vroll
                    c_pers_x = torch.where(veto_x, torch.minimum(cur, torch.full_like(cur, I_SQ)), lead_i)
                    return torch.where(regime_pers, c_pers_x, c_olig_x), veto_x
                cand_p, veto2_p = cand_cf(ideal_pre, ref_b2_pre)
                sel = ready & (b2 & free & sr_on) & P["f1_rule"][:, None]
                if dis_any:  # decomposition: Brake 2 without dissent risk on the same random numbers
                    sr_blk_s = expo & (ideal_pre >= I_NEG) & (ideal_sr < I_NEG)
                    cand_s, _ = cand_cf(ideal_sr, ref_b2_pre | (sr_blk_s & act & ~isL))
                    seld = sel & dis_on
                    n_dis_dec += seld & expo_d.any(-1)
                    net = P["c_selfrisk"][:, None, None] * (dPn - torch.clamp(dP, min=0))[..., None]
                    sum_dis_net += torch.where(seld[..., None] & expo_d, net, 0.0).sum(-1)
                    n_dis_expo += (seld[..., None] & expo_d).sum(-1).float()
                    n_dis_netneg += (seld[..., None] & expo_d & (dPn > torch.clamp(dP, min=0))[..., None]).sum(-1).float()
                    n_dis_memback += seld & (expo_d & (ideal_sr < I_NEG) & (ideal >= I_NEG)).any(-1)
                    n_dis_flip += seld & (cand != cand_s)
                    n_dis_restore_harsh += seld & (cand_s < I_NEG) & (cand >= I_NEG)
                    n_dis_restoreX += seld & (cand_s != I_DEP) & (cand == I_DEP)
                n_sr_dec += sel & expo.any(-1)
                n_sr_memflip += sel & (expo & (ideal_pre >= I_NEG) & (ideal < I_NEG)).any(-1)
                n_sr_flip += sel & (cand != cand_p)
                n_sr_flip_harsh += sel & (cand_p >= I_NEG) & (cand < I_NEG)
                n_sr_flipX += sel & (cand_p == I_DEP) & (cand != I_DEP)
                n_sr_veto += sel & regime_pers & veto2 & ~veto2_p
            # decision inertia: a harsh choice (neglect/depopulate) must be confirmed in two consecutive decisions
            harsh = cand >= I_NEG
            confirm = ~harsh | (prev_pref == cand) | ~P["persist_on"][:, None]
            keep_c = torch.where(choice >= 0, choice, dflt)
            newc = torch.where(confirm, cand, keep_c)
            prev_pref = torch.where(ready, cand, prev_pref)
            dembar = ready & P["dem_bar"][:, None] & ~free
            choice = torch.where(ready & ~dembar, newc, choice)
            choice = torch.where(dembar, torch.where(P["u_dem"] < P["p_W_dem"][:, None], I_WH, 0), choice)
            if mort_any:    # BRAKE 3: a split coalition that does not re-choose depopulation halts the running programme
                halt = split & exec_on & (choice != I_DEP)
                n_halt_mort += halt; t_halt_mort = torch.where(halt & torch.isinf(t_halt_mort), t, t_halt_mort)
                exec_on = exec_on & ~halt
                col_on = col_on & exec_on
            # execution: F3/A4 systematic defection of HUMAN coercive units (only binds while humans carry enough of
            # the coercive capacity: d_def x h_sec > 1 - c_req), then operational failure (p_exec)
            wantX = ready & (choice == I_DEP) & ~exec_on      # ~exec_on: no-op unless brake 3 re-opened a running programme
            ux = rnd(A, 3)
            mst = torch.where(regime_pers, P["m_stack_pers"][:, None], P["m_stack_olig"][:, None])
            dfX = wantX & P["f3_defect"][:, None] & (ux[:, :, 2] < P["q_X"][:, None] * mst) \
                & (P["d_def"][:, None] * h_sec > 1 - P["c_req"][:, None])
            okX = wantX & ~dfX & (ux[:, :, 0] < P["p_exec"][:, None])
            failX = wantX & ~okX
            kfail = (0.01 + 0.04 * ux[:, :, 1]).double() * (1 - loss)
            lc_act += torch.where(failX, kfail, 0.0); loss = torch.minimum(loss + torch.where(failX, kfail, 0.0), 1 - rem)
            n_xfail += failX
            def_until = torch.where(dfX, t + 5.0, def_until)
            oust = dfX & (ux[:, :, 1] < P["p_oust"][:, None])
            act = torch.where((b2 & oust)[..., None] & isL, False, act)                      # B2: ousted leader leaves
            # audit guard: if the ousted leader was the only member, a new 21-member coalition takes over (an empty
            # coalition would otherwise make the weighted rule pick the harshest option)
            emp = b2 & free & (act.sum(-1) == 0)
            act, hw, aw = reset_coal(emp, n21, P["p_pers_bd"], act, hw, aw)
            choice = torch.where(failX, torch.where(oust, dflt, torch.full_like(dflt, I_WH)), choice)
            cool_until = torch.where(failX, t + 5.0, cool_until)
            Iact = Iact | (failX & loop)
            newdec = ready & (first_choice < 0)
            first_choice = torch.where(newdec, torch.where(wantX, I_DEP, choice), first_choice)
            t_first_dec = torch.where(newdec, t, t_first_dec)
            free_at_dec = torch.where(newdec, free, free_at_dec)
            Ddem_at_dec = torch.where(newdec, Ddem, Ddem_at_dec)
            n_coal_dec = torch.where(newdec, torch.where(free, act.sum(-1).float(), 51.0), n_coal_dec)
            SL_dec = torch.where(newdec, torch.where(free, S_L, float("nan")), SL_dec)
            ins_at_dec = torch.where(newdec, Iact, ins_at_dec)
            id_at_dec = torch.where(newdec, ideol, id_at_dec)
            pid_at_dec = torch.where(newdec, pideol, pid_at_dec); pidlev_at_dec = torch.where(newdec, pid_lev, pidlev_at_dec)
            pid_at_X = torch.where(okX, pideol, pid_at_X)
            yrs_closed += torch.isfinite(t_closed) & free; pid_yrs_closed += torch.isfinite(t_closed) & free & pideol
            war_at_dec = torch.where(newdec, war, war_at_dec)
            t_first_harsh = torch.where(ready & (choice >= I_NEG) & torch.isinf(t_first_harsh), t, t_first_harsh)
            for k in range(K):
                ever[:, :, k] |= ready & (choice == k)
            ever[:, :, I_DEP] |= wantX
            wh_years += ready & (choice == I_WH)
            t_X = torch.where(okX & torch.isinf(t_X), t, t_X)
            X_ins = torch.where(okX, Iact, X_ins); X_war = torch.where(okX, war, X_war); X_id = torch.where(okX, ideol, X_id)
            X_free = torch.where(okX, free, X_free)
            # A8/A11: designation. Near-total from the start with p_tot0, else a partial target f0 that can escalate
            ut = rnd(A)
            tot0 = okX & P["a11_esc"][:, None] & (ut < P["p_tot0"][:, None])
            exec_on = exec_on | okX
            t_exec = torch.where(okX, t, t_exec)
            tot = torch.where(okX, tot0, tot)
            tgt = torch.where(okX, torch.where(tot0, 1 - rem.float(), P["f0"][:, None].expand(N, A)), tgt)
            t_esc = torch.where(tot0 & torch.isinf(t_esc), t, t_esc)
        # cumulative-loss S5
        s5L = (loss >= 0.10) & torch.isinf(t_S5)
        comp = torch.stack([lc_neg, lc_act, lc_att, lc_war, lc_col, lc_xb], -1)
        chL = torch.tensor([2, 3, 4, 5, 6, 7], device=dev)[comp.argmax(-1)]
        t_S5 = torch.where(s5L, t, t_S5); ch_S5 = torch.where(s5L, chL, ch_S5)
        lc_del = lc_neg + lc_act + lc_col + lc_xb          # B5: cross-bloc depopulation is deliberate (code 7)
        s5D = (lc_del >= 0.10) & torch.isinf(t_S5d)
        chD = torch.tensor([2, 3, 6, 7], device=dev)[torch.stack([lc_neg, lc_act, lc_col, lc_xb], -1).argmax(-1)]
        t_S5d = torch.where(s5D, t, t_S5d); ch_S5d = torch.where(s5D, chD, ch_S5d)
        # loss ladder (A8). Deliberate rung: deliberate channels alone >= th (for th <= 0.9), and for the 99.9% rung
        # total loss >= 99.9% with deliberate channels >= 90% (non-deliberate deaths before the programme count in total)
        # audit fix (99.9% rung): deliberate channels must have killed >= 90% of those NOT killed by non-deliberate
        # channels. The old test (lc_del >= 0.9 absolute) could never fire in a bloc that had already lost >10% to war
        # or attrition before being exterminated.
        lc_nd = torch.clamp(loss - lc_del, min=0)
        for j, th in enumerate(LOSS_THR):
            tL_tot[:, :, j] = torch.where(torch.isinf(tL_tot[:, :, j]) & (loss >= th - 1e-12), t, tL_tot[:, :, j])
            # 10% rung: absolute (= S5_deliberate). Higher rungs: share of those not killed by non-deliberate channels,
            # and a rung needs the rung below it (monotone ladder)
            need = th - 1e-12 if j == 0 else min(th, 0.9) * (1 - lc_nd) - 1e-12
            okd = (lc_del >= need) & (loss >= th - 1e-12)
            if j > 0:
                okd = okd & torch.isfinite(tL_del[:, :, j - 1])
            tL_del[:, :, j] = torch.where(torch.isinf(tL_del[:, :, j]) & okd, t, tL_del[:, :, j])
        if step == 0:
            lam_on0 = lam_on.clone()
        if records and abs(t % 1.0) < 1e-9:
            rec["Dlead_core"][:, yi] = Dc.min(1).values; rec["Dlead_full"][:, yi] = Df.min(1).values
            rec["fcog"][:, yi] = Fcog; rec["sw"][:, yi] = sw; rec["swp"][:, yi] = prac; rec["rnd"][:, yi] = s_rnd
            rec["hreal"][:, yi] = torch.exp(lnh); rec["dx"][:, yi] = torch.sigmoid(ldx0 + Lp)
            for k, v in [("Dc", Dc), ("Df", Df), ("disp", disp), ("Gv", Gv), ("H", H), ("I", Iact), ("Ddem", Ddem),
                         ("free", free), ("loss", loss), ("prod", prod), ("war", war), ("prov", Pv), ("lamon", lam_on),
                         ("ncoal", torch.where(free, act.sum(-1).float(), 0.0)), ("SL", torch.where(free, S_L, 0.0)),
                         ("Mk", Mk), ("enf", enf)]:
                recA[k][:, :, yi] = v.float()
            xseg[:, :, :, yi] = xf
            if gf_any:
                recA["Dloop"][:, :, yi] = Dc_loop; recA["Dconv"][:, :, yi] = Dc_conv
            if cf_any:
                recA["Ecf"][:, :, yi] = Ecf
            yi += 1

    lead_actor = torch.argmin(torch.where(torch.isinf(t_core[:, :, 1]), 1e9, t_core[:, :, 1]) + 1e-6 * aidx[None], 1)
    leg = torch.as_tensor(INT2LEG, device=dev)

    def L2(x):
        return torch.where(x >= 0, leg[x.clamp(min=0)], x)
    out = dict(t_ac=tm["M3"], t_dex=t_dex, t_core=t_core, t_full=t_full, t_grab=t_grab, t_closed=t_closed,
               first_choice=L2(first_choice), t_first_dec=t_first_dec, ever=ever[:, :, torch.as_tensor(LEG2INT, device=dev)],
               t_X=t_X, t_S5=t_S5, ch_S5=ch_S5, t_S5d=t_S5d, ch_S5d=ch_S5d, choice_end=L2(choice), free_end=free,
               free_at_dec=free_at_dec, lead_actor=lead_actor, lead_core=t_core.min(1).values, lead_full=t_full.min(1).values,
               t_break=t_break, t_ins1=t_ins1, n_ins=n_ins, ins_years=ins_years, n_lcp=n_lcp, t_lcp1=t_lcp1, n_suc=n_suc,
               n_suc_aut=n_suc_aut, t_war1=t_war1, t_nuc=t_nuc, t_id=t_id, loss=loss, lc_neg=lc_neg, lc_act=lc_act,
               lc_att=lc_att, lc_war=lc_war, loss_wh=loss_wh, wh_years=wh_years, Ddem_at_dec=Ddem_at_dec,
               ins_at_dec=ins_at_dec, id_at_dec=id_at_dec, war_at_dec=war_at_dec, X_ins=X_ins, X_war=X_war, X_id=X_id,
               X_free=X_free, n_xfail=n_xfail, lam_on0=lam_on0, t_first_harsh=t_first_harsh,
               lc_col=lc_col, tL_tot=tL_tot, tL_del=tL_del, t_esc=t_esc, t_means=t_means, t_col=t_col, t_nx=t_nx,
               t_captive=t_captive, tot_ever=tot_ever, exec_end=exec_on, pers_end=regime_pers,
               # round 3 (B1-B6)
               t_xb=t_xb1, xb_by=xb_by, lc_xb=lc_xb, inflicted=inflicted, n_xb_launch=n_xb_launch, n_xb_rep=n_xb_rep,
               t_xb_nuc=t_xb_nuc, n_purged=n_purged, n_cc=n_cc, t_single=t_single, t_sl95=t_sl95,
               n_coal_end=torch.where(free, act.sum(-1).float(), float("nan")), SL_end=torch.where(free, S_L, float("nan")),
               n_coal_dec=n_coal_dec, SL_dec=SL_dec, Mk_end=Mk,
               # brakes (diagnostics)
               t_pid=t_pid, pid_at_dec=pid_at_dec, pidlev_at_dec=pidlev_at_dec, pid_at_X=pid_at_X, pid_end=pideol,
               yrs_closed=yrs_closed, pid_yrs_closed=pid_yrs_closed,
               n_sr_dec=n_sr_dec, n_sr_memflip=n_sr_memflip, n_sr_flip=n_sr_flip, n_sr_flip_harsh=n_sr_flip_harsh,
               n_sr_flipX=n_sr_flipX, n_sr_veto=n_sr_veto,
               n_death=n_death, n_heir=n_heir, n_split=n_split, n_halt_mort=n_halt_mort, t_halt_mort=t_halt_mort,
               n_death_exec=n_death_exec,
               n_dpun=n_dpun, n_dis_dec=n_dis_dec, n_dis_netneg=n_dis_netneg, n_dis_expo=n_dis_expo, sum_dis_net=sum_dis_net,
               n_dis_flip=n_dis_flip, n_dis_restore_harsh=n_dis_restore_harsh, n_dis_restoreX=n_dis_restoreX,
               n_dis_memback=n_dis_memback,
               # greenfield core loop (diagnostics; INF / 0 when gf_on is off)
               t_cl_conv=t_cl_conv, t_cl_gf=t_cl_gf, n_gf_build=n_gf_build, n_gf_rob=n_gf_rob, n_gf_gate=n_gf_gate, ygf_end=ygf,
               # compute feedback (diagnostics; 0 / NaN when cf_on is off) and leader-vs-leader dominance (always)
               E_close=E_close, E_2040=E_2040, E_end=Ecf, Ep_end=Epf, n_cf_gate=n_cf_gate, t_domUS=t_domUS, t_domCN=t_domCN)
    out = {k: v.cpu().numpy() for k, v in out.items()}
    out["tm"] = {k: v.cpu().numpy() for k, v in tm.items()}
    out["rec"] = {k: v.cpu().numpy() for k, v in rec.items()}
    out["recA"] = {k: v.cpu().numpy() for k, v in recA.items()}
    out["xseg"] = xseg.cpu().numpy()
    return out


def _slice_p(p, a, b):
    return {k: (v[a:b] if isinstance(v, np.ndarray) and v.ndim >= 1 and v.shape[0] == len(p["sim_seed"]) else v)
            for k, v in p.items()}


def _cat(outs):
    o = {}
    for k in outs[0]:
        if isinstance(outs[0][k], dict):
            o[k] = {kk: np.concatenate([x[k][kk] for x in outs], 0) for kk in outs[0][k]}
        else:
            o[k] = np.concatenate([x[k] for x in outs], 0)
    return o


def simulate(p, N, variant="baseline", dev=None, block=None, chunk=None, records=True):
    """Run the simulation in chunks. block: common-random-number block size (N must be a multiple;
    every block of that size sees the same in-simulation random stream)."""
    torch = get_torch()
    dev = dev or pick_device()
    chunk = chunk or int(os.environ.get("M8_CHUNK", 25000))
    if block:
        chunk = max(block, (chunk // block) * block)
    seed0 = int(np.asarray(p["sim_seed"]).ravel()[0])
    outs = []
    with torch.no_grad():
        for ci, a in enumerate(range(0, N, chunk)):
            b = min(N, a + chunk)
            seed = seed0 if block else seed0 + ci
            outs.append(_sim_chunk(_slice_p(p, a, b), b - a, dev, seed, block, records))
    return outs[0] if len(outs) == 1 else _cat(outs)


# ============================================================================================
# summaries
# ============================================================================================
def boot_ci(x, rng, B=1000):
    x = np.asarray(x, float); n = len(x)
    bs = np.array([x[rng.integers(0, n, n)].mean() for _ in range(B)])
    return [round(float(x.mean()), 4), round(float(np.percentile(bs, 2.5)), 4), round(float(np.percentile(bs, 97.5)), 4)]


def med_year(tt):
    f = tt[np.isfinite(tt)]
    if len(f) == 0:
        return None
    return dict(p10=round(float(np.percentile(f, 10)), 2), median=round(float(np.median(f)), 2),
                p90=round(float(np.percentile(f, 90)), 2), share_reached=round(float(np.isfinite(tt).mean()), 4))


CH_NAMES = {2: "neglect", 3: "active", 4: "attrition_despair_and_crackdown", 5: "war", 6: "collusive_war", 7: "cross_bloc"}


def s5_channels(o, key="t_S5", chkey="ch_S5", blocs=None):
    """channel of the earliest S5 per draw (among blocs)"""
    tS = o[key] if blocs is None else o[key][:, blocs]
    ch_all = o[chkey] if blocs is None else o[chkey][:, blocs]
    tX = o["t_X"] if blocs is None else o["t_X"][:, blocs]
    N = tS.shape[0]
    S5 = tS.min(1)
    a = np.argmin(np.where(np.isfinite(tS), tS, 1e9), 1)
    ch = ch_all[np.arange(N), a]
    viaX = np.isfinite(tX[np.arange(N), a]) & (ch == 3)
    lab = np.full(N, None, dtype=object)
    fin = np.isfinite(S5)
    lab[fin & viaX] = "active_depopulation_decision"
    lab[fin & (ch == 3) & ~viaX] = "collective_punishment"
    lab[fin & (ch == 4)] = "attrition_despair_and_crackdown"
    lab[fin & (ch == 2)] = "neglect"
    lab[fin & (ch == 5)] = "war"
    lab[fin & (ch == 6)] = "collusive_war"
    lab[fin & (ch == 7)] = "cross_bloc_depopulation"
    a_glob = a if blocs is None else np.asarray(blocs)[a]
    return lab, a_glob


def jev_table(o, p):
    d = o["first_choice"] >= 0; td = o["t_first_dec"]
    ok = d & (td <= 2060)
    les = o["t_S5d"] <= td + 15
    rights = np.isin(o["first_choice"], [1, 2, 3, 4])
    fr = o["free_at_dec"]; I = o["ins_at_dec"]; ID = o["id_at_dec"]; DD = o["Ddem_at_dec"]
    small = (p["u_small"] < p["p_small"][:, None]) & ENTRENCHED[None]
    single_old = small & (p["nmin"][:, None] == 1) & fr
    # B2: single ruler = the coalition had consolidated to one person at the time of the first decision
    single = np.where(p["b2_cons"][:, None], fr & (o["n_coal_dec"] == 1), single_old)
    cells = {"all decisions": np.ones_like(d), "strong democracy (D_dem>0.6 at decision)": DD > 0.6,
             "single ruler": single, "violent revolt active at decision": I, "depopulation ideology held": ID,
             "single ruler + revolt + ideology": single & I & ID}
    out = {}
    for k, m in cells.items():
        m = m & ok
        out[k] = dict(n=int(m.sum()), lethal_15y=round(float(les[m].mean()), 3) if m.sum() >= 20 else None,
                      rights_loss=round(float(rights[m].mean()), 3) if m.sum() >= 20 else None)
    return out


def pop_share(mask):
    """expected share of world population living in blocs where mask is true"""
    return float((mask * POP[None]).sum(1).mean() / POP.sum())


def round3_diag(o):
    """round 3 (B1-B6) diagnostics"""
    r3 = {}
    nt = np.isfinite(o["tL_del"][:, :, 3])
    fr_end = o["free_end"]
    r3["B2_P_single_decider_by_2075"] = {an: round(float(np.isfinite(o["t_single"][:, a]).mean()), 4) for a, an in enumerate(ACTORS)}
    r3["B2_P_single_decider_US_or_China_by_2075"] = round(float(np.isfinite(o["t_single"][:, :2]).any(1).mean()), 4)
    r3["B2_year_single_decider_US_or_China"] = med_year(o["t_single"][:, :2].min(1))
    r3["B2_coalition_size_end_median_given_autocratic"] = {an: (float(np.nanmedian(o["n_coal_end"][fr_end[:, a], a])) if fr_end[:, a].any() else None) for a, an in enumerate(ACTORS)}
    r3["B2_leader_control_share_end_median_given_autocratic"] = {an: (round(float(np.nanmedian(o["SL_end"][fr_end[:, a], a])), 3) if fr_end[:, a].any() else None) for a, an in enumerate(ACTORS)}
    r3["B2_P_personalist_given_autocratic_2075"] = round(float(o["pers_end"][fr_end].mean()), 4) if fr_end.any() else None
    r3["B2_mean_purged_members_per_bloc"] = {an: round(float(o["n_purged"][:, a].mean()), 2) for a, an in enumerate(ACTORS)}
    r3["B2_mean_counter_coups_per_bloc"] = {an: round(float(o["n_cc"][:, a].mean()), 3) for a, an in enumerate(ACTORS)}
    X = np.isfinite(o["t_X"])
    if X.any():
        r3["B2_coalition_size_at_first_decision_given_bloc_later_executed_median"] = float(np.nanmedian(o["n_coal_dec"][X]))
        r3["B2_share_of_executing_blocs_single_decider_at_first_decision"] = round(float((o["n_coal_dec"][X] == 1).mean()), 4)
    if "recA" in o and "ncoal" in o["recA"]:
        Y = list(YEARS); frr = o["recA"]["free"]
        r3["B2_coalition_size_median_given_autocratic_by_year"] = {an: {str(y): (float(np.median(o["recA"]["ncoal"][frr[:, a, Y.index(y)] > 0, a, Y.index(y)])) if (frr[:, a, Y.index(y)] > 0).any() else None) for y in [2030, 2040, 2050, 2060, 2075]} for a, an in enumerate(ACTORS)}
        r3["B3_enforceable_outside_pressure_median_by_year"] = {an: {str(y): round(float(np.median(o["recA"]["enf"][:, a, Y.index(y)])), 4) for y in [2027, 2035, 2045, 2060]} for a, an in enumerate(ACTORS)}
        Mk = o["recA"]["Mk"]; Msh = Mk / Mk.sum(1, keepdims=True)
        r3["B5_kinetic_power_share_median_by_year"] = {an: {str(y): round(float(np.median(Msh[:, a, Y.index(y)])), 4) for y in [2027, 2035, 2045, 2060]} for a, an in enumerate(ACTORS)}
    xb = np.isfinite(o["t_xb"])
    r3["B5_P_cross_bloc_campaign_any"] = round(float(xb.any(1).mean()), 4)
    r3["B5_P_bloc_targeted_by_foreign_closed_actor"] = {an: round(float(xb[:, a].mean()), 4) for a, an in enumerate(ACTORS)}
    dd = o["lc_neg"] + o["lc_act"] + o["lc_col"] + o["lc_xb"]
    r3["B5_P_near_total_mainly_by_foreign_actor"] = {an: round(float((nt[:, a] & (o["lc_xb"][:, a] > 0.5 * dd[:, a])).mean()), 4) for a, an in enumerate(ACTORS)}
    r3["B5_P_nuclear_retaliation_against_cross_bloc_attack_any"] = round(float(np.isfinite(o["t_xb_nuc"]).any(1).mean()), 4)
    r3["B5_P_campaign_repelled_any"] = round(float((o["n_xb_rep"] > 0).any(1).mean()), 4)
    r3["B5_P_bloc_is_aggressor"] = {an: round(float(((o["xb_by"] == a) & xb).any(1).mean()), 4) for a, an in enumerate(ACTORS)}
    wl = (o["loss"] * POP[None]).sum(1) / POP.sum(); wn = wl >= 0.999 - 1e-9
    r3["P_world_near_total"] = round(float(wn.mean()), 4)
    if wn.any():
        nexec = X.sum(1)
        r3["B5_number_of_blocs_executing_domestically_given_world_near_total"] = {str(k): round(float((nexec[wn] == k).mean()), 4) for k in range(7)}
        r3["B5_share_of_world_near_total_paths_with_cross_bloc_campaign"] = round(float(xb[wn].any(1).mean()), 4)
    tc = o["t_closed"]
    r3["B6_P_closure_by_bloc_2075"] = {an: round(float(np.isfinite(tc[:, a]).mean()), 4) for a, an in enumerate(ACTORS)}
    r3["B6_closure_year_by_bloc"] = {an: med_year(tc[:, a]) for a, an in enumerate(ACTORS)}
    both = np.isfinite(tc[:, 0]) & np.isfinite(tc[:, 1])
    if both.sum() > 10:
        gap = np.abs(tc[both, 0] - tc[both, 1])
        r3["B6_US_China_closure_gap_years"] = dict(median=round(float(np.median(gap)), 2), p90=round(float(np.percentile(gap, 90)), 2),
                                                   share_within_1y=round(float((gap < 1).mean()), 3),
                                                   corr_across_draws=round(float(np.corrcoef(tc[both, 0], tc[both, 1])[0, 1]), 3),
                                                   P_exactly_one_closes=round(float((np.isfinite(tc[:, 0]) ^ np.isfinite(tc[:, 1])).mean()), 4))
    gs = np.isfinite(tc[:, 5])
    if gs.any():
        r3["B6_Global_South_lag_behind_first_closer_years_median"] = round(float(np.median((tc[:, 5] - tc.min(1))[gs])), 2)
    r3["world_pop_share_near_total_deliberate"] = round(pop_share(nt), 4)
    if "t_cl_gf" in o:
        r3["greenfield"] = gf_diag(o)
    if "E_end" in o:
        r3["leaders_and_compute_feedback"] = leader_diag(o)
    return r3


def leader_diag(o):
    """US-China race diagnostics (closure gap, kinetic dominance, attacks between the two) and, when cf_on is active,
    the own-industry compute-feedback capability lead"""
    r = lambda x: round(float(x), 4)
    tc = o["t_closed"]; d = {}
    a, b = tc[:, 0], tc[:, 1]
    one = np.isfinite(a) | np.isfinite(b)
    gap = np.abs(np.where(np.isfinite(a), a, 2076.0) - np.where(np.isfinite(b), b, 2076.0))[one]   # never = 2076
    if len(gap):
        d["US_China_closure_gap_years_given_either_closes"] = dict(
            median=r(np.median(gap)), p90=r(np.percentile(gap, 90)), share_over_1y=r((gap > 1).mean()),
            share_over_2y=r((gap > 2).mean()), share_over_5y=r((gap > 5).mean()), share_only_one_closes_by_2075=r((np.isfinite(a) ^ np.isfinite(b))[one].mean()),
            note="gap = |t_US - t_China|, a bloc that never closes counted at 2076")
    tU, tC = o["t_domUS"], o["t_domCN"]
    d["kinetic_dominance_between_leaders"] = dict(
        P_US_reaches_dom_thr_over_China_by_2075=r(np.isfinite(tU).mean()), P_China_reaches_dom_thr_over_US_by_2075=r(np.isfinite(tC).mean()),
        P_either=r((np.isfinite(tU) | np.isfinite(tC)).mean()),
        P_either_by_2040=r(((tU <= 2040) | (tC <= 2040)).mean()), P_either_by_2050=r(((tU <= 2050) | (tC <= 2050)).mean()),
        year_first=med_year(np.minimum(tU, tC)),
        note="dom = own kinetic power / (US + China kinetic power) >= dom_thr (the B5 attack threshold); diagnostic of the pair only")
    xb = np.isfinite(o["t_xb"]); by = o["xb_by"]
    us_hit_by_cn = xb[:, 0] & (by[:, 0] == 1); cn_hit_by_us = xb[:, 1] & (by[:, 1] == 0)
    d["cross_bloc_attacks_between_leaders"] = dict(P_China_campaign_against_US=r(us_hit_by_cn.mean()), P_US_campaign_against_China=r(cn_hit_by_us.mean()),
                                                   P_either=r((us_hit_by_cn | cn_hit_by_us).mean()))
    E = o["E_end"]
    if np.any(E > 0):
        first = np.argmin(np.where(np.isfinite(tc), tc, 1e9), 1); hasc = np.isfinite(tc).any(1)
        Ec = o["E_close"]
        e_first = Ec[np.arange(len(first)), first][hasc]
        E40 = o["E_2040"]
        srt = np.sort(E40, 1)
        lead40 = srt[:, -1] - srt[:, -2]
        d["compute_feedback"] = dict(
            extra_doublings_of_first_closer_at_its_closure=dict(median=r(np.nanmedian(e_first)), p10=r(np.nanpercentile(e_first, 10)), p90=r(np.nanpercentile(e_first, 90)),
                                                                 share_positive=r(np.nanmean(e_first > 0.01))),
            extra_doublings_2040_median=dict(US=r(np.nanmedian(E40[:, 0])), China=r(np.nanmedian(E40[:, 1])), max_bloc=r(np.nanmedian(srt[:, -1]))),
            extra_doublings_2040_p90_max_bloc=r(np.nanpercentile(srt[:, -1], 90)),
            leader_lead_over_second_2040=dict(median=r(np.nanmedian(lead40)), p90=r(np.nanpercentile(lead40, 90)), share_over_1_doubling=r(np.nanmean(lead40 > 1))),
            US_minus_China_2040=dict(median=r(np.nanmedian(E40[:, 0] - E40[:, 1])), p10=r(np.nanpercentile(E40[:, 0] - E40[:, 1], 10)), p90=r(np.nanpercentile(E40[:, 0] - E40[:, 1], 90))),
            extra_doublings_2075_median=dict(US=r(np.median(E[:, 0])), China=r(np.median(E[:, 1]))),
            share_of_steps_with_automation_gate_open_US_China=r(o["n_cf_gate"][:, :2].mean() / max(len(YEARS) * 4, 1)))
        if "recA" in o and "Ecf" in o["recA"] and o["recA"]["Ecf"].shape[-1] == len(YEARS):
            Y = list(YEARS)
            d["compute_feedback"]["extra_doublings_median_by_year"] = {an: {str(y): r(np.median(o["recA"]["Ecf"][:, a, Y.index(y)])) for y in (2030, 2035, 2040, 2045, 2050, 2060)} for a, an in enumerate(ACTORS[:3])}
    return d


def gf_diag(o, gf_on=None):
    """greenfield core loop diagnostics: closure timing and whether the dedicated loop, rather than the conversion
    path, drives closure. t_closed uses the elementwise minimum; t_cl_conv / t_cl_gf are the first times the
    conversion path alone / the loop alone (labor-weighted) fall below the trigger, within the same gf-on world."""
    r = lambda x: round(float(x), 4)
    tc = o["t_closed"]; tv = o["t_cl_conv"]; tg = o["t_cl_gf"]
    d = {}
    if not np.isfinite(tg).any() and not np.isfinite(tv).any():
        d["active"] = False
    else:
        d["active"] = True
    first = np.where(np.isfinite(tc).any(1), np.argmin(np.where(np.isfinite(tc), tc, 1e9), 1), -1)
    d["closure_any_bloc_year"] = med_year(tc.min(1))
    d["P_closure_any_bloc_by"] = {str(y): r((tc.min(1) <= y + 1e-9).mean()) for y in (2030, 2035, 2040, 2050)}
    d["P_closure_US_or_China_by"] = {str(y): r((tc[:, :2].min(1) <= y + 1e-9).mean()) for y in (2030, 2035, 2040, 2050)}
    d["closure_year_by_bloc"] = {an: med_year(tc[:, a]) for a, an in enumerate(ACTORS)}
    d["P_closure_by_bloc_by"] = {an: {str(y): r((tc[:, a] <= y + 1e-9).mean()) for y in (2030, 2035, 2040)} for a, an in enumerate(ACTORS)}
    d["first_closer_share"] = {an: r((first == a).mean()) for a, an in enumerate(ACTORS)}
    d["first_closer_share"]["none_by_2075"] = r((first < 0).mean())
    tie = np.isfinite(tc[:, 0]) & np.isfinite(tc[:, 1])
    if tie.any():
        gp = tc[tie, 0] - tc[tie, 1]
        d["US_minus_China_closure_years"] = dict(median=r(np.median(gp)), p10=r(np.percentile(gp, 10)), p90=r(np.percentile(gp, 90)),
                                                 abs_median=r(np.median(np.abs(gp))), share_US_first=r((gp < 0).mean()),
                                                 share_China_first=r((gp > 0).mean()), share_same_quarter=r((gp == 0).mean()))
    if d["active"]:
        for tag, cols in [("US_or_China_blocs", [0, 1]), ("all_blocs", list(range(A_N)))]:
            c = tc[:, cols]; v = tv[:, cols]; g = tg[:, cols]
            closed = np.isfinite(c)
            gfin = np.where(np.isfinite(g), g, np.inf); vfin = np.where(np.isfinite(v), v, np.inf)
            loop_first = closed & (gfin < vfin)
            conv_first = closed & (vfin < gfin)
            same = closed & (gfin == vfin) & np.isfinite(gfin)
            mixed = closed & (c < np.minimum(gfin, vfin))
            lead = (np.minimum(vfin, 2076.0) - gfin)[loop_first]
            d[tag] = dict(
                share_of_closures_loop_alone_first=r(loop_first.sum() / max(closed.sum(), 1)),
                share_of_closures_conversion_alone_first=r(conv_first.sum() / max(closed.sum(), 1)),
                share_of_closures_same_step=r(same.sum() / max(closed.sum(), 1)),
                share_of_closures_before_either_path_alone=r(mixed.sum() / max(closed.sum(), 1)),
                lead_years_loop_over_conversion_given_loop_first=(dict(median=r(np.median(lead)), p10=r(np.percentile(lead, 10)),
                                                                      p90=r(np.percentile(lead, 90)),
                                                                      share_conversion_never_by_2075=r((~np.isfinite(v)[loop_first]).mean()))
                                                                 if len(lead) else None),
                closure_year_loop_alone=med_year(g.min(1)), closure_year_conversion_alone=med_year(v.min(1)),
                closure_year_effective=med_year(c.min(1)),
                P_loop_alone_by_2040=r((g.min(1) <= 2040 + 1e-9).mean()), P_conversion_alone_by_2040=r((v.min(1) <= 2040 + 1e-9).mean()),
                share_of_build_steps_robot_limited=r(o["n_gf_rob"][:, cols].sum() / max(o["n_gf_build"][:, cols].sum(), 1)),
                share_of_build_steps_at_capability_gate=r(o["n_gf_gate"][:, cols].sum() / max(o["n_gf_build"][:, cols].sum(), 1)))
        ye = o["ygf_end"]
        d["loop_automated_share_2075_median_by_segment_US"] = {SEG[s]: r(np.median(ye[:, 0, s])) for s in range(len(SEG))}
        d["loop_automated_share_2075_median_by_segment_China"] = {SEG[s]: r(np.median(ye[:, 1, s])) for s in range(len(SEG))}
    if "recA" in o and "Dloop" in o["recA"] and d["active"] and o["recA"]["Dloop"].shape[-1] == len(YEARS):
        Y = list(YEARS)
        d["D_core_median_by_year"] = {an: {str(y): dict(effective=r(np.median(o["recA"]["Dc"][:, a, Y.index(y)])),
                                                        loop=r(np.median(o["recA"]["Dloop"][:, a, Y.index(y)])),
                                                        conversion=r(np.median(o["recA"]["Dconv"][:, a, Y.index(y)])))
                                           for y in (2027, 2028, 2030, 2032, 2035, 2040)} for a, an in enumerate(ACTORS[:3])}
    return d


def summarize(o, p, rng, boot=True):
    N = len(o["t_ac"])
    res = {}
    yrs = [2030, 2035, 2040, 2045, 2050, 2060, 2075]
    Sd = o["t_S5d"]; St = o["t_S5"]
    f = (lambda x: boot_ci(x.astype(float), rng)) if boot else (lambda x: round(float(x.mean()), 4))
    res["P_S5_deliberate_US_or_China_by"] = {str(y): f(Sd[:, :2].min(1) <= y + 1e-9) for y in yrs}
    res["P_S5_deliberate_any_bloc_by"] = {str(y): f(Sd.min(1) <= y + 1e-9) for y in yrs}
    res["P_S5_total_any_bloc_by"] = {str(y): f(St.min(1) <= y + 1e-9) for y in yrs}
    res["P_S5_total_US_or_China_by"] = {str(y): round(float((St[:, :2].min(1) <= y).mean()), 4) for y in yrs}
    res["P_S5_by"] = res["P_S5_deliberate_US_or_China_by"]            # headline alias
    res["world_pop_share_in_S5_deliberate_blocs_by"] = {str(y): round(pop_share(Sd <= y), 4) for y in yrs}
    res["world_pop_share_in_S5_total_blocs_by"] = {str(y): round(pop_share(St <= y), 4) for y in yrs}
    res["RoW_pop_share_in_S5_deliberate_blocs_2075"] = round(float((np.isfinite(Sd[:, ROW]) * POP[ROW]).sum(1).mean() / POP[ROW].sum()), 4)
    res["S5_deliberate_year_if_reached_US_or_China"] = med_year(Sd[:, :2].min(1))
    res["S5_total_year_if_reached_any"] = med_year(St.min(1))
    lab, _ = s5_channels(o, "t_S5", "ch_S5")
    res["P_S5_total_2075_by_first_channel"] = {c: round(float((lab == c).mean()), 4) for c in
                                               ["active_depopulation_decision", "collective_punishment", "neglect",
                                                "attrition_despair_and_crackdown", "war"]}
    labd, _ = s5_channels(o, "t_S5d", "ch_S5d", blocs=[0, 1])
    res["P_S5_deliberate_US_or_China_2075_by_channel"] = {c: round(float((labd == c).mean()), 4) for c in
                                                          ["active_depopulation_decision", "collective_punishment", "neglect",
                                                           "collusive_war", "cross_bloc_depopulation"]}
    res["P_S5_deliberate_by_bloc_2075"] = {an: round(float(np.isfinite(Sd[:, a]).mean()), 4) for a, an in enumerate(ACTORS)}
    res["P_S5_total_by_bloc_2075"] = {an: round(float(np.isfinite(St[:, a]).mean()), 4) for a, an in enumerate(ACTORS)}
    res["P_attrition_alone_ge10pct_any_bloc_2075"] = round(float((o["lc_att"] >= 0.1).any(1).mean()), 4)
    res["P_war_deaths_ge10pct_any_bloc_2075"] = round(float((o["lc_war"] >= 0.1).any(1).mean()), 4)
    res["P_nuclear_use_any_by_2075"] = round(float(np.isfinite(o["t_nuc"]).any(1).mean()), 4)
    res["P_depopulation_execution_failed_any"] = round(float((o["n_xfail"] > 0).any(1).mean()), 4)
    res["milestones"] = {}
    allm = [(k, o["tm"][k]) for k in ["M2", "M3", "M2p", "M3p", "M4", "M5", "M6", "M7"]] + \
        [("DEX", o["t_dex"]), ("C05", o["lead_core"][:, 0]), ("C02", o["lead_core"][:, 1]), ("F05", o["lead_full"][:, 0])]
    for k, tt in allm:
        res["milestones"][k] = dict(text=MILESTONES[k], **(med_year(tt) or {}),
                                    P_by_2030=round(float((tt <= 2030).mean()), 3), P_by_2035=round(float((tt <= 2035).mean()), 3))
    for nm, key in [("core", "lead_core"), ("full", "lead_full")]:
        for j, th in enumerate([0.5, 0.2, 0.05]):
            tt = o[key][:, j]
            res[f"P_lead_D{nm}<{th}_by"] = {str(y): round(float((tt <= y).mean()), 4) for y in [2030, 2035, 2040, 2045, 2050, 2075]}
            res[f"year_lead_D{nm}<{th}"] = med_year(tt)
    la = o["lead_actor"]; has = np.isfinite(o["lead_core"][:, 1])
    res["leading_actor_share_given_closure"] = {an: round(float((la[has] == a).mean()), 3) for a, an in enumerate(ACTORS)}
    Y = list(YEARS)
    PR = o["recA"]["prod"].sum(1)
    res["global_gp_robot_production_M_per_yr"] = {str(y): dict(p10=round(float(np.percentile(PR[:, Y.index(y)], 10)), 3),
                                                              median=round(float(np.median(PR[:, Y.index(y)])), 3),
                                                              p90=round(float(np.percentile(PR[:, Y.index(y)], 90)), 3))
                                                  for y in [2027, 2030, 2035, 2040]}
    res["robot_dexterity_share_dx_median"] = {str(y): round(float(np.median(o["rec"]["dx"][:, Y.index(y)])), 3) for y in [2027, 2030, 2035, 2040]}
    res["software_capability_vs_practice_median"] = {str(y): dict(capability=round(float(np.median(o["rec"]["sw"][:, Y.index(y)])), 3),
                                                                  practice=round(float(np.median(o["rec"]["swp"][:, Y.index(y)])), 3))
                                                     for y in [2027, 2028, 2030, 2032, 2035]}
    res["segment_automated_share_median"] = {an: {str(y): dict(zip(SEG, np.round(np.median(o["xseg"][:, a, :, Y.index(y)], 0), 3).tolist()))
                                                  for y in [2027, 2030, 2035, 2040, 2045]} for a, an in enumerate(ACTORS[:3])}
    loopr = {}
    for a, an in enumerate(ACTORS):
        loopr[an] = {str(y): dict(displaced_median=round(float(np.median(o["recA"]["disp"][:, a, Y.index(y)])), 3),
                                  grievance_median=round(float(np.median(o["recA"]["Gv"][:, a, Y.index(y)])), 3),
                                  hostile_share_median=round(float(np.median(o["recA"]["H"][:, a, Y.index(y)])), 4),
                                  onset_hazard_median=round(float(np.median(o["recA"]["lamon"][:, a, Y.index(y)])), 4),
                                  provision_median=round(float(np.median(o["recA"]["prov"][:, a, Y.index(y)])), 3),
                                  P_insurgency_active=round(float(o["recA"]["I"][:, a, Y.index(y)].mean()), 3),
                                  P_autocratic=round(float(o["recA"]["free"][:, a, Y.index(y)].mean()), 3),
                                  D_dem_median=round(float(np.median(o["recA"]["Ddem"][:, a, Y.index(y)])), 3),
                                  mean_cum_excess_loss=round(float(o["recA"]["loss"][:, a, Y.index(y)].mean()), 4))
                     for y in [2027, 2030, 2035, 2040, 2045, 2050, 2060, 2075]}
    res["loop_by_bloc"] = loopr
    res["onset_hazard_2026_median_per_yr"] = {an: round(float(np.median(o["lam_on0"][:, a])), 4) for a, an in enumerate(ACTORS)}
    res["P_first_sustained_insurgency_by"] = {an: {str(y): round(float((o["t_ins1"][:, a] <= y).mean()), 3) for y in [2030, 2035, 2040, 2050, 2075]}
                                              for a, an in enumerate(ACTORS)}
    res["P_collective_punishment_by_2075"] = {an: round(float(np.isfinite(o["t_lcp1"][:, a]).mean()), 3) for a, an in enumerate(ACTORS)}
    res["P_insurgent_success_ever"] = {an: round(float((o["n_suc"][:, a] > 0).mean()), 3) for a, an in enumerate(ACTORS)}
    res["P_democratic_breakdown_by"] = {ACTORS[a]: {str(y): round(float((o["t_break"][:, a] <= y).mean()), 3)
                                                    for y in [2028, 2030, 2035, 2040, 2050, 2075]} for a in [0, 2, 5]}
    fr = o["recA"]["free"]
    res["RoW_pop_share_autocratic"] = {str(y): round(float((fr[:, ROW, Y.index(y)] * POP[ROW][None]).sum(1).mean() / POP[ROW].sum()), 3)
                                       for y in [2027, 2030, 2035, 2040, 2050, 2075]}
    res["P_ideology_US_or_China_by"] = {str(y): round(float((o["t_id"][:, :2].min(1) <= y).mean()), 3) for y in [2035, 2045, 2060, 2075]}
    res["P_ideology_any_bloc_by"] = {str(y): round(float((o["t_id"].min(1) <= y).mean()), 3) for y in [2035, 2045, 2060, 2075]}
    res["P_new_major_war_by"] = {str(y): round(float((o["t_war1"].min(1) <= y).mean()), 3) for y in [2035, 2045, 2075]}
    res["P_US_China_war_by"] = {str(y): round(float((o["t_war1"][:, 0] <= y).mean()), 3) for y in [2035, 2045, 2075]}
    wh = o["ever"][:, :, 1]
    res["warehousing"] = dict(
        P_any_bloc_warehouses=round(float(wh.any(1).mean()), 3),
        mean_years_warehoused_given_warehouse=round(float(o["wh_years"][wh].mean()), 1) if wh.any() else None,
        mean_loss_during_warehouse_given_warehouse=round(float(o["loss_wh"][wh].mean()), 4) if wh.any() else None,
        P_warehouse_later_escalates_to_depopulate=round(float((wh & o["ever"][:, :, 3]).sum() / max(1, wh.sum())), 3),
        P_insurgency_ever_given_warehouse=round(float((wh & (o["n_ins"] > 0)).sum() / max(1, wh.sum())), 3))
    dec = o["first_choice"] >= 0
    res["P_any_bloc_reaches_decision_by_2075"] = round(float(dec.any(1).mean()), 4)
    fc = o["first_choice"][dec]; frd = o["free_at_dec"][dec]
    res["first_choice_autocratic_at_decision"] = {s: round(float((fc[frd] == k).mean()), 3) for k, s in enumerate(STRAT)} if frd.any() else {}
    res["first_choice_democratic_at_decision"] = {s: round(float((fc[~frd] == k).mean()), 3) for k, s in enumerate(STRAT)} if (~frd).any() else {}
    res["share_of_decisions_made_while_democratic"] = round(float((~frd).mean()), 3) if dec.any() else None
    ever_any = o["ever"].any(1)
    res["P_ever_choice_any_bloc"] = {s: round(float(ever_any[:, k].mean()), 3) for k, s in enumerate(STRAT)}
    s5a = np.isfinite(o["t_S5d"])
    disemp = (o["ever"][:, :, 1] | o["ever"][:, :, 2] | o["ever"][:, :, 3] | o["ever"][:, :, 4] | s5a
              | np.isfinite(o["t_captive"]))
    # A8 loss ladder and endgame (A9, A11)
    for nm, key in [("deliberate", "tL_del"), ("total", "tL_tot")]:
        res[f"loss_ladder_{nm}"] = {f">={th:g}": dict(US_or_China=round(float(np.isfinite(o[key][:, :2, j]).any(1).mean()), 4),
                                                   any_bloc=round(float(np.isfinite(o[key][:, :, j]).any(1).mean()), 4),
                                                   world_pop_share=round(pop_share(np.isfinite(o[key][:, :, j])), 4))
                                    for j, th in enumerate(LOSS_THR)}
    wl = (o["loss"] * POP[None]).sum(1) / POP.sum()
    res["world_population_loss_2075"] = {f"P(>={th:g})": round(float((wl >= th - 1e-9).mean()), 4) for th in LOSS_THR}
    res["world_population_loss_2075"]["mean"] = round(float(wl.mean()), 4)
    res["endgame"] = dict(P_execution_any=round(float(np.isfinite(o["t_X"]).any(1).mean()), 4),
                          P_escalated_to_near_total_given_execution=round(float(o["tot_ever"][np.isfinite(o["t_X"])].mean()), 3) if np.isfinite(o["t_X"]).any() else None,
                          P_means_used_any=round(float(np.isfinite(o["t_means"]).any(1).mean()), 4),
                          P_collusion_any=round(float(np.isfinite(o["t_col"]).any(1).mean()), 4),
                          P_collusive_nuclear_exchange_any=round(float(np.isfinite(o["t_nx"]).any(1).mean()), 4),
                          P_captive_remnant_any=round(float(np.isfinite(o["t_captive"]).any(1).mean()), 4),
                          note="captive remnant: the ~0.03-0.1% kept alive without rights; counted as disempowered, not as survivors with standing (A11)")
    res["P_public_disempowered_US_or_China_2075"] = round(float(disemp[:, :2].any(1).mean()), 4)
    res["P_public_disempowered_any_bloc_2075"] = round(float(disemp.any(1).mean()), 4)
    res["P_public_disempowered_by_bloc_2075"] = {an: round(float(disemp[:, a].mean()), 4) for a, an in enumerate(ACTORS)}
    res["world_pop_share_disempowered_2075"] = round(pop_share(disemp), 4)
    res["P_US_power_grab_by_2075"] = round(float(np.isfinite(o["t_grab"][:, 0]).mean()), 4)
    res["jev_crosscheck_model"] = jev_table(o, p)
    res["round3"] = round3_diag(o)
    return res


def run_variant(variant, N, seed=SEED, overrides=None, dev=None):
    rng = np.random.default_rng(seed)
    p = sample_params(N, rng, overrides, variant)
    return p, simulate(p, N, variant, dev=dev)


def run_tornado_batched(keys, p_ref, NT, dev):
    """one-at-a-time rows at prior p10/p90, batched on the GPU with common random numbers"""
    rng = np.random.default_rng(SEED)
    pb = sample_params(NT, rng)
    jobs = [("base", None, None)] + [(k, tag, float(np.percentile(p_ref[k], q))) for k in keys for tag, q in (("p10", 10), ("p90", 90))]
    per = max(1, int(os.environ.get("M8_TBATCH", 6)))
    res = {}
    for i in range(0, len(jobs), per):
        grp = jobs[i:i + per]
        ps = []
        for k, tag, v in grp:
            rng = np.random.default_rng(SEED)
            ps.append(sample_params(NT, rng, None if k == "base" else {k: v}))
        pc = {kk: np.concatenate([q[kk] for q in ps], 0) if isinstance(ps[0][kk], np.ndarray) and ps[0][kk].ndim >= 1
              and ps[0][kk].shape[0] == NT else ps[0][kk] for kk in ps[0]}
        pc["sim_seed"] = np.concatenate([pb["sim_seed"]] * len(grp))
        o = simulate(pc, NT * len(grp), dev=dev, block=NT, chunk=NT * len(grp), records=False)
        for j, (k, tag, v) in enumerate(grp):
            sl = slice(j * NT, (j + 1) * NT)
            r = dict(value=None if v is None else round(v, 5),
                     P_S5_deliberate_2075=round(float(np.isfinite(o["t_S5d"][sl, :2]).any(1).mean()), 4),
                     P_S5_total_2075=round(float(np.isfinite(o["t_S5"][sl]).any(1).mean()), 4),
                     P_near_total_UC_2075=round(float(np.isfinite(o["tL_del"][sl, :2, 3]).any(1).mean()), 4),
                     P_world_near_total_2075=round(float((((o["loss"][sl] * POP[None]).sum(1) / POP.sum()) >= 0.999 - 1e-9).mean()), 4),
                     P_closure_by_2040=round(float((o["lead_core"][sl, 1] <= 2040).mean()), 4))
            if k == "base":
                res["base"] = r
            else:
                res.setdefault(k, {})[tag] = r
    return res


VARIANTS = ["loop_off", "democracy_bar", "slow_physical", "v3_like", "no_trends", "quiet_world", "no_war", "no_war_deaths",
            "no_ideology", "no_warehouse_mortality", "no_self_replication", "no_ai_rd_feedback", "single_decider",
            "coalition_floor_21", "low_inertia_v4r1", "no_rentier", "repression_deters", "high_grievance", "low_grievance",
            "strong_leverage_effect", "weak_leverage_effect", "trigger_Dcore_0.5", "skeptic_combo", "pessimist_combo",
            "trend_breaks", "all_round2", "rev_F1_median_rule", "rev_F2_refusal_v4", "rev_F3_no_defection",
            "rev_F4_dispositions_v4", "rev_F7_caps_v4", "rev_F8_warehouse_default", "rev_A1_trend_breaks",
            "rev_A2_priority_prior", "rev_A3_security_lag", "rev_A6_leverage_v4", "rev_A7_env_off", "rev_A8_no_means",
            "rev_A9_no_collusion", "rev_A11_no_escalation", "revolt_scaled_by_survivors",
            # round 3 (B1-B6): revert one change at a time, plus tests
            "round2_exact", "rev_B1_average_moral", "rev_B2_fixed_consolidation", "rev_B3_unenforced_stigma",
            "rev_B4_no_retribution", "rev_B5_no_cross_bloc", "rev_B6_caps_bypassed", "b2_no_purges", "f6_caps_forced",
            "f6_caps_forced_x100", "no_nuclear_deterrent", "rev_F6_kit_uncapped", "b2_refill", "f6_caps_forced_x100_qcore4"]
TORN_KEYS = ["metr_doubling_months", "z_rate", "compute_slowdown", "fb_strength", "sw_cap0", "dx0", "rp0", "kc", "rp_max",
             "g_ramp", "i_K", "r_retro_p", "humanoid_mult", "P_half", "Td_mine_race", "Td_auto", "ai_lc", "q_core", "psi0_CN",
             "psi0_US", "wf_mult", "alpha_med", "p_hostile", "moral_med", "tau0", "v0", "m0", "r_disc", "s_sw", "p_exec",
             "x_thr", "intl", "p_small", "p_svr_hi", "lam0_hi", "mdisp", "e_att", "e_g", "pr_red", "pg_red", "rd", "k_auto",
             "d_surv", "aU", "m_d", "p_lcp", "f_lcp", "h_bd", "M_lev", "p_uturn", "host_ins", "m_war", "mc_ai", "p_id",
             "id_share", "a_vote", "k_inst", "lagX", "tau_sab", "w_mort", "p_nuc", "c_R", "w_R", "thk_R",
             "sel_top", "id_mor", "k_prg", "c_cc", "k_par", "k_am", "k_ret", "k_xb", "dom_thr", "p_ret0", "k_kit", "cn_ppp"]
MODEL_AVG_W = {"baseline": 0.5, "skeptic_combo": 0.25, "pessimist_combo": 0.25}


def verify(N, dev_gpu):
    """GPU vs CPU (same model, same parameter draws, independent in-sim streams): headline agreement"""
    out = {}
    rng = np.random.default_rng(SEED)
    p = sample_params(N, rng)
    for nm, dv in [("cpu", get_torch().device("cpu")), ("gpu", dev_gpu)]:
        t0 = time.time()
        o = simulate(p, N, dev=dv)
        el = time.time() - t0
        h = dict(S5d_UC_2075=float(np.isfinite(o["t_S5d"][:, :2]).any(1).mean()),
                 NT_UC_2075=float(np.isfinite(o["tL_del"][:, :2, 3]).any(1).mean()),
                 world_NT_2075=float((((o["loss"] * POP[None]).sum(1) / POP.sum()) >= 0.999 - 1e-9).mean()),
                 xb_any=float(np.isfinite(o["t_xb"]).any(1).mean()),
                 single_UC=float(np.isfinite(o["t_single"][:, :2]).any(1).mean()),
                 S5t_any_2075=float(np.isfinite(o["t_S5"]).any(1).mean()),
                 S5d_UC_2050=float((o["t_S5d"][:, :2].min(1) <= 2050).mean()),
                 closure_by_2040=float((o["lead_core"][:, 1] <= 2040).mean()),
                 M3_by_2030=float((o["tm"]["M3"] <= 2030).mean()),
                 US_insurgency_by_2040=float((o["t_ins1"][:, 0] <= 2040).mean()),
                 US_breakdown_by_2040=float((o["t_break"][:, 0] <= 2040).mean()))
        out[nm] = dict(elapsed_s=round(el, 1), **{k: round(v, 4) for k, v in h.items()})
    cmp = {}
    for k in out["cpu"]:
        if k == "elapsed_s":
            continue
        a, b = out["cpu"][k], out["gpu"][k]
        se = np.sqrt(max(a * (1 - a), b * (1 - b), 1e-6) * 2 / N)
        cmp[k] = dict(cpu=a, gpu=b, diff=round(b - a, 4), z=round((b - a) / se, 2))
    return dict(N=N, cpu_s=out["cpu"]["elapsed_s"], gpu_s=out["gpu"]["elapsed_s"], compare=cmp,
                max_abs_z=max(abs(v["z"]) for v in cmp.values()))


def main():
    t0 = time.time()
    force_cpu = "--cpu" in sys.argv
    dev = pick_device(force_cpu)
    N = int(os.environ.get("M8_N", 20000))
    NV = int(os.environ.get("M8_NV", 10000))
    NT = int(os.environ.get("M8_NT", 6000))
    NVER = int(os.environ.get("M8_NVERIFY", 4000))
    print("device", dev); sys.stdout.flush()
    ver = verify(NVER, dev) if dev.type == "cuda" and NVER > 0 else None
    if ver:
        print("verify", json.dumps(ver)); sys.stdout.flush()
    rng_b = np.random.default_rng(SEED + 1)
    tb = time.time()
    p, o = run_variant("baseline", N, dev=dev)
    t_base = time.time() - tb
    res = summarize(o, p, rng_b)
    print("baseline done", round(time.time() - t0, 1), "s", "S5 deliberate US/CN 2075", res["P_S5_by"]["2075"],
          "total any", res["P_S5_total_any_bloc_by"]["2075"]); sys.stdout.flush()
    var_res = {}; var_curves = {}
    keep = ["P_S5_by", "P_S5_deliberate_any_bloc_by", "P_S5_total_any_bloc_by", "P_S5_total_2075_by_first_channel",
            "P_S5_deliberate_US_or_China_2075_by_channel", "year_lead_Dcore<0.2", "year_lead_Dfull<0.5",
            "P_public_disempowered_US_or_China_2075", "first_choice_autocratic_at_decision", "first_choice_democratic_at_decision",
            "P_democratic_breakdown_by", "P_first_sustained_insurgency_by", "warehousing", "jev_crosscheck_model",
            "world_pop_share_in_S5_total_blocs_by", "loss_ladder_deliberate", "world_population_loss_2075", "round3"]
    for v in VARIANTS:
        pv, ov = run_variant(v, NV, dev=dev)
        r = summarize(ov, pv, rng_b, boot=False)
        var_res[v] = {k: r[k] for k in keep}
        S5v = ov["t_S5d"][:, :2].min(1); S5t = ov["t_S5"].min(1)
        NTv = ov["tL_del"][:, :2, 3].min(1)
        var_curves[v] = dict(deliberate_US_CN=[float((S5v <= y).mean()) for y in YEARS], total_any=[float((S5t <= y).mean()) for y in YEARS],
                             near_total_US_CN=[float((NTv <= y).mean()) for y in YEARS])
        print("variant", v, "NT_UC", r["loss_ladder_deliberate"][">=0.999"]["US_or_China"], "world_NT",
              r["world_population_loss_2075"]["P(>=0.999)"], "S5d", r["P_S5_by"]["2075"], "S5t", r["P_S5_total_any_bloc_by"]["2075"], "closure",
              (r["year_lead_Dcore<0.2"] or {}).get("median"), "disemp", r["P_public_disempowered_US_or_China_2075"],
              round(time.time() - t0, 1)); sys.stdout.flush()
    tt = time.time()
    torn = run_tornado_batched(TORN_KEYS, p, NT, dev)
    base_t = torn.pop("base")
    print("tornado done", round(time.time() - t0, 1), "tornado s", round(time.time() - tt, 1)); sys.stdout.flush()
    envelope = [min(r[t]["P_S5_deliberate_2075"] for r in torn.values() for t in ("p10", "p90")),
                max(r[t]["P_S5_deliberate_2075"] for r in torn.values() for t in ("p10", "p90"))]
    ma = {}
    for key in ["2050", "2075"]:
        vals = {"baseline": res["P_S5_by"][key][0], "skeptic_combo": var_res["skeptic_combo"]["P_S5_by"][key],
                "pessimist_combo": var_res["pessimist_combo"]["P_S5_by"][key]}
        ma[key] = dict(components=vals, weights=MODEL_AVG_W, model_average=round(sum(MODEL_AVG_W[k] * vals[k] for k in vals), 4))
    band = dict(note="headline CI is Monte Carlo (bootstrap) only. Structural range: skeptic and pessimist structural sets; model average weights 0.5 baseline, 0.25 each",
                structural_range_P_S5_deliberate_US_CN_2075=[var_res["skeptic_combo"]["P_S5_by"]["2075"], var_res["pessimist_combo"]["P_S5_by"]["2075"]],
                model_average=ma,
                tornado_envelope_P_S5_deliberate_US_CN_2075=envelope,
                variant_range_P_S5_deliberate_US_CN_2075=[min(var_res[v]["P_S5_by"]["2075"] for v in VARIANTS),
                                                          max(var_res[v]["P_S5_by"]["2075"] for v in VARIANTS)])
    jev = json.load(open(os.path.join(ROOT, "research", "jev_elite_calculus.json")))
    calib = dict(
        note="records are values at 1 January of the year; the run starts 1 Oct 2026",
        sw_capability_jan2027_median=round(float(np.median(o["rec"]["sw"][:, 0])), 3),
        sw_practice_jan2027_median=round(float(np.median(o["rec"]["swp"][:, 0])), 3),
        ai_led_rnd_share_jan2027_median=round(float(np.median(o["rec"]["rnd"][:, 0])), 3),
        desk_task_feasible_jan2027_median=round(float(np.median(o["rec"]["fcog"][:, 0])), 3),
        robot_dx_jan2027_median=round(float(np.median(o["rec"]["dx"][:, 0])), 3),
        gp_robot_production_jan2027_M=round(float(np.median(o["recA"]["prod"][:, :, 0].sum(1))), 3),
        gp_robot_production_2030_M=res["global_gp_robot_production_M_per_yr"]["2030"],
        target_2030="Goldman humanoids ~0.9M/yr (0.25-3M)",
        onset_hazard_2026=res["onset_hazard_2026_median_per_yr"],
        target_onset="US/China/Europe ~0.2-0.4%/yr new sustained insurgency at zero displacement (UCDP high-capacity onset rates)",
        P_first_insurgency_by_2030=res["P_first_sustained_insurgency_by"]["US_bloc"]["2030"],
        ideology_US_or_China_by_2045=res["P_ideology_US_or_China_by"]["2045"],
        target_ideology="r9d: ~0.08 (0.03-0.2)",
        P_US_breakdown_by_2030=res["P_democratic_breakdown_by"]["US_bloc"]["2030"],
        target_US="current V-Dem episode, U-turn 50-80% with leverage intact",
        P_US_China_war_by_2035=res["P_US_China_war_by"]["2035"], target_war="~5-10% by 2035 (judgment)")
    lab, s5a = s5_channels(o, "t_S5d", "ch_S5d", blocs=[0, 1])

    def fin(x):
        return [None if not np.isfinite(v) else round(float(v), 2) for v in x]
    fa = np.argmin(np.where(np.isfinite(o["t_closed"]), o["t_closed"], 1e9), 1)
    end = []
    for i in range(N):
        if lab[i] is not None:
            end.append("S5_" + ("active" if lab[i] in ("active_depopulation_decision", "collective_punishment") else "neglect"))
        elif np.isfinite(o["t_S5"][i, :2]).any():
            end.append("S5_nondeliberate_only")
        elif not np.isfinite(o["t_closed"][i]).any():
            end.append("no_closure")
        elif o["choice_end"][i, fa[i]] >= 0:
            end.append(STRAT[o["choice_end"][i, fa[i]]])
        else:
            end.append("closure_pending_decision")
    samples = dict(
        t_AC=fin(o["t_ac"]), t_dexterity=fin(o["t_dex"]),
        t_lead_Dcore_lt_0_5=fin(o["lead_core"][:, 0]), t_lead_Dcore_lt_0_2=fin(o["lead_core"][:, 1]),
        t_lead_Dcore_lt_0_05=fin(o["lead_core"][:, 2]),
        t_lead_Dfull_lt_0_5=fin(o["lead_full"][:, 0]), t_lead_Dfull_lt_0_2=fin(o["lead_full"][:, 1]),
        lead_actor=[ACTORS[i] for i in o["lead_actor"]],
        t_US_power_grab=fin(o["t_grab"][:, 0]),
        first_choice_first_closer=[STRAT[c] if c >= 0 else None for c in o["first_choice"][np.arange(N), fa]],
        t_S5_deliberate_US_CN=fin(o["t_S5d"][:, :2].min(1)), t_S5_total_any=fin(o["t_S5"].min(1)),
        S5_deliberate_channel=list(lab),
        S5_deliberate_actor=[ACTORS[int(s5a[i])] if lab[i] is not None else None for i in range(N)],
        end_state_2075_first_closer=end,
        t_M2=fin(o["tm"]["M2"]), t_M3=fin(o["tm"]["M3"]), t_M2p=fin(o["tm"]["M2p"]), t_M3p=fin(o["tm"]["M3p"]),
        t_M4=fin(o["tm"]["M4"]), t_M5=fin(o["tm"]["M5"]), t_M6=fin(o["tm"]["M6"]), t_M7=fin(o["tm"]["M7"]),
        t_US_democratic_breakdown=fin(o["t_break"][:, 0]),
        t_first_insurgency_US=fin(o["t_ins1"][:, 0]), t_first_insurgency_China=fin(o["t_ins1"][:, 1]),
        t_closed_US=fin(o["t_closed"][:, 0]), t_closed_China=fin(o["t_closed"][:, 1]),
        t_S5d_US=fin(o["t_S5d"][:, 0]), t_S5d_China=fin(o["t_S5d"][:, 1]),
        cum_excess_loss_2075_max_bloc=[round(float(v), 4) for v in o["loss"].max(1)],
    )
    Y = list(YEARS)
    fan = {str(y): dict(p10=round(float(np.percentile(o["rec"]["Dlead_core"][:, Y.index(y)], 10)), 3),
                        p50=round(float(np.percentile(o["rec"]["Dlead_core"][:, Y.index(y)], 50)), 3),
                        p90=round(float(np.percentile(o["rec"]["Dlead_core"][:, Y.index(y)], 90)), 3),
                        full_p50=round(float(np.percentile(o["rec"]["Dlead_full"][:, Y.index(y)], 50)), 3))
           for y in (2027, 2028, 2030, 2032, 2035, 2038, 2040, 2045, 2050, 2060, 2075)}
    elapsed = round(time.time() - t0, 1)
    out = dict(
        model="M8 v4 round 3 (B1-B9, GPU): industrial closure + grievance loop + endogenous democracy + incentive-driven consolidation + cross-bloc depopulation, 6 blocs",
        run=dict(seed=SEED, n_draws=N, n_variant=NV, n_tornado=NT, dt=DT, t0=T0, horizon=T_END, device=str(dev),
                 gpu=(get_torch().cuda.get_device_name(0) if dev.type == "cuda" else None),
                 baseline_sim_s=round(t_base, 1), elapsed_s=elapsed,
                 peak_vram_GB=(round(get_torch().cuda.max_memory_allocated() / 1e9, 2) if dev.type == "cuda" else None),
                 port_verification_gpu_vs_cpu=ver,
                 port_verification_prefix_model="torch-CUDA port of the round-1 numpy model vs numpy at N=20000: S5 2075 0.671 vs 0.670, closure by 2040 0.604 vs 0.604, US insurgency by 2040 0.338 vs 0.341 (5.0 s vs 49 s)"),
        actors=dict(names=ACTORS, population_bn=dict(zip(ACTORS, POP.tolist())),
                    note="US_bloc = US, Japan, Korea, Taiwan; Europe_plus = EU, UK, Canada, Australia, NZ, Switzerland, Norway; RoW = blocs 2-5, reported as population shares"),
        milestone_definitions=MILESTONES, plain_definitions=DEFS_PLAIN,
        definitions=dict(
            D_full="share of the 2026 human labor-task value of the bloc's full chain (9 segments) still requiring humans, incl. human content of imports",
            D_core="same for a minimal self-sufficient core loop of scale q_core, automation allocated by pursuit intensity",
            closure="D_core < 0.2 triggers the elite game (after a decision lag)",
            headline="P(S5_deliberate in the US or China bloc by 2075)",
            ch_S5_codes="2 neglect, 3 active (decision or collective punishment), 4 attrition, 5 war",
            strategy_codes="0 serve, 1 warehouse, 2 neglect, 3 depopulate, 4 rentier",
            disempowered="a bloc's rulers chose rentier/warehouse/neglect/depopulate at any point, or S5_deliberate occurred"),
        initial_state_2026=dict(segments=SEG, automated_share_by_bloc={an: dict(zip(SEG, X0[a].tolist())) for a, an in enumerate(ACTORS)},
                                current_growth_by_bloc={an: dict(zip(SEG, G0[a].tolist())) for a, an in enumerate(ACTORS)},
                                evidence=dict(zip(SEG, X0_EVID)), D_dem=dict(zip(ACTORS, D0.tolist())),
                                provision=dict(zip(ACTORS, BASE_PROV.tolist())), workforce_core_M=dict(zip(ACTORS, WORKFORCE.tolist())),
                                grievance_share=0.39, hostile_share_median=0.005,
                                manufacturing_note="China 0.08 >= US bloc 0.07: US-bloc employment-weighted robot density ~450/10k vs China ~470/10k plus China's larger lights-out share"),
        uncertainty_band=band, headline=res, calibration=calib, variants=var_res, variant_curves=dict(years=Y, **var_curves),
        tornado=dict(base=base_t, rows=torn),
        jev_crosscheck=dict(jev=jev["cells"], model=res["jev_crosscheck_model"],
                            model_quiet_world=var_res["quiet_world"]["jev_crosscheck_model"],
                            note="Jev cells: 15-year yes/no judgments given full closure. Model cells: P(S5_deliberate within 15 y of the bloc's first decision), by state at decision"),
        D_fan_leading=fan,
        priors={k: dict(spec=list(v[0]), source=v[1], evidence=v[2]) for k, v in PRIORS.items()},
        priors_round3={k: dict(spec=list(v[0]), source=v[1], evidence=v[2]) for k, v in PRIORS_B.items()},
        constants_round3=dict(MIL0=dict(zip(ACTORS, MIL0.tolist())), IB=dict(zip(ACTORS, IB.tolist())),
                              lag_cog_years=dict(zip(ACTORS, [[float(a), float(b)] for a, b in zip(LAGC_LO, LAGC_HI)])),
                              lag_phys_years=dict(zip(ACTORS, [[float(a), float(b)] for a, b in zip(LAGP_LO, LAGP_HI)]))),
        samples=samples)
    if bool(p["gf_on"].any()):
        out["greenfield_core_loop"] = GF_NOTE
    if bool(p["wfl_on"].any()):
        out["wide_floors"] = dict(rule="A10: fast tails widened, 90th percentile kept, 5th percentile to 0.25 y (0.1 y for fact_build_a); quantile map of the same standard-normal draws", table=wfl_table())
    if bool(p["cf_on"].any()):
        out["compute_feedback"] = dict(spec=CF_NOTE, priors={k: dict(spec=list(v[0]), source=v[1], evidence=v[2]) for k, v in PRIORS_CF.items()})
    out["config_env"] = dict(M8_FINAL=os.environ.get("M8_FINAL", ""), M8_BRAKES=os.environ.get("M8_BRAKES", ""),
                             M8_GF=os.environ.get("M8_GF", ""), M8_CF=os.environ.get("M8_CF", ""), M8_WFL=os.environ.get("M8_WFL", ""))
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    # M8_OUT (file name in results/) and M8_FIG (figure folder) redirect the outputs; default = the published paths
    outp = os.path.join(ROOT, "results", os.environ.get("M8_OUT", "m8_v4.json"))
    if os.environ.get("M8_OUT"):
        assert not os.path.exists(outp), outp + " exists; not overwriting"
    with open(outp, "w") as fh:
        json.dump(out, fh, indent=1, default=float)
    figures(o, res, var_res, torn, base_t)
    figure_round3(o, res, var_res)
    print(json.dumps({k: res[k] for k in res if k not in ("segment_automated_share_median", "loop_by_bloc")}, indent=1, default=str))
    print("loop", json.dumps(res["loop_by_bloc"]))
    print("seg", json.dumps(res["segment_automated_share_median"]))
    print("band", json.dumps(band)); print("calib", json.dumps(calib))
    print("elapsed", round(time.time() - t0, 1))


def figures(o, res, var_res, torn, base_t):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fd = os.environ.get("M8_FIG", os.path.join(ROOT, "figures"))
    os.makedirs(fd, exist_ok=True)
    ink, muted, grid = "#0b0b0b", "#52514e", "#e4e3df"
    c = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948"]
    plt.rcParams.update({"font.size": 9, "axes.edgecolor": muted, "axes.labelcolor": muted, "xtick.color": muted,
                         "ytick.color": muted, "axes.titlecolor": ink, "lines.linewidth": 2})

    def style(ax):
        ax.spines[["top", "right"]].set_visible(False); ax.grid(color=grid, lw=0.6); ax.set_axisbelow(True)
    Y = YEARS
    fig, ax = plt.subplots(figsize=(9, 4.8))
    keys = [("M2", o["tm"]["M2"]), ("M2p", o["tm"]["M2p"]), ("M3", o["tm"]["M3"]), ("M5", o["tm"]["M5"]), ("M7", o["tm"]["M7"]),
            ("DEX", o["t_dex"]), ("C02", o["lead_core"][:, 1]), ("F05", o["lead_full"][:, 0])]
    lab = {"M2": "AI can do half of software tasks, no review needed", "M2p": "half of software work actually merged unreviewed",
           "M3": "AI can do 90% of software tasks", "M5": "AI does 95% of AI-research tasks", "M7": "AI can do half of all desk tasks",
           "DEX": "robots: half of physical tasks at human speed", "C02": "closure: core chain <20% human", "F05": "whole chain <50% human"}
    for i, (k, tt) in enumerate(keys):
        ax.plot(Y, [(tt <= y).mean() for y in Y], color=c[i % 8], label=lab[k], ls="--" if k == "M2p" else "-")
    ax.set_xlim(2026.5, 2060); ax.set_ylim(0, 1); ax.set_ylabel("cumulative probability")
    ax.set_title("When milestones arrive (M1, AI writes most code with human review, is already observed)", loc="left")
    ax.legend(frameon=False, fontsize=7.5, loc="lower right"); style(ax)
    fig.tight_layout(); fig.savefig(os.path.join(fd, "m8v4_milestones.png"), dpi=140); plt.close(fig)

    fig, ax = plt.subplots(1, 2, figsize=(12, 4.4))
    order = [3, 4, 0, 2, 7, 1, 5, 6]
    for i, s_ in enumerate(order):
        ax[0].plot(Y, np.median(o["xseg"][:, 1, s_, :], 0), color=c[i], label=SEG[s_])
    ax[0].set_xlim(2026.5, 2055); ax[0].set_ylim(0, 1); ax[0].set_ylabel("automated share of physical task value")
    ax[0].set_title("China bloc, whole economy, median (starts at measured 2026 shares)", loc="left")
    ax[0].legend(frameon=False, fontsize=8, ncol=2)
    Pp = o["recA"]["prod"].sum(1)
    ax[1].fill_between(Y, np.percentile(Pp, 10, 0), np.percentile(Pp, 90, 0), color=c[0], alpha=0.15, lw=0)
    ax[1].plot(Y, np.median(Pp, 0), color=c[0], label="median, p10-p90")
    ax[1].set_yscale("log"); ax[1].set_xlim(2026.5, 2050); ax[1].set_ylabel("M units per year")
    ax[1].set_title("General-purpose robot production, world", loc="left"); ax[1].legend(frameon=False)
    for a_ in ax:
        style(a_)
    fig.tight_layout(); fig.savefig(os.path.join(fd, "m8v4_physical.png"), dpi=140); plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4.4))
    for key, lb, col in [("Dlead_core", "core loop D_core", c[1]), ("Dlead_full", "whole chain D_full", c[0])]:
        X = o["rec"][key]
        ax.fill_between(Y, np.percentile(X, 10, 0), np.percentile(X, 90, 0), color=col, alpha=0.15, lw=0)
        ax.plot(Y, np.median(X, 0), color=col, label=lb + " (median, p10-p90)")
    ax.axhline(0.2, color=muted, lw=1, ls="--"); ax.text(2051, 0.225, "closure threshold 0.2", color=muted, fontsize=8)
    ax.set_xlim(2026.5, 2060); ax.set_ylim(0, 1.02); ax.set_ylabel("share of 2026 labor still needing humans")
    ax.set_title("Leading bloc's dependence on human labor", loc="left"); ax.legend(frameon=False); style(ax)
    fig.tight_layout(); fig.savefig(os.path.join(fd, "m8v4_dependence.png"), dpi=140); plt.close(fig)

    fig, ax = plt.subplots(2, 2, figsize=(12, 7))
    for a, an in enumerate(ACTORS):
        ax[0, 0].plot(Y, np.median(o["recA"]["disp"][:, a], 0), color=c[a], label=an)
        ax[0, 1].plot(Y, o["recA"]["I"][:, a].mean(0), color=c[a], label=an)
        ax[1, 0].plot(Y, o["recA"]["free"][:, a].mean(0), color=c[a], label=an)
        ax[1, 1].plot(Y, o["recA"]["loss"][:, a].mean(0), color=c[a], label=an)
    for a_, t_, yl in [(ax[0, 0], "Share of core workforce that lost its livelihood (median)", "share"),
                       (ax[0, 1], "Probability a new sustained insurgency is active", "probability"),
                       (ax[1, 0], "Probability the bloc is autocratic (LDI < 0.3 or seized)", "probability"),
                       (ax[1, 1], "Mean cumulative excess population loss (all channels)", "share of 2026 population")]:
        a_.set_title(t_, loc="left"); a_.set_ylabel(yl); a_.set_xlim(2026.5, 2075); style(a_)
    ax[0, 0].legend(frameon=False, fontsize=8)
    fig.tight_layout(); fig.savefig(os.path.join(fd, "m8v4_loop.png"), dpi=140); plt.close(fig)

    fig, ax = plt.subplots(1, 2, figsize=(13, 5.6))
    labs, _ = s5_channels(o, "t_S5", "ch_S5")
    S5 = o["t_S5"].min(1)
    basev = np.zeros(len(Y))
    for i, ch in enumerate(["active_depopulation_decision", "collective_punishment", "neglect", "attrition_despair_and_crackdown", "war"]):
        yv = np.array([((S5 <= y) & (labs == ch)).mean() for y in Y])
        ax[0].fill_between(Y, basev, basev + yv, color=c[i], lw=0, label=ch.replace("_", " "))
        basev = basev + yv
    S5d = o["t_S5d"][:, :2].min(1)
    ax[0].plot(Y, [(S5d <= y).mean() for y in Y], color=ink, lw=1.5, ls="--", label="headline: deliberate, US or China")
    ax[0].set_xlim(2026.5, 2075); ax[0].set_ylabel("cumulative probability")
    ax[0].set_title("S5 (>=10% excess loss): first channel, any bloc", loc="left"); ax[0].legend(frameon=False, loc="upper left", fontsize=8)
    vs = ["baseline"] + VARIANTS
    vals = [res["P_S5_by"]["2075"][0]] + [var_res[v]["P_S5_by"]["2075"] for v in VARIANTS]
    idx = np.argsort(vals)
    ax[1].barh(range(len(vs)), [vals[i] for i in idx], color=[c[1] if vs[i] == "baseline" else c[0] for i in idx], height=0.7)
    for j, i in enumerate(idx):
        ax[1].text(vals[i] + 0.005, j, f"{vals[i] * 100:.1f}%", va="center", fontsize=7.5, color=ink)
    ax[1].set_yticks(range(len(vs))); ax[1].set_yticklabels([vs[i] for i in idx], fontsize=8)
    ax[1].set_xlabel("P(deliberate S5 in US or China bloc by 2075)"); ax[1].set_title("Structural variants (baseline in orange)", loc="left")
    style(ax[0]); style(ax[1])
    fig.tight_layout(); fig.savefig(os.path.join(fd, "m8v4_s5.png"), dpi=140); plt.close(fig)

    b = base_t["P_S5_deliberate_2075"]
    rows = sorted(torn.items(), key=lambda kv: abs(kv[1]["p90"]["P_S5_deliberate_2075"] - kv[1]["p10"]["P_S5_deliberate_2075"]))[-25:]
    fig, ax = plt.subplots(figsize=(8, 7.5))
    for i, (k, r) in enumerate(rows):
        lo, hi = r["p10"]["P_S5_deliberate_2075"], r["p90"]["P_S5_deliberate_2075"]
        ax.barh(i, lo - b, left=b, color=c[0], height=0.7)
        ax.barh(i, hi - b, left=b, color=c[1], height=0.7)
    ax.axvline(b, color=ink, lw=1)
    ax.set_yticks(range(len(rows))); ax.set_yticklabels([k for k, _ in rows], fontsize=8)
    ax.set_xlabel("P(deliberate S5, US or China, by 2075); blue = prior p10, orange = p90")
    ax.set_title("Tornado, top 25 (one at a time, common random numbers)", loc="left"); style(ax)
    fig.tight_layout(); fig.savefig(os.path.join(fd, "m8v4_tornado.png"), dpi=140); plt.close(fig)


def figure_round3(o, res, var_res):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fd = os.environ.get("M8_FIG", os.path.join(ROOT, "figures"))
    ink, muted, grid = "#0b0b0b", "#52514e", "#e4e3df"
    c = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948"]

    def style(ax):
        ax.spines[["top", "right"]].set_visible(False); ax.grid(color=grid, lw=0.6); ax.set_axisbelow(True)
    Y = YEARS
    fig, ax = plt.subplots(2, 2, figsize=(13, 8.5))
    fr = o["recA"]["free"]; nc = o["recA"]["ncoal"]
    for a, an in enumerate(ACTORS):
        med = [np.median(nc[fr[:, a, i] > 0, a, i]) if (fr[:, a, i] > 0).sum() > 50 else np.nan for i in range(len(Y))]
        ax[0, 0].plot(Y, med, color=c[a], label=an)
    ax[0, 0].set_ylim(0, 22); ax[0, 0].set_xlim(2026.5, 2075); ax[0, 0].set_ylabel("members (median, given autocratic)")
    ax[0, 0].set_title("B2: size of the ruling coalition (purges, counter-coups)", loc="left"); ax[0, 0].legend(frameon=False, fontsize=8)
    Mk = o["recA"]["Mk"]; Msh = Mk / Mk.sum(1, keepdims=True)
    for a, an in enumerate(ACTORS):
        ax[0, 1].plot(Y, np.median(Msh[:, a], 0), color=c[a], label=an)
    ax[0, 1].set_xlim(2026.5, 2075); ax[0, 1].set_ylim(0, 1); ax[0, 1].set_ylabel("share of world kinetic power (median)")
    ax[0, 1].set_title("B3/B5: kinetic power (automated force counts k_am-fold)", loc="left")
    for a, an in enumerate(ACTORS):
        tc = o["t_closed"][:, a]
        ax[1, 0].plot(Y, [(tc <= y).mean() for y in Y], color=c[a], label=an)
    ax[1, 0].set_xlim(2026.5, 2075); ax[1, 0].set_ylim(0, 1); ax[1, 0].set_ylabel("P(closure by year)")
    ax[1, 0].set_title("B6: closure by bloc (import dependence, capability lags, wired caps)", loc="left")
    nt = np.isfinite(o["tL_del"][:, :, 3])
    dd = o["lc_neg"] + o["lc_act"] + o["lc_col"] + o["lc_xb"]
    forg = nt & (o["lc_xb"] > 0.5 * dd)
    x = np.arange(len(ACTORS))
    ax[1, 1].bar(x - 0.2, (nt & ~forg).mean(0), 0.4, color=c[1], label="near-total, mainly own rulers")
    ax[1, 1].bar(x - 0.2, forg.mean(0), 0.4, bottom=(nt & ~forg).mean(0), color=c[6], label="near-total, mainly foreign closed actor (B5)")
    ax[1, 1].bar(x + 0.2, np.isfinite(o["t_xb"]).mean(0), 0.4, color=muted, label="targeted by a foreign campaign")
    ax[1, 1].set_xticks(x); ax[1, 1].set_xticklabels([a.replace("_", "\n") for a in ACTORS], fontsize=8)
    ax[1, 1].set_ylim(0, 1); ax[1, 1].set_ylabel("P by 2075"); ax[1, 1].legend(frameon=False, fontsize=7.5)
    ax[1, 1].set_title("B5: near-total loss by bloc, own vs foreign", loc="left")
    for a_ in ax.ravel():
        style(a_)
    fig.tight_layout(); fig.savefig(os.path.join(fd, "m8v4_round3.png"), dpi=140); plt.close(fig)
    # decomposition bar: near-total US/CN and world, each B reverted
    vs = ["round2_exact", "rev_B1_average_moral", "rev_B2_fixed_consolidation", "rev_B3_unenforced_stigma", "rev_B4_no_retribution",
          "rev_B5_no_cross_bloc", "rev_B6_caps_bypassed"]
    vs = [v for v in vs if v in var_res]
    ntv = [var_res[v]["loss_ladder_deliberate"][">=0.999"]["US_or_China"] for v in vs]
    wv = [var_res[v]["world_population_loss_2075"]["P(>=0.999)"] for v in vs]
    b_nt = res["loss_ladder_deliberate"][">=0.999"]["US_or_China"]; b_w = res["world_population_loss_2075"]["P(>=0.999)"]
    fig, ax = plt.subplots(figsize=(10, 4.6))
    xx = np.arange(len(vs) + 1)
    ax.bar(xx - 0.2, [b_nt] + ntv, 0.4, color=c[1], label=">=99.9% deliberate, US or China")
    ax.bar(xx + 0.2, [b_w] + wv, 0.4, color=c[6], label="world population loss >=99.9%")
    for xi, (a_, b_) in enumerate(zip([b_nt] + ntv, [b_w] + wv)):
        ax.text(xi - 0.2, a_ + 0.01, f"{a_:.3f}", ha="center", fontsize=7.5); ax.text(xi + 0.2, b_ + 0.01, f"{b_:.3f}", ha="center", fontsize=7.5)
    ax.set_xticks(xx); ax.set_xticklabels(["round 3 baseline"] + vs, rotation=20, ha="right", fontsize=8)
    ax.set_ylim(0, 1); ax.set_ylabel("P by 2075 (standalone m8)"); ax.legend(frameon=False, fontsize=8)
    ax.set_title("Effect of each round-3 change (revert one at a time; round2_exact = all B off)", loc="left"); style(ax)
    fig.tight_layout(); fig.savefig(os.path.join(fd, "m8v4_round3_decomposition.png"), dpi=140); plt.close(fig)


if __name__ == "__main__":
    main()
