"""
S3 Provider concentration model (v2, after review).

Question: GIVEN S1 (automation race: firms broadly depend on AI providers for
automated professional work) AND S2 (the "no customers" domino: aggregate demand
contracts in cascades as professional categories are automated), what is the
probability that AI providers (model labs + compute layer) capture a MAJORITY of
the automation surplus, sustained for >= 2 consecutive years, and when?

Event: K_t = provider rent / automation surplus.
  Units: everything per automated task, as a fraction of the 2026 wage for that task.
    q_t   market price of compute per task (declines c_decl per year)
    chip  = q_t * chip_share * chip_gm_t          (compute-layer rent)
    r_t   = q_t - chip                             (true resource cost)
    w_t   = 1 - omega_w * D_t                      (human outside option; S2 bids wages down)
    m_t   = model-layer markup over market compute cost (endogenous, below)
    p_t   = q_t + m_t                              (price the customer pays = AI spend)
    W_t   = w_t - r_t                              (automation surplus)
    K_t   = (m_t + chip) / W_t
  Consistency: m_t <= S*kappa*(w_t - q_t) <= w_t - q_t, so rent <= spend <= wage by construction.
  S3 occurs in year t if K_t >= 0.5 and K_{t-1} >= 0.5. Horizon 2027-2045.

Markup:
  Frontier-only tasks (fraction f_F = 1 - exp(-L/tau), less self-supply):
      m_F = phi_t * S(theta) * kappa * (w - q)
      S(theta) = share of monopoly profit implied by conduct theta.
        base: linear-demand conduct mapping 4 theta/(1+theta)^2 (Cournot at theta=1/N)
        variant: S = theta (strong-substitution differentiated Bertrand, lower bound)
      theta = N_eff^(-a) (a in [0.5,1]; theta=1 at monopoly) unless in a collusive regime.
      kappa = share of surplus above cost a monopolist extracts (limit price <= wage);
        three specs: demand-curvature derived / judgement Beta / buyer bargaining.
  Open-doable tasks: lock-in premium over the open fringe (priced at compute cost):
      m_O = phi_t * pi_t * q_t, pi_t = switching cost x status-quo multiplier x agentic
      lock-in growth x regulation; capped at kappa*(w - q).
  phi_t: 1 in the static-equilibrium spec; in the "penetration pricing" spec
      providers start below equilibrium (phi0) and converge (the scenario text's claim).

Calibration: importance weights (ABC-style likelihood) on 2027 observables:
  frontier-lab gross margin m/p ~ N(0.5, 0.08) (research: 0.4-0.6),
  AI spend per displaced task p ~ lognormal(median 0.10, 90% 0.03-0.3) (judgement).

Dynamics:
  log N_eff: OU towards log N_inf (median 3.5, 2-6) with entry (China, Meta, xAI,
      sovereign labs), minus exits under S2 demand collapse.
  log open lag L: OU towards log L_inf (median 6, 3-12 months) while open releases
      continue; if all major open releasers stop (US and China), L grows 12 mo/yr until
      reopening.
  tau (value time-scale of capability progress) drifts log-linearly with a symmetric
      prior: acceleration (tau falls) vs saturation (tau rises).
  Collusion: Markov regime. Feasible if per-period delta >= 1 - 1/N_coll (N_coll includes
      open fringe and non-US frontier labs); entry hazard falls with N_coll and early tech
      turbulence; persistent until break; Green-Porter price wars a fraction of the time.
  Self-supply: large buyers integrate / distil when frontier Lerner index is high.
  Regulation: baseline behavioural rules (EU Data Act, DMA) cut lock-in from 2027;
      enforcement hazard once K is salient, reduced by capture (rentier logic under S2),
      remedies (structural with small probability) after lognormal lag; repeatable.
  Shared "capability speed" latent z correlates S2 timing/severity with lower N_inf,
      faster tau decline and longer open lag.

Uncertainty reported: Monte Carlo CI (noise only) AND a structural band across
model variants (conduct mapping x kappa spec x pricing spec x period length x
correlation), with an equal-weight central value.
"""
import itertools
import json
import os

import numpy as np
from scipy import stats
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEED = 20260930
N_DRAWS = 40000
N_VAR = 20000
YEARS = np.arange(2027, 2046)
NY = len(YEARS)
T0 = 2026
THRESH = 0.5

PRIORS_DOC = {
    "z_speed": "N(0,1) shared capability-speed latent; Gaussian copula rho=0.5 (base) with T2 (earlier), D_max (higher), N_inf (lower), g_tau (more negative), L_inf (longer).",
    "hhi_2026": "Triangular(2200, 2800, 3500). Menlo Ventures 2025 enterprise LLM API share (Anthropic ~40, OpenAI ~27, Google ~21).",
    "N_inf": "Lognormal median 4.0 (HHI 2500), 90% 2.3-7: long-run effective number of frontier suppliers (entry from China, Meta, xAI, sovereign labs vs 2.4x/yr training cost growth, Cottier et al. 2024).",
    "k_N": "Uniform(0.1, 0.3)/yr: OU reversion speed of log N_eff.",
    "beta_exit": "Uniform(0, 0.6): reduction of log N_inf per unit demand collapse D (revenue base shrinks under S2).",
    "lag0": "Lognormal median 4 months, 90% 3-7 (Epoch AI open-closed ECI gap).",
    "L_inf": "Lognormal median 6, 90% 3-12 months: long-run open-weight lag while releases continue (research: 2030 median 6; observed flat 3-4 months 2023-2026).",
    "k_L": "Uniform(0.15, 0.5)/yr: OU reversion speed of log lag.",
    "lag_sigma": "Uniform(0.1, 0.25)/yr log-lag noise.",
    "h_close": "Beta(mean 0.03, sd 0.02)/yr: hazard that ALL major open releasers stop near-frontier releases (needs US labs and Chinese labs, for whom open release is a geopolitical strategy).",
    "h_reopen": "Uniform(0.05, 0.3)/yr: reopening hazard (other jurisdiction, new entrant, DeepSeek-type shock).",
    "tau0": "Lognormal median 10 months, 90% 4-30: e-folding time scale of economic value of recent capability progress.",
    "g_tau": "Normal(0, 0.07)/yr drift of log tau: symmetric between acceleration (frontier months worth more) and saturation (commodity models do professional work).",
    "a_cond": "Uniform(0.5, 1.0): theta = N_eff^-a (a=1 homogeneous Cournot; lower = differentiation softens competition). theta=1 at monopoly.",
    "delta_annual": "Beta(mean 0.85, sd 0.06): providers' annual discount factor; per-period delta = delta^(1/periods), periods=4 (quarterly price adjustment) in base.",
    "n_out": "Uniform(1, 4): additional effective players in the collusion game outside N_eff (Chinese frontier labs, open fringe); halved while open releases are stopped.",
    "h_coll0": "Uniform(0.02, 0.2)/yr: hazard of entering a tacit-collusion regime at N_coll=2 when feasible; scaled exp(-0.3 (N_coll-2)) and by early tech turbulence (judgement; no documented tacit collusion in fast-moving software markets).",
    "tech_uncert": "Uniform(0.3, 0.8): early tech-turbulence reduction of collusion entry hazard, decays with 8y time constant.",
    "p_break": "Uniform(0.05, 0.25)/yr: exogenous breakdown of a collusive regime (new entrant, capability leap, defection).",
    "war_frac": "Uniform(0.1, 0.4): Green-Porter fraction of time in price wars within a collusive regime.",
    "theta_coll": "Uniform(0.5, 1.0): conduct within the collusive regime (mapped through S(theta)).",
    "kappa_curv": "spec 'curvature' (base): task-value demand q=(1-x)^s, s~Lognormal(1, 0.3-3) gives single-price monopoly share of realised surplus (1+s)/(1+2s); plus price discrimination disc~U(0,0.5) of the remainder; minus buyer power bp~U(0,0.3). Limit price bounded by wage.",
    "kappa_judg": "spec 'judgement': Beta(mean 0.6, sd 0.12) (v1 prior).",
    "kappa_barg": "spec 'bargaining': Beta(mean 0.4, sd 0.12): Nash bargaining with large enterprise buyers who can threaten to self-supply.",
    "kappa_limit": "spec 'limit' (high end): Beta(mean 0.85, sd 0.07): provider limit-prices just below the (falling) wage with near-perfect discrimination via per-seat / per-outcome enterprise contracts; the only outside option is human labour.",
    "eps_D": "Uniform(0, 0.3): reduction of kappa per unit D (customer-viability constraint: squeezing failing customers kills demand).",
    "omega_w": "Uniform(0.2, 0.8): wage fall per unit D (displaced workers bid wages down, lowering the price cap).",
    "sw0": "Lognormal median 0.10, 90% 0.02-0.4: switching cost as fraction of spend (Dataiku: 55% switched; 81% use 3+ families).",
    "lambda_sq": "Uniform(1.5, 2.5): loss-aversion / status-quo multiplier on switching cost.",
    "g_lock": "Uniform(0.0, 0.15)/yr: growth of lock-in from agentic memory, workflows, proprietary data.",
    "reg0": "Uniform(0, 0.25): baseline behavioural regulation cut to lock-in from 2027 (EU Data Act egress ban, DMA; EU ~20% of market).",
    "sigma_max": "Uniform(0.0, 0.3): max share of frontier-task demand that buyers self-supply (large enterprises distilling from frontier outputs or training own models; hyperscalers already counted in N_eff). Frontier-only tasks by definition exceed open capability, so self-supply is limited.",
    "rho_self": "Uniform(0.2, 0.6): frontier Lerner index at which self-supply reaches 63% of its max.",
    "q0": "Lognormal median 0.05, 90% 0.015-0.17: market compute cost per automated task in 2027 as fraction of wage (judgement; calibrated jointly with markup to spend/margin observables).",
    "c_decl": "Uniform(0.7, 1.0)/yr: decline of compute cost per task (40x/yr at fixed capability offset by agentic token growth and frontier-tier pricing; research frontier-tier price trend -15%/yr, -60% to +50%).",
    "chip_share": "Uniform(0.35, 0.6): chip share of compute cost.",
    "chip_margin_2026": "Uniform(0.6, 0.78): Nvidia gross margin (filings ~0.74).",
    "chip_margin_2032": "Uniform(0.4, 0.75): accelerator margin after custom-ASIC ramp.",
    "phi0": "penetration spec only: Uniform(0.1, 1.0) ratio of 2027 markup to equilibrium markup; converges at k_phi~U(0.05, 0.3)/yr.",
    "vis_thresh": "Uniform(0.25, 0.4): capture share at which rent becomes salient.",
    "h_file0": "Beta(mean 0.15, sd 0.07)/yr: base hazard of suit / ex-ante rule once salient.",
    "chi0": "Beta(mean 0.35, sd 0.15): regulatory capture.",
    "eta_rentier": "Uniform(0, 0.8): extra capture per unit D as the state's tax base shifts to AI firms (S4 rentier logic).",
    "gamma_sal": "Uniform(0, 2): salience boost of enforcement per unit D.",
    "remedy_lag": "Lognormal median 6y, 90% 3-12 (US suit-to-remedy ~8y; EU faster).",
    "p_struct": "Beta(mean 0.1, sd 0.06): P(structural remedy | remedy) (AT&T yes; Microsoft, Google no).",
    "b_behav": "Uniform(0.2, 0.6): behavioural remedy cut to lock-in and collusion entry.",
    "T2": "Triangular(2028, 2032, 2040): S2 demand-collapse onset (conditioning; copula-linked to z).",
    "D_max": "Beta(mean 0.35, sd 0.12): peak fraction of aggregate demand lost under S2 (copula-linked to z).",
    "D_width": "Uniform(1.5, 4) years: logistic width of cascade (B2C first, B2B lag).",
    "calibration": "Importance weights: gross margin 2027 ~ N(0.5, 0.08); spend p_2027 ~ lognormal(median 0.10, sd ln(3)/1.645).",
}


def beta_ms_ppf(u, mean, sd):
    v = mean * (1 - mean) / sd**2 - 1
    return stats.beta.ppf(u, mean * v, (1 - mean) * v)


def lognorm_ppf(u, median, p95):
    sig = np.log(p95 / median) / 1.645
    return median * np.exp(sig * stats.norm.ppf(u))


def tri_ppf(u, a, c, b):
    return stats.triang.ppf(u, (c - a) / (b - a), loc=a, scale=b - a)


def draw_params(rng, n, rho=0.5):
    U = lambda: rng.random(n)
    p = {}
    z = rng.standard_normal(n)
    p["z_speed"] = z

    def cop(sign):  # uniform correlated with z
        return stats.norm.cdf(sign * rho * z + np.sqrt(1 - rho**2) * rng.standard_normal(n))

    p["hhi_2026"] = rng.triangular(2200, 2800, 3500, n)
    p["N_inf"] = lognorm_ppf(cop(-1), 4.0, 7.0)
    p["k_N"] = rng.uniform(0.1, 0.3, n)
    p["beta_exit"] = rng.uniform(0, 0.6, n)
    p["lag0"] = np.clip(lognorm_ppf(U(), 4.0, 7.0), 1.5, 12)
    p["L_inf"] = lognorm_ppf(cop(+1), 6.0, 12.0)
    p["k_L"] = rng.uniform(0.15, 0.5, n)
    p["lag_sigma"] = rng.uniform(0.1, 0.25, n)
    p["h_close"] = beta_ms_ppf(U(), 0.03, 0.02)
    p["h_reopen"] = rng.uniform(0.05, 0.3, n)
    p["tau0"] = lognorm_ppf(U(), 10.0, 30.0)
    p["g_tau"] = 0.07 * stats.norm.ppf(cop(-1))
    p["a_cond"] = rng.uniform(0.5, 1.0, n)
    p["delta_annual"] = beta_ms_ppf(U(), 0.85, 0.06)
    p["n_out"] = rng.uniform(1, 4, n)
    p["h_coll0"] = rng.uniform(0.02, 0.2, n)
    p["tech_uncert"] = rng.uniform(0.3, 0.8, n)
    p["p_break"] = rng.uniform(0.05, 0.25, n)
    p["war_frac"] = rng.uniform(0.1, 0.4, n)
    p["theta_coll"] = rng.uniform(0.5, 1.0, n)
    # kappa specs (all drawn, spec chosen at simulate time)
    s = lognorm_ppf(U(), 1.0, 3.0)
    ks = (1 + s) / (1 + 2 * s)
    ks = ks + (1 - ks) * rng.uniform(0, 0.5, n)
    p["kappa_curv"] = ks * (1 - rng.uniform(0, 0.3, n))
    p["kappa_judg"] = beta_ms_ppf(U(), 0.6, 0.12)
    p["kappa_barg"] = beta_ms_ppf(U(), 0.4, 0.12)
    p["kappa_limit"] = beta_ms_ppf(U(), 0.85, 0.07)
    p["eps_D"] = rng.uniform(0, 0.3, n)
    p["omega_w"] = rng.uniform(0.2, 0.8, n)
    p["sw0"] = np.clip(lognorm_ppf(U(), 0.10, 0.4), 0.01, 0.8)
    p["lambda_sq"] = rng.uniform(1.5, 2.5, n)
    p["g_lock"] = rng.uniform(0.0, 0.15, n)
    p["reg0"] = rng.uniform(0, 0.25, n)
    p["sigma_max"] = rng.uniform(0.0, 0.3, n)
    p["rho_self"] = rng.uniform(0.2, 0.6, n)
    p["q0"] = np.clip(lognorm_ppf(U(), 0.05, 0.17), 0.005, 0.6)
    p["c_decl"] = rng.uniform(0.7, 1.0, n)
    p["chip_share"] = rng.uniform(0.35, 0.6, n)
    p["chip_margin_2026"] = rng.uniform(0.6, 0.78, n)
    p["chip_margin_2032"] = rng.uniform(0.4, 0.75, n)
    p["phi0"] = rng.uniform(0.1, 1.0, n)
    p["k_phi"] = rng.uniform(0.05, 0.3, n)
    p["vis_thresh"] = rng.uniform(0.25, 0.4, n)
    p["h_file0"] = beta_ms_ppf(U(), 0.15, 0.07)
    p["chi0"] = beta_ms_ppf(U(), 0.35, 0.15)
    p["eta_rentier"] = rng.uniform(0, 0.8, n)
    p["gamma_sal"] = rng.uniform(0, 2, n)
    p["remedy_lag"] = np.clip(lognorm_ppf(U(), 6.0, 12.0), 1, 20)
    p["p_struct"] = beta_ms_ppf(U(), 0.1, 0.06)
    p["b_behav"] = rng.uniform(0.2, 0.6, n)
    p["T2"] = tri_ppf(cop(-1), 2028, 2032, 2040)
    p["D_max"] = beta_ms_ppf(cop(+1), 0.35, 0.12)
    p["D_width"] = rng.uniform(1.5, 4.0, n)
    return p


def draw_noise(rng, n):
    """Common random numbers for all scenarios / variants."""
    return {k: rng.random((n, NY)) for k in
            ["close", "reopen", "coll_in", "coll_out", "file", "struct"]} | \
           {"eN": rng.standard_normal((n, NY)), "eL": rng.standard_normal((n, NY))}


def share(theta, mapping):
    if mapping == "cournot":
        return 4 * theta / (1 + theta) ** 2
    return theta


BASE_SPEC = dict(mapping="cournot", kappa="curv", pricing="static", periods=4, lag="ou")


def simulate(p, e, n, spec=None, s2=True, antitrust=True, force_open=None, force_closed=False,
             compute_shock=None):
    spec = {**BASE_SPEC, **(spec or {})}
    kap0 = p["kappa_" + spec["kappa"]]
    logN = np.log(10000.0 / p["hhi_2026"])
    L = p["lag0"].copy()
    open_on = np.ones(n, bool) & (not force_closed)
    coll = np.zeros(n, bool)
    filed = np.zeros(n, bool)
    remedy_year = np.full(n, np.inf)
    n_rem = np.zeros(n)
    lock_cut = np.ones(n)
    coll_cut = np.ones(n)
    out = {k: np.zeros((n, NY)) for k in ["K", "N", "L", "D", "coll", "p", "gm", "m", "fF", "chip"]}
    delta_p = p["delta_annual"] ** (1.0 / spec["periods"])
    for j, yr in enumerate(YEARS):
        t = yr - T0
        D = p["D_max"] / (1 + np.exp(-(yr - p["T2"]) / p["D_width"])) if s2 else np.zeros(n)
        # --- effective frontier firms: OU on log N ---
        target = np.log(p["N_inf"]) - p["beta_exit"] * D
        logN = logN + p["k_N"] * (target - logN) + 0.06 * e["eN"][:, j]
        logN = np.clip(logN, 0.0, np.log(12.0))
        # --- remedies (repeatable) ---
        new_rem = antitrust & (yr >= remedy_year)
        if new_rem.any():
            struct = new_rem & (e["struct"][:, j] < p["p_struct"])
            logN = np.where(struct, np.minimum(logN + np.log(2), np.log(12.0)), logN)
            lock_cut = np.where(new_rem, lock_cut * (1 - p["b_behav"]), lock_cut)
            coll_cut = np.where(new_rem & ~struct, coll_cut * (1 - p["b_behav"]), coll_cut)
            coll = coll & ~new_rem  # remedy breaks an existing regime
            n_rem += new_rem
            filed = filed & ~new_rem
            remedy_year = np.where(new_rem, np.inf, remedy_year)
        N = np.exp(logN)
        # --- open-weight regime and lag ---
        if force_open is not None:
            L = np.full(n, float(force_open))
        else:
            if not force_closed:
                close = open_on & (e["close"][:, j] < p["h_close"])
                reopen = (~open_on) & (e["reopen"][:, j] < p["h_reopen"])
                open_on = (open_on & ~close) | reopen
                L = np.where(reopen, p["L_inf"], L)
            lL = np.log(np.maximum(L, 0.5))
            if spec["lag"] == "ou":
                lL_new = lL + p["k_L"] * (np.log(p["L_inf"]) - lL) + p["lag_sigma"] * e["eL"][:, j]
            else:  # v1 random walk with drift (rejected; reference only)
                lL_new = lL + np.log(1.5) / 4 + p["lag_sigma"] * e["eL"][:, j]
            L = np.where(open_on, np.exp(lL_new), L + 12.0)
            L = np.clip(L, 0.5, 240)
        tau = p["tau0"] * np.exp(p["g_tau"] * t)
        fF = 1 - np.exp(-L / tau)
        # --- conduct ---
        theta_c = N ** (-p["a_cond"])
        n_coll = N + p["n_out"] * np.where(open_on, 1.0, 0.5)
        feasible = delta_p >= 1 - 1 / n_coll
        h_in = p["h_coll0"] * np.exp(-0.3 * (n_coll - 2)) * (1 - p["tech_uncert"] * np.exp(-t / 8.0)) * coll_cut
        enter = (~coll) & feasible & (e["coll_in"][:, j] < h_in) & (j > 0)
        brk = coll & ((~feasible) | (e["coll_out"][:, j] < p["p_break"]))
        coll = (coll | enter) & ~brk
        th_coll = np.maximum(p["theta_coll"], theta_c)
        S_comp = share(theta_c, spec["mapping"])
        S_coll = (1 - p["war_frac"]) * share(th_coll, spec["mapping"]) + p["war_frac"] * S_comp
        S = np.where(coll, S_coll, S_comp)
        # --- prices ---
        q = p["q0"] * p["c_decl"] ** (t - 1)
        wgt = np.clip(t / 6.0, 0, 1)
        gm_chip = (1 - wgt) * p["chip_margin_2026"] + wgt * p["chip_margin_2032"]
        if compute_shock is not None:
            k = np.where(yr >= compute_shock, np.exp(-(yr - compute_shock) / 3.0), 0.0)
            q = q * (1 + 2.0 * k)
            gm_chip = gm_chip + (0.88 - gm_chip) * k
        chip = q * p["chip_share"] * gm_chip
        r = q - chip
        w = 1 - p["omega_w"] * D
        head = np.maximum(w - q, 0.0)
        kappa = kap0 * (1 - p["eps_D"] * D)
        phi = 1.0 if spec["pricing"] == "static" else 1 - (1 - p["phi0"]) * np.exp(-p["k_phi"] * (t - 1))
        mF_eq = S * kappa * head
        lerner = mF_eq / np.maximum(q + mF_eq, 1e-9)
        sig_self = p["sigma_max"] * (1 - np.exp(-lerner / p["rho_self"]))
        fF_eff = fF * (1 - sig_self)
        pi = p["sw0"] * p["lambda_sq"] * np.exp(p["g_lock"] * t) * lock_cut * (1 - p["reg0"])
        mO = np.minimum(pi * q, kappa * head)
        m = phi * (fF_eff * mF_eq + (1 - fF_eff) * mO)
        price = q + m
        W = np.maximum(w - r, 1e-6)
        K = np.clip((m + chip) / W, 0, 1)
        for k_, v_ in (("K", K), ("N", N), ("L", L), ("D", D), ("coll", coll), ("p", price),
                       ("gm", m / price), ("m", m), ("fF", fF_eff), ("chip", chip)):
            out[k_][:, j] = v_
        if antitrust:
            chi = p["chi0"] + (1 - p["chi0"]) * p["eta_rentier"] * D
            h_file = np.clip(p["h_file0"] * (1 + p["gamma_sal"] * D) * (1 - chi), 0, 1)
            newf = (~filed) & (K > p["vis_thresh"]) & (e["file"][:, j] < h_file)
            remedy_year = np.where(newf, yr + np.maximum(1, np.round(p["remedy_lag"])), remedy_year)
            filed |= newf
    ok = out["K"] >= THRESH
    sus = ok[:, 1:] & ok[:, :-1]
    has = sus.any(1)
    out["year"] = np.where(has, YEARS[1:][np.argmax(sus, 1)], np.nan)
    out["n_rem"] = n_rem
    return out


def calib_weights(r):
    gm, pr = r["gm"][:, 0], r["p"][:, 0]
    lw = -0.5 * ((gm - 0.5) / 0.08) ** 2 - 0.5 * ((np.log(pr) - np.log(0.10)) / (np.log(3) / 1.645)) ** 2
    w = np.exp(lw - lw.max())
    return w / w.sum()


def wmean(x, w):
    return float(np.sum(w * x))


def wquant(x, w, qs):
    o = np.argsort(x)
    cw = np.cumsum(w[o])
    cw /= cw[-1]
    return [float(np.interp(q / 100, cw, x[o])) for q in qs]


def summarize(r, w):
    ev = ~np.isnan(r["year"])
    return {"p_by_2045": wmean(ev, w), "p_by_2035": wmean(r["year"] <= 2035, w),
            "median_year_if_occurs": (wquant(r["year"][ev], w[ev], [50])[0] if ev.any() else None),
            "cum": [wmean(r["year"] <= y, w) for y in YEARS]}


def main():
    rng = np.random.default_rng(SEED)
    p = draw_params(rng, N_DRAWS)
    e = draw_noise(np.random.default_rng(SEED + 1), N_DRAWS)
    base = simulate(p, e, N_DRAWS)
    w = calib_weights(base)
    ess = float(1 / np.sum(w**2))
    ev = ~np.isnan(base["year"])
    evf = ev.astype(float)
    mean = wmean(evf, w)
    # weighted bootstrap (Monte Carlo noise only)
    brng = np.random.default_rng(SEED + 2)
    bs = []
    for _ in range(1000):
        idx = brng.integers(0, N_DRAWS, N_DRAWS)
        bs.append(np.sum(w[idx] * evf[idx]) / np.sum(w[idx]))
    mc_lo, mc_hi = (float(v) for v in np.percentile(bs, [2.5, 97.5]))

    yrs = base["year"][ev]
    p10, p50, p90 = wquant(yrs, w[ev], [10, 50, 90])
    cum = {int(y): wmean(base["year"] <= y, w) for y in YEARS}
    K = base["K"]
    Kq = {int(y): wquant(K[:, j], w, [10, 50, 90]) for j, y in enumerate(YEARS)}
    jy = {int(y): j for j, y in enumerate(YEARS)}

    # ---------------- structural variants ----------------
    pv = {k: v[:N_VAR] for k, v in p.items()}
    ev_ = {k: v[:N_VAR] for k, v in e.items()}
    p_nocorr = draw_params(np.random.default_rng(SEED), N_VAR, rho=0.0)
    variants = []
    grid = list(itertools.product(["cournot", "theta"], ["curv", "judg", "barg", "limit"],
                                  ["static", "penetration"], [4, 1], [0.5, 0.0]))
    for mp, kp, pr, per, rho in grid:
        spec = dict(mapping=mp, kappa=kp, pricing=pr, periods=per)
        pp = pv if rho > 0 else p_nocorr
        rv = simulate(pp, ev_, N_VAR, spec=spec)
        wv = calib_weights(rv)
        evv = ~np.isnan(rv["year"])
        variants.append({"mapping": mp, "kappa": kp, "pricing": pr, "periods_per_year": per, "copula_rho": rho,
                         "p_by_2045": wmean(evv, wv), "p_by_2035": wmean(rv["year"] <= 2035, wv),
                         "K2027_median": wquant(rv["K"][:, 0], wv, [50])[0],
                         "K2035_median": wquant(rv["K"][:, jy[2035]], wv, [50])[0],
                         "ess": float(1 / np.sum(wv**2))})
        print(f"  variant {mp:7s} {kp:4s} {pr:11s} per{per} rho{rho}: P={variants[-1]['p_by_2045']:.3f} "
              f"P35={variants[-1]['p_by_2035']:.3f} K27={variants[-1]['K2027_median']:.3f} ess={variants[-1]['ess']:.0f}")
    vp = np.array([v["p_by_2045"] for v in variants])
    vp35 = np.array([v["p_by_2035"] for v in variants])
    struct = {"central_equal_weight": float(vp.mean()), "min": float(vp.min()), "max": float(vp.max()),
              "p10_across_variants": float(np.percentile(vp, 10)), "p90_across_variants": float(np.percentile(vp, 90)),
              "by2035_central": float(vp35.mean()), "by2035_min": float(vp35.min()), "by2035_max": float(vp35.max()),
              "n_variants": len(variants)}
    for dim in ["mapping", "kappa", "pricing", "periods_per_year", "copula_rho"]:
        struct[f"mean_by_{dim}"] = {str(k): float(np.mean([v["p_by_2045"] for v in variants if v[dim] == k]))
                                    for k in sorted({v[dim] for v in variants}, key=str)}
    # rejected v1 random-walk lag, reference only
    rw = simulate(pv, ev_, N_VAR, spec=dict(lag="rw"))
    wrw = calib_weights(rw)
    struct["reference_v1_random_walk_lag_base_spec"] = wmean(~np.isnan(rw["year"]), wrw)

    # ---------------- scenarios (base spec, common random numbers) ----------------
    scen = {}

    def run(name, **kw):
        # counterfactual futures of the same calibrated world: reuse base 2027 weights
        r = simulate(p, e, N_DRAWS, **kw)
        scen[name] = summarize(r, w)
    run("base (S1+S2)")
    run("no S2 demand collapse (S1 only)", s2=False)
    run("no antitrust / regulation enforcement", antitrust=False)
    run("open-weight lag fixed at 3 months", force_open=3)
    run("open-weight lag fixed at 12 months", force_open=12)
    run("open-weight releases stop from 2027", force_closed=True)
    run("compute supply shock 2029 (e.g. Taiwan)", compute_shock=2029)
    r_pen = simulate(p, e, N_DRAWS, spec=dict(pricing="penetration"))
    scen["penetration pricing (raise-later) spec, own calibration"] = summarize(r_pen, calib_weights(r_pen))

    # ---------------- ablations: what moved P from v1 ----------------
    abl = {"base_spec_calibrated": mean, "base_spec_uncalibrated_prior": float(evf.mean())}
    def ablate(name, mod):
        pp = dict(p); pp.update(mod(pp))
        r = simulate(pp, e, N_DRAWS)
        abl[name] = wmean(~np.isnan(r["year"]), calib_weights(r))
    ablate("no_self_supply", lambda q_: {"sigma_max": np.zeros(N_DRAWS)})
    ablate("no_tau_drift", lambda q_: {"g_tau": np.zeros(N_DRAWS)})
    ablate("h_close_v1_mean_0.05", lambda q_: {"h_close": q_["h_close"] * 0.05 / 0.03})
    ablate("no_baseline_regulation", lambda q_: {"reg0": np.zeros(N_DRAWS)})
    ablate("collusion_entry_x3", lambda q_: {"h_coll0": np.minimum(q_["h_coll0"] * 3, 1)})
    ablate("kappa_curv_no_buyer_power_full_discrimination", lambda q_: {"kappa_curv": np.ones(N_DRAWS) * 0.95})
    ablate("wage_cap_off_omega_w_0", lambda q_: {"omega_w": np.zeros(N_DRAWS)})

    # ---------------- sensitivity (weighted quintiles) ----------------
    sens = []
    for k, v in p.items():
        q20, q80 = np.percentile(v, [20, 80])
        lo_m, hi_m = v <= q20, v >= q80
        plo = float(np.sum(w[lo_m] * evf[lo_m]) / np.sum(w[lo_m]))
        phi_ = float(np.sum(w[hi_m] * evf[hi_m]) / np.sum(w[hi_m]))
        sens.append({"param": k, "p_bottom_quintile": plo, "p_top_quintile": phi_, "delta": phi_ - plo})
    sens.sort(key=lambda d: -abs(d["delta"]))

    j27, j30, j32, j35, j45 = jy[2027], jy[2030], jy[2032], jy[2035], jy[2045]
    derived = {
        "calibration_ess": ess,
        "gross_margin_2027_weighted_median": wquant(base["gm"][:, j27], w, [50])[0],
        "spend_per_task_2027_weighted_median": wquant(base["p"][:, j27], w, [50])[0],
        "spend_per_task_2035_weighted_median": wquant(base["p"][:, j35], w, [50])[0],
        "frontier_price_change_per_yr_2027_2032_median": float(wquant((base["p"][:, j32] / base["p"][:, j27]) ** (1 / 5) - 1, w, [50])[0]),
        "rent_exceeds_spend_fraction_of_draw_years": float(np.mean(base["m"] + base["chip"] > base["p"] + 1e-12)),
        "mean_capture_share_2030": wmean(K[:, j30], w),
        "mean_capture_share_2035": wmean(K[:, j35], w),
        "mean_capture_share_2045": wmean(K[:, j45], w),
        "p_capture_ge_0.3_2035": wmean(K[:, j35] >= 0.3, w),
        "p_hhi_gt_2500_2032": wmean(10000 / base["N"][:, j32] > 2500, w),
        "p_neff_lt_1.5_2045": wmean(base["N"][:, j45] < 1.5, w),
        "p_open_lag_gt_12mo_2030": wmean(base["L"][:, j30] > 12, w),
        "median_open_lag_2030_months": wquant(base["L"][:, j30], w, [50])[0],
        "median_open_lag_2045_months": wquant(base["L"][:, j45], w, [50])[0],
        "p_lag_ever_gt_24mo": wmean((base["L"] > 24).any(1), w),
        "p_tacit_collusion_2035": wmean(base["coll"][:, j35], w),
        "p_any_remedy_by_2045": wmean(base["n_rem"] > 0, w),
        "share_of_events_after_2035": float(np.sum(w[ev] * (base["year"][ev] > 2035)) / np.sum(w[ev])),
        "p_event_during_open_closure_or_lag_gt_12": None,
    }
    if ev.any():
        idx = np.where(ev)[0]
        jj = np.searchsorted(YEARS, base["year"][idx].astype(int))
        derived["p_event_during_open_closure_or_lag_gt_12"] = float(
            np.sum(w[idx] * (base["L"][idx, jj] > 12)) / np.sum(w[idx]))
        derived["p_event_in_collusive_regime"] = float(np.sum(w[idx] * (base["coll"][idx, jj] > 0)) / np.sum(w[idx]))
    for th in (0.4, 0.6):
        ok = K >= th
        derived[f"p_capture_ge_{th}_sustained_by_2045"] = wmean((ok[:, 1:] & ok[:, :-1]).any(1), w)

    # posterior-resampled samples for integrator
    srng = np.random.default_rng(SEED + 3)
    thin = srng.choice(N_DRAWS, 5000, replace=True, p=w)
    out = {
        "stage": "S3 provider concentration",
        "version": 2,
        "stage_probability": {
            "mean": struct["central_equal_weight"],
            "ci_low": struct["min"], "ci_high": struct["max"],
            "definition": ("P(AI providers, model labs + chip layer, capture >= 50% of the automation surplus "
                           "for >= 2 consecutive years at some point 2027-2045 | S1 and S2 with onset ~Triangular(2028,2032,2040)). "
                           "Automation surplus = displaced labour cost (at the S2-depressed wage) minus true compute resource cost."),
            "ci_method": ("STRUCTURAL band: min-max of calibrated P across 64 model variants (conduct mapping x kappa spec x "
                          "pricing spec x period length x copula). Central = equal-weight mean of variants. "
                          "Not a statistical CI."),
            "base_spec_p": mean,
            "base_spec_monte_carlo_95ci": [mc_lo, mc_hi],
        },
        "structural_uncertainty": struct,
        "ablations_base_spec": abl,
        "variants": variants,
        "timeline": {"p10_year": p10, "median_year": p50, "p90_year": p90,
                     "definition": "base spec: second year of first 2-year window with K>=0.5, among draws where S3 occurs by 2045 (calibration-weighted); censored at 2045"},
        "cumulative_probability_by_year_base_spec": cum,
        "capture_share_quantiles_by_year_p10_p50_p90_base_spec": Kq,
        "scenarios": scen,
        "sensitivity_quintile": sens,
        "derived_for_other_stages": derived,
        "notes_for_integrator": [
            "Use stage_probability.mean (structural central) with ci_low/ci_high as a structural range, not a CI.",
            "Price and rent are now consistent: rent <= spend <= wage in every draw-year; calibrated to 2027 lab gross margin ~0.5 and spend ~0.1 of displaced wage.",
            "The biggest structural swing is pricing: static equilibrium vs penetration pricing (low now, raise later) which is the scenario text's own mechanism.",
            "S3 events concentrate in worlds where open-weight releases stop or collusion forms; S3 therefore anti-correlates with Alternative B (decentralised AI) viability.",
            "Enforcement is weakened by rentier capture that rises with demand collapse: link to S4.",
            "Post-2035 events are lower-confidence extrapolation (see derived.share_of_events_after_2035).",
        ],
        "n_draws": N_DRAWS, "n_draws_per_variant": N_VAR, "seed": SEED,
        "samples_posterior_resampled": {
            "event": ev[thin].astype(int).tolist(),
            "year": [None if np.isnan(y) else int(y) for y in base["year"][thin]],
            "capture_share_2035": np.round(K[thin, j35], 4).tolist()},
        "priors": PRIORS_DOC,
    }
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    with open(os.path.join(ROOT, "results", "m3_provider_concentration.json"), "w") as f:
        json.dump(out, f, indent=1)

    # ---------------- figures ----------------
    os.makedirs(os.path.join(ROOT, "figures"), exist_ok=True)
    fig, ax = plt.subplots(1, 3, figsize=(17, 4.8))
    for name, s in scen.items():
        ax[0].plot(YEARS, s["cum"], lw=2.2 if name.startswith("base") else 1.3,
                   color="black" if name.startswith("base") else None, label=f"{name} ({s['p_by_2045']:.2f})")
    ax[0].set_title("P(S3 by year), base spec, scenarios"); ax[0].set_ylabel("cumulative probability")
    ax[0].set_ylim(0, 1); ax[0].grid(alpha=.3); ax[0].legend(fontsize=6.5, loc="upper left")
    q = np.array([Kq[int(y)] for y in YEARS])
    ax[1].fill_between(YEARS, q[:, 0], q[:, 2], alpha=.25, label="p10-p90 (quantiles)")
    ax[1].plot(YEARS, q[:, 1], lw=2, label="median")
    ax[1].axhline(THRESH, ls="--", color="gray", label="S3 threshold")
    ax[1].set_title("Provider capture share K (base spec)"); ax[1].set_ylim(0, 1); ax[1].grid(alpha=.3)
    ax[1].legend(fontsize=8)
    order = np.argsort(vp)
    ax[2].barh(range(len(vp)), vp[order], color=["tab:red" if variants[i]["pricing"] == "penetration" else "tab:blue" for i in order])
    ax[2].axvline(struct["central_equal_weight"], color="black", ls="--", lw=1, label=f"central {struct['central_equal_weight']:.2f}")
    ax[2].set_yticks([]); ax[2].set_xlabel("P(S3 by 2045)")
    ax[2].set_title(f"{len(vp)} structural variants (red = penetration pricing)"); ax[2].legend(fontsize=8); ax[2].grid(alpha=.3, axis="x")
    fig.tight_layout()
    fig.savefig(os.path.join(ROOT, "figures", "m3_provider_concentration_timeline.png"), dpi=140)
    plt.close(fig)

    top = sens[:14][::-1]
    fig, ax = plt.subplots(figsize=(8, 5.5))
    for i, s in enumerate(top):
        ax.plot([s["p_bottom_quintile"], s["p_top_quintile"]], [i, i], color="gray", lw=1)
        ax.scatter(s["p_bottom_quintile"], i, color="tab:blue", zorder=3, label="bottom 20%" if i == 0 else None)
        ax.scatter(s["p_top_quintile"], i, color="tab:red", zorder=3, label="top 20%" if i == 0 else None)
    ax.axvline(mean, ls="--", color="black", lw=1)
    ax.set_yticks(range(len(top))); ax.set_yticklabels([s["param"] for s in top])
    ax.set_xlabel("P(S3 by 2045) within parameter quintile (base spec, calibrated)")
    ax.set_title("S3 sensitivity (quintile split)"); ax.legend(fontsize=8); ax.grid(alpha=.3, axis="x")
    fig.tight_layout()
    fig.savefig(os.path.join(ROOT, "figures", "m3_provider_concentration_sensitivity.png"), dpi=140)
    plt.close(fig)

    print(f"BASE spec P = {mean:.4f} MC95 [{mc_lo:.4f},{mc_hi:.4f}] ESS {ess:.0f}")
    print("STRUCT:", json.dumps({k: v for k, v in struct.items()}, indent=0))
    print("ABL:", json.dumps(abl, indent=0))
    print("K 2027/2030/2035:", Kq[2027], Kq[2030], Kq[2035])
    print(f"Timeline: p10 {p10:.0f} median {p50:.0f} p90 {p90:.0f}")
    for k, s in scen.items():
        print(f"  {k:42s} by2035 {s['p_by_2035']:.3f} by2045 {s['p_by_2045']:.3f} median {s['median_year_if_occurs']}")
    print("derived:", json.dumps(derived, indent=0))
    for s in sens[:10]:
        print(f"  {s['param']:18s} bottom {s['p_bottom_quintile']:.3f} top {s['p_top_quintile']:.3f}")


if __name__ == "__main__":
    main()
