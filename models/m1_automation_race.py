"""
S1 model: the automation race (m1_automation_race), v2
=======================================================

Question: given the world on 2026-09-30, how likely is it that competitive
pressure makes "automate" the dominant strategy across most of the economy,
forcing even benevolent employers to shed labor, with large NET labor-demand
displacement after general-equilibrium reallocation, and when?

v2 addresses a structural review of v1 (v1 was ~98.8% a capability+lag forecast):
* Capability: saturating (per-draw ceiling) benchmark horizon, uncertain trend
  break mean, a no-transfer mass (benchmark gains do not carry over to economic
  tasks), and an acceleration branch (AI R&D automation shortens doubling time).
* Physical automation: its own capability trajectory (slower doubling, own
  plateau and ceiling) and its own cost ratio (robot hardware ~0.5-1.5x wage in
  2026, falling 5-15%/yr), not the software curve.
* GE closure: real expenditure = 1 + phi*(1/P - 1) (phi = share of automation
  gains that becomes effective demand; S2 hook), allocated across sectors with
  CES elasticity sigma < 1 (Baumol). Net displacement is endogenous.
* Frictions scaled to the gain: one-off adoption cost = k x annual savings,
  oversight cost rising with depth, liability premium; switching derived from
  lognormal firm heterogeneity (not a step function).
* Real PD test: demand externality (firm revenue depends on aggregate labor
  income). PD exists only where all-A profit < all-R profit. Where a PD exists,
  an industry/government-brokered retention pact can form if legal and
  repeated-game sustainable (delta >= delta*); it shields the non-tradable part.
* Government/education: budget-pressure hazard, no rival threat, no market
  selection, higher union friction, political veto if regulation passes.
* Regulation: wide prior on effective strength (0-0.3) and instrument type
  (flat tax, payroll-parity tax, sector licensing ceilings, procurement rules).
* Adoption starts from process-automation shares (a few %), not "AI use".
* Records are end-of-year (state at y+1.0).

S1 event: in the same year (end of year), (i) ADOPTION: automated firms hold
>= 80% of output with realized depth >= 50% in sectors covering >= 50% of
baseline employment, and (ii) DISPLACEMENT: economy-wide net labor demand
(after GE reallocation and new tasks) is >= 15% below 2026. Horizon: end 2060.
Decomposition reported: P(feasible), P(deployed depth), P(adoption | depth),
P(displacement | adoption).
"""

import json
import os
import time
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)

import numpy as np
from scipy.special import expit
from scipy.stats import norm, spearmanr, beta as beta_dist

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = r"C:\code\sims\dystopia"
SEED = 20260930
N_DRAWS = int(os.environ.get("M1_N", 20000))
N_SUB = int(os.environ.get("M1_NSUB", 6000))
T0 = 2026.75
T_END = 2101.0
DT = 0.25
HORIZON = 2060
DOM_SHARE, DOM_DEPTH, DOM_EMP, DISP_THRESH = 0.80, 0.50, 0.50, 0.15

# name, emp, lcs, phys, mess, ceil, b2c, trad, comp, union, z0(process automation), liab, lic
SECTORS = [
    ("Information",        0.018, 0.22, 0.05, 0.60, 0.95, 0.50, 0.80, 1.2, 0.08, 0.08, 1.0, 0.0),
    ("Finance/insurance",  0.058, 0.25, 0.03, 0.35, 0.95, 0.50, 0.50, 1.0, 0.02, 0.06, 1.5, 0.5),
    ("Prof/business svcs", 0.142, 0.50, 0.15, 0.35, 0.92, 0.15, 0.50, 1.0, 0.02, 0.06, 1.2, 0.3),
    ("Trade (retail/whl)", 0.137, 0.25, 0.60, 0.20, 0.90, 0.80, 0.20, 1.2, 0.04, 0.04, 1.0, 0.0),
    ("Manufacturing",      0.080, 0.13, 0.75, 0.20, 0.95, 0.30, 0.90, 1.2, 0.08, 0.06, 1.0, 0.0),
    ("Transport/utilities",0.044, 0.33, 0.80, 0.20, 0.92, 0.40, 0.30, 1.0, 0.16, 0.03, 1.5, 0.5),
    ("Health/social",      0.147, 0.50, 0.55, 0.12, 0.75, 0.90, 0.05, 0.5, 0.07, 0.03, 2.0, 1.0),
    ("Government/educ",    0.173, 0.55, 0.35, 0.15, 0.75, 0.90, 0.00, 0.0, 0.32, 0.03, 1.5, 1.0),
    ("Leisure/hospitality",0.107, 0.33, 0.80, 0.20, 0.80, 1.00, 0.10, 1.0, 0.03, 0.02, 1.0, 0.0),
    ("Construction/mining",0.056, 0.35, 0.90, 0.10, 0.85, 0.50, 0.00, 0.8, 0.11, 0.02, 1.2, 0.3),
    ("Other services",     0.037, 0.40, 0.70, 0.15, 0.80, 0.90, 0.10, 0.8, 0.03, 0.02, 1.0, 0.2),
]
S = len(SECTORS)
SEC_NAMES = [s[0] for s in SECTORS]
col = lambda i: np.array([s[i] for s in SECTORS], float)
EMP, LCS, PHYS, MESS, CEIL, B2C, TRAD, COMP, UNION, Z0, LIAB, LIC = (col(i) for i in range(1, 13))
EMP = EMP / EMP.sum()
GOV = SEC_NAMES.index("Government/educ")
ALPHA = EMP / LCS
ALPHA = ALPHA / ALPHA.sum()          # 2026 expenditure (gross output) shares
BEN = np.array([0.1, 0.3, 0.5, 0.7, 0.9])
J = len(BEN)
M0 = 0.08                            # baseline net margin (cost-share units)
ANNUITY = 0.26                       # 5y amortization at 10%

# (central, low, high) ~ (median, 5th, 95th)
PRIORS = {
    # --- cognitive capability
    "H50_2026_hours": ((20, 8, 60), "METR (May 2026): best model 50% horizon >=16h, measurements >16h unreliable; Opus 4.6 ~12h. Extrapolation to 2026-09 at 3-7mo doubling, widened for the measurement ceiling [web]"),
    "H80_over_H50": ((0.15, 0.08, 0.25), "METR: Opus 4.6 80%/50% ~0.10; Mythos 3.1h/16h ~0.19 [web]"),
    "doubling_months": ((4.5, 3.0, 8.0), "METR TH1.1 (Jan 2026): ~7mo long run, ~4.3mo since 2023, ~3-4mo recently [web]"),
    "trend_break_mean_years": ((3.0, 1.0, 8.0), "Judgmental; per-draw mean of exponential waiting time to a slowdown (compute/power/data limits)"),
    "post_break_slowdown": ((3.0, 1.2, 20.0), "Judgmental: doubling-time multiplier after the break"),
    "p_plateau": ((0.25, 0.10, 0.45), "Judgmental (NOT tuned in v2): prob. of near-halt after break (x50 slowdown)"),
    "ceiling_decades": ((3.0, 1.2, 5.0), "Per-draw saturation of benchmark 80% horizon, decades above 2026 level (~3h): ~50h to ~300,000h (5-95%). Judgmental; long tasks are decomposable, so the upper range is wide"),
    "p_no_transfer": ((0.15, 0.05, 0.30), "Prob. benchmark horizon gains largely fail to transfer to economic tasks (METR limitations note; Humlum & Vestergaard realized savings 3%). In that case economic horizon grows at U(0,0.3) of benchmark rate"),
    "p_accel": ((0.15, 0.05, 0.30), "Prob. of AI-R&D feedback: after benchmark 80% horizon passes the threshold, each doubling takes x accel_factor the previous (AI 2027 / METR superexponential discussions). Judgmental"),
    "accel_threshold_h": ((160, 40, 1000), "Benchmark 80% horizon at which AI R&D is substantially automated (~1 work-month). Judgmental"),
    "accel_factor": ((0.8, 0.7, 0.9), "Doubling-time shrink per doubling in acceleration branch"),
    "task_horizon_median_h": ((60, 15, 250), "Judgmental; 2026 end-to-end feasibility a few % of tasks (Acemoglu 2024 4.6%; Humlum & Vestergaard 3%)"),
    "task_horizon_logsd": ((1.8, 1.3, 2.4), "Judgmental: tasks span minutes to months"),
    "mess_scale": ((1.0, 0.4, 2.5), "Draw-level scaling of sector messiness multipliers (METR messiness results)"),
    "ceiling_scale": ((0.90, 0.65, 1.05), "Scaling of sector automation ceilings; widened to include x0.7 (IMF 2024: ~half of AE exposure is complementary; Eloundou 2023)"),
    # --- physical
    "phys_gap_doublings": ((6.0, 3.0, 10.0), "Physical 'horizon' below cognitive in 2026, log2 units (McKinsey 2025: 13% robot-automatable hours vs 44% agent). Judgmental"),
    "phys_doubling_months": ((12.0, 6.0, 30.0), "Physical capability doubling time; slower than software (hardware iteration, data scarcity). Judgmental"),
    "p_plateau_phys": ((0.25, 0.10, 0.45), "Prob. dexterity/generalist robotics stalls (x20 slowdown after its own break, mean 5y). Judgmental"),
    "phys_ceiling_decades": ((3.0, 1.0, 5.0), "Physical capability saturation, decades above the 2026 COGNITIVE level (physical starts phys_gap_doublings lower). Judgmental"),
    "r_phys_2026": ((0.9, 0.5, 1.5), "Robot all-in cost (capex annualized + maintenance + integration) / wage per replaced task, 2026. IFR/ARK: arm ~$27k (2017) to ~$11k, but integration 2-4x hardware [web]"),
    "r_phys_decline": ((0.10, 0.05, 0.15), "e-fold/yr decline of robot cost; IFR ASP -3-5%/yr recently, -80% 1995-2017 (~7%/yr) [web]"),
    "r_phys_floor": ((0.20, 0.10, 0.40), "Floor on physical automation cost / wage (materials, energy, maintenance). Judgmental"),
    # --- cognitive AI cost and frictions
    "ai_cost_ratio_2026": ((0.15, 0.03, 0.6), "AI compute cost per feasible task / wage; Epoch price trends [web]"),
    "ai_cost_decline": ((0.5, 0.1, 1.5), "e-fold/yr decline of frontier-task cost; sticky frontier pricing (S3)"),
    "ai_cost_floor": ((0.03, 0.01, 0.10), "Judgmental floor (energy, hardware, provider margin)"),
    "oversight_cost": ((0.15, 0.05, 0.40), "Verification/oversight cost (wage units) per automated task at full depth; rises linearly with depth (longer tasks need more checking). Judgmental"),
    "liability_premium": ((0.04, 0.01, 0.12), "Liability/insurance premium (wage units) for automated tasks, scaled by sector (health x2). Judgmental"),
    "deployment_lag_years": ((5.0, 2.0, 12.0), "Realizing feasible tasks (David 1990; Brynjolfsson, Rock, Syverson 2021 J-curve); physical x1.5; speeds up with adopter share (learning by doing)"),
    "adoption_cost_multiple": ((2.0, 0.8, 5.0), "One-off integration/intangible cost as multiple of annual savings (intangibles several x technology cost: Brynjolfsson, Rock, Syverson 2021), annualized 5y@10%"),
    "firm_het_sigma": ((0.6, 0.3, 1.2), "Log-sd of firm-level net gain (firm heterogeneity; replaces step sigmoid). Judgmental"),
    "selection_rate": ((1.5, 0.4, 5.0), "Log-odds share gain per yr per unit price gap (Koch, Manuylov, Smolka 2021; Acemoglu, Lelarge, Restrepo 2020)"),
    "pass_through": ((0.75, 0.5, 1.0), "Cost pass-through to prices"),
    "switch_rate": ((0.25, 0.06, 0.8), "Max yearly R->A hazard among willing firms (Comin & Hobijn 2010; Fed 2026 worker adoption +31%/yr)"),
    "competitive_forcing_prob": ((0.7, 0.4, 0.9), "Research prior #22; psi = 3p multiplies rival-threat term"),
    "loss_aversion": ((2.25, 1.5, 3.0), "Tversky & Kahneman 1992"),
    "status_quo_bias": ((0.01, 0.002, 0.03), "Samuelson & Zeckhauser 1988 (cost-share units)"),
    "benevolence_mean": ((0.25, 0.1, 0.45), "Sraer & Thesmar 2007; Ellul, Pagano, Schivardi 2018"),
    "benevolence_max_sacrifice": ((0.06, 0.02, 0.15), "Max margin a fully benevolent owner forgoes (net margins ~5-10%)"),
    "shareholder_pressure_eta": ((2.0, 0.5, 5.0), "Benevolence erodes as (1-distress)^eta"),
    "union_strength": ((0.06, 0.01, 0.15), "Cost-equivalent at 100% density (ILA 2024-25; WGA/SAG 2023); x2 in government"),
    "human_premium": ((0.02, 0.003, 0.08), "Consumer premium for human-made"),
    "human_niche": ((0.08, 0.02, 0.25), "Share of B2C demand paying the premium"),
    "gov_budget_pressure": ((0.5, 0.2, 1.0), "Government adoption responds to budget savings at this fraction of a market firm's incentive; no rival threat. Judgmental"),
    # --- GE closure and labor
    "sigma_sub": ((0.5, 0.2, 0.9), "CES elasticity of substitution across sectors (<1 = Baumol); Nordhaus 2008 finds stagnant sectors price-inelastic [lit]"),
    "phi_recycle": ((0.8, 0.4, 1.0), "Share of real income gains from automation that becomes effective demand (capital-income recycling after monetary/fiscal offset; S2 hook). Judgmental"),
    "demand_lag_years": ((2.0, 1.0, 5.0), "Adjustment of sector demand to prices/income. Judgmental"),
    "reinstatement_rate": ((0.004, 0.0025, 0.006), "New-task labor demand per yr; Acemoglu & Restrepo 2019 JEP: 0.47%/yr 1947-87, 0.35%/yr 1987-2017 [web, verified]"),
    "newtask_automatable": ((0.7, 0.3, 1.0), "New tasks automatable in proportion abar * this. Judgmental"),
    "wage_elasticity": ((0.7, 0.3, 1.5), "Wage response to displacement (Acemoglu & Restrepo 2020)"),
    "wage_floor": ((0.45, 0.30, 0.65), "Reservation wage floor (min wage ~0.3-0.4 of median plus transfers) / 2026 wage. Judgmental"),
    "labor_income_demand_share": ((0.5, 0.2, 0.8), "Elasticity of firm demand to aggregate labor income (demand externality for the PD test; B2C-weighted). Judgmental"),
    # --- coordination
    "p_pact_legal": ((0.2, 0.05, 0.5), "Prob. a retention pact is legal/brokered (antitrust normally forbids competitor agreements; government-brokered sector deals possible). Judgmental"),
    "discount_factor": ((0.85, 0.70, 0.95), "Annual discount factor for repeated-game sustainability"),
    # --- regulation
    "p_regulation": ((0.40, 0.15, 0.70), "Prob. binding response once displacement bites; robot taxes mostly rejected so far (EU Parl. 2017)"),
    "reg_strength": ((0.08, 0.01, 0.25), "Effective strength after capture, 0-0.3 (tax cost share; payroll-parity fraction = strength/0.3; licensing ceiling cut = 2*strength). Beta prior"),
    "reg_trigger": ((0.06, 0.03, 0.12), "Displacement level that triggers response"),
    "reg_lag_years": ((2.0, 1.0, 5.0), "Legislative lag"),
    "trade_leak": ((0.5, 0.2, 0.9), "Share of tradable output escaping national regulation"),
    "p_gov_veto": ((0.5, 0.2, 0.8), "Prob. a regulating polity also halts public-sector automation (procurement/political veto)"),
    # --- v1 structural variant only
    "robot_lag_years": ((10, 4, 25), "v1 structural variant only: physical tasks on the cognitive curve shifted by this lag"),
}
BOUNDED = {"competitive_forcing_prob", "p_regulation", "benevolence_mean", "p_plateau", "p_no_transfer", "p_accel",
           "p_plateau_phys", "p_pact_legal", "discount_factor", "p_gov_veto", "phi_recycle", "accel_factor",
           "labor_income_demand_share", "newtask_automatable", "trade_leak"}
REG_TYPES = ["flat_tax", "payroll_parity", "licensing", "procurement"]
REG_TYPE_P = [0.30, 0.30, 0.25, 0.15]


def split_lognormal(rng, c, lo, hi, n):
    z = rng.standard_normal(n)
    s_lo = (np.log(c) - np.log(lo)) / 1.645
    s_hi = (np.log(hi) - np.log(c)) / 1.645
    return c * np.exp(np.where(z < 0, z * s_lo, z * s_hi))


def split_logit(rng, c, lo, hi, n):
    hi = min(hi, 0.995)
    c = min(c, 0.99)
    lc, ll, lh = (np.log(x / (1 - x)) for x in (c, lo, hi))
    z = rng.standard_normal(n)
    return expit(lc + np.where(z < 0, z * (lc - ll) / 1.645, z * (lh - lc) / 1.645))


def draw_params(rng, n):
    P = {}
    for k, ((c, lo, hi), _) in PRIORS.items():
        if k == "reg_strength":
            P[k] = 0.3 * rng.beta(1.2, 3.2, n)  # mean ~0.08, 95th ~0.2
        elif k in BOUNDED:
            P[k] = split_logit(rng, c, lo, hi, n)
        else:
            P[k] = split_lognormal(rng, c, lo, hi, n)
    P["ceiling_scale"] = np.clip(P["ceiling_scale"], 0.5, 1.05)
    P["pass_through"] = np.clip(P["pass_through"], 0.3, 1.0)
    P["sigma_sub"] = np.clip(P["sigma_sub"], 0.05, 0.98)
    P["trend_break_year"] = T0 + rng.exponential(1.0, n) * P["trend_break_mean_years"]
    P["phys_break_year"] = T0 + rng.exponential(5.0, n)
    P["plateau"] = rng.random(n) < P["p_plateau"]
    P["slowdown_eff"] = np.where(P["plateau"], np.maximum(P["post_break_slowdown"] * 50.0, 60.0), P["post_break_slowdown"])
    P["plateau_phys"] = rng.random(n) < P["p_plateau_phys"]
    P["no_transfer"] = rng.random(n) < P["p_no_transfer"]
    P["transfer_frac"] = np.where(P["no_transfer"], rng.uniform(0, 0.3, n), 1.0)
    P["accel"] = rng.random(n) < P["p_accel"]
    P["regulation_happens"] = rng.random(n) < P["p_regulation"]
    P["reg_type"] = rng.choice(4, n, p=REG_TYPE_P)
    P["gov_veto"] = rng.random(n) < P["p_gov_veto"]
    P["pact_legal"] = rng.random(n) < P["p_pact_legal"]
    # structural switches (0 = v2 baseline)
    P["mode_unbounded_cap"] = np.zeros(n)
    P["mode_robot_software"] = np.zeros(n)
    P["mode_demand_feedback"] = np.zeros(n)
    P["mode_no_coordination"] = np.zeros(n)
    return P


def benevolence_weights(mean, n, conc=4.0):
    edges = np.linspace(0, 1, J + 1)
    cdf = beta_dist.cdf(edges[None, :], (mean * conc)[:, None], ((1 - mean) * conc)[:, None])
    w = np.diff(cdf, axis=1)
    return w / w.sum(axis=1, keepdims=True)


def simulate(P, n, overrides=None):
    P = dict(P)
    if overrides:
        for k, v in overrides.items():
            P[k] = v(P) if callable(v) else np.broadcast_to(np.asarray(v), (n,)).copy()
    times = np.arange(T0, T_END + 1e-9, DT)
    years = np.arange(2027, 2101)
    # end-of-year y = state at time y+1.0
    rec_idx = {int(round((y + 1.0 - T0) / DT)): i for i, y in enumerate(years)}
    NY = len(years)

    unb = P["mode_unbounded_cap"] > 0.5
    rsw = P["mode_robot_software"] > 0.5
    dfb = P["mode_demand_feedback"] > 0.5
    nocoord = P["mode_no_coordination"] > 0.5

    # capability state (log2 hours of 80% horizon)
    l0 = np.log2(P["H50_2026_hours"] * P["H80_over_H50"])
    lb = l0.copy()                         # benchmark
    Lmax = np.where(unb, np.inf, l0 + P["ceiling_decades"] * np.log2(10))
    transfer = np.where(unb, 1.0, P["transfer_frac"])
    accel = P["accel"] & ~unb
    lacc = np.log2(P["accel_threshold_h"])
    rate0 = 12.0 / P["doubling_months"]
    lp0 = l0 - P["phys_gap_doublings"]
    lp = lp0.copy()
    Lpmax = np.minimum(Lmax, l0 + P["phys_ceiling_decades"] * np.log2(10))
    ratep0 = 12.0 / P["phys_doubling_months"]
    hist_le = np.zeros((len(times), n))     # for robot_software variant

    lnm = np.log(P["task_horizon_median_h"])
    sig = P["task_horizon_logsd"]
    mess = np.clip(MESS[None, :] * P["mess_scale"][:, None], 0.01, 1.0)
    ceil0 = np.clip(CEIL[None, :] * P["ceiling_scale"][:, None], 0.2, 0.99)
    ceil = ceil0.copy()

    def feas_from(l2):
        return norm.cdf((l2[:, None] * np.log(2) + np.log(mess) - lnm[:, None]) / sig[:, None])

    bw = benevolence_weights(P["benevolence_mean"], n)
    tilt = (1 - BEN)[None, None, :] * np.ones((n, S, J))
    z0 = np.clip(Z0[None, :, None] * tilt / (tilt * bw[:, None, :]).sum(2, keepdims=True), 0, 0.95)
    yA = bw[:, None, :] * z0
    yR = bw[:, None, :] * (1 - z0)
    qR = np.ones((n, S))

    psi = 3.0 * P["competitive_forcing_prob"]
    lam = P["loss_aversion"]
    sel = P["selection_rate"][:, None] * COMP[None, :]
    niche = P["human_niche"][:, None] * B2C[None, :]
    sigma = P["sigma_sub"][:, None]
    liab = P["liability_premium"][:, None] * LIAB[None, :]
    eL = P["labor_income_demand_share"]
    union_eff = UNION.copy()
    union_eff[GOV] *= 2.0
    nontrade = 1 - TRAD[None, :] * P["trade_leak"][:, None]

    fc = feas_from(l0)
    fp = np.minimum(feas_from(lp0), fc)
    Dc = ceil * fc
    Dp = ceil * fp
    Q = np.ones((n, S))
    MA = yA.sum(2)
    E0 = (EMP[None, :] * (1 - MA * ((1 - PHYS) * Dc + PHYS * Dp))).sum(1)
    disp = np.zeros(n)
    reg_on = np.full(n, np.inf)
    coord = np.zeros((n, S), bool)
    rt = P["reg_type"]
    rs = P["reg_strength"]

    K = ("disp", "wage", "abar", "rawfeas", "cogfeas", "physfeas", "dom_emp", "depth_emp", "feas_emp",
         "ben_R_share", "R_share", "tax", "coord_emp", "pd_emp", "LI", "Pidx", "l_econ", "l_phys")
    out = {k: np.zeros((n, NY), np.float32) for k in K}
    for k in ("MA", "D", "a", "E_sec"):
        out[k] = np.zeros((n, S, NY), np.float32)

    for it, t in enumerate(times):
        # ---- capability
        if it > 0:
            broke = t >= P["trend_break_year"]
            slow = np.where(broke, P["slowdown_eff"], 1.0)
            r = rate0 / slow
            am = np.where(accel, np.minimum(50.0, (1.0 / P["accel_factor"]) ** np.maximum(0, lb - lacc)), 1.0)
            r = r * am
            sat = np.where(unb, 1.0, np.clip(1 - np.exp(-(Lmax - lb) / 1.0), 0, 1))
            lb = lb + r * sat * DT
            slowp = np.where(P["plateau_phys"] & (t >= P["phys_break_year"]), 20.0, 1.0)
            satp = np.clip(1 - np.exp(-(Lpmax - lp) / 1.0), 0, 1)
            lp = lp + ratep0 / slowp * np.sqrt(am) * satp * DT
        le = l0 + transfer * (lb - l0)
        hist_le[it] = le
        fc = feas_from(le)
        if rsw.any():
            lag_steps = np.round(P["robot_lag_years"] / DT).astype(int)
            idx = np.clip(it - lag_steps, 0, it)
            le_lag = hist_le[idx, np.arange(n)]
            le_lag = np.where(it - lag_steps < 0, le_lag - (lag_steps - it) * DT * rate0, le_lag)
            fp_sw = feas_from(le_lag)
        else:
            fp_sw = fc
        fp_own = np.minimum(feas_from(lp), fc)
        fp = np.where(rsw[:, None], fp_sw, fp_own)

        # ---- regulation state
        trig = P["regulation_happens"] & (disp >= P["reg_trigger"]) & np.isinf(reg_on)
        reg_on = np.where(trig, t + P["reg_lag_years"], reg_on)
        on = t >= reg_on
        lic_cut = np.where(on & (rt == 2), np.minimum(0.9, 2 * rs), 0.0)
        ceil = ceil0 * (1 - lic_cut[:, None] * LIC[None, :])
        proc = on & ((rt == 3) | P["gov_veto"])
        ceil[:, GOV] = np.where(proc, np.minimum(ceil[:, GOV], 0.25), ceil[:, GOV])

        ac = ceil * fc
        ap = ceil * fp
        a = (1 - PHYS) * ac + PHYS * ap
        MA = yA.sum(2)
        speed = (0.5 + MA) / P["deployment_lag_years"][:, None]
        Dc = np.minimum(ac, Dc + np.maximum(ac - Dc, 0) * speed * DT) if it else Dc
        Dp = np.minimum(ap, Dp + np.maximum(ap - Dp, 0) * speed / 1.5 * DT) if it else Dp
        Dc = np.minimum(Dc, ac)
        Dp = np.minimum(Dp, ap)
        Dtot = (1 - PHYS) * Dc + PHYS * Dp

        # ---- costs
        w = np.maximum(P["wage_floor"], np.clip(1 - disp, 0, None) ** P["wage_elasticity"])[:, None]
        rc = np.maximum(P["ai_cost_floor"], P["ai_cost_ratio_2026"] * np.exp(-P["ai_cost_decline"] * (t - T0)))[:, None]
        rp_own = np.maximum(P["r_phys_floor"], P["r_phys_2026"] * np.exp(-P["r_phys_decline"] * (t - T0)))[:, None]
        rp = np.where(rsw[:, None], rc, rp_own)
        rc_all = rc + P["oversight_cost"][:, None] * Dc / np.maximum(ceil, 1e-6) + liab
        rp_all = rp + 0.5 * P["oversight_cost"][:, None] * Dp / np.maximum(ceil, 1e-6) + liab
        G = LCS[None, :] * ((1 - PHYS) * Dc * np.maximum(0, w - rc_all) + PHYS * Dp * np.maximum(0, w - rp_all))
        flat = np.where(on & (rt == 0), rs, 0.0)[:, None] * LCS[None, :] * (Dtot > 0.05)
        pp = np.where(on & (rt == 1), rs / 0.3, 0.0)[:, None] * LCS[None, :] * Dtot * w[:, :] * 1.0
        tax = (flat + pp) * nontrade
        Delta = G - tax

        # ---- selection
        MR = 1 - MA
        omega = expit((niche - MR) / 0.01)
        prem = P["human_premium"][:, None] * B2C[None, :] * np.clip(1 - disp, 0, 1)[:, None]
        sel_eff = sel * np.where(coord, TRAD[None, :], 1.0)
        fR = sel_eff * (omega * prem - P["pass_through"][:, None] * Delta)
        fbar = MR * fR
        dyR = yR * (fR - fbar)[:, :, None]
        dyA = yA * (-fbar)[:, :, None]
        qR = qR * np.exp((fR - fbar) * DT)
        distress = np.clip(1 - qR, 0, 1)

        # ---- PD test (economy-wide all-A vs all-R) and retention pacts
        E_allA = (EMP[None, :] * Q * (1 - Dtot)).sum(1)
        LI_allA = w[:, 0] * E_allA / E0
        dLI = np.clip(1 - LI_allA, 0, 1)
        demand_A = (1 + P["phi_recycle"][:, None] * P["pass_through"][:, None] * np.maximum(Delta, 0)) * \
                   (1 - eL[:, None] * (0.5 + 0.5 * B2C[None, :]) * dLI[:, None])
        pi_allA = (M0 + (1 - P["pass_through"][:, None]) * np.maximum(Delta, 0)) * demand_A
        pd = (Delta > 0) & (pi_allA < M0)
        pi_D = (M0 + np.maximum(Delta, 0)) * (1 + sel * P["pass_through"][:, None] * np.maximum(Delta, 0))
        dstar = (pi_D - M0) / np.maximum(pi_D - pi_allA, 1e-9)
        coord = pd & (P["discount_factor"][:, None] >= dstar) & P["pact_legal"][:, None] & ~nocoord[:, None]
        coord[:, GOV] = False

        # ---- switching (firm heterogeneity)
        gain = Delta * (1 + psi[:, None] * lam[:, None] * MA)
        gain[:, GOV] = Delta[:, GOV] * P["gov_budget_pressure"]
        adopt = lam[:, None] * P["adoption_cost_multiple"][:, None] * ANNUITY * G * (1 - 0.6 * MA)
        cost = adopt + P["status_quo_bias"][:, None] + union_eff[None, :] * P["union_strength"][:, None]
        benev = P["benevolence_max_sacrifice"][:, None, None] * BEN[None, None, :] * \
            ((1 - distress) ** P["shareholder_pressure_eta"][:, None])[:, :, None]
        tot_cost = cost[:, :, None] + benev
        frac = np.where(gain[:, :, None] > 0,
                        norm.cdf(np.log(np.maximum(gain, 1e-12)[:, :, None] / tot_cost) / P["firm_het_sigma"][:, None, None]), 0.0)
        frac = frac * np.where(coord, TRAD[None, :], 1.0)[:, :, None]
        gv = np.where(proc, 0.0, 1.0)
        frac[:, GOV, :] *= gv[:, None]
        haz = P["switch_rate"][:, None, None] * frac
        flow = yR * (1 - np.exp(-haz * DT))
        yR = np.clip(yR + dyR * DT - flow, 0, None)
        yA = np.clip(yA + dyA * DT + flow, 0, None)
        tot = (yR.sum(2) + yA.sum(2))[:, :, None]
        yR /= tot
        yA /= tot
        MA = yA.sum(2)

        # ---- GE closure: CES demand across sectors
        lab_int = 1 - MA * Dtot
        price = 1 - P["pass_through"][:, None] * MA * np.maximum(Delta, 0) + LCS[None, :] * lab_int * (w - 1)
        price = np.maximum(price, 0.05)
        Pidx = (ALPHA[None, :] * price ** (1 - sigma)).sum(1) ** (1 / (1 - sigma[:, 0]))
        Ireal = 1 + P["phi_recycle"] * (1 / Pidx - 1)
        LI = w[:, 0] * (1 - disp)
        Ireal = np.where(dfb, Ireal * np.clip(1 - eL * (1 - LI), 0.1, None), Ireal)
        Qstar = (price / Pidx[:, None]) ** (-sigma) * Ireal[:, None]
        Q = Q + (Qstar - Q) / P["demand_lag_years"][:, None] * DT
        E_sec = EMP[None, :] * Q * lab_int
        abar = (a * EMP).sum(1)
        newtasks = P["reinstatement_rate"] * (t - T0) * np.clip(1 - abar * P["newtask_automatable"], 0, 1)
        E = E_sec.sum(1) + newtasks
        disp = 1 - E / E0

        k = rec_idx.get(it)
        if k is not None:
            dom = (MA >= DOM_SHARE) & (Dtot >= DOM_DEPTH)
            out["disp"][:, k] = disp
            out["wage"][:, k] = w[:, 0]
            out["abar"][:, k] = abar
            raw = (1 - PHYS) * fc + PHYS * fp
            out["rawfeas"][:, k] = (raw * EMP).sum(1)
            out["cogfeas"][:, k] = (fc * EMP).sum(1)
            out["physfeas"][:, k] = (fp * EMP).sum(1)
            out["dom_emp"][:, k] = (dom * EMP).sum(1)
            out["depth_emp"][:, k] = ((Dtot >= DOM_DEPTH) * EMP).sum(1)
            out["feas_emp"][:, k] = ((a >= DOM_DEPTH) * EMP).sum(1)
            hib = BEN >= 0.7
            out["ben_R_share"][:, k] = (yR[:, :, hib].sum(2) / np.maximum(1e-12, (yR + yA)[:, :, hib].sum(2)) * EMP).sum(1)
            out["R_share"][:, k] = ((1 - MA) * EMP).sum(1)
            out["tax"][:, k] = tax.mean(1)
            out["coord_emp"][:, k] = (coord * EMP).sum(1)
            out["pd_emp"][:, k] = (pd * EMP).sum(1)
            out["LI"][:, k] = LI
            out["Pidx"][:, k] = Pidx
            out["l_econ"][:, k] = le
            out["l_phys"][:, k] = lp
            out["MA"][:, :, k] = MA
            out["D"][:, :, k] = Dtot
            out["a"][:, :, k] = a
            out["E_sec"][:, :, k] = E_sec / EMP[None, :]
    out["years"] = years
    return out


def first_year(mask, years):
    hit = mask.any(1)
    return np.where(hit, years[np.argmax(mask, axis=1)], np.inf)


def boot_ci(x, rng, B=2000, w=None):
    n = len(x)
    if w is None:
        bs = [x[rng.integers(0, n, n)].mean() for _ in range(B)]
    else:
        bs = []
        for _ in range(B):
            i = rng.integers(0, n, n)
            bs.append((x[i] * w[i]).sum() / w[i].sum())
    return float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))


def event_from(o):
    return first_year((o["dom_emp"] >= DOM_EMP) & (o["disp"] >= DISP_THRESH), o["years"])


def reweight(var_year, targets):
    """Weights making the CDF of var_year hit targets [(year, cdf), ...] (bin reweighting)."""
    edges = [-np.inf] + [y for y, _ in targets] + [np.inf]
    cdfs = [0.0] + [c for _, c in targets] + [1.0]
    w = np.ones(len(var_year))
    for i in range(len(edges) - 1):
        m = (var_year > edges[i]) & (var_year <= edges[i + 1])
        tgt = cdfs[i + 1] - cdfs[i]
        if m.mean() > 0:
            w[m] = tgt / m.mean()
        elif tgt > 0:
            pass  # unreachable target mass; left unmatched (reported)
    return w / w.mean()


def main():
    t_start = time.time()
    rng = np.random.default_rng(SEED)
    P = draw_params(rng, N_DRAWS)
    out = simulate(P, N_DRAWS)
    years = out["years"]
    yi = lambda y: int(np.where(years == y)[0][0])
    ye = event_from(out)
    hit = ye <= HORIZON
    p = float(hit.mean())
    brng = np.random.default_rng(SEED + 1)
    ci = boot_ci(hit.astype(float), brng)

    # ---- decomposition
    y_feas = first_year(out["feas_emp"] >= DOM_EMP, years)
    y_depth = first_year(out["depth_emp"] >= DOM_EMP, years)
    y_adopt = first_year(out["dom_emp"] >= DOM_EMP, years)
    y_disp = first_year(out["disp"] >= DISP_THRESH, years)
    F, Dd, A, X = (y <= HORIZON for y in (y_feas, y_depth, y_adopt, y_disp))
    both = hit & Dd
    agree = float(((hit == Dd)).mean())
    dec = {
        "P_feasible(a>=0.5 in >=50% emp)": float(F.mean()),
        "P_depth(D>=0.5 in >=50% emp; firm-strategy-free)": float(Dd.mean()),
        "P_adoption(MA>=0.8 & D>=0.5 in >=50% emp)": float(A.mean()),
        "P_displacement>=15%_any_year": float(X.mean()),
        "P_event": p,
        "P_event_given_depth": float(hit[Dd].mean()) if Dd.any() else None,
        "P_adoption_given_depth": float(A[Dd].mean()) if Dd.any() else None,
        "P_displacement_given_adoption(same-year event)": float(hit[A].mean()) if A.any() else None,
        "agreement_event_vs_depth_criterion": agree,
        "median_timing_gap_event_minus_depth_years": float(np.median((ye - y_depth)[both])) if both.any() else None,
        "P_event_given_capability_plateau": float(hit[P["plateau"]].mean()),
        "P_event_given_no_transfer": float(hit[P["no_transfer"]].mean()),
        "P_event_given_accel": float(hit[P["accel"]].mean()),
        "P_event_given_phys_plateau": float(hit[P["plateau_phys"]].mean()),
    }

    # ---- timeline, CDF
    yh = ye[hit]
    tl = {"p10_year": float(np.percentile(yh, 10)), "median_year": float(np.median(yh)), "p90_year": float(np.percentile(yh, 90))}
    fin = np.isfinite(ye)
    tl_all = {"p10_year": float(np.percentile(ye[fin], 10)), "median_year": float(np.median(ye[fin])),
              "p90_year": float(np.percentile(ye[fin], 90)), "share_ever_by_2100": float(fin.mean())}
    cdf_years = [2030, 2035, 2040, 2045, 2050, 2060, 2075, 2100]
    cdf = {y: float((ye <= y).mean()) for y in cdf_years}
    cdf_ci = {y: boot_ci((ye <= y).astype(float), brng, B=1000) for y in cdf_years}
    cum = np.cumsum(hit) / np.arange(1, N_DRAWS + 1)
    checkpoints = {k: float(cum[k - 1]) for k in (1000, 2500, 5000, 10000, 20000) if k <= N_DRAWS}

    thr = {}
    for d in (0.05, 0.10, 0.15, 0.25, 0.40):
        for de in (0.3, 0.5, 0.7):
            thr[f"disp>={d:.2f},dom_emp>={de:.1f}"] = float((first_year((out["dom_emp"] >= de) & (out["disp"] >= d), years) <= HORIZON).mean())

    q3 = lambda x: {"p10": float(np.percentile(x, 10)), "p50": float(np.median(x)), "p90": float(np.percentile(x, 90))}
    disp_q = {y: q3(out["disp"][:, yi(y)]) for y in (2027, 2030, 2035, 2040, 2045, 2050, 2060, 2075, 2100)}
    raw_q = {y: q3(out["rawfeas"][:, yi(y)]) for y in (2027, 2030, 2035, 2040, 2050, 2060)}
    abar_q = {y: q3(out["abar"][:, yi(y)]) for y in (2027, 2030, 2035, 2040, 2050, 2060)}
    wage_q = {y: float(np.median(out["wage"][:, yi(y)])) for y in (2030, 2040, 2050, 2060)}
    P_q = {y: float(np.median(out["Pidx"][:, yi(y)])) for y in (2030, 2040, 2050, 2060)}

    # ---- sectors (incl. who makes up the 50%)
    sector = {}
    for s, nm in enumerate(SEC_NAMES):
        dm = (out["MA"][:, s, :] >= DOM_SHARE) & (out["D"][:, s, :] >= DOM_DEPTH)
        ys = first_year(dm, years)
        ok = ys <= HORIZON
        dom_at_event = np.array([dm[i, yi(int(ye[i]))] if hit[i] else False for i in range(N_DRAWS)])
        sector[nm] = {"emp_weight": float(EMP[s]), "p_dominant_by_2040": float((ys <= 2040).mean()),
                      "p_dominant_by_2060": float(ok.mean()),
                      "median_year_if_by_2060": float(np.median(ys[ok])) if ok.any() else None,
                      "share_of_events_where_sector_dominant": float(dom_at_event[hit].mean()) if hit.any() else None,
                      "employment_2060_vs_2026_median": float(np.median(out["E_sec"][:, s, yi(2060)]))}

    # ---- PD / coordination / benevolence
    pd_info = {}
    for y in (2035, 2045, 2060):
        pd_info[str(y)] = {"mean_emp_share_with_PD": float(out["pd_emp"][:, yi(y)].mean()),
                           "P(PD in >=50% emp)": float((out["pd_emp"][:, yi(y)] >= 0.5).mean()),
                           "mean_emp_share_under_pact": float(out["coord_emp"][:, yi(y)].mean())}
    ben60 = out["ben_R_share"][:, yi(2060)]
    surv = ben60 >= 0.10
    ben = {"P(benevolent R firms keep >=10% capacity in 2060)": float(surv.mean()),
           "...given S1 event": float(surv[hit].mean()), "...given no S1 event": float(surv[~hit].mean()),
           "...given pact legal": float(surv[P["pact_legal"]].mean()),
           "...given benevolence_max_sacrifice > 0.10": float(surv[P["benevolence_max_sacrifice"] > 0.10].mean())}

    # ---- calibration anchors via reweighting (no retuning)
    y_raw90 = first_year(out["rawfeas"] >= 0.90, years)
    y_raw98 = first_year(out["rawfeas"] >= 0.98, years)
    y_meta = first_year((out["cogfeas"] >= 0.5) & (out["physfeas"] >= 0.25), years)
    anchors = {
        "prior_only (no reweighting)": np.ones(N_DRAWS),
        "Grace2024_HLMI (raw feasibility>=90%: 50% by 2047)": reweight(y_raw90, [(2047, 0.5)]),
        "Grace2024_FAOL (raw feasibility>=98%: 10% by 2037, ~45% by 2100)": reweight(y_raw98, [(2037, 0.10), (2100, 0.45)]),
        "Metaculus_AGI (cog>=50% & phys>=25%: 25% by 2029, 50% by 2033)": reweight(y_meta, [(2029, 0.25), (2033, 0.50)]),
        "2026_exposure (2027 raw feasibility 1-10% w.p. 0.9)": None,
    }
    r27 = out["rawfeas"][:, yi(2027)]
    inb = (r27 >= 0.01) & (r27 <= 0.10)
    w_exp = np.where(inb, 0.9 / max(inb.mean(), 1e-9), 0.1 / max((~inb).mean(), 1e-9))
    anchors["2026_exposure (2027 raw feasibility 1-10% w.p. 0.9)"] = w_exp / w_exp.mean()
    # equal-weight linear opinion pool: judgmental prior + three external capability anchors,
    # each multiplied by the 2026-exposure consistency weight
    wx = anchors["2026_exposure (2027 raw feasibility 1-10% w.p. 0.9)"]
    pool_members = [k for k in anchors if not k.startswith("2026_exposure")]
    w_pool = np.zeros(N_DRAWS)
    for k in pool_members:
        wk = anchors[k] * wx
        w_pool += wk / wk.mean()
    w_pool /= w_pool.mean()
    anchors["POOLED (equal weight: prior, HLMI, FAOL, Metaculus; x exposure)"] = w_pool
    calib = {}
    for nm, w in anchors.items():
        ess = float(w.sum() ** 2 / (w ** 2).sum())
        calib[nm] = {"p_event_by_2060": float((hit * w).sum() / w.sum()), "ess": round(ess),
                     "ci": boot_ci(hit.astype(float), brng, B=500, w=w),
                     "median_year_if_by_2060": float(np.median(np.repeat(ye[hit], np.maximum(1, np.round(w[hit] * 3).astype(int))))) if hit.any() else None}
    # ---- pooled headline
    def wq(x, w, q):
        o = np.argsort(x); x, w = x[o], w[o]
        c = np.cumsum(w) / w.sum()
        return float(np.interp(q, c, x))
    p_pool = float((hit * w_pool).sum() / w_pool.sum())
    ci_pool = boot_ci(hit.astype(float), brng, B=1000, w=w_pool)
    tl_pool = {"p10_year": wq(ye[hit], w_pool[hit], 0.10), "median_year": wq(ye[hit], w_pool[hit], 0.5), "p90_year": wq(ye[hit], w_pool[hit], 0.9)}
    cdf_pool = {y: float(((ye <= y) * w_pool).sum() / w_pool.sum()) for y in cdf_years}
    ess_pool = float(w_pool.sum() ** 2 / (w_pool ** 2).sum())
    cal_checks = {"P(raw feas>=90% by 2047)": float((y_raw90 <= 2047).mean()),
                  "P(raw feas>=98% by 2037)": float((y_raw98 <= 2037).mean()),
                  "P(raw feas>=98% by 2100)": float((y_raw98 <= 2100).mean()),
                  "P(metaculus-proxy by 2029)": float((y_meta <= 2029).mean()),
                  "P(metaculus-proxy by 2033)": float((y_meta <= 2033).mean()),
                  "P(2027 raw feasibility in 1-10%)": float(inb.mean())}

    # ---- Spearman
    sens = {}
    d2045 = out["disp"][:, yi(2045)]
    for k, v in P.items():
        x = np.asarray(v, float)
        if x.ndim != 1 or np.std(x) == 0 or k.startswith("mode_"):
            continue
        sens[k] = {"rho_event2060": float(spearmanr(x, hit)[0]), "rho_disp2045": float(spearmanr(x, d2045)[0])}
    sens = dict(sorted(sens.items(), key=lambda kv: -abs(kv[1]["rho_event2060"])))

    # ---- paired toggles on a common-random-number subsample
    ns = min(N_SUB, N_DRAWS)
    Ps = {k: v[:ns] for k, v in P.items()}
    hb = event_from(simulate(Ps, ns)) <= HORIZON
    ones = lambda Q: np.ones(ns, bool)
    zeros_b = lambda Q: np.zeros(ns, bool)
    toggles = {
        "psi=0 (no rival-threat term)": {"competitive_forcing_prob": 0.0},
        "no_retention_pacts": {"mode_no_coordination": 1.0},
        "pacts_legal_and_patient (legal, delta=0.97)": {"pact_legal": ones, "discount_factor": 0.97},
        "no_behavioral_frictions": {"loss_aversion": 1.0, "status_quo_bias": 0.0, "benevolence_max_sacrifice": 0.0, "union_strength": 0.0, "adoption_cost_multiple": 0.0},
        "high_frictions (adopt 5x, oversight 0.4, liab 0.12)": {"adoption_cost_multiple": 5.0, "oversight_cost": 0.4, "liability_premium": 0.12},
        "high_benevolence (mean 0.6, sacrifice 0.15)": {"benevolence_mean": 0.6, "benevolence_max_sacrifice": 0.15},
        "ai_cost_x3 (S3 markup)": {"ai_cost_ratio_2026": lambda Q: Q["ai_cost_ratio_2026"] * 3, "ai_cost_floor": lambda Q: Q["ai_cost_floor"] * 3},
        "regulation_never": {"regulation_happens": zeros_b},
        "regulation_certain (drawn instrument/strength)": {"regulation_happens": ones},
        "strong_plateau max(slowdown,20)": {"slowdown_eff": lambda Q: np.maximum(Q["slowdown_eff"], 20.0)},
        "trend_break_2027": {"trend_break_year": 2027.0},
        "no_acceleration": {"accel": zeros_b},
        "acceleration_certain": {"accel": ones},
        "ceilings_x0.7": {"ceiling_scale": lambda Q: Q["ceiling_scale"] * 0.7},
        "deployment_lag_12y": {"deployment_lag_years": 12.0},
        "no_wage_adjustment": {"wage_elasticity": 1e-6},
        "sigma=0.2 (strong Baumol)": {"sigma_sub": 0.2},
        "sigma=0.9": {"sigma_sub": 0.9},
        "phi=0.4 (weak recycling)": {"phi_recycle": 0.4},
        "phi=1.0 (full recycling)": {"phi_recycle": 1.0},
    }
    for tx in (0.05, 0.10, 0.15, 0.20, 0.30):
        toggles[f"payroll_parity_tax certain, strength {tx:.2f}"] = {"regulation_happens": ones, "reg_type": 1, "reg_strength": tx, "reg_trigger": 0.03}
    for tx in (0.10, 0.25):
        toggles[f"flat_tax certain, strength {tx:.2f}"] = {"regulation_happens": ones, "reg_type": 0, "reg_strength": tx, "reg_trigger": 0.03}
        toggles[f"licensing certain, strength {tx:.2f}"] = {"regulation_happens": ones, "reg_type": 2, "reg_strength": tx, "reg_trigger": 0.03}
    structural = {
        "STRUCT v1 capability form (unbounded, no transfer/accel)": {"mode_unbounded_cap": 1.0, "trend_break_year": lambda Q: T0 + (Q["trend_break_year"] - T0) / Q["trend_break_mean_years"] * 3.0},
        "STRUCT robots on cognitive curve at software cost (v1 form)": {"mode_robot_software": 1.0},
        "STRUCT v1 capability + v1 robots": {"mode_unbounded_cap": 1.0, "mode_robot_software": 1.0},
        "STRUCT demand feedback on (S2 channel inside S1)": {"mode_demand_feedback": 1.0},
        "STRUCT no Baumol (sigma~1, Cobb-Douglas)": {"sigma_sub": 0.98},
    }
    toggles.update(structural)
    scen = {"baseline_subsample": {"p_by_2060": float(hb.mean()), "n": ns}}
    prng = np.random.default_rng(SEED + 5)
    for nm, ov in toggles.items():
        ht = event_from(simulate(Ps, ns, overrides=ov)) <= HORIZON
        dlt = ht.astype(float) - hb.astype(float)
        scen[nm] = {"p_by_2060": float(ht.mean()), "paired_diff": float(dlt.mean()), "paired_diff_ci95": boot_ci(dlt, prng, B=1000)}
        print(f"  {nm:62s} {ht.mean():.3f}  diff {dlt.mean():+.3f}", flush=True)

    # tax threshold (payroll parity, certain)
    tax_curve = {k: v["p_by_2060"] for k, v in scen.items() if k.startswith("payroll_parity")}
    xs = np.array([0.0] + [float(k.split()[-1]) for k in tax_curve])
    ys_ = np.array([scen["regulation_never"]["p_by_2060"]] + list(tax_curve.values()))
    def thresh(level):
        below = np.where(ys_ <= level)[0]
        if not len(below):
            return None
        i = below[0]
        if i == 0:
            return 0.0
        return float(xs[i - 1] + (xs[i] - xs[i - 1]) * (ys_[i - 1] - level) / (ys_[i - 1] - ys_[i]))
    tax_thr = {"curve_strength_to_p": dict(zip([f"{x:.2f}" for x in xs], [float(v) for v in ys_])),
               "strength_halving_p_vs_no_regulation": thresh(ys_[0] / 2), "strength_for_p_below_0.10": thresh(0.10),
               "note": "payroll-parity strength s taxes s/0.3 of gross labor cost saved (0.3 = full parity), non-tradable share, trigger 3% displacement, drawn lag"}

    # structural band: baseline + structural forms + calibration anchors
    band_vals = {"POOLED headline": p_pool, "prior-only baseline": p}
    band_vals.update({k: scen[k]["p_by_2060"] - scen["baseline_subsample"]["p_by_2060"] + p for k in structural})
    band_vals.update({"CAL " + k: v["p_event_by_2060"] for k, v in calib.items()})
    band = {"low": float(min(band_vals.values())), "high": float(max(band_vals.values())), "members": band_vals,
            "note": "Structural variants rescaled to full-sample baseline via paired difference. Toggles of single priors (regulation, ceilings, lags) are NOT in the band; they are prior tails."}

    elapsed = time.time() - t_start

    # ---- export
    b2c_w, b2b_w = EMP * B2C, EMP * (1 - B2C)
    Eb2c = (out["E_sec"] * b2c_w[None, :, None]).sum(1) / b2c_w.sum()
    Eb2b = (out["E_sec"] * b2b_w[None, :, None]).sum(1) / b2b_w.sum()
    samp = np.random.default_rng(SEED + 2).choice(N_DRAWS, min(4000, N_DRAWS), replace=False)
    res = {
        "stage": "S1 automation race",
        "version": 2,
        "run": {"seed": SEED, "n_draws": N_DRAWS, "n_toggle_subsample": ns, "dt_years": DT, "t0": T0, "elapsed_s": round(elapsed, 1)},
        "stage_probability": {
            "mean": p_pool, "ci_low": ci_pool[0], "ci_high": ci_pool[1], "ess": round(ess_pool),
            "prior_only_mean": p, "prior_only_ci": list(ci),
            "structural_band": [band["low"], band["high"]],
            "definition": (f"Unconditional (first stage). P that by end of {HORIZON}, in the same year, (i) automated firms hold >= {DOM_SHARE:.0%} of "
                           f"output with realized automation depth >= {DOM_DEPTH:.0%} in sectors covering >= {DOM_EMP:.0%} of 2026 employment, and (ii) "
                           f"economy-wide net labor demand after CES/Baumol reallocation and new tasks is >= {DISP_THRESH:.0%} below 2026. "
                           "Headline = equal-weight linear pool of 4 capability views (judgmental prior; draws reweighted to Grace et al 2024 HLMI; to FAOL; to Metaculus AGI), "
                           "each also weighted for consistency with 2026 exposure. CI = Monte Carlo sampling error only (weighted bootstrap); "
                           "structural_band = range across alternative model forms and calibration anchors."),
        },
        "decomposition": dec,
        "timeline": {**tl_pool, "definition": f"Pooled: calendar year (end of year) of first S1 event among draws with event by {HORIZON}"},
        "timeline_prior_only": tl,
        "cdf_event_by_year_pooled": {str(k): v for k, v in cdf_pool.items()},
        "timeline_all_by_2100": tl_all,
        "cdf_event_by_year_prior_only": {str(k): v for k, v in cdf.items()},
        "cdf_event_by_year_prior_only_ci": {str(k): v for k, v in cdf_ci.items()},
        "convergence_running_mean": {str(k): v for k, v in checkpoints.items()},
        "threshold_sensitivity_by_2060": thr,
        "displacement_quantiles": {str(k): v for k, v in disp_q.items()},
        "raw_feasibility_quantiles_emp_weighted": {str(k): v for k, v in raw_q.items()},
        "ceilinged_feasible_share_quantiles": {str(k): v for k, v in abar_q.items()},
        "wage_index_median": {str(k): v for k, v in wage_q.items()},
        "price_index_median": {str(k): v for k, v in P_q.items()},
        "sectors": sector,
        "prisoners_dilemma_and_pacts": pd_info,
        "benevolent_survival": ben,
        "calibration_anchors": calib,
        "calibration_checks_prior": cal_checks,
        "scenario_toggles_paired": scen,
        "regulation_tax_threshold": tax_thr,
        "structural_band": band,
        "sensitivity_spearman": sens,
        "for_other_stages": {
            "note": "End-of-year values, years 2027..2100. Demand feedback (S2) is OFF in the headline; its effect is in scenario 'STRUCT demand feedback on'.",
            "years": years.tolist(),
            "displacement_median": np.median(out["disp"], 0).round(4).tolist(),
            "displacement_p10": np.percentile(out["disp"], 10, 0).round(4).tolist(),
            "displacement_p90": np.percentile(out["disp"], 90, 0).round(4).tolist(),
            "labor_income_index_median": np.median(out["LI"], 0).round(4).tolist(),
            "b2c_employment_index_median": np.median(Eb2c, 0).round(4).tolist(),
            "b2b_employment_index_median": np.median(Eb2b, 0).round(4).tolist(),
            "automated_output_share_emp_weighted_median": np.median(1 - out["R_share"], 0).round(4).tolist(),
        },
        "samples": {
            "note": "4000 random draws; event_year null if none by 2100.",
            "event_year": [None if not np.isfinite(v) else int(v) for v in ye[samp]],
            "hit_by_2060": hit[samp].astype(int).tolist(),
            "disp_2035": out["disp"][samp, yi(2035)].round(4).tolist(),
            "disp_2045": out["disp"][samp, yi(2045)].round(4).tolist(),
            "disp_2060": out["disp"][samp, yi(2060)].round(4).tolist(),
            "labor_income_2045": out["LI"][samp, yi(2045)].round(4).tolist(),
        },
        "priors": {k: {"central": v[0][0], "low": v[0][1], "high": v[0][2], "source": v[1]} for k, v in PRIORS.items()},
    }
    with open(os.path.join(ROOT, "results", "m1_automation_race.json"), "w") as f:
        json.dump(res, f, indent=1)

    # ---- figures
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.5))
    x = years
    ax[0].fill_between(x, np.percentile(out["disp"], 10, 0) * 100, np.percentile(out["disp"], 90, 0) * 100, color="#4a7bb7", alpha=0.2, label="10-90%")
    ax[0].fill_between(x, np.percentile(out["disp"], 25, 0) * 100, np.percentile(out["disp"], 75, 0) * 100, color="#4a7bb7", alpha=0.35, label="25-75%")
    ax[0].plot(x, np.median(out["disp"], 0) * 100, color="#1f3f73", lw=2, label="median")
    ax[0].axhline(DISP_THRESH * 100, color="#b0413e", ls="--", lw=1, label=f"threshold {DISP_THRESH:.0%}")
    ax[0].set_xlim(2027, 2090)
    ax[0].set_ylabel("Net labor-demand displacement vs 2026 (%)")
    ax[0].set_title("Net displacement after GE reallocation")
    ax[0].legend(frameon=False, fontsize=8)
    ax[0].grid(alpha=0.3)
    cy = np.arange(2027, 2101)
    for yv, lab, c, ls in ((y_feas, "feasible (a>=0.5, >=50% emp)", "#7a9a3a", ":"), (y_depth, "deployed depth (firm-free)", "#c28a2c", "-."),
                           (y_adopt, "adoption dominant", "#6a4c93", "--"), (ye, "S1 event, prior only", "#1f3f73", "-")):
        ax[1].plot(cy, [(yv <= y).mean() for y in cy], color=c, lw=2 if lab.startswith("S1") else 1.3, ls=ls, label=lab)
    ax[1].plot(cy, [((ye <= y) * w_pool).sum() / w_pool.sum() for y in cy], color="#b0413e", lw=2.2, label="S1 event, pooled calibration (headline)")
    ax[1].axvline(HORIZON, color="grey", ls="--", lw=1)
    ax[1].set_xlim(2027, 2100)
    ax[1].set_ylim(0, 1)
    ax[1].set_ylabel("Cumulative probability")
    ax[1].set_title(f"P(S1 by {HORIZON}): pooled {p_pool:.2f}, prior-only {p:.2f}; band {band['low']:.2f}-{band['high']:.2f}", fontsize=10)
    ax[1].legend(frameon=False, fontsize=8)
    ax[1].grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(ROOT, "figures", "m1_automation_race_timeline.png"), dpi=140)
    plt.close(fig)

    fig, ax = plt.subplots(1, 2, figsize=(13, 5))
    order = np.argsort([sector[nm]["p_dominant_by_2060"] for nm in SEC_NAMES])
    names = [SEC_NAMES[i] for i in order]
    ax[0].barh(names, [sector[nm]["p_dominant_by_2040"] for nm in names], color="#1f3f73", label="by 2040")
    ax[0].barh(names, [sector[nm]["p_dominant_by_2060"] - sector[nm]["p_dominant_by_2040"] for nm in names],
               left=[sector[nm]["p_dominant_by_2040"] for nm in names], color="#8fb0dc", label="2041-2060")
    ax[0].set_xlim(0, 1)
    ax[0].set_xlabel("P(automation dominant in sector)")
    ax[0].set_title("Automation dominant, by sector")
    ax[0].legend(frameon=False, fontsize=8)
    ax[0].grid(alpha=0.3, axis="x")
    items = [(k, v) for k, v in scen.items() if k != "baseline_subsample"]
    items.sort(key=lambda kv: kv[1]["paired_diff"])
    labs = [k[:48] for k, _ in items]
    d = np.array([v["paired_diff"] for _, v in items])
    lo = np.array([v["paired_diff_ci95"][0] for _, v in items])
    hi = np.array([v["paired_diff_ci95"][1] for _, v in items])
    yy = np.arange(len(items))
    ax[1].barh(yy, d, color=np.where(d < 0, "#4a7bb7", "#b0413e"), alpha=0.8)
    ax[1].errorbar(d, yy, xerr=[d - lo, hi - d], fmt="none", ecolor="k", lw=0.8)
    ax[1].set_yticks(yy)
    ax[1].set_yticklabels(labs, fontsize=6.5)
    ax[1].axvline(0, color="k", lw=0.8)
    ax[1].set_xlabel(f"Paired change in P(S1 by {HORIZON}) vs baseline ({scen['baseline_subsample']['p_by_2060']:.2f})")
    ax[1].set_title("Toggles and structural variants (CRN, 95% CI)")
    ax[1].grid(alpha=0.3, axis="x")
    fig.tight_layout()
    fig.savefig(os.path.join(ROOT, "figures", "m1_automation_race_sectors.png"), dpi=140)
    plt.close(fig)

    print(f"draws={N_DRAWS} elapsed={elapsed:.1f}s")
    print(f"POOLED P(S1 by {HORIZON}) = {p_pool:.4f} CI {ci_pool} ess {ess_pool:.0f}; timeline {tl_pool}; cdf {cdf_pool}")
    print(f"prior-only P(S1 by {HORIZON}) = {p:.4f} CI [{ci[0]:.4f}, {ci[1]:.4f}]  band [{band['low']:.3f}, {band['high']:.3f}]")
    print("timeline:", tl, tl_all)
    print("cdf:", cdf)
    print("decomposition:", json.dumps(dec, indent=0))
    print("calib:", json.dumps(calib, indent=0))
    print("cal checks:", cal_checks)
    print("disp:", json.dumps(disp_q))
    print("rawfeas:", json.dumps(raw_q))
    print("PD:", json.dumps(pd_info))
    print("benev:", json.dumps(ben))
    print("tax thr:", json.dumps(tax_thr))
    print("band:", json.dumps(band, indent=0))
    for nm, v in sector.items():
        print(f"  {nm:22s} P2040={v['p_dominant_by_2040']:.2f} P2060={v['p_dominant_by_2060']:.2f} inEvent={v['share_of_events_where_sector_dominant']} E2060={v['employment_2060_vs_2026_median']:.2f}")
    for k, v in list(sens.items())[:14]:
        print(f"  {k:28s} {v['rho_event2060']:+.3f} {v['rho_disp2045']:+.3f}")


if __name__ == "__main__":
    main()
