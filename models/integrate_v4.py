"""
Integrated scenario-tree / competing-hazards Monte Carlo, v4.

v4 = integrate_v3.py rebuilt around m8_v4 (6 blocs, endogenous grievance loop and democracy, review round 3
wiring of F1-F8 and the binding assumptions A1-A11, incl. the A8/A9/A11 endgame).

Changes from v3
1. m8_v4 replaces m8_industrial_closure (v3). Six blocs (US_bloc, China_bloc, Europe_plus, Russia_MENA,
   South_Asia, Global_South) instead of US / China / one RoW actor. Headlines are reported for US-or-China,
   for any bloc, and as the expected share of world population living in blocs where the event happens.
2. Channel labeling fixed. v3 line 392 mapped every m8 channel that was not "active" to "neglect", which in v4
   would have relabeled attrition (despair, crackdown) and war deaths as neglect. v4 keeps m8's codes:
   deliberate = executed depopulation decision, collective punishment, deliberate lethal neglect, collusive war
   between depopulating coalitions (A9); total = deliberate + attrition + ordinary war. v3 line 390 read m8's
   total t_S5 where the deliberate headline needs t_S5d; v4 reads the deliberate and total clocks separately.
3. Loss ladder (A8): >=10%, >=50%, >=90%, >=99.9% of a bloc's 2026 population, deliberate vs total. The 99.9%
   rung is the scenario's near-total depopulation (8 billion to ~8 million). Survivors of a completed programme
   are a CAPTIVE remnant without rights (A11) and are counted as disempowered, not as survivors with standing.
   In m8_v4 an executed designation is simulated as deaths (hazard ramp over T_full, abstract means availability
   driven by capability, escalation from partial to near-total driven by the rulers' perceived revenge threat,
   collusion between depopulating coalitions decided by a payoff comparison incl. rulers' own survival). v3/m8
   round 2 booked S5 at decision time + lagX with no simulated deaths; that is gone.
4. The broad path (S1 -> S2 -> S4 -> S5, v2 m4/m5 analogs) exists only for the US and China blocs (m4 has no
   other blocs). As in v3 the analogs hold only while the bloc's core chain still needs humans (D_core >= 0.2).
   A US S4 regime alive at closure takes the m8 outcome of a US-autocratic counterfactual on the same replicate
   (or the baseline outcome if the baseline US was already autocratic at its decision). v3 then ALSO kept the
   baseline US closure path, double counting two different US histories; v4 uses one or the other.
5. v3 leftovers removed: single RoW actor, "warehousing is mortality-free" (m8_v4 has despair mortality), the
   5-option strategy codes (m8_v4 has 6: serve, warehouse, neglect, depopulate, rentier, status_quo).

Round 3 (B1-B9 agreed with the scenario): m8_v4 now carries B1-B6 (see its docstring). Here:
 B5 cross-bloc depopulation by a foreign closed actor is a deliberate channel (code 8) and feeds the world loss.
 B8 fix: after a US broad-analog S5 (or S5b) under a US S4 regime before US closure, the later closure path uses the
   US-autocratic counterfactual history (round 2 fell back to the baseline US history, which may still be democratic).
 B9: Alt B (decentralized AI) is kept exactly as in round 2: baseline historical adoption, no mobilization, black box.
The frozen round-2 integrator is integrate_v4_round2.py (imports m8_v4_round2.py).
Round 3 outputs pass (this file; the pre-pass round-3 integrator is frozen as integrate_v4_round3a.py):
 cf_world: when a US broad S4 regime reaches closure and the US-autocratic counterfactual replaces the US history, all six
   blocs are now taken from that same counterfactual simulation, so its cross-bloc campaigns reach the other blocs (round
   3a mixed one US history with five blocs from the other). Variant 'cf_world off' reproduces round 3a.
 New outputs: mutually exclusive outcome breakdown (US or China, each bloc, population-weighted world), B5 who
   depopulates whom (aggressor x target), world-level near-total composition, and B2 consolidation to a single decider.

Horizon 2026.75 - end of 2075. NO epistemic draws x R8 m8 aleatory replicates x NI inner paths >= 200,000.
The m8 part runs on the GPU (torch); the scenario tree is vectorised numpy (runtime a few minutes).
Run: python models/integrate_v4.py
"""
import json
import os
import sys
import time

import numpy as np
from scipy.special import expit, logit
from scipy.stats import norm, rankdata, spearmanr

ROOT = r"C:\code\sims\dystopia"
RES = os.path.join(ROOT, "results")
FIG = os.path.join(ROOT, "figures")
sys.path.insert(0, os.path.join(ROOT, "models"))
import m8_v4 as M8  # noqa: E402

# m8_v4 standalone stops at 2075.0; the integrator counts events to the end of 2075 (HZ = 2076.0)
M8.T_END = 2076.0
M8.NSTEP = int(round((M8.T_END - M8.T0) / M8.DT))
M8.YEARS = np.arange(2027, 2077)

SEED = 20260930
HZ1 = 2076.0
T0 = 2026.75
A_N = M8.A_N
ACT = M8.ACTORS
POP = M8.POP
LTH = M8.LOSS_THR
NL = len(LTH)
INF = np.inf


def load(name):
    with open(os.path.join(RES, name)) as f:
        return json.load(f)


def arr(x):
    return np.array([np.nan if v is None else v for v in x], float)


M1 = load("m1_automation_race.json")
M4 = load("m4_state_repression.json")
M5 = load("m5_depopulation_singleton.json")
M6 = load("m6_multipolar_race_ai_dissent.json")
M7 = load("m7_decentralized_alternative.json")

# ---- m4 samples (as v2/v3) -----------------------------------------------------------------
M4_N = 16
m4_kUS = np.round(arr(M4["samples"]["p_US"]) * M4_N); m4_kCN = np.round(arr(M4["samples"]["p_China"]) * M4_N)
m4_off = arr(M4["samples"]["year"]) - arr(M4["samples"]["S2_midpoint_year"])
m4_off = np.where(np.isnan(m4_off), np.nanmedian(m4_off), m4_off)


def eb_beta(k, n):
    p = k / n; m = p.mean(); v = p.var()
    vp = max((v - m * (1 - m) / n) / (1 - 1 / n), 1e-6)
    s = max(m * (1 - m) / vp - 1, 0.5)
    return m * s, (1 - m) * s


A_US, B_US = eb_beta(m4_kUS, M4_N); A_CN, B_CN = eb_beta(m4_kCN, M4_N)

# ---- m5 / m6 / m7 (as v2/v3) ------------------------------------------------------------------
m5_p5 = arr(M5["samples"]["p_s5_given_s4"]); m5_lag5 = arr(M5["samples"]["s5_lag_after_s4"])
m5_lag5 = np.where(np.isnan(m5_lag5), np.nanmedian(m5_lag5), m5_lag5)
m5_p6 = arr(M5["samples"]["p_s6_given_s5"])
P6_HEAD = M5["s6_given_s5"]["mean"]
m5_p6 = np.clip(m5_p6 * P6_HEAD / m5_p6.mean(), 0, 1)
m5_lag6 = arr(M5["samples"]["s6_lag_after_s5"]); m5_lag6 = m5_lag6[~np.isnan(m5_lag6)]
S5B_ONLY_RATIO = (M5["s5_or_s5b_20y"] - M5["stage_probability"]["mean"]) / M5["stage_probability"]["mean"]
m6_p7 = arr(M6["samples"]["stage_probability"]); m6_pmis = arr(M6["samples"]["p_misaligned"])
m6_yrs = arr(M6["samples"]["moral_rebellion_years_after_s6"]); m6_agi = arr(M6["samples"]["agi_year"])
m6_yrs_f = np.where(np.isnan(m6_yrs), np.nanmedian(m6_yrs), m6_yrs)
m6_agi_f = m6_agi[~np.isnan(m6_agi)]
PW_WAR = M6["outcome_distribution_given_s6"]["war_collapse"]["mean"]
m7_yB = arr(M7["samples"]["year_B"]); m7_yB = m7_yB[~np.isnan(m7_yB)]

# ---- m1 CDF (only for the v2-S1 variant) ------------------------------------------------------
_c = M1["cdf_event_by_year_pooled"]
P1_POOLED = _c["2075"]; P1_PRIOR = M1["cdf_event_by_year_prior_only"]["2075"]
P1_ANCH = np.mean([0.432, 0.395, 0.345]) * P1_POOLED / _c["2060"]
S1_KNOTS_T = np.array([2027.0, 2031.0, 2036.0, 2041.0, 2046.0, 2051.0, 2061.0, 2076.0])
S1_KNOTS_F = np.array([0, _c["2030"], _c["2035"], _c["2040"], _c["2045"], _c["2050"], _c["2060"], _c["2075"]]) / P1_POOLED
S1_KNOTS_F[-1] = 1.0
S3_Q = np.array([0, 0.1, 0.5, 0.9, 1.0]); S3_T = np.array([2028.0, 2032.0, 2039.0, 2044.0, 2050.0])

EX = M5["exits_before_20y"]
W_EXIT = dict(reform=EX["reform_redistribution"]["mean"], ext=EX["external_intervention"]["mean"],
              coup=EX["coup_collapse"]["mean"],
              ware=M5["s5_breakdown"]["ware"]["mean"] + EX["ai_takeover_independent"]["mean"])
ACT_SHARE = M5["s5_breakdown"]["act"]["mean"] / (M5["s5_breakdown"]["act"]["mean"] + M5["s5_breakdown"]["neg"]["mean"])

# deliberate/total channel codes used in the integrator
CH = {0: "active_depopulation_decision", 1: "collective_punishment", 2: "deliberate_lethal_neglect",
      3: "collusive_war_between_depopulating_coalitions", 4: "broad_path_killing_human_staffed_regime",
      5: "broad_path_famine_human_staffed_regime", 6: "attrition_despair_and_crackdown", 7: "war",
      8: "cross_bloc_depopulation_by_foreign_closed_actor"}
DELIB_CH = [0, 1, 2, 3, 4, 5, 8]

# ============================================================================================
# m8_v4 in-process: epistemic draws x aleatory replicates, plus US-autocratic counterfactual
# ============================================================================================
M8_ALEATORY = {"corr_start", "corr_len", "capex_corr", "t_leth", "u_grab", "mem_z", "mem_u_host", "mem_zm",
               "mem_u_ref", "mem_zt", "u_dem", "wf_mult", "u_small", "ep0", "u_reg", "u_lead", "mem_zc", "sim_seed",
               "mem_zh", "mem_u_sx"}
SENS_SKIP = {"sim_seed", "p_cog_wall", "p_phys_wall", "p_capex_correction", "g0_mult_sd", "t_leth_rate", "fb_zero_mass",
             "nmin", "p_W_dem", "trig", "surv_on", "cp_scale", "Np", "sw_auto0", "ac_horizon_hours", "F_ac", "tau_phys",
             "g_h", "tau_cog", "Td_mine_h", "Td_fab_h", "s_task"}


def score(x):
    """rank-based normal score"""
    return norm.ppf((rankdata(x) - 0.5) / len(x))


def chan_m8(tS5d, chS5d, tX):
    """m8 deliberate channel -> integrator code"""
    with np.errstate(invalid="ignore"):
        dec = np.isfinite(tX) & (tX <= tS5d + 1e-9)
    return np.select([(chS5d == 3) & dec, chS5d == 3, chS5d == 2, chS5d == 6, chS5d == 7], [0, 1, 2, 3, 8], -1)


def chan_tot(chS5):
    return np.select([chS5 == 4, chS5 == 5], [6, 7], -1)


def run_m8(NO, R, variant="baseline", seed=SEED + 800):
    rng = np.random.default_rng(seed)
    pe = M8.sample_params(NO, rng, None, variant)
    pa = M8.sample_params(NO * R, rng, None, variant)
    for k in pe:
        if k not in M8_ALEATORY and isinstance(pe[k], np.ndarray) and pe[k].shape[:1] == (NO,):
            pa[k] = np.repeat(pe[k], R, axis=0)
    o = M8.simulate(pa, NO * R, variant, records=False)
    pc = dict(pa); ug = pa["u_grab"].copy(); ug[:, 0] = -1.0; pc["u_grab"] = ug   # US bloc seized from t0
    oc = M8.simulate(pc, NO * R, variant, records=False)
    def world(x):
        """per-bloc arrays that describe one simulated world (switched as a whole in the integrator, see cf_world)"""
        return dict(tc=x["t_core"][:, :, 1],
                    tLd=x["tL_del"], tLt=x["tL_tot"], chd=chan_m8(x["t_S5d"], x["ch_S5d"], x["t_X"]), cht=chan_tot(x["ch_S5"]),
                    tX=x["t_X"], tcap=x["t_captive"], loss=x["loss"], tbreak=x["t_break"], tharsh=x["t_first_harsh"],
                    fc=x["first_choice"], fad=x["free_at_dec"], tdec=x["t_first_dec"], ce=x["choice_end"], fe=x["free_end"],
                    tmeans=x["t_means"], tcol=x["t_col"], tnx=x["t_nx"],
                    # round 3: B5 cross-bloc (who depopulates whom) and B2 consolidation
                    txb=x["t_xb"], xb_by=x["xb_by"], lc_xb=x["lc_xb"], inflicted=x["inflicted"], txb_nuc=x["t_xb_nuc"],
                    n_xb_rep=x["n_xb_rep"], lc_dom=x["lc_neg"] + x["lc_act"] + x["lc_col"],
                    tsing=x["t_single"], tsl95=x["t_sl95"], ncd=x["n_coal_dec"], nce=x["n_coal_end"], sle=x["SL_end"], pers=x["pers_end"])
    WK = list(world(o).keys())
    D = dict(NO=NO, R=R, variant=variant, WK=WK,
             tf05=o["t_full"][:, :, 0], tf02=o["t_full"][:, :, 1],
             tS5d=o["t_S5d"], tS5=o["t_S5"],
             tgrab=o["t_grab"][:, 0],
             tac=o["t_ac"], tdex=o["t_dex"], tesc=o["t_esc"],
             cf_tS5d=oc["t_S5d"][:, 0], cf_tS5=oc["t_S5"][:, 0],
             cf_chd=chan_m8(oc["t_S5d"][:, 0], oc["ch_S5d"][:, 0], oc["t_X"][:, 0]), cf_cht=chan_tot(oc["ch_S5"][:, 0]),
             cf_tLd=oc["tL_del"][:, 0], cf_tLt=oc["tL_tot"][:, 0], cf_tcap=oc["t_captive"][:, 0], cf_loss=oc["loss"][:, 0],
             cf_fc=oc["first_choice"][:, 0], cf_tdec=oc["t_first_dec"][:, 0], cf_ce=oc["choice_end"][:, 0])
    D.update(world(o))
    D.update({"cfw_" + k: v for k, v in world(oc).items()})   # the whole US-autocratic counterfactual world
    tac =np.where(np.isfinite(o["t_ac"]), o["t_ac"], 2100.0).reshape(NO, R).mean(1)
    tdx = np.where(np.isfinite(o["t_dex"]), o["t_dex"], 2100.0).reshape(NO, R).mean(1)
    D["z_cap"] = score(-(0.6 * score(tac) + 0.4 * score(tdx)))
    pe_s = {}
    for k, v in pe.items():
        if k in SENS_SKIP or not isinstance(v, np.ndarray) or v.shape != (NO,):
            continue
        if k in BRK_KEYS and not any(pe[f].any() for f in BRK_KEYS[k]):    # brakes off: keep the baseline table as before
            continue
        v = v.astype(float)
        if np.std(v) > 0:
            pe_s[k] = v
    pe_s["fb_strength_eff"] = np.where(pe["fb_zero"], 0.0, pe["fb_strength"])
    pe_s["collusion_incentive (b_col - (1-s_bunk) p_nx c_self)"] = np.log(pe["b_col"]) - np.log((1 - pe["s_bunk"]) * pe["p_nx"] * pe["c_self"])
    D["pe"] = pe_s
    D["brk_diag"] = brake_diag(o)
    return D


# brake parameters enter the sensitivity table only when their brake is on (flags in m8_v4.BRK_FLAGS)
BRK_KEYS = {"p_pid": ["pid_on"], "k_pid": ["pid_on"], "c_selfrisk": ["sr_on"], "e_ex": ["sr_on"],
            "h_mort": ["brk_mort"], "g_mort": ["brk_mort"], "k_le": ["brk_mort"], "p_heir": ["brk_mort"],
            "b_id": ["sr_on"], "m_dis": ["dis_on"]}


def brake_diag(o):
    """diagnostics showing each brake is active (m8 main world, all draws x replicates)"""
    r = lambda x: round(float(x), 5)
    d = {}
    UC = [0, 1]
    dec = np.isfinite(o["t_first_dec"])
    for tag, cols in [("US_or_China_blocs", UC), ("all_blocs", list(range(A_N)))]:
        dm = dec[:, cols]
        X = np.isfinite(o["t_X"][:, cols])
        yc = o["yrs_closed"][:, cols].sum()
        d[tag] = dict(
            P_protective_doctrine_held_at_first_decision=r(o["pid_at_dec"][:, cols][dm].mean()) if dm.any() else None,
            mean_pid_level_at_first_decision=r(np.nanmean(o["pidlev_at_dec"][:, cols][dm])) if dm.any() else None,
            P_doctrine_held_at_execution=r(o["pid_at_X"][:, cols][X].mean()) if X.any() else None,
            share_closed_autocracy_years_with_doctrine=r(o["pid_yrs_closed"][:, cols].sum() / yc) if yc > 0 else None,
            P_doctrine_ever_adopted_per_bloc=r(np.isfinite(o["t_pid"][:, cols]).mean()),
            selfrisk_decision_years_with_exposed_members_per_bloc_path=r(o["n_sr_dec"][:, cols].mean()),
            selfrisk_decision_years_with_a_member_vote_flipped_harsh_to_mild_per_bloc_path=r(o["n_sr_memflip"][:, cols].mean()),
            selfrisk_share_of_exposed_decisions_where_coalition_choice_changed=r(o["n_sr_flip"][:, cols].sum() / max(o["n_sr_dec"][:, cols].sum(), 1)),
            selfrisk_coalition_choice_flipped_per_bloc_path=r(o["n_sr_flip"][:, cols].mean()),
            selfrisk_harsh_to_mild_flips_per_bloc_path=r(o["n_sr_flip_harsh"][:, cols].mean()),
            selfrisk_depopulate_blocked_per_bloc_path=r(o["n_sr_flipX"][:, cols].mean()),
            selfrisk_extra_vetoes_per_bloc_path=r(o["n_sr_veto"][:, cols].mean()),
            P_selfrisk_blocked_depopulation_at_least_once_per_bloc=r((o["n_sr_flipX"][:, cols] > 0).mean()),
            mean_leader_deaths_per_bloc_path=r(o["n_death"][:, cols].mean()),
            mean_leader_deaths_per_path_summed_over_blocs=r(o["n_death"][:, cols].sum(1).mean()),
            heir_successions_per_bloc_path=r(o["n_heir"][:, cols].mean()),
            split_successions_per_bloc_path=r(o["n_split"][:, cols].mean()),
            leader_deaths_during_execution_per_bloc_path=r(o["n_death_exec"][:, cols].mean()),
            executions_halted_by_split_per_bloc_path=r(o["n_halt_mort"][:, cols].mean()),
            P_execution_halted_by_split_at_least_once_per_bloc=r((o["n_halt_mort"][:, cols] > 0).mean()),
            P_execution_started_per_bloc=r(X.mean()),
            dissent_decision_years_with_dissent_risk_per_bloc_path=r(o["n_dis_dec"][:, cols].mean()),
            dissent_failed_veto_punishments_per_bloc_path=r(o["n_dpun"][:, cols].mean()),
            P_failed_veto_punishment_at_least_once_per_bloc=r((o["n_dpun"][:, cols] > 0).mean()),
            dissent_share_exposed_member_decisions_net_selfrisk_negative=r(o["n_dis_netneg"][:, cols].sum() / max(o["n_dis_expo"][:, cols].sum(), 1)),
            dissent_mean_c_x_dPno_minus_dPyes_over_exposed_member_decisions=r(o["sum_dis_net"][:, cols].sum() / max(o["n_dis_expo"][:, cols].sum(), 1)),
            dissent_decision_years_with_a_member_pushed_back_to_harsh_per_bloc_path=r(o["n_dis_memback"][:, cols].mean()),
            dissent_coalition_choice_changed_vs_selfrisk_only_per_bloc_path=r(o["n_dis_flip"][:, cols].mean()),
            dissent_restored_harsh_choice_per_bloc_path=r(o["n_dis_restore_harsh"][:, cols].mean()),
            dissent_restored_depopulation_per_bloc_path=r(o["n_dis_restoreX"][:, cols].mean()),
        )
    return d


BASE_CFG = dict(
    HZ_D=2076.0,
    s1_mode="m8", s1_D="0.5", s1_lag_med=2.0, s1_lag_sig=0.6, p1_depth=0.849, s1_noise3=0.5, b1_inst=0.3,
    dfb_lo=1.0, dfb_hi=1.0, share_latent=True,
    s1_views=[(P1_PRIOR, 0.25), (P1_POOLED, 0.50), (P1_ANCH, 0.25)], a1_cap=0.9, s1_noise=0.45, shift_cap=1.5,
    p2_centers=[(0.5, 0.5), (0.8, 0.5)], a2_cap=0.5, s2_noise=0.6, lag2_med=3.0,
    pess_w=0.15, s2b_pess=0.25, s2b_base=0.002, s2b_or_noredist=2.0, s2b_or_redist=0.5,
    p3_mean=0.04, a3_open=1.1, a3_cap=0.3, a3_inst=0.2, s3_noise=1.0,
    pB_mean=0.081, aB_cap=0.6, aB_open=0.5, sB_noise=0.9, B_S2_factor=0.75, B_US_mech=0.5 * 0.173,
    coopt_lo=0.2, coopt_hi=0.5,
    rho_m4_inst=0.5, s4_cap_US=0.1, s4_cap_CN=0.1, us_s4_shift=0.0,
    strict_US=0.293 / 0.415, strict_CN=0.192 / 0.855,
    kact_lo=0.05, kact_hi=0.4, kneg_lo=0.3, kneg_hi=1.0, kbroad_fixed=None,
    rho_m5_inst=0.3, s5_cap=0.15, s2b_s5_or=1.5, reform_inst=0.3, count_S5b=True,
    A_form=0.224, A_form_sd=0.6, A_surv=0.038 / 0.224, A_surv_sd=1.2, A_s2b_logit=0.5, A_strict_logit=-0.5,
    p7_scale=1.0,
    Pai_med=0.025, Pai_sig=0.8, Pai_cap_load=0.4, Pai_cap=0.4, Pai_window=40.0, ai_s4_mult_lo=1.0, ai_s4_mult_hi=2.0,
    Pcat_med=0.04, Pcat_sig=0.5, agi_lag=1.0,
    m8_on=True, broad_on=True, d_replace=True,
    fert_a=1.2, fert_b=22.8, fert_lag_lo=15.0, fert_lag_hi=25.0,
    b8_fix=True, cf_world=True,
)


def pick_by_copula(rng, values, z, rho):
    order = np.argsort(values)
    u = norm.cdf(rho * z + np.sqrt(1 - rho ** 2) * rng.standard_normal(z.shape))
    idx = np.minimum((u * len(values)).astype(int), len(values) - 1)
    return order[idx]


def calib_intercept(target, slopes_sd, n=200000, seed=1):
    r = np.random.default_rng(seed).standard_normal(n) * slopes_sd
    lo, hi = -12, 6
    for _ in range(60):
        m = 0.5 * (lo + hi)
        if expit(m + r).mean() < target:
            lo = m
        else:
            hi = m
    return 0.5 * (lo + hi)


def mixture_pick(rng, opts, n):
    vals = np.array([v for v, _ in opts]); w = np.array([w for _, w in opts], float); w /= w.sum()
    return vals[rng.choice(len(vals), n, p=w)]


def first_of(cands):
    """cands: list of (T, ch, path). returns T, ch, path of the earliest"""
    Tst = np.stack([c[0] for c in cands]); Cst = np.stack([np.broadcast_to(c[1], Tst.shape[1:]) for c in cands])
    Pst = np.stack([np.full(Tst.shape[1:], c[2]) for c in cands])
    i = Tst.argmin(0); n = np.arange(Tst.shape[1])
    T = Tst[i, n]
    return T, np.where(np.isfinite(T), Cst[i, n], -1), np.where(np.isfinite(T), Pst[i, n], -1)


def simulate(cfg, D8, NI, seed):
    rng = np.random.default_rng(seed)
    NO, R8 = D8["NO"], D8["R"]
    N = NO * NI
    HZ = cfg["HZ_D"]
    o = np.repeat(np.arange(NO), NI)
    P = {}
    j = o * R8 + rng.integers(0, R8, N)                       # m8 replicate used by this trajectory
    if cfg["share_latent"]:
        ob = np.arange(NO); jb = j
    else:
        perm = rng.permutation(NO); ob = perm; jb = perm[o] * R8 + rng.integers(0, R8, N)
    z_cap_b = D8["z_cap"][ob]
    z_inst = rng.standard_normal(NO); z_open = rng.standard_normal(NO)
    P["z_cap (shared AI capability speed, from m8)"] = D8["z_cap"]
    P["z_inst (institutional strength)"] = z_inst
    P["z_open (open-weight continuity)"] = z_open
    for k, v in D8["pe"].items():
        P["m8: " + k] = v

    # ---------------- S1 ----------------
    e1 = rng.standard_normal(NO)
    dfb = rng.uniform(cfg["dfb_lo"], cfg["dfb_hi"], NO)
    if cfg["s1_mode"] == "m8":
        tf = D8["tf05"] if cfg["s1_D"] == "0.5" else D8["tf02"]
        Td = np.minimum(tf[jb, 0], tf[jb, 1])
        T1 = Td + np.exp(np.log(cfg["s1_lag_med"]) + cfg["s1_lag_sig"] * rng.standard_normal(N))
        p1 = dfb * expit(logit(cfg["p1_depth"]) + cfg["s1_noise3"] * e1 - cfg["b1_inst"] * z_inst)
        P["P(S1|depth) draw (m1 pacts/frictions/regulation)"] = p1
    else:
        view = mixture_pick(rng, cfg["s1_views"], NO)
        zz = np.random.default_rng(7).standard_normal((3, 100000)); uu = np.random.default_rng(8).random(100000)
        t_test = np.maximum(np.interp(uu, S1_KNOTS_F, S1_KNOTS_T) - cfg["shift_cap"] * zz[0], 2028.0)
        x_test = cfg["a1_cap"] * zz[0] + cfg["s1_noise"] * zz[1] - cfg["b1_inst"] * zz[2]
        c1_of = {}
        for tgt in np.unique(view):
            lo, hi = -10, 8
            for _ in range(50):
                c = 0.5 * (lo + hi)
                if (expit(c + x_test) * (t_test < HZ1)).mean() < tgt:
                    lo = c
                else:
                    hi = c
            c1_of[tgt] = 0.5 * (lo + hi)
        c1 = np.array([c1_of[v] for v in view])
        p1 = dfb * expit(c1 + cfg["a1_cap"] * z_cap_b + cfg["s1_noise"] * e1 - cfg["b1_inst"] * z_inst)
        T1 = np.maximum(np.interp(rng.random(N), S1_KNOTS_F, S1_KNOTS_T) - cfg["shift_cap"] * z_cap_b[o], 2028.0)
    S1 = (rng.random(N) < p1[o]) & (T1 < HZ1)
    T1 = np.where(S1, T1, INF)

    # ---------------- AGI year: m8 M3 capability + lag ----------------
    tac = D8["tac"][j]
    agi = np.where(np.isfinite(tac), tac + cfg["agi_lag"], rng.choice(m6_agi_f[m6_agi_f > 2045], N))

    # ---------------- Alt B ----------------
    eB = rng.standard_normal(NO)
    cB = calib_intercept(cfg["pB_mean"], np.sqrt(cfg["aB_cap"] ** 2 + cfg["aB_open"] ** 2 + cfg["sB_noise"] ** 2))
    pB = expit(cB - cfg["aB_cap"] * z_cap_b + cfg["aB_open"] * z_open + cfg["sB_noise"] * eB)
    coopt = rng.uniform(cfg["coopt_lo"], cfg["coopt_hi"], NO)
    TB = rng.choice(m7_yB, N) + rng.uniform(-0.5, 0.5, N)
    Bocc = (rng.random(N) < pB[o]) & (TB < HZ)
    Beff = Bocc & (rng.random(N) >= coopt[o])
    TB = np.where(Bocc, TB, INF); TBe = np.where(Beff, TB, INF)

    # ---------------- S2a timing candidate ----------------
    lag_mu = np.log(cfg["lag2_med"]) + 0.3 * rng.standard_normal(NO) - 0.15 * z_cap_b
    T2c = T1 + np.exp(lag_mu[o] + 0.6 * rng.standard_normal(N))

    # ---------------- S3 ----------------
    e3 = rng.standard_normal(NO)
    c3 = calib_intercept(cfg["p3_mean"], np.sqrt(cfg["a3_open"] ** 2 + cfg["a3_cap"] ** 2 + cfg["a3_inst"] ** 2 + cfg["s3_noise"] ** 2))
    p3 = expit(c3 - cfg["a3_open"] * z_open + cfg["a3_cap"] * z_cap_b - cfg["a3_inst"] * z_inst + cfg["s3_noise"] * e3)
    T3 = np.maximum(np.interp(rng.random(N), S3_Q, S3_T), T1) + rng.uniform(0, 2, N)
    S3 = S1 & (rng.random(N) < p3[o]) & ~(TBe < T3) & (T3 < HZ)
    T3 = np.where(S3, T3, INF)

    # ---------------- S2a ----------------
    e2 = rng.standard_normal(NO)
    p2c = mixture_pick(rng, cfg["p2_centers"], NO)
    P["P(S2|S1) centre (0.5 m2 / 0.8 m1)"] = p2c
    p2 = expit(logit(p2c) + cfg["a2_cap"] * z_cap_b + cfg["s2_noise"] * e2)
    f2 = np.ones(N)
    f2 = np.where(TBe < T2c, f2 * cfg["B_S2_factor"], f2)
    f2 = np.where(T3 < T2c, f2 * 0.8, f2)
    S2 = S1 & (rng.random(N) < p2[o] * f2) & (T2c < HZ)
    T2 = np.where(S2, T2c, INF)

    # ---------------- S4 per jurisdiction (US, China: m4) ----------------
    k4 = pick_by_copula(rng, m4_kUS + 0.01 * rng.random(len(m4_kUS)), -z_inst, cfg["rho_m4_inst"])
    pUS = rng.beta(A_US + m4_kUS[k4], B_US + M4_N - m4_kUS[k4])
    pCN = rng.beta(A_CN + m4_kCN[k4], B_CN + M4_N - m4_kCN[k4])
    off = m4_off[k4]
    pUS = expit(logit(np.clip(pUS, 1e-4, 1 - 1e-4)) + cfg["s4_cap_US"] * z_cap_b + cfg["us_s4_shift"])
    pCN = expit(logit(np.clip(pCN, 1e-4, 1 - 1e-4)) + cfg["s4_cap_CN"] * z_cap_b)
    P["m4 draw P(S4 US)"] = pUS; P["m4 draw P(S4 China)"] = pCN
    T4U = np.maximum(T2 + off[o] + rng.normal(0, 1, N), T1 + 0.25)
    T4C = np.maximum(T2 + off[o] + rng.normal(0, 1, N), T1 + 0.25)
    pU = pUS[o].copy()
    pU = np.where(TBe < T4U, np.maximum(0.5 * pU, pU - cfg["B_US_mech"]), pU)
    bon = cfg["broad_on"]
    S4U_raw = S2 & (rng.random(N) < pU) & bon
    S4C_raw = S2 & (rng.random(N) < pCN[o]) & bon
    S4U = S4U_raw & (T4U < HZ); S4C = S4C_raw & (T4C < HZ)
    US_pending_raw = S4U_raw & ~(T4U < HZ)
    T4U = np.where(S4U, T4U, INF); T4C = np.where(S4C, T4C, INF)
    sU = np.clip(cfg["strict_US"] + rng.normal(0, 0.08, NO), 0.05, 0.98)
    sC = np.clip(cfg["strict_CN"] + rng.normal(0, 0.06, NO), 0.02, 0.9)
    strictU = S4U & (rng.random(N) < sU[o]); strictC = S4C & (rng.random(N) < sC[o])

    # ---------------- S2b ----------------
    pess = rng.random(NO) < cfg["pess_w"]
    ps2b = np.where(pess, cfg["s2b_pess"], cfg["s2b_base"])[o]
    odds = ps2b / (1 - ps2b) * np.where(S4U_raw, cfg["s2b_or_noredist"], cfg["s2b_or_redist"])
    T2b = T2 + rng.uniform(0, 4, N)
    S2b = S2 & (rng.random(N) < odds / (1 + odds)) & (T2b < HZ)
    T2b = np.where(S2b, T2b, INF)

    # ---------------- S4 aftermath via m5 analogs (valid while rulers need human staff) ----------
    k5 = pick_by_copula(rng, m5_p5, -z_inst, cfg["rho_m5_inst"])
    p5 = expit(logit(np.clip(m5_p5[k5], 1e-4, 1 - 1e-4)) + cfg["s5_cap"] * z_cap_b)
    lag5_d = m5_lag5[k5]
    P["m5 draw P(S5|S4) (human-staffed analogs)"] = p5
    if cfg["kbroad_fixed"] is not None:
        kbroad = np.full(NO, cfg["kbroad_fixed"], float); act_nb = np.full(NO, ACT_SHARE)
    else:
        kact = rng.uniform(cfg["kact_lo"], cfg["kact_hi"], NO); kneg = rng.uniform(cfg["kneg_lo"], cfg["kneg_hi"], NO)
        kbroad = ACT_SHARE * kact + (1 - ACT_SHARE) * kneg
        act_nb = ACT_SHARE * kact / np.maximum(kbroad, 1e-9)
    P["k_broad (S5 given neglect-only S4)"] = kbroad
    p6d = rng.choice(m5_p6, NO)
    j7 = rng.integers(0, len(m6_p7), NO)
    p7d = np.clip(m6_p7[j7] * cfg["p7_scale"], 0, 1); pmisd = m6_pmis[j7]

    def aftermath(S4, T4, strict):
        pj = p5[o] * np.where(strict, 1.0, kbroad[o])
        od = pj / (1 - pj) * np.where(T2b < T4 + 5, cfg["s2b_s5_or"], 1.0)
        pj = od / (1 + od)
        pb = np.minimum(pj * S5B_ONLY_RATIO, 0.5 * (1 - pj)) if cfg["count_S5b"] else np.zeros(N)
        wr = [W_EXIT["reform"] * np.exp(cfg["reform_inst"] * z_inst[o]), np.full(N, W_EXIT["ext"]),
              np.full(N, W_EXIT["coup"]), np.full(N, W_EXIT["ware"])]
        w = np.stack(wr); w = w / w.sum(0) * (1 - pj - pb)
        cum = np.cumsum(np.vstack([pj, pb, w]), 0)
        cat = (rng.random(N)[None, :] > cum).sum(0)   # 0 S5, 1 S5b, 2 reform, 3 ext, 4 coup, 5 ware
        cat = np.where(S4, cat, -1)
        lag = lag5_d[o] + rng.normal(0, 1.5, N)
        T5 = np.where(cat == 0, T4 + np.maximum(lag, 0.5), INF)
        T5b = np.where(cat == 1, T4 + np.maximum(lag, 0.5), INF)
        Tex = np.where(cat >= 2, T4 + rng.uniform(2, 20, N), INF)
        Tex = np.where(cat == 5, INF, Tex)
        ch = np.where(rng.random(N) < np.where(strict, ACT_SHARE, act_nb[o]), 4, 5)   # broad killing / famine
        return cat, T5, T5b, Tex, ch

    catU, T5U_an, T5bU_an, TexU_an, chU_an = aftermath(S4U, T4U, strictU)
    catC, T5C_an, T5bC_an, TexC_an, chC_an = aftermath(S4C, T4C, strictC)

    # ---------------- m8 closure path (parallel, no S2 required), 6 blocs ----------------------
    def m8t(x):
        return np.where(x < HZ, x, INF)
    on = cfg["m8_on"]
    tc = m8t(D8["tc"][j]) if on else np.full((N, A_N), INF)                     # D_core < 0.2 per bloc
    tcU_r = tc[:, 0] if cfg["d_replace"] else np.full(N, INF)
    tcC_r = tc[:, 1] if cfg["d_replace"] else np.full(N, INF)
    fc = D8["fc"][j]; fad = D8["fad"][j]

    def gate(x):
        return m8t(x) if on else np.full(np.shape(x), INF)
    tgrab = gate(D8["tgrab"][j])

    # US broad path: analogs before closure; a regime in place at/after closure -> autocratic m8 outcome
    preU = T5U_an < tcU_r
    T5U_pre = np.where(preU, T5U_an, INF)
    T5bU_pre = np.where(T5bU_an < tcU_r, T5bU_an, INF)
    TexU = np.where(TexU_an < tcU_r, TexU_an, INF)
    # B8 fix: a US S4 regime that committed a broad-analog S5 (or S5b) before closure is still in place at closure, so
    # the closure path must use the US-autocratic history; round 2 excluded these (~preU, ~S5b) and fell back to the
    # baseline US history. Only regimes that EXITED before closure (reform, external, coup) revert to the baseline.
    regU = S4U & (tcU_r < HZ) & ~(TexU_an < tcU_r) & on
    if not cfg.get("b8_fix", True):
        regU = regU & ~preU & ~(T5bU_an < tcU_r)
    use_base = fad[:, 0] & (fc[:, 0] >= 0)
    cfU = regU & ~use_base                           # US history replaced by the US-autocratic counterfactual
    # Round 3 (cf_world): when the US history is replaced, the WHOLE world is taken from the same counterfactual
    # simulation, so the other blocs see the cross-bloc campaigns (B5) that this autocratic US launches and no longer
    # carry campaigns or kinetic balances from the replaced democratic-US history. Round 3a switched only the US
    # columns (one US history, five blocs from another). The US closure clock used for the gating above stays baseline.
    cfw = cfg.get("cf_world", True) and on

    def W(k):
        x = D8[k][j]
        if not cfw:
            return x
        m = cfU.reshape((-1,) + (1,) * (x.ndim - 1))
        return np.where(m, D8["cfw_" + k][j], x)
    fc = W("fc"); fad = W("fad"); tdec = W("tdec"); ce = W("ce"); fe = W("fe")
    TLd8 = gate(W("tLd")); TLt8 = gate(W("tLt"))                               # (N, 6, 4)
    chd8 = W("chd"); cht8 = W("cht")
    tcap8 = gate(W("tcap")); loss8 = W("loss") if on else np.zeros((N, A_N))
    if cfw:
        tc_w = m8t(W("tc")) if on else np.full((N, A_N), INF)
        tc = np.column_stack([tc[:, 0], tc_w[:, 1:]])
        if cfg["d_replace"]:
            tcC_r = tc[:, 1]
    cf_tLd = gate(D8["cf_tLd"][j]); cf_tLt = gate(D8["cf_tLt"][j])
    tLdA = np.where(use_base[:, None], TLd8[:, 0, :], cf_tLd); tLtA = np.where(use_base[:, None], TLt8[:, 0, :], cf_tLt)
    chdA = np.where(use_base, chd8[:, 0], D8["cf_chd"][j]); chtA = np.where(use_base, cht8[:, 0], D8["cf_cht"][j])
    tda = np.where(use_base, tdec[:, 0], D8["cf_tdec"][j]); cea = np.where(use_base, ce[:, 0], D8["cf_ce"][j])
    fca = np.where(use_base, fc[:, 0], D8["cf_fc"][j])
    capA = np.where(use_base, tcap8[:, 0], gate(D8["cf_tcap"][j]))
    lossA = np.where(use_base, loss8[:, 0], D8["cf_loss"][j] if on else 0.0)
    with np.errstate(invalid="ignore"):
        lag_a = np.where(np.isfinite(tLdA[:, 0]) & np.isfinite(tda), np.maximum(tLdA[:, 0] - tda, 0.5), 1.0)
    floorU = np.maximum(T4U + lag_a, 0)[:, None]
    TLdU_post = m8t(np.where(regU[:, None] & np.isfinite(tLdA), np.maximum(tLdA, floorU), INF))
    TLtU_post = m8t(np.where(regU[:, None] & np.isfinite(tLtA), np.maximum(tLtA, floorU), INF))
    # audit fix: the captive-remnant clock gets the same floor as the ladder (it was left unfloored)
    capA = m8t(np.where(regU & np.isfinite(capA), np.maximum(capA, floorU[:, 0]), INF))
    # China broad path: analogs before China closes; after closure China's m8 outcome (autocratic) applies
    preC = T5C_an < tcC_r
    T5C_pre = np.where(preC, T5C_an, INF)
    T5bC_pre = np.where(T5bC_an < tcC_r, T5bC_an, INF)
    TexC = np.where(TexC_an < tcC_r, TexC_an, INF)
    regC = S4C & (tcC_r < HZ) & ~preC & ~(T5bC_an < tcC_r) & ~(TexC_an < tcC_r) & on

    # ---------------- S5b (non-lethal fertility suppression) under autocratic warehousing -------
    pf = rng.beta(cfg["fert_a"], cfg["fert_b"], NO)
    P["P(fertility suppression | autocratic warehousing)"] = pf

    def fert(mask, tstart):
        occ = mask & np.isfinite(tstart) & (rng.random(N) < pf[o])
        return np.where(occ, tstart + rng.uniform(cfg["fert_lag_lo"], cfg["fert_lag_hi"], N), INF)
    wareA = [((fc[:, a] == 1) & fad[:, a]) | ((ce[:, a] == 1) & fe[:, a]) for a in range(A_N)]
    T5b_m8 = [m8t(fert(wareA[a] & on & ((~cfU) if a == 0 else True), tdec[:, a])) for a in range(A_N)]
    wareUpost = regU & ((fca == 1) | (cea == 1))
    T5bU_post = m8t(fert(wareUpost, np.maximum(tda, T4U)))

    # ---------------- Alt A ----------------
    fA = rng.standard_normal(NO); sA = rng.standard_normal(NO)
    pform = expit(logit(cfg["A_form"]) + cfg["A_form_sd"] * fA)
    TAf = T2 + rng.uniform(0, 10, N)
    pform_p = expit(logit(pform[o]) + np.where(T2b < TAf, cfg["A_s2b_logit"], 0.0))
    Aform = S2 & ~(TBe < T2 + 5) & (rng.random(N) < pform_p) & (TAf < HZ)
    psurv = expit(logit(cfg["A_surv"]) + cfg["A_surv_sd"] * sA)
    psurv_p = expit(logit(psurv[o]) + np.where(strictU, cfg["A_strict_logit"], 0.0) + 0.3 * z_inst[o])
    Asurv = Aform & (rng.random(N) < psurv_p)
    TAf = np.where(Aform, TAf, INF)

    # ---------------- background absorbing hazards ----------------
    Pai = np.minimum(cfg["Pai_med"] * np.exp(cfg["Pai_sig"] * rng.standard_normal(NO) + cfg["Pai_cap_load"] * D8["z_cap"]), cfg["Pai_cap"])
    P["P(background AI takeover prior)"] = Pai
    hai = -np.log(1 - Pai) / cfg["Pai_window"]
    mS4 = rng.uniform(cfg["ai_s4_mult_lo"], cfg["ai_s4_mult_hi"], NO)
    T4min = np.minimum.reduce([T4U, T4C, tgrab])
    sw = np.maximum(T4min, agi)
    E = rng.exponential(1.0, N); H1 = np.where(np.isfinite(sw), hai[o] * (sw - agi), INF)
    with np.errstate(invalid="ignore"):
        Tai = np.where(E < H1, agi + E / hai[o], sw + (E - H1) / (hai[o] * mS4[o]))
    Pcat = np.minimum(cfg["Pcat_med"] * np.exp(cfg["Pcat_sig"] * rng.standard_normal(NO)), 0.4)
    P["P(non-AI catastrophe by 2075)"] = Pcat
    Tcat = T0 + rng.exponential(1.0, N) / (-np.log(1 - Pcat[o]) / (2076.0 - T0))
    Tabs0 = np.minimum(Tai, Tcat)
    lim = np.minimum(Tabs0, HZ)

    def cens(T):
        return np.where(T < (lim if np.ndim(T) == 1 else lim[:, None] if np.ndim(T) == 2 else lim[:, None, None]), T, INF)
    T1r = np.where(T1 < np.minimum(Tabs0, HZ1), T1, INF)
    T2r = np.where(T1r < INF, cens(T2), INF); T2br = np.where(T2r < INF, cens(T2b), INF)
    T3r = np.where(T1r < INF, cens(T3), INF)
    T4Ur = np.where(T2r < INF, cens(T4U), INF); T4Cr = np.where(T2r < INF, cens(T4C), INF)
    g4U = T4Ur < INF; g4C = T4Cr < INF

    # ---------------- per-bloc ladders (deliberate and total), paths, channels ----------------
    # path codes: 0 broad analog, 1 broad S4 then closure, 2 closure path (m8)
    TLd = np.full((N, A_N, NL), INF); TLt = np.full((N, A_N, NL), INF)
    T5d = np.full((N, A_N), INF); ch5d = np.full((N, A_N), -1); pth5d = np.full((N, A_N), -1)
    for a in range(A_N):
        m8d = cens(TLd8[:, a, :]); m8tt = cens(TLt8[:, a, :])
        if a == 0:
            m8d = np.where(cfU[:, None], INF, m8d); m8tt = np.where(cfU[:, None], INF, m8tt)
            postd = np.where(g4U[:, None], cens(TLdU_post), INF); postt = np.where(g4U[:, None], cens(TLtU_post), INF)
            pre = np.where(g4U, cens(T5U_pre), INF)
            cands = [(pre, chU_an, 0), (postd[:, 0], chdA, 1), (m8d[:, 0], chd8[:, 0], 2)]
            TLd[:, a, :] = np.minimum(m8d, postd); TLt[:, a, :] = np.minimum(m8tt, postt)
        elif a == 1:
            pre = np.where(g4C, cens(T5C_pre), INF)
            cands = [(pre, chC_an, 0), (m8d[:, 0], chd8[:, 1], 2)]
            TLd[:, a, :] = m8d; TLt[:, a, :] = m8tt
        else:
            pre = np.full(N, INF)
            cands = [(m8d[:, 0], chd8[:, a], 2)]
            TLd[:, a, :] = m8d; TLt[:, a, :] = m8tt
        TLd[:, a, 0] = np.minimum(TLd[:, a, 0], pre)                    # human-staffed analogs: >=10% rung only
        TLt[:, a, :] = np.minimum(TLt[:, a, :], TLd[:, a, :])            # a deliberate rung is also a total rung
        T5d[:, a], ch5d[:, a], pth5d[:, a] = first_of(cands)
    # China m8 S5 after a China broad S4 counts as "broad S4 then closure"
    pth5d[:, 1] = np.where((pth5d[:, 1] == 2) & (T4Cr < T5d[:, 1]), 1, pth5d[:, 1])
    T5t = TLt[:, :, 0]
    ch5t = np.where(T5t < T5d, np.where(np.arange(A_N)[None] == 0, np.where(cfU, chtA, cht8[:, 0])[:, None], cht8), ch5d)
    # captive remnant (A11) and world population loss at the horizon
    capt = cens(np.column_stack([np.where(regU, capA, np.where(cfU, INF, tcap8[:, 0]))] + [tcap8[:, a] for a in range(1, A_N)]))
    lossH = loss8.copy(); lossH[:, 0] = np.where(regU, lossA, loss8[:, 0])
    # audit fix: the horizon loss must agree with the (floored, censored) total ladder. Old code zeroed every bloc's
    # loss when a background absorbing event occurred, even for blocs already depopulated before it (4% of paths).
    # lo = highest rung reached before censoring; hi = first rung not reached (loss is kept strictly below it).
    thr_arr = np.asarray(LTH)
    reached = np.isfinite(TLt)                                          # (N, A, NL), already censored
    lo = np.where(reached, thr_arr[None, None, :], 0.0).max(-1)
    hi = np.where(~reached, thr_arr[None, None, :] - 1e-6, 1.0).min(-1)
    absorbed = (Tabs0 < HZ)[:, None]
    lossH = np.where(absorbed, lo, np.clip(lossH, lo, hi))              # absorbed: only what was reached before it
    lossH = np.maximum(lossH, 0.10 * np.isfinite(T5d))                 # analog S5 = at least 10% of that bloc
    world_loss = (lossH * POP[None]).sum(1) / POP.sum()

    # first deliberate S5, US-or-China and any bloc
    def first_bloc(blocs):
        b = np.asarray(blocs)
        i = T5d[:, b].argmin(1); n = np.arange(N)
        T = T5d[:, b][n, i]
        return T, np.where(np.isfinite(T), ch5d[:, b][n, i], -1), np.where(np.isfinite(T), pth5d[:, b][n, i], -1), b[i]
    T5any, ch5, pth5, jur5 = first_bloc(range(A_N))
    T5UC, ch5UC, pth5UC, jurUC = first_bloc([0, 1])
    reachedS5 = T5any < INF

    def path_label(T, pth):
        return np.select([~np.isfinite(T), pth == 0, pth == 1, (pth == 2) & (T2r < T)],
                         ["none", "broad_analog", "broad_S4_then_closure", "closure_after_S2_not_required"],
                         "closure_without_S2")
    path_lab = path_label(T5any, pth5); path_labUC = path_label(T5UC, pth5UC)

    T5b_list = [np.where(g4U, cens(T5bU_pre), INF), np.where(g4C, cens(T5bC_pre), INF),
                np.where(g4U, cens(T5bU_post), INF)] + [cens(x) for x in T5b_m8]
    T5bany = np.minimum.reduce(T5b_list) if cfg["count_S5b"] else np.full(N, INF)
    TBr = cens(TB); TBer = cens(TBe); TAfr = np.where(T2r < INF, cens(TAf), INF)
    tgr = cens(tgrab)
    tcl = cens(tc.min(1))

    # ---------------- S6 / S7 (after a deliberate S5, v2 logic) ----------------
    occ6 = reachedS5 & (rng.random(N) < p6d[o])
    T6 = cens(np.where(occ6, T5any + rng.choice(m5_lag6, N), INF))
    u7 = rng.random(N)
    cat7 = np.where(u7 < p7d[o], 1, np.where(u7 < p7d[o] + pmisd[o], 2, np.where(u7 < p7d[o] + pmisd[o] + PW_WAR, 3, 0)))
    T7x = T6 + m6_yrs_f[rng.integers(0, len(m6_yrs_f), N)]
    T7 = np.where((T6 < INF) & (cat7 == 1) & (T7x < HZ), T7x, INF)
    Tmis = np.where((T6 < INF) & (cat7 == 2) & (T7x < HZ), T7x, INF)

    # ---------------- status at horizon ----------------
    ai_first = Tai < np.minimum(Tcat, HZ)
    cat_first = Tcat < np.minimum(Tai, HZ)
    alive = ~(Tabs0 < HZ)
    exU = np.where(TexU < lim, TexU, INF); exC = np.where(TexC < lim, TexC, INF)
    US_S4_persist = g4U & ~(exU < INF) & ~regU
    CN_S4_persist = g4C & ~(exC < INF) & ~regC
    # held without rights after closure: current choice warehouse/neglect/depopulate/rentier under autocracy
    harsh = np.isin(ce, [1, 2, 3, 4]) & fe & on & (tdec < HZ)
    harsh[:, 0] = np.where(regU, np.isin(cea, [1, 2, 3, 4]) & (tda < HZ), harsh[:, 0] & ~cfU)
    held = harsh & alive[:, None]
    captive = np.isfinite(capt)
    autoc_end = fe.copy(); autoc_end[:, 0] = np.where(regU, True, fe[:, 0])
    autoc_end = autoc_end & on & alive[:, None]
    us_grab_persist = (tgr < INF) & alive
    closure_decided = on & (np.where(np.isfinite(tdec), tdec, INF).min(1) < HZ) & alive
    S5nd_only = (T5t.min(1) < INF) & ~reachedS5
    near_total_d = np.isfinite(TLd[:, :, 3]).any(1)
    names = [
        "S7: AI moral rebellion vs dictators",
        "S6 then misaligned AI takeover",
        "S6: paranoid singleton",
        "S5 deliberate, near-total (>=99.9%) in some bloc: captive remnant without rights",
        "S5 deliberate, partial (>=10%, <99.9%): active killing, collusive or cross-bloc war",
        "S5 deliberate, partial (>=10%, <99.9%): lethal neglect / famine",
        "S5 non-deliberate only (attrition or war >=10%)",
        "S5b: fertility suppression only (non-lethal)",
        "AI takeover not tied to dictators",
        "Non-AI global catastrophe",
        "Public held without rights after loop closure (warehouse/neglect/rentier, any bloc)",
        "Broad S4 repression regime persisting (before closure)",
        "US narrow power grab persisting (public not warehoused)",
        "Alt B: decentralized AI wins (baseline historical adoption, no mobilization; unchanged black box)",
        "Alt A: tolerated parallel economy",
        "Other (S4 ended by coup/external, US S4 pending)",
        "S2, accommodated (no S4, or S4 then reform)",
        "Loop closed, public served or status quo (democratic or benevolent)",
        "Automation race (S1) without participation collapse",
        "No automation race by 2075",
    ]
    held_any = held.any(1)
    other_m = (g4U & (exU < INF) & np.isin(catU, [3, 4])) | (g4C & (exC < INF) & np.isin(catC, [3, 4])) \
        | ((T2r < INF) & US_pending_raw & ~g4U)
    masks = [T7 < INF, Tmis < INF, T6 < INF, reachedS5 & near_total_d, reachedS5 & np.isin(ch5, [0, 1, 3, 4, 8]),
             reachedS5 & np.isin(ch5, [2, 5]), S5nd_only, T5bany < INF,
             ai_first, cat_first, held_any, US_S4_persist | CN_S4_persist, us_grab_persist,
             TBer < INF, Asurv & (TAfr < INF), other_m, T2r < INF, closure_decided,
             T1r < INF, np.ones(N, bool)]
    ES = np.full(N, -1, dtype=np.int16)
    for i, m in enumerate(masks):
        ES[(ES < 0) & m] = i

    R = dict(S1=T1r, S2=T2r, S4=np.minimum(T4Ur, T4Cr), S5_deliberate_any=T5any, S5_deliberate_US_or_China=T5UC,
             S5_total_any=T5t.min(1), S5_total_US_or_China=T5t[:, :2].min(1), S5b=T5bany, S6=T6, S7=T7,
             AltB=TBer, S2b=T2br, closure_any_bloc=tcl, US_power_grab=tgr)
    for jth, th in enumerate(LTH):
        R[f"loss>={th:g} deliberate US_or_China"] = TLd[:, :2, jth].min(1)
        R[f"loss>={th:g} deliberate any"] = TLd[:, :, jth].min(1)
        R[f"loss>={th:g} total any"] = TLt[:, :, jth].min(1)
    for lab in ["broad_analog", "broad_S4_then_closure", "closure_after_S2_not_required", "closure_without_S2"]:
        R["S5d any via " + lab] = np.where(path_lab == lab, T5any, INF)
        R["S5d US/CN via " + lab] = np.where(path_labUC == lab, T5UC, INF)
    R["S3"] = np.where((T2r < INF) & (T3r < INF), np.maximum(T3r, T1r), INF)
    # first-disempowerment clock per bloc (for the disempowerment figure): democratic breakdown or seizure,
    # first harsh decision, S5, captivity; US broad S4 counts from S4
    tbk = gate(W("tbreak")); thr_ = gate(W("tharsh"))
    tdis = np.minimum.reduce([tbk, thr_, T5d, capt])
    tdis[:, 0] = np.minimum(tdis[:, 0], T4Ur); tdis[:, 1] = np.minimum(tdis[:, 1], T4Cr)
    tdis = cens(tdis)
    txb_c = cens(gate(W("txb"))); tsing_c = cens(gate(W("tsing"))); tsl95_c = cens(gate(W("tsl95")))
    # audit diagnostic: cf_world trajectories where the US-autocratic counterfactual launches a cross-bloc campaign before the
    # floored US S4 regime date (T4U + lag); these campaigns are not floored (known approximation)
    xb_early = cfU & cfw & ((W("xb_by") == 0) & np.isfinite(txb_c) & (txb_c < floorU)).any(1)
    extras = dict(S4U=g4U, S4C=g4C, T5d=T5d, T5t=T5t, ch5d=ch5d, ch5t=ch5t, pth5d=pth5d, TLd=TLd, TLt=TLt,
                  regU=regU & g4U, regC=regC & g4C, cfU=cfU, held=held, captive=captive, autoc_end=autoc_end,
                  us_grab_persist=us_grab_persist, US_S4_persist=US_S4_persist, CN_S4_persist=CN_S4_persist,
                  path_lab=path_lab, path_labUC=path_labUC, ch5=ch5, ch5UC=ch5UC, jur5=jur5, world_loss=world_loss,
                  ai_any=Tai < HZ, alive=alive, tdis=tdis, near_total_d=near_total_d,
                  means=np.isfinite(cens(gate(W("tmeans")))).any(1), collusion=np.isfinite(cens(gate(W("tcol")))).any(1),
                  nuclear_collusive=np.isfinite(cens(gate(W("tnx")))).any(1),
                  cross_bloc=np.isfinite(txb_c).any(1),
                  single_UC=np.isfinite(tsing_c[:, :2]).any(1),
                  txb=txb_c, xb_by=np.where(np.isfinite(txb_c), W("xb_by"), -1), lc_xb=W("lc_xb") * on, lc_dom=W("lc_dom") * on,
                  inflicted=W("inflicted") * on, xb_nuc=np.isfinite(cens(gate(W("txb_nuc")))).any(1),
                  xb_rep=(W("n_xb_rep") > 0).any(1) & on,
                  tsing=tsing_c, tsl95=tsl95_c, xb_early=xb_early, ncd=W("ncd"), nce=W("nce"), sle=W("sle"), pers=W("pers") & on, fe_end=fe & on,
                  tdec=cens(gate(tdec)), tX=cens(gate(W("tX"))), cfw=cfw,
                  T5b_bloc=np.column_stack([np.minimum.reduce([T5b_list[0], T5b_list[2], cens(T5b_m8[0])]),
                                            np.minimum(T5b_list[1], cens(T5b_m8[1]))] + [cens(T5b_m8[a]) for a in range(2, A_N)]),
                  TBer=TBer, TBr=TBr, Aalt=Asurv & (TAfr < INF), T2r=T2r, T1r=T1r, closure_decided=closure_decided,
                  absorbed_ai=ai_first, absorbed_cat=cat_first, tcl=tcl, T4Ur=T4Ur, T4Cr=T4Cr, exU=exU, exC=exC,
                  S4U_before_closure=g4U & (T4Ur < tc[:, 0]), S4C_before_closure=g4C & (T4Cr < tc[:, 1]))
    return dict(o=o, NO=NO, NI=NI, R=R, ES=ES, names=names, P=P, extras=extras, HZ=HZ, p1=p1, rep=j % R8, R8=R8)


# ============================== summaries ==============================
def per_draw(sim, ind):
    return np.bincount(sim["o"], weights=np.asarray(ind, float), minlength=sim["NO"]) / sim["NI"]


def stats(sim, ind, n_boot=1000, seed=3):
    rng = np.random.default_rng(seed)
    ind = np.asarray(ind, float)
    pd_ = per_draw(sim, ind); NO, NI = sim["NO"], sim["NI"]
    m = pd_.mean()
    bm = pd_[rng.integers(0, NO, (n_boot, NO))].mean(1)
    var = pd_.var()
    R8 = sim.get("R8", 1); rep = sim.get("rep", np.zeros(len(ind), int))
    key = sim["o"] * R8 + rep
    cnt = np.bincount(key, minlength=NO * R8).reshape(NO, R8)
    s1 = np.bincount(key, weights=ind, minlength=NO * R8).reshape(NO, R8)
    with np.errstate(invalid="ignore", divide="ignore"):
        pr = np.where(cnt > 0, s1 / np.maximum(cnt, 1), 0.0)
    w = cnt / NI
    pd_r = (w * pr).sum(1)
    noise_d = (w * (pr - pd_r[:, None]) ** 2).sum(1) / (R8 - 1) if R8 > 1 else pd_ * (1 - pd_) / NI
    noise = float(noise_d.mean())
    shrink = np.sqrt(max(var - noise, 0) / var) if var > 0 else 0.0
    pd_dn = m + shrink * (pd_ - m)
    r = lambda x: float(round(x, 5))
    return dict(mean=r(m), mc_ci95_bootstrap=[r(np.quantile(bm, .025)), r(np.quantile(bm, .975))],
                epistemic_ci95=[r(np.quantile(pd_, .025)), r(np.quantile(pd_, .975))],
                epistemic_ci95_denoised=[r(max(np.quantile(pd_dn, .025), 0)), r(min(np.quantile(pd_dn, .975), 1))],
                epistemic_p10_p90=[r(np.quantile(pd_, .10)), r(np.quantile(pd_, .90))],
                sd_epistemic=r(np.sqrt(max(var - noise, 0))), share_noise_var=r(noise / var if var > 0 else 0)), pd_


def popw(mask2d):
    """per-trajectory share of world population in blocs where mask is true"""
    return (mask2d * POP[None]).sum(1) / POP.sum()


YRS_REP = [2030, 2035, 2040, 2045, 2050, 2060, 2075]


def stage_table(sim):
    tab = {}
    for k, T in sim["R"].items():
        row = {f"p_by_{y}": float(round(np.mean(T < y + 1), 5)) for y in YRS_REP}
        reached = T[T < sim["HZ"]]
        if len(reached) >= 50:
            row["median_year_if_reached"] = float(round(np.median(reached), 1))
            row["p10_year"] = float(round(np.quantile(reached, .1), 1))
            row["p90_year"] = float(round(np.quantile(reached, .9), 1))
        s, _ = stats(sim, T < sim["HZ"])
        row["p_by_horizon_epistemic_ci95_denoised"] = s["epistemic_ci95_denoised"]
        row["p_by_horizon_mc_ci95"] = s["mc_ci95_bootstrap"]
        tab[k] = row
    return tab


def sensitivity(sim, target_pd):
    P = sim["P"]; keys = list(P.keys())
    X = np.column_stack([np.asarray(P[k], float) for k in keys])
    NI = sim["NI"]
    noise = np.mean(target_pd * (1 - target_pd)) / min(NI, sim.get("R8", NI))
    vt = max(target_pd.var() - noise, 1e-12)
    Rk = np.column_stack([rankdata(X[:, i]) for i in range(X.shape[1])]); ry = rankdata(target_pd)
    res = []
    for i, k in enumerate(keys):
        v = X[:, i]
        rho = spearmanr(v, target_pd).statistic if np.std(v) > 0 else 0.0
        others = np.column_stack([np.ones(len(v)), np.delete(Rk, i, 1)])
        rx = Rk[:, i] - others @ np.linalg.lstsq(others, Rk[:, i], rcond=None)[0]
        rr = ry - others @ np.linalg.lstsq(others, ry, rcond=None)[0]
        prcc = float(np.corrcoef(rx, rr)[0, 1]) if np.std(rx) > 1e-9 else 0.0
        uniq = np.unique(v)
        if len(uniq) <= 4:
            groups = [target_pd[v == u] for u in uniq]
            lo_m, hi_m = target_pd[v == uniq.min()].mean(), target_pd[v == uniq.max()].mean()
        else:
            q = np.quantile(v, np.linspace(0, 1, 21)); b = np.clip(np.searchsorted(q, v, side="right") - 1, 0, 19)
            groups = [target_pd[b == g] for g in range(20)]
            t1, t2 = np.quantile(v, [1 / 3, 2 / 3])
            lo_m, hi_m = target_pd[v <= t1].mean(), target_pd[v >= t2].mean()
        gm = np.array([g.mean() for g in groups if len(g)]); gn = np.array([len(g) for g in groups if len(g)])
        eta2 = float(np.sum(gn * (gm - target_pd.mean()) ** 2) / len(target_pd) / vt)
        res.append(dict(param=k, spearman=round(float(rho), 3), partial_rank_corr=round(prcc, 3),
                        first_order_eta2_noise_corrected=round(min(eta2, 1.0), 3),
                        p_low_tercile=round(float(lo_m), 4), p_high_tercile=round(float(hi_m), 4), delta=round(float(hi_m - lo_m), 4)))
    res.sort(key=lambda r: -abs(r["delta"]))
    return res


def headline(sim):
    ES = sim["ES"]; X = sim["extras"]; R = sim["R"]; HZ = sim["HZ"]
    T5d, T5t, TLd, TLt = X["T5d"], X["T5t"], X["TLd"], X["TLt"]
    held_h = X["held"] | X["captive"] | np.isfinite(T5d)
    held_h[:, 0] |= X["US_S4_persist"] | X["us_grab_persist"]
    held_h[:, 1] |= X["CN_S4_persist"]
    dis_aut = held_h | X["autoc_end"]
    return dict(
        s5d_UC=np.isfinite(T5d[:, :2]).any(1), s5d_any=np.isfinite(T5d).any(1),
        s5t_UC=np.isfinite(T5t[:, :2]).any(1), s5t_any=np.isfinite(T5t).any(1),
        nt_UC=np.isfinite(TLd[:, :2, 3]).any(1), nt_any=np.isfinite(TLd[:, :, 3]).any(1),
        nt_world=X["world_loss"] >= LTH[3] - 1e-9,
        held=held_h, dis_aut=dis_aut,
        disemp_UC=held_h[:, :2].any(1), disemp_aut_UC=dis_aut[:, :2].any(1), disemp_any=held_h.any(1),
        disemp_aut_any=dis_aut.any(1), us_disemp=held_h[:, 0], us_disemp_aut=dis_aut[:, 0],
        s5plus=ES <= 6)


OUTCOME_CATS = [
    ("near_total_deliberate", ">=99.9% deliberate loss (near-total depopulation; captive remnant without rights)"),
    ("partial_deliberate", "deliberate loss >=10% but <99.9% (killing, collective punishment, lethal neglect, collusive or cross-bloc war, broad-path analog)"),
    ("non_deliberate_mass_death", ">=10% loss from attrition (despair, crackdown) or ordinary war only, no deliberate S5"),
    ("background_absorbing_event", "background AI takeover not tied to dictators, or non-AI global catastrophe, before any of the above (public's fate not modeled)"),
    ("stripped_of_rights_no_mass_death", "public held without rights (warehouse/neglect/rentier, broad S4 persisting, US grab, fertility suppression), no >=10% loss"),
    ("autocratic_short_of_that", "autocratic rule at 2075 (A6), public not stripped of rights, no mass death"),
    ("public_keeps_standing", "public keeps its standing: democratic or served/status quo, incl. Alt B at baseline adoption"),
]


def outcome_class(sim, H):
    """mutually exclusive outcome class per trajectory and bloc (N, A): index into OUTCOME_CATS, worst first.
    The background absorbing event is global; the others are bloc-level. A bloc's class is the first that applies."""
    X = sim["extras"]; N = len(sim["ES"])
    nt = np.isfinite(X["TLd"][:, :, 3]); pdl = np.isfinite(X["T5d"]); ndl = np.isfinite(X["T5t"])
    absb = np.broadcast_to(~X["alive"][:, None], nt.shape)
    strip = H["held"] | np.isfinite(X["T5b_bloc"])
    aut = H["dis_aut"]
    cls = np.full(nt.shape, 6, dtype=np.int8)
    for i, m in reversed(list(enumerate([nt, pdl, ndl, absb, strip, aut]))):
        cls = np.where(m, i, cls)
    return cls


def breakdown(sim, H, blocs):
    """joint class for a set of blocs = worst (lowest index) class among them; sums to 1 by construction"""
    X = sim["extras"]
    cls = outcome_class(sim, H)[:, blocs].min(1)
    out = {}
    for i, (k, lab) in enumerate(OUTCOME_CATS):
        s, _ = stats(sim, cls == i)
        s["definition"] = lab
        out[k] = s
    keep = cls == 6
    sub = {"Alt B decentralized AI effective (baseline historical adoption, no mobilization; black box, unchanged)": keep & np.isfinite(X["TBer"]),
           "Alt A tolerated parallel economy": keep & ~np.isfinite(X["TBer"]) & X["Aalt"],
           "loop closed (some bloc), public served or status quo, no autocracy in these blocs": keep & ~np.isfinite(X["TBer"]) & ~X["Aalt"] & X["closure_decided"],
           "no closure decision by 2075 (automation race or earlier stage only)": keep & ~np.isfinite(X["TBer"]) & ~X["Aalt"] & ~X["closure_decided"]}
    out["_public_keeps_standing_split"] = {k: round(float(v.mean()), 5) for k, v in sub.items()}
    out["_sum_check"] = round(float(sum(out[k]["mean"] for k, _ in OUTCOME_CATS)), 6)
    out["_P(Alt B effective) within each class"] = {k: (round(float(np.isfinite(X["TBer"])[cls == i].mean()), 4) if (cls == i).any() else None)
                                                   for i, (k, _) in enumerate(OUTCOME_CATS)}
    return out, cls


def med_q(T):
    T = T[np.isfinite(T)]
    if len(T) < 30:
        return None
    return dict(median=float(round(np.median(T), 2)), p10=float(round(np.quantile(T, .1), 2)), p90=float(round(np.quantile(T, .9), 2)))


def round3_outputs(sim, H):
    X = sim["extras"]; HZ = sim["HZ"]; N = len(sim["ES"])
    TLd, TLt, T5d = X["TLd"], X["TLt"], X["T5d"]
    alive = X["alive"]
    out = {}
    # ---------- outcome breakdown (mutually exclusive) ----------
    bd_UC, cls_UC = breakdown(sim, H, [0, 1])
    out["outcome_breakdown_US_or_China_2075"] = bd_UC
    out["outcome_breakdown_US_bloc_2075"] = breakdown(sim, H, [0])[0]
    out["outcome_breakdown_China_bloc_2075"] = breakdown(sim, H, [1])[0]
    clsA = outcome_class(sim, H)
    out["outcome_breakdown_by_bloc_2075"] = {ACT[a]: {k: round(float((clsA[:, a] == i).mean()), 5) for i, (k, _) in enumerate(OUTCOME_CATS)} for a in range(A_N)}
    out["outcome_breakdown_world_population_weighted_2075"] = {k: round(float(popw(clsA == i).mean()), 5) for i, (k, _) in enumerate(OUTCOME_CATS)}
    out["outcome_breakdown_semantics"] = ("Each trajectory is assigned to exactly one class per bloc, worst first, in the listed order. For US-or-China "
                                          "the joint class is the worse of the two blocs, so near_total_deliberate equals the headline. "
                                          "The background absorbing event is global and censors later events (as in v2-v4). Autocratic "
                                          "rule includes the US-autocratic counterfactual history when a US broad S4 regime reaches closure. "
                                          "Because the China bloc starts autocratic, the joint US-or-China class 'public keeps standing' is "
                                          "near 0 by construction; the per-bloc US breakdown is the informative one for that class.")
    # ---------- B2 consolidation ----------
    ts = X["tsing"]; fe = X["fe_end"] & alive[:, None]
    single_end = fe & (X["nce"] == 1)
    dec_aut = np.isfinite(X["tdec"]) & np.isfinite(X["ncd"]) & (X["ncd"] <= 21)
    exe = np.isfinite(X["tX"])
    cons = {"definition": "B2: a coalition of one (all other members purged or dead) controls the bloc's coercive force. m8_v4 imposes no singleton; this is what purge/counter-coup incentives produce.",
            "P(single decider reached by 2075) US or China": stats(sim, np.isfinite(ts[:, :2]).any(1))[0],
            "P(single decider reached by 2075) any bloc": stats(sim, np.isfinite(ts).any(1))[0],
            "year single decider first reached, US or China (median, p10, p90)": med_q(ts[:, :2].min(1)),
            "expected world population share whose bloc reached a single decider by 2075": round(float(popw(np.isfinite(ts)).mean()), 5),
            "expected world population share ruled by a single decider AT 2075 (alive, autocratic, coalition of one)": round(float(popw(single_end).mean()), 5),
            "by_bloc": {}}
    for a in range(A_N):
        fa = fe[:, a]; da = dec_aut[:, a]; xa = exe[:, a]
        cons["by_bloc"][ACT[a]] = {
            "P(single decider reached by 2075)": round(float(np.isfinite(ts[:, a]).mean()), 5),
            "year reached (median, p10, p90)": med_q(ts[:, a]),
            "P(ruled by single decider at 2075)": round(float(single_end[:, a].mean()), 5),
            "P(autocratic at 2075)": round(float(fa.mean()), 5),
            "P(single decider at 2075 | autocratic at 2075)": round(float(single_end[fa, a].mean()), 4) if fa.any() else None,
            "P(personalist, leader holds >=50% of coercive control, at 2075 | autocratic)": round(float(X["pers"][fa, a].mean()), 4) if fa.any() else None,
            "median coalition size at 2075 | autocratic": float(np.nanmedian(X["nce"][fa, a])) if fa.any() else None,
            "P(single decider at first closure decision | autocratic decision)": round(float((X["ncd"][da, a] == 1).mean()), 4) if da.any() else None,
            "median coalition size at first decision | bloc later executes a depopulation order": float(np.nanmedian(X["ncd"][xa, a])) if xa.any() else None,
            "P(single decider before first deliberate S5 | deliberate S5 in bloc)": round(float((ts[:, a] < T5d[:, a])[np.isfinite(T5d[:, a])].mean()), 4) if np.isfinite(T5d[:, a]).any() else None,
            "P(single decider before >=99.9% rung | near-total in bloc)": round(float((ts[:, a] <= TLd[:, a, 3])[np.isfinite(TLd[:, a, 3])].mean()), 4) if np.isfinite(TLd[:, a, 3]).any() else None,
        }
    # joint: both US and China with a single decider
    cons["P(both US and China blocs reach a single decider by 2075)"] = stats(sim, np.isfinite(ts[:, :2]).all(1))[0]
    # audit: coalitions in m8_v4 are never refilled after purges (they can only shrink until a regime change), which pushes
    # the coalition-of-one count up. The leader's control share is the robust measure; variant b2_refill refills purged seats.
    cons["P(leader holds >=95% of coercive control by 2075) US or China (robust concentration measure)"] = stats(sim, np.isfinite(X["tsl95"][:, :2]).any(1))[0]
    cons["P(leader holds >=95% of coercive control by 2075) by bloc"] = {ACT[a]: round(float(np.isfinite(X["tsl95"][:, a]).mean()), 5) for a in range(A_N)}
    cons["audit_note"] = ("Purged seats are not refilled in the baseline, so 'coalition of one' is partly a bookkeeping artifact; with refilling "
                          "(variant m8: b2_refill) the coalition-of-one share goes to ~0 while the headline changes by about -0.01 and the "
                          "leader-control>=95% share falls from ~0.60 to ~0.46 (m8 standalone, US or China). Decisions depend on the leader's "
                          "control share, not the head count.")
    out["B2_consolidation"] = cons
    # ---------- B5 cross-bloc: who depopulates whom ----------
    txb = X["txb"]; by = X["xb_by"]; tg = np.isfinite(txb)
    ntA = np.isfinite(TLd[:, :, 3])
    foreign = ntA & (X["lc_xb"] > 0.5 * (X["lc_dom"] + X["lc_xb"]))
    wl = X["world_loss"]; wn = wl >= LTH[3] - 1e-9
    b5 = {"definition": "B5: an executing coalition with a near-total designation extends depopulation to a non-colluding bloc it overpowers kinetically (dominance >= dom_thr) when the payoff beats the nuclear-deterrent risk to its rulers. Aggressor = the attacking bloc of the (last) campaign against the target.",
          "P(some bloc targeted by a foreign closed actor)": stats(sim, tg.any(1))[0],
          "year of first cross-bloc campaign (median, p10, p90)": med_q(np.where(tg, txb, INF).min(1)),
          "P(bloc targeted)": {ACT[c]: round(float(tg[:, c].mean()), 5) for c in range(A_N)},
          "P(bloc is an aggressor)": {ACT[a]: round(float((by == a).any(1).mean()), 5) for a in range(A_N)},
          "who_depopulates_whom P(aggressor row attacks target column)": {ACT[a]: {ACT[c]: round(float((by[:, c] == a).mean()), 5) for c in range(A_N)} for a in range(A_N)},
          "P(bloc depopulated >=99.9% mainly by a foreign actor)": {ACT[c]: round(float(foreign[:, c].mean()), 5) for c in range(A_N)},
          "P(bloc depopulated >=99.9% mainly by its own rulers)": {ACT[c]: round(float((ntA & ~foreign)[:, c].mean()), 5) for c in range(A_N)},
          "expected world pop share depopulated >=99.9%, mainly foreign": round(float(popw(foreign).mean()), 5),
          "expected world pop share depopulated >=99.9%, mainly domestic": round(float(popw(ntA & ~foreign).mean()), 5),
          "P(nuclear retaliation against a cross-bloc attack)": stats(sim, X["xb_nuc"])[0],
          "P(a cross-bloc campaign repelled)": stats(sim, X["xb_rep"])[0],
          "expected deaths inflicted abroad by bloc, bn (mean over trajectories)": {ACT[a]: round(float((X["inflicted"][:, a] * POP[a]).mean()), 4) for a in range(A_N)},
          }
    if wn.any():
        nexec = exe.sum(1); nagg = np.array([len(set(r[r >= 0])) for r in by[wn]])
        b5["given world loss >=99.9%"] = {
            "n_trajectories": int(wn.sum()),
            "share with a cross-bloc campaign": round(float(tg[wn].any(1).mean()), 4),
            "distribution of number of blocs whose own rulers executed a depopulation order": {str(k): round(float((nexec[wn] == k).mean()), 4) for k in range(A_N + 1)},
            "distribution of number of distinct aggressor blocs": {str(k): round(float((nagg == k).mean()), 4) for k in range(A_N + 1)},
            "P(bloc is an aggressor)": {ACT[a]: round(float((by[wn] == a).any(1).mean()), 4) for a in range(A_N)},
            "P(bloc depopulated mainly by a foreign actor)": {ACT[c]: round(float(foreign[wn, c].mean()), 4) for c in range(A_N)},
            "share where only US and/or China executed domestically and the rest was cross-bloc": round(float(((nexec[wn] <= 2) & ~exe[wn][:, 2:].any(1)).mean()), 4),
        }
    allb = np.isfinite(TLt[:, :, 3]).all(1)
    Tw = np.where(allb, TLt[:, :, 3].max(1), INF)
    b5["P(every bloc >=99.9% total loss by 2075) (consistency check vs world loss >=99.9%)"] = round(float(allb.mean()), 5)
    b5["year every bloc reached >=99.9% (median, p10, p90)"] = med_q(Tw)
    b5["world population loss distribution 2075 (share of trajectories)"] = {
        "<10%": round(float((wl < 0.1).mean()), 5), "10-50%": round(float(((wl >= 0.1) & (wl < 0.5)).mean()), 5),
        "50-90%": round(float(((wl >= 0.5) & (wl < 0.9)).mean()), 5), "90-99.9%": round(float(((wl >= 0.9) & (wl < 0.999 - 1e-9)).mean()), 5),
        ">=99.9%": round(float(wn.mean()), 5)}
    b5["US-autocratic counterfactual world used (cf_world) share of trajectories"] = round(float((X["cfU"] & X["cfw"]).mean()), 5)
    b5["audit: share of trajectories where the counterfactual US launches a cross-bloc campaign before its floored S4 date (not floored)"] = round(float(X["xb_early"].mean()), 5)
    out["B5_cross_bloc"] = b5
    yrs = np.arange(2027, 2076)
    curves = dict(world_all_blocs_near_total=[float(np.mean(Tw < y + 1)) for y in yrs],
                  cross_bloc_campaign_any=[float(np.mean(np.where(tg, txb, INF).min(1) < y + 1)) for y in yrs],
                  single_decider_by_bloc={ACT[a]: [float(np.mean(ts[:, a] < y + 1)) for y in yrs] for a in range(A_N)},
                  single_decider_US_or_China=[float(np.mean(ts[:, :2].min(1) < y + 1)) for y in yrs])
    return out, curves, cls_UC


def quick(cfg, D8, NI=200, seed=SEED + 11):
    sv = simulate(cfg, D8, NI, seed)
    h = headline(sv); X = sv["extras"]
    return {"P(>=99.9% deliberate) US or China": round(float(h["nt_UC"].mean()), 4),
            "P(>=99.9% deliberate) any bloc": round(float(h["nt_any"].mean()), 4),
            "P(world population loss >=99.9%)": round(float(h["nt_world"].mean()), 4),
            "P(S5 deliberate >=10%) US or China": round(float(h["s5d_UC"].mean()), 4),
            "P(S5 deliberate >=10%) any bloc": round(float(h["s5d_any"].mean()), 4),
            "P(S5 total >=10%) any bloc": round(float(h["s5t_any"].mean()), 4),
            "world pop share in blocs with >=99.9% deliberate loss": round(float(popw(np.isfinite(X["TLd"][:, :, 3])).mean()), 4),
            "P(S5d US/CN) by 2040": round(float(np.mean(sv["R"]["S5_deliberate_US_or_China"] < 2041)), 4),
            "P(US or China public stripped of rights, 2075)": round(float(h["disemp_UC"].mean()), 4),
            "P(US or China public disempowered incl. autocratic at 2075)": round(float(h["disemp_aut_UC"].mean()), 4),
            "P(closure any bloc by 2040)": round(float(np.mean(sv["R"]["closure_any_bloc"] < 2041)), 4),
            "P(B5 cross-bloc campaign, any)": round(float(X["cross_bloc"].mean()), 4),
            "P(B2 single decider US or China by 2075)": round(float(X["single_UC"].mean()), 4),
            "US/China breakdown": {k: round(float((breakdown(sv, h, [0, 1])[1] == i).mean()), 4) for i, (k, _) in enumerate(OUTCOME_CATS)}}


def main():
    t0 = time.time()
    NO, R8, NI = 3000, 8, 200
    small = os.environ.get("INT_SMALL")          # smoke test only: never used for results
    if small:
        NO = int(small)
    D8 = run_m8(NO, R8, "baseline")
    print("m8 baseline bundle", round(time.time() - t0, 1), "s"); sys.stdout.flush()
    sim = simulate(BASE_CFG, D8, NI, SEED)
    ES = sim["ES"]; R = sim["R"]; X = sim["extras"]; names = sim["names"]; HZ = sim["HZ"]
    es = {nm: stats(sim, ES == i)[0] for i, nm in enumerate(names)}
    H = headline(sim)
    s_nt, pd_nt = stats(sim, H["nt_UC"])
    s_s5, pd_s5 = stats(sim, H["s5d_UC"])
    T5d, T5t, TLd, TLt = X["T5d"], X["T5t"], X["TLd"], X["TLt"]
    # ladder
    ladder = {}
    for jth, th in enumerate(LTH):
        row = {}
        for nm, TL in [("deliberate", TLd), ("total", TLt)]:
            fin = np.isfinite(TL[:, :, jth])
            row[nm] = dict(US_or_China=stats(sim, fin[:, :2].any(1))[0], any_bloc=stats(sim, fin.any(1))[0],
                           world_pop_share_expected=round(float(popw(fin).mean()), 5),
                           by_bloc={ACT[a]: round(float(fin[:, a].mean()), 5) for a in range(A_N)})
        row["world_population_loss_at_least_this"] = stats(sim, X["world_loss"] >= th - 1e-9)[0]
        ladder[f">={th:g}"] = row
    by_year = {k: {str(y): round(float(np.mean(R[k] < y + 1)), 5) for y in YRS_REP}
               for k in ["loss>=0.999 deliberate US_or_China", "loss>=0.999 deliberate any", "S5_deliberate_US_or_China",
                         "S5_deliberate_any", "S5_total_any"]}
    # channels of the first deliberate S5
    chan_UC = {CH[c]: round(float(np.mean(H["s5d_UC"] & (X["ch5UC"] == c))), 5) for c in DELIB_CH}
    chan_any = {CH[c]: round(float(np.mean(H["s5d_any"] & (X["ch5"] == c))), 5) for c in DELIB_CH}
    # first S5 in total accounting by channel (any bloc)
    T5t_any = T5t.min(1); at = T5t.argmin(1); cht_first = X["ch5t"][np.arange(len(at)), at]
    chan_tot = {CH[c]: round(float(np.mean(np.isfinite(T5t_any) & (cht_first == c))), 5) for c in range(9)}
    aggs = {
        "HEADLINE P(>=99.9% deliberate depopulation of the US or China bloc by 2075)": s_nt,
        "HEADLINE P(>=99.9% deliberate depopulation of any bloc by 2075)": stats(sim, H["nt_any"])[0],
        "HEADLINE P(world population loss >=99.9% by 2075, all blocs)": stats(sim, H["nt_world"])[0],
        "HEADLINE expected share of world population living in blocs depopulated >=99.9%": round(float(popw(np.isfinite(TLd[:, :, 3])).mean()), 5),
        "P(S5 deliberate >=10%) US or China": s_s5,
        "P(S5 deliberate >=10%) any bloc": stats(sim, H["s5d_any"])[0],
        "P(S5 total >=10%) US or China": stats(sim, H["s5t_UC"])[0],
        "P(S5 total >=10%) any bloc": stats(sim, H["s5t_any"])[0],
        "expected world pop share in blocs with S5 deliberate": round(float(popw(np.isfinite(T5d)).mean()), 5),
        "expected world pop share in blocs with S5 total": round(float(popw(np.isfinite(T5t)).mean()), 5),
        "expected world population loss by 2075 (mean)": round(float(X["world_loss"].mean()), 5),
        "P(captive remnant exists in some bloc at 2075)": stats(sim, X["captive"].any(1))[0],
        "P(abstract means of rapid mass killing used in some bloc)": stats(sim, X["means"])[0],
        "P(collusion between depopulating coalitions)": stats(sim, X["collusion"])[0],
        "P(collusive nuclear exchange)": stats(sim, X["nuclear_collusive"])[0],
        "P(B5 cross-bloc depopulation campaign by a foreign closed actor, any bloc)": stats(sim, X["cross_bloc"])[0],
        "P(B2 US or China coalition consolidated to a single decider by 2075)": stats(sim, X["single_UC"])[0],
        "P(S5b fertility suppression, no deliberate S5)": stats(sim, (R["S5b"] < HZ) & ~H["s5d_any"])[0],
        "P(US or China public stripped of rights at 2075: held/captive/S5/S4 persisting/grab)": stats(sim, H["disemp_UC"])[0],
        "P(US or China public disempowered at 2075 incl. autocratic rule)": stats(sim, H["disemp_aut_UC"])[0],
        "P(any bloc public stripped of rights at 2075)": stats(sim, H["disemp_any"])[0],
        "expected world pop share stripped of rights at 2075": round(float(popw(H["held"]).mean()), 5),
        "expected world pop share disempowered incl. autocratic rule at 2075": round(float(popw(H["dis_aut"]).mean()), 5),
        "P(US-bloc public stripped of rights at 2075)": stats(sim, H["us_disemp"])[0],
        "P(US-bloc public disempowered incl. autocratic rule at 2075)": stats(sim, H["us_disemp_aut"])[0],
        "P(US narrow power grab by 2075)": stats(sim, R["US_power_grab"] < HZ)[0],
        "P(closure: some bloc core chain <20% human by 2040)": stats(sim, R["closure_any_bloc"] < 2041)[0],
    }
    by_bloc = {ACT[a]: dict(S5_deliberate=round(float(np.isfinite(T5d[:, a]).mean()), 5),
                            S5_total=round(float(np.isfinite(T5t[:, a]).mean()), 5),
                            near_total_deliberate=round(float(np.isfinite(TLd[:, a, 3]).mean()), 5),
                            captive_remnant=round(float(X["captive"][:, a].mean()), 5),
                            stripped_of_rights=round(float(H["held"][:, a].mean()), 5),
                            disempowered_incl_autocratic=round(float(H["dis_aut"][:, a].mean()), 5),
                            population_bn=float(POP[a])) for a in range(A_N)}
    path_out = {}
    for tag, pl, T, s5m in [("any_bloc", X["path_lab"], R["S5_deliberate_any"], H["s5d_any"]),
                            ("US_or_China", X["path_labUC"], R["S5_deliberate_US_or_China"], H["s5d_UC"])]:
        po = {}
        for lab in ["broad_analog", "broad_S4_then_closure", "closure_after_S2_not_required", "closure_without_S2"]:
            m = pl == lab
            tt = T[m]
            po[lab] = dict(P=stats(sim, m)[0], share_of_S5=round(float(m.sum() / max(s5m.sum(), 1)), 4),
                           median_year=float(round(np.median(tt), 1)) if len(tt) else None)
        path_out[tag] = po
    path_out["_labels"] = {
        "broad_analog": "S1->S2->S4->S5 while the ruling coalition still needs human staff (v2 m5 analogs); >=10% rung only",
        "broad_S4_then_closure": "S1->S2->S4, then the repression regime closes its loop; m8_v4 elite game and endgame decide",
        "closure_after_S2_not_required": "single-bloc closure path; S2 had occurred but was not needed",
        "closure_without_S2": "single-bloc closure path before any broad participation collapse (scenario's core mechanism)"}
    r3out, r3curves, cls_UC = round3_outputs(sim, H)
    stages = stage_table(sim)
    sens = sensitivity(sim, pd_nt)
    sens_s5 = sensitivity(sim, pd_s5)[:20]
    sens_dis = sensitivity(sim, per_draw(sim, H["disemp_UC"]))[:15]

    def cp(a, b):
        return round(float(a[b].mean()), 4) if b.sum() else None
    S1 = R["S1"] < HZ; S2 = R["S2"] < HZ
    zc = np.repeat(D8["z_cap"], NI)
    cond = {
        "P(S2|S1)": cp(S2, S1),
        "P(S4 US before US closure | S4 US)": cp(X["S4U_before_closure"], X["S4U"]),
        "P(US S4 regime reaches closure | S4 US)": cp(X["regU"], X["S4U"]),
        "P(near-total US or China | S5 deliberate US or China)": cp(H["nt_UC"], H["s5d_UC"]),
        "P(near-total any | S5 deliberate any)": cp(H["nt_any"], H["s5d_any"]),
        "P(S5d US/CN | fast capability tercile)": cp(H["s5d_UC"], zc > np.quantile(D8["z_cap"], 2 / 3)),
        "P(S5d US/CN | slow capability tercile)": cp(H["s5d_UC"], zc < np.quantile(D8["z_cap"], 1 / 3)),
        "P(near-total US/CN | fast capability tercile)": cp(H["nt_UC"], zc > np.quantile(D8["z_cap"], 2 / 3)),
        "P(near-total US/CN | slow capability tercile)": cp(H["nt_UC"], zc < np.quantile(D8["z_cap"], 1 / 3)),
        "median year of closure (any bloc) if reached": float(np.median(R["closure_any_bloc"][np.isfinite(R["closure_any_bloc"])])),
        "median year near-total US/CN if reached": float(np.median(R["loss>=0.999 deliberate US_or_China"][np.isfinite(R["loss>=0.999 deliberate US_or_China"])])) if H["nt_UC"].any() else None,
    }
    print("baseline integrated", round(time.time() - t0, 1),
          json.dumps({k: (v["mean"] if isinstance(v, dict) else v) for k, v in aggs.items()}, indent=0)); sys.stdout.flush()

    # ---------- structural variants ----------
    NOv, R8v = (1000, 8) if not small else (int(small), 8)
    B = BASE_CFG
    m8_vars = ["baseline", "round2_exact", "rev_B1_average_moral", "rev_B2_fixed_consolidation", "rev_B3_unenforced_stigma",
               "rev_B4_no_retribution", "rev_B5_no_cross_bloc", "rev_B6_caps_bypassed", "b2_no_purges", "no_nuclear_deterrent",
               "f6_caps_forced_x100", "all_round2", "rev_F1_median_rule", "rev_F2_refusal_v4", "rev_F3_no_defection",
               "rev_F4_dispositions_v4", "rev_F7_caps_v4", "rev_F8_warehouse_default", "rev_A2_priority_prior",
               "rev_A3_security_lag", "rev_A6_leverage_v4", "rev_A7_env_off", "rev_A8_no_means", "rev_A9_no_collusion",
               "rev_A11_no_escalation", "trend_breaks", "no_ai_rd_feedback", "no_self_replication", "skeptic_combo",
               "pessimist_combo", "single_decider", "coalition_floor_21", "no_war", "loop_off", "repression_deters",
               # audit round 3: F6 switch now wired, forced caps, B2 refill test
               "rev_F6_kit_uncapped", "f6_caps_forced", "f6_caps_forced_x100_qcore4", "b2_refill"]
    var_specs = {"BASE (variant size)": ("baseline", {})}
    for v in m8_vars[1:]:
        var_specs["m8: " + v] = (v, {})
    var_specs.update({
        "integrator: m8 path OFF, v2 S1 (v2-like broad path only)": ("baseline", dict(m8_on=False, s1_mode="v2", dfb_lo=0.85, dfb_hi=1.0)),
        "integrator: broad S4 path OFF (m8 only)": ("baseline", dict(broad_on=False)),
        "integrator: no D-dependence of analogs": ("baseline", dict(d_replace=False)),
        "integrator: capability latent not shared": ("baseline", dict(share_latent=False)),
        "integrator: background AI high (median 0.07)": ("baseline", dict(Pai_med=0.07)),
        "integrator: S1 requires D_full<0.2": ("baseline", dict(s1_D="0.2")),
        "integrator: B8 fix off (round-2 US history after broad-analog S5)": ("baseline", dict(b8_fix=False)),
        "integrator: cf_world off (round 3a: only the US columns taken from the US-autocratic counterfactual)": ("baseline", dict(cf_world=False)),
    })
    Dv = {}
    var_out = {}
    for vn, (mv, ch) in var_specs.items():
        if mv not in Dv:
            Dv[mv] = run_m8(NOv, R8v, mv, seed=SEED + 900)
        cfg = dict(B); cfg.update(ch)
        var_out[vn] = quick(cfg, Dv[mv])
        print("variant", vn, var_out[vn]["P(>=99.9% deliberate) US or China"], var_out[vn]["P(S5 deliberate >=10%) US or China"],
              round(time.time() - t0, 1)); sys.stdout.flush()
        if mv != "baseline":
            del Dv[mv]
    rng_vals = [v["P(>=99.9% deliberate) US or China"] for v in var_out.values()]
    var_out["m8: coalition_floor_21"]["_audit_note"] = ("inert under B2: p_small/nmin no longer set the coalition size (coalitions start at 21 "
                                                        "and shrink only through purges), so this variant equals BASE")

    # ---------- curves ----------
    v3res = load("integrated_v3.json")
    cv3 = v3res["cumulative_curves"]
    yrs = np.arange(2027, 2076)

    def cum(T):
        return [float(np.mean(T < y + 1)) for y in yrs]
    v4curve = dict(years=yrs.tolist(),
                   S5_deliberate_any=cum(R["S5_deliberate_any"]), S5_deliberate_US_or_China=cum(R["S5_deliberate_US_or_China"]),
                   S5_total_any=cum(R["S5_total_any"]),
                   near_total_deliberate_US_or_China=cum(R["loss>=0.999 deliberate US_or_China"]),
                   near_total_deliberate_any=cum(R["loss>=0.999 deliberate any"]),
                   S1=cum(R["S1"]), closure_any=cum(R["closure_any_bloc"]),
                   S5d_any_by_path={lab: cum(R["S5d any via " + lab]) for lab in
                                    ["broad_analog", "broad_S4_then_closure", "closure_after_S2_not_required", "closure_without_S2"]},
                   disempowered_by_bloc={ACT[a]: cum(X["tdis"][:, a]) for a in range(A_N)},
                   disempowered_pop_share=[float(popw(X["tdis"] < y + 1).mean()) for y in yrs],
                   world_loss_ge_99_9_all_blocs=r3curves["world_all_blocs_near_total"],
                   cross_bloc_campaign_any=r3curves["cross_bloc_campaign_any"],
                   single_decider_by_bloc=r3curves["single_decider_by_bloc"],
                   single_decider_US_or_China=r3curves["single_decider_US_or_China"])
    lo, hi = np.quantile(np.column_stack([per_draw(sim, R["S5_deliberate_any"] < y + 1) for y in yrs]), [0.1, 0.9], axis=0)
    v4curve["S5_deliberate_any_epistemic_p10"] = lo.tolist(); v4curve["S5_deliberate_any_epistemic_p90"] = hi.tolist()
    lo, hi = np.quantile(np.column_stack([per_draw(sim, R["loss>=0.999 deliberate US_or_China"] < y + 1) for y in yrs]), [0.1, 0.9], axis=0)
    v4curve["near_total_UC_epistemic_p10"] = lo.tolist(); v4curve["near_total_UC_epistemic_p90"] = hi.tolist()

    config_out = {k: (v if not isinstance(v, (list, tuple)) else [list(map(float, x)) for x in v]) for k, v in BASE_CFG.items()}
    res = {
        "model": "integrate_v4.py round 3 (v2 scenario tree + m8_v4 closure path with 6 blocs, F1-F8, A1-A11, B1-B9, A8 loss ladder)",
        "seed": SEED, "n_outer_draws": NO, "m8_replicates_per_draw": R8, "n_inner_paths": NI, "n_trajectories": NO * NI,
        "horizon": "2026.75 - end of 2075",
        "interval_semantics": "mc_ci95_bootstrap: bootstrap over outer (epistemic) draws of the mean, Monte Carlo precision only. epistemic_ci95: 2.5-97.5% quantiles of per-draw probabilities (each draw = 200 inner paths over 8 m8 aleatory replicates, so the raw range includes replicate noise). epistemic_ci95_denoised: after shrinking per-draw values toward the mean by sqrt(1 - noise/total variance), noise estimated from the replicate structure. Structural range: spread across variants.",
        "READ_FIRST": [
            "Every probability here is conditional on the binding assumptions A1-A11 agreed with the scenario and on m8_v4's judgment priors. The endgame (A8/A9/A11) parameters T_full, dL_means, h_use, f_eng, p_tot0, f0, k_esc, rem, k_col, b_col, c_self, s_bunk, p_nx, f_nx, w_col have no empirical anchor (evidence label J). Per A10 they are wide, not discounted.",
            "Given an executed designation, completion to >=99.9% is close to automatic in this model (A11 escalation plus no stopping rule other than a successful revolt). So P(>=99.9%) is essentially P(some coalition executes a depopulation order) times ~0.95: the near-total headline is driven by the elite game (moral cost vs revolt threat, refusal shares, decision rule), not by the endgame dials. The rev_A11_no_escalation variant shows the rung collapsing without A11.",
            "The round-2 model (all_round2 variant: every round-3 switch and prior reverted) gives a much lower execution rate. The difference comes mainly from the F2 refusal priors (literature: few absolute refusers in party and personalist elites) and the F1 regime rule (personalist leaders drawn toward the harsh tail of the coalition's preferences, oligarchies turning personalist as security automates), combined with A6 (democracy collapses as labor leverage goes). No single switch explains it; they interact.",
            "Standard (non-deliberate) channels, attrition and war, contribute little to the higher rungs; >=50% losses are nearly all deliberate.",
            "Round 3 (B1-B9): moral cost of those at the top anchored to autocrat selection (B1, judgment mapping of qualitative evidence), consolidation from purge incentives (B2), outside cost only if enforceable (B3), retribution fear growing with atrocities (B4), cross-bloc depopulation of blocs that cannot resist (B5), physical caps wired and bloc heterogeneity (B6), B8 US-history fix. Alt B unchanged (B9). The rev_B* variants revert one change at a time; round2_exact reproduces round 2.",
        ],
        "aggregates": aggs,
        "outcome_breakdown_US_or_China_2075": r3out["outcome_breakdown_US_or_China_2075"],
        "outcome_breakdown_US_bloc_2075": r3out["outcome_breakdown_US_bloc_2075"],
        "outcome_breakdown_China_bloc_2075": r3out["outcome_breakdown_China_bloc_2075"],
        "outcome_breakdown_by_bloc_2075": r3out["outcome_breakdown_by_bloc_2075"],
        "outcome_breakdown_world_population_weighted_2075": r3out["outcome_breakdown_world_population_weighted_2075"],
        "outcome_breakdown_semantics": r3out["outcome_breakdown_semantics"],
        "B5_cross_bloc": r3out["B5_cross_bloc"],
        "B2_consolidation": r3out["B2_consolidation"],
        "loss_ladder": ladder,
        "by_year": by_year,
        "S5_deliberate_first_channel_US_or_China": chan_UC,
        "S5_deliberate_first_channel_any_bloc": chan_any,
        "S5_total_first_channel_any_bloc": chan_tot,
        "by_bloc": by_bloc,
        "S5_paths": path_out,
        "end_states": es,
        "end_state_sum_check": float(sum(v["mean"] for v in es.values())),
        "structural_range_P(>=99.9% deliberate, US or China) across variants": [min(rng_vals), max(rng_vals)],
        "structural_variants (1000 draws x 8 m8 reps x 200 paths)": var_out,
        "stage_reached": stages,
        "conditional_diagnostics": cond,
        "sensitivity_P_near_total_US_or_China": sens,
        "sensitivity_P_S5_deliberate_US_or_China_top20": sens_s5,
        "sensitivity_P_US_or_China_stripped_of_rights_top15": sens_dis,
        "cumulative_curves": {"v2": cv3["v2"], "v3": cv3["v3"], "v4": v4curve},
        "curve_definitions": {"v2": "v2 integrate: lethal S5 (>=10%) any jurisdiction (US, China, RoW)",
                              "v3": "v3 integrate: lethal S5 any jurisdiction incl. m8-v3 closure path (total, v3 labeling)",
                              "v4": "v4: deliberate S5 (>=10%) any of 6 blocs; total S5; near-total (>=99.9%) deliberate"},
        "v3_to_v4_changes": [
            "m8_industrial_closure (v3) replaced by m8_v4: 6 blocs; endogenous grievance/insurgency loop and democracy; status-quo provision default (F8/A5); regime-dependent decision rule weighted by control over automated force (F1/A6); layered refusal with separate neglect refusal (F2); defection as a coercive-capacity threshold that autonomous systems remove (F3/A4); security automation tracking the capability/capacity frontier (A3); US/China priority max from 2026 (A2); trend capability with sampled acceleration (A1, F5 sign fix); A7 environment trends; endgame simulated as deaths with escalation (A11), abstract means (A8) and collusion game (A9).",
            "Channel labeling fixed (v3 line 392 relabeled attrition/war as neglect; line 390 read total t_S5 for the deliberate headline).",
            "US double counting removed: when the US broad S4 regime reaches closure and the US-autocratic counterfactual is used, the baseline US closure-path events are not also counted.",
            "Loss ladder >=10/50/90/99.9%, deliberate vs total; world population loss computed from bloc losses (population weights, UN WPP 2024 grouped: US 0.53, China 1.42, Europe+ 0.62, Russia/MENA 0.99, South Asia 1.97, Global South 2.67 bn).",
            "Disempowerment reported two ways: stripped of rights (harsh choice incl. rentier, captive remnant, S5, broad S4 persisting, US grab), and incl. autocratic rule at 2075 (A6: democracy collapses as leverage disappears).",
        ],
        "notes": [
            "End-state precedence: S7 > S6->misaligned > S6 > S5 deliberate near-total > S5 deliberate partial (active/collusive) > S5 deliberate partial (neglect) > S5 non-deliberate only > S5b > AI takeover > non-AI catastrophe > held without rights > broad S4 persisting > US grab persisting > Alt B > Alt A > other > S2 accommodated > closure served/status quo > S1 only > no race.",
            "S5 = >=10% of a bloc's 2026 population lost (gross simulated excess loss). The broad-path analogs (human-staffed regimes) reach only the >=10% rung.",
            "Background AI takeover and non-AI catastrophe censor later events (competing absorbing states), as in v2/v3.",
            "The captive remnant (0.03-0.1% of a bloc) is counted as disempowered, not as survivors with standing (A11).",
            "Timewave Zero is not used.",
        ],
        "config": config_out,
        "audit_round3": [
            "f6_kitcap was defined but never read; now wired (kit cap needs b6_wire and f6_kitcap). Variant rev_F6_kit_uncapped is no longer inert.",
            "Guard added: a B2 coalition emptied by the ouster of its only member is replaced by a new 21-member coalition (an empty coalition made the weighted rule pick depopulation). It never fired in the baseline (checked at N=20000), so baseline numbers are unchanged.",
            "B2 purged seats are not refilled; variant b2_refill and the leader-control>=95% measure show that the coalition-of-one share is largely an artifact while the headline is not.",
            "B6: forced caps bind (robot output at 2035 falls 4-9x with pools/100) but move the leaders' closure little because the minimal core loop is small (q_core median 0.15); with q_core x4 the same caps delay US/China closure by ~6/13 years and cut the headline (variant f6_caps_forced_x100_qcore4). At baseline magnitudes the physical input pools do not bind closure (rev_F6_kit_uncapped and rev_B6_caps_bypassed ~ BASE).",
            "US and China closure dates remain almost perfectly correlated (A2 priority for both, shared frontier capability, lags <= 1 y, non-binding inputs); B6 heterogeneity mainly separates the other blocs.",
            "The remnant draw rem is up to 0.1%, equal to the 99.9% rung, so executions with rem near 0.001 reach the rung slightly later or not at all (P(rung | near-total designation) 0.954 at rem 0.03-0.06% vs 0.943 at 0.09-0.1%).",
        ],
    }
    res["runtime_s"] = round(time.time() - t0, 1)
    global FIG
    outp = os.path.join(RES, "integrated_v4.json")
    if os.environ.get("INT_OUT"):            # brake runs: new output file and figure folder (never the published ones)
        outp = os.path.join(RES, os.environ["INT_OUT"]); FIG = os.environ.get("INT_FIG", os.path.join(ROOT, "figures", "brakes_v5"))
        os.makedirs(FIG, exist_ok=True)
        assert not os.path.exists(outp), outp + " exists"
        res["brakes"] = dict(M8_BRAKES=os.environ.get("M8_BRAKES", ""), diagnostics_m8_world=D8["brk_diag"],
                             note="all brake flags on in every run of this file, incl. structural variants (M8_BRAKES=final)")
    if small:
        outp = os.path.join(os.environ["INT_SMALL_DIR"], "integrated_v4_smoke.json"); FIG = os.environ["INT_SMALL_DIR"]
    with open(outp, "w") as f:
        json.dump(res, f, indent=1, default=float)
    make_figures(res)
    print(json.dumps({"aggs": {k: (v.get("mean"), v.get("epistemic_ci95_denoised")) if isinstance(v, dict) else v for k, v in aggs.items()},
                      "ladder": {k: {nm: (v[nm]["US_or_China"]["mean"], v[nm]["any_bloc"]["mean"], v[nm]["world_pop_share_expected"]) for nm in ["deliberate", "total"]} | {"world": v["world_population_loss_at_least_this"]["mean"]} for k, v in ladder.items()},
                      "paths": {t: {k: (v["P"]["mean"], v["share_of_S5"], v["median_year"]) for k, v in po.items()} for t, po in path_out.items() if not t.startswith("_")},
                      "chan_UC": chan_UC, "chan_any": chan_any, "chan_tot": chan_tot, "by_bloc": by_bloc, "cond": cond,
                      "by_year": by_year, "es": {k: v["mean"] for k, v in es.items()},
                      "sens_top": [(s["param"], s["p_low_tercile"], s["p_high_tercile"], s["partial_rank_corr"]) for s in sens[:15]],
                      "breakdown_UC": {k: (v["mean"], v["epistemic_ci95_denoised"]) for k, v in r3out["outcome_breakdown_US_or_China_2075"].items() if not k.startswith("_")},
                      "r3": {k: v for k, v in r3out.items() if not k.startswith("outcome_breakdown_US")},
                      "variants": var_out, "runtime": res["runtime_s"]}, indent=1, default=str))


def make_figures(res):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    os.makedirs(FIG, exist_ok=True)
    ink, muted, grid = "#0b0b0b", "#52514e", "#e4e3df"
    c = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948"]
    plt.rcParams.update({"font.size": 9, "axes.edgecolor": muted, "axes.labelcolor": muted, "xtick.color": muted,
                         "ytick.color": muted, "axes.titlecolor": ink, "lines.linewidth": 2})

    def style(ax):
        ax.spines[["top", "right"]].set_visible(False); ax.grid(color=grid, lw=0.6); ax.set_axisbelow(True)
    cv = res["cumulative_curves"]; v4 = cv["v4"]; yrs = np.array(v4["years"])
    # 1. cumulative P(S5): v2 vs v3 vs v4
    fig, ax = plt.subplots(figsize=(10, 5.8))
    ax.fill_between(yrs, v4["S5_deliberate_any_epistemic_p10"], v4["S5_deliberate_any_epistemic_p90"], color=c[7], alpha=0.12, lw=0,
                    label="v4 deliberate S5, any bloc: epistemic p10-p90 (per draw)")
    ax.plot(yrs, cv["v2"]["S5"], color=c[0], ls="--", label="v2: lethal S5 (>=10%), any jurisdiction")
    ax.plot(yrs, cv["v3"]["S5"], color=c[6], ls="-.", label="v3: lethal S5 (>=10%), any jurisdiction")
    ax.plot(yrs, v4["S5_deliberate_any"], color=c[7], label="v4: deliberate S5 (>=10%), any of 6 blocs")
    ax.plot(yrs, v4["S5_total_any"], color=c[1], lw=1.2, label="v4: total S5 incl. attrition and war, any bloc")
    ax.plot(yrs, v4["S5_deliberate_US_or_China"], color=c[3], label="v4: deliberate S5, US or China bloc")
    ax.plot(yrs, v4["near_total_deliberate_US_or_China"], color=ink, lw=2.2, label="v4 HEADLINE: >=99.9% deliberate loss, US or China")
    ax.plot(yrs, v4["near_total_deliberate_any"], color=ink, lw=1.2, ls=":", label="v4: >=99.9% deliberate loss, any bloc")
    for y in [2035, 2040, 2050, 2075]:
        v = v4["near_total_deliberate_US_or_China"][y - 2027]
        ax.annotate(f"{v:.3f}", (y, v), textcoords="offset points", xytext=(-12, -14), fontsize=8, color=ink)
    ax.set_xlim(2027, 2075); ax.set_ylim(0, 1); ax.set_xlabel("year"); ax.set_ylabel("cumulative probability")
    ax.set_title("Cumulative P(S5): v2 vs v3 vs v4 (v4 conditional on A1-A11 and m8_v4 priors)", loc="left")
    ax.legend(frameon=False, fontsize=8, loc="upper left"); style(ax)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "integrated_v4_cumulative_v2_v3_v4.png"), dpi=150); plt.close(fig)
    # 2. path decomposition + ladder
    fig, axs = plt.subplots(1, 2, figsize=(14, 5.8), gridspec_kw=dict(width_ratios=[1.8, 1]))
    labs = ["closure_without_S2", "closure_after_S2_not_required", "broad_S4_then_closure", "broad_analog"]
    nice = {"closure_without_S2": "single-bloc closure, before S2", "closure_after_S2_not_required": "single-bloc closure, S2 present (not required)",
            "broad_S4_then_closure": "broad path: S4 regime then closes loop", "broad_analog": "broad path: human-staffed analog (v2 mechanism)"}
    ys = np.array([v4["S5d_any_by_path"][l] for l in labs])
    axs[0].stackplot(yrs, ys, labels=[nice[l] for l in labs], colors=[c[7], c[1], c[3], c[0]], alpha=0.9)
    axs[0].set_xlim(2027, 2075); axs[0].set_xlabel("year"); axs[0].set_ylabel("P(deliberate S5 by year), stacked by first path")
    axs[0].set_title("v4 deliberate S5 (any bloc) by path", loc="left"); axs[0].legend(frameon=False, fontsize=8, loc="upper left"); style(axs[0])
    lad = res["loss_ladder"]; ks = list(lad.keys()); x = np.arange(len(ks)); w = 0.2
    series = [("deliberate", "US_or_China", c[3], "deliberate, US or China"), ("total", "US_or_China", c[1], "total, US or China"),
              ("deliberate", "any_bloc", c[7], "deliberate, any bloc"), ("total", "any_bloc", "#f4a3a3", "total, any bloc")]
    for i, (nm, sc, col, lb) in enumerate(series):
        vals = [lad[k][nm][sc]["mean"] for k in ks]
        axs[1].bar(x + (i - 1.5) * w, vals, w, color=col, label=lb)
    wv = [lad[k]["world_population_loss_at_least_this"]["mean"] for k in ks]
    axs[1].plot(x, wv, "o-", color=ink, lw=1.2, label="world population loss (all blocs)")
    for xi, v in zip(x, wv):
        axs[1].annotate(f"{v:.3f}", (xi, v), textcoords="offset points", xytext=(4, 4), fontsize=7.5)
    axs[1].set_xticks(x); axs[1].set_xticklabels([f"loss {k}" for k in ks]); axs[1].set_ylim(0, 1)
    axs[1].set_ylabel("P by 2075"); axs[1].set_title("Loss ladder (A8): deliberate vs total", loc="left")
    axs[1].legend(frameon=False, fontsize=7.5); style(axs[1])
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "integrated_v4_paths.png"), dpi=150); plt.close(fig)
    # 3. disempowerment
    fig, axs = plt.subplots(1, 2, figsize=(13, 5.2))
    for a, an in enumerate(ACT):
        axs[0].plot(yrs, v4["disempowered_by_bloc"][an], color=c[a], label=an)
    axs[0].plot(yrs, v4["disempowered_pop_share"], color=ink, lw=2.4, ls="--", label="expected world population share")
    axs[0].set_xlim(2027, 2075); axs[0].set_ylim(0, 1); axs[0].set_ylabel("cumulative probability / share")
    axs[0].set_title("First disempowerment: breakdown/seizure, harsh decision, S5 or captivity", loc="left")
    axs[0].legend(frameon=False, fontsize=8); style(axs[0])
    bb = res["by_bloc"]; x = np.arange(A_N)
    for i, (k, col, lb) in enumerate([("stripped_of_rights", c[1], "stripped of rights (harsh choice, S5, captive, S4)"),
                                      ("disempowered_incl_autocratic", c[0], "incl. autocratic rule at 2075"),
                                      ("near_total_deliberate", ink, ">=99.9% deliberate loss (captive remnant)")]):
        axs[1].bar(x + (i - 1) * 0.27, [bb[a][k] for a in ACT], 0.27, color=col, label=lb)
    axs[1].set_xticks(x); axs[1].set_xticklabels([a.replace("_", "\n") for a in ACT], fontsize=8); axs[1].set_ylim(0, 1)
    axs[1].set_ylabel("P at 2075"); axs[1].set_title("Public disempowerment by bloc, 2075", loc="left")
    axs[1].legend(frameon=False, fontsize=7.5); style(axs[1])
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "integrated_v4_disempowerment.png"), dpi=150); plt.close(fig)
    # 4. tornado
    sens = res["sensitivity_P_near_total_US_or_China"][:20][::-1]
    base = res["aggregates"]["HEADLINE P(>=99.9% deliberate depopulation of the US or China bloc by 2075)"]["mean"]
    fig, ax = plt.subplots(figsize=(11, 7.5))
    for i, s in enumerate(sens):
        ax.barh(i, s["p_high_tercile"] - base, left=base, color=c[1], height=0.7)
        ax.barh(i, s["p_low_tercile"] - base, left=base, color=c[0], height=0.7)
    ax.axvline(base, color=ink, lw=1)
    ax.set_yticks(range(len(sens)))
    ax.set_yticklabels([f"{s['param']}  (PRCC {s['partial_rank_corr']:+.2f})" for s in sens], fontsize=8)
    ax.set_xlabel("P(>=99.9% deliberate loss, US or China, by 2075): bottom (blue) vs top (orange) tercile of the epistemic draw")
    ax.set_title("v4 global sensitivity of the headline (per-draw, 3000 epistemic draws)", loc="left"); style(ax)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "integrated_v4_tornado.png"), dpi=150); plt.close(fig)
    # 5. mutually exclusive outcome breakdown (round 3)
    cats = [k for k, _ in OUTCOME_CATS]
    nice5 = {"near_total_deliberate": ">=99.9% deliberate (near-total)", "partial_deliberate": "partial deliberate (10-99.9%)",
             "non_deliberate_mass_death": "non-deliberate mass death (>=10%)", "background_absorbing_event": "background AI takeover / catastrophe",
             "stripped_of_rights_no_mass_death": "stripped of rights, no mass death", "autocratic_short_of_that": "autocratic, short of that",
             "public_keeps_standing": "public keeps standing (incl. Alt B baseline)"}
    cols5 = [ink, c[7], c[1], muted, c[3], c[0], c[2]]
    rows = [("US or China", {k: res["outcome_breakdown_US_or_China_2075"][k]["mean"] for k in cats}),
            ("US bloc", {k: res["outcome_breakdown_US_bloc_2075"][k]["mean"] for k in cats}),
            ("China bloc", {k: res["outcome_breakdown_China_bloc_2075"][k]["mean"] for k in cats})]
    rows += [(a.replace("_", " "), res["outcome_breakdown_by_bloc_2075"][a]) for a in ACT[2:]]
    rows += [("world population (weighted)",res["outcome_breakdown_world_population_weighted_2075"])]
    fig, ax = plt.subplots(figsize=(12, 5.6))
    for r, (lab, d) in enumerate(rows):
        left = 0.0
        for k, col in zip(cats, cols5):
            v = d[k]
            ax.barh(r, v, left=left, color=col, height=0.66, edgecolor="white", linewidth=1.5, label=nice5[k] if r == 0 else None)
            if v >= 0.05:
                ax.text(left + v / 2, r, f"{v:.2f}", ha="center", va="center", fontsize=7.5, color="white" if col in (ink, c[7], muted, c[0]) else ink)
            left += v
    ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows]); ax.invert_yaxis(); ax.set_xlim(0, 1)
    ax.set_xlabel("share of trajectories at 2075 (mutually exclusive, worst class first; sums to 1)")
    ax.set_title("Round 3: outcome breakdown at 2075 (conditional on A1-A11 and m8_v4 priors)", loc="left")
    ax.legend(frameon=False, fontsize=7.5, ncol=4, loc="upper center", bbox_to_anchor=(0.5, -0.13)); style(ax)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "integrated_v4_outcome_breakdown.png"), dpi=150); plt.close(fig)
    # 6. B5 who depopulates whom + world curve + B2 consolidation curves
    b5 = res["B5_cross_bloc"]; M = np.array([[b5["who_depopulates_whom P(aggressor row attacks target column)"][a][t] for t in ACT] for a in ACT])
    fig, axs = plt.subplots(1, 3, figsize=(17, 5.4), gridspec_kw=dict(width_ratios=[1.1, 1, 1]))
    im = axs[0].imshow(M, cmap="Oranges", vmin=0, vmax=max(M.max(), 1e-3))
    for i in range(A_N):
        for k in range(A_N):
            if i != k:
                axs[0].text(k, i, f"{M[i, k]:.3f}", ha="center", va="center", fontsize=7.5, color=ink if M[i, k] < 0.6 * M.max() else "white")
    short = [a.replace("_bloc", "").replace("_", " ") for a in ACT]
    axs[0].set_xticks(range(A_N)); axs[0].set_xticklabels(short, fontsize=7.5); axs[0].set_yticks(range(A_N)); axs[0].set_yticklabels(short, fontsize=7.5)
    axs[0].set_xlabel("target bloc"); axs[0].set_ylabel("aggressor bloc"); axs[0].set_title("B5: P(aggressor attacks target by 2075)", loc="left")
    fig.colorbar(im, ax=axs[0], fraction=0.046, pad=0.04)
    v4 = res["cumulative_curves"]["v4"]
    axs[1].plot(yrs, v4["near_total_deliberate_US_or_China"], color=ink, label=">=99.9% deliberate, US or China (headline)")
    axs[1].plot(yrs, v4["near_total_deliberate_any"], color=c[7], label=">=99.9% deliberate, any bloc")
    axs[1].plot(yrs, v4["cross_bloc_campaign_any"], color=c[1], label="a cross-bloc campaign has started")
    axs[1].plot(yrs, v4["world_loss_ge_99_9_all_blocs"], color=c[6], lw=2.4, label="every bloc >=99.9% (world near-total)")
    axs[1].set_xlim(2027, 2075); axs[1].set_ylim(0, 1); axs[1].set_ylabel("cumulative probability")
    axs[1].set_title("World-level depopulation (B5)", loc="left"); axs[1].legend(frameon=False, fontsize=7.5, loc="upper left"); style(axs[1])
    for a, an in enumerate(ACT):
        axs[2].plot(yrs, v4["single_decider_by_bloc"][an], color=c[a], lw=1.5, label=an)
    axs[2].plot(yrs, v4["single_decider_US_or_China"], color=ink, lw=2.2, ls="--", label="US or China")
    axs[2].set_xlim(2027, 2075); axs[2].set_ylim(0, 1); axs[2].set_ylabel("cumulative probability")
    axs[2].set_title("B2: coalition consolidated to a single decider", loc="left"); axs[2].legend(frameon=False, fontsize=7.5, loc="upper left"); style(axs[2])
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "integrated_v4_b5_b2.png"), dpi=150); plt.close(fig)


if __name__ == "__main__":
    main()
