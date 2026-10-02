"""
m7_decentralized_alternative.py  (v2, after review)
===================================================
Stage "AltA-AltB" of the 2nd-manifesto simulation.

Alt B (best case): decentralized, permissionless AI (consensus network, distilled frontier
capability in a shared substrate) gains adoption faster than the economy is automated and
wins on price inside the ordinary economy.

Alt A: people pushed out of the formal economy by the "no customers" domino form a parallel
economy / currency that excludes centralized AI providers; the public's survival then depends
on the AI elite / state tolerating it.

Model (v2)
----------
1. Automation A(t): logistic in an "effective time" whose speed responds to demand
   (firms with no customers may stop investing, or revenue pressure may accelerate automation;
   sign uncertain, m2 found the net effect near zero) and to cheap decentralized AI. Optional
   capability plateau. "Economy automated" := A >= 0.5 (t_auto).
2. AI market as three options per unit of workload (tokens):
     closed frontier  price 1 + markup (markup only if provider concentration, S3)
     open-weight on centralized hosts  price r_open*(1 + oms*markup), quality lag qpen
     permissionless network  price r_open*r_cost*(1 - subsidy discount), same qpen,
                             plus permissionless-specific friction (privacy, SLAs, legal)
   Buyers have heterogeneous non-price friction f_i ~ lognormal(f_med, sigma_f) across workload.
   f_med is ANCHORED to revealed preference: at the 2025-26 open-vs-closed price gap
   (open 3-10x cheaper), open-weight holds only 11% (Menlo, enterprise) to 33% (OpenRouter,
   developer tokens) of workload, so f_med is solved per draw such that the model reproduces
   an anchor share in U(0.11,0.25) at t0. Revealed preference already contains status quo bias
   and loss aversion, so no separate switching cost and no individual-level lambda is applied to
   it; a firm-level lambda U(1.0,1.5) multiplies only the (unanchored) permissionless friction.
   Non-closed workload target N = P(f_i < best gain). Split between permissionless and
   open-centralized by a logit on the utility difference. Plus a niche segment (censorship-
   resistant, sanctioned, privacy) that uses permissionless regardless, a large-player tipping
   hazard, and demand from the parallel economy. D moves toward its target by Bass diffusion
   (innovation term NOT gated by gain) or churns down.
   Alt B success := permissionless workload share D >= 0.25 AND permissionless quality-adjusted
   price below closed price, at some t <= min(t_auto, 2060). Co-optation (incumbents capture the
   protocol, AWS-on-Linux) is drawn separately: B_structural = B and not co-opted.
   Second, broader "S3-averting" metric W = D + selfhost share of open-weight workload.
3. No-customers domino (user's S2): direct job loss = A*exposure*displacement*(1 - new jobs),
   B2B/second round follows client demand loss with a lag (B2B runway) and multiplier;
   UBI/redistribution replaces part of lost income; Alt B network rewards are modelled
   explicitly as per-capita income against lost wages (no assumed cap). AI spend M growth
   falls with uncompensated exclusion. S2_m7 := uncompensated excluded share >= 0.25 for 2 years.
   NOTE: m2 is the canonical S2 model; m7's S2 is only used as the conditioning set for Alt A.
4. Parallel economy P(t): critical-mass push, in-group bonus, loss-domain risk seeking,
   scaled by resource access (land/energy/compute not enclosed by the automated elite) and a
   productivity boost if open/decentralized models remain usable locally. Collapse hazard is a
   mixture of trueque-like (0.3-0.6/yr) and institutionalised (0.02-0.10/yr) systems, rising
   when resource access falls.
5. Tolerance game: each year
       Delta = V_res*P + V_tax*P*(1-A) + paranoia - C_enf*(1-A) - C_legit*democracy(t)
               - C_valve*E*(1-A)      (safety valve loses value as coercion is automated)
   Suppression effectiveness rises with automated coercion: e_t = e + (1-e)*A (cap 0.97), and
   permanently cuts the join propensity (legal risk).
   Alt A(w) := forms (P >= 10%) by 2055 and is still >= 5% w years later without having been
   suppressed below 5% in between. Reported for w = 5, 10, 15 years; headline w = 10.
"""
import json
import os

import numpy as np
from scipy.special import ndtr, ndtri

SEED = 20260930
N = 40_000
T0, T1, T1A, DT = 2026.75, 2060.0, 2075.0, 0.25
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(BASE, "results")
FIG = os.path.join(BASE, "figures")

D_WIN = 0.25      # permissionless share of AI workload that counts as "winning"
A_CRIT = 0.5      # automation level that counts as "economy automated"
E_S2 = 0.25       # uncompensated excluded share that counts as the no-customers domino (S2)
P_FORM = 0.10     # parallel-economy participation that counts as "formed"
P_SURV = 0.05     # participation floor for "still exists"
WINDOWS = (5, 10, 15)
W_HEAD = 10
GDP0 = 115_000.0  # world GDP 2026, $B (IMF WEO ~ $115T)
LABOUR_SHARE = 0.55

# name: (distribution, args, source / rationale)
PRIORS = {
    # --- automation trajectory (S1) ---
    "t50_years": ("lognormal", (13.0, 0.55),
                  "Years from 2026 to A=0.5. ESPAI 2023 (Grace et al. 2024) HLMI 50% by 2047; Metaculus AGI "
                  "~2033; plus adoption lag (Comin & Hobijn 2010). Median 2039, p10~2033, p90~2052."),
    "A0": ("uniform", (0.02, 0.08), "Realised automation share late 2026 (Anthropic Economic Index; Eloundou 2023)."),
    "p_plateau": ("uniform", (0.15, 0.40), "P(capability plateau); judgement."),
    "plateau_year": ("uniform", (2028.0, 2040.0), "judgement"),
    "A_cap_plateau": ("uniform", (0.30, 0.80), "Automation ceiling if plateau; judgement (Eloundou et al. 2023)."),
    "fb_A": ("uniform", (-0.4, 0.2),
             "Automation-speed response per unit uncompensated exclusion: negative = firms with no customers "
             "stop investing, positive = revenue pressure accelerates. m2 found net feedback ~ +0.5-1.5%."),
    "accel_D": ("uniform", (0.0, 0.3), "Automation speed-up per unit permissionless share (cheaper AI)."),
    # --- AI market ---
    "D0_spend": ("lognormal", (0.0008, 0.7),
                 "Permissionless share of AI spend 2026: DePIN ~$200-300M vs AI infra spend (Messari, blockeden); "
                 "Bittensor verified revenue $3-45M/yr (Pine Analytics). Converted to workload share via prices."),
    "r_open": ("uniform", (0.10, 0.33),
               "Open-weight (centrally hosted) price relative to closed frontier, 3-10x cheaper (OpenRouter/a16z)."),
    "r0": ("lognormal", (2.3, 0.255),
           "Unsubsidized permissionless / centralized-hosting cost ratio for the same model, 2.3 (1.6-3.5), Pine."),
    "r_floor": ("uniform", (0.6, 1.2), "Structural permissionless relative cost at scale; judgement."),
    "learning_rate": ("uniform", (0.10, 0.25), "Cost drop per doubling of D (Wright's law; Way et al. 2022)."),
    "g_rel": ("normal", (0.0, 0.03), "Exogenous relative cost drift per year; judgement."),
    "subsidy0_B": ("uniform", (0.3, 1.0), "Token-emission subsidy $B/yr (emissions ~20x revenue, Pine); halves / 4y."),
    "M0_B": ("uniform", (100.0, 250.0), "2026 AI workload spend $B (hyperscaler capex ~$700B, CNBC 2026)."),
    "M_growth": ("uniform", (0.15, 0.35), "Annual AI spend growth at full demand; Epoch trends."),
    "m_dem": ("uniform", (0.5, 1.5), "Reduction of AI spend growth per unit uncompensated exclusion (demand link)."),
    "open_lag_months": ("lognormal", (4.5, 0.45), "Open-weight lag 3-12 months (Epoch open-closed ECI gap)."),
    "quality_per_month": ("uniform", (0.01, 0.04), "Price-equivalent quality penalty per month of lag; judgement."),
    "h_open_stop": ("uniform", (0.01, 0.06), "Hazard/yr that leading labs stop releasing weights (m3 research)."),
    "decentral_train_lag_months": ("uniform", (36.0, 60.0),
                                   "If open releases stop: permissionless training ~1000x compute behind, 3-5 y "
                                   "(Covenant-72B arXiv 2603.08163)."),
    # --- adoption behaviour ---
    "anchor_share": ("uniform", (0.11, 0.25),
                     "Non-closed (open-weight) workload share at the 2025-26 price gap: Menlo 2025 enterprise 11% "
                     "(19% in 2024), OpenRouter 33% of tokens (developer-skewed). Revealed preference; anchors f_med."),
    "sigma_f": ("uniform", (0.8, 1.5), "Dispersion of buyer friction (log units); judgement, heterogeneous niches."),
    "g_fric": ("uniform", (-0.04, 0.02), "Friction drift per year (tooling maturation vs enterprise share falling "
                                          "2024->25); judgement."),
    "frontier_part": ("uniform", (0.3, 0.8), "Part of friction that is frontier-capability demand (decays under plateau)."),
    "squeeze": ("uniform", (0.0, 0.5), "Friction reduction per unit uncompensated exclusion (squeezed firms)."),
    "perm_fric0": ("uniform", (0.05, 0.30), "Permissionless-specific friction at tiny scale (privacy to anonymous "
                                            "nodes, SLAs, compliance), price units; falls with network size."),
    "D_crit": ("uniform", (0.02, 0.10), "Network size at which permissionless friction falls by 1/e; judgement."),
    "lambda_firm": ("uniform", (1.0, 1.5), "Firm-level loss aversion on permissionless friction only (B2B "
                                           "procurement; individual TK lambda ~2 not applied)."),
    "ideology": ("uniform", (0.0, 0.08), "Private premium for decentralization; small (Olson 1965)."),
    "anger": ("uniform", (0.0, 0.30), "Protest migration per unit markup (Mastodon retention ~30%)."),
    "beta_split": ("uniform", (5.0, 15.0), "Logit sensitivity of permissionless vs open-centralized split."),
    "niche0": ("uniform", (0.002, 0.02), "Niche workload using permissionless regardless (censorship-resistant, "
                                         "sanctioned jurisdictions, privacy, batch); judgement."),
    "h_tip": ("uniform", (0.0, 0.02), "Hazard/yr of a large player (state, consortium) unilaterally adopting."),
    "tip_size": ("uniform", (0.03, 0.12), "Workload added by a tipping event."),
    "par_ai": ("uniform", (0.05, 0.3), "Permissionless workload per unit parallel-economy participation."),
    "bass_p": ("uniform", (0.005, 0.03), "Bass innovation coef (Sultan, Farley & Lehmann 1990: mean 0.03)."),
    "bass_q": ("uniform", (0.20, 0.60), "Bass imitation coef (Sultan et al. 1990: mean 0.38)."),
    "churn": ("uniform", (0.10, 0.40), "Annual churn toward lower target (BitTorrent -90%, TorrentFreak)."),
    "kappa_O": ("uniform", (0.3, 0.8), "Adjustment speed of open-centralized share per year."),
    "selfhost": ("uniform", (0.3, 0.6), "Share of open-weight workload self-hosted / off top-N providers."),
    "p_coopt": ("uniform", (0.2, 0.5), "P(incumbents co-opt the protocol so markups persist after B), AWS-on-Linux."),
    "reward_share": ("uniform", (0.05, 0.30), "Share of permissionless spend paid out as network rewards."),
    "reward_breadth": ("uniform", (0.1, 0.5), "Share of rewards reaching excluded workers (vs capital holders)."),
    # --- centralized providers (S3 interaction) ---
    "p_conc": ("uniform", (0.20, 0.50), "P(tight oligopoly with pricing power): m3 research."),
    "markup_max": ("lognormal", (0.5, 0.6), "Extractable markup if concentrated (Nvidia ~75% GM, AWS ~35% OM)."),
    "oms": ("uniform", (0.3, 1.0), "Share of markup passed to open-weight hosting (runs on concentrated compute)."),
    "A_conc": ("uniform", (0.20, 0.50), "Automation level at which dependence lets providers raise prices."),
    "incumbent_response": ("uniform", (0.3, 0.9), "Share of markup given up as D reaches ~10% (limit pricing)."),
    # --- state ---
    "p_state_support": ("uniform", (0.15, 0.45), "P(material public/open AI subsidy, EU/Swiss Apertus/India)."),
    "state_support_cut": ("uniform", (0.05, 0.25), "Open-weight cost cut from public support (NOT permissionless)."),
    "D_threat": ("uniform", (0.03, 0.15), "Share at which states see permissionless AI as a threat."),
    "crack_rate": ("uniform", (0.03, 0.25), "Annual crackdown prob at full rentier dependence (Tornado Cash)."),
    "crack_eff": ("uniform", (0.15, 0.40), "Share of D removed by crackdown (China mining 34%->0->14-20%)."),
    "crack_friction": ("uniform", (0.1, 0.3), "Permanent permissionless friction added after crackdown."),
    # --- no-customers domino (S2) ---
    "exposure": ("uniform", (0.5, 0.85), "Workforce share in automatable categories (Eloundou et al. 2023)."),
    "displace": ("uniform", (0.5, 1.0), "Job loss per unit task automation (reinstatement/price-elasticity effects, "
                                         "Acemoglu & Restrepo 2019)."),
    "new_jobs": ("uniform", (0.1, 0.6), "Share of lost jobs recreated early (Autor et al. 2024)."),
    "nj_decay": ("uniform", (0.3, 1.0), "How much new-job creation shrinks as A->1."),
    "domino_mult": ("uniform", (0.2, 0.8), "B2B/second-round job loss per unit uncompensated demand loss."),
    "b2b_lag": ("uniform", (1.0, 3.0), "Years of B2B runway before client demand loss hits (user's S2)."),
    "p_ubi": ("uniform", (0.40, 0.75), "P(substantial income replacement); m2: P(large transfer by 2060)=0.63."),
    "ubi_trigger": ("uniform", (0.08, 0.20), "Excluded share that triggers redistribution."),
    "ubi_cov": ("uniform", (0.3, 0.9), "Share of lost income replaced."),
    "ubi_erosion": ("uniform", (0.0, 0.10), "Annual erosion of coverage (rentier state logic)."),
    # --- parallel economy (Alt A) ---
    "join": ("uniform", (0.2, 0.6), "Share of uncompensated excluded who join; trueque 2002 (IPS)."),
    "cm_threshold": ("uniform", (0.05, 0.20), "Critical-mass push before joining starts (Granovetter 1978)."),
    "ingroup": ("uniform", (0.0, 0.5), "In-group network bonus to joining."),
    "loss_aversion": ("uniform", (1.5, 2.5), "Individual lambda (TK 1992: 2.25; Brown et al. 2024: ~1.96)."),
    "loss_domain": ("uniform", (0.0, 0.3), "Extra risk seeking in loss domain per unit (lambda-1)."),
    "currency_form": ("uniform", (0.4, 1.0), "Share of parallel activity in a distinct AI-excluding system."),
    "kappa": ("uniform", (0.3, 1.0), "Adjustment speed of participation per year."),
    "p_inst": ("uniform", (0.3, 0.7), "P(parallel economy is institutionalised, WIR-like) vs trueque-like."),
    "h_inst": ("uniform", (0.02, 0.10), "Collapse hazard/yr, institutionalised (WIR 90 years)."),
    "h_trueque": ("uniform", (0.30, 0.60), "Collapse hazard/yr, crisis-grown weakly governed (trueque -85% in ~1y)."),
    "collapse_frac": ("uniform", (0.7, 0.9), "Participants lost in a collapse (IPS 2002)."),
    "local_own": ("uniform", (0.1, 0.5), "Share of land/energy/means held by the public outside elite control."),
    "enclosure": ("uniform", (0.3, 1.0), "Fraction of the rest enclosed by the automated elite as A->1."),
    "open_boost": ("uniform", (0.0, 0.5), "Parallel-economy productivity boost from local open/decentralized models."),
    # --- tolerance game ---
    "V_res": ("uniform", (0.5, 3.0), "Elite value of land/energy held by parallel economy (per unit P)."),
    "V_tax": ("uniform", (0.5, 3.0), "Value of formal tax base eroded (per unit P)."),
    "paranoia": ("uniform", (-0.3, 0.3), "Threat perception offset."),
    "C_enf": ("uniform", (0.1, 0.6), "Enforcement cost before coercion automated."),
    "C_legit": ("uniform", (0.1, 0.8), "Legitimacy cost under full democratic accountability."),
    "C_valve": ("uniform", (0.0, 1.0), "Safety-valve value per unit E, scaled by (1-A) (S4: unrest stops mattering)."),
    "democracy0": ("uniform", (0.4, 1.0), "Initial democratic accountability."),
    "ai_tax_share_max": ("uniform", (0.4, 0.9), "AI-firm share of tax base at full automation (rentier)."),
    "h_supp_max": ("uniform", (0.15, 0.60), "Max annual suppression prob; calibrated so formed parallel economies "
                                            "face ~0.5-0.7 suppression within a decade (m7 research)."),
    "supp_scale": ("uniform", (0.1, 0.4), "Noise scale of elite decision."),
    "supp_eff": ("uniform", (0.3, 0.8), "Share removed by suppression before automation (China ban, Woergl)."),
    "supp_join_cut": ("uniform", (0.2, 0.6), "Permanent cut in join propensity after suppression (legal risk)."),
}


def draw(rng, n, override=None):
    pri = dict(PRIORS)
    if override:
        pri.update(override)
    p = {}
    for k, (dist, a, *_) in pri.items():
        if dist == "uniform":
            p[k] = rng.uniform(a[0], a[1], n)
        elif dist == "normal":
            p[k] = rng.normal(a[0], a[1], n)
        elif dist == "lognormal":
            p[k] = a[0] * np.exp(rng.normal(0, a[1], n))
        elif dist == "const":
            p[k] = np.full(n, float(a[0]))
    p["open_lag_months"] = np.clip(p["open_lag_months"], 2, 18)
    p["D0_spend"] = np.clip(p["D0_spend"], 1e-4, 0.01)
    p["t50_years"] = np.maximum(p["t50_years"], 3.0)
    p["width_years"] = 2 * np.log(9) * (p["t50_years"] - (T0 - 2026.0)) / np.log((1 - p["A0"]) / p["A0"])
    p["plateau"] = rng.uniform(size=n) < p["p_plateau"]
    p["conc"] = rng.uniform(size=n) < p["p_conc"]
    p["state_support"] = rng.uniform(size=n) < p["p_state_support"]
    p["state_support_year"] = rng.uniform(2027, 2032, n)
    p["ubi_enacts"] = rng.uniform(size=n) < p["p_ubi"]
    p["coopt"] = rng.uniform(size=n) < p["p_coopt"]
    p["inst"] = rng.uniform(size=n) < p["p_inst"]
    # anchored friction median: CDF_f(u_O at t0) = anchor_share
    q0 = p["open_lag_months"] * p["quality_per_month"]
    u0 = 1 - p["r_open"] * (1 + q0)
    p["u_anchor"] = u0
    p["f_med0"] = u0 * np.exp(-ndtri(p["anchor_share"]) * p["sigma_f"])
    return p


def sig(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -50, 50)))


DEFAULT_VAR = dict(d_win=D_WIN, a_crit=A_CRIT, share="workload", fric_mult=1.0, lam_double=False,
                   niche=True, tip=True, access=True, supp_new=True, valve_new=True, open_boost=True,
                   hazard="mixture")


def simulate(p, rng, keep_paths=0, **var):
    v = dict(DEFAULT_VAR); v.update(var)
    n = len(p["D0_spend"])
    times = np.arange(T0, T1A + 1e-9, DT)
    nt = len(times)
    k = 2 * np.log(9) / p["width_years"]
    t50 = 2026.0 + p["t50_years"]
    idx = np.arange(n)

    # initial workload share of permissionless from spend share
    sub_disc0 = np.minimum(0.7, p["subsidy0_B"] / (p["D0_spend"] * p["M0_B"]))
    price_perm0 = p["r_open"] * p["r0"] * (1 - sub_disc0)
    avg_price0 = (1 - p["anchor_share"]) + p["anchor_share"] * p["r_open"]
    D = np.clip(p["D0_spend"] * avg_price0 / price_perm0, 5e-4, 0.05)
    D_init = D.copy()
    O = np.maximum(p["anchor_share"] - D, 0.01)
    te = np.full(n, T0)
    M = p["M0_B"].copy()
    niche_extra = np.zeros(n)
    tipped = np.zeros(n, bool)
    crack = np.zeros(n, bool)
    extra_fric = np.zeros(n)
    open_stopped = np.zeros(n, bool)

    t_auto = np.full(n, np.inf); t_B = np.full(n, np.inf); t_W = np.full(n, np.inf)
    t_S2 = np.full(n, np.inf); t_form = np.full(n, np.inf)
    t_supp_fail = np.full(n, np.inf); t_first_supp = np.full(n, np.inf)
    ubi_on = np.zeros(n, bool); t_ubi = np.full(n, np.inf)
    s2_run = np.zeros(n)
    Pp = np.zeros(n)
    join = p["join"].copy()
    P_at = {w: np.full(n, np.nan) for w in WINDOWS}
    ever_supp = np.zeros(n, bool)
    peak_P = np.zeros(n); peak_E = np.zeros(n); peak_push = np.zeros(n)
    markup_hist = np.zeros(n); covB_max = np.zeros(n)
    lag_steps = np.round(p["b2b_lag"] / DT).astype(int)
    direct_hist = np.zeros((nt, n))
    push = np.zeros(n)
    snaps = {}
    paths = {"t": times, "A": [], "D": [], "W": [], "E": [], "P": []} if keep_paths else None
    if v["hazard"] == "mixture":
        h_col = np.where(p["inst"], p["h_inst"], p["h_trueque"])
    elif v["hazard"] == "inst":
        h_col = p["h_inst"]
    else:
        h_col = p["h_trueque"]

    for i, t in enumerate(times):
        tau = t - 2026.0
        # ---- automation with demand feedback ----
        speed = np.maximum(0.2, 1 + p["fb_A"] * push + p["accel_D"] * D)
        if i > 0:
            te = te + DT * speed
        A = sig(k * (te - t50))
        capA = np.where(p["plateau"] & (t > p["plateau_year"]), p["A_cap_plateau"], 1.0)
        A = np.minimum(A, np.maximum(capA, sig(k * (p["plateau_year"] - t50))))
        newly = (A >= v["a_crit"]) & np.isinf(t_auto) & (t <= T1)
        t_auto[newly] = t

        # ---- prices ----
        markup = np.where(p["conc"], p["markup_max"] * sig((A - p["A_conc"]) / 0.05), 0.0)
        markup = markup * (1 - p["incumbent_response"] * D / (D + 0.1) * 2.0).clip(0, 1)
        markup_hist = np.maximum(markup_hist, markup)
        P_closed = 1 + markup
        sup = p["state_support"] & (t >= p["state_support_year"])
        P_open = p["r_open"] * (1 + p["oms"] * markup) * np.where(sup, 1 - p["state_support_cut"], 1.0)
        ratio = np.maximum(D / D_init, 1.0)
        b = -np.log2(1 - p["learning_rate"])
        r_cost = np.maximum(p["r_floor"], p["r0"] * ratio ** (-b)) * np.exp(p["g_rel"] * tau)
        # permissionless runs on independent compute: no markup; priced vs base open hosting cost
        price_perm_raw = p["r_open"] * r_cost
        avg_price = (1 - D - O) * P_closed + O * P_open + D * price_perm_raw
        D_spend = D * price_perm_raw / avg_price
        subsidy = p["subsidy0_B"] * 0.5 ** (tau / 4.0)
        sub_disc = np.minimum(0.7, subsidy / np.maximum(D_spend * M, 1e-6))
        P_perm = price_perm_raw * (1 - sub_disc)
        stop = rng.uniform(size=n) < p["h_open_stop"] * DT
        open_stopped |= stop
        lag_now = np.where(open_stopped, p["decentral_train_lag_months"], p["open_lag_months"])
        qpen = np.minimum(1.5, lag_now * p["quality_per_month"])
        plat_dec = np.where(p["plateau"] & (t > p["plateau_year"]),
                            0.5 ** (np.maximum(t - p["plateau_year"], 0) / 3.0), 1.0)
        qpen = qpen * plat_dec
        u_O = 1 - P_open * (1 + qpen) / P_closed
        pf = p["perm_fric0"] * np.exp(-D / p["D_crit"]) + extra_fric
        lam = p["loss_aversion"] if v["lam_double"] else p["lambda_firm"]
        u_D = (1 - P_perm * (1 + qpen) / P_closed - lam * pf + p["ideology"] + p["anger"] * markup)
        perm_cheaper = P_perm * (1 + qpen) < P_closed

        # ---- no-customers domino (S2) ----
        n_eff = p["new_jobs"] * (1 - p["nj_decay"] * A)
        direct = A * p["exposure"] * p["displace"] * (1 - n_eff)
        direct_hist[i] = direct
        lagged = direct_hist[np.maximum(i - lag_steps, 0), idx]
        cov = np.where(ubi_on, p["ubi_cov"] * np.exp(-p["ubi_erosion"] * np.maximum(t - t_ubi, 0)), 0.0)
        E = np.minimum(0.95, direct + p["domino_mult"] * lagged * (1 - cov))
        GDP = GDP0 * np.exp(0.025 * tau) * (1 - LABOUR_SHARE * push)
        rewards = p["reward_share"] * D_spend * M * p["reward_breadth"]
        covB = np.minimum(0.9, rewards / (LABOUR_SHARE * GDP * np.maximum(E, 0.01)))
        covB_max = np.maximum(covB_max, covB)
        push = E * (1 - cov) * (1 - covB)
        new_ubi = p["ubi_enacts"] & ~ubi_on & (E >= p["ubi_trigger"])
        ubi_on |= new_ubi
        t_ubi[new_ubi] = t
        s2_run = np.where(push >= E_S2, s2_run + DT, 0.0)
        newS2 = (s2_run >= 2.0 - 1e-9) & np.isinf(t_S2) & (t <= T1)
        t_S2[newS2] = t - 2.0 + DT
        peak_E = np.maximum(peak_E, E); peak_push = np.maximum(peak_push, push)
        M = np.minimum(M * np.exp(p["M_growth"] * (1 - p["m_dem"] * push) * DT), 8000.0)

        # ---- adoption targets ----
        fmed = (v["fric_mult"] * p["f_med0"] * np.exp(p["g_fric"] * tau)
                * (1 - p["frontier_part"] + p["frontier_part"] * plat_dec)
                * (1 - p["squeeze"] * push))
        u_best = np.maximum(u_O, u_D)
        Ntar = np.where(u_best > 0, ndtr((np.log(np.maximum(u_best, 1e-9)) - np.log(fmed)) / p["sigma_f"]), 0.0)
        sD = sig(p["beta_split"] * (u_D - u_O))
        if v["tip"]:
            tip_now = (~tipped) & (rng.uniform(size=n) < p["h_tip"] * DT) & (t <= T1)
            niche_extra = np.where(tip_now, niche_extra + p["tip_size"], niche_extra)
            tipped |= tip_now
        niche = (p["niche0"] if v["niche"] else 0.0) + niche_extra + p["par_ai"] * Pp
        niche = niche * np.where(crack, 1 - p["crack_eff"], 1.0)
        D_tar = np.minimum(0.99, niche + (1 - niche) * Ntar * sD)
        O_tar = (1 - niche) * Ntar * (1 - sD)
        up = D_tar > D
        dD = np.where(up, (p["bass_p"] + p["bass_q"] * D / np.maximum(D_tar, 1e-4)) * (D_tar - D),
                      p["churn"] * (D_tar - D))
        D = np.clip(D + dD * DT, 1e-5, 0.99)
        O = np.clip(O + p["kappa_O"] * (O_tar - O) * DT, 0.0, 0.99 - D)
        # state crackdown (rentier dependence ~ A)
        risk = (~crack) & (D > p["D_threat"])
        hit = risk & (rng.uniform(size=n) < p["crack_rate"] * (0.3 + A) * DT)
        D = np.where(hit, D * (1 - p["crack_eff"]), D)
        extra_fric = np.where(hit, p["crack_friction"], extra_fric)
        crack |= hit

        if v["share"] == "workload":
            shareD = D
        else:
            shareD = D * P_perm / ((1 - D - O) * P_closed + O * P_open + D * P_perm)
        winB = (shareD >= v["d_win"]) & perm_cheaper & np.isinf(t_B) & (t <= t_auto) & (t <= T1)
        t_B[winB] = t
        W = D + p["selfhost"] * O
        winW = (W >= D_WIN) & np.isinf(t_W) & (t <= t_auto) & (t <= T1)
        t_W[winW] = t

        # ---- parallel economy (Alt A) ----
        access = (p["local_own"] + (1 - p["local_own"]) * (1 - p["enclosure"] * A)) if v["access"] else 1.0
        aiavail = np.where(open_stopped, 0.5, 1.0) * np.where(crack, 0.7, 1.0)
        boost = p["open_boost"] * aiavail if v["open_boost"] else 0.0
        active = push > p["cm_threshold"]
        j_eff = join * (1 + p["loss_domain"] * (p["loss_aversion"] - 1))
        target = np.where(active, push * j_eff * p["currency_form"] * (1 + p["ingroup"] * Pp / (Pp + 0.05))
                          * access * (1 + 0.5 * boost), 0.0)
        Pp = np.clip(Pp + p["kappa"] * (target - Pp) * DT, 0, 0.9)
        # scale-dependent hazard: weakly governed systems become fragile as they grow (trueque grew for
        # 7 years at low hazard, then collapsed ~85% within a year of peaking at ~7-10% of population)
        h_base = np.where(p["inst"], p["h_inst"], p["h_inst"] + (h_col - p["h_inst"]) * np.minimum(1.0, Pp / P_FORM))
        if v["hazard"] != "mixture":
            h_base = h_col if v["hazard"] == "inst" else p["h_inst"] + (h_col - p["h_inst"]) * np.minimum(1.0, Pp / P_FORM)
        h_now = h_base * (1 + 2 * (1 - access)) / (1 + boost)
        col = (Pp >= P_SURV) & (rng.uniform(size=n) < h_now * DT)
        Pp = np.where(col, Pp * (1 - p["collapse_frac"]), Pp)
        join = np.where(col, join * 0.5, join)
        newform = (Pp >= P_FORM) & np.isinf(t_form)
        t_form[newform] = t
        formed = np.isfinite(t_form)
        dem = p["democracy0"] * (1 - A * p["ai_tax_share_max"])
        valve = p["C_valve"] * E * ((1 - A) if v["valve_new"] else 1.0)
        delta = (p["V_res"] * Pp + p["V_tax"] * Pp * (1 - A) + p["paranoia"]
                 - p["C_enf"] * (1 - A) - p["C_legit"] * dem - valve)
        psupp = p["h_supp_max"] * sig(delta / p["supp_scale"])
        supp = formed & (Pp >= P_SURV) & (rng.uniform(size=n) < psupp * DT)
        if v["supp_new"]:
            e_t = np.minimum(0.97, p["supp_eff"] + (1 - p["supp_eff"]) * A)
            join = np.where(supp, join * (1 - p["supp_join_cut"]), join)
        else:
            e_t = p["supp_eff"]
        Pp = np.where(supp, Pp * (1 - e_t), Pp)
        t_first_supp[supp & ~ever_supp] = t
        ever_supp |= supp
        fail = supp & (Pp < P_SURV) & np.isinf(t_supp_fail)
        t_supp_fail[fail] = t
        peak_P = np.maximum(peak_P, Pp)
        for w in WINDOWS:
            chk = formed & np.isnan(P_at[w]) & (t >= t_form + w - 1e-9)
            P_at[w][chk] = Pp[chk]

        for yr in (2030, 2035, 2040, 2050):
            if abs(t - yr) < 1e-9:
                snaps[yr] = dict(D=D.copy(), W=W.copy(), Dspend=D_spend.copy(), push=push.copy())
        if keep_paths:
            paths["A"].append(A[:keep_paths]); paths["D"].append(D[:keep_paths])
            paths["W"].append(W[:keep_paths])
            paths["E"].append(push[:keep_paths]); paths["P"].append(Pp[:keep_paths])

    B = np.isfinite(t_B)
    S2 = np.isfinite(t_S2)
    formedA = np.isfinite(t_form) & (t_form <= 2055)
    Aw = {}
    for w in WINDOWS:
        tol = formedA & ~(t_supp_fail <= t_form + w)
        Aw[w] = tol & (P_at[w] >= P_SURV)
    return dict(t_auto=t_auto, t_B=t_B, B=B, B_struct=B & ~p["coopt"], t_W=t_W, W=np.isfinite(t_W),
                t_S2=t_S2, S2=S2, t_form=t_form, formedA=formedA, Aw=Aw, A=Aw[W_HEAD],
                t_first_supp=t_first_supp, ever_supp=ever_supp, peak_P=peak_P, peak_E=peak_E,
                peak_push=peak_push, covB_max=covB_max, snaps=snaps, markup_max_seen=markup_hist,
                crack=crack, open_stopped=open_stopped, tipped=tipped, paths=paths)


def boot_ci(x, rng, nb=1000):
    x = np.asarray(x, float)
    if len(x) == 0:
        return (np.nan, np.nan)
    m = np.array([x[rng.integers(0, len(x), len(x))].mean() for _ in range(nb)])
    return (float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5)))


def qyears(t):
    t = t[np.isfinite(t)]
    if len(t) == 0:
        return dict(p10_year=None, median_year=None, p90_year=None, n=0)
    return dict(p10_year=float(np.percentile(t, 10)), median_year=float(np.percentile(t, 50)),
                p90_year=float(np.percentile(t, 90)), n=int(len(t)))


def tercile_delta(x, y):
    """P(y | top tercile of x) - P(y | bottom tercile of x)."""
    x = np.asarray(x, float); y = np.asarray(y, float)
    if len(x) < 30 or np.all(x == x[0]):
        return 0.0
    lo, hi = np.percentile(x, [33.33, 66.67])
    if lo == hi:  # binary
        return float(y[x > lo].mean() - y[x <= lo].mean()) if (x > lo).any() else 0.0
    return float(y[x >= hi].mean() - y[x <= lo].mean())


def run_variant(n, seed, override=None, **var):
    r = np.random.default_rng(seed)
    p = draw(r, n, override)
    o = simulate(p, r, **var)
    c = o["S2"] & ~o["B"]
    return {"P(B)": float(o["B"].mean()), "P(B struct)": float(o["B_struct"].mean()),
            "P(W>=25% before t_auto)": float(o["W"].mean()),
            **{f"P(A{w}|S2,notB)": float(o["Aw"][w][c].mean()) for w in WINDOWS},
            "P(S2_m7)": float(o["S2"].mean())}


def main():
    rng = np.random.default_rng(SEED)
    p = draw(rng, N)
    out = simulate(p, rng, keep_paths=400)
    brng = np.random.default_rng(SEED + 1)

    B = out["B"].astype(float)
    pB, ciB = B.mean(), boot_ci(B, brng)
    condA = out["S2"] & ~out["B"]
    A_c = out["A"][condA].astype(float)
    pA, ciA = A_c.mean(), boot_ci(A_c, brng)
    Aw_c = {w: float(out["Aw"][w][condA].mean()) for w in WINDOWS}
    formed_c = float(out["formedA"][condA].mean())
    fA = out["formedA"]
    f10 = fA & (out["t_form"] <= 2050)
    supp10 = float((out["t_first_supp"][f10] <= out["t_form"][f10] + 10).mean())
    joint = {
        "P(B)": float(out["B"].mean()),
        "P(B and not co-opted)": float(out["B_struct"].mean()),
        "P(A10 tolerated, no B)": float((out["A"] & ~out["B"]).mean()),
        "P(A10 and B both)": float((out["A"] & out["B"]).mean()),
        "P(A10 | S2, B)": float(out["A"][out["S2"] & out["B"]].mean()) if (out["S2"] & out["B"]).any() else None,
        "P(S2_m7 | B)": float(out["S2"][out["B"]].mean()) if out["B"].any() else None,
        "P(S2_m7 | not B)": float(out["S2"][~out["B"]].mean()),
    }

    # ---- structural variants (20k each, common seed) ----
    NS, SS = 20000, SEED + 7
    Bvars = {
        "baseline": ({}, {}),
        "share measured in spend (not workload)": ({}, {"share": "spend"}),
        "D_win = 0.10": ({}, {"d_win": 0.10}),
        "D_win = 0.50": ({}, {"d_win": 0.50}),
        "automation threshold A = 0.7": ({}, {"a_crit": 0.7}),
        "anchor = developer level U(0.25,0.40)": ({"anchor_share": ("uniform", (0.25, 0.40))}, {}),
        "anchor = enterprise only U(0.08,0.13)": ({"anchor_share": ("uniform", (0.08, 0.13))}, {}),
        "friction x0.5 (unanchored)": ({}, {"fric_mult": 0.5}),
        "individual lambda on perm friction": ({}, {"lam_double": True}),
        "no niche, no tipping": ({}, {"niche": False, "tip": False}),
        "no markup on open hosting (oms=0)": ({"oms": ("const", (0.0,))}, {}),
        "high friction dispersion sigma U(1.5,2.2)": ({"sigma_f": ("uniform", (1.5, 2.2))}, {}),
        "perm friction U(0.2,0.6)": ({"perm_fric0": ("uniform", (0.2, 0.6))}, {}),
    }
    Avars = {
        "collapse hazard all institutionalised": ({}, {"hazard": "inst"}),
        "collapse hazard all trueque-like": ({}, {"hazard": "trueque"}),
        "no resource-access cap": ({}, {"access": False}),
        "v1 suppression (constant eff, no join cut)": ({}, {"supp_new": False}),
        "v1 safety valve (no (1-A))": ({}, {"valve_new": False}),
        "v1 suppression + v1 valve + no access cap": ({}, {"supp_new": False, "valve_new": False, "access": False}),
        "no open-AI productivity boost": ({}, {"open_boost": False}),
        "low UBI p U(0.25,0.60) (v1)": ({"p_ubi": ("uniform", (0.25, 0.60))}, {}),
    }
    struct = {}
    for lab, (ov, kw) in {**Bvars, **Avars}.items():
        struct[lab] = run_variant(NS, SS, ov, **kw)
        print(f"{lab:45s} " + " ".join(f"{k}={v:.3f}" for k, v in struct[lab].items()))
    # headline structural ranges (exclude pure definitional thresholds D_win and A=0.7)
    defs = {"D_win = 0.10", "D_win = 0.50", "automation threshold A = 0.7"}
    vb = [s["P(B)"] for l, s in struct.items() if l in Bvars and l not in defs]
    va = {w: [s[f"P(A{w}|S2,notB)"] for l, s in struct.items() if l in Avars or l == "baseline"] for w in WINDOWS}

    # ---- P(B) as a function of the friction anchor (curve) ----
    curve = []
    for a in (0.05, 0.08, 0.11, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50):
        rr = run_variant(10000, SEED + 11, {"anchor_share": ("const", (a,))})
        curve.append({"anchor_share": a, "P(B)": rr["P(B)"], "P(W)": rr["P(W>=25% before t_auto)"]})
    curve_pf = []
    for f in (0.0, 0.05, 0.1, 0.2, 0.3, 0.5):
        rr = run_variant(10000, SEED + 12, {"perm_fric0": ("const", (max(f, 1e-6),))})
        curve_pf.append({"perm_fric0": f, "P(B)": rr["P(B)"]})

    # convergence
    cm = np.cumsum(B) / np.arange(1, N + 1)
    conv = {c: float(cm[c - 1]) for c in [1000, 2500, 5000, 10000, 20000, 40000] if c <= N}

    yrs_B = qyears(out["t_B"])
    yrs_A = qyears(np.where(out["A"], out["t_form"], np.inf))
    yrs_auto = qyears(out["t_auto"]); yrs_S2 = qyears(out["t_S2"]); yrs_W = qyears(out["t_W"])

    # sensitivities: tercile deltas of conditional probabilities
    keys = [k for k in PRIORS if not k.startswith("p_")] + ["plateau", "conc", "state_support", "ubi_enacts",
                                                           "coopt", "inst", "f_med0"]
    sensB = {k: tercile_delta(p[k], B) for k in keys}
    sensA = {k: tercile_delta(p[k][condA], A_c) for k in keys}
    topB = sorted(sensB.items(), key=lambda kv: -abs(kv[1]))[:12]
    topA = sorted(sensA.items(), key=lambda kv: -abs(kv[1]))[:12]

    def split(mask, key="B"):
        return float(out[key][mask].mean()) if mask.sum() else None
    splits = {
        "P(B | plateau)": split(p["plateau"]), "P(B | no plateau)": split(~p["plateau"]),
        "P(B | provider concentration)": split(p["conc"]), "P(B | no concentration)": split(~p["conc"]),
        "P(B | state support)": split(p["state_support"]), "P(B | no state support)": split(~p["state_support"]),
        "P(B | open releases stopped by 2075)": split(out["open_stopped"]),
        "P(B | tipping event)": split(out["tipped"]), "P(B | no tipping)": split(~out["tipped"]),
        "P(B | automation reaches 0.5 by 2060)": split(np.isfinite(out["t_auto"])),
        "P(B | automation never reaches 0.5 by 2060)": split(np.isinf(out["t_auto"])),
    }
    ubi_split = {
        "P(A10 | S2, not B, UBI enacted)": float(out["A"][condA & p["ubi_enacts"]].mean()),
        "P(A10 | S2, not B, no UBI)": float(out["A"][condA & ~p["ubi_enacts"]].mean()),
        "P(A10 | S2, not B, institutionalised)": float(out["A"][condA & p["inst"]].mean()),
        "P(A10 | S2, not B, trueque-like)": float(out["A"][condA & ~p["inst"]].mean()),
    }
    Dq = {str(y): {"D_workload_median": float(np.median(s["D"])), "D_workload_p90": float(np.percentile(s["D"], 90)),
                   "D_spend_median": float(np.median(s["Dspend"])),
                   "P(D_workload>10%)": float((s["D"] > 0.10).mean()),
                   "W_median": float(np.median(s["W"])), "P(W>25%)": float((s["W"] > 0.25).mean()),
                   "uncompensated_excluded_median": float(np.median(s["push"]))}
          for y, s in out["snaps"].items()}
    init = {"D0_workload_median": float(np.median(np.clip(p["D0_spend"] * ((1 - p["anchor_share"]) + p["anchor_share"] * p["r_open"])
                                                        / (p["r_open"] * p["r0"] * (1 - np.minimum(0.7, p["subsidy0_B"] / (p["D0_spend"] * p["M0_B"])))), 5e-4, 0.05))),
            "f_med0_median_price_units": float(np.median(p["f_med0"])),
            "f_med0_p10_p90": [float(np.percentile(p["f_med0"], 10)), float(np.percentile(p["f_med0"], 90))]}

    part = {
        "Alt B (permissionless wins before automation)": float(out["B"].mean()),
        "Alt A tolerated >=10y (no B)": float((out["A"] & ~out["B"]).mean()),
        "S2 domino, parallel economy formed but suppressed/collapsed within 10y (no B)": float(
            (out["S2"] & out["formedA"] & ~out["A"] & ~out["B"]).mean()),
        "S2 domino, no parallel economy formed (no B)": float((out["S2"] & ~out["formedA"] & ~out["B"]).mean()),
        "No S2_m7 by 2060, no B, no A (slow diffusion / redistribution / muddling)": float(
            (~out["S2"] & ~out["B"] & ~out["A"]).mean()),
        "Other (A without S2_m7, no B)": float((~out["S2"] & out["A"] & ~out["B"]).mean()),
    }

    rs = np.random.default_rng(SEED + 2)
    samp = rs.choice(N, 5000, replace=False)
    res = {
        "stage": "AltA-AltB", "version": 2, "n_runs": N, "seed": SEED,
        "stage_probability": {
            "mean": float(pB), "ci_low": ciB[0], "ci_high": ciB[1],
            "structural_range": [float(min(vb)), float(max(vb))],
            "definition": ("P(Alt B | S1): permissionless/consensus-network AI reaches >=25% of AI workload (tokens) "
                           "while its quality-adjusted price is below the closed providers', before automation "
                           "reaches 50% of professional task categories, within 2026-2060. ci = bootstrap MC error "
                           "only; structural_range = min/max across defensible specification variants (excludes "
                           "threshold changes), which is the honest uncertainty band."),
        },
        "timeline": {**{k: v for k, v in yrs_B.items() if k != "n"},
                     "definition": "Calendar year Alt B condition first met, among successful draws (few draws)."},
        "alt_B_extra": {
            "P(B and not co-opted by incumbents)": float(out["B_struct"].mean()),
            "P(S3-averting share W>=25% before automation)": float(out["W"].mean()),
            "W_definition": "W = permissionless + self-hosted/off-top-N open-weight share of workload (tokens).",
            "W_timeline": yrs_W,
            "network_income_replacement_max_median_given_B": float(np.median(out["covB_max"][out["B"]]))
            if out["B"].any() else None,
            "network_income_replacement_max_p90_given_B": float(np.percentile(out["covB_max"][out["B"]], 90))
            if out["B"].any() else None,
            "P_B_curve_vs_anchor_share": curve,
            "P_B_curve_vs_permissionless_friction": curve_pf,
            "initial_state": init,
        },
        "alt_A": {
            "probability": {"mean": float(pA), "ci_low": ciA[0], "ci_high": ciA[1],
                            "structural_range": [float(min(va[W_HEAD])), float(max(va[W_HEAD]))],
                            "definition": ("P(Alt A | S2, not Alt B): parallel economy reaches >=10% of population "
                                           "by 2055 and is still >=5% ten years later without being suppressed below "
                                           "5%, given m7's no-customers condition (uncompensated excluded share >=25% "
                                           "for 2 years by 2060) and no Alt B. Medium-term survival only; the public's "
                                           "fate under S5 is not modelled here.")},
            "by_window_years": {str(w): {"mean": Aw_c[w], "structural_range": [float(min(va[w])), float(max(va[w]))]}
                                for w in WINDOWS},
            "n_conditioning_draws": int(condA.sum()),
            "P(forms | S2, not B)": formed_c,
            "P(ever suppressed | forms)": float(out["ever_supp"][fA].mean()),
            "P(survives 10y | forms)": float(out["A"][fA].mean()),
            "timeline_formation_of_successful": yrs_A,
            "splits": ubi_split,
        },
        "joint_A_B": joint,
        "outcome_partition": part,
        "calibration_P(first suppression within 10y | formed by 2050)": supp10,
        "structural_variants_20k": struct,
        "convergence_running_mean_B": conv,
        "decentralized_share_snapshots": Dq,
        "scenario_splits": splits,
        "sensitivity_tercile_delta_B_top12": topB,
        "sensitivity_tercile_delta_A10_top12": topA,
        "in_model_timelines": {"t_auto_A50": yrs_auto, "t_S2_m7": yrs_S2,
                               "P(S2_m7 by 2060)": float(out["S2"].mean()),
                               "note": "m7's S2 is a simplified conditioning device; use m2 for P(S2)."},
        "interactions": {
            "B_effect_on_S3": ("Uncoopted B competes away provider markups (averts S3) and weakens S4 rentier "
                               "logic by lowering AI-firm tax dominance. It does NOT cap S2: cheap AI accelerates "
                               "automation, and network rewards replace only a small share of lost wages (see "
                               "network_income_replacement). Integrator: in B draws treat S3 as averted with "
                               "prob 1 - p_coopt (~0.65), S2 unchanged."),
            "P(B | concentration)": splits["P(B | provider concentration)"],
            "P(parallel economy formed | S2, not B)": formed_c,
            "S2_note": ("Do not pass m7's P(S2_m7) to the integrator; m2 is canonical (m2 P(S2)=0.154 on a stricter "
                        "consumption-based definition)."),
            "P(crackdown on permissionless AI by 2075)": float(out["crack"].mean()),
        },
        "samples": {
            "note": "5000 random draws; B and A are per-draw binary outcomes; years null if not reached.",
            "B": out["B"][samp].astype(int).tolist(),
            "year_B": [None if not np.isfinite(v) else float(v) for v in out["t_B"][samp]],
            "S2": out["S2"][samp].astype(int).tolist(),
            "A10": out["A"][samp].astype(int).tolist(),
            "year_A_formation": [None if not (a and np.isfinite(v)) else float(v)
                                 for a, v in zip(out["A"][samp], out["t_form"][samp])],
            "year_auto": [None if not np.isfinite(v) else float(v) for v in out["t_auto"][samp]],
        },
        "priors": {k: {"dist": d, "args": list(a), "source": s} for k, (d, a, s) in PRIORS.items()},
    }
    os.makedirs(RES, exist_ok=True)
    with open(os.path.join(RES, "m7_decentralized_alternative.json"), "w") as f:
        json.dump(res, f, indent=1)

    make_figs(out, cm, topB, topA, curve, struct, Bvars, Avars)

    print(f"N={N} seed={SEED}")
    print(f"P(B|S1) = {pB:.4f}  MC CI [{ciB[0]:.4f}, {ciB[1]:.4f}]  structural {min(vb):.4f}-{max(vb):.4f}")
    print("  B years:", yrs_B, " B uncoopted:", out["B_struct"].mean(), " W:", out["W"].mean())
    print(f"P(A10|S2,notB) = {pA:.4f}  MC CI [{ciA[0]:.4f}, {ciA[1]:.4f}]  n={condA.sum()}")
    for w in WINDOWS:
        print(f"  window {w}: {Aw_c[w]:.3f}  structural {min(va[w]):.3f}-{max(va[w]):.3f}")
    print(f"  P(forms|S2,notB)={formed_c:.3f}  supp10={supp10:.3f}  P(S2_m7)={out['S2'].mean():.3f}")
    print("Joint:", joint)
    print("Init:", init)
    print("Snapshots:", json.dumps(Dq, indent=0))
    print("Curve:", curve); print("Curve pf:", curve_pf)
    print("Splits:", splits); print("A splits:", ubi_split)
    print("Partition:", json.dumps(part, indent=0))
    print("Top B:", [(k, round(v, 4)) for k, v in topB])
    print("Top A:", [(k, round(v, 3)) for k, v in topA])
    print("Timelines auto/S2/W:", yrs_auto, yrs_S2, yrs_W)


def make_figs(out, cm, topB, topA, curve, struct, Bvars, Avars):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    os.makedirs(FIG, exist_ok=True)
    fig, ax = plt.subplots(1, 3, figsize=(17, 4.8))
    bins = np.arange(2026, 2061, 1)
    for t, lab, c in ((out["t_auto"], "Automation reaches 50%", "#888888"),
                      (out["t_S2"], "m7 no-customers condition (S2_m7)", "#d95f02"),
                      (np.where(out["A"], out["t_form"], np.inf), "Parallel economy forms, tolerated 10y (Alt A)", "#1b9e77"),
                      (out["t_W"], "S3-averting share W >= 25%", "#e7298a"),
                      (out["t_B"], "Permissionless AI wins (Alt B)", "#7570b3")):
        v = t[np.isfinite(t)]
        ax[0].hist(v, bins=bins, weights=np.full(len(v), 1 / N), histtype="step", lw=2, label=lab, color=c)
    ax[0].set_xlabel("Calendar year"); ax[0].set_ylabel("Share of all draws per year")
    ax[0].set_title("Timing of events (unconditional)"); ax[0].legend(fontsize=7, frameon=False)
    pa = out["paths"]; t = pa["t"]
    for key, col, lab in (("D", "#7570b3", "permissionless D"), ("W", "#e7298a", "S3-averting W")):
        arr = np.array(pa[key])
        for q, a in ((50, 1.0), (90, 0.55), (99, 0.25)):
            ax[1].plot(t, np.percentile(arr, q, axis=1), color=col, alpha=a, label=f"{lab} p{q}")
    ax[1].axhline(D_WIN, ls="--", color="k", lw=1)
    ax[1].set_yscale("log"); ax[1].set_ylim(1e-4, 1)
    ax[1].set_title("Workload shares (400 paths)"); ax[1].set_xlabel("Calendar year")
    ax[1].legend(fontsize=6, frameon=False, ncol=2)
    xs = [c["anchor_share"] for c in curve]
    ax[2].plot(xs, [c["P(B)"] for c in curve], "o-", color="#7570b3", label="P(Alt B)")
    ax[2].plot(xs, [c["P(W)"] for c in curve], "s--", color="#e7298a", label="P(W>=25% before automation)")
    ax[2].axvspan(0.11, 0.25, color="#cccccc", alpha=0.4, label="anchor prior range")
    ax[2].set_xlabel("Anchor: open-weight workload share at 2025 price gap (revealed friction)")
    ax[2].set_ylabel("Probability"); ax[2].set_title("Alt B vs friction anchor"); ax[2].legend(fontsize=7, frameon=False)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "m7_decentralized_alternative_timeline.png"), dpi=130)
    plt.close(fig)

    fig, ax = plt.subplots(1, 4, figsize=(22, 5.5))
    ax[0].plot(np.arange(1, N + 1), cm, color="#7570b3")
    ax[0].set_xscale("log"); ax[0].set_title("Convergence of P(Alt B | S1)"); ax[0].set_xlabel("Draws")
    for a_, top, title in ((ax[1], topB, "Alt B: P(top tercile) - P(bottom tercile)"),
                           (ax[2], topA, "Alt A10 | S2, not B: tercile delta")):
        names = [k for k, _ in top][::-1]; vals = [v for _, v in top][::-1]
        a_.barh(names, vals, color=["#1b9e77" if v > 0 else "#d95f02" for v in vals])
        a_.axvline(0, color="k", lw=0.8); a_.set_title(title, fontsize=9); a_.tick_params(labelsize=7)
    labs = list(struct.keys())
    yv = np.arange(len(labs))
    ax[3].scatter([struct[l]["P(B)"] for l in labs], yv, color="#7570b3", label="P(B)")
    ax[3].scatter([struct[l]["P(A10|S2,notB)"] for l in labs], yv, color="#1b9e77", marker="s", label="P(A10|S2,notB)")
    ax[3].set_yticks(yv); ax[3].set_yticklabels(labs, fontsize=6); ax[3].invert_yaxis()
    ax[3].set_xlim(0, 1); ax[3].set_title("Structural variants (20k draws each)", fontsize=9)
    ax[3].legend(fontsize=7, frameon=False)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "m7_decentralized_alternative_sensitivity.png"), dpi=130)
    plt.close(fig)


if __name__ == "__main__":
    main()
