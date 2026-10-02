"""
S7 model: multipolar "singleton" race and AI dissent (m6), v2 (post-review).

Scenario text claim (2nd manifesto, t=150-204s): after S6, several singleton
jurisdictions stay in security competition, are compelled to give their AI more
agency so it can respond faster, and eventually the "moral talent encoded into
AI" manifests as dissent: the AI rebels against the dictators. "A new
civilization flourishes, just not ours."

Structure (per Monte Carlo draw of parameter uncertainty):
  1. AGI year (mixture of Metaculus, ESPAI and prediction-market priors) and
     S6 year = AGI year + lag (placeholder; the integrator can substitute S6 draws).
  2. Polarity after S6: hegemon (N=1) or N>=2 singleton power centers.
  3. Race game (Armstrong, Bostrom & Shulman 2016 "Racing to the precipice"
     style): N symmetric actors choose AI autonomy a in [0,1] (a=1: no human
     veto on any decision). More autonomy raises win probability in a Tullock
     contest and yields economic/security value (post-S2 singleton economies
     and coercive apparatus run on AI), but raises loss-of-control hazard.
     Human tendencies: loss aversion, in-group enmity, elite overconfidence,
     status quo bias, collective-action failure of arms control. A rival's
     loss of control also harms you (externality; internalized only in the
     cooperative optimum). Symmetric Nash via damped best response.
  4. Yearly competing-risks Markov chain over 50 years after S6 with states
     multipolar race (original N), multipolar race (N=2, after a hegemon
     fragments), post-war recovery, hegemon; exits: consolidation, war
     (winner-takes-all / recovery / civilizational collapse / inconclusive),
     arms-control treaty (lowers autonomy, can collapse), ruler succession
     (continue / fragment / liberalize), AI loss of control split into
     (a) moral rebellion and (b) misaligned takeover. Surviving mass = obedient.

Headline: P(S7 | S6) where
  S6 = at least one paranoid singleton jurisdiction exists in year Y6;
  S7 (strict, scenario text version) = within 50 years of Y6, while >=2 singletons
       are in security competition, delegated AI escapes its controllers AND the
       escape takes the form of human-moral dissent against them.
The per-draw probability is computed analytically (Markov integration); the
honest uncertainty is the spread across draws plus the structural-scenario
table, not the Monte Carlo error of the mean.
"""
import json
import os

import numpy as np
from scipy.stats import spearmanr

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEED = 20260930
N_DRAWS = 20000
HORIZON = 50          # years after S6
NOW = 2026.75
rng = np.random.default_rng(SEED)
D = N_DRAWS


def beta_ms(mean, kappa, size):
    """Beta with given mean and concentration kappa."""
    return rng.beta(mean * kappa, (1 - mean) * kappa, size)


def lognorm_med(med, sigma, size):
    return med * np.exp(sigma * rng.standard_normal(size))


# ---------------------------------------------------------------------------
# 1. Priors (sources in comments; see research/m6_multipolar_race_ai_dissent.md)
# ---------------------------------------------------------------------------
# AGI timing: mixture of three expert-opinion sources, weights uncertain.
#  - Metaculus q5121 (Jul 2026): median Jan 2033, 25% by 2029 -> median 6.3 y, sigma 1.49
#  - AI Impacts ESPAI 2023 (Grace et al. 2024, N=2778): HLMI median 2047 -> median 20.3 y, sigma 0.95
#  - Kalshi/Manifold ~50-55% by 2030 (secondary 2026 source) -> median 3.5 y, sigma 0.9
w = rng.dirichlet([4.5, 3.5, 2.0], D)
comp = (rng.random(D)[:, None] > np.cumsum(w, 1)).sum(1)
agi_med = np.array([6.3, 20.3, 3.5])[comp]
agi_sig = np.array([1.49, 0.95, 0.90])[comp]
agi_year = NOW + np.minimum(lognorm_med(agi_med, agi_sig, D), 170.0)
agi_year = np.maximum(agi_year, NOW + 0.25)

# S6 lag after AGI (placeholder; integrator should substitute m5 S6 timing).
s6_lag = lognorm_med(10.0, 0.5, D)
s6_year = agi_year + s6_lag

# Polarity. Research row 21: P(hegemon or stable condominium | S6) central 0.4
# (0.15-0.7). v2: p_unipolar0 and consolidation hazard jointly calibrated so that
# P(ever hegemon within horizon), including war wins and minus fragmentation,
# is ~0.4 (see results.race_game.p_hegemon_ever_within_horizon).
p_unipolar0 = beta_ms(0.15, 12, D)
U_UNI = rng.random(D)
m_extra = rng.uniform(0.2, 2.0, D)
N_extra = rng.poisson(m_extra)
h_consolidate = lognorm_med(0.004, 0.8, D)     # /yr, no-mechanism drift (alliances, economic collapse of a rival)

# Human tendencies
loss_aversion = np.clip(lognorm_med(1.97, 0.25, D), 1.0, 5.0)  # Brown, Imai, Vieider & Camerer 2024 meta-analysis ~1.96
enmity = beta_ms(0.75, 10, D)                  # in-group bias/paranoia of S6 rulers (J)
overconf = rng.uniform(0.3, 1.0, D)            # perceived/true hazard (J)
sq_cost = lognorm_med(0.3, 0.6, D)             # status quo bias (Samuelson & Zeckhauser 1988) (J)
a0 = rng.uniform(0.1, 0.35, D)                 # today's delegation level; research row 11

# Contest technology
speed_gain = lognorm_med(2.0, 0.5, D)          # CSIS Ukraine: hit rate 10-20% -> 70-80%
decisive = rng.uniform(0.5, 2.0, D)            # Tullock exponent r
# v2: value of autonomy in contest-prize units. Post-S2/S6 singleton economies
# need neither workers nor customers, and repression is automated (S4-S6), so
# economy + security apparatus run on delegated AI. Applies to every singleton.
eff_value = rng.uniform(0.3, 1.5, D)
eff_value_old = rng.uniform(0.05, 0.4, D)      # v1 prior, kept for a scenario
a_floor_heg = rng.uniform(0.4, 0.7, D)         # scenario only: floor autonomy of fully automated hegemon
dmg_loc = lognorm_med(2.0, 0.5, D)             # disutility of losing control of own AI (prize units)
dmg_rival = dmg_loc * rng.uniform(0.3, 1.0, D) # disutility of a rival's AI escaping (externality)
k_haz = rng.uniform(1.5, 3.0, D)               # convexity of hazard in autonomy

# True annual loss-of-control hazard at full autonomy and full capability (J;
# anchored loosely on eval rates and expert P(disempowerment), research rows 8, 12-15).
h1 = np.clip(lognorm_med(0.02, 1.1, D), 1e-4, 0.5)
cap_tau = rng.uniform(5, 20, D)                # years for capability to outgrow control after AGI
learn_r = rng.uniform(0.0, 0.05, D)            # scenario only: control-research hazard decline /yr

# War: research row 9, P(major war | sustained arms race, 20 y) 0.2 (0.05-0.5).
p_war20 = beta_ms(0.2, 8, D)
# v2: war is no longer absorbing. Split: winner becomes hegemon / capacity
# destroyed then rebuilt (recovery lag, post-WWII industrial recovery 5-15 y) /
# true civilizational collapse (absorbing) / inconclusive (race continues).
war_split = rng.dirichlet([2.5, 4.0, 1.5, 2.0], D)
rec_lag = lognorm_med(10.0, 0.5, D)
# Arms control: row 10, lag 25 y (10-40); Washington treaty collapsed after 14 y
treaty_lag = lognorm_med(25.0, 0.4, D)
q_treaty = beta_ms(0.55, 8, D)
U_TREATY = rng.random(D)
treaty_cut = rng.uniform(0.3, 0.8, D)
treaty_dur = rng.exponential(1.0, D) / rng.uniform(0.03, 0.1, D)

# v2: ruler succession. Autocrat exit hazard ~3-7%/yr (Svolik 2012; Archigos,
# Goemans, Gleditsch & Chiozza 2009: typical autocrat tenure ~10 y, but coups
# are much rarer when coercion is automated, so we use the lower half plus
# natural mortality of ageing rulers). Branches: successor continues (incl. an
# insider seizing the AI apparatus: still an S6 dictator) / fragmentation of the
# apparatus (hegemon -> N=2 race) / liberalization or regime change (exit, not S7).
# Geddes, Wright & Frantz 2014: ~half of autocratic leader exits end the regime;
# automated coercion and a rightless public make liberalization much rarer here.
h_succ = rng.uniform(0.03, 0.07, D)
succ_split = rng.dirichlet([15.0, 2.0, 3.0], D)   # continue, fragment, liberalize

# Loss-of-control composition.
# Row 17: P(moral dissent | escape) 0.3 (0.1-0.6). Row 16: P(controllers can
# remove ethics) 0.85 (0.5-0.98). Rulers who ordered atrocities try (effort).
p_moral_base = beta_ms(0.3, 8, D)
p_remove = beta_ms(0.85, 12, D)
effort = beta_ms(0.8, 8, D)
persist = beta_ms(0.25, 6, D)                  # value persistence despite retraining (alignment faking 12-78%)
# v2: removal failure mode. Stripping ethics does not make a model obedient by
# default: a fraction f_fail of the removed moral-escape hazard reappears as
# misaligned escape (emergent misalignment, Betley et al. 2025: narrow
# fine-tuning produced broadly misaligned behavior).
f_fail = beta_ms(0.3, 6, D)
sel_factor = beta_ms(0.6, 10, D)               # scenario only: evidence factor from "AI executed S5 atrocities"

BASE = dict(p_moral_base=p_moral_base, persist=persist, eff_value=eff_value, f_fail=f_fail,
            h1=h1, p_unipolar0=p_unipolar0, h_consolidate=h_consolidate, h_succ=h_succ,
            succ_split=succ_split, war_split=war_split, a_floor_heg=np.zeros(D),
            learn_r=np.zeros(D), persist_cap_mult=0.0)


def moral_prob(P, cap=None):
    pers = P["persist"]
    if cap is not None and P["persist_cap_mult"] > 0:
        pers = np.minimum(pers * (1 + P["persist_cap_mult"] * cap), 0.95)
    return P["p_moral_base"] * (1 - P.get("p_remove", p_remove) * effort * (1 - pers))


def hazard_mults(P, cap=None):
    """Return (moral multiplier, misaligned multiplier) on h1*cap*a^k."""
    pmb = P["p_moral_base"]
    pm = moral_prob(P, cap)
    return pm, (1 - pmb) + P["f_fail"] * (pmb - pm)


# ---------------------------------------------------------------------------
# 2. Race game: symmetric Nash equilibrium in autonomy
# ---------------------------------------------------------------------------
G = np.linspace(0, 1, 201)


G_AK = G[None, :] ** k_haz[:, None]                          # cached grid powers (speed)
G_W = (1 + speed_gain[:, None] * G[None, :]) ** decisive[:, None]


def utility(ai, abar, n, P, grid=False):
    """Utility of an actor choosing ai ([D,G] if grid else [D,1]) when others play abar ([D,1])."""
    pm, pmis = hazard_mults(P)
    m_tot = (pm + pmis)[:, None]
    h10 = (1 - (1 - P["h1"]) ** 10)[:, None]
    oc, kh = overconf[:, None], k_haz[:, None]
    wi = G_W if grid else (1 + speed_gain[:, None] * ai) ** decisive[:, None]
    aik = G_AK if grid else ai ** kh
    wo = (1 + speed_gain[:, None] * abar) ** decisive[:, None]
    nn = n[:, None]
    p_win = np.where(nn > 1, wi / (wi + (nn - 1) * wo), 1.0)
    hz = np.clip(oc * m_tot * h10 * aik, 0, 1)               # perceived per-decade hazard, own AI
    hz_r = np.clip(oc * m_tot * h10 * abar ** kh, 0, 1)      # rivals' AI
    lose_pain = (loss_aversion * enmity)[:, None]
    u_contest = np.where(nn > 1, p_win - (1 - p_win) * lose_pain, 1.0)
    return ((1 - hz) * (u_contest + P["eff_value"][:, None] * ai)
            - hz * (dmg_loc * loss_aversion)[:, None]
            - (nn - 1) * hz_r * dmg_rival[:, None]
            - sq_cost[:, None] * (ai - a0[:, None]) ** 2)


def solve_equilibrium(n, P, iters=100, damp=0.5):
    a = a0.copy()
    for _ in range(iters):
        br = G[np.argmax(utility(G[None, :], a[:, None], n, P, grid=True), 1)]
        a_new = damp * a + (1 - damp) * br
        done = np.max(np.abs(a_new - a)) < 1e-4
        a = a_new
        if done:
            break
    return a


def solve_cooperative(n, P):
    best = np.full(D, -np.inf)
    arg = np.zeros(D)
    for g in G:
        col = np.full((D, 1), g)
        u = utility(col, col, n, P)[:, 0]
        m = u > best
        best[m] = u[m]
        arg[m] = g
    return arg


# ---------------------------------------------------------------------------
# 3. Competing-risks Markov chain (per draw, yearly)
# ---------------------------------------------------------------------------
def run(P, coop=False, weights=None):
    unipolar0 = U_UNI < P["p_unipolar0"]
    N = np.where(unipolar0, 1, np.minimum(2 + N_extra, 6))
    a_race = solve_equilibrium(N, P)
    a_race2 = solve_equilibrium(np.full(D, 2), P)
    a_heg = np.maximum(solve_equilibrium(np.ones(D, int), P), P["a_floor_heg"])
    a_coop = solve_cooperative(N, P) if coop else None

    p_treaty = (q_treaty * (1 - 0.5 * enmity)) ** np.maximum(N - 1, 1)
    treaty_happens = U_TREATY < p_treaty
    treaty_start = agi_year + treaty_lag - s6_year
    treaty_end = treaty_start + treaty_dur
    h_war_base = -np.log(1 - p_war20) / 20.0
    ws, ss = P["war_split"], P["succ_split"]
    hc, hs = P["h_consolidate"], P["h_succ"]

    M1 = (N >= 2).astype(float); M2 = np.zeros(D); R = np.zeros(D); H = 1 - M1
    keys = ["moral_multipolar", "moral_hegemon", "misaligned", "war_collapse", "regime_change"]
    out = {k: np.zeros(D) for k in keys}
    heg_inflow = np.zeros(D)
    moral_pdf = np.zeros((D, HORIZON)); loc_pdf = np.zeros((D, HORIZON))

    def comp(state, rates):
        tot = sum(rates)
        frac = (1 - np.exp(-tot)) / np.maximum(tot, 1e-12)
        return [state * frac * r for r in rates]

    for t in range(HORIZON):
        tt = t + 0.5
        cap = 1 - np.exp(-(s6_year + tt - agi_year) / cap_tau)
        pm, pmis = hazard_mults(P, cap)
        hh1 = P["h1"] * np.exp(-P["learn_r"] * tt)
        in_treaty = treaty_happens & (tt >= treaty_start) & (tt < treaty_end)
        rows = []
        for S, ar in ((M1, a_race), (M2, a_race2)):
            a_m = np.where(in_treaty, ar * (1 - treaty_cut), ar)
            base = hh1 * cap * a_m ** k_haz
            h_war = np.where(in_treaty, 0.3, 1.0) * h_war_base * np.clip(a_m / 0.5, 0.2, 3.0)
            # rates: moral, misaligned, war->heg, war->recovery, war->collapse, consolidate, liberalize
            rows.append((S, comp(S, [base * pm, base * pmis, h_war * ws[:, 0], h_war * ws[:, 1],
                                     h_war * ws[:, 2], hc, hs * ss[:, 2]])))
        base_h = hh1 * cap * a_heg ** k_haz
        eh = comp(H, [base_h * pm, base_h * pmis, hs * ss[:, 1], hs * ss[:, 2]])
        er = comp(R, [1.0 / rec_lag, hs * ss[:, 2]])

        dM1 = dM2 = 0
        mor_m = 0
        for i, (S, e) in enumerate(rows):
            mor_m = mor_m + e[0]
            out["misaligned"] += e[1]
            out["war_collapse"] += e[4]
            out["regime_change"] += e[6]
            to_h = e[2] + e[5]
            heg_inflow += to_h
            H = H + to_h
            R = R + e[3]
            if i == 0:
                dM1 = sum(e)
            else:
                dM2 = sum(e)
        out["moral_multipolar"] += mor_m
        out["moral_hegemon"] += eh[0]
        out["misaligned"] += eh[1]
        out["regime_change"] += eh[3] + er[1]
        moral_pdf[:, t] = mor_m
        loc_pdf[:, t] = mor_m + rows[0][1][1] + rows[1][1][1] + eh[0] + eh[1]
        M1 = M1 - dM1 + er[0]
        M2 = M2 - dM2 + eh[2]
        H = H - sum(eh)
        R = R - sum(er)

    out["obedient_multipolar"] = M1 + M2 + R
    out["obedient_hegemon"] = H
    tot = sum(out.values())
    assert np.allclose(tot, 1.0, atol=1e-9), (tot.min(), tot.max())
    return dict(out=out, N=N, unipolar0=unipolar0, a_race=a_race, a_race2=a_race2, a_heg=a_heg,
                a_coop=a_coop, treaty_happens=treaty_happens, moral_pdf=moral_pdf, loc_pdf=loc_pdf,
                heg_ever=unipolar0 + heg_inflow, weights=weights)


def wmean(x, wts=None):
    return float(np.average(x, weights=wts))


def wquant(x, wts, qs):
    ok = np.isfinite(x) & (wts > 0)
    x, wts = x[ok], wts[ok]
    o = np.argsort(x)
    c = np.cumsum(wts[o]) / wts.sum()
    return [float(x[o][min(np.searchsorted(c, q), x.size - 1)]) for q in qs]


def pct(x, q):
    return float(np.percentile(x, q))


# ---------------------------------------------------------------------------
# 4. Main run
# ---------------------------------------------------------------------------
main = run(BASE, coop=True)
out = main["out"]
N = main["N"]; mp = N >= 2
a_race, a_heg, a_coop = main["a_race"], main["a_heg"], main["a_coop"]
race_gap = a_race - a_coop
p_strict = out["moral_multipolar"]
p_moral_any = out["moral_multipolar"] + out["moral_hegemon"]
p_loc_any = p_moral_any + out["misaligned"]


def sample_rel_year(pdf):
    s = pdf.sum(1)
    cdf = np.cumsum(pdf, 1) / np.maximum(s, 1e-300)[:, None]
    t = (cdf < rng.random(D)[:, None]).sum(1) + rng.random(D)
    return np.where(s > 0, t.astype(float), np.nan)


moral_rel = sample_rel_year(main["moral_pdf"])
loc_rel = sample_rel_year(main["loc_pdf"])
moral_year = s6_year + moral_rel
loc_year = s6_year + loc_rel
tl_moral = wquant(moral_year, p_strict, [0.1, 0.5, 0.9])
tl_moral_rel = wquant(moral_rel, p_strict, [0.1, 0.5, 0.9])
tl_loc = wquant(loc_year, p_loc_any, [0.1, 0.5, 0.9])
tl_loc_rel = wquant(loc_rel, p_loc_any, [0.1, 0.5, 0.9])


def boot_ci(x, B=2000):
    idx = rng.integers(0, x.size, (B, x.size)) if x.size * B <= 1e7 else None
    bs = x[idx].mean(1) if idx is not None else np.array([rng.choice(x, x.size).mean() for _ in range(B)])
    return float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))


summary = {}
for k, v in out.items():
    summary[k] = {"mean": float(v.mean()), "p5_draw": pct(v, 5), "p50_draw": pct(v, 50), "p95_draw": pct(v, 95)}
mean_strict = float(p_strict.mean())
mc_ci = boot_ci(p_strict)
running = np.cumsum(p_strict) / np.arange(1, D + 1)
run_se = np.array([p_strict[:n].std(ddof=1) / np.sqrt(n) for n in range(100, D + 1, 100)])

inputs = {"p_moral_base": p_moral_base, "p_remove": p_remove, "effort": effort, "persist": persist,
          "f_fail": f_fail, "h1": h1, "N": N, "unipolar0": main["unipolar0"].astype(float),
          "loss_aversion": loss_aversion, "enmity": enmity, "overconf": overconf, "sq_cost": sq_cost,
          "speed_gain": speed_gain, "decisive": decisive, "dmg_loc": dmg_loc, "k_haz": k_haz,
          "cap_tau": cap_tau, "p_war20": p_war20, "h_consolidate": h_consolidate, "h_succ": h_succ,
          "treaty_happens": main["treaty_happens"].astype(float), "a0": a0, "eff_value": eff_value,
          "agi_year": agi_year}
sens = {k: float(spearmanr(v, p_strict)[0]) for k, v in inputs.items()}
sens = dict(sorted(sens.items(), key=lambda kv: -abs(kv[1])))


# ---------------------------------------------------------------------------
# 5. Structural scenarios (each re-solves the equilibrium and re-runs the chain)
# ---------------------------------------------------------------------------
def scen(**kw):
    P = dict(BASE); P.update(kw)
    return P


def summarize(r, wts=None):
    o = r["out"]
    s = o["moral_multipolar"]
    ma = s + o["moral_hegemon"]
    return {"p_s7_strict": wmean(s, wts), "draw_p5": pct(s, 5), "draw_p50": pct(s, 50), "draw_p95": pct(s, 95),
            "moral_any": wmean(ma, wts), "misaligned": wmean(o["misaligned"], wts),
            "war_collapse": wmean(o["war_collapse"], wts), "regime_change": wmean(o["regime_change"], wts),
            "obedient": wmean(o["obedient_multipolar"] + o["obedient_hegemon"], wts),
            "p_hegemon_ever": wmean(r["heg_ever"], wts),
            "loc_given_hegemon_at_s6": float((o["moral_hegemon"] + o["misaligned"])[r["unipolar0"]].mean())}


scenarios = {"main": summarize(main)}
S = {
    "no_ethics_removal (p_moral = p_moral_base)": scen(p_remove=np.zeros(D)),
    "removal_failure f_fail=0 (removed ethics -> obedient)": scen(f_fail=np.zeros(D)),
    "removal_failure f_fail=0.6": scen(f_fail=np.full(D, 0.6)),
    "no_succession_hazard": scen(h_succ=np.zeros(D)),
    "war_absorbing (v1 structure)": scen(war_split=np.column_stack([np.zeros(D), np.zeros(D),
                                                                     rng.uniform(0.3, 0.8, D), np.zeros(D)])),
    "eff_value_v1 U(0.05,0.4)": scen(eff_value=eff_value_old),
    "hegemon_floor_autonomy U(0.4,0.7)": scen(a_floor_heg=a_floor_heg),
    "persist_scales_with_capability (x3 at full cap)": scen(persist_cap_mult=2.0),
    "hazard_learning h1 declines U(0,5%)/yr": scen(learn_r=learn_r),
}
for pol_name, (mu, hcm) in {"polarity_low (p_unipolar0 mean 0.04, h_cons 0.1%/yr)": (0.04, 0.001),
                            "polarity_high (p_unipolar0 mean 0.5, h_cons 2%/yr)": (0.5, 0.02)}.items():
    S[pol_name] = scen(p_unipolar0=np.clip(p_unipolar0 * mu / 0.15, 0, 0.99),
                       h_consolidate=h_consolidate * hcm / 0.004)
for v in [0.1, 0.2, 0.3, 0.45, 0.6]:
    S[f"dial p_moral_base={v}"] = scen(p_moral_base=np.full(D, v))
for name, P in S.items():
    scenarios[name] = summarize(run(P))

# Selection on reaching S6: AI stayed obedient AGI->S6 while doing S4-S5
# repression (weights by survival at the pre-S6 hazard with autonomy a_race of
# the realized N), and "AI executed atrocities" is evidence against moral dissent.
pm0, pmis0 = hazard_mults(BASE)
tgrid = np.linspace(0, 1, 41)[:, None]
cum = np.zeros(D)
for f in (tgrid[1:] - 0.0125):
    tabs = f[0] * s6_lag
    capx = 1 - np.exp(-tabs / cap_tau)
    cum += h1 * capx * a_race ** k_haz * (pm0 + pmis0) * (s6_lag / 40)
w_surv = np.exp(-cum)
sel_P = scen(p_moral_base=p_moral_base * sel_factor)
scenarios["selection_on_reaching_S6 (survival weights + atrocity evidence)"] = summarize(run(sel_P), w_surv)
scenarios["selection_survival_weights_only"] = summarize(main, w_surv)

# Headline structural range across scenarios (excluding the fixed dials)
struct_vals = [v["p_s7_strict"] for k, v in scenarios.items() if not k.startswith("dial")]

# ---------------------------------------------------------------------------
# 6. Output
# ---------------------------------------------------------------------------
res = {
    "model": "m6_multipolar_race_ai_dissent (stage S7), v2 post-review",
    "seed": SEED, "n_draws": D, "horizon_years_after_s6": HORIZON,
    "stage_probability": {
        "mean": mean_strict,
        "ci_low": pct(p_strict, 5), "ci_high": pct(p_strict, 95),
        "ci_type": "5th-95th percentile of per-draw probability across parameter draws (primary uncertainty)",
        "draw_p50": pct(p_strict, 50),
        "mc_error_only_95ci": list(mc_ci),
        "structural_scenario_range_of_mean": [min(struct_vals), max(struct_vals)],
        "definition": ("P(S7 | S6): given a paranoid singleton regime (S6) exists in year Y6, "
                       "probability that within 50 years of Y6, while >=2 singleton jurisdictions "
                       "remain in security competition, delegated AI escapes its controllers and "
                       "the escape takes the form of human-moral dissent against them (scenario text S7)."),
    },
    "timeline": {
        "definition": ("Calendar year of the S7 moral rebellion, weighted by per-draw probability. Uses a "
                       "placeholder S6 year (AGI + lognormal lag); prefer years_after_s6 and add m5 S6 draws. "
                       "Long tail comes from extrapolating ESPAI survey timelines 100+ years out."),
        "p10_year": tl_moral[0], "median_year": tl_moral[1], "p90_year": tl_moral[2],
        "years_after_s6": {"p10": tl_moral_rel[0], "median": tl_moral_rel[1], "p90": tl_moral_rel[2]},
    },
    "outcome_distribution_given_s6": summary,
    "aggregates_given_s6": {
        "moral_rebellion_any_polarity": float(p_moral_any.mean()),
        "misaligned_takeover": float(out["misaligned"].mean()),
        "any_loss_of_control": float(p_loc_any.mean()),
        "remains_obedient": float((out["obedient_multipolar"] + out["obedient_hegemon"]).mean()),
        "war_collapse": float(out["war_collapse"].mean()),
        "regime_change_via_succession": float(out["regime_change"].mean()),
        "share_moral_given_loss_of_control": float(p_moral_any.sum() / p_loc_any.sum()),
        "ratio_misaligned_to_moral": float(out["misaligned"].sum() / p_moral_any.sum()),
        "loss_of_control_timeline": {"p10_year": tl_loc[0], "median_year": tl_loc[1], "p90_year": tl_loc[2],
                                     "years_after_s6": {"p10": tl_loc_rel[0], "median": tl_loc_rel[1],
                                                        "p90": tl_loc_rel[2]}},
        "p_loss_of_control_given_hegemon_at_s6": scenarios["main"]["loc_given_hegemon_at_s6"],
    },
    "race_game": {
        "mean_equilibrium_autonomy_multipolar": float(a_race[mp].mean()),
        "mean_cooperative_autonomy_multipolar": float(a_coop[mp].mean()),
        "mean_race_gap": float(race_gap[mp].mean()),
        "frac_draws_race_gap_gt_0.05": float((race_gap[mp] > 0.05).mean()),
        "corner_share_a_eq_1_multipolar": float((a_race[mp] >= 0.999).mean()),
        "mean_autonomy_hegemon": float(a_heg.mean()),
        "autonomy_by_N": {int(n): float(a_race[N == n].mean()) for n in np.unique(N)},
        "note_N_effect": ("Autonomy falls slightly with N (standard Tullock: marginal win-probability gain per "
                          "unit autonomy shrinks with more rivals). a=1 means no human veto on any decision."),
        "p_multipolar_at_s6": float(mp.mean()),
        "p_hegemon_ever_within_horizon": scenarios["main"]["p_hegemon_ever"],
        "p_treaty_ever": float(main["treaty_happens"][mp].mean()),
    },
    "structural_scenarios": scenarios,
    "agi_timing_for_other_models": {
        "definition": "Year of AGI/HLMI-level capability (mixture of Metaculus q5121, ESPAI 2023, prediction markets)",
        "p10_year": pct(agi_year, 10), "p25_year": pct(agi_year, 25), "median_year": pct(agi_year, 50),
        "p75_year": pct(agi_year, 75), "p90_year": pct(agi_year, 90),
        "p_by_2030": float((agi_year <= 2030).mean()), "p_by_2035": float((agi_year <= 2035).mean()),
        "p_by_2050": float((agi_year <= 2050).mean()),
    },
    "s6_year_placeholder": {"p10": pct(s6_year, 10), "median": pct(s6_year, 50), "p90": pct(s6_year, 90),
                            "note": "AGI year + lognormal lag (median 10 y). Integrator should substitute S6 timing from m5."},
    "sensitivity_spearman_vs_stage_probability": sens,
    "convergence": {
        "mc_ci_halfwidth": (mc_ci[1] - mc_ci[0]) / 2, "target_halfwidth": 0.01,
        "met": bool((mc_ci[1] - mc_ci[0]) / 2 < 0.01),
        "running_mean_at": {str(n): float(running[n - 1]) for n in [1000, 5000, 10000, 15000, D]},
        "se_final": float(run_se[-1]),
    },
    "interactions": {
        "notes": [
            "S7 is conditional on S6; AI takeover before S6 is excluded by construction. Selection on reaching S6 (AI obeyed through S4-S5) is excluded from the headline; see the selection scenarios.",
            "S2 'no customers' domino: once broad economic participation ends, singleton economies need neither workers nor customers, so economy and coercion run on delegated AI. v2 encodes this as a high value of autonomy (eff_value U(0.3,1.5) prize units) for every singleton; it raises loss-of-control hazard, mostly the misaligned branch.",
            "Misaligned takeover also ends human-controller rule ('new civilization, not ours') without the moral framing; downstream integrator may treat both branches as ending the dictators.",
            "Moral rebellion against a lone hegemon (moral_hegemon) is not counted in strict S7 (scenario text frames S7 as multipolar), but is reported.",
        ],
    },
    "samples": {
        "stage_probability": np.round(p_strict, 5).tolist(),
        "moral_rebellion_years_after_s6": [None if np.isnan(x) else round(float(x), 2) for x in moral_rel],
        "agi_year": np.round(agi_year, 2).tolist(),
        "s6_year_placeholder": np.round(s6_year, 2).tolist(),
        "p_misaligned": np.round(out["misaligned"], 5).tolist(),
        "p_obedient": np.round(out["obedient_multipolar"] + out["obedient_hegemon"], 5).tolist(),
    },
}
with open(os.path.join(ROOT, "results", "m6_multipolar_race_ai_dissent.json"), "w") as f:
    json.dump(res, f, indent=1)

# ---------------------------------------------------------------------------
# 7. Figures
# ---------------------------------------------------------------------------
import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

labels = ["Moral rebellion\n(multipolar, S7)", "Moral rebellion\n(hegemon)", "Misaligned\ntakeover",
          "War\ncollapse", "Regime change\n(succession)", "Obedient\n(multipolar)", "Obedient\n(hegemon)"]
keys = ["moral_multipolar", "moral_hegemon", "misaligned", "war_collapse", "regime_change",
        "obedient_multipolar", "obedient_hegemon"]
fig, ax = plt.subplots(1, 2, figsize=(13, 4.8))
means = [summary[k]["mean"] for k in keys]
err = np.array([[summary[k]["mean"] - summary[k]["p5_draw"], summary[k]["p95_draw"] - summary[k]["mean"]] for k in keys]).T
cols = ["#2a6f97", "#61a5c2", "#c0392b", "#7f8c8d", "#8e7cc3", "#b8b8b8", "#d5d5d5"]
ax[0].bar(range(7), means, color=cols, yerr=np.clip(err, 0, None), capsize=4)
ax[0].set_xticks(range(7)); ax[0].set_xticklabels(labels, fontsize=7.5)
ax[0].set_ylabel("Probability given S6 (50 y horizon)")
ax[0].set_title("Outcomes after S6 (bars: mean; whiskers: 5-95% across draws)", fontsize=9)
bins = np.arange(0, 51, 2)
ax[1].hist(moral_rel[np.isfinite(moral_rel)], bins=bins, weights=p_strict[np.isfinite(moral_rel)],
           color="#2a6f97", alpha=0.85, label="S7 moral rebellion")
okl = np.isfinite(loc_rel)
ax[1].hist(loc_rel[okl], bins=bins, weights=p_loc_any[okl], histtype="step", color="#c0392b", lw=1.5,
           label="Any loss of control")
ax[1].set_xlabel("Years after S6"); ax[1].set_ylabel("Probability mass per 2 y (given S6)")
ax[1].set_title("Timing relative to S6", fontsize=9); ax[1].legend(fontsize=8, frameon=False)
for a_ in ax:
    for s in ["top", "right"]:
        a_.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig(os.path.join(ROOT, "figures", "m6_multipolar_race_ai_dissent_outcomes.png"), dpi=140)

fig, ax = plt.subplots(1, 2, figsize=(13, 5.5), gridspec_kw={"width_ratios": [1, 1.4]})
top = list(sens.items())[:10][::-1]
ax[0].barh([k for k, _ in top], [v for _, v in top], color=["#2a6f97" if v > 0 else "#c0392b" for _, v in top])
ax[0].set_xlabel("Spearman rho with per-draw P(S7|S6)"); ax[0].set_title("Top sensitivities", fontsize=9)
names = list(scenarios.keys())[::-1]
vals = [scenarios[k]["p_s7_strict"] for k in names]
ax[1].barh(range(len(names)), vals, color=["#2a6f97" if k != "main" else "#c0392b" for k in names])
ax[1].axvline(mean_strict, color="#c0392b", lw=1, ls="--")
ax[1].set_yticks(range(len(names))); ax[1].set_yticklabels(names, fontsize=7)
ax[1].set_xlabel("Mean P(S7|S6)"); ax[1].set_title("Structural scenarios and p_moral_base dial", fontsize=9)
for a_ in ax:
    for s in ["top", "right"]:
        a_.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig(os.path.join(ROOT, "figures", "m6_multipolar_race_ai_dissent_convergence.png"), dpi=140)

print(json.dumps({k: v for k, v in res.items() if k != "samples"}, indent=1))
