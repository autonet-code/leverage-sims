"""
v7 actor constants: 17 actors replacing the six v6 blocs (research/v7_design.md, research/v7_actor_inputs.md).

Every array is indexed in ACTORS order. US = 0 and China = 1 (the integrator relies on that). Values marked
[P] are provisional estimates pending the sourced inputs in research/v7_actor_inputs.json; values marked [J] are
judgment. Where a six-bloc value was itself a judgment, the actor value is derived from it and the reason is given.
"""
import numpy as np

ACTORS = ["US", "China", "Japan", "South_Korea", "Taiwan", "Western_EU", "Eastern_EU", "UK", "CANZ",
          "Russia_CAsia", "Gulf", "Rest_MENA", "India", "Rest_South_Asia", "SE_Asia", "Latin_America", "SS_Africa"]
A_N = len(ACTORS)
IX = {a: i for i, a in enumerate(ACTORS)}
US, CN, JP, KR, TW, WEU, EEU, UK, CANZ, RU, GULF, RMENA, IN, RSA, SEA, LATAM, SSA = range(A_N)
PARENT = np.array([0, 1, 0, 0, 0, 2, 2, 2, 2, 3, 3, 3, 4, 4, 5, 5, 5])     # v6 bloc of each actor
ROW = [a for a in range(A_N) if a not in (US, CN)]

# ---- SOURCED INPUTS (research/v7_actor_inputs.json and .md: UN WPP 2024, ILOSTAT, SIPRI 2025, V-Dem v16 / Democracy
# Report 2026, UNIDO / World Bank, Ember / IEA, IFR World Robotics 2025-26, FAS 2026, USGS, SIA / TrendForce, Epoch AI).
# Order: US, China, Japan, South Korea, Taiwan, Western EU, Eastern EU, UK, CANZ, Russia, Gulf, Rest of MENA, India,
# Rest of South Asia, SE Asia, Latin America, SS Africa.
_SRC = dict(
    pop=[0.349, 1.421, 0.1224, 0.0516, 0.023, 0.3622, 0.1599, 0.0699, 0.073, 0.2373, 0.0624, 0.576, 1.4766, 0.5365, 0.7496, 0.6721, 1.3575],
    core_wf=[50.0, 294.3, 21.8, 9.7, 5.1, 52.1, 29.6, 8.3, 10.7, 39.6, 11.9, 63.5, 204.4, 59.1, 120.4, 92.9, 101.7],
    soc_exp=[19.8, 10.8, 24.7, 15.3, 11.0, 26.9, 20.6, 23.0, 18.9, 15.6, 8.7, 9.6, 5.1, 2.1, 4.7, 14.3, 2.5],
    gov_eff=[84.0, 69.9, 99.5, 91.0, 91.5, 86.1, 57.7, 85.8, 95.7, 31.1, 72.2, 31.8, 67.5, 25.6, 51.3, 41.7, 22.1],
    milex=[0.3306, 0.1162, 0.0215, 0.0165, 0.0063, 0.139, 0.0597, 0.0308, 0.0262, 0.0683, 0.0495, 0.0496, 0.0319, 0.0062, 0.0246, 0.0266, 0.0089],
    ldi=[0.571, 0.04, 0.734, 0.739, 0.704, 0.755, 0.473, 0.689, 0.761, 0.068, 0.07, 0.14, 0.26, 0.182, 0.238, 0.479, 0.243],
    autoc=[1.0, 0.005, 0.0, 0.0, 0.0, 0.192, 0.548, 1.0, 0.0, 0.069, 0.083, 0.025, 1.0, 0.562, 0.639, 0.358, 0.176],
    mva=[0.1734, 0.2802, 0.0474, 0.03, 0.0171, 0.1584, 0.0246, 0.0177, 0.0193, 0.0223, 0.0183, 0.032, 0.0297, 0.0102, 0.0486, 0.0607, 0.0115],
    ind_va=[0.1789, 0.2408, 0.0395, 0.0224, 0.0114, 0.1459, 0.0254, 0.0222, 0.0387, 0.0306, 0.0391, 0.0399, 0.0333, 0.0093, 0.0488, 0.0629, 0.0175],
    gw=[1333.2, 3901.1, 322.9, 158.9, 62.9, 1087.4, 267.7, 110.7, 281.9, 319.2, 217.5, 455.4, 555.5, 94.7, 368.6, 623.0, 153.2],
    re_mine=[0.1308, 0.6923, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0744, 0.0067, 0.0, 0.0, 0.0074, 0.0, 0.0694, 0.0051, 0.0108],
    re_ref=[0.025, 0.91, 0.005, 0.0, 0.0, 0.003, 0.005, 0.0, 0.002, 0.005, 0.0, 0.0, 0.005, 0.0, 0.035, 0.0, 0.0],
    magnet=[0.002, 0.94, 0.04, 0.002, 0.0, 0.005, 0.002, 0.001, 0.0, 0.0, 0.0, 0.0, 0.001, 0.0, 0.007, 0.0, 0.0],
    rob_inst=[0.0637, 0.5871, 0.06, 0.0497, 0.0116, 0.087, 0.0166, 0.0038, 0.0075, 0.0033, 0.0005, 0.0083, 0.0174, 0.0003, 0.0282, 0.0215, 0.0008],
    rob_dens=[307.0, 166.0, 446.0, 1220.0, 302.0, 267.0, 130.0, 110.0, 180.0, 10.0, 10.0, 30.0, 9.0, 1.0, 40.0, 25.0, 2.0],
    humanoid=[0.02, 0.97, 0.002, 0.003, 0.0, 0.003, 0.0, 0.0005, 0.0005, 0.0, 0.0, 0.0005, 0.0, 0.0, 0.0, 0.0, 0.0],
    fab=[0.1, 0.27, 0.14, 0.17, 0.18, 0.072, 0.002, 0.004, 0.001, 0.003, 0.0, 0.012, 0.001, 0.0, 0.045, 0.001, 0.0],
    adv=[0.08, 0.06, 0.0, 0.15, 0.7, 0.003, 0.0, 0.0, 0.0, 0.0, 0.0, 0.005, 0.0, 0.0, 0.0, 0.0, 0.0],
)
_S = {k: np.array(v, float) for k, v in _SRC.items()}

POP = _S["pop"]
WORKFORCE = _S["core_wf"]                                   # core-chain workers, millions (labor force x ISIC shares)
WORLD_W = _S["ind_va"] / _S["ind_va"].sum()                 # share of world industrial value added (import mix, output)
MFG_SHARE = _S["mva"] / _S["mva"].sum()                     # share of world manufacturing value added (human build capacity)
IB = np.minimum(1.0, np.sqrt(MFG_SHARE / MFG_SHARE[US]))
IB[CN] = 1.0
# general-purpose robot output: humanoid shipments (97% Chinese, 1H2026) blended 3:1 with industrial-robot installs
# (incumbent robot makers can switch) [J weights]
ROBOT_SHARE0 = np.maximum(0.75 * _S["humanoid"] + 0.25 * _S["rob_inst"], 5e-4)
# robot-input minerals: NdFeB magnets 0.5, rare-earth refining 0.3, mining 0.2 [J weights]
RE_SHARE0 = np.maximum(0.5 * _S["magnet"] + 0.3 * _S["re_ref"] + 0.2 * _S["re_mine"], 5e-4)
# robot inference chips: total fab capacity 0.7, advanced-node (<=7 nm) capacity 0.3 [J weights]
CHIP_SHARE0 = np.maximum(0.7 * _S["fab"] + 0.3 * _S["adv"], 5e-4)
E_GW0 = _S["gw"]
MIL0 = _S["milex"]

# ---- measured 2026 automated share of physical task value per segment (mining, energy, chips, manufacturing,
# logistics, construction, maintenance, security, admin). Manufacturing from IFR robot density, 0.02 + 1.3e-4 x density,
# capped at 0.15 (KR 1220 -> 0.15, JP 446 -> 0.078, US 307 -> 0.06, WEU 267 -> 0.055); China set to 0.06, not 0.042:
# IFR's 2026 revision (470 -> 166/10k) reflects a larger worker count, while value-weighted automation in leading sectors
# is higher [J]. Mining: autonomous haul trucks (GlobalData Jul 2025: China 2,090 of 3,832, Australia 1,024, Canada 344,
# Chile 208). Security higher for actors at war or fielding drones at scale (Ukraine, Russia, Israel/Turkey) [J].
X0 = np.array([
    [0.05, 0.05, 0.35, 0.00, 0.05, 0.005, 0.010, 0.03, 0.05],    # US
    [0.10, 0.05, 0.30, 0.00, 0.05, 0.006, 0.010, 0.03, 0.05],    # China
    [0.04, 0.06, 0.35, 0.00, 0.06, 0.006, 0.012, 0.02, 0.05],    # Japan
    [0.04, 0.05, 0.40, 0.00, 0.06, 0.006, 0.010, 0.03, 0.05],    # South Korea
    [0.03, 0.05, 0.40, 0.00, 0.05, 0.005, 0.010, 0.03, 0.05],    # Taiwan
    [0.05, 0.05, 0.30, 0.00, 0.05, 0.004, 0.008, 0.02, 0.05],    # Western EU
    [0.04, 0.04, 0.20, 0.00, 0.03, 0.003, 0.006, 0.05, 0.03],    # Eastern EU (+Ukraine)
    [0.04, 0.05, 0.25, 0.00, 0.05, 0.004, 0.008, 0.02, 0.05],    # UK
    [0.10, 0.05, 0.20, 0.00, 0.05, 0.004, 0.008, 0.02, 0.05],    # CANZ
    [0.05, 0.04, 0.15, 0.00, 0.02, 0.002, 0.004, 0.05, 0.03],    # Russia
    [0.05, 0.05, 0.10, 0.00, 0.04, 0.003, 0.005, 0.03, 0.04],    # Gulf
    [0.04, 0.04, 0.15, 0.00, 0.02, 0.002, 0.004, 0.04, 0.03],    # Rest of MENA
    [0.03, 0.03, 0.20, 0.00, 0.02, 0.002, 0.003, 0.01, 0.03],    # India
    [0.02, 0.02, 0.10, 0.00, 0.01, 0.001, 0.002, 0.01, 0.02],    # Rest of South Asia
    [0.05, 0.04, 0.30, 0.00, 0.04, 0.002, 0.004, 0.01, 0.02],    # SE Asia
    [0.06, 0.04, 0.20, 0.00, 0.02, 0.002, 0.004, 0.01, 0.02],    # Latin America
    [0.04, 0.03, 0.10, 0.00, 0.01, 0.001, 0.002, 0.01, 0.01]])   # SS Africa
X0[:, 3] = np.minimum(0.02 + 1.3e-4 * _S["rob_dens"], 0.15)
X0[CN, 3] = 0.06
# current growth of the automated share: the v6 parent bloc's row (Eastern EU security at war pace)
_G0_V6 = np.array([
    [0.25, 0.08, 0.05, 0.08, 0.20, 0.08, 0.05, 0.30, 0.05],
    [0.30, 0.12, 0.08, 0.15, 0.25, 0.10, 0.06, 0.30, 0.05],
    [0.15, 0.07, 0.05, 0.06, 0.15, 0.06, 0.04, 0.20, 0.05],
    [0.15, 0.05, 0.04, 0.05, 0.10, 0.04, 0.03, 0.30, 0.04],
    [0.20, 0.08, 0.05, 0.10, 0.12, 0.05, 0.04, 0.15, 0.05],
    [0.20, 0.06, 0.04, 0.07, 0.10, 0.04, 0.03, 0.15, 0.04]])
G0 = _G0_V6[PARENT].copy()
G0[EEU, 7] = 0.30
# automation-kit (robot stock) growth now: IFR 2025-26 (US stock +3-5%/yr, Japan installs -19%, EU -11%, India +15-17%)
G_IND = np.array([0.04, 0.15, 0.03, 0.04, 0.05, 0.03, 0.06, 0.03, 0.05, 0.03, 0.06, 0.05, 0.16, 0.05, 0.08, 0.05, 0.05])
# domestic share of each segment's inputs [J]: Japan, Korea, Taiwan import nearly all minerals and most energy;
# Taiwan and Korea make their own chips; CANZ and Russia are resource exporters
_OWN5 = np.array([
    [0.40, 0.90, 0.35, 0.65, 0.95],   # US
    [0.60, 0.80, 0.40, 0.95, 0.95],   # China (v6)
    [0.05, 0.15, 0.55, 0.85, 0.95],   # Japan
    [0.05, 0.20, 0.85, 0.80, 0.95],   # South Korea
    [0.02, 0.10, 0.95, 0.70, 0.95],   # Taiwan
    [0.20, 0.55, 0.30, 0.75, 0.95],   # Western EU
    [0.30, 0.65, 0.10, 0.60, 0.95],   # Eastern EU
    [0.10, 0.60, 0.10, 0.55, 0.95],   # UK
    [0.90, 0.95, 0.05, 0.45, 0.95],   # CANZ
    [0.85, 1.00, 0.05, 0.45, 0.95],   # Russia
    [0.40, 1.00, 0.02, 0.30, 0.95],   # Gulf
    [0.50, 0.85, 0.08, 0.45, 0.95],   # Rest of MENA
    [0.45, 0.70, 0.05, 0.55, 0.95],   # India
    [0.20, 0.60, 0.02, 0.35, 0.95],   # Rest of South Asia
    [0.60, 0.75, 0.25, 0.50, 0.95],   # SE Asia
    [0.80, 0.85, 0.05, 0.45, 0.95],   # Latin America
    [0.70, 0.75, 0.01, 0.25, 0.95]])  # SS Africa
OWN0 = np.concatenate([_OWN5, np.ones((A_N, 4))], 1)

# years each actor's deployable capability lags the frontier, U(lo, hi) [J]. AI compute share (Epoch): US 0.72,
# China 0.12, Western EU 0.05, SE Asia 0.04 (Johor), Gulf 0.015 (Stargate UAE under construction)
LAGC_LO = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0, 0.5, 0.25, 0.5, 0.25, 0.5, 0.25, 0.5, 0.5])
LAGC_HI = np.array([0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.5, 1.0, 1.0, 3.0, 1.5, 3.0, 2.0, 3.0, 2.5, 3.0, 3.0])
LAGP_LO = np.array([0.0, 0.0, 0.0, 0.0, 0.5, 0.5, 1.0, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.5, 1.0, 1.0, 1.5])
LAGP_HI = np.array([1.0, 0.0, 1.0, 1.0, 2.0, 2.0, 3.0, 2.5, 3.0, 4.0, 3.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0])

# ---- democracy: V-Dem v16 LDI (data year 2025), population-weighted within actors
D0 = _S["ldi"]
DMAX = np.array([0.80, 0.20, 0.80, 0.78, 0.80, 0.87, 0.75, 0.85, 0.87, 0.30, 0.25, 0.45, 0.60, 0.50, 0.55, 0.70, 0.55])
# starting provision: 0.1 + 0.018 x public social expenditure (% GDP), which reproduces the v6 anchors (US 19.8% -> 0.46,
# China 10.8% -> 0.29, Western EU 26.9% -> 0.58). Gulf 0.30: generous citizen transfers, nothing for the roughly half of
# residents who are migrant workers [J]
BASE_PROV = np.clip(0.1 + 0.018 * _S["soc_exp"], 0.08, 0.7)
BASE_PROV[GULF] = 0.30
# share of the actor's population in an ongoing autocratization episode (V-Dem Democracy Report 2026, Figure 14)
P_EP0 = _S["autoc"]
D_A_LO = np.array([-0.020, -0.005, -0.010, -0.010, -0.010, -0.010, -0.010, -0.010, -0.010, -0.010, -0.005, -0.010, -0.010, -0.010, -0.010, -0.010, -0.010])
D_A_HI = np.array([0.000, 0.015, 0.005, 0.005, 0.005, 0.005, 0.005, 0.005, 0.005, 0.010, 0.005, 0.010, 0.010, 0.010, 0.010, 0.010, 0.010])
DM_LO = np.full(A_N, 0.5)
DM_LO[US] = 0.6
DM_HI = np.full(A_N, 0.9)
ENTRENCHED = np.zeros(A_N, bool)
ENTRENCHED[[CN, RU, GULF, RMENA]] = True
# high-capacity state weight from the research capacity class (World Bank Government Effectiveness): high 1, medium 0.5,
# low 0.2, Rest of South Asia and SS Africa 0 as in v6; coercive-capacity overrides for Russia 0.7, Rest of MENA 0.4 and
# China 1.0, whose security states outrun their GE score [J]
HI_CAP = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5, 1.0, 1.0, 0.7, 1.0, 0.4, 0.5, 0.0, 0.5, 0.2, 0.0])
RICH_DEM = np.zeros(A_N, bool)
RICH_DEM[[US, JP, KR, TW, WEU, EEU, UK, CANZ]] = True          # breakdown hazard h_bd (Przeworski)
# nuclear status (FAS 2026), fractional where the arsenal belongs to a small member of the actor: India 190, Pakistan 170
# (Rest of South Asia), Israel 90 (Rest of MENA, which also hosts US weapons in Turkey), DPRK 60 (SE Asia) [J]
NUC_ARMED = np.zeros(A_N)
NUC_ARMED[[US, CN, WEU, UK, RU]] = 1.0
NUC_ARMED[IN] = 0.95
NUC_ARMED[RSA] = 0.85
NUC_ARMED[RMENA] = 0.45
NUC_ARMED[SEA] = 0.3
LETH_M = np.array([1.0, 1.0, 1.4, 1.0, 0.9, 1.3, 0.9, 1.2, 1.3, 0.6, 1.0, 0.8, 1.3, 1.5, 1.5, 1.8, 1.8])
GRAB_W = np.array([1.0, 0.0, 0.3, 0.6, 0.3, 0.4, 0.6, 0.4, 0.3, 0.0, 0.0, 0.3, 0.6, 0.6, 0.5, 0.6, 0.6])
RED_W = np.array([1.0, 0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.25, 0.2, 0.4, 1.0, 0.8, 0.6, 1.0, 0.8])
# pursuit-intensity multiplier on psi0_RW (US and China have their own priors and A2) [J]
PSI_M = np.array([1.0, 1.0, 2.5, 2.5, 2.0, 1.5, 1.0, 1.5, 1.2, 1.2, 1.5, 0.8, 1.0, 0.5, 0.8, 0.6, 0.4])
# personalist starting regimes: beta parameters of the leader's initial share (0 = not personalist at start)
PERS0 = {CN: (5.0, 5.0), RU: (7.5, 2.5), GULF: (7.0, 3.0)}

# ---- wars. Dyads (a, b, base hazard per year at 2026 conflict intensity) [J]. The v6 US-China pair hazard w_pair
# (median 0.007) is split into a direct US-China war and a China-Taiwan war that the US may join through its tie.
WAR_DYADS = [(US, CN, 0.003), (CN, TW, 0.006), (RU, EEU, 0.010), (IN, RSA, 0.020), (IN, CN, 0.004),
             (KR, SEA, 0.003), (CN, JP, 0.002), (CN, SEA, 0.004), (GULF, RMENA, 0.008)]
# remaining regional or civil war hazard multiplier on w_row (v6: x0.5 Europe, x1 Russia_MENA, x0.8 South Asia, x0.6
# Global South) [J]
WROW_M = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.2, 0.3, 0.1, 0.05, 0.5, 0.5, 1.0, 0.3, 0.8, 0.5, 0.4, 1.0])
AT_WAR0 = [RU, EEU]          # Russia-Ukraine war ongoing in 2026 (ukr_rem)

# ---- alliances: AL0[a, b] = strength of a's commitment to come to b's armed defence in 2026 (0 none, 1 credible and
# automatic), combining legal obligation, forward presence, nuclear umbrella and recent behaviour (research/
# v7_actor_inputs.json, alliances.pair_matrix; all judgment). Adjusted here where a commitment covers only a small member
# of a mixed actor, scaled by that member's weight [J]: Russia <-> SE Asia 0.55/0.6 -> 0.06 (the 2024 DPRK treaty; DPRK is
# ~4% of the actor), China -> SE Asia 0.4 -> 0.15 (DPRK treaty, Cambodia), US -> SE Asia 0.3 -> 0.2 (Philippines,
# Thailand), US -> Rest of MENA 0.4 -> 0.25 (Israel, Turkey in NATO, but Iran is in the same actor; cohesion 0.05).
AL0 = np.array([
    [0.0, 0.0, 0.7, 0.68, 0.3, 0.55, 0.5, 0.65, 0.5, 0.0, 0.4, 0.25, 0.05, 0.0, 0.2, 0.15, 0.0],
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.15, 0.0, 0.02, 0.0, 0.3, 0.15, 0.0, 0.0],
    [0.3, 0.0, 0.0, 0.05, 0.15, 0.0, 0.0, 0.0, 0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.12, 0.0, 0.0],
    [0.3, 0.0, 0.05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [0.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.55, 0.55, 0.35, 0.0, 0.2, 0.2, 0.0, 0.0, 0.0, 0.0, 0.05],
    [0.35, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.4, 0.2, 0.0, 0.0, 0.15, 0.0, 0.0, 0.0, 0.0, 0.0],
    [0.55, 0.0, 0.0, 0.0, 0.0, 0.6, 0.55, 0.0, 0.35, 0.0, 0.2, 0.2, 0.0, 0.0, 0.08, 0.0, 0.0],
    [0.45, 0.0, 0.2, 0.0, 0.0, 0.35, 0.4, 0.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.12, 0.0, 0.0],
    [0.0, 0.15, 0.0, 0.0, 0.0, 0.0, 0.05, 0.0, 0.0, 0.0, 0.0, 0.05, 0.05, 0.0, 0.06, 0.03, 0.12],
    [0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.2, 0.0, 0.3, 0.0, 0.0, 0.0],
    [0.25, 0.0, 0.0, 0.0, 0.0, 0.2, 0.0, 0.0, 0.0, 0.05, 0.3, 0.0, 0.0, 0.25, 0.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.15, 0.03, 0.0, 0.0],
    [0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.55, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0],
    [0.08, 0.2, 0.05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.06, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [0.05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]])
# within-actor security cohesion (research): Western EU 0.65, Eastern EU 0.4, Russia+CA 0.45, Gulf 0.45, Rest of MENA
# 0.05. Not used by the model (each actor decides as one coalition); reported as a limitation of the grouping.
COHESION = {WEU: 0.65, EEU: 0.4, RU: 0.45, GULF: 0.45, RMENA: 0.05}

# ---- institutions of the ruling elite: shares of (state, military, owners of AI and automated industry) [J]
INST_MIX = np.array([
    [0.45, 0.20, 0.35], [0.70, 0.20, 0.10], [0.50, 0.10, 0.40], [0.45, 0.15, 0.40], [0.50, 0.15, 0.35],
    [0.60, 0.15, 0.25], [0.55, 0.25, 0.20], [0.55, 0.15, 0.30], [0.55, 0.15, 0.30], [0.40, 0.45, 0.15],
    [0.70, 0.15, 0.15], [0.40, 0.45, 0.15], [0.55, 0.15, 0.30], [0.35, 0.50, 0.15], [0.50, 0.30, 0.20],
    [0.50, 0.25, 0.25], [0.45, 0.40, 0.15]])
# owners' share of control over the actor's automated force (private firms building and operating autonomous systems) [J]
OWN_AUTO = np.array([0.35, 0.05, 0.15, 0.20, 0.15, 0.10, 0.10, 0.15, 0.15, 0.05, 0.20, 0.10, 0.15, 0.05, 0.10, 0.15, 0.15])
DRIVES = ["Survival", "Status", "Meaning", "Connection", "Autonomy", "Comfort", "Curiosity"]
# Dirichlet concentration: base 1.5 per drive plus an institution tilt [J]
DRIVE_BASE = 1.5
DRIVE_TILT = np.array([
    [0.0, 0.8, 0.3, 0.5, 0.0, 0.2, 0.0],    # state: status, connection (constituencies), some meaning
    [0.8, 0.6, 0.4, 0.0, 0.0, 0.0, 0.0],    # military: survival (threat focus), status, meaning (mission)
    [0.0, 0.7, 0.2, 0.0, 0.8, 0.0, 0.8]])   # owners: status, autonomy, curiosity
# trait loadings on standardized drive shares (rows: traits; columns: DRIVES). Signs from the design doc [J]
TRAITS = ["moral", "concern", "hostile", "refuse", "threat", "exposed", "network", "ideology"]
TRAIT_W = np.array([
    [0.0, -1.0, 0.5, 1.0, 0.0, 0.0, 0.0],   # moral cost of ordering killing
    [0.0, -0.5, 0.0, 1.0, 0.0, 0.5, 0.0],   # concern for the public
    [0.0, 1.0, 0.0, -1.0, 0.0, 0.0, 0.0],   # hostility to the public
    [0.0, 0.0, 0.0, 1.0, 0.7, 0.0, 0.0],    # absolute refusal to order killing
    [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],    # threat sensitivity (revolt and latent threat)
    [1.0, 0.0, 0.0, 0.0, -0.3, 0.0, 0.0],   # feels exposed to purges (Brake 2)
    [0.0, 1.0, 0.0, 0.3, 0.0, 0.0, 0.0],    # strength of human network (who leads)
    [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.7]])   # susceptibility to a depopulation ideology
