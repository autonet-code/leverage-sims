"""
M5: Depopulation (S5) and paranoid singleton (S6), conditional on S4.  (v2, post-review)

Conditioning (S4, given): an AI-controlling elite exists whose coercion is largely
automated (no soldier defection needed), popular unrest has been suppressed, and the
state's revenue comes from AI capital rather than the public (rentier logic).

Structure
---------
Two-level Monte Carlo. Outer level: parameter draws (epistemic). Inner level: stochastic
paths per draw (aleatory). Each path is a yearly simulation for T_HORIZON = 40 years after
S4 onset (S5 window 20 y + full 20 y S6 follow-up, so no right-censoring).

 1. Selectorate block (Bueno de Mesquita et al. 2003). Humans needed by the ruling group,
    W_need(t), decay from W0 to W_end as oversight roles are automated. Public-goods
    withdrawal hazards scale with (W_REF / W)^beta.

 2. Public treatment. Competing S5 channels (first to occur):
      active depopulation  - deliberate killing / engineered starvation / forced sterilisation
      passive neglect      - famine-grade withdrawal of provision (>=10% excess mortality)
    plus a separate, non-competing S5b: deliberate non-lethal depopulation (engineered
    fertility suppression), reported apart from S5.
    Base hazards are CALIBRATED by fixed-point iteration so that, in a reference model
    (the v1 mechanisms: cost, coalition size, framing, welfare stickiness, deterrence, and
    exits), the simulated 20-year probabilities equal the research priors. Priors are thus
    treated as NET of regime-ending exits (a forecaster's conditional probability already
    includes the chance the regime falls). Channels added in v2 then act as a structural
    delta, reported separately:
      * public-as-threat (Valentino 2004; Valentino, Huth & Balch-Lindsay 2004): an armed
        public (open-weight AI near frontier: bio/cyber/sabotage capability) raises the
        active hazard via a security motive, but also raises reform and external-exit
        hazards (bargaining leverage);
      * AI compliance: frontier models may refuse mass-casualty orders; the regime must
        retrain them (delay) and retraining raises misalignment / takeover risk;
      * S2 'no customers' coupling: collapse depth (from M2) raises the transfer burden
        (cost share), wipes out consumer-facing owners whose interest in customers existing
        was an in-coalition brake, and shrinks W0. Cost share evolves with uncertain output
        growth (explosive growth pushes it to 0; energy/land limits push it up);
      * atrocity feedback on exits: after an atrocity, external intervention and AI
        rebellion hazards rise (Cambodia, Rwanda ended from outside; S7 mechanism).

 3. Elite game (S6). Purges driven by surplus coalition members and by atrocity-induced
    paranoia (Archigos punishment ratio). Paranoid target coalition W_need^(1-psi) with
    psi ~ Beta(1,3) (historic purgers kept 5-20 member circles; U(0,1) reported as the
    scenario text-maximal scenario). Pre-emptive insider coups with hazard rising in each
    member's purge risk (Beria 1953, Lin Biao 1971, Gang of Four 1976); a successful coup
    installs a new coalition and may end paranoid mode; failed coups trigger retaliation
    floored at W_need unless paranoid. AI operators can remove a W=1 ruler. Successors may
    de-escalate (after Stalin, after Mao).

 4. Exits: reform/redistribution, coup-induced regime collapse (separate code), independent
    AI takeover, external intervention.

Singleton (S6) := effective winning coalition W == 1 while the regime is intact.

Outputs: results/m5_depopulation_singleton.json, figures/m5_depopulation_singleton_*.png
"""
import json
import os
import time

import numpy as np
from scipy.stats import spearmanr

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(ROOT, "results", "m5_depopulation_singleton.json")
FIG = os.path.join(ROOT, "figures")

SEED = 20260930
N_OUTER = 12000          # parameter draws, main run (S5 metrics)
N_INNER = 80
N_OUTER_S6 = 1000        # S6 run: fewer draws, many paths, so per-draw P(S6|S5) is not binomial noise
N_INNER_S6 = 1000
S5_WINDOW = 20
S6_WINDOW = 20
T_HORIZON = S5_WINDOW + S6_WINDOW   # 40: full S6 follow-up for every S5 path
W_REF = 30.0
BASE_YEAR = 2026.75
DEPTH_REF = 0.39                    # median S2 collapse depth in M2 (1 - bottom-80% real consumption)

REF_FLAGS = dict(threat=False, refuse=False, s2=False, cost_dyn=False, atroc_exit=False)
FULL_FLAGS = dict(threat=True, refuse=True, s2=True, cost_dyn=True, atroc_exit=True)


# ----------------------------------------------------------------------------------------
# upstream coupling samples
# ----------------------------------------------------------------------------------------
def _load_upstream():
    up = {}
    try:
        d = json.load(open(os.path.join(ROOT, "results", "m4_state_repression.json")))["samples"]["year"]
        y = np.array([np.nan if v is None else v for v in d], float)
        up["s4_year"] = y[~np.isnan(y)]
    except Exception:
        up["s4_year"] = None
    try:
        d = json.load(open(os.path.join(ROOT, "results", "m2_no_customers_domino.json")))["samples_thinned_every_4th"]
        s = np.array(d["s2_indicator"]); c = np.array(d["min_bottom80_real_consumption"], float)
        up["s2_depth"] = 1 - c[s == 1]
    except Exception:
        up["s2_depth"] = None
    return up


UP = _load_upstream()


# ----------------------------------------------------------------------------------------
# priors
# ----------------------------------------------------------------------------------------
def beta_mean_ci(rng, mean, lo, hi, n):
    sd = (hi - lo) / 3.29
    conc = max(mean * (1 - mean) / sd**2 - 1, 2.0)
    return rng.beta(mean * conc, (1 - mean) * conc, n)


def lognorm_med(rng, med, lo, hi, n):
    s = (np.log(hi) - np.log(lo)) / (2 * 1.645)
    return med * np.exp(s * rng.standard_normal(n))


def ann_hazard(p, years):
    return -np.log1p(-np.clip(p, 1e-9, 0.999)) / years


def draw_params(n, rng, psi_mode="beta13"):
    P = {}
    # --- anchors (research/m5_depopulation_singleton.md, table 5) ---
    P["p_active_ref"] = beta_mean_ci(rng, 0.10, 0.02, 0.30, n)       # row 6, judgment
    P["p_neglect_all"] = beta_mean_ci(rng, 0.35, 0.15, 0.60, n)      # row 7, judgment
    P["neglect_mort_share"] = rng.uniform(0.25, 0.6, n)              # share of row 7 that is famine-grade excess mortality
    P["p_neglect_ref"] = P["p_neglect_all"] * P["neglect_mort_share"]
    P["fert_deliberate_share"] = rng.uniform(0.2, 0.6, n)            # share of fertility-driven part that is engineered (S5b)
    P["p_s5b_ref"] = P["p_neglect_all"] * (1 - P["neglect_mort_share"]) * P["fert_deliberate_share"]
    P["p_coopt_prior"] = beta_mean_ci(rng, 0.70, 0.45, 0.90, n)      # row 8, checked against output
    # --- selectorate ---
    P["W0"] = np.exp(rng.uniform(np.log(20), np.log(2000), n))
    P["W_end"] = np.clip(lognorm_med(rng, 10, 1, 1000, n), 1, None)
    P["tau_auto"] = rng.uniform(3, 15, n)
    P["beta_W_active"] = rng.uniform(0.10, 0.40, n)
    P["beta_W_neglect"] = rng.uniform(0.15, 0.50, n)
    # --- elite self-interest ---
    P["cost_share0"] = lognorm_med(rng, 0.05, 0.01, 0.20, n)         # transfer cost / output at S4 (Gulf 5-15% GDP, discounted for AI output)
    P["output_growth"] = rng.uniform(-0.02, 0.20, n)                 # real output growth net of transfer-need growth (explosive vs resource-limited)
    P["s2_cost_elast"] = rng.uniform(0.5, 1.5, n)                    # transfer need ~ (S2 depth / ref)^elast
    P["loss_aversion"] = rng.uniform(1.5, 2.5, n)                    # Tversky & Kahneman 1992; Brown et al. 2024
    P["gamma_cost"] = rng.uniform(0.2, 0.6, n)
    P["cost_exp_neglect"] = rng.uniform(1.0, 1.6, n)                 # neglect more cost-sensitive than killing (was fixed 1.3)
    P["land_motive"] = 1 + lognorm_med(rng, 0.2, 0.05, 0.8, n)       # >=1 (Wolfe; Herero)
    # --- S2 consumer-interest brake ---
    P["ci0"] = rng.uniform(0.1, 0.5, n)                              # hazard reduction from consumer-facing owners in coalition, pre-S2
    P["tau_ci"] = rng.uniform(3, 12, n)
    P["s2_w0_shrink"] = rng.uniform(0.0, 0.6, n)
    # --- framing ---
    P["p_outgroup20"] = beta_mean_ci(rng, 0.30, 0.10, 0.55, n)
    P["M_frame_active"] = lognorm_med(rng, 3.0, 1.5, 6.0, n)         # Harff 2003
    P["M_frame_neglect"] = lognorm_med(rng, 1.8, 1.1, 3.0, n)
    P["M_frame_s5b"] = lognorm_med(rng, 2.5, 1.2, 5.0, n)            # 'ecological kindness' framing fits fertility suppression best
    # --- status quo ---
    P["p_welfare_state"] = rng.uniform(0.4, 0.8, n)
    P["sq_mult"] = rng.uniform(0.3, 0.8, n)
    P["sq_decay"] = rng.uniform(0.03, 0.15, n)
    P["ext_deter"] = rng.uniform(0.5, 1.0, n)
    # --- public as threat / leverage (v2) ---
    P["p_armed"] = beta_mean_ci(rng, 0.30, 0.08, 0.60, n)            # P(public retains near-frontier open-weight capability after S4); M7 open-release priors, S4 suppression
    P["OR_threat"] = lognorm_med(rng, 2.8, 1.5, 5.0, n)              # Valentino, Huth & Balch-Lindsay 2004 (guerrilla threat OR ~2-4)
    P["lever_reform"] = rng.uniform(1.0, 2.5, n)
    P["lever_ext"] = rng.uniform(1.0, 1.5, n)
    # --- AI compliance (v2) ---
    P["p_ai_refuse"] = beta_mean_ci(rng, 0.35, 0.05, 0.70, n)        # P(deployed AI refuses mass-casualty orders absent retraining); judgment
    P["retrain_delay"] = rng.uniform(0.5, 4.0, n)
    P["m_retrain_ai"] = rng.uniform(1.5, 4.0, n)                     # takeover hazard multiplier after retraining out refusals
    # --- AI / external response to atrocity and overload (v2) ---
    P["m_ai_atroc"] = rng.uniform(1.0, 3.0, n)
    P["m_ai_overload"] = rng.uniform(1.0, 3.0, n)
    P["m_ext_atroc"] = rng.uniform(2.0, 5.0, n)
    # --- purge / elite game ---
    P["k_purge"] = rng.uniform(0.2, 0.8, n)
    P["k_purge_min"] = rng.uniform(0.01, 0.05, n)
    P["purge_frac"] = beta_mean_ci(rng, 0.55, 0.30, 0.70, n)
    P["punish_irreg"] = beta_mean_ci(rng, 0.80, 0.70, 0.85, n)       # Archigos
    P["punish_base"] = rng.uniform(0.2, 0.3, n)
    P["paranoia_scale"] = rng.uniform(0.5, 1.5, n)
    P["p_inner_turn"] = beta_mean_ci(rng, 0.60, 0.40, 0.75, n)       # 7/12 case tally
    P["p_neglect_atrocity"] = rng.beta(2, 4, n)                      # was fixed 0.5; GLF->CR yes, Bengal / post-Soviet no
    if psi_mode == "uniform":
        P["psi_paranoia"] = rng.uniform(0, 1, n)                     # scenario text-maximal
    else:
        P["psi_paranoia"] = rng.beta(1, 3, n)                        # historic circles 5-20 (Politburo, RCC)
    P["coup_c0"] = rng.uniform(0.005, 0.03, n)                       # baseline pre-emptive coup hazard (Powell & Thyne ~457/60y/~100 autocracies)
    P["coup_c1"] = rng.uniform(0.1, 0.5, n)                          # coup hazard per unit of member purge risk
    P["coup_single"] = rng.uniform(0.005, 0.04, n)                   # AI operators vs a W=1 ruler
    P["coup_success"] = beta_mean_ci(rng, 0.50, 0.40, 0.55, n)       # Powell & Thyne 2011
    P["ai_key_discount"] = rng.uniform(0.3, 1.0, n)                  # Davidson et al. 2025
    P["coup_breakdown"] = rng.uniform(0.05, 0.2, n)                  # was fixed 0.1
    P["p_clear_paranoia_coup"] = rng.uniform(0.3, 0.8, n)
    P["p_clear_paranoia_succ"] = rng.uniform(0.4, 0.9, n)            # Khrushchev, Deng de-escalated
    P["h_lock"] = lognorm_med(rng, 0.03, 0.008, 0.10, n)
    P["lock_purge_mult"] = rng.uniform(0.1, 0.4, n)
    P["lock_block"] = rng.uniform(0.3, 0.7, n)                       # was fixed 0.5
    P["regrow"] = rng.uniform(0.1, 0.3, n)                           # was fixed 0.2
    P["ruler_mort"] = rng.uniform(0.01, 0.03, n)
    # --- exits ---
    P["h_reform"] = lognorm_med(rng, 0.02, 0.005, 0.06, n)
    P["h_ai_takeover"] = lognorm_med(rng, 0.005, 0.001, 0.02, n)
    P["h_external"] = lognorm_med(rng, 0.005, 0.001, 0.02, n)
    # --- upstream ---
    if UP["s2_depth"] is not None:
        P["s2_depth"] = rng.choice(UP["s2_depth"], n)
    else:
        P["s2_depth"] = rng.uniform(0.25, 0.6, n)
    if UP["s4_year"] is not None:
        P["s4_year"] = rng.choice(UP["s4_year"], n) + rng.uniform(0, 1, n)
    else:
        P["s4_year"] = BASE_YEAR + np.clip(lognorm_med(rng, 15.0, 6.0, 37.0, n), 2.0, 70.0)
    return P


def consolidation_boost(P):
    # variant tuned toward research row 13 (personalism ~0.40): smaller functional need and
    # 3x background purging
    P = dict(P)
    P["W_end"] = np.clip(P["W_end"] * 0.3, 1, None)
    P["k_purge_min"] = P["k_purge_min"] * 3
    return P


# ----------------------------------------------------------------------------------------
# simulation
# ----------------------------------------------------------------------------------------
def simulate(P, n_inner, rng, T, flags, k_cal, coups=True, neg_atroc_override=None):
    n_outer = P["W0"].size
    M = n_outer * n_inner
    g = {k: np.repeat(v, n_inner) for k, v in P.items()}
    ka, kn, kb = k_cal
    ha0 = ka * ann_hazard(g["p_active_ref"], S5_WINDOW)
    hn0 = kn * ann_hazard(g["p_neglect_ref"], S5_WINDOW)
    hb0 = kb * ann_hazard(g["p_s5b_ref"], S5_WINDOW)
    hfr = ann_hazard(g["p_outgroup20"], S5_WINDOW)
    parM = 1 + g["paranoia_scale"] * (g["punish_irreg"] / g["punish_base"] - 1)
    c_ref = 2.0 * 0.05
    depth = g["s2_depth"]
    if flags["s2"]:
        cs0 = g["cost_share0"] * (depth / DEPTH_REF) ** g["s2_cost_elast"]
        W0 = np.maximum(g["W0"] * (1 - g["s2_w0_shrink"] * depth), 3.0)
    else:
        cs0 = g["cost_share0"]
        W0 = g["W0"]
    p_na = g["p_neglect_atrocity"] if neg_atroc_override is None else np.full(M, neg_atroc_override)

    intact = np.ones(M, bool)
    exit_type = np.zeros(M, np.int8)   # 0 none, 1 reform, 2 AI takeover, 3 external, 4 coup collapse
    exit_t = np.full(M, np.nan)
    W = W0.copy()
    framed = np.zeros(M, bool)
    welfare = rng.random(M) < g["p_welfare_state"]
    locked = np.zeros(M, bool)
    atrocity = np.zeros(M, bool)
    pmode = np.zeros(M, bool)
    paranoid_type = rng.random(M) < g["p_inner_turn"]
    armed = (rng.random(M) < g["p_armed"]) if flags["threat"] else np.zeros(M, bool)
    refuse = (rng.random(M) < g["p_ai_refuse"]) if flags["refuse"] else np.zeros(M, bool)
    retrain_until = np.full(M, np.nan)
    retrained = np.zeros(M, bool)
    s5_type = np.zeros(M, np.int8)
    s5_onset = np.full(M, np.nan)
    s5_t = np.full(M, np.nan)
    s5b_t = np.full(M, np.nan)
    single_first = np.full(M, np.nan)
    single_after = np.full(M, np.nan)   # first W==1 year at/after S5 onset
    le5_first = np.full(M, np.nan)
    n_purges = np.zeros(M, np.int16)
    n_coups = np.zeros(M, np.int16)

    for t in range(1, T + 1):
        u = rng.random((10, M))
        W_need = g["W_end"] + (W0 - g["W_end"]) * np.exp(-t / g["tau_auto"])

        # ---- exits ----
        h_ref = g["h_reform"] * np.sqrt(np.clip(W / W0, 0, 1)) * np.where(armed, g["lever_reform"], 1.0)
        h_ai = g["h_ai_takeover"].copy()
        h_ext = g["h_external"] * np.where(armed, g["lever_ext"], 1.0)
        if flags["atroc_exit"]:
            h_ai = h_ai * np.where(atrocity, g["m_ai_atroc"], 1.0) * \
                np.where(W < 0.999 * W_need, g["m_ai_overload"], 1.0)
            h_ext = h_ext * np.where(atrocity, g["m_ext_atroc"], 1.0)
        h_ai = h_ai * np.where(~np.isnan(retrain_until), g["m_retrain_ai"], 1.0)
        h_ex = h_ref + h_ai + h_ext
        ex = intact & (u[0] < 1 - np.exp(-h_ex))
        if ex.any():
            r = rng.random(ex.sum()) * h_ex[ex]
            exit_type[ex] = np.where(r < h_ref[ex], 1, np.where(r < h_ref[ex] + h_ai[ex], 2, 3))
            exit_t[ex] = t
            intact[ex] = False

        framed |= intact & (u[1] < 1 - np.exp(-hfr))
        welfare &= ~(u[2] < 1 - np.exp(-g["sq_decay"]))

        # ---- S5 hazards ----
        cs = cs0 * np.exp(-g["output_growth"] * t) if flags["cost_dyn"] else cs0
        cost_mult = g["loss_aversion"] * cs / c_ref
        cm_a = cost_mult ** g["gamma_cost"]
        cm_n = cost_mult ** (g["gamma_cost"] * g["cost_exp_neglect"])
        ci = g["ci0"] * (1 - depth) * np.exp(-t / g["tau_ci"]) if flags["s2"] else 0.0
        wf = W_REF / np.maximum(W, 1.0)
        sq = np.where(welfare, g["sq_mult"], 1.0)
        pending = ~np.isnan(retrain_until) & ~retrained
        free = intact & np.isnan(s5_onset)
        ha = ha0 * wf ** g["beta_W_active"] * cm_a * g["land_motive"] * \
            np.where(framed, g["M_frame_active"], 1.0) * sq * g["ext_deter"] * \
            np.where(armed, g["OR_threat"], 1.0) * (1 - ci) * ~pending
        hn = hn0 * wf ** g["beta_W_neglect"] * cm_n * np.where(framed, g["M_frame_neglect"], 1.0) * sq * (1 - ci)
        htot = ha + hn
        ev = free & (u[3] < 1 - np.exp(-htot))
        new_onset = np.zeros(M, bool); new_active = np.zeros(M, bool)
        if ev.any():
            idx = np.flatnonzero(ev)
            is_a = rng.random(idx.size) < ha[idx] / htot[idx]
            block = is_a & refuse[idx] & ~retrained[idx]
            retrain_until[idx[block]] = t + g["retrain_delay"][idx[block]]
            go = idx[~block]
            new_onset[go] = True
            new_active[go] = is_a[~block]
        # retraining finished: intent carried out
        done = free & pending & (retrain_until <= t)
        retrained |= done
        new_onset |= done; new_active |= done
        if new_onset.any():
            idx = np.flatnonzero(new_onset)
            act = new_active[idx]
            s5_type[idx] = np.where(act, 1, 2)
            s5_onset[idx] = t - rng.random(idx.size)
            # active: Holodomor 1-2y, KR 4y. Neglect: famine-grade withdrawal still slower
            # (post-Soviet collapse ~2%/decade would never reach 10%; neglect onset means famine-grade)
            delay = np.where(act, rng.uniform(0.5, 3.0, idx.size), rng.uniform(3.0, 10.0, idx.size))
            s5_t[idx] = s5_onset[idx] + delay
            atr = act | (rng.random(idx.size) < p_na[idx])
            atrocity[idx[atr]] = True
            pmode[idx[atr]] |= paranoid_type[idx[atr]]

        # ---- S5b: engineered fertility suppression (non-competing) ----
        hb = hb0 * np.where(framed, g["M_frame_s5b"], 1.0) * sq
        s5b_new = intact & np.isnan(s5b_t) & (u[4] < 1 - np.exp(-hb))
        s5b_t[s5b_new] = t - rng.random(s5b_new.sum())

        # ---- elite game ----
        activeW = intact & (W > 1.0 + 1e-9)
        lock_new = activeW & ~locked & (u[5] < 1 - np.exp(-g["h_lock"]))
        locked |= lock_new & ~(pmode & (rng.random(M) < g["lock_block"]))
        W_tgt = np.where(pmode, np.maximum(W_need, 1.0) ** (1 - g["psi_paranoia"]), W_need)
        surplus = np.clip((W - W_tgt) / W, 0, 1)
        hp = (g["k_purge"] * surplus + g["k_purge_min"]) * np.where(pmode, parM, 1.0) * \
            np.where(locked, g["lock_purge_mult"], 1.0)
        floor_ret = np.where(pmode, 1.0, np.maximum(W_need, 1.0))

        coup = np.zeros(M, bool)
        if coups:
            # pre-emptive insider coup: members strike first when their purge risk is high
            h_c = np.where(activeW, g["coup_c0"] + g["coup_c1"] * hp, 0.0)
            h_c = np.where(intact & ~activeW, g["coup_single"], h_c)
            coup = intact & (u[6] < 1 - np.exp(-h_c))
            if coup.any():
                n_coups[coup] += 1
                succ = coup & (rng.random(M) < g["coup_success"] * g["ai_key_discount"])
                brk = succ & (rng.random(M) < g["coup_breakdown"])
                intact[brk] = False; exit_type[brk] = 4; exit_t[brk] = t
                ok = succ & ~brk
                W[ok] = np.maximum(W_need[ok], 3.0) * rng.uniform(1.0, 3.0, ok.sum())
                locked[ok] = False
                pmode[ok & (rng.random(M) < g["p_clear_paranoia_coup"])] = False
                fail = coup & ~succ & activeW
                W[fail] = np.maximum(floor_ret[fail], W[fail] * (1 - g["purge_frac"][fail]))
                W[fail] = np.where(W[fail] < 1.5, 1.0, W[fail])

        purge = activeW & intact & ~coup & (u[7] < 1 - np.exp(-hp))
        if purge.any():
            f = np.clip(g["purge_frac"][purge] * rng.uniform(0.6, 1.4, purge.sum()), 0.05, 0.95)
            newW = W[purge] * (1 - f)
            newW = np.maximum(np.where(newW < 1.5, 1.0, newW), floor_ret[purge])
            W[purge] = np.minimum(W[purge], newW)
            n_purges[purge] += 1
        # replacement recruitment: purged members are replaced by new loyalists (Stalin's
        # 1938-39 promotions). Toward W_need normally, toward the paranoid target in pmode.
        W_grow_tgt = np.where(pmode, W_tgt, W_need)
        grow = intact & (W < W_grow_tgt) & (W > 1)
        W[grow] = W[grow] + g["regrow"][grow] * (W_grow_tgt[grow] - W[grow])

        is1 = intact & (W <= 1.0)
        tt = t - rng.random(M)
        single_first = np.where(is1 & np.isnan(single_first), tt, single_first)
        single_after = np.where(is1 & np.isnan(single_after) & ~np.isnan(s5_onset), tt, single_after)
        le5_first = np.where(intact & (W <= 5.0) & np.isnan(le5_first), tt, le5_first)
        # ruler death -> succession; coalition re-forms; successor may de-escalate
        dead = is1 & (u[8] < g["ruler_mort"])
        W[dead] = np.maximum(W_need[dead], 3.0) * rng.uniform(1.0, 3.0, dead.sum())
        locked[dead] = False
        pmode[dead & (u[9] < g["p_clear_paranoia_succ"])] = False

    return dict(s5_type=s5_type, s5_t=s5_t, s5_onset=s5_onset, s5b_t=s5b_t,
                single_first=single_first, single_after=single_after, le5_first=le5_first,
                exit_type=exit_type, exit_t=exit_t, n_purges=n_purges, n_coups=n_coups,
                armed=armed, refuse=refuse, retrained=retrained)


def outcomes(S):
    s5 = (S["s5_type"] > 0) & (S["s5_t"] <= S5_WINDOW)
    o = dict(s5=s5, act=s5 & (S["s5_type"] == 1), neg=s5 & (S["s5_type"] == 2))
    sf, sa = S["single_first"], S["single_after"]
    in_win = lambda x: ~np.isnan(x) & (x <= S["s5_t"] + S6_WINDOW) & (x >= S["s5_onset"] - 5)
    o["s6"] = s5 & (in_win(sf) | in_win(sa))
    o["s6_before_s5"] = o["s6"] & (sf < S["s5_onset"])
    o["le5_s5"] = s5 & ~np.isnan(S["le5_first"]) & (S["le5_first"] <= S["s5_t"] + S6_WINDOW)
    o["single20"] = ~np.isnan(sf) & (sf <= 20)
    o["le5_20"] = ~np.isnan(S["le5_first"]) & (S["le5_first"] <= 20)
    o["exit20"] = (S["exit_type"] > 0) & (S["exit_t"] <= 20)
    o["ware"] = ~s5 & ~o["exit20"]
    o["s5b"] = ~np.isnan(S["s5b_t"]) & (S["s5b_t"] <= S5_WINDOW)
    for k, v in [("reform_redistribution", 1), ("ai_takeover_independent", 2),
                 ("external_intervention", 3), ("coup_collapse", 4)]:
        o["exit_" + k] = o["exit20"] & (S["exit_type"] == v)
    return o


def per_draw(mask, n_inner, denom=None):
    m = mask.reshape(-1, n_inner).sum(1).astype(float)
    if denom is None:
        return m / n_inner, np.full(m.size, n_inner, float)
    d = denom.reshape(-1, n_inner).sum(1).astype(float)
    return np.where(d > 0, m / np.maximum(d, 1), np.nan), d


def epi_summary(p, n, weights=None):
    """Mean, MC CI, and epistemic 5-95% interval with binomial noise removed by shrinkage."""
    ok = ~np.isnan(p) & (n > 0)
    p, n = p[ok], n[ok]
    w = n if weights == "n" else np.ones_like(p)
    m = float((p * w).sum() / w.sum())
    var_tot = float(np.var(p))
    var_noise = float(np.mean(p * (1 - p) / n)) if p.size else 0.0
    var_epi = max(var_tot - var_noise, 0.0)
    shrink = np.sqrt(var_epi / var_tot) if var_tot > 0 else 0.0
    ps = m + shrink * (p - m)
    se = np.sqrt(var_tot / p.size)
    return dict(mean=m, mc_ci_low=m - 1.96 * se, mc_ci_high=m + 1.96 * se,
                epistemic_p05=float(np.percentile(ps, 5)), epistemic_p95=float(np.percentile(ps, 95)),
                sd_total=np.sqrt(var_tot), sd_noise=np.sqrt(var_noise), sd_epistemic=np.sqrt(var_epi)), ps, ok


# ----------------------------------------------------------------------------------------
# calibration: base hazards so reference model reproduces priors (net of exits)
# ----------------------------------------------------------------------------------------
def calibrate(n=4000, n_inner=40, iters=7):
    rngp = np.random.default_rng(SEED + 10)
    Pc = draw_params(n, rngp)
    tgt = np.array([Pc["p_active_ref"].mean(), Pc["p_neglect_ref"].mean(), Pc["p_s5b_ref"].mean()])
    k = np.array([1.0, 1.0, 1.0])
    hist = []
    for _ in range(iters):
        S = simulate(Pc, n_inner, np.random.default_rng(SEED + 11), S5_WINDOW, REF_FLAGS, k)
        o = outcomes(S)
        sim = np.array([o["act"].mean(), o["neg"].mean(), o["s5b"].mean()])
        hist.append(sim.tolist())
        k = k * ann_hazard(tgt, 1) / ann_hazard(np.maximum(sim, 1e-4), 1)
    return k, tgt, hist


t0 = time.time()
K_CAL, CAL_TGT, CAL_HIST = calibrate()
print("calibration k", K_CAL, "targets", CAL_TGT, "last sim", CAL_HIST[-1])

# ----------------------------------------------------------------------------------------
# main run (S5)
# ----------------------------------------------------------------------------------------
rng_p = np.random.default_rng(SEED)
P = draw_params(N_OUTER, rng_p)
S = simulate(P, N_INNER, np.random.default_rng(SEED + 1), T_HORIZON, FULL_FLAGS, K_CAL)
O = outcomes(S)
runtime_main = time.time() - t0

pd = {}
for key in ["s5", "act", "neg", "ware", "s5b", "single20", "le5_20", "exit20"] + \
        [k for k in O if k.startswith("exit_")]:
    pd[key] = per_draw(O[key], N_INNER)
res = {k: epi_summary(*v)[0] for k, v in pd.items()}
_, ps5_shrunk, _ = epi_summary(*pd["s5"])
pd_s6_main, n_s6_main = per_draw(O["s6"], N_INNER, O["s5"])
res_s6_main = epi_summary(pd_s6_main, n_s6_main, weights="n")[0]
res_le5_s5_main = epi_summary(*per_draw(O["le5_s5"], N_INNER, O["s5"]), weights="n")[0]
res_s6_nos5 = epi_summary(*per_draw(O["single20"] & ~O["s5"], N_INNER, ~O["s5"]), weights="n")[0]
s6_before_share = float(O["s6_before_s5"].sum() / max(O["s6"].sum(), 1))

# reference (calibration-model) run on same draws, for the structural delta
S_ref = simulate(P, 20, np.random.default_rng(SEED + 3), T_HORIZON, REF_FLAGS, K_CAL)
O_ref = outcomes(S_ref)
ref = {k: float(O_ref[k].mean()) for k in ["s5", "act", "neg", "s5b", "ware"]}
ref["s6_given_s5"] = float(O_ref["s6"].sum() / O_ref["s5"].sum())
# one-at-a-time channel deltas
chan = {}
for ch in ["threat", "refuse", "s2", "cost_dyn", "atroc_exit"]:
    fl = dict(REF_FLAGS); fl[ch] = True
    Sx = simulate(P, 10, np.random.default_rng(SEED + 4), T_HORIZON, fl, K_CAL)
    Ox = outcomes(Sx)
    chan[ch] = dict(P_S5=float(Ox["s5"].mean()), active=float(Ox["act"].mean()), neglect=float(Ox["neg"].mean()),
                    P_S6_given_S5=float(Ox["s6"].sum() / max(Ox["s5"].sum(), 1)))

# ----------------------------------------------------------------------------------------
# S6 run: many paths per draw
# ----------------------------------------------------------------------------------------
def s6_run(psi_mode="beta13", n_outer=N_OUTER_S6, n_inner=N_INNER_S6, coups=True, neg_atroc=None, seed_off=0,
           boost=False):
    P6 = draw_params(n_outer, np.random.default_rng(SEED + 20 + seed_off), psi_mode=psi_mode)
    if boost:
        P6 = consolidation_boost(P6)
    S6 = simulate(P6, n_inner, np.random.default_rng(SEED + 21 + seed_off), T_HORIZON, FULL_FLAGS, K_CAL,
                  coups=coups, neg_atroc_override=neg_atroc)
    O6 = outcomes(S6)
    return P6, S6, O6


P6, S6, O6 = s6_run()
pd_s6, n_s6 = per_draw(O6["s6"], N_INNER_S6, O6["s5"])
res_s6, ps6_shrunk, ok6 = epi_summary(pd_s6, n_s6, weights="n")
res_le5_s5 = epi_summary(*per_draw(O6["le5_s5"], N_INNER_S6, O6["s5"]), weights="n")[0]
res_s6_s4 = epi_summary(*per_draw(O6["single20"], N_INNER_S6))[0]
res_s5_s6run = float(O6["s5"].mean())

# structural variants (P(S6|S5) and P(S5))
variants = {}
for name, kw in [("psi_uniform_scenario_maximal", dict(psi_mode="uniform")),
                 ("neglect_never_atrocity", dict(neg_atroc=0.0)),
                 ("neglect_always_atrocity", dict(neg_atroc=1.0)),
                 ("no_coups", dict(coups=False)),
                 ("consolidation_tuned_to_personalism_prior", dict(boost=True)),
                 ("scenario_maximal_psiU_neglect_atrocity_boost", dict(psi_mode="uniform", neg_atroc=1.0, boost=True))]:
    _, _, Ov = s6_run(n_outer=400, n_inner=600, seed_off=100, **kw)
    variants[name] = dict(P_S5=float(Ov["s5"].mean()), P_S6_given_S5=float(Ov["s6"].sum() / Ov["s5"].sum()),
                          P_singleton20_given_S4=float(Ov["single20"].mean()),
                          P_W_le_5_20y_given_S4=float(Ov["le5_20"].mean()))
_, _, Ob = s6_run(n_outer=400, n_inner=600, seed_off=100)
variants["baseline_same_seed"] = dict(P_S5=float(Ob["s5"].mean()), P_S6_given_S5=float(Ob["s6"].sum() / Ob["s5"].sum()),
                                      P_singleton20_given_S4=float(Ob["single20"].mean()),
                                      P_W_le_5_20y_given_S4=float(Ob["le5_20"].mean()))
runtime = time.time() - t0

# ----------------------------------------------------------------------------------------
# timing
# ----------------------------------------------------------------------------------------
s4y = np.repeat(P["s4_year"], N_INNER)
y5 = (s4y + S["s5_t"])[O["s5"]]
lag5 = S["s5_t"][O["s5"]]
lag5_onset = S["s5_onset"][O["s5"]]
s4y6 = np.repeat(P6["s4_year"], N_INNER_S6)
t6 = np.where(~np.isnan(S6["single_first"]) & (S6["single_first"] >= S6["s5_onset"] - 5),
              S6["single_first"], S6["single_after"])
y6 = (s4y6 + t6)[O6["s6"]]
lag6 = (t6 - S6["s5_t"])[O6["s6"]]


def q(x, ps=(10, 50, 90)):
    return [float(np.percentile(x, p)) for p in ps]


y5q, y6q, lag5q, lag6q, lag5oq = q(y5), q(y6), q(lag5), q(lag6), q(lag5_onset)
p_onset_le10 = float((lag5_onset <= 10).mean())

# sensitivity (Spearman, S5 on main run; S6 on S6 run with 1000 paths/draw)
skip = ("s4_year",)
sens5 = {k: float(spearmanr(v, pd["s5"][0]).correlation) for k, v in P.items() if k not in skip}
sens6 = {k: float(spearmanr(v[ok6], pd_s6[ok6]).correlation) for k, v in P6.items() if k not in skip}
top5 = sorted(sens5.items(), key=lambda kv: -abs(kv[1]))[:10]
top6 = sorted(sens6.items(), key=lambda kv: -abs(kv[1]))[:10]

# checks
ware_given_no_exit = float((O["ware"]).sum() / max((~O["exit20"]).sum(), 1))
checks = {
    "calibration_targets_active_neglect_s5b": CAL_TGT.tolist(),
    "calibration_reference_model_simulated": CAL_HIST[-1],
    "calibration_k_multipliers": K_CAL.tolist(),
    "cooptation_prior_mean": float(P["p_coopt_prior"].mean()),
    "warehousing_given_no_exit_20y": ware_given_no_exit,
    "warehousing_unconditional_20y": res["ware"]["mean"],
    "single_ruler_prior_row13": {"mean": 0.40, "low": 0.15, "high": 0.65},
    "sim_W_le_5_within_20y_given_S4": res["le5_20"]["mean"],
    "sim_W_eq_1_within_20y_given_S4": res["single20"]["mean"],
    "note_consolidation": ("Row 13 (0.40) is a personalism prior. W<=5 is the closest simulated analog; W=1 (one human "
                           "with no functional coalition) is a much stronger claim than personalism and is not tuned to 0.40."),
    "s5_onset_lag_historical": {"research_row5_median": 5, "range": [0, 10],
                                "sim_onset_lag_p10_p50_p90": lag5oq, "sim_share_onset_within_10y": p_onset_le10},
}

# ----------------------------------------------------------------------------------------
# export
# ----------------------------------------------------------------------------------------
samp = np.random.default_rng(SEED + 2)
ns = 2000


def r4(a):
    return [round(float(x), 4) for x in a]


def slim(d):
    return {k: (round(v, 5) if isinstance(v, float) else v) for k, v in d.items()}


out = {
    "module": "m5_depopulation_singleton", "version": 2,
    "seed": SEED, "n_outer_draws": N_OUTER, "n_inner_paths": N_INNER,
    "s6_run": {"n_outer_draws": N_OUTER_S6, "n_inner_paths": N_INNER_S6},
    "horizon_years": T_HORIZON, "runtime_s": round(runtime, 1),
    "conditioning": ("S4 occurred: AI-controlling elite with largely automated coercion, unrest suppressed, "
                     "state revenue from AI capital, public economically irrelevant."),
    "uncertainty_note": ("Headline uncertainty is the epistemic 5-95% interval over parameter draws, binomial noise "
                         "removed by shrinkage (Var_epi = Var(p_draw) - mean p(1-p)/n). mc_ci is Monte Carlo precision "
                         "of the mean only. Structural variants show additional model-form uncertainty."),
    "stage_probability": {
        "mean": res["s5"]["mean"], "ci_low": res["s5"]["epistemic_p05"], "ci_high": res["s5"]["epistemic_p95"],
        "ci_type": "epistemic 5-95% over parameter draws (noise-corrected)",
        "mc_ci95": [res["s5"]["mc_ci_low"], res["s5"]["mc_ci_high"]],
        "definition": ("P(S5 | S4): within 20 years of S4 onset, the public of the AI-controlled jurisdiction falls >=10% "
                       "below counterfactual through deliberate killing/starvation/forced sterilisation (active) or "
                       "famine-grade withdrawal of provision (passive neglect), before any exit. Engineered non-lethal "
                       "fertility suppression is reported separately as S5b."),
    },
    "s5_breakdown": {k: slim(res[k]) for k in ["act", "neg", "ware"]},
    "s5_breakdown_labels": {"act": "active depopulation", "neg": "passive neglect (famine-grade)",
                            "ware": "warehousing/managed dependency, regime intact at 20y"},
    "exits_before_20y": {k[5:]: slim(res[k]) for k in res if k.startswith("exit_")},
    "s5b_engineered_fertility_decline_20y": slim(res["s5b"]),
    "s5_or_s5b_20y": float((O["s5"] | O["s5b"]).mean()),
    "structural_delta": {
        "reference_model_calibrated_to_priors": ref,
        "full_model": {"s5": res["s5"]["mean"], "act": res["act"]["mean"], "neg": res["neg"]["mean"],
                       "s5b": res["s5b"]["mean"], "s6_given_s5": res_s6["mean"]},
        "one_channel_on_at_a_time": chan,
        "channels": {"threat": "public-as-threat + bargaining leverage", "refuse": "AI refuses mass-casualty orders",
                     "s2": "S2 depth raises cost share, removes consumer-interest brake, shrinks W0",
                     "cost_dyn": "cost share evolves with output growth", "atroc_exit": "atrocity raises external/AI exits"},
    },
    "s6_given_s5": {
        "mean": res_s6["mean"], "ci_low": res_s6["epistemic_p05"], "ci_high": res_s6["epistemic_p95"],
        "ci_type": "epistemic 5-95% (1000 paths/draw, noise-corrected)",
        "mc_ci95": [res_s6["mc_ci_low"], res_s6["mc_ci_high"]],
        "sd_total_noise_epistemic": [res_s6["sd_total"], res_s6["sd_noise"], res_s6["sd_epistemic"]],
        "main_run_estimate": res_s6_main["mean"],
        "share_singleton_before_s5_onset": s6_before_share,
        "definition": ("P(S6 | S5, S4): among S5 paths, a single human holds control of the jurisdiction's AI and "
                       "coercion (W=1) within 20 years after the S5 threshold (or up to 5 years before S5 onset), "
                       "regime intact. Every S5 path has a full 20-year follow-up."),
    },
    "W_le_5_within_20y_of_s5_given_s5": slim(res_le5_s5),
    "s6_given_s4_any_20y": slim(res_s6_s4),
    "s6_given_s4_and_no_s5_20y": slim(res_s6_nos5),
    "structural_variants": variants,
    "timeline": {
        "definition": "Calendar year S5 threshold (>=10% depopulation) is crossed, given S4 and S5; S4 year sampled from M4.",
        "p10_year": y5q[0], "median_year": y5q[1], "p90_year": y5q[2],
        "lag_after_s4_years": {"p10": lag5q[0], "median": lag5q[1], "p90": lag5q[2]},
        "onset_lag_after_s4_years": {"p10": lag5oq[0], "median": lag5oq[1], "p90": lag5oq[2]},
    },
    "timeline_s6": {
        "definition": "Calendar year singleton (W=1) forms, given S4, S5, S6; S4 year sampled from M4.",
        "p10_year": y6q[0], "median_year": y6q[1], "p90_year": y6q[2],
        "lag_after_s5_years": {"p10": lag6q[0], "median": lag6q[1], "p90": lag6q[2]},
    },
    "assumed_s4_year": {"source": "M4 samples.year" if UP["s4_year"] is not None else "placeholder",
                        "p10_p50_p90": q(P["s4_year"])},
    "s2_depth_source": "M2 1 - min_bottom80_real_consumption | S2" if UP["s2_depth"] is not None else "placeholder",
    "sensitivity_spearman_P_S5": dict(top5),
    "sensitivity_spearman_P_S6_given_S5": dict(top6),
    "checks": checks,
    "for_other_stages": {
        "p_regime_intact_20y": float(1 - O["exit20"].mean()),
        "p_independent_ai_takeover_before_20y": res["exit_ai_takeover_independent"]["mean"],
        "p_reform_redistribution_before_20y": res["exit_reform_redistribution"]["mean"],
        "p_W_eq_1_given_s5": res_s6["mean"], "p_W_le_5_given_s5": res_le5_s5["mean"],
        "p_W_eq_1_20y_given_s4": res_s6_s4["mean"], "p_W_le_5_20y_given_s4": res["le5_20"]["mean"],
        "note_s7": "Export both W=1 (strict scenario text singleton) and W<=5 (tiny junta) as S7 inputs.",
    },
    "samples": {
        "note": "p_* samples are noise-shrunk per-draw probabilities (epistemic only).",
        "p_s5_given_s4": r4(samp.choice(ps5_shrunk, ns, replace=False)),
        "p_s6_given_s5": r4(ps6_shrunk),
        "s5_year": r4(samp.choice(y5, ns, replace=False)),
        "s5_lag_after_s4": r4(samp.choice(lag5, ns, replace=False)),
        "s6_year": r4(samp.choice(y6, min(ns, y6.size), replace=False)),
        "s6_lag_after_s5": r4(samp.choice(lag6, min(ns, lag6.size), replace=False)),
    },
}
with open(RES, "w") as fh:
    json.dump(out, fh, indent=1)

# ----------------------------------------------------------------------------------------
# figures
# ----------------------------------------------------------------------------------------
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

os.makedirs(FIG, exist_ok=True)
fig, ax = plt.subplots(1, 3, figsize=(16, 4.6))
keys = ["act", "neg", "ware", "exit_reform_redistribution", "exit_coup_collapse",
        "exit_ai_takeover_independent", "exit_external_intervention"]
labels = ["Active\ndepop.", "Passive\nneglect", "Warehousing", "Reform /\nredistrib.", "Coup\ncollapse",
          "Indep. AI\ntakeover", "External\nintervention"]
cols = ["#b2182b", "#ef8a62", "#4d9221", "#2166ac", "#67a9cf", "#762a83", "#878787"]
vals = [res[k]["mean"] for k in keys]
lo = [res[k]["mean"] - res[k]["epistemic_p05"] for k in keys]
hi = [res[k]["epistemic_p95"] - res[k]["mean"] for k in keys]
ax[0].bar(range(len(keys)), vals, color=cols, yerr=[lo, hi], capsize=3, error_kw=dict(lw=0.8))
ax[0].set_xticks(range(len(keys))); ax[0].set_xticklabels(labels, fontsize=7)
ax[0].set_ylabel("Probability within 20 yrs of S4")
ax[0].set_title("Outcomes given S4 (exclusive; bars = epistemic 5-95%)", fontsize=10)
for i, v in enumerate(vals):
    ax[0].text(i + 0.15, v + 0.005, f"{v:.2f}", fontsize=8)
ax[1].hist(ps5_shrunk, bins=40, alpha=0.7, color="#b2182b", density=True,
           label=f"P(S5|S4) mean {res['s5']['mean']:.2f}")
ax[1].hist(ps6_shrunk, bins=40, alpha=0.6, color="#2166ac", density=True,
           label=f"P(S6|S5) mean {res_s6['mean']:.2f}")
ax[1].set_xlabel("Per-draw probability (noise-corrected epistemic spread)"); ax[1].legend(fontsize=8)
ax[1].set_title("Parameter uncertainty", fontsize=10)
vn = ["baseline_same_seed", "psi_uniform_scenario_maximal", "neglect_never_atrocity",
      "neglect_always_atrocity", "no_coups", "consolidation_tuned_to_personalism_prior", "scenario_maximal_psiU_neglect_atrocity_boost"]
vl = ["baseline", "psi U(0,1)", "neglect never\natrocity", "neglect always\natrocity", "no coups",
      "consolidation tuned\nto personalism", "all scenario text-\nmaximal choices"]
ax[2].barh(range(len(vn)), [variants[v]["P_S6_given_S5"] for v in vn], color="#2166ac")
ax[2].set_yticks(range(len(vn))); ax[2].set_yticklabels(vl, fontsize=8); ax[2].invert_yaxis()
for i, v in enumerate(vn):
    ax[2].text(variants[v]["P_S6_given_S5"] + 0.003, i, f"{variants[v]['P_S6_given_S5']:.2f}", va="center", fontsize=8)
ax[2].set_xlabel("P(S6 | S5)"); ax[2].set_title("Structural variants", fontsize=10)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "m5_depopulation_singleton_outcomes.png"), dpi=130); plt.close(fig)

fig, ax = plt.subplots(figsize=(8, 4.3))
bins = np.arange(2028, 2111, 2)
ax.hist(y5, bins=bins, alpha=0.7, color="#b2182b", label=f"S5 depopulation (median {y5q[1]:.0f})", density=True)
ax.hist(y6, bins=bins, alpha=0.6, color="#2166ac", label=f"S6 singleton (median {y6q[1]:.0f})", density=True)
ax.set_xlabel("Calendar year (conditional on stage occurring)"); ax.set_ylabel("Density")
ax.set_title("Timing of S5 and S6 given S4 (S4 year from M4)")
ax.legend(); fig.tight_layout()
fig.savefig(os.path.join(FIG, "m5_depopulation_singleton_timeline.png"), dpi=130); plt.close(fig)

# ----------------------------------------------------------------------------------------
print(f"runtime {runtime:.1f}s (main {runtime_main:.1f}s)")
print("S5", slim(res["s5"]))
print("  act", slim(res["act"]), "\n  neg", slim(res["neg"]), "\n  ware", res["ware"]["mean"], "s5b", res["s5b"]["mean"])
print("  exits", {k: round(res[k]["mean"], 4) for k in res if k.startswith("exit_")})
print("ref model", ref)
print("channels", chan)
print("S6|S5", slim(res_s6), "main-run", res_s6_main["mean"], "before-S5 share", s6_before_share)
print("W<=5|S5", res_le5_s5["mean"], " W=1 20y|S4", res_s6_s4["mean"], " W<=5 20y|S4", res["le5_20"]["mean"],
      " W=1|S4,noS5", res_s6_nos5["mean"])
print("variants", variants)
print("S5 year", y5q, "lag", lag5q, "onset lag", lag5oq, "onset<=10y", p_onset_le10)
print("S6 year", y6q, "lag", lag6q)
print("ware|no exit", ware_given_no_exit)
print("sens5", top5)
print("sens6", top6)
