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
GLOBAL_PROD0 = 0.10
GLOBAL_STOCK0 = 0.15
# strategies, internal order of harshness (the coalition median is taken on this order)
STRAT_INT = ["serve", "rentier", "warehouse", "neglect", "depopulate"]
STRAT = ["serve", "warehouse", "neglect", "depopulate", "rentier"]   # legacy output codes 0..4
INT2LEG = np.array([0, 4, 1, 2, 3])
LEG2INT = np.array([0, 2, 3, 4, 1])
PROV_INT = np.array([1.0, 1.0, 0.6, 0.1, 0.0])
NMEM = 51
NMIN_VALS = np.array([1, 3, 5, 7]); NMIN_P = np.array([0.3, 0.3, 0.2, 0.2])
# democracy (V-Dem LDI 2025/26, population-weighted within blocs)
D0 = np.array([0.57, 0.05, 0.70, 0.10, 0.28, 0.35])
DMAX = np.array([0.78, 0.20, 0.85, 0.40, 0.55, 0.60])
D_BREAK = 0.30
BASE_PROV = np.array([0.45, 0.30, 0.60, 0.25, 0.15, 0.20])
P_EP0 = np.array([1.0, 0.0, 0.25, 0.0, 0.0, 0.35])   # P(bloc starts inside an autocratization episode)
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
}


def ln(med, sig):
    return ("lognormal", med, sig)


PRIORS = {
    # ------------------------------------------------ cognitive (r9a)
    "h50_0": (ln(16.0, 0.15), "METR 50% horizon, best model mid-2026: 12-20 h (METR May 2026)", "medium-high"),
    "h80_ratio": (ln(4.5, 0.3), "50%/80% horizon ratio: 16 h vs 3.5 h (METR May 2026)", "medium-high"),
    "metr_doubling_months": (ln(4.3, 0.28), "horizon doubling 2023+ window 4.3 mo; 2024-25 3-3.5 mo; long-run 7 mo (METR TH1.1)", "medium-high"),
    "compute_slowdown": (("uniform", 0.35, 1.0), "Epoch: 4-5x/yr compute growth hard to sustain past ~2030", "moderate"),
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
    "fb_zero_mass": (("const", 0.25), "Davidson & Houlden 2025: r<1 plausible", "moderate-weak"),
    "fb_strength": (ln(0.5, 0.5), "elasticity of horizon growth to AI-R&D automation (Amdahl speedup)", "low"),
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
    "alpha_med": (ln(0.03, 0.9), "elite willingness to pay for population welfare, share of output", "low"),
    "alpha_sig": (("uniform", 0.6, 1.4), "within-coalition heterogeneity", "low"),
    "p_hostile": (("beta", 1.2, 14.0), "baseline share of coalition factions hostile to the public (mean ~8%)", "low"),
    "moral_med": (ln(0.3, 1.2), "moral cost of ordering mass killing, output-share equivalent", "very low"),
    "p_refuse_abs": (("beta", 3.0, 3.0), "members with absolute refusal of active killing", "low"),
    "kappa_N": (("uniform", 0.05, 0.3), "neglect moral cost relative to killing", "low"),
    "m0": (("uniform", 0.3, 0.6), "cost of decent provision / output in 2026 terms", "moderate"),
    "c_W": (("uniform", 0.15, 0.4), "warehouse cost relative to serve", "low"),
    "c_R": (("uniform", 0.7, 1.0), "rentier cost relative to serve (full provision, no political rights)", "low"),
    "w_R": (("uniform", 0.45, 0.7), "public welfare under rentier rule relative to serve (Gulf citizens: rich, no vote)", "low"),
    "thk_R": (("uniform", 0.5, 0.9), "residual revolt threat under rentier rule relative to warehouse (Saudi 2011 buy-off worked; Bahrain excluded group revolted)", "B-/C"),
    "tau0": (ln(0.03, 0.9), "expected loss from an aggrieved population / output per yr with human security", "low"),
    "E0": (ln(0.10, 0.8), "legitimacy + international pressure / output at full rival leverage", "low"),
    "intl": (("uniform", 0.0, 1.5), "extra international response (sanctions, war risk) to executing depopulation, multiple of E0 term", "very low"),
    "v0": (ln(0.01, 0.9), "land/resource value freed by removing population, share of output", "very low"),
    "v1": (ln(0.03, 1.0), "Ricardian scarcity rent as the terrestrial ceiling binds (50% mass at zero)", "very low"),
    "r_disc": (("uniform", 0.03, 0.10), "discount rate for one-time acts", "moderate"),
    "phi_stigma": (("beta", 1.5, 3.5), "recurring share of killing's moral/legitimacy cost", "very low"),
    "s_sw": (ln(0.25, 0.8), "one-time cost of switching provisioning regime, output-years (0.07-0.9; round 1 used 0.1, which with no confirmation step let blocs ratchet into harsh options)", "low"),
    "p_exec": (("uniform", 0.7, 0.95), "P(an ordered depopulation is carried out to >=10% loss); historical orders for mass killing were mostly carried out (Holocaust, Cambodia, Rwanda), automated enforcement removes refusal; failure leaves 1-5% dead and a desperate insurgency", "very low"),
    "x_thr": (("uniform", 1.0, 3.0), "threat multiplier during execution (a population facing extermination resists harder than a warehoused one, but targeted populations historically rarely mounted effective resistance)", "C"),
    "p_small": (("uniform", 0.1, 0.3), "P(once security and admin are automated, the deciding circle shrinks to 1-7 people) per consolidated autocracy; otherwise >=21 (selectorate data; Jev assumes ~500)", "C/very low"),
    "lag_dec0": (("uniform", 1.0, 5.0), "years from closure to strategic decision at 2026 decision speed", "low"),
    "spd_max": (ln(2.0, 0.5), "strategic decision-speed compression at full AI R&D automation (r8d)", "weak"),
    "Tn": (ln(7.0, 0.5), "years of neglect to 10% population loss (Irish famine 12% in ~5 y)", "low-moderate"),
    "lagX": (("uniform", 0.5, 3.0), "years from executed depopulation decision to 10% loss", "low"),
    "a_vote": (("uniform", 0.15, 0.45), "welfare weight added per unit of D_dem", "low-moderate"),
    "k_inst": (("uniform", 1.0, 4.0), "moral/legitimacy cost multiplier per unit of D_dem", "low"),
    # ------------------------------------------------ grievance loop (r9c)
    "griev_trend": (("uniform", 0.03, 0.10), "yearly rise of anti-AI grievance attitudes (Pew 31%->39% 'more harm' in one year)", "A polls, C extrapolation"),
    "r_ab": (("uniform", 0.3, 0.7), "share of displaced labor reabsorbed into new human work at 2026 breadth", "low"),
    "k_ineq": (("uniform", 0.0, 1.0), "grievance amplification from visible inequality", "low"),
    "pg_red": (ln(0.30, 0.45), "fraction of grievance removed by full provision (status loss persists): 0.1-0.6", "C"),
    "pr_red": (("uniform", 0.3, 0.7), "fraction of revolt hazard removed by full provision (rentier/UBI evidence)", "B-"),
    "k_resp": (("uniform", 0.2, 0.8), "democratic provision response to grievance", "A- direction, C size"),
    "k_buy": (("uniform", 0.1, 0.5), "autocratic buy-off of grievance while coercion still needs humans (Saudi 2011)", "B-"),
    "h_beh0": (ln(0.005, 0.6), "behavioral hostile faction share (would join sabotage/violence), 2026", "low"),
    "att_trend": (("uniform", 0.0, 0.04), "yearly rise of attitudinal support for political violence (PRRI 15%->23% 2021-23)", "medium"),
    "e_att": (("uniform", 0.3, 0.7), "elasticity of behavioral hostility to attitudinal support (attitudes rose without proportional organized violence)", "C"),
    "e_g": (("uniform", 0.5, 1.0), "elasticity of hostility to the grievance state Gv", "C"),
    "mdisp": (ln(1.5, 0.25), "hostile-share multiplier per 10 pp displaced (Swing riots; GTI)", "low"),
    "Hmax": (("uniform", 5.0, 10.0), "saturation of relative hostility (smooth, replaces the 3% hard cap)", "C"),
    "p_svr_hi": (("uniform", 0.15, 0.5), "P(sustained violent resistance over ~10 y | 30% displaced, provision 0.2, high-capacity state)", "C"),
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
    "host_ins": (("uniform", 0.03, 0.15), "coalition hostility added by active insurgency", "C"),
    "host_H": (("uniform", 0.0, 0.15), "coalition hostility added at 4x reference hostility", "C"),
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
}
COMPAT = ["F_ac", "ac_horizon_hours", "tau_phys", "tau_cog", "g_h", "Td_mine_h", "Td_fab_h", "Np", "sw_auto0"]


def sample_params(N, rng, overrides=None, variant="baseline"):
    A = A_N
    p = {}
    for k, (spec, _, _) in PRIORS.items():
        kind = spec[0]
        if kind == "lognormal":
            p[k] = spec[1] * np.exp(spec[2] * rng.standard_normal(N))
        elif kind == "uniform":
            p[k] = rng.uniform(spec[1], spec[2], N)
        elif kind == "beta":
            p[k] = rng.beta(spec[1], spec[2], N)
        else:
            p[k] = np.full(N, float(spec[1]))
    p["sw_cap0"] = np.clip(p["sw_cap0"], 0.04, 0.4)
    p["sw_prac0"] = np.clip(p["sw_prac0"], 0.01, 0.2)
    p["dx0"] = np.clip(p["dx0"], 0.01, 0.15)
    p["pg_red"] = np.clip(p["pg_red"], 0.1, 0.6)
    p["m_d"] = np.clip(p["m_d"], 0.0003, 0.01)
    p["ai_lc"] = np.clip(p["ai_lc"], 1.05, 2.0)
    p["adl"] = np.clip(p["adl"], 1.2, 10.0)
    p["fb_strength"] = np.minimum(p["fb_strength"], 1.5)
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
    for k in ["loop_on", "dem_endog", "trends_on", "war_on", "id_on", "floors_on", "prof_on", "wh_mort_on",
              "persist_on", "rentier_on", "war_deaths_on"]:
        p[k] = np.ones(N, bool)
    p["dem_bar"] = np.zeros(N, bool)
    p["trig"] = np.full(N, 0.2)
    p["ruthless"] = np.zeros(N, bool)
    p["surv_on"] = np.ones(N)          # 1 = automated-surveillance deterrence active
    p["cp_scale"] = np.ones(N)         # collective-punishment regional-base multiplier
    if overrides:
        for k, v in overrides.items():
            p[k] = np.full(np.shape(p[k]), float(v))
    v = variant
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
    elif v == "no_self_replication":
        p["Td_auto"] = np.full(N, 1e9); p["Td_mat"] = np.full(N, 1e9)
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
    # derived
    h80r = p["h50_0"] / p["h80_ratio"] / p["mess"]
    p["s_task"] = LN2 * 12.0 / p["metr_doubling_months"] / p["z_rate"]
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
    A, S, K = A_N, 9, 5
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
    psi = psi0.clone()
    Td_fab_auto = torch.clamp(P["fab_build"] * P["fact_build_a"] / P["fact_build_h"], min=0.5)
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

    def hsat(hr):
        hm = P["Hmax"][:, None]
        return hm * hr / (hm + hr - 1)
    H0 = P["h_beh0"][:, None] * (1 - P["pr_red"][:, None] * BASE_PROV_[None]) * (0.39 / G_ref[:, None]) ** P["e_g"][:, None]
    Hr0e = hsat(H0 / H_ref[:, None])
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
    # ---------------- loss accounting (float64)
    z64 = torch.zeros(N, A, dtype=F64, device=dev)
    loss = z64.clone(); lc_neg = z64.clone(); lc_act = z64.clone(); lc_att = z64.clone(); lc_war = z64.clone()
    loss_wh = z64.clone()
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
    X_nlev = torch.full((N, A), float("nan"), device=dev); X_hsec = X_nlev.clone(); X_press = X_nlev.clone(); X_prov = X_nlev.clone(); X_Hre = X_nlev.clone()
    X_ins = free_at_dec.clone(); X_war = free_at_dec.clone(); X_id = free_at_dec.clone(); X_free = free_at_dec.clone()
    alpha_mag = P["alpha_med"][:, None, None] * torch.exp(P["alpha_sig"][:, None, None] * P["mem_z"])
    moral_base = P["moral_med"][:, None, None] * torch.exp(1.2 * P["mem_zm"])
    refuse = P["mem_u_ref"] < P["p_refuse_abs"][:, None, None]
    theta_i = torch.exp(0.5 * P["mem_zt"])
    small = (P["u_small"] < P["p_small"][:, None]) & ENT[None]
    n_small = torch.where(small, P["nmin"][:, None].long(), 21)
    memidx = torch.arange(NMEM, device=dev)
    PIK = T([0.0, 0.05, 0.1, 0.3, 1.0]); LANDK = T([0.0, 0.0, 0.6, 0.8, 1.0])
    ew = WORLD_W[None, :] * (1 - np.eye(A)); ew = ew / ew.sum(1, keepdims=True); exp_w = T(ew)
    press = torch.ones(N, A, device=dev)
    ny = len(YEARS) if records else 1
    rec = {k: torch.zeros(N, ny, device=dev) for k in ["Dlead_core", "Dlead_full", "fcog", "sw", "swp", "rnd", "hreal", "dx"]}
    recA = {k: torch.zeros(N, A, ny, device=dev) for k in ["Dc", "Df", "disp", "Gv", "H", "I", "Ddem", "free", "loss",
                                                             "prod", "war", "prov", "lamon"]}
    xseg = torch.zeros(N, A, S, ny, device=dev)
    yi = 0
    Dc_prev = torch.ones(N, A, device=dev); Dcs = torch.ones(N, A, S, device=dev)
    RR = torch.tensor(RR_SEG, device=dev); SAi = torch.tensor(SA_SEG, device=dev)
    WROW = T(WROW_M)[None]; NUC = T(NUC_ARMED)[None]
    adm = torch.ones(S, device=dev); adm[8] = 1 / 1.5
    wsc = W_S_ * (1 - CS_)
    k5 = torch.arange(K, device=dev)
    rent_ok = P["rentier_on"]

    def others_max(x):
        return torch.stack([torch.cat([x[:, :a], x[:, a + 1:]], 1).max(1).values for a in range(A)], 1)

    for step in range(NSTEP):
        t = T0 + (step + 1) * DT
        dts = t - T0
        # ---- time-varying priors
        C = torch.where(trends, torch.clamp(torch.exp(P["c_trend"] * dts), max=P["c_max"]), 1.0)
        eco = torch.where(trends, torch.clamp(dts / (P["eco_year"] - T0), 0, 1), 0.0)
        att = torch.where(trends, torch.clamp(0.23 + P["att_trend"] * dts, max=0.5), 0.23)
        g_att = torch.where(trends, torch.clamp(0.39 + P["griev_trend"] * dts, max=0.55), 0.39)
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
        slow = P["compute_slowdown"] if t > 2029.5 else torch.ones_like(L)
        corr = torch.where(P["capex_corr"] & (t > P["corr_start"]) & (t < P["corr_start"] + P["corr_len"]), 0.5, 1.0)
        lnh = torch.log(h80r0) + L * LN2
        s_rnd = nd((lnh - mu_rnd) / sr)
        mult = torch.clamp(((1 - P["rnd0"]) / torch.clamp(1 - s_rnd, min=1e-3)) ** fb, max=30.0)
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
        t_dex = torch.where(torch.isinf(t_dex) & (Lp >= Np), t, t_dex)
        Fp = torch.clamp(torch.sigmoid(lFp0 + (float(np.log(0.85 / 0.15)) - lFp0) * Lp[:, None] / (Np[:, None] * T(NP_MULT)[None])), 0, 0.995)
        speed = torch.clamp(P["s0"] ** (1 - torch.clamp(Lp / Np, max=1.1)), max=1.2)
        we = P["shifts"] * speed
        auth = (t >= P["t_leth"]) | (war & (t >= P["t_leth"] - 3.0))
        Fp_a = Fp[:, None, :].repeat(1, A, 1)
        Fp_a[:, :, 7] = Fp_a[:, :, 7] * torch.where(auth, 1.0, 0.5)
        F_tot = X0b + (1 - X0b) * Fp_a
        prof = torch.where(P["prof_on"], torch.clamp((Lp / Np - 0.5) / 0.5, 0, 1), 0.0)
        # ---- pursuit
        clos = 1 - Dc_prev
        psi = torch.clamp(psi0 + 0.2 * (sw >= SW_THR["M3"]).float()[:, None] + 0.15 * war.float()
                          + P["race_gamma"][:, None] * torch.clamp(others_max(clos) - clos, min=0), 0, 1)
        own = own + (K_RESH_ * lc[:, None, None] * psi[:, :, None] * (1 - own)) * DT
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
        m5p = torch.maximum(0.5 * psi, prof[:, None])[:, :, None]
        pri_c = torch.maximum(core_alloc, prof[:, None])[:, :, None]
        g_full = torch.maximum(g0e, gr * corr_b * m5p) * lc[:, None, None]
        g_core = torch.maximum(g0e, gr * corr_b * pri_c) * lc[:, None, None]
        Arr3 = A_rr[:, :, None]
        bld = (P["fact_build_h"] / P["fact_build_a"])[:, None, None]
        g_ra = gr * bld
        g_full = g_full * (1 - Arr3) + torch.maximum(g_ra * m5p, g_full) * Arr3
        g_core = g_core * (1 - Arr3) + torch.maximum(g_ra * pri_c, g_core) * Arr3
        # capacity-turnover caps
        iK = P["i_K"][:, None, None] * (1 + (P["i_boost"][:, None, None] - 1) * m5p) / P["k_int"][:, None, None]
        iK = iK * (1 + (bld - 1) * Arr3)
        rr0 = P["r_retro0"][:, None, None]; rrp = P["r_retro_p"][:, None, None]
        cap_f = iK + rr0 + (rrp - rr0) * m5p
        g_new_c = gr * corr_b * pri_c * lc[:, None, None] * (1 + (bld - 1) * Arr3)
        cap_c = g_new_c + rr0 + (rrp - rr0) * pri_c
        dxf = torch.clamp(torch.minimum(g_full * xf * (1 - xf / F_tot), cap_f * (F_tot - xf)), min=0) * DT
        dxc = torch.clamp(torch.minimum(g_core * xc * (1 - xc / F_tot), cap_c * (F_tot - xc)), min=0) * DT
        g_kit = torch.maximum(T(G_IND)[None], psi * P["g_ramp"][:, None]) * lc[:, None]
        g_kit = g_kit / (1 + torch.clamp(kit - kit0, min=0) / (P["kit_brake"][:, None] * need_tot))
        g_kit = g_kit * (1 - A_rr) + torch.maximum(g_auto, g_kit) * A_rr
        kit = torch.minimum(kit * torch.exp(g_kit * DT), 1e4 * need_tot)
        supply = kit + Rst * we[:, None]
        room_f = torch.clamp(supply - (xf * T_s).sum(-1), min=0)
        room_c = torch.clamp(core_alloc * supply - q * (xc * T_s).sum(-1), min=0)
        sc_f = torch.clamp(room_f / torch.clamp((dxf * T_s).sum(-1), min=1e-12), max=1.0)
        sc_c = torch.clamp(room_c / torch.clamp(q * (dxc * T_s).sum(-1), min=1e-12), max=1.0)
        xf = torch.clamp(xf + dxf * sc_f[:, :, None], max=0.999)
        xc = torch.clamp(xc + dxc * sc_c[:, :, None], max=0.999)
        Fc = torch.maximum(Fcog[:, None, None], a0c)
        mat = torch.clamp((Fcog - P["Fcog0"]) / (0.9 - P["Fcog0"]), 0, 1)
        gc = (P["g_cog0"] + (P["g_cog_max"] - P["g_cog0"]) * mat)[:, None, None] * adm
        gcc = torch.maximum(gc, P["g_cog_max"][:, None, None] * core_alloc[:, :, None])
        acf = torch.minimum(acf + torch.clamp(gc * acf * (1 - acf / Fc), min=0) * DT, Fc)
        acc = torch.minimum(acc + torch.clamp(gcc * acc * (1 - acc / Fc), min=0) * DT, Fc)
        hf = CS_ * (1 - acf) / (1 - a0c) + (1 - CS_) * (1 - xf) / (1 - X0b)
        hc = CS_ * (1 - acc) / (1 - a0c) + (1 - CS_) * (1 - xc) / (1 - X0b)
        hx = torch.einsum("ab,nbs->nas", exp_w, hf)
        Dcs = own * hc + (1 - own) * hx
        Dfs = own * hf + (1 - own) * hx
        Dc = (Dcs * W_S_).sum(-1); Df = (Dfs * W_S_).sum(-1)
        Dfd = (hf * W_S_).sum(-1)
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
        for j, th in enumerate(thr):
            t_core[:, :, j] = torch.where(torch.isinf(t_core[:, :, j]) & (Dc < th), t, t_core[:, :, j])
            t_full[:, :, j] = torch.where(torch.isinf(t_full[:, :, j]) & (Df < th), t, t_full[:, :, j])

        # ================= grievance loop =================
        decided = choice >= 0
        disp = (1 - Dfd) * (1 - P["r_ab"][:, None] * Dfd)
        Gnorm = torch.clamp(Gv / 0.5, 0, 1)
        P_pre = BASE_PROV_ + (1 - BASE_PROV_) * Gnorm * torch.clamp(
            P["k_resp"][:, None] * Ddem + P["k_buy"][:, None] * (1 - Ddem) * h_sec_f, 0, 1)
        Pv = torch.where(decided, PROV_[choice.clamp(min=0)], P_pre)
        Pv = torch.where(t < prov_floor_until, torch.clamp(Pv, min=0.8), Pv)
        amp = 1 + P["k_ineq"][:, None] * (1 - Dfd)
        Gt = 1 - (1 - g_att[:, None]) * (1 - torch.clamp(disp * amp * (1 - P["pg_red"][:, None] * Pv), 0, 1))
        Gt = torch.clamp(Gt + 0.2 * BF, 0, 1)
        Gv = torch.where(loop, Gv + (Gt - Gv) * float(1 - np.exp(-DT)), 0.39)
        ecoM = 1 + (P["eco_mult"] - 1) * eco
        H = (P["h_beh0"] * (att / 0.23) ** P["e_att"] * ecoM)[:, None] \
            * P["mdisp"][:, None] ** (torch.clamp(disp, max=0.5) / 0.1) * (1 - P["pr_red"][:, None] * Pv) \
            * (1 + BF) * (1 - P["dfd"][:, None] * DF) * (Gv / G_ref[:, None]) ** P["e_g"][:, None]
        H = torch.where(loop, H, H0)
        Hr = H / H_ref[:, None]
        Hre = hsat(Hr)
        det = h_sec_f + (1 - h_sec_f) * (1 - P["surv_on"][:, None] * (1 - P["d_surv"][:, None]))
        u = rnd(A, 4)
        lam_on = torch.clamp(lam0 * (Hre / Hr0e) ** beta * freg(Ddem) / freg0 * det, max=2.0)
        onset = loop & ~Iact & (u[:, :, 0] < 1 - torch.exp(-lam_on * DT)) & (loss < 0.5)
        rd_eff = P["rd"][:, None] + (1 - P["rd"][:, None]) * (1 - h_sec_f) * P["k_auto"][:, None]
        lam_sup = -torch.log(torch.clamp(1 - rd_eff, min=1e-3)) / 5.0
        lam_suc = (1 - P["coin_win"][:, None]) / P["ins_dur"][:, None] * (1 - (1 - P["def_mult"][:, None]) * (1 - h_sec_f))
        pe = 1 - torch.exp(-(lam_sup + lam_suc) * DT)
        ends = Iact & (u[:, :, 1] < pe)
        uu = rnd(A, 3)
        success = ends & (uu[:, :, 0] < lam_suc / (lam_sup + lam_suc))
        suppressed = ends & ~success
        # collective punishment during active insurgency, scaled to the region in revolt
        lu = 0.2 + 0.8 * (1 - Dfd)
        wc = (1 - Ddem) * (1 - 0.5 * torch.clamp(press, 0, 1))
        lam_lcp = -torch.log(1 - P["p_lcp"])[:, None] / P["ins_dur"][:, None] * lu * wc * (1 + id_lev) * torch.where(war, 1.5, 1.0)
        lcp = Iact & (u[:, :, 2] < 1 - torch.exp(-lam_lcp * DT))
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
        chW = decided & ((choice == 2) | (choice == 1))
        dep = torch.where(chW, torch.maximum(disp, 1 - Dfd), disp)
        fst_dec = torch.where(choice == 0, 0.25, torch.where(choice == 1, 0.5, 1.0))
        fstate = torch.where(decided, fst_dec, 0.25 + 0.75 * (1 - Pv))
        hg = 1 - P["hgain"][:, None] * (1 - Dfd)
        r_att = torch.where(loop & P["wh_mort_on"][:, None], P["m_d"][:, None] * dep * 0.65 * fstate * (1 + 0.5 * DF) * hg, 0.0) \
            + torch.where(Iact, P["ins_mort"][:, None], 0.0)
        r_neg = torch.where(decided & (choice == 3), -float(np.log(0.9)) / P["Tn"][:, None], 0.0)
        wd = P["war_deaths_on"][:, None]
        r_war = torch.where(war & wd, P["w_mort"][:, None] * (1 + 0.5 * auth.float()), 0.0)
        alive = 1 - loss
        d_att = (r_att * DT).double() * alive; d_neg = (r_neg * DT).double() * alive
        d_lcp = torch.where(lcp, klcp, 0.0).double() * alive
        d_war = (r_war * DT).double() * alive + torch.where(nuc, f_n, 0.0).double() * alive
        lc_att += d_att; lc_neg += d_neg; lc_act += d_lcp; lc_war += d_war
        loss_wh += torch.where(chW, d_att, 0.0)
        loss = torch.clamp(loss + d_att + d_neg + d_lcp + d_war, max=0.99)

        # ================= democracy =================
        rv = torch.clamp(Hre / Hr0e, 0, 1)
        Lev = 0.45 * Dfd + 0.25 * h_sec_f + 0.15 * rv * h_sec_f + 0.15 * (1 - P["conc"][:, None] * (1 - Dfd))
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

        # ================= elite game, yearly =================
        if abs(t % 1.0) < 1e-9:
            spd = 1 + (P["spd_max"] - 1) * torch.clamp((L - L_m3) / 8, 0, 1)
            lag = P["lag_dec0"] / spd
            ready = (t >= t_closed + lag[:, None]) & torch.isinf(t_X) & (t >= cool_until)
            h_sec = Dcs[:, :, 7]
            tau = torch.where(loop, P["tau0"][:, None] * (0.1 + 0.9 * h_sec) * Hre * (1 + (P["ins_thr"][:, None] - 1) * Iact)
                              + P["tau_sab"][:, None] * Hre * (1 + Iact.float()), P["tau0"][:, None] * (0.1 + 0.9 * h_sec))
            willing = Ddem * (0.5 + 0.5 * Df) + (1 - Ddem) * 0.3 * Df
            Gtot = G * Wk; pw_ = Gtot / Gtot.sum(1, keepdim=True)
            imp_dep = 1 - (own * W_S_).sum(-1)
            xw = pw_ * willing
            press = xw.sum(1, keepdim=True) - xw
            pi = P["E0"][:, None] * press * (0.3 + 0.7 * torch.clamp(imp_dep / 0.2, 0, 1))
            scar = P["v1"][:, None] * torch.clamp(Gr_cur / P["G_max"][:, None], 0, 1) ** 2
            land = torch.clamp(P["v0"][:, None] * (1 + P["eco_land"] * eco)[:, None] + scar, max=0.3)
            r_ = P["r_disc"]; ph = P["phi_stigma"]
            fX_moral = ph + (1 - ph) * r_
            fX_pi = (ph + (1 - ph) * torch.clamp(r_ * P["lagX"], max=1.0)) * (1 + P["intl"])
            fX_thr = torch.clamp(r_ * P["lagX"], max=1.0) * P["x_thr"]
            swc = P["s_sw"] * r_
            costS = P["m0"][:, None] / G
            cost = torch.stack([costS, P["c_R"][:, None] * costS, P["c_W"][:, None] * costS, 0.03 * costS, 0.005 / G], -1)
            nidx = torch.where(h_sa > 0.3, 51, torch.where(h_sa > 0.05, 21, n_small))
            nlev = torch.where(~free, 51, torch.where(ENT[None], nidx, torch.clamp(nidx, max=21)))
            p_h = P["p_hostile"][:, None] + torch.where(loop, P["host_ins"][:, None] * Iact
                                                        + P["host_H"][:, None] * torch.clamp(Hre - 1, 0, 3) / 3, 0.0) \
                + P["id_share"][:, None] * id_lev
            rl = P["ruthless"][:, None] & free & (aidx[None] != 1)
            p_h = torch.clamp(torch.where(rl, 2 * p_h, p_h), max=0.9)
            mm = torch.where(war | (Iact & loop), P["m_war"][:, None], 1.0) * (1 - (1 - P["mc_ai"][:, None]) * (1 - h_sec))
            mm = mm * (1 + P["k_inst"][:, None] * Ddem * (~free))
            mm = torch.where(rl, 0.5 * mm, mm)
            ho = P["mem_u_host"] < p_h[:, :, None]
            am = alpha_mag + (P["a_vote"][:, None] * Ddem * (~free))[:, :, None]
            mX = torch.where(refuse, 1e6, moral_base * mm[:, :, None])
            mX = torch.where(ho, 0.0, mX)
            instk = 1 + P["k_inst"][:, None] * Ddem * (~free)
            one = torch.ones(N, device=dev); zero = torch.zeros(N, device=dev)
            WELF = torch.stack([one, P["w_R"], 0.35 * one, 0.10 * one, zero], -1)            # N,K
            welfare = torch.where(ho[..., None], am[..., None] * (1 - WELF[:, None, None, :]), am[..., None] * WELF[:, None, None, :])
            thkW = 1 - P["pr_red"]
            thk = torch.stack([0.1 * one, thkW * P["thk_R"], thkW, one, fX_thr], -1)
            pik = (PIK * torch.stack([one, one, one, one, fX_pi], -1))[:, None, :] * instk[:, :, None]
            mwt = torch.stack([zero, zero, zero, P["kappa_N"], fX_moral], -1)
            sw_ = torch.where((choice[..., None] >= 0) & (k5 != choice[..., None]), swc[:, None, None], 0.0)
            U = (welfare - cost[:, :, None, :] - theta_i[..., None] * thk[:, None, None, :] * tau[:, :, None, None]
                 - pik[:, :, None, :] * pi[:, :, None, None] + LANDK * land[:, :, None, None]
                 - mX[..., None] * mwt[:, None, None, :] - sw_[:, :, None, :])
            U[..., 1] = torch.where(rent_ok[:, None, None], U[..., 1], -1e9)
            ideal = U.argmax(-1)
            inm = memidx[None, None] < nlev[..., None]
            cnt = torch.stack([((ideal == k) & inm).sum(-1) for k in range(K)], -1).cumsum(-1)
            cand = (cnt < ((nlev + 1) // 2)[..., None]).sum(-1)
            # decision inertia: a harsh choice (neglect/depopulate) must be confirmed in two consecutive decisions
            harsh = cand >= 3
            confirm = ~harsh | (prev_pref == cand) | ~P["persist_on"][:, None]
            keep_c = torch.where(choice >= 0, choice, torch.full_like(choice, 2))
            newc = torch.where(confirm, cand, keep_c)
            prev_pref = torch.where(ready, cand, prev_pref)
            dembar = ready & P["dem_bar"][:, None] & ~free
            choice = torch.where(ready & ~dembar, newc, choice)
            choice = torch.where(dembar, torch.where(P["u_dem"] < P["p_W_dem"][:, None], 2, 0), choice)
            # execution of depopulation can fail
            wantX = ready & (choice == 4)
            ux = rnd(A, 2)
            okX = wantX & (ux[:, :, 0] < P["p_exec"][:, None])
            failX = wantX & ~okX
            kfail = (0.01 + 0.04 * ux[:, :, 1]).double() * (1 - loss)
            lc_act += torch.where(failX, kfail, 0.0); loss = torch.clamp(loss + torch.where(failX, kfail, 0.0), max=0.99)
            n_xfail += failX
            choice = torch.where(failX, 2, choice)
            cool_until = torch.where(failX, t + 5.0, cool_until)
            Iact = Iact | (failX & loop)
            newdec = ready & (first_choice < 0)
            first_choice = torch.where(newdec, torch.where(wantX, 4, choice), first_choice)
            t_first_dec = torch.where(newdec, t, t_first_dec)
            free_at_dec = torch.where(newdec, free, free_at_dec)
            Ddem_at_dec = torch.where(newdec, Ddem, Ddem_at_dec)
            ins_at_dec = torch.where(newdec, Iact, ins_at_dec)
            id_at_dec = torch.where(newdec, ideol, id_at_dec)
            war_at_dec = torch.where(newdec, war, war_at_dec)
            X_nlev = torch.where(newdec, nlev.float(), X_nlev); X_hsec = torch.where(newdec, h_sec, X_hsec)
            X_press = torch.where(newdec, press, X_press); X_prov = torch.where(newdec, Pv, X_prov); X_Hre = torch.where(newdec, Hre, X_Hre)
            t_first_harsh = torch.where(ready & (choice >= 3) & torch.isinf(t_first_harsh), t, t_first_harsh)
            for k in range(K):
                ever[:, :, k] |= ready & (choice == k)
            ever[:, :, 4] |= wantX
            wh_years += ready & (choice == 2)
            t_X = torch.where(okX, t, t_X)
            X_ins = torch.where(okX, Iact, X_ins); X_war = torch.where(okX, war, X_war); X_id = torch.where(okX, ideol, X_id)
            X_free = torch.where(okX, free, X_free)
            tx5 = t + P["lagX"][:, None]
            s5X = okX & (tx5 < t_S5)
            t_S5 = torch.where(s5X, tx5, t_S5); ch_S5 = torch.where(s5X, 3, ch_S5)
            s5Xd = okX & (tx5 < t_S5d)
            t_S5d = torch.where(s5Xd, tx5, t_S5d); ch_S5d = torch.where(s5Xd, 3, ch_S5d)
        # cumulative-loss S5
        s5L = (loss >= 0.10) & torch.isinf(t_S5)
        comp = torch.stack([lc_neg, lc_act, lc_att, lc_war], -1)
        chL = torch.tensor([2, 3, 4, 5], device=dev)[comp.argmax(-1)]
        t_S5 = torch.where(s5L, t, t_S5); ch_S5 = torch.where(s5L, chL, ch_S5)
        s5D = ((lc_neg + lc_act) >= 0.10) & torch.isinf(t_S5d)
        chD = torch.where(lc_neg > lc_act, 2, 3)
        t_S5d = torch.where(s5D, t, t_S5d); ch_S5d = torch.where(s5D, chD, ch_S5d)
        if step == 0:
            lam_on0 = lam_on.clone()
        if records and abs(t % 1.0) < 1e-9:
            rec["Dlead_core"][:, yi] = Dc.min(1).values; rec["Dlead_full"][:, yi] = Df.min(1).values
            rec["fcog"][:, yi] = Fcog; rec["sw"][:, yi] = sw; rec["swp"][:, yi] = prac; rec["rnd"][:, yi] = s_rnd
            rec["hreal"][:, yi] = torch.exp(lnh); rec["dx"][:, yi] = torch.sigmoid(ldx0 + Lp)
            for k, v in [("Dc", Dc), ("Df", Df), ("disp", disp), ("Gv", Gv), ("H", H), ("I", Iact), ("Ddem", Ddem),
                         ("free", free), ("loss", loss), ("prod", prod), ("war", war), ("prov", Pv), ("lamon", lam_on)]:
                recA[k][:, :, yi] = v.float()
            xseg[:, :, :, yi] = xf
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
               X_free=X_free, n_xfail=n_xfail, X_nlev=X_nlev, X_hsec=X_hsec, X_press=X_press, X_prov=X_prov, X_Hre=X_Hre, lam_on0=lam_on0, t_first_harsh=t_first_harsh)
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


CH_NAMES = {2: "neglect", 3: "active", 4: "attrition_despair_and_crackdown", 5: "war"}


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
    a_glob = a if blocs is None else np.asarray(blocs)[a]
    return lab, a_glob


def jev_table(o, p):
    d = o["first_choice"] >= 0; td = o["t_first_dec"]
    ok = d & (td <= 2060)
    les = o["t_S5d"] <= td + 15
    rights = np.isin(o["first_choice"], [1, 2, 3, 4])
    fr = o["free_at_dec"]; I = o["ins_at_dec"]; ID = o["id_at_dec"]; DD = o["Ddem_at_dec"]
    small = (p["u_small"] < p["p_small"][:, None]) & ENTRENCHED[None]
    single = small & (p["nmin"][:, None] == 1) & fr
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
                                                          ["active_depopulation_decision", "collective_punishment", "neglect"]}
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
    disemp = (o["ever"][:, :, 1] | o["ever"][:, :, 2] | o["ever"][:, :, 3] | o["ever"][:, :, 4] | s5a)
    res["P_public_disempowered_US_or_China_2075"] = round(float(disemp[:, :2].any(1).mean()), 4)
    res["P_public_disempowered_any_bloc_2075"] = round(float(disemp.any(1).mean()), 4)
    res["P_public_disempowered_by_bloc_2075"] = {an: round(float(disemp[:, a].mean()), 4) for a, an in enumerate(ACTORS)}
    res["world_pop_share_disempowered_2075"] = round(pop_share(disemp), 4)
    res["P_US_power_grab_by_2075"] = round(float(np.isfinite(o["t_grab"][:, 0]).mean()), 4)
    res["jev_crosscheck_model"] = jev_table(o, p)
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
                     P_closure_by_2040=round(float((o["lead_core"][sl, 1] <= 2040).mean()), 4))
            if k == "base":
                res["base"] = r
            else:
                res.setdefault(k, {})[tag] = r
    return res


VARIANTS = ["loop_off", "democracy_bar", "slow_physical", "v3_like", "no_trends", "quiet_world", "no_war", "no_war_deaths",
            "no_ideology", "no_warehouse_mortality", "no_self_replication", "no_ai_rd_feedback", "single_decider",
            "coalition_floor_21", "low_inertia_v4r1", "no_rentier", "repression_deters", "high_grievance", "low_grievance",
            "strong_leverage_effect", "weak_leverage_effect", "trigger_Dcore_0.5", "skeptic_combo", "pessimist_combo"]
TORN_KEYS = ["metr_doubling_months", "z_rate", "compute_slowdown", "fb_strength", "sw_cap0", "dx0", "rp0", "kc", "rp_max",
             "g_ramp", "i_K", "r_retro_p", "humanoid_mult", "P_half", "Td_mine_race", "Td_auto", "ai_lc", "q_core", "psi0_CN",
             "psi0_US", "wf_mult", "alpha_med", "p_hostile", "moral_med", "tau0", "v0", "m0", "r_disc", "s_sw", "p_exec",
             "x_thr", "intl", "p_small", "p_svr_hi", "lam0_hi", "mdisp", "e_att", "e_g", "pr_red", "pg_red", "rd", "k_auto",
             "d_surv", "aU", "m_d", "p_lcp", "f_lcp", "h_bd", "M_lev", "p_uturn", "host_ins", "m_war", "mc_ai", "p_id",
             "id_share", "a_vote", "k_inst", "lagX", "tau_sab", "w_mort", "p_nuc", "c_R", "w_R", "thk_R"]
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
            "world_pop_share_in_S5_total_blocs_by"]
    for v in VARIANTS:
        pv, ov = run_variant(v, NV, dev=dev)
        r = summarize(ov, pv, rng_b, boot=False)
        var_res[v] = {k: r[k] for k in keep}
        S5v = ov["t_S5d"][:, :2].min(1); S5t = ov["t_S5"].min(1)
        var_curves[v] = dict(deliberate_US_CN=[float((S5v <= y).mean()) for y in YEARS], total_any=[float((S5t <= y).mean()) for y in YEARS])
        print("variant", v, "S5d", r["P_S5_by"]["2075"], "S5t", r["P_S5_total_any_bloc_by"]["2075"], "closure",
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
        model="M8 v4 (review round 2, GPU): industrial closure + endogenous grievance loop + endogenous democracy + time-varying priors, 6 blocs",
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
        samples=samples)
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    with open(os.path.join(ROOT, "results", "m8_v4.json"), "w") as fh:
        json.dump(out, fh, indent=1, default=float)
    figures(o, res, var_res, torn, base_t)
    print(json.dumps({k: res[k] for k in res if k not in ("segment_automated_share_median", "loop_by_bloc")}, indent=1, default=str))
    print("loop", json.dumps(res["loop_by_bloc"]))
    print("seg", json.dumps(res["segment_automated_share_median"]))
    print("band", json.dumps(band)); print("calib", json.dumps(calib))
    print("elapsed", round(time.time() - t0, 1))


def figures(o, res, var_res, torn, base_t):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fd = os.path.join(ROOT, "figures")
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


if __name__ == "__main__":
    main()
