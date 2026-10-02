"""
S2 "No customers" domino: Monte Carlo input-output cascade model (v2, post-review).

Question: GIVEN S1 (a competitive automation race is under way), how likely is
(a) the end of broad economic participation, and (b) a self-reinforcing collapse
of mass-market demand that cascades from B2C into B2B, when, and does the demand
collapse speed up or slow down automation?

Two outcome definitions (reported separately, see OUTCOMES below):
  S2a  participation collapse: jobs-lost share (vs 2026 employment) >= 0.30 for
       >= 8 consecutive quarters. This is the scenario's stated S2 ("end of broad
       economic participation") and is the input for the S4/S5 "mouths to feed"
       logic. Transfer dependence of bottom-80 households is reported alongside.
  S2b  consumption cascade ("no customers"): bottom-80 real consumption <= 0.75
       of 2026 for >= 8 consecutive quarters AND household-serving B2B real
       output <= 0.90 of 2026 within that window.

Structure (quarterly, 2026Q4 .. 2060Q4, vectorised over N parameter draws)
* 10 occupational categories; automation becomes technically possible at T_k
  (frontier timeline D x difficulty) then diffuses logistically; adoption is
  accelerated by revenue pressure and slowed early by benevolent firms (S1).
* Sectors: B2C mass, B2C premium (human-premium Baumol share), B2B household-
  serving (lagged, bullwhip; ALSO hit directly by employers cancelling per-seat /
  per-employee services as they automate), government, investment (accelerator
  + reinvested profits + AI capex).
* Households (v2): disposable income (after tax). Bottom-80 APC ~0.92-1.02;
  top-20 consume apc_t x disposable income plus a wealth effect (MPC out of
  wealth 3-5%/yr). Permanent-income rule C* = C0 (Y/Y0)^e (proportional).
* Retained profits not invested accumulate as top-household wealth (no leak).
* Broad-household nominal debt (0.8 x income): deflation and income loss raise
  the debt-service ratio, defaults write debt down and cause a credit crunch on
  B2B and investment (Fisher debt-deflation). Monetary offset: helicopter
  transfers when deflation > 2%/yr, blocked (ZLB / politics) in some draws.
* Policy: continuous hazard re-evaluated every election cycle while jobs lost
  exceed the visibility threshold; rises with jobs lost, duration and B2C
  business-lobby pressure; cut by elite capture. Programmes are financed first
  by a tax on automation profits and AI fees, then by deficit up to a cap.
* Labour supply capped at the 2026 labour force (excess demand -> wages).

The 95% interval on the headline is a STRUCTURAL band across model variants
(consumption rule, policy design, leak, B2B channel, debt/monetary, D prior),
not Monte Carlo noise (MC noise is reported separately and is ~+-0.5pp).

Run:  python m2_no_customers_domino.py   (seed fixed; ~1-2 min)
"""
import json
import os
import time

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(ROOT, "results")
FIG = os.path.join(ROOT, "figures")
os.makedirs(RES, exist_ok=True)
os.makedirs(FIG, exist_ok=True)

SEED = 20260930
N = int(os.environ.get("M2_N", 20000))
N_VAR = int(os.environ.get("M2_NVAR", 8000))
T0 = 2026.75                 # 2026Q4
NQ = 137                     # through 2060Q4
DT = 0.25
YEARS = T0 + DT * np.arange(NQ)

PART_LEVEL = 0.30            # S2a jobs-lost threshold
COLLAPSE_LEVEL = 0.75        # S2b bottom-80 real consumption index threshold
RUN_Q = 8                    # consecutive quarters
B2B_CASCADE_LEVEL = 0.90

# ---------------------------------------------------------------------------
# Occupational categories (employment shares ~ BLS OES major groups, rounded;
# relative wages ~ OES mean / all-occupation mean; difficulty/ceiling judgment
# informed by Eloundou et al. 2023). top_sh = share of category wage bill going
# to top-20% households; v2 scales the judgment values so that the top-20% gets
# ~48% of the total wage bill (Census/CBO earnings distribution [M]).
# ---------------------------------------------------------------------------
CATS = [
    # name,                          emp,  wrel, top_sh, diff, cap, licensed
    ("office_admin",                 0.12, 0.80, 0.10, 0.15, 0.90, 0),
    ("sales_customer_service",       0.10, 0.80, 0.15, 0.25, 0.80, 0),
    ("business_finance_legal",       0.08, 1.60, 0.55, 0.20, 0.85, 1),
    ("software_it_eng_science",      0.06, 2.00, 0.60, 0.30, 0.85, 0),
    ("management",                   0.07, 2.20, 0.70, 0.50, 0.70, 0),
    ("media_arts_education",         0.07, 1.10, 0.30, 0.45, 0.70, 1),
    ("healthcare_professional",      0.07, 1.60, 0.50, 0.60, 0.60, 1),
    ("transport_logistics",          0.09, 0.85, 0.10, 0.55, 0.85, 0),
    ("production_construction",      0.14, 0.95, 0.15, 0.75, 0.75, 0),
    ("care_food_personal_services",  0.20, 0.60, 0.05, 0.85, 0.55, 0),
]
K = len(CATS)
EMP = np.array([c[1] for c in CATS]); EMP /= EMP.sum()
WREL = np.array([c[2] for c in CATS])
WW = EMP * WREL / (EMP * WREL).sum()          # wage-bill weights
_top_raw = np.array([c[3] for c in CATS])
TOPSH = np.clip(_top_raw * 0.48 / (WW * _top_raw).sum(), 0, 0.92)
DIFF = np.array([c[4] for c in CATS])
CAP0 = np.array([c[5] for c in CATS])
LIC = np.array([c[6] for c in CATS], dtype=bool)

BASE_OPT = dict(cons="prop", policy="hazard", cycle_q=8, leak="wealth", seat=True,
                debt=True, mon="draw", D_prior="mixture", labcap=True, tax_fin=True)


def tri(rng, lo, mode, hi, n):
    return rng.triangular(lo, mode, hi, n)


def lognorm_med(rng, med, sig, n, lo=None, hi=None):
    x = med * np.exp(sig * rng.standard_normal(n))
    if lo is not None or hi is not None:
        x = np.clip(x, lo, hi)
    return x


def draw_D(rng, n, prior):
    """Years from 2026 until the frontier can substitute the median professional
    task category. Mixture over forecaster families [v2]:
      fast   median 7  (Metaculus 'first general AI' community median Jan 2033,
                        mid-2026; weakly-general AI median 2028)
      medium median 20 (ESPAI 2023 HLMI 50% year 2047)
      slow   median 45 (ESPAI 2023 full automation of occupations much later,
                        50% ~2116; Karger et al. 2026 economists expect modest labour
                        effects even under rapid progress)
    Weights 0.45/0.35/0.20, tilted to fast because S1 (race under way) is given."""
    if prior == "aggressive":          # v1 prior
        return lognorm_med(rng, 7.0, 0.6, n, 1.5, 40.0)
    if prior == "slow":
        return lognorm_med(rng, 20.0, 0.7, n, 2.0, 90.0)
    comp = rng.choice(3, n, p=[0.45, 0.35, 0.20])
    med = np.array([7.0, 20.0, 45.0])[comp]
    sig = np.array([0.45, 0.5, 0.5])[comp]
    return np.clip(med * np.exp(sig * rng.standard_normal(n)), 1.5, 90.0)


def draw_params(rng, n, opt):
    """Priors. [R#] = row # in research/m2_no_customers_domino.md; [J] = judgment."""
    p = {}
    p["D"] = draw_D(rng, n, opt["D_prior"])
    p["cat_noise"] = np.exp(0.3 * rng.standard_normal((n, K)))
    p["T1090"] = lognorm_med(rng, 8.0, 0.45, n, 2.5, 30.0)       # Comin & Hobijn 2010 [J]
    p["reg_regime"] = rng.random(n) < 0.30                        # licensing slowdown [J]
    p["benev"] = rng.uniform(0.05, 0.30, n)                       # S1 laggards [J]
    p["chi"] = rng.uniform(0.0, 2.0, n)                           # Hershbein & Kahn 2018 [J]
    p["psi"] = rng.uniform(0.0, 0.6, n)                           # revenue-funded R&D [J]
    p["cap_mult"] = rng.uniform(0.8, 1.1, n)
    # --- wages, prices, costs ---
    p["omega"] = rng.uniform(0.0, 0.4, n)                         # Korinek & Suh 2024 [J]
    p["pi"] = rng.uniform(0.3, 0.8, n)                            # pass-through [J]
    p["c_ai"] = lognorm_med(rng, 0.20, 0.5, n, 0.05, 0.8)         # AI cost / wage [J]
    p["Lc"] = rng.uniform(0.53, 0.58, n)                          # labour share [R research s1]
    # --- households (v2 disposable-income calibration) ---
    # Top-20 consumption share: BLS CE 0.35 .. Dallas Fed 0.57 [R4]. Draws above
    # ~0.5 are only NIPA-consistent via top consumption out of wealth (below).
    p["s_top"] = tri(rng, 0.35, 0.45, 0.60, n)
    p["apc_b"] = rng.uniform(0.92, 1.02, n)        # bottom-80 saving ~0 (Dynan, Skinner & Zeldes 2004) [M]
    p["apc_t"] = rng.uniform(0.55, 0.75, n)        # top-20 saving 25-45% of disposable income [M]
    p["tax_t"] = rng.uniform(0.22, 0.32, n)        # avg tax rate top quintile (CBO) [M]
    p["e_b"] = rng.uniform(0.8, 1.0, n)            # permanent-income elasticity (PIH ~1) [J]
    p["e_t"] = rng.uniform(0.5, 0.9, n)            # top: smoother consumption [J]
    p["mw"] = rng.uniform(0.03, 0.05, n)           # MPC out of wealth /yr (Case, Quigley & Shiller) [M]
    p["k_down"] = rng.uniform(0.15, 0.40, n)       # loss-averse downward adjustment /q [J]
    p["k_up_top"] = rng.uniform(0.10, 0.30, n)
    p["theta_prem"] = rng.uniform(0.30, 0.60, n)
    p["h_prem"] = rng.uniform(0.20, 0.50, n)       # human-premium share [J][R24]
    p["cap_to_broad"] = rng.uniform(0.12, 0.25, n) # SCF [M]
    # --- debt / finance (v2) ---
    p["debt_ratio"] = rng.uniform(0.7, 0.9, n)     # hh debt / disposable income, bottom-80 [M] (Fed Z.1 ~0.9-1.0 all hh)
    p["dsr0"] = rng.uniform(0.09, 0.12, n)         # debt service ratio (Fed DSR ~9.8-11%) [M]
    p["dsr_crit"] = rng.uniform(0.15, 0.25, n)     # distress threshold [J]
    p["kdef"] = rng.uniform(0.01, 0.04, n)         # max quarterly write-off rate in distress [J]
    p["gcc"] = rng.uniform(0.5, 2.0, n)            # credit-crunch elasticity to losses [J]
    p["mon_k"] = rng.uniform(0.5, 2.0, n)          # helicopter size per pp excess deflation [J]
    p["mon_blocked"] = rng.random(n) < rng.uniform(0.3, 0.7, n)   # ZLB/political blockage [J]
    # --- supply network ---
    p["b2b_hh_share"] = tri(rng, 0.55, 0.65, 0.72, n)             # [R7]
    p["amp"] = np.clip(lognorm_med(rng, 3.0, 0.4, n), 1.5, 6.0)    # [R8]
    p["lag_q"] = np.clip(lognorm_med(rng, 2.0, 0.6, n), 0.5, 6.0)  # [R9]
    p["s_seat"] = rng.uniform(0.10, 0.30, n)       # per-seat/per-employee share of B2B_hh [J]
    p["inv_accel"] = rng.uniform(1.0, 2.0, n)
    p["phi"] = rng.uniform(0.3, 0.7, n)            # payout of extra profits [J]
    p["nu"] = rng.uniform(0.2, 0.8, n)             # retained profits invested [J]
    p["capex_ai"] = rng.uniform(0.3, 0.7, n)
    # --- stabilisers and policy ---
    p["stab_short"] = tri(rng, 0.25, 0.34, 0.47, n)  # [R10]
    p["stab_long"] = rng.uniform(0.08, 0.20, n)
    p["theta"] = rng.uniform(0.05, 0.12, n)          # visibility threshold [J]
    p["p_sudden"] = tri(rng, 0.60, 0.85, 0.95, n)    # [R11]
    p["p_gradual"] = tri(rng, 0.15, 0.35, 0.60, n)   # [R12]
    p["g_cycle"] = rng.uniform(0.3, 0.7, n)          # per-cycle hazard as share of p_gradual at U=theta [J]
    p["eta"] = rng.uniform(0.5, 1.5, n)              # escalation per theta multiple [J]
    p["lobby"] = rng.uniform(0.0, 1.0, n)            # B2C/B2B business pressure weight [J]
    p["lag_pol_q"] = np.round(4 * np.clip(lognorm_med(rng, 1.5, 0.8, n), 0.1, 5.0)).astype(int)  # [R13]
    p["kappa"] = rng.uniform(0.1, 0.8, n)            # elite capture [J]
    p["rho0"] = rng.uniform(0.4, 1.0, n)
    p["ingroup"] = rng.uniform(0.0, 0.3, n)
    p["cap_gdp"] = rng.uniform(0.08, 0.25, n)        # [R23]
    p["tau_ai"] = rng.uniform(0.15, 0.40, n)         # max tax take on automation rents [J]
    p["impl_q"] = rng.integers(1, 5, n)
    p["ubi_offset"] = tri(rng, 0.0, 0.25, 0.35, n)   # [R21]
    # --- new work (r0 is now a JOBS share per year, not a task-content rate) ---
    # Autor et al. 2024: ~60% of 2018 jobs in post-1940 titles -> ~0.8%/yr gross;
    # net of obsolescence lower. [J]
    p["r0"] = tri(rng, 0.002, 0.004, 0.007, n)
    p["zeta"] = lognorm_med(rng, 1.0, 0.7, n)
    p["absorb"] = rng.uniform(0.02, 0.15, n)
    p["maxshift"] = tri(rng, 0.005, 0.008, 0.015, n)  # [R16]
    p["gen"] = rng.uniform(0.0, 1.0, n)
    p["w_new"] = rng.uniform(0.6, 1.0, n)
    return p


def simulate(p, n, opt, rng_pol):
    C0, G0, I0 = 0.66, 0.17, 0.17
    Lc = p["Lc"]; K0 = 0.22; T0_ = 0.15
    s_top = p["s_top"]
    Cb0 = (1 - s_top) * C0; Ct0 = s_top * C0
    tp = p["theta_prem"]
    Cmass0 = Cb0 + (1 - tp) * Ct0; Cprem0 = tp * Ct0
    u_GI = 0.35; s = p["b2b_hh_share"]
    u_C = s * u_GI * (G0 + I0) / (C0 * (1 - s))
    VA_mass = Cmass0 * (1 - u_C); VA_prem = Cprem0 * (1 - u_C); VA_b2b = C0 * u_C
    VA_G = np.full(n, G0); VA_I = np.full(n, I0)
    Wtop_frac = (WW * TOPSH).sum()
    Wb0 = Lc * (1 - Wtop_frac); Wt0 = Lc * Wtop_frac
    cb = p["cap_to_broad"]
    Tb0 = 0.85 * T0_; Tt0 = 0.15 * T0_
    # ---- disposable-income calibration ----
    tax_b = np.clip(1 - (Cb0 / p["apc_b"] - Tb0) / (Wb0 + cb * K0), 0.08, 0.35)
    Yb0 = (1 - tax_b) * (Wb0 + cb * K0) + Tb0
    apc_b = Cb0 / Yb0
    tax_t = p["tax_t"]
    Yt0 = (1 - tax_t) * (Wt0 + (1 - cb) * K0) + Tt0
    apc_t = np.minimum(p["apc_t"], Ct0 / Yt0)
    WC0 = Ct0 - apc_t * Yt0                         # top consumption out of wealth
    Wlth0 = WC0 / p["mw"]
    # debt
    Debt0 = p["debt_ratio"] * Yb0
    S0 = p["dsr0"] * Yb0
    Debt = Debt0.copy()

    T_k = p["D"][:, None] * (0.2 + 2.3 * DIFF[None, :] ** 1.3) * p["cat_noise"]
    cap = np.clip(CAP0[None, :] * p["cap_mult"][:, None], 0.0, 0.97)
    lam = np.log(81.0) / p["T1090"]
    lam_k = np.repeat(lam[:, None], K, axis=1)
    lam_k = np.where(p["reg_regime"][:, None] & LIC[None, :], lam_k * 0.4, lam_k)
    f = np.zeros((n, K)); f_cf = np.zeros((n, K))
    tau = np.zeros(n); tau_cf = 0.0
    Cb = Cb0.copy(); Ct = Ct0.copy()
    N_new = np.zeros(n)
    policy_on = np.zeros(n, bool); policy_year = np.full(n, np.nan)
    policy_start_q = np.full(n, 10 ** 6)
    last_eval = np.full(n, -10 ** 6); first_done = np.zeros(n, bool)
    q_above = np.zeros(n)
    chance_used = np.zeros((n, 3), bool)
    hist_Qc = np.ones((n, 12)); U_hist = np.zeros((n, 5)); LBW_hist = np.zeros((n, 5))
    P_hist = np.ones((n, 5)); loss_hist = np.zeros((n, 4))
    pressure = np.zeros(n); m_cap = np.ones(n)
    R_acc = np.zeros(n)
    I_nom = np.full(n, I0)
    idx = np.arange(n)
    L = np.maximum(1, np.round(p["lag_q"]).astype(int))
    cf_credit = np.ones(n)

    keys = ["BR", "GDPr", "Qmass", "B2B", "U", "direct", "dem", "dem_nom", "A", "A_cf", "aishare",
            "Qprem", "Ireal", "trdep", "dsr", "Pm", "Yb_rel", "Wb_rel", "mon", "capb", "pol", "stabT", "Cb_nom"]
    out = {k: np.zeros((n, NQ), np.float32) for k in keys}
    for q in range(NQ):
        tau += DT * m_cap; tau_cf += DT
        for ff, tt, press in ((f, tau, pressure), (f_cf, np.full(n, tau_cf), 0.0)):
            capable = tt[:, None] >= T_k
            seed = capable & (ff < 0.02 * cap)
            ff[seed] = 0.02 * cap[seed]
            fbar = (ff * EMP).sum(1)
            mult = (1 - p["benev"] * np.exp(-fbar / 0.3)) * (1 + p["chi"] * press)
            growth = lam_k * mult[:, None] * ff * (1 - ff / np.maximum(cap, 1e-9))
            ff += DT * np.where(capable, growth, 0.0)
            np.clip(ff, 0, cap, out=ff)
        a_emp = (f * EMP).sum(1); a_wage = (f * WW).sum(1)
        auto_prem = 1 - p["h_prem"]
        P_mass = 1 - p["pi"] * Lc * a_wage * (1 - p["c_ai"])
        P_prem = 1 - p["pi"] * Lc * a_wage * auto_prem * (1 - p["c_ai"])
        Q_mass = (Cb + (1 - tp) * Ct) / P_mass / Cmass0
        Q_prem = (tp * Ct) / P_prem / Cprem0
        Qc = (Cmass0 * Q_mass + Cprem0 * Q_prem) / (Cmass0 + Cprem0)
        hist_Qc = np.roll(hist_Qc, 1, axis=1); hist_Qc[:, 0] = Qc
        QL = hist_Qc[idx, np.minimum(L, 11)]; QL2 = hist_Qc[idx, np.minimum(L + 2, 11)]
        amp_eff = 1 + (p["amp"] - 1) * 0.5
        X = np.maximum(0.0, QL + (amp_eff - 1) * (QL - QL2))
        seat_cut = p["s_seat"] * a_emp if opt["seat"] else np.zeros(n)
        X = X * (1 - seat_cut) * cf_credit
        Ireal = I_nom / I0
        # ---- employment ----
        esec = np.stack([VA_mass * Q_mass, VA_prem * Q_prem, VA_b2b * X, VA_G, VA_I * Ireal], 1)
        autofac = np.stack([np.ones(n), auto_prem, np.ones(n), np.ones(n), np.ones(n)], 1)
        S_ = esec.sum(1); S_auto = (esec * autofac).sum(1)
        emp_k = EMP[None, :] * (S_[:, None] - f * S_auto[:, None])
        emp_new = N_new * (0.5 * Q_mass + 0.5 * Q_prem)
        Emp_d = emp_k.sum(1) + emp_new
        ratio = np.maximum(1.0, Emp_d) if opt["labcap"] else np.ones(n)
        Emp = Emp_d / ratio          # labour cap; wage bill unchanged (excess demand -> wages)
        U = np.clip(1 - Emp, -0.5, 1.0)
        direct = a_emp * (1.0 - VA_prem * p["h_prem"])
        wage_k = (emp_k * WREL[None, :] * (1 - p["omega"][:, None] * f)) / (EMP * WREL).sum() * Lc[:, None]
        W_b = (wage_k * (1 - TOPSH[None, :])).sum(1) + emp_new * p["w_new"] * Lc * 0.9
        W_t = (wage_k * TOPSH[None, :]).sum(1) + emp_new * p["w_new"] * Lc * 0.1
        # ---- automation rents ----
        AL = Lc * a_wage * S_auto
        fees = p["c_ai"] * AL
        seat_save = VA_b2b * X / np.maximum(1 - seat_cut, 1e-6) * seat_cut / np.maximum(cf_credit, 1e-6)
        xprof = (1 - p["pi"]) * (1 - p["c_ai"]) * AL + seat_save
        nom_out = (VA_mass * Q_mass * P_mass + VA_prem * Q_prem * P_prem + VA_b2b * X * P_mass
                   + VA_G + VA_I * Ireal)
        GDPn = Cb + Ct + G0 + I_nom
        # ---- transfers ----
        LBW = np.maximum(0.0, Wb0 - W_b)
        LBW_hist = np.roll(LBW_hist, 1, 1); LBW_hist[:, 0] = LBW
        recent = np.clip((LBW - LBW_hist[:, 4]) / np.maximum(LBW, 1e-9), 0, 1)
        # Dolls et al. 34% = taxes + transfers; the tax part is already in (1 - tax_b), so
        # only the transfer excess over the tax rate is added (floor = long-run transfers)
        stab = p["stab_long"] + np.maximum(0.0, p["stab_short"] - tax_b - p["stab_long"]) * recent
        active = policy_on & (q >= policy_start_q)
        rho = p["rho0"] * (1 - p["ingroup"])
        pol = np.where(active, np.minimum(rho * (1 - tax_b) * LBW, p["cap_gdp"] * GDPn), 0.0)
        pol = np.minimum(pol, np.maximum(0.0, (1 - tax_b - stab) * LBW + 0.02))
        # financing: tax on automation rents first (rate cut by elite capture)
        if opt["tax_fin"]:
            capac = p["tau_ai"] * (1 - 0.5 * p["kappa"]) * (xprof + fees)
            taxed = np.minimum(pol, capac)
            sh = xprof / np.maximum(xprof + fees, 1e-9)
            xprof = xprof - taxed * sh; fees = fees - taxed * (1 - sh)
        # monetary offset
        P_hist = np.roll(P_hist, 1, 1); P_hist[:, 0] = P_mass
        defl = 1 - P_mass / P_hist[:, 4]
        if opt["mon"] == "off":
            mon_ok = np.zeros(n, bool)
        elif opt["mon"] == "on":
            mon_ok = np.ones(n, bool)
        else:
            mon_ok = ~p["mon_blocked"]
        mon = np.where(mon_ok, np.minimum(0.05 * GDPn, p["mon_k"] * np.maximum(0, defl - 0.02) * GDPn), 0.0)
        Kinc = K0 * nom_out + p["phi"] * xprof + (1 - p["capex_ai"]) * fees
        resid = (1 - p["phi"]) * (1 - p["nu"]) * xprof
        if opt["leak"] == "wealth":
            R_acc = R_acc + DT * resid
        Wlth = Wlth0 * (Kinc / K0) + R_acc
        Yb = (1 - tax_b) * (W_b + cb * Kinc) + Tb0 + stab * LBW + pol + mon
        Yt = (1 - tax_t) * (W_t + (1 - cb) * Kinc) + Tt0
        trdep = (Tb0 + stab * LBW + pol + mon) / np.maximum(Yb, 1e-9)
        # ---- debt service, defaults, credit ----
        if opt["debt"]:
            Sd = S0 * Debt / Debt0
            dsr = Sd / np.maximum(Yb, 1e-6)
            distress = 1 / (1 + np.exp(-(dsr - p["dsr_crit"]) / 0.02))
            wo = p["kdef"] * distress * Debt
            Debt = Debt - wo
            loss_hist = np.roll(loss_hist, 1, 1); loss_hist[:, 0] = wo / Debt0
            cf_credit = 1 - np.minimum(0.5, p["gcc"] * loss_hist.sum(1))
        else:
            Sd = S0.copy(); dsr = Sd / np.maximum(Yb, 1e-6)
        # ---- policy ----
        U_hist = np.roll(U_hist, 1, 1); U_hist[:, 0] = U
        speed = U - U_hist[:, 4]
        w_s = 1 / (1 + np.exp(-(speed - 0.04) / 0.01))
        aishare = (fees + xprof) / np.maximum(GDPn, 1e-6)
        capture = np.clip(1 - p["kappa"] * aishare / 0.15, 0.05, 1.0)
        above = U > p["theta"]
        q_above = q_above + above
        enact = np.zeros(n, bool)
        if opt["policy"] == "hazard":
            first = (~policy_on) & above & (~first_done)
            p1 = (w_s * p["p_sudden"] + (1 - w_s) * p["p_gradual"]) * capture
            enact |= first & (rng_pol.random(n) < p1)
            first_done |= first
            last_eval = np.where(first, q, last_eval)
            again = (~policy_on) & above & (~first) & (q - last_eval >= opt["cycle_q"])
            mlt = U / p["theta"]
            short = np.maximum(0.0, 1 - Q_mass)
            dur = np.minimum(2.0, 1 + 0.1 * q_above * DT)
            pc = (p["g_cycle"] * p["p_gradual"] * (1 + p["eta"] * 0.5 * (mlt - 1)) * dur
                  + p["lobby"] * short)
            pc = np.minimum(pc, p["p_sudden"]) * capture
            enact |= again & (rng_pol.random(n) < pc)
            last_eval = np.where(again, q, last_eval)
        else:   # v1 one-shot gated chances (with the eta bug fixed), kept as a variant
            for j, m in enumerate((1.0, 2.0, 3.0)):
                fire = (~policy_on) & (~chance_used[:, j]) & (U > m * p["theta"])
                if j == 0:
                    pc = (w_s * p["p_sudden"] + (1 - w_s) * p["p_gradual"]) * capture
                else:
                    pc = (1 - (1 - p["p_gradual"]) ** (1 + p["eta"])) * capture
                enact |= fire & (rng_pol.random(n) < pc)
                chance_used[:, j] |= fire
        policy_on |= enact
        policy_start_q = np.where(enact, q + p["lag_pol_q"] + p["impl_q"], policy_start_q)
        policy_year = np.where(enact, YEARS[q], policy_year)
        # domino diagnostic (real and nominal)
        dem_loss = (VA_mass * np.maximum(0, 1 - Q_mass) * (1 - a_emp)
                    + VA_prem * np.maximum(0, 1 - Q_prem) * (1 - a_emp * auto_prem)
                    + VA_b2b * np.maximum(0, 1 - X) * (1 - a_emp))
        dem_nom = (VA_mass * np.maximum(0, 1 - Q_mass * P_mass) * (1 - a_emp)
                   + VA_prem * np.maximum(0, 1 - Q_prem * P_prem) * (1 - a_emp * auto_prem)
                   + VA_b2b * np.maximum(0, 1 - X * P_mass) * (1 - a_emp))
        # ---- consumption update ----
        if opt["cons"] == "prop":
            Yav = np.maximum(0.05 * Yb0, Yb - Sd); Yav0 = Yb0 - S0
            Cb_star = np.maximum(0.25 * Cb0, Cb0 * (Yav / Yav0) ** p["e_b"])
        else:   # additive MPC = APC x U(0.9,1.2) (reviewer's variant)
            mb = apc_b * (0.9 + 1.5 * (p["e_b"] - 0.8))
            Cb_star = np.maximum(0.25 * Cb0, Cb0 + mb * ((Yb - Sd) - (Yb0 - S0)))
        Ct_star = (apc_t * Yt0 * np.maximum(Yt / Yt0, 0.05) ** p["e_t"] + p["mw"] * Wlth)
        Ct_star = np.maximum(0.25 * Ct0, Ct_star)
        kb = np.where(Cb_star < Cb, p["k_down"], 0.5)
        Cb = Cb + kb * (Cb_star - Cb)
        Ct = Ct + p["k_up_top"] * (Ct_star - Ct)
        Cn = Cb + Ct
        I_nom = (I0 * np.clip(Cn / C0, 0.05, 3) ** p["inv_accel"] + p["nu"] * (1 - p["phi"]) * xprof
                 + p["capex_ai"] * fees) * cf_credit
        # ---- new work ----
        Upos = np.maximum(U, 0)
        create = np.minimum(p["r0"] * (1 + p["zeta"] * a_emp) + p["absorb"] * Upos, p["maxshift"])
        create *= (1 - p["ubi_offset"] * np.clip(pol / np.maximum(Yb0, 1e-9), 0, 1))
        N_new = N_new + DT * (create - p["gen"] * a_emp * 0.15 * N_new)
        pressure = np.maximum(0.0, 1 - Qc)
        m_cap = np.clip(GDPn, 0.2, 2.0) ** p["psi"]
        BR = (Cb / P_mass) / Cb0
        GDPr = (Cn / P_mass + G0 + I_nom) / (C0 + G0 + I0)
        for k_, v_ in (("BR", BR), ("GDPr", GDPr), ("Qmass", Q_mass), ("B2B", X), ("U", U),
                       ("direct", direct), ("dem", dem_loss), ("dem_nom", dem_nom), ("A", a_emp),
                       ("A_cf", (f_cf * EMP).sum(1)), ("aishare", aishare), ("Qprem", Q_prem),
                       ("Ireal", Ireal), ("trdep", trdep), ("dsr", dsr), ("Pm", P_mass),
                       ("Yb_rel", Yb / Yb0), ("Wb_rel", W_b / Wb0), ("mon", mon), ("capb", (1 - tax_b) * cb * Kinc),
                       ("pol", pol), ("stabT", stab * LBW), ("Cb_nom", Cb / Cb0)):
            out[k_][:, q] = v_
    out["policy_on"] = policy_on; out["policy_year"] = policy_year
    out["apc_b"] = apc_b; out["apc_t_income"] = Ct0 / Yt0; out["tax_b"] = tax_b
    return out


def first_sustained(mask, run):
    n, T = mask.shape
    c = np.zeros(n, int); start = np.full(n, -1)
    for q in range(T):
        c = np.where(mask[:, q], c + 1, 0)
        hit = (c >= run) & (start < 0)
        start = np.where(hit, q - run + 1, start)
    return start


def first_cross(x, lvl, above=False):
    m = x > lvl if above else x < lvl
    return np.where(m.any(1), m.argmax(1), -1)


def outcomes(o, n, part_level=PART_LEVEL, level=COLLAPSE_LEVEL, run=RUN_Q, b2b=B2B_CASCADE_LEVEL):
    idx = np.arange(n)
    sa = first_sustained(o["U"] > part_level, run)
    s2a = sa >= 0
    sb = first_sustained(o["BR"] < level, run)
    raw = sb >= 0
    sj = np.maximum(sb, 0)
    wb = np.stack([o["B2B"][idx, np.minimum(sj + j, NQ - 1)] for j in range(run)], 1).min(1)
    s2b = raw & (wb <= b2b)
    return s2a, sa, s2b, sb, raw, wb


def s2b_nominal(o, n, level=COLLAPSE_LEVEL, run=RUN_Q, b2b=B2B_CASCADE_LEVEL):
    """Firms' view: bottom-80 NOMINAL spending <= level and nominal household-serving B2B
    revenue <= b2b (deflation counts as lost revenue)."""
    idx = np.arange(n)
    sb = first_sustained(o["Cb_nom"] < level, run)
    sj = np.maximum(sb, 0)
    bn = o["B2B"] * o["Pm"]
    wb = np.stack([bn[idx, np.minimum(sj + j, NQ - 1)] for j in range(run)], 1).min(1)
    return (sb >= 0) & (wb <= b2b)


def run_model(opt, n, seed=SEED):
    rng = np.random.default_rng(seed)
    p = draw_params(rng, n, opt)
    if opt.get("provider_capture"):   # S3 premise: providers capture margins, little pass-through
        p["pi"] = rng.uniform(0.05, 0.30, n)
        p["c_ai"] = np.clip(p["c_ai"] * 2.5, 0.1, 0.9)
    if opt.get("harsh_hh"):           # bottom-80 get little capital income, weak stabilisers, full pass of wage loss
        p["cap_to_broad"] = rng.uniform(0.03, 0.08, n)
        p["stab_long"] = rng.uniform(0.03, 0.08, n)
        p["e_b"] = np.ones(n)
        p["omega"] = rng.uniform(0.3, 0.6, n)
    o = simulate(p, n, opt, np.random.default_rng(seed + 1))
    return p, o


def boot_ci(x, B=2000, rng=None):
    rng = rng or np.random.default_rng(1)
    n = len(x)
    means = np.array([x[rng.integers(0, n, n)].mean() for _ in range(B)])
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def yi(y):
    return int(round((y - T0) / DT))


def pct(x, qs=(10, 50, 90)):
    return {f"p{q}": float(np.percentile(x, q)) for q in qs} if len(x) else None


VARIANTS = {
    "base": {},
    "cycle_16q_elections": {"cycle_q": 16},
    "policy_oneshot_v1_etafixed": {"policy": "oneshot"},
    "cons_additive_mpc_eq_apc": {"cons": "additive"},
    "leak_savings_glut": {"leak": "glut"},
    "no_seat_channel": {"seat": False},
    "no_debt_channel": {"debt": False},
    "monetary_always_blocked": {"mon": "off"},
    "monetary_always_available": {"mon": "on"},
    "transfers_costless": {"tax_fin": False},
    "no_labour_cap": {"labcap": False},
    "S3_provider_margin_capture": {"provider_capture": True},
    "S3_capture_and_aggressive_D": {"provider_capture": True, "D_prior": "aggressive"},
    "harsh_all_pessimistic_combined": {"provider_capture": True, "D_prior": "aggressive", "harsh_hh": True,
                                       "policy": "oneshot", "leak": "glut", "mon": "off"},
    "D_prior_aggressive_v1": {"D_prior": "aggressive"},
    "D_prior_slow": {"D_prior": "slow"},
}


def main():
    t_start = time.time()
    opt = dict(BASE_OPT)
    p, o = run_model(opt, N)
    n = N; idx = np.arange(n)
    U = o["U"]; BR = o["BR"]
    s2a, sa, s2b, sb, raw, wb = outcomes(o, n)
    s2a_year = np.where(s2a, YEARS[np.maximum(sa, 0)], np.nan)
    s2b_year = np.where(s2b, YEARS[np.maximum(sb, 0)], np.nan)
    both = s2a & s2b
    pa, pb = float(s2a.mean()), float(s2b.mean())
    mc_a, mc_b = boot_ci(s2a.astype(float)), boot_ci(s2b.astype(float))

    def tl(yrs, ind):
        y = yrs[ind]
        d = {"p10_year": float(np.percentile(y, 10)), "median_year": float(np.percentile(y, 50)),
             "p90_year": float(np.percentile(y, 90))} if ind.any() else {}
        for Y in (2030, 2035, 2040, 2050, 2060):
            d[f"p_by_{Y}"] = float((yrs <= Y + 0.99).mean())
        return d

    # ---- structural variants ----
    var = {}
    for name, ch in VARIANTS.items():
        vo = dict(BASE_OPT); vo.update(ch)
        _, ov = run_model(vo, N_VAR, seed=SEED + 7)
        a, _, b, _, _, _ = outcomes(ov, N_VAR)
        var[name] = {"S2a": float(a.mean()), "S2b": float(b.mean()),
                     "S2b_nominal": float(s2b_nominal(ov, N_VAR).mean()),
                     "median_U2050": float(np.median(ov["U"][:, yi(2050)])),
                     "p_programme": float(ov["policy_on"].mean())}
        print(f"  variant {name:32s} S2a={a.mean():.3f} S2b={b.mean():.3f} "
              f"U2050={np.median(ov['U'][:, yi(2050)]):.3f} prog={ov['policy_on'].mean():.3f}")
    nonD = [k for k in var if not k.startswith("D_prior")]
    band = {}
    for key in ("S2a", "S2b"):
        vals_all = np.array([var[k][key] for k in var])
        vals_nd = np.array([var[k][key] for k in nonD])
        band[key] = {"min_all_variants": float(vals_all.min()), "max_all_variants": float(vals_all.max()),
                     "min_mechanism_variants": float(vals_nd.min()), "max_mechanism_variants": float(vals_nd.max()),
                     "equal_weight_average_all": float(vals_all.mean())}

    # ---- sensitivity curves ----
    part_curve = {str(lv): float(outcomes(o, n, part_level=lv)[0].mean()) for lv in (0.15, 0.2, 0.25, 0.3, 0.4, 0.5)}
    b2b_curve = {str(bl): float(outcomes(o, n, b2b=bl)[2].mean()) for bl in (1.0, 0.95, 0.9, 0.85, 0.8)}
    level_curve = {str(lv): float(outcomes(o, n, level=lv)[2].mean()) for lv in (0.85, 0.8, 0.75, 0.7, 0.65)}

    # ---- D terciles ----
    t1, t2 = np.percentile(p["D"], [33.3, 66.7])
    Dter = {}
    for lab, m in (("fast_D<=%.1f" % t1, p["D"] <= t1), ("mid", (p["D"] > t1) & (p["D"] < t2)),
                   ("slow_D>=%.1f" % t2, p["D"] >= t2)):
        Dter[lab] = {"S2a": float(s2a[m].mean()), "S2b": float(s2b[m].mean()),
                     "median_U2050": float(np.median(U[m, yi(2050)]))}

    # ---- validation vs expert forecasts ----
    valid = {y: {"median_jobs_lost": float(np.median(U[:, yi(y)])),
                 "p10": float(np.percentile(U[:, yi(y)], 10)), "p90": float(np.percentile(U[:, yi(y)], 90)),
                 "mean_automation_share": float(o["A"][:, yi(y)].mean())} for y in (2030, 2040, 2050)}
    valid["share_draws_U2050_below_0.06_(Karger_rapid_~10M_jobs)"] = float((U[:, yi(2050)] < 0.06).mean())

    # ---- policy and conditional stats ----
    pol = o["policy_on"]; py = o["policy_year"]
    m3 = U > 3 * p["theta"][:, None]
    has3 = m3.any(1); q3 = np.where(has3, m3.argmax(1), -1)
    ref_year = np.where(has3, YEARS[np.maximum(q3, 0)], np.nan)
    grpA = has3 & pol & (py <= ref_year)
    grpB = has3 & ~(pol & (py <= ref_year))
    cond = {"definition": "among draws whose jobs-lost share exceeds 3x theta; group A = programme decided "
                          "before U first crossed 3x theta, B = not decided by then (still confounded by speed)",
            "n_A": int(grpA.sum()), "n_B": int(grpB.sum()),
            "P_S2b_A": float(s2b[grpA].mean()) if grpA.any() else None,
            "P_S2b_B": float(s2b[grpB].mean()) if grpB.any() else None,
            "P_S2a_A": float(s2a[grpA].mean()) if grpA.any() else None,
            "P_S2a_B": float(s2a[grpB].mean()) if grpB.any() else None}
    mon_ok = ~p["mon_blocked"]
    rec = s2b & (BR[:, -1] >= 0.9)

    # ---- domino multiplier over the path at 15% B2C drop ----
    q15 = first_cross(o["Qmass"], 0.85)
    h15 = q15 >= 0; j15 = np.maximum(q15, 0)
    D15 = o["direct"][idx, j15]; M15 = o["dem"][idx, j15]; Mn15 = o["dem_nom"][idx, j15]
    qb2b = first_cross(o["B2B"], 0.85)
    bothc = h15 & (qb2b >= 0)
    lagq = (qb2b - q15)[bothc]

    # ---- automation feedback ----
    auto = {}
    for y in (2030, 2035, 2040, 2050, 2060):
        r = o["A"][:, yi(y)] / np.maximum(o["A_cf"][:, yi(y)], 1e-6)
        v = o["A_cf"][:, yi(y)] > 0.01
        auto[str(y)] = {"mean_ratio": float(r[v].mean()) if v.any() else None,
                        "mean_ratio_given_S2b": float(r[v & s2b].mean()) if (v & s2b).any() else None,
                        "p_accelerated_gt2pct": float((r[v] > 1.02).mean()) if v.any() else None,
                        "p_slowed_gt2pct": float((r[v] < 0.98).mean()) if v.any() else None}

    # ---- drivers (tercile deltas) for both outcomes ----
    def drivers(ind):
        ds = []
        for k, v in p.items():
            v = np.asarray(v)
            if v.ndim != 1:
                continue
            v = v.astype(float)
            if np.unique(v).size < 3:
                hi, lo = ind[v > 0.5].mean(), ind[v <= 0.5].mean()
            else:
                a1, a2 = np.percentile(v, [33.3, 66.7]); hi, lo = ind[v >= a2].mean(), ind[v <= a1].mean()
            ds.append({"param": k, "p_lo": float(lo), "p_hi": float(hi), "delta": float(hi - lo)})
        return sorted(ds, key=lambda d: -abs(d["delta"]))[:10]

    trdep_on = o["trdep"][idx, np.maximum(sa, 0)]
    U_peak = U.max(1); minBR = BR.min(1)
    th = np.arange(0, n, 4)
    res = {
        "stage": "S2_no_customers_domino", "version": 2, "generated": "2026-09-30",
        "seed": SEED, "n_runs": n, "n_runs_per_variant": N_VAR,
        "stage_probability": {
            "mean": pa, "ci_low": band["S2a"]["min_all_variants"], "ci_high": band["S2a"]["max_all_variants"],
            "ci_type": "structural band: min/max of P across model variants (not Monte Carlo)",
            "definition": ("S2a, participation collapse: P(jobs-lost share vs 2026 employment >= 0.30 for >= 8 "
                           "consecutive quarters before end-2060 | S1). This is the scenario's S2 ('end of broad "
                           "economic participation') and the input for S4/S5. It does not require demand collapse: "
                           "transfers can keep consumption up while participation ends."),
        },
        "S2b_consumption_cascade": {
            "mean": pb, "ci_low": band["S2b"]["min_all_variants"], "ci_high": band["S2b"]["max_all_variants"],
            "definition": ("bottom-80 real consumption <= 0.75 of 2026 for >= 8 consecutive quarters AND "
                           "household-serving B2B real output <= 0.90 within that window (the 'no customers' "
                           "domino proper)."),
            "timeline": tl(s2b_year, s2b)},
        "S2b_nominal_variant": {"mean": float(s2b_nominal(o, n).mean()),
                                "definition": "as S2b but in nominal terms (bottom-80 nominal spending <= 0.75, "
                                              "nominal B2B_hh revenue <= 0.90): firms' revenue view, deflation counts"},
        "bottom80_real_consumption_min_below": {str(l): float((BR.min(1) < l).mean()) for l in (0.95, 0.9, 0.85, 0.8)},
        "P_S2a_and_S2b": float(both.mean()),
        "P_S2b_given_S2a": float(s2b[s2a].mean()) if s2a.any() else None,
        "P_S2a_given_S2b": float(s2a[s2b].mean()) if s2b.any() else None,
        "timeline": {**tl(s2a_year, s2a), "definition": "calendar year of S2a onset, conditional on S2a by 2060"},
        "monte_carlo_ci_95": {"S2a": mc_a, "S2b": mc_b},
        "structural_band": band, "variants": var,
        "sensitivity_S2a_jobs_lost_threshold": part_curve,
        "sensitivity_S2b_B2B_threshold": b2b_curve,
        "sensitivity_S2b_consumption_level": level_curve,
        "by_D_tercile": Dter,
        "validation_jobs_lost": valid,
        "transfer_dependence_bottom80_at_S2a_onset": pct(trdep_on[s2a]),
        "transfer_dependence_bottom80_2050_given_S2a": pct(o["trdep"][s2a, yi(2050)]),
        "calibration_check": {"apc_bottom80": pct(o["apc_b"]), "top20_C_over_disposable_income": pct(o["apc_t_income"]),
                              "tax_rate_bottom80": pct(o["tax_b"])},
        "policy": {"p_programme_enacted_by_2060": float(pol.mean()),
                   "median_enact_year": float(np.nanmedian(py)) if pol.any() else None,
                   "p_programme_given_S2a": float(pol[s2a].mean()) if s2a.any() else None,
                   "conditional_comparison": cond},
        "monetary": {"P_S2b_monetary_available": float(s2b[mon_ok].mean()),
                     "P_S2b_monetary_blocked": float(s2b[~mon_ok].mean()),
                     "P_S2a_monetary_available": float(s2a[mon_ok].mean()),
                     "P_S2a_monetary_blocked": float(s2a[~mon_ok].mean())},
        "debt": {"peak_dsr_median": float(np.median(o["dsr"].max(1))),
                 "peak_dsr_median_given_S2b": float(np.median(o["dsr"][s2b].max(1))) if s2b.any() else None},
        "recovery_by_2060_given_S2b": float(rec.sum() / max(s2b.sum(), 1)),
        "recovery_note": "conditional on the policy-hazard design; not a robust finding",
        "domino_multiplier_at_15pct_B2C_drop": {
            "n": int(h15.sum()),
            "demand_induced_share_real": pct((M15 / np.maximum(D15 + M15, 1e-9))[h15]),
            "demand_induced_share_nominal": pct((Mn15 / np.maximum(D15 + Mn15, 1e-9))[h15]),
            "b2b_lag_quarters_behind_b2c": pct(lagq) if bothc.any() else None},
        "automation_feedback": auto,
        "for_other_stages": {
            "peak_jobs_lost_share": {**pct(U_peak), "median_given_S2a": float(np.median(U_peak[s2a])) if s2a.any() else None},
            "automation_rents_share_gdp_2040": pct(o["aishare"][:, yi(2040)]),
            "min_real_gdp_index": pct(o["GDPr"].min(1)),
            "min_bottom80_real_consumption_index": pct(minBR),
            "note": ("S4/S5 should use S2a (participation) for 'mouths to feed'; S2b for firm-level 'no customers'. "
                     "Programme probability and rents share feed S4. c_ai fixed here (S3 would raise it)."),
        },
        "top_drivers_S2a": drivers(s2a), "top_drivers_S2b": drivers(s2b),
        "samples_thinned_every_4th": {
            "s2a_indicator": s2a[th].astype(int).tolist(),
            "s2a_year": [None if np.isnan(y) else round(float(y), 2) for y in s2a_year[th]],
            "s2b_indicator": s2b[th].astype(int).tolist(),
            "policy_enacted": pol[th].astype(int).tolist(),
            "peak_jobs_lost_share": [round(float(x), 4) for x in U_peak[th]],
            "min_bottom80_real_consumption": [round(float(x), 4) for x in minBR[th]],
        },
        "runtime_sec": round(time.time() - t_start, 1),
    }
    with open(os.path.join(RES, "m2_no_customers_domino.json"), "w") as fh:
        json.dump(res, fh, indent=1)
    make_figures(o, s2a, s2a_year, s2b, s2b_year, var)
    print(json.dumps({k: res[k] for k in ("stage_probability", "S2b_consumption_cascade", "S2b_nominal_variant",
                                           "bottom80_real_consumption_min_below", "P_S2a_and_S2b",
                                           "timeline", "monte_carlo_ci_95", "structural_band", "by_D_tercile",
                                           "validation_jobs_lost", "policy", "monetary", "debt",
                                           "sensitivity_S2a_jobs_lost_threshold", "sensitivity_S2b_B2B_threshold",
                                           "domino_multiplier_at_15pct_B2C_drop", "calibration_check",
                                           "transfer_dependence_bottom80_at_S2a_onset", "automation_feedback",
                                           "recovery_by_2060_given_S2b")}, indent=1))
    for d in res["top_drivers_S2b"][:6]:
        print("S2b driver", d)
    print(f"runtime {res['runtime_sec']} s")


def make_figures(o, s2a, s2a_year, s2b, s2b_year, var):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    ink, muted, grid = "#1f2328", "#6b7280", "#e5e7eb"
    c1, c2, c3 = "#2a78d6", "#eb6834", "#1baf7a"
    plt.rcParams.update({"font.size": 9, "axes.edgecolor": muted, "axes.labelcolor": ink,
                         "xtick.color": muted, "ytick.color": muted})

    def clean(ax):
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        ax.grid(color=grid, lw=0.6)

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.3))
    ax = axes[0]
    for key, col, lab in (("BR", c1, "Bottom-80% real consumption"), ("GDPr", c2, "Real GDP"),
                          ("B2B", c3, "Household-serving B2B output")):
        p10, p50, p90 = np.percentile(o[key], [10, 50, 90], axis=0)
        ax.fill_between(YEARS, p10, p90, color=col, alpha=0.15, lw=0)
        ax.plot(YEARS, p50, color=col, lw=2, label=lab)
    ax.axhline(COLLAPSE_LEVEL, color=muted, lw=0.8, ls="--")
    ax.set_ylim(0.4, 1.6); ax.set_ylabel("Index, 2026 = 1")
    ax.set_title("Demand paths (median, 10-90%)", loc="left", color=ink)
    ax.legend(frameon=False, fontsize=7.5, loc="upper left"); clean(ax)

    ax = axes[1]
    p10, p50, p90 = np.percentile(o["U"], [10, 50, 90], axis=0)
    ax.fill_between(YEARS, p10, p90, color=c1, alpha=0.15, lw=0)
    ax.plot(YEARS, p50, color=c1, lw=2, label="Jobs lost vs 2026 (median, 10-90%)")
    t10, t50, t90 = np.percentile(o["trdep"], [10, 50, 90], axis=0)
    ax.plot(YEARS, t50, color=c2, lw=2, label="Transfer share of bottom-80 income (median)")
    ax.axhline(PART_LEVEL, color=muted, lw=0.8, ls="--")
    ax.set_ylim(-0.05, 1.0); ax.set_ylabel("Share")
    ax.set_title("Participation and transfer dependence", loc="left", color=ink)
    ax.legend(frameon=False, fontsize=7.5, loc="upper left"); clean(ax)

    ax = axes[2]
    bins = np.arange(2026, 2061.01, 0.25)
    for yrs, col, lab in ((s2a_year, c1, "S2a participation collapse"), (s2b_year, c2, "S2b consumption cascade")):
        cdf = [(yrs <= b).mean() for b in bins]
        ax.plot(bins, cdf, color=col, lw=2, label=f"{lab} (by 2060: {cdf[-1]:.2f})")
    ax.set_ylim(0, 1); ax.set_xlabel("Calendar year"); ax.set_ylabel("Cumulative probability given S1")
    ax.set_title("Onset timing", loc="left", color=ink)
    ax.legend(frameon=False, fontsize=7.5, loc="upper left"); clean(ax)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "m2_no_customers_domino_paths_timing.png"), dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 5))
    names = list(var.keys())
    ypos = np.arange(len(names))
    ax.scatter([var[k]["S2a"] for k in names], ypos, color=c1, s=40, label="S2a participation", zorder=3)
    ax.scatter([var[k]["S2b"] for k in names], ypos, color=c2, s=40, label="S2b consumption cascade", zorder=3)
    ax.set_yticks(ypos); ax.set_yticklabels([k.replace("_", " ") for k in names], fontsize=8)
    ax.invert_yaxis(); ax.set_xlim(0, 1); ax.set_xlabel("P(outcome | S1)")
    ax.set_title("Structural uncertainty across model variants", loc="left", color=ink)
    ax.legend(frameon=False, fontsize=8, loc="lower right"); clean(ax)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "m2_no_customers_domino_structural_band.png"), dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6, 4))
    r = o["A"][:, yi(2040)] / np.maximum(o["A_cf"][:, yi(2040)], 1e-6)
    v = o["A_cf"][:, yi(2040)] > 0.01
    b = np.linspace(0.6, 1.6, 51)
    ax.hist(np.clip(r[v & ~s2b], 0.6, 1.6), bins=b, color=muted, alpha=0.6, label="No S2b", density=True)
    ax.hist(np.clip(r[v & s2b], 0.6, 1.6), bins=b, color=c1, alpha=0.7, label="S2b occurs", density=True)
    ax.axvline(1.0, color=ink, lw=0.8)
    ax.set_xlabel("Automation share 2040: with demand feedback / without"); ax.set_ylabel("Density")
    ax.set_title("Does demand collapse speed or slow automation?", loc="left", color=ink)
    ax.legend(frameon=False); clean(ax)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "m2_no_customers_domino_automation_feedback.png"), dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    main()
