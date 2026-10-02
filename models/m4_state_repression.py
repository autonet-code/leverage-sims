"""
S4 model (v2): unrest suppressed. State vs AI capital vs citizens.

Extended Acemoglu-Robinson democratization/repression game, simulated year by year over
parameter uncertainty (Monte Carlo) and path randomness.

Players
  Citizens  : protest participation P_t (collective action with loss aversion, in-group
              fragmentation, reference-point adaptation, perceived efficacy from last year's
              success odds, discounting of non-credible transfers); violence share v_t rises.
  State     : each year of mass unrest picks one of four actions by multinomial logit on
              utilities (with a one-step deterrence continuation value for repression):
                CONCEDE  transfer covering cov*D of labor income, with an explicit budget cost
                MIX      partial transfer (0.5*cov) plus repression (carrot and stick)
                REPRESS  no transfer
                POPULIST unrest channelled into nativism/scapegoating: no transfer, no repression
  AI capital: (a) share rr of state revenue (rentier logic, threshold effect on accountability),
              (b) continuous lobbying that raises elite alignment in proportion to rr,
              (c) bears the net tax of transfers (loss-averse), recaptures part of transfers as
                  revenue in proportion to c_mass (Fordist counterforce),
              (d) suffers sabotage costs from violent unrest (falls with coercion automation).

Scenario text mechanisms: coercion automation a_t (removes defection channel, cheapens
repression, enables pre-emptive surveillance); rentier shift rr_t; "people not needed"
(state dependence on labor for revenue and soldiers falls continuously with D and a).

"No customers" (user's S2 point): mass demand loss = kd * uncompensated displacement;
AI rents scale by (1 - c_mass * demand_loss), so AI rents and the rentier channel shrink
when AI sells mostly to the public, and AI capital gains from transfers that restore demand.

Stage definition (headline = BROAD S4 in a jurisdiction, within 20 y of the S2 midpoint):
  strict S4: state represses (REPRESS or MIX) in >=3 of the last 4 mass-unrest years
     (participation >=1%) while no ADEQUATE redistribution is in place; absorbing.
  broad S4: strict, OR at the horizon the regime was not overthrown, displacement >=20% of
     labor income, no adequate redistribution in place, for >=3 consecutive years.
  ADEQUATE redistribution: transfers in place >= adeq * D (adeq 0.5, sensitivity 0.3/0.7).

Conditioning: S1, S2 (plateau labor-income loss D_max 30-80%), S3 (AI providers capture
30-80% of displaced income) have occurred. S2 midpoint T2 is aligned to the S2 model's
S2a onset distribution (p10 2038.75, median 2046, p90 2055.5); offsets exported.

Headline jurisdictions US and China reported separately. The combined "US or China" figure
assumes conditional independence; comonotone and countermonotone bounds are also reported.
China's S4 is labelled party-state repression, not AI-capital capture.

Run: python m4_state_repression.py
"""
import json
import os
import time
import warnings

import numpy as np
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SEED = 20260930
N_DRAWS = 20000        # parameter draws
M_PATHS = 16           # stochastic paths per draw
YEARS = np.arange(2027, 2091)
CFG_DEFAULT = dict(
    horizon=20, adeq=0.5, cov="beta45", lock_rule="3of4", actions=("con", "mix", "rep", "pop"),
    coerce_shift=0.0, rho=(0.005, 0.04), p_dr=(0.25, 0.5, 0.75), US_I=(0.55, 0.85),
    CN_pp=(0.05, 0.5), CN_SQ=(0.5, 1.5), c_mass=(0.2, 0.9), fisc_scale=1.0,
    fiscal_cost=True, ratchet=True, noise=(0.5, 1.5),
)
CFG = dict(CFG_DEFAULT)
MASS_UNREST = 0.01
MIX_FRAC = 0.5
LOCK_YEARS = 3

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(BASE, "results", "m4_state_repression.json")
FIG1 = os.path.join(BASE, "figures", "m4_state_repression_by_regime.png")
FIG2 = os.path.join(BASE, "figures", "m4_state_repression_convergence_sensitivity.png")


def U(rng, lo, hi, n):
    return rng.uniform(lo, hi, n)


def tri(rng, lo, mode, hi, n):
    return rng.triangular(lo, mode, hi, n)


def sig(x):
    return 1.0 / (1.0 + np.exp(-x))


PRIOR_DOC = {
    "T2": "S2 midpoint year. Aligned to S2 model S2a onset (results/m2_no_customers_domino.json: p10 2038.75, median 2046, p90 2055.5): 2026 + LogNormal(median 20y, sigma 0.33).",
    "D_max": "Plateau share of labor income lost, conditional on S2: U(0.3,0.8). S2 model median peak jobs lost given S2a 0.42.",
    "tau_D": "Displacement ramp time scale U(2,6)y; judgment.",
    "lam": "Loss aversion N(2.0,0.3) clipped [1.3,3]: Tversky & Kahneman 1992; Brown et al. 2024 meta-analysis.",
    "tau_ref": "Reference-point adaptation U(2,6)y; Clark et al. 2008.",
    "mu_abs": "Weight of absolute deprivation in grievance U(0.5,1.5); judgment.",
    "phi": "Protest coalition cohesion U(0.4,0.9): UBI support 68% Dem vs 28% Rep (Gallup/Northeastern 2018).",
    "P_cap": "Max participation share U(0.05,0.25): Chile 2019 ~6%, Hong Kong 2019 up to ~25%; Chenoweth 2020.",
    "g50": "Grievance at half-max participation U(0.3,0.9); Granovetter 1978 thresholds; judgment.",
    "v_max": "Eventual violent share U(0.3,0.7); scenario text; Soufan Center May 2026.",
    "tau_v": "Violence escalation U(1,4) unrest-years; judgment.",
    "s_loyal": "Campaign success with loyal forces Beta mean 0.15: Iran 2026, Syria, Bahrain, HK, Belarus.",
    "s_def": "Campaign success with defection U(0.6,0.9): Tunisia, Egypt, Bangladesh 2024, Nepal 2025, Madagascar 2025.",
    "viol_pen": "Violence penalty on success U(0.4,0.6): violent 26% vs nonviolent 53% (Chenoweth & Stephan).",
    "k_auto": "Curvature of defection removal (1-a)^k, U(1,3); judgment.",
    "camp_dur": "Campaign duration U(2,4)y (NAVCO median ~3y).",
    "t_half": "Coercion automation a_t = sigmoid((t - t_half)/w). t_half = 2042.6 + N(0,4) + 0.5*(T2-2046) + regime shift: calendar-anchored so a(2035) median ~0.2 for leading states (prior 0.2, 0.05-0.5; Ukraine drones, Xinjiang), partially correlated with S2 timing.",
    "deter": "Deterrence of participation by automated surveillance after repression U(0.3,0.8): Xinjiang (Greitens et al. 2019). Stock builds with repression, decays 20%/y.",
    "deter_pre": "Pre-emptive surveillance/AI persuasion deterrence before any repression = deter * U(0.1,0.5); judgment.",
    "r0": "AI/Big Tech share of state revenue today U(0.005,0.02): 10-K estimate.",
    "L0": "Labor-linked revenue share: US 0.84 (CBO FY2025); other democracies 0.75; autocracies/China 0.6.",
    "LS": "Labor share of GDP: US 0.55 (BLS), China 0.5, others 0.55. Converts transfers to GDP shares.",
    "cap_share": "Share of displaced labor income captured as AI rents (S3) U(0.3,0.8).",
    "eff_tax": "Effective tax on AI rents feeding ordinary revenue U(0.2,0.9).",
    "head": "Extra taxable share of AI rents available to finance transfers U(0.2,0.6) (profit shifting, capital mobility); judgment.",
    "c_mass": "Share of AI revenue ultimately dependent on mass consumer demand U(0.2,0.9): low = AI sells to state/military/firms (scenario text view); high = Fordist.",
    "kd": "Mass demand loss per unit of uncompensated displacement U(0.3,0.9): savings, capital-income consumption buffers; S2 model finds consumption protected mainly by transfers.",
    "h_dom": "Domestic share of AI rents for non-host states U(0.1,0.5).",
    "r_thr": "Rentier threshold tri(0.25,0.4,0.6): petrostates vs Norway.",
    "m_rent": "Rentier multiplier on accountability tri(0.5,0.67,1.0): Ross vs Haber & Menaldo.",
    "shield": "Institutional shielding U(0,0.6): Norway/Canada/Australia.",
    "alpha1": "Threshold increase in elite alignment with AI capital once rentier U(0.2,0.6); Drago & Laine 2025.",
    "lob": "Continuous AI-capital lobbying/persuasion: alignment += lob*rr*(1-shield*I), lob U(0.2,1.0); judgment.",
    "A": "Elite (AI capital) loss from net transfer tax, per 10% of GDP, U(0.3,1.5) times loss aversion and alignment; judgment (value of office per year = 1).",
    "Bf": "Cost of transfer financing not covered by AI-rent tax (other taxes, deficit), per 10% of GDP, U(0.3,1.5); judgment.",
    "B": "Electoral reward for restoring income U(1,3) times I; Acemoglu & Robinson; New Deal.",
    "B_perf": "Performance-legitimacy reward U(0.3,1.2) times (1-I).",
    "Nd": "'People needed' value U(0.5,2) times dependence dep = 0.5*labor revenue share + 0.5*(1-a)^k (revenue and soldiers). Falls continuously with D and a; no threshold.",
    "C_rep": "Repression cost U(0.2,1.0) per (P/0.035)^0.7 (concave), times (1-a)^k and (1-leg*v).",
    "leg": "Violence legitimizes repression U(0.2,0.6); Luddites/Swing.",
    "K_inst": "Institutional repression cost U(0.5,2) times I.",
    "V_off": "Value of office lost on overthrow U(2,10).",
    "Sb": "Sabotage cost to AI capital U(0,1) times v*min(P/0.035,3)*(1-a)^k; internalised by the state via alignment. 75 data-center projects blocked/delayed Q1 2026.",
    "g_x": "Extra growth after automation log-U(0.005,0.2): abundance makes transfers cheaper relative to GDP.",
    "p_dr": "P(democracy enacts a redistribution programme before mass unrest) tri(0.25,0.5,0.75). Calibrated per path so P(pre-empt before first mass unrest or horizon | mechanisms off) equals the target.",
    "p_perf": "Autocracies' own P(pre-emptive transfer programme before mass unrest): China U(0.05,0.5) (1990s SOE layoffs of ~30M: xiagang allowances and dibao expansion from ~2.6M to ~22M recipients 1999-2002 show programmes do appear, but at low replacement rates, which cov captures; 'common prosperity' 2021 mostly rhetorical), generic autocracy U(0.05,0.5) (Gulf rentier welfare, small citizen populations). Independent of p_dr.",
    "cov": "Coverage per concession round (share of the currently uncompensated labor-income loss replaced; rounds ratchet cumulatively, as welfare programmes expanded incrementally) 0.1 + 0.9*Beta(2.4,3.77), mean 0.45: China shock transfers offset ~10% of lost wages (Autor, Dorn & Hanson AER 2013) at the low end; CARES Act 2020 emergency UI (>100% replacement for many) at the high end.",
    "p_temp": "P(transfer is temporary, emergency style) U(0.2,0.6); expires after U(2,5)y (CARES Act expired 2020-21). Permanence separate from coverage.",
    "p_index": "P(permanent transfer is indexed to ongoing displacement) U(0.2,0.6).",
    "rho": "Rollback hazard of transfers U(0.005,0.04)/y times alignment: Pierson 1994.",
    "beta_sq": "Path dependence bonus for continuing repression U(0.2,1.0).",
    "noise": "Logit noise scale U(0.5,1.5).",
    "pop0": "Base utility of populist redirection U(-1.0,0.3), decays 0.3 per prior use: China shock political response was polarization, not transfers (Autor et al. AER 2020).",
    "pop_div": "Participation diverted by populist redirection next year U(0.2,0.6), effectiveness 0.7^uses.",
    "cred": "Credibility of transfers = 0.3+0.7*I: citizens discount non-credible transfers (Acemoglu-Robinson commitment problem); state's reward scales with it.",
    "eps_cap": "Backsliding per unrest-year times alignment U(0,0.06); V-Dem 2026.",
    "p_dem_new": "P(overthrow yields democracy): liberal/US U(0.5,0.9); others U(0.15,0.5). Overthrow into autocracy redraws SQ and m from the autocracy spec.",
}

REGIMES = {
    "liberal_democracy":   dict(I=(0.75, 0.95), SQ=(-1.0, 0.0), m=(1.0, 1.0), pd=(0.3, 0.6), lag=2.0,
                                L0=0.75, LS=0.55, a0=(0.1, 0.3), host=False, eb=(-0.005, 0.01), pdn=(0.5, 0.9),
                                pp=(0.05, 0.5), w=0.07),
    "electoral_democracy": dict(I=(0.4, 0.7), SQ=(-0.5, 0.5), m=(0.7, 1.0), pd=(0.2, 0.5), lag=0.0,
                                L0=0.75, LS=0.55, a0=(0.2, 0.4), host=False, eb=(-0.005, 0.015), pdn=(0.15, 0.5),
                                pp=(0.05, 0.5), w=0.19),
    "autocracy":           dict(I=(0.05, 0.3), SQ=(0.3, 1.5), m=(0.2, 0.5), pd=(0.1, 0.3), lag=-2.0,
                                L0=0.6, LS=0.55, a0=(0.3, 0.6), host=False, eb=(0.0, 0.01), pdn=(0.15, 0.5),
                                pp=(0.05, 0.5), w=0.74),
    "US":                  dict(I=(0.55, 0.85), SQ=(-0.7, 0.2), m=(1.0, 1.0), pd=(0.2, 0.5), lag=0.0,
                                L0=0.84, LS=0.55, a0=(0.2, 0.45), host=True, eb=(-0.005, 0.015), pdn=(0.5, 0.9),
                                pp=(0.05, 0.5), w=0.0),
    "China":               dict(I=(0.03, 0.12), SQ=(0.5, 1.5), m=(0.15, 0.4), pd=(0.05, 0.25), lag=-3.0,
                                L0=0.6, LS=0.5, a0=(0.2, 0.5), host=True, eb=(0.0, 0.005), pdn=(0.15, 0.5),
                                pp=(0.05, 0.5), w=0.0),
}
AUTO_SPEC = REGIMES["autocracy"]


def draw_cov(rng, n):
    c = CFG["cov"]
    if c == "beta45":
        return 0.1 + 0.9 * rng.beta(2.4, 3.77, n)
    if c == "beta30":
        return 0.1 + 0.9 * rng.beta(2.0, 7.0, n)
    if c == "generous":
        return U(rng, 0.6, 1.0, n)
    raise ValueError(c)


def draw_global(rng, n):
    g = {}
    g["T2"] = 2026 + np.exp(rng.normal(np.log(20.0), 0.33, n))
    g["D_max"] = U(rng, 0.3, 0.8, n)
    g["tau_D"] = U(rng, 2, 6, n)
    g["lam"] = np.clip(rng.normal(2.0, 0.3, n), 1.3, 3.0)
    g["tau_ref"] = U(rng, 2, 6, n)
    g["mu_abs"] = U(rng, 0.5, 1.5, n)
    g["phi"] = U(rng, 0.4, 0.9, n)
    g["P_cap"] = U(rng, 0.05, 0.25, n)
    g["g50"] = U(rng, 0.3, 0.9, n)
    g["v_max"] = U(rng, 0.3, 0.7, n)
    g["tau_v"] = U(rng, 1, 4, n)
    g["s_loyal"] = rng.beta(4, 22.7, n)
    g["s_def"] = U(rng, 0.6, 0.9, n)
    g["viol_pen"] = U(rng, 0.4, 0.6, n)
    g["k_auto"] = U(rng, 1, 3, n)
    g["camp_dur"] = U(rng, 2, 4, n)
    g["t_half0"] = 2042.6 + rng.normal(0, 4, n)
    g["w_auto"] = U(rng, 3, 8, n)
    g["deter"] = U(rng, 0.3, 0.8, n)
    g["deter_pre_f"] = U(rng, 0.1, 0.5, n)
    g["r0"] = U(rng, 0.005, 0.02, n)
    g["cap_share"] = U(rng, 0.3, 0.8, n)
    g["eff_tax"] = U(rng, 0.2, 0.9, n)
    g["head"] = U(rng, 0.2, 0.6, n)
    g["c_mass"] = U(rng, *CFG["c_mass"], n)
    g["kd"] = U(rng, 0.3, 0.9, n)
    g["h_dom"] = U(rng, 0.1, 0.5, n)
    g["r_thr"] = tri(rng, 0.25, 0.4, 0.6, n)
    g["m_rent"] = tri(rng, 0.5, 0.67, 1.0, n)
    g["shield"] = U(rng, 0.0, 0.6, n)
    g["alpha1"] = U(rng, 0.2, 0.6, n)
    g["lob"] = U(rng, 0.2, 1.0, n)
    g["A"] = U(rng, 0.3, 1.5, n)
    g["Bf"] = U(rng, 0.3, 1.5, n)
    g["B"] = U(rng, 1, 3, n)
    g["B_perf"] = U(rng, 0.3, 1.2, n)
    g["Nd"] = U(rng, 0.5, 2.0, n)
    g["C_rep"] = U(rng, 0.2, 1.0, n)
    g["leg"] = U(rng, 0.2, 0.6, n)
    g["K_inst"] = U(rng, 0.5, 2, n)
    g["V_off"] = U(rng, 2, 10, n)
    g["Sb"] = U(rng, 0.0, 1.0, n)
    g["g_x"] = np.exp(U(rng, np.log(0.005), np.log(0.2), n))
    g["p_dr"] = tri(rng, *CFG["p_dr"], n)
    g["rho"] = U(rng, *CFG["rho"], n)
    g["beta_sq"] = U(rng, 0.2, 1.0, n)
    g["noise"] = U(rng, *CFG["noise"], n)
    g["eps_cap"] = U(rng, 0.0, 0.06, n)
    g["cov"] = draw_cov(rng, n)
    g["p_temp"] = U(rng, 0.2, 0.6, n)
    g["dur_temp"] = U(rng, 2, 5, n)
    g["p_index"] = U(rng, 0.2, 0.6, n)
    g["pop0"] = U(rng, -1.0, 0.3, n)
    g["pop_div"] = U(rng, 0.2, 0.6, n)
    return g


def draw_regime(rng, n, spec, name=None):
    r = {}
    r["I0"] = U(rng, *(CFG["US_I"] if name == "US" else spec["I"]), n)
    r["SQ"] = U(rng, *(CFG["CN_SQ"] if name == "China" else spec["SQ"]), n)
    r["m"] = U(rng, *spec["m"], n)
    r["pd"] = U(rng, *spec["pd"], n)
    r["a0"] = U(rng, *spec["a0"], n)
    r["eb"] = U(rng, *spec["eb"], n)
    r["pdn"] = U(rng, *spec["pdn"], n)
    r["p_perf"] = U(rng, *(CFG["CN_pp"] if name == "China" else spec["pp"]), n)
    return r


def simulate(g, r, spec, seed, mechanisms=True, calib=False, h_base=None):
    """One path per row. All random draws are full-size arrays in a fixed order so that runs
    with the same seed use common random numbers. calib=True: no pre-emption, no game;
    returns the pre-mass-unrest exposure used to calibrate the pre-emption hazard."""
    rng = np.random.default_rng(seed)
    n = len(g["T2"])
    host = spec["host"]
    L0, LS = spec["L0"], spec["LS"]
    adeq = CFG["adeq"]
    acts = CFG["actions"]
    I = r["I0"].copy()
    SQ = r["SQ"].copy()
    mpart = r["m"].copy()
    ref = np.zeros(n)
    unrest_years = np.zeros(n)
    rep_years = np.zeros(n)
    pop_years = np.zeros(n)
    rep_count = np.zeros(n)
    hist = np.zeros((n, 4))
    S = np.zeros(n)                      # surveillance deterrence stock
    pop_eff_next = np.zeros(n)
    p_prev = np.full(n, 0.2)
    state = np.zeros(n, int)             # 0 open, 1 strict S4 locked, 2 conceded, 3 overthrown->dem
    s4_year = np.full(n, np.nan)
    a_at = np.full(n, np.nan); r_at = np.full(n, np.nan)
    ever_conceded = np.zeros(n, bool)
    ever_mass = np.zeros(n, bool)
    pre_before_mass = np.zeros(n, bool)
    comp_fixed = np.zeros(n)     # permanent, fixed level (erodes in adequacy as D grows)
    idx_ratio = np.zeros(n)      # permanent, indexed: idx_ratio * D
    comp_temp = np.zeros(n)      # temporary (emergency) transfers
    expire = np.full(n, np.inf)
    streak_unmet = np.zeros(n)
    first_unmet3 = np.full(n, np.nan)
    rr_max = np.zeros(n)
    E = np.zeros(n)
    t_end = g["T2"] + CFG["horizon"]
    t_half = (g["t_half0"] + 0.5 * (g["T2"] - 2046) + spec["lag"] + CFG["coerce_shift"])
    dom = 1.0 if host else g["h_dom"]
    ccm = 1.0 if host else 1.0 / (0.5 + 0.5 * g["h_dom"])
    target = None
    terms = {k: 0.0 for k in ["conc_cost", "conc_reward", "rep_cost", "overthrow", "SQ", "sabotage", "deter_gain"]}
    terms_n = 0
    choice_counts = {k: 0 for k in ["con", "mix", "rep", "pop"]}

    for t in YEARS:
        # fixed-order random draws (CRN)
        u_pre, u_idx, u_temp, u_choice, u_over, u_dem, u_rb = (rng.random(n) for _ in range(7))
        sq_new = rng.uniform(*AUTO_SPEC["SQ"], n); m_new = rng.uniform(*AUTO_SPEC["m"], n)
        active = t <= t_end
        D = g["D_max"] * sig((t - g["T2"]) / g["tau_D"])
        # expiry of temporary transfers
        ex = active & (t >= expire)
        comp_temp[ex] = 0; expire[ex] = np.inf
        comp = idx_ratio * D + comp_fixed + comp_temp
        Deff = np.maximum(D - comp, 0)
        adequate = comp >= adeq * D - 1e-12
        reopen = (state == 2) & ((Deff > 0.1) | ~adequate & (D >= 0.2))
        state[reopen] = 0
        cred = 0.3 + 0.7 * I
        Dperc = np.maximum(D - comp * (0.5 + 0.5 * cred), 0)
        ref = ref + (Dperc - ref) * (1 - np.exp(-1.0 / g["tau_ref"]))
        griev = g["lam"] * np.maximum(Dperc - ref, 0) + g["mu_abs"] * Dperc
        P = g["phi"] * mpart * g["P_cap"] * griev**2 / (griev**2 + g["g50"]**2)
        a = sig((t - t_half) / g["w_auto"]) if mechanisms else np.zeros(n)
        P = P * (1 - a * g["deter"] * (S + g["deter_pre_f"] * (1 - S)))
        P = P * np.clip(0.6 + 0.4 * p_prev / 0.2, 0.6, 1.2)
        P = P * (1 - pop_eff_next)
        pop_eff_next[:] = 0
        # Fiscal composition with the no-customers feedback
        dl = g["kd"] * Deff * LS / 0.55
        rents = LS * D * g["cap_share"] * (1 - g["c_mass"] * dl)       # share of GDP
        ai_rev = g["r0"] + L0 * D * g["cap_share"] * (1 - g["c_mass"] * dl) * g["eff_tax"] * dom
        lab_rev = L0 * (1 - D)
        other = (1 - L0 - g["r0"]) * (1 - dl)
        tot = ai_rev + lab_rev + other
        rr = ai_rev / tot if mechanisms else g["r0"] * np.ones(n)
        labsh = lab_rev / tot if mechanisms else np.full(n, L0)
        rr_max = np.where(active, np.maximum(rr_max, rr), rr_max)
        rent_on = sig((rr - g["r_thr"]) / 0.07)
        shield_I = 1 - g["shield"] * I
        align = np.clip(r["a0"] + (g["alpha1"] * rent_on + g["lob"] * rr) * shield_I, 0, 1.5)
        resp = 1 - (1 - g["m_rent"]) * rent_on * shield_I
        ka = (1 - a) ** g["k_auto"]
        dep = 0.5 * labsh / L0 + 0.5 * ka
        v = 0.1 + (g["v_max"] - 0.1) * (1 - np.exp(-(unrest_years + rep_count) / g["tau_v"]))

        open_ = active & (state == 0)
        mass = P >= MASS_UNREST
        pre = open_ & ~mass & (Deff > 0.03)
        w_pre = np.minimum(1, Deff / 0.2) / ccm

        # campaign success (computed for all; feeds efficacy)
        pd_eff = r["pd"] * (1 - 0.4 * v) * ka
        part = np.minimum(1.0, P / 0.035) ** 0.5
        p_camp = np.clip(part * (pd_eff * g["s_def"] + (1 - pd_eff) * g["s_loyal"])
                         * (1 - g["viol_pen"] * (v - 0.1) / 0.9), 0, 0.99)
        p_prev = np.where(active, p_camp, p_prev)

        if calib:
            E += np.where(pre & ~ever_mass, w_pre, 0)
            ever_mass |= active & mass
            continue

        # Pre-unrest redistribution (hazard calibrated to the prior)
        h_pre = h_base * w_pre * resp
        hit = pre & (u_pre < 1 - np.exp(-h_pre))
        pre_before_mass |= hit & ~ever_mass

        def enact(mask, frac):
            # Cumulative (ratchet): each round replaces frac*cov of the currently uncompensated loss
            add = frac * g["cov"] * Deff if CFG["ratchet"] else np.maximum(frac * g["cov"] * D - comp, 0)
            temp = mask & (u_temp < g["p_temp"])
            idx = mask & ~temp & (u_idx < g["p_index"])
            fix = mask & ~temp & ~idx
            comp_temp[temp] += add[temp]
            expire[temp] = t + g["dur_temp"][temp]
            idx_ratio[idx] += add[idx] / np.maximum(D[idx], 1e-9)
            comp_fixed[fix] += add[fix]
            ever_conceded[mask] = True

        enact(hit, 1.0)
        state[hit] = 2

        # Mass-unrest game
        game = open_ & mass & ~hit
        ever_mass |= active & mass
        x = P / 0.035
        h_over = 1 - (1 - p_camp) ** (1 / g["camp_dur"])
        abund = (1 + g["g_x"]) ** (-np.maximum(t - g["T2"], 0))

        def concession_terms(frac):
            added = frac * g["cov"] * Deff if CFG["ratchet"] else np.maximum(frac * g["cov"] * D - comp, 0)
            transfer = added * LS                                  # share of GDP
            if CFG["fiscal_cost"]:
                tax_ai = np.minimum(transfer, g["head"] * rents * dom)
                excess = transfer - tax_ai
                recap = g["c_mass"] * g["cap_share"] * transfer
                net_ai = np.maximum(tax_ai - recap, 0)
                cost = CFG["fisc_scale"] * abund * (g["lam"] * g["A"] * align * net_ai / 0.1 + g["Bf"] * excess / 0.1)
            else:  # v1-style: elite cost proportional to grievance removed
                cost = g["lam"] * 1.25 * align * added * abund * ccm
            removed = np.minimum(added, Deff)
            reward = ((g["B"] * I + g["B_perf"] * (1 - I)) * resp + g["Nd"] * dep) * cred * removed
            return cost, reward

        cc1, cr1 = concession_terms(1.0)
        ccm_, crm = concession_terms(MIX_FRAC)
        rc = (g["C_rep"] * ka * (1 - g["leg"] * v) + I * g["K_inst"]) * x ** 0.7
        over_cost = g["V_off"] * h_over
        sab = g["Sb"] * v * np.minimum(x, 3) * ka * align
        det_gain = 0.9 * g["deter"] * a * (1 - S) * 0.5 * (rc + over_cost)
        sqb = SQ + g["beta_sq"] * (rep_count > 0)
        Ucon = -cc1 + cr1
        Urep = -rc - over_cost + sqb + det_gain - sab
        Umix = -ccm_ + crm - 0.6 * rc - 0.6 * over_cost + 0.5 * sqb + 0.5 * det_gain - 0.5 * sab
        Upop = g["pop0"] - 0.3 * pop_years - 0.5 * over_cost - 0.8 * sab
        Us = {"con": Ucon, "mix": Umix, "rep": Urep, "pop": Upop}
        names = [k for k in ["con", "mix", "rep", "pop"] if k in acts]
        Um = np.stack([Us[k] for k in names], 1) / g["noise"][:, None]
        Um -= Um.max(1, keepdims=True)
        pr = np.exp(Um); pr /= pr.sum(1, keepdims=True)
        cidx = (u_choice[:, None] > np.cumsum(pr, 1)).sum(1)
        cidx = np.minimum(cidx, len(names) - 1)
        ch = {k: game & (cidx == i) for i, k in enumerate(names)}
        for k in ["con", "mix", "rep", "pop"]:
            ch.setdefault(k, np.zeros(n, bool))
            choice_counts[k] += int(ch[k].sum())
        if game.any():
            gm = game
            for k, arr in [("conc_cost", cc1), ("conc_reward", cr1), ("rep_cost", rc), ("overthrow", over_cost),
                           ("SQ", sqb), ("sabotage", sab), ("deter_gain", det_gain)]:
                terms[k] += float(arr[gm].sum())
            terms_n += int(gm.sum())

        enact(ch["con"], 1.0)
        enact(ch["mix"], MIX_FRAC)
        state[ch["con"]] = 2
        rep_count[ch["con"]] = 0
        repm = ch["rep"] | ch["mix"]
        rep_count[repm] += 1
        rep_years[repm] += 1
        pop_years[ch["pop"]] += 1
        pop_eff_next[ch["pop"]] = g["pop_div"][ch["pop"]] * 0.7 ** (pop_years[ch["pop"]] - 1)
        S = np.where(ch["rep"], S + (1 - S) * 0.5, np.where(ch["mix"], S + (1 - S) * 0.25, S * 0.8))
        unrest_years[game] += 1
        hist[game] = np.roll(hist[game], -1, axis=1)
        hist[game, -1] = repm[game]
        # Overthrow
        ho = np.where(ch["rep"], h_over, np.where(ch["mix"], 0.6 * h_over, np.where(ch["pop"], 0.5 * h_over, 0)))
        over = game & ~ch["con"] & (u_over < ho)
        to_dem = over & (u_dem < r["pdn"])
        state[to_dem] = 3
        to_aut = over & ~to_dem
        I[to_aut] = np.minimum(I[to_aut], 0.15)
        SQ[to_aut] = sq_new[to_aut]; mpart[to_aut] = m_new[to_aut]
        rep_count[to_aut] = 0; hist[to_aut] = 0
        # Strict lock-in
        comp = idx_ratio * D + comp_fixed + comp_temp
        adequate = comp >= adeq * D - 1e-12
        if CFG["lock_rule"] == "3of4":
            lock_ok = hist.sum(1) >= LOCK_YEARS
        else:
            lock_ok = rep_count >= LOCK_YEARS
        lock = repm & ~over & lock_ok & ~adequate
        state[lock] = 1; s4_year[lock] = t
        a_at[lock] = a[lock]; r_at[lock] = rr[lock]
        # Rollback of transfers (elites aligned with AI capital)
        has = comp > 0
        rb = active & (state != 3) & (state != 1) & has & (u_rb < g["rho"] * align)
        comp_fixed[rb] = 0; idx_ratio[rb] = 0; comp_temp[rb] = 0; expire[rb] = np.inf
        state[rb & (state == 2)] = 0
        # Unmet streak (no adequate redistribution, D>=0.2, not overthrown/locked)
        comp = idx_ratio * D + comp_fixed + comp_temp
        adequate = comp >= adeq * D - 1e-12
        unmet = active & ((state == 0) | (state == 2)) & ~adequate & (D >= 0.2)
        streak_unmet = np.where(unmet, streak_unmet + 1, np.where(active, 0, streak_unmet))
        newb = np.isnan(first_unmet3) & (streak_unmet >= LOCK_YEARS)
        first_unmet3[newb] = t
        # Backsliding
        I = np.clip(I - r["eb"] - g["eps_cap"] * align * (active & mass & (state == 0)), 0.02, 1)

    if calib:
        return E

    comp_end = idx_ratio * g["D_max"] * sig((t_end - g["T2"]) / g["tau_D"]) + comp_fixed + comp_temp
    strict = state == 1
    broad_only = ((state == 0) | (state == 2)) & (streak_unmet >= LOCK_YEARS)
    broad = strict | broad_only
    year = np.where(strict, s4_year, np.where(broad_only, first_unmet3, np.nan))
    D_end = g["D_max"] * sig((t_end - g["T2"]) / g["tau_D"])
    kind = np.full(n, "", dtype=object)
    kind[broad_only & (rep_years > 0) & (rep_years >= pop_years)] = "repression_nonstrict"
    kind[broad_only & (pop_years > rep_years)] = "populist_redirection"
    kind[broad_only & (rep_years == 0) & (pop_years == 0)] = "ignored_or_preempted_no_game"
    adequate_end = (comp_end >= adeq * D_end - 1e-12)
    return dict(broad=broad, strict=strict, broad_year=year, state=state, kind=kind,
                adequate_end=adequate_end & ~broad & (state != 3), s4_year=s4_year,
                a_at=a_at, r_at=r_at, ever_conceded=ever_conceded, pre_before_mass=pre_before_mass,
                ever_mass=ever_mass, rr_max=rr_max, r_thr=g["r_thr"], terms={k: v / max(terms_n, 1) for k, v in terms.items()},
                choice_counts=choice_counts, Deff_end=np.maximum(D_end - comp_end, 0))


def calibrate(g, r, spec, name, seed):
    """Per-path pre-emption hazard such that P(pre-emptive programme before first mass unrest
    or the horizon) equals the target, in the mechanisms-off world."""
    E = simulate(g, r, spec, seed, mechanisms=False, calib=True)
    Iw = np.clip((r["I0"] - 0.15) / 0.65, 0, 1)
    target = Iw * g["p_dr"] + (1 - Iw) * r["p_perf"]
    h = -np.log(1 - np.clip(target, 0, 0.99)) / np.maximum(E, 1e-9)
    h = np.where(E > 1e-9, h, 0.0)
    return h, target, E


def run_jur(g, r, spec, name, seed, mechanisms=True):
    h, target, E = calibrate(g, r, spec, name, seed + 999)
    res = simulate(g, r, spec, seed, mechanisms=mechanisms, h_base=h)
    res["target"] = target; res["E"] = E
    return res


def bootstrap_ci(x, rng, B=2000):
    n = len(x)
    ms = np.array([x[rng.integers(0, n, n)].mean() for _ in range(B)])
    return float(np.percentile(ms, 2.5)), float(np.percentile(ms, 97.5))


STRUCTURAL = {   # pre-registered structural/definitional variants -> headline range
    "base": {},
    "adeq_0.3": dict(adeq=0.3),
    "adeq_0.7": dict(adeq=0.7),
    "cov_generous_U(0.6,1.0)_v1": dict(cov="generous"),
    "cov_low_mean_0.30": dict(cov="beta30"),
    "binary_actions_con_rep": dict(actions=("con", "rep")),
    "no_populist_action": dict(actions=("con", "mix", "rep")),
    "lock_3_consecutive_v1": dict(lock_rule="consec"),
    "no_fiscal_cost_v1_style": dict(fiscal_cost=False),
    "fiscal_cost_x0.5": dict(fisc_scale=0.5),
    "fiscal_cost_x2": dict(fisc_scale=2.0),
    "c_mass_low_(0.05,0.3)": dict(c_mass=(0.05, 0.3)),
    "c_mass_high_(0.7,0.95)": dict(c_mass=(0.7, 0.95)),
    "China_SQ_low_(0,0.8)": dict(CN_SQ=(0.0, 0.8)),
    "China_p_perf_high_(0.2,0.8)": dict(CN_pp=(0.2, 0.8)),
    "China_p_perf_low_(0.02,0.2)": dict(CN_pp=(0.02, 0.2)),
    "no_ratchet_single_round": dict(ratchet=False),
    "low_logit_noise_(0.15,0.5)": dict(noise=(0.15, 0.5)),
}
SCENARIOS = {    # assumptions about the world (reported, not in the structural range)
    "horizon_30y": dict(horizon=30),
    "fast_coercion_automation (-5y)": dict(coerce_shift=-5.0),
    "slow_coercion_automation (+5y)": dict(coerce_shift=5.0),
    "US_severe_backsliding (I 0.3-0.6)": dict(US_I=(0.3, 0.6)),
    "high_rollback (rho 0.03-0.10)": dict(rho=(0.03, 0.10)),
    "weak_democratic_response (p_dr 0.1-0.4)": dict(p_dr=(0.1, 0.25, 0.4)),
}


def quick_run(overrides, n=4000, m=8, seed=SEED + 7):
    CFG.clear(); CFG.update(CFG_DEFAULT); CFG.update(overrides)
    rng = np.random.default_rng(seed)
    g0 = draw_global(rng, n)
    rows = {k: np.repeat(v, m) for k, v in g0.items()}
    out = {}
    for j, name in enumerate(["US", "China"]):
        r0 = draw_regime(rng, n, REGIMES[name], name)
        rr = {k: np.repeat(v, m) for k, v in r0.items()}
        on = run_jur(rows, rr, REGIMES[name], name, seed + 100 + j, True)
        off = run_jur(rows, rr, REGIMES[name], name, seed + 100 + j, False)
        out[name] = on["broad"].reshape(n, m).mean(1)
        out[name + "_cf"] = off["broad"].reshape(n, m).mean(1)
        out[name + "_strict"] = float(on["strict"].mean())
    CFG.clear(); CFG.update(CFG_DEFAULT)
    p_any = 1 - (1 - out["US"]) * (1 - out["China"])
    p_any_cf = 1 - (1 - out["US_cf"]) * (1 - out["China_cf"])
    return dict(p_any=float(p_any.mean()), p_US=float(out["US"].mean()), p_China=float(out["China"].mean()),
                p_US_strict=out["US_strict"], p_China_strict=out["China_strict"],
                mech_increment_any=float(p_any.mean() - p_any_cf.mean()),
                mech_increment_US=float(out["US"].mean() - out["US_cf"].mean()),
                mech_increment_China=float(out["China"].mean() - out["China_cf"].mean()))


def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    g0 = draw_global(rng, N_DRAWS)
    rows = {k: np.repeat(v, M_PATHS) for k, v in g0.items()}
    out, per_draw, cf, strict, cf_strict, r0s = {}, {}, {}, {}, {}, {}
    for j, (name, spec) in enumerate(REGIMES.items()):
        r0 = draw_regime(rng, N_DRAWS, spec, name)
        rr = {k: np.repeat(v, M_PATHS) for k, v in r0.items()}
        res = run_jur(rows, rr, spec, name, SEED + 100 + j, True)
        res_cf = run_jur(rows, rr, spec, name, SEED + 100 + j, False)   # common random numbers
        out[name] = res; out[name + "_cf"] = res_cf; r0s[name] = r0
        per_draw[name] = res["broad"].reshape(N_DRAWS, M_PATHS).mean(1)
        strict[name] = res["strict"].reshape(N_DRAWS, M_PATHS).mean(1)
        cf[name] = res_cf["broad"].reshape(N_DRAWS, M_PATHS).mean(1)
        cf_strict[name] = res_cf["strict"].reshape(N_DRAWS, M_PATHS).mean(1)
        print(f"  {name} done {time.time()-t0:.0f}s", flush=True)

    brng = np.random.default_rng(SEED + 1)
    pU, pC = per_draw["US"], per_draw["China"]
    p_any = 1 - (1 - pU) * (1 - pC)
    p_any_cf = 1 - (1 - cf["US"]) * (1 - cf["China"])
    p_any_como = np.maximum(pU, pC)
    p_any_counter = np.minimum(1, pU + pC)
    world_w = {k: REGIMES[k]["w"] for k in ["liberal_democracy", "electoral_democracy", "autocracy"]}
    p_world = sum(world_w[k] * per_draw[k] for k in world_w)

    summary = {}
    for name in REGIMES:
        o = out[name]; st = o["state"]
        lo, hi = bootstrap_ci(per_draw[name], brng)
        yrs = o["broad_year"][o["broad"]]
        kinds = {k: float((o["kind"] == k).mean()) for k in ["repression_nonstrict", "populist_redirection", "ignored_or_preempted_no_game"]}
        cc = o["choice_counts"]; tot = max(sum(cc.values()), 1)
        mterms = o["terms"]
        em = o["ever_mass"]
        partial_unmet = (~o["broad"]) & (st != 3) & (o["Deff_end"] > 0.2)
        summary[name] = dict(
            p_s4=float(per_draw[name].mean()), mc_ci=[lo, hi],
            p_s4_counterfactual_no_automation_no_rentier=float(cf[name].mean()),
            mechanism_increment=float(per_draw[name].mean() - cf[name].mean()),
            p_s4_strict_repression_lockin=float(strict[name].mean()),
            p_s4_strict_counterfactual=float(cf_strict[name].mean()),
            broad_without_strict_by_kind=kinds,
            p_adequate_redistribution_at_horizon=float(o["adequate_end"].mean()),
            p_overthrow_to_democracy=float((st == 3).mean()),
            p_other_not_S4=float(1 - o["broad"].mean() - o["adequate_end"].mean() - (st == 3).mean()),
            diag_not_S4_but_Deff_gt_20pct_at_horizon=float(partial_unmet.mean()),
            p_ever_conceded=float(o["ever_conceded"].mean()),
            p_ever_mass_unrest=float(em.mean()),
            implied_p_preempt_before_mass_unrest=float(o["pre_before_mass"].mean()),
            preempt_target_mean=float(o["target"].mean()),
            game_action_shares={k: v / tot for k, v in cc.items()},
            mean_utility_terms_in_game_years=mterms,
            share_paths_rr_crosses_r_thr=float((o["rr_max"] > o["r_thr"]).mean()),
            median_max_ai_revenue_share=float(np.median(o["rr_max"])),
            first_year_claims_unmet_provisional_p10_p50_p90=[float(v) for v in np.percentile(yrs, [10, 50, 90])] if len(yrs) else None,
            median_coercion_automation_at_strict=float(np.nanmedian(o["a_at"])) if o["strict"].any() else None,
            median_ai_revenue_share_at_strict=float(np.nanmedian(o["r_at"])) if o["strict"].any() else None,
            per_draw_sd=float(per_draw[name].std()),
        )
    any_lo, any_hi = bootstrap_ci(p_any, brng)
    w_lo, w_hi = bootstrap_ci(p_world, brng)

    yU = out["US"]["broad_year"]; yC = out["China"]["broad_year"]
    first = np.fmin(yU, yC)
    first_ok = first[~np.isnan(first)]
    offs = (first - rows["T2"])[~np.isnan(first)]
    p10, p50, p90 = np.percentile(first_ok, [10, 50, 90])
    yU_ok = yU[~np.isnan(yU)]

    run_mean = np.cumsum(p_any) / np.arange(1, N_DRAWS + 1)
    halfw = 1.96 * p_any.std(ddof=1) / np.sqrt(N_DRAWS)
    checkpoints = {int(k): float(run_mean[k - 1]) for k in [1000, 2500, 5000, 10000, 15000, 20000] if k <= N_DRAWS}
    cum = {name: [float(np.mean(out[name]["broad_year"] <= Y)) for Y in YEARS] for name in REGIMES}
    cum_any = [float(np.mean(first <= Y)) for Y in YEARS]

    def spearman(target, regs):
        s = {}
        for k, v in g0.items():
            if np.ptp(v) > 0:
                s[k] = float(stats.spearmanr(v, target).statistic)
        for pre, rn in regs:
            for k, v in r0s[rn].items():
                if np.ptp(v) > 0:
                    s[pre + k] = float(stats.spearmanr(v, target).statistic)
        return dict(sorted(s.items(), key=lambda kv: -abs(kv[1]))[:12])
    sens_US = spearman(pU, [("US_", "US")])
    sens_CN = spearman(pC, [("CN_", "China")])

    a2035 = sig((2035 - (g0["t_half0"] + 0.5 * (g0["T2"] - 2046))) / g0["w_auto"])

    print("  running structural variants and scenarios...", flush=True)
    struct = {k: quick_run(v) for k, v in STRUCTURAL.items()}
    scen = {k: quick_run(v) for k, v in SCENARIOS.items()}
    sv = [v["p_any"] for v in struct.values()]
    svU = [v["p_US"] for v in struct.values()]
    svC = [v["p_China"] for v in struct.values()]

    sub = np.random.default_rng(SEED + 2).choice(N_DRAWS, 5000, replace=False)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        med_year_draw = np.nanmedian(first.reshape(N_DRAWS, M_PATHS), axis=1)

    result = {
        "stage": "S4 unrest suppressed (claims of displaced citizens defeated: repression, populist redirection, or neglect without adequate redistribution)",
        "version": 2,
        "stage_probability": {
            "mean": float(p_any.mean()),
            "ci_low": float(min(sv)), "ci_high": float(max(sv)),
            "ci_type": "structural range: min/max of P(US or China) across pre-registered structural variants (4000x8 runs); Monte Carlo CI is separate",
            "monte_carlo_ci_95": [any_lo, any_hi],
            "definition": ("P(in at least one of US/China, within 20y of the S2 midpoint, EITHER the state represses (REPRESS or carrot-and-stick MIX) "
                           "in >=3 of the last 4 mass-unrest years (>=1% participation) with no adequate redistribution in place (strict S4), "
                           "OR at the horizon the regime is not overthrown and for >=3 consecutive years displacement >=20% of labor income has had "
                           "no adequate redistribution (transfers >= 50% of lost labor income) | S1, S2, S3). Independence between US and China."),
            "dependence_bounds_p_any": {"comonotone_lower": float(p_any_como.mean()), "independent": float(p_any.mean()),
                                        "countermonotone_upper": float(p_any_counter.mean())},
            "per_draw_sd": float(p_any.std()),
            "per_draw_p10_p90": [float(v) for v in np.percentile(p_any, [10, 90])],
        },
        "by_jurisdiction_headline": {
            "US_S4_AI_capital_capture_or_neglect": summary["US"]["p_s4"],
            "US_structural_range": [float(min(svU)), float(max(svU))],
            "China_S4_party_state_repression": summary["China"]["p_s4"],
            "China_structural_range": [float(min(svC)), float(max(svC))],
            "mechanism_increment_any": float(p_any.mean() - p_any_cf.mean()),
            "mechanism_increment_US": summary["US"]["mechanism_increment"],
            "mechanism_increment_China": summary["China"]["mechanism_increment"],
            "note": ("China's S4 is mostly pre-existing autocratic inertia (see counterfactual), not the scenario text's AI-rentier story. "
                     "Pass S5/S6 the per-jurisdiction probabilities and the mechanism increment, not only the combined number."),
        },
        "timeline": {
            "p10_year": float(p10), "median_year": float(p50), "p90_year": float(p90),
            "definition": "Calendar year of the first S4 among US/China (strict lock-in year, or first year claims had been unmet >=3 consecutive years, provisional), conditional on S4. T2 aligned to the S2 model's S2a onset distribution.",
            "US_only_p10_p50_p90": [float(v) for v in np.percentile(yU_ok, [10, 50, 90])] if len(yU_ok) else None,
            "offset_from_S2_midpoint_years": {"p10": float(np.percentile(offs, 10)), "median": float(np.percentile(offs, 50)),
                                              "p90": float(np.percentile(offs, 90))},
            "S2_midpoint_prior": {"p10": float(np.percentile(g0["T2"], 10)), "median": float(np.median(g0["T2"])),
                                  "p90": float(np.percentile(g0["T2"], 90))},
            "integrator_note": "Re-time with the S2 model's own onset draws using the exported offsets if the S2 distribution changes.",
        },
        "by_jurisdiction": summary,
        "world_population_weighted": {"mean": float(p_world.mean()), "mc_ci": [w_lo, w_hi], "weights": world_w},
        "structural_variants_4000x8": struct,
        "scenarios_4000x8": scen,
        "cumulative_p_s4_by_year": {"years": YEARS.tolist(), **cum, "any_US_or_China": cum_any},
        "counterfactual_note": "Counterfactual sets coercion automation a=0 and AI revenue share at today's level (dependence on labor stays full); common random numbers with the main run.",
        "convergence": {"n_draws": N_DRAWS, "paths_per_draw": M_PATHS, "headline_mc_halfwidth": float(halfw),
                        "running_mean_checkpoints": checkpoints},
        "sensitivity_spearman_US": sens_US,
        "sensitivity_spearman_China": sens_CN,
        "implied_coercion_automation_2035_leading_state": {"p10": float(np.percentile(a2035, 10)),
                                                           "median": float(np.median(a2035)),
                                                           "p90": float(np.percentile(a2035, 90))},
        "quantities_for_other_stages": {
            "p_S4_US": summary["US"]["p_s4"],
            "p_S4_China_party_state_repression": summary["China"]["p_s4"],
            "p_S4_any_independent": float(p_any.mean()),
            "p_S4_any_structural_range": [float(min(sv)), float(max(sv))],
            "mechanism_increment_any": float(p_any.mean() - p_any_cf.mean()),
            "p_strict_repression_US": summary["US"]["p_s4_strict_repression_lockin"],
            "p_strict_repression_China": summary["China"]["p_s4_strict_repression_lockin"],
            "p_adequate_redistribution_US": summary["US"]["p_adequate_redistribution_at_horizon"],
            "p_adequate_redistribution_China": summary["China"]["p_adequate_redistribution_at_horizon"],
            "p_overthrow_to_democracy_US": summary["US"]["p_overthrow_to_democracy"],
            "median_coercion_automation_at_strict_US": summary["US"]["median_coercion_automation_at_strict"],
            "median_coercion_automation_at_strict_China": summary["China"]["median_coercion_automation_at_strict"],
            "note_for_S5_S6": "Broad S4 includes populist redirection and neglect, not only violent repression. Only strict S4 implies the state has actively crushed unrest. China's number is party-state repression, not AI-capital capture.",
        },
        "samples": {
            "note": "5000-draw subsample; per-draw probabilities over 16 paths; year = per-draw median first-S4 year (NaN if none).",
            "p_any_US_or_China": np.round(p_any[sub], 4).tolist(),
            "p_US": np.round(pU[sub], 4).tolist(),
            "p_China": np.round(pC[sub], 4).tolist(),
            "year": [None if np.isnan(v) else round(float(v), 2) for v in med_year_draw[sub]],
            "S2_midpoint_year": np.round(g0["T2"][sub], 2).tolist(),
        },
        "priors": PRIOR_DOC,
        "seed": SEED,
    }
    result["runtime_s"] = round(time.time() - t0, 1)
    with open(RES, "w") as f:
        json.dump(result, f, indent=1)

    # ---------------- Figures ----------------
    colors = {"liberal_democracy": "#2a6fdb", "electoral_democracy": "#6aa84f", "autocracy": "#c0392b",
              "US": "#1b2a49", "China": "#e67e22"}
    fig, ax = plt.subplots(1, 2, figsize=(13, 5))
    for name in REGIMES:
        ax[0].plot(YEARS, cum[name], label=name.replace("_", " "), color=colors[name], lw=2)
    ax[0].plot(YEARS, cum_any, label="US or China", color="k", ls="--", lw=2)
    ax[0].set_title("Cumulative P(S4 by year | S1-S3), broad definition")
    ax[0].set_xlabel("year"); ax[0].set_ylabel("probability"); ax[0].set_ylim(0, 1); ax[0].grid(alpha=0.3)
    ax[0].legend(fontsize=8, frameon=False)
    names = list(REGIMES); x = np.arange(len(names))
    ps = [summary[k]["p_s4"] for k in names]; pc = [summary[k]["p_s4_counterfactual_no_automation_no_rentier"] for k in names]
    pst = [summary[k]["p_s4_strict_repression_lockin"] for k in names]
    ax[1].bar(x - 0.27, ps, 0.27, color=[colors[k] for k in names], label="broad S4, mechanisms on")
    ax[1].bar(x, pc, 0.27, color=[colors[k] for k in names], alpha=0.35, label="broad S4, counterfactual a=0, r=today")
    ax[1].bar(x + 0.27, pst, 0.27, color="grey", label="strict repression lock-in")
    ax[1].set_xticks(x); ax[1].set_xticklabels([k.replace("_", "\n") for k in names], fontsize=8)
    ax[1].set_title("P(S4) by jurisdiction"); ax[1].set_ylim(0, 1); ax[1].grid(alpha=0.3, axis="y")
    ax[1].legend(fontsize=8, frameon=False)
    plt.tight_layout(); plt.savefig(FIG1, dpi=130); plt.close()

    fig, ax = plt.subplots(1, 3, figsize=(18, 5.5))
    items = sorted(struct.items(), key=lambda kv: kv[1]["p_any"])
    ax[0].barh([k for k, _ in items], [v["p_any"] for _, v in items], color="#555")
    ax[0].barh([k for k, _ in items], [v["p_US"] for _, v in items], color="#1b2a49", height=0.4)
    ax[0].axvline(p_any.mean(), color="k", ls="--", lw=1)
    ax[0].set_title("Structural variants: P(US or China) grey, P(US) navy"); ax[0].set_xlim(0, 1)
    ax[0].tick_params(axis="y", labelsize=7); ax[0].grid(alpha=0.3, axis="x")
    for axi, (ttl, s) in zip(ax[1:], [("Spearman rho, per-draw P(US)", sens_US), ("Spearman rho, per-draw P(China)", sens_CN)]):
        it = list(s.items())[::-1]
        axi.barh([i[0] for i in it], [i[1] for i in it], color=["#c0392b" if i[1] > 0 else "#2a6fdb" for i in it])
        axi.set_title(ttl); axi.grid(alpha=0.3, axis="x"); axi.tick_params(axis="y", labelsize=8)
    plt.tight_layout(); plt.savefig(FIG2, dpi=130); plt.close()

    print(f"Runtime {result['runtime_s']}s")
    print(f"HEADLINE P(S4 US or China) = {p_any.mean():.3f} MC[{any_lo:.3f},{any_hi:.3f}] structural [{min(sv):.3f},{max(sv):.3f}]  CF {p_any_cf.mean():.3f}")
    print(f"  bounds como {p_any_como.mean():.3f} counter {p_any_counter.mean():.3f}")
    print(f"Timeline p10 {p10:.1f} med {p50:.1f} p90 {p90:.1f}")
    for k in REGIMES:
        s = summary[k]
        print(k, {kk: (round(vv, 3) if isinstance(vv, float) else vv) for kk, vv in s.items() if kk not in ("mc_ci",)})
    for k, v in struct.items():
        print(f"  struct {k:32s} " + " ".join(f"{a}={b:.3f}" for a, b in v.items()))
    for k, v in scen.items():
        print(f"  scen   {k:32s} " + " ".join(f"{a}={b:.3f}" for a, b in v.items()))
    print("sens US", {k: round(v, 3) for k, v in sens_US.items()})
    print("sens CN", {k: round(v, 3) for k, v in sens_CN.items()})
    print("a2035", result["implied_coercion_automation_2035_leading_state"])


if __name__ == "__main__":
    main()
