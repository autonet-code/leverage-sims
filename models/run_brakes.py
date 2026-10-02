"""Brake runs (paper/brake_search_protocol.md). Uses integrate_v4's pipeline unchanged:
  stage 'variants': each brake alone, all three together (plus the brake-1 sel_top sensitivity), 1000 outer draws x 8 m8
                    replicates x 200 inner paths, matched baseline at the same seeds (SEED+900 m8, SEED+11 integrator),
                    as in integrate_v4's structural-variants block. Paired bootstrap over outer draws for the change.
  stage 'main':     3000 x 8 x 200 at the main-run seeds (SEED+800 m8, SEED integrator): baseline (reproduction check,
                    must give 0.44656 / 0.13853) and all three brakes on (brake-inclusive headline).
Outputs: results/brakes_variants.json, results/brakes_main.json (never overwrites; refuses if they exist).
"""
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import integrate_v4 as I  # noqa: E402
M8 = I.M8
import torch  # noqa: E402

RES = I.RES
SEED = I.SEED


def metrics(sv):
    h = I.headline(sv); R = sv["R"]
    return {
        "P(>=99.9% deliberate) US or China, 2075": h["nt_UC"],
        "P(>=99.9% deliberate) any bloc, 2075": h["nt_any"],
        "P(world population loss >=99.9%), 2075": h["nt_world"],
        "P(S5 deliberate >=10%) US or China, 2075": h["s5d_UC"],
        "P(S5 deliberate >=10%) any bloc, 2075": h["s5d_any"],
        "P(>=99.9% deliberate) US or China, by 2050": R["loss>=0.999 deliberate US_or_China"] < 2051,
        "P(S5 deliberate >=10%) US or China, by 2050": R["S5_deliberate_US_or_China"] < 2051,
        "P(US or China public stripped of rights, 2075)": h["disemp_UC"],
    }


def paired(sv_b, sv_v, mb, mv, B=2000, seed=5):
    rng = np.random.default_rng(seed)
    out = {}
    NO = sv_b["NO"]
    idx = rng.integers(0, NO, (B, NO))
    for k in mb:
        pb = I.per_draw(sv_b, mb[k]); pv = I.per_draw(sv_v, mv[k])
        d = pv - pb
        bm = d[idx].mean(1)
        out[k] = dict(variant=round(float(pv.mean()), 5), matched_baseline=round(float(pb.mean()), 5),
                      change=round(float(d.mean()), 5),
                      change_paired_bootstrap_ci95=[round(float(np.quantile(bm, .025)), 5), round(float(np.quantile(bm, .975)), 5)],
                      relative_change=round(float(d.mean() / pb.mean()), 4) if pb.mean() > 0 else None)
    return out


def log(*a):
    print(*a); sys.stdout.flush()


def stage_variants():
    outp = os.path.join(RES, "brakes_variants.json")
    assert not os.path.exists(outp), outp + " exists; not overwriting"
    t0 = time.time()
    NO, R8, NI = 1000, 8, 200
    vars_ = ["baseline", "brake_pid", "brake_selfrisk", "brake_mort", "brakes_all", "brake_pid_noselm"]
    sims = {}; mets = {}; diags = {}
    for v in vars_:
        D = I.run_m8(NO, R8, v, seed=SEED + 900)
        diags[v] = D["brk_diag"]
        sv = I.simulate(I.BASE_CFG, D, NI, SEED + 11)
        sims[v] = sv; mets[v] = metrics(sv)
        log("variant", v, {k: round(float(np.mean(x)), 4) for k, x in mets[v].items()}, round(time.time() - t0, 1), "s")
        del D
    res = {"design": f"{NO} outer draws x {R8} m8 replicates x {NI} inner paths; m8 seed SEED+900, integrator seed SEED+11 "
                     "(integrate_v4 structural-variants setup). Every variant shares the baseline's outer draws and inner "
                     "random numbers; brake parameters come from a separate stream. Change = variant - matched baseline; "
                     "95% CI from a paired bootstrap over outer draws (2000 resamples).",
           "seed": SEED, "device": str(M8.pick_device()), "results": {}, "diagnostics_m8_world": diags}
    for v in vars_[1:]:
        res["results"][v] = paired(sims["baseline"], sims[v], mets["baseline"], mets[v])
    res["results"]["baseline"] = {k: round(float(np.mean(x)), 5) for k, x in mets["baseline"].items()}
    res["quick_check_vs_integrate_v4_BASE_variant_size"] = {
        "integrated_v4.json BASE (variant size) P(>=99.9%) US or China": 0.4473,
        "this run": res["results"]["baseline"]["P(>=99.9% deliberate) US or China, 2075"]}
    res["runtime_s"] = round(time.time() - t0, 1)
    with open(outp, "w") as f:
        json.dump(res, f, indent=1, default=float)
    log(json.dumps(res["results"], indent=1))
    log(json.dumps(diags, indent=1))


def stage_main():
    outp = os.path.join(RES, "brakes_main.json")
    assert not os.path.exists(outp), outp + " exists; not overwriting"
    t0 = time.time()
    NO, R8, NI = 3000, 8, 200
    out = {"design": f"{NO} x {R8} x {NI}, main-run seeds (m8 SEED+800, integrator SEED), as integrate_v4.main()",
           "device": str(M8.pick_device())}
    sims = {}; mets = {}
    for v in ["baseline", "brakes_all"]:
        D = I.run_m8(NO, R8, v)
        sv = I.simulate(I.BASE_CFG, D, NI, SEED)
        sims[v] = sv; mets[v] = metrics(sv)
        st = {k: I.stats(sv, x)[0] for k, x in mets[v].items()}
        out[v] = {"headline": st, "diagnostics_m8_world": D["brk_diag"]}
        if v == "brakes_all":
            pd_nt = I.per_draw(sv, mets[v]["P(>=99.9% deliberate) US or China, 2075"])
            sens = I.sensitivity(sv, pd_nt)
            out[v]["sensitivity_P_near_total_US_or_China_brake_params"] = [s for s in sens if s["param"].replace("m8: ", "") in I.BRK_KEYS]
            out[v]["sensitivity_rank_of_brake_params_among_all"] = {s["param"]: i + 1 for i, s in enumerate(sens) if s["param"].replace("m8: ", "") in I.BRK_KEYS}
        log("main", v, {k: s["mean"] for k, s in st.items()}, round(time.time() - t0, 1), "s")
        del D
    b = out["baseline"]["headline"]
    out["reproduction_check"] = {
        "expected P(>=99.9% deliberate) US or China": 0.44656, "got": b["P(>=99.9% deliberate) US or China, 2075"]["mean"],
        "expected P(world loss >=99.9%)": 0.13853, "got_world": b["P(world population loss >=99.9%), 2075"]["mean"],
        "identical": bool(b["P(>=99.9% deliberate) US or China, 2075"]["mean"] == 0.44656
                          and b["P(world population loss >=99.9%), 2075"]["mean"] == 0.13853)}
    out["brakes_all_vs_baseline_paired"] = paired(sims["baseline"], sims["brakes_all"], mets["baseline"], mets["brakes_all"])
    out["runtime_s"] = round(time.time() - t0, 1)
    with open(outp, "w") as f:
        json.dump(out, f, indent=1, default=float)
    log(json.dumps({k: v for k, v in out.items() if k in ("reproduction_check", "brakes_all_vs_baseline_paired")}, indent=1))
    log(json.dumps(out["brakes_all"].get("sensitivity_P_near_total_US_or_China_brake_params"), indent=1))


def stage_variants2():
    """follow-up round: revised self-risk, dissent risk, fixed mortality, final configuration"""
    outp = os.path.join(RES, "brakes_v5_variants.json")
    assert not os.path.exists(outp), outp + " exists; not overwriting"
    assert os.environ.get("M8_BRAKES", "") in ("", "off"), "variants are defined by name; unset M8_BRAKES"
    t0 = time.time()
    NO, R8, NI = 1000, 8, 200
    vars_ = ["baseline", "brake_pid", "brake_selfrisk", "brake_selfrisk_dis", "brake_mort", "brakes_final"]
    sims = {}; mets = {}; diags = {}
    for v in vars_:
        D = I.run_m8(NO, R8, v, seed=SEED + 900)
        diags[v] = D["brk_diag"]
        sv = I.simulate(I.BASE_CFG, D, NI, SEED + 11)
        sims[v] = sv; mets[v] = metrics(sv)
        log("variant", v, {k: round(float(np.mean(x)), 4) for k, x in mets[v].items()}, round(time.time() - t0, 1), "s")
        del D
    res = {"design": f"{NO} outer draws x {R8} m8 replicates x {NI} inner paths; m8 seed SEED+900, integrator seed SEED+11 "
                     "(integrate_v4 structural-variants setup), matched baseline on the same draws and random numbers. "
                     "Change = variant - matched baseline; 95% CI from a paired bootstrap over outer draws (2000 resamples).",
           "variants": {"brake_pid": "Brake 1 protective doctrine (unchanged from round 1)",
                        "brake_selfrisk": "Brake 2 revised (c_selfrisk ln(1.0,1.5), e_ex U(0.25,0.6), ideology exemption b_id), no dissent risk",
                        "brake_selfrisk_dis": "Brake 2 revised plus dissent risk (m_dis)",
                        "brake_mort": "Brake 3 leader mortality, fixed hazard (set at closure, declining with k_le, age term reset at succession)",
                        "brakes_final": "final configuration: all four on (pid_on, sr_on, dis_on, brk_mort)"},
           "seed": SEED, "device": str(M8.pick_device()), "results": {}, "diagnostics_m8_world": diags}
    for v in vars_[1:]:
        res["results"][v] = paired(sims["baseline"], sims[v], mets["baseline"], mets[v])
    res["results"]["baseline"] = {k: round(float(np.mean(x)), 5) for k, x in mets["baseline"].items()}
    # how much dissent risk offsets self-risk: (selfrisk+dissent) - (selfrisk alone), paired, and offset share
    rng = np.random.default_rng(9); idx = rng.integers(0, NO, (2000, NO)); off = {}
    for k in mets["baseline"]:
        pb = I.per_draw(sims["baseline"], mets["baseline"][k]); ps = I.per_draw(sims["brake_selfrisk"], mets["brake_selfrisk"][k])
        pd_ = I.per_draw(sims["brake_selfrisk_dis"], mets["brake_selfrisk_dis"][k])
        ds, dd = ps - pb, pd_ - pb
        bs, bd = ds[idx].mean(1), dd[idx].mean(1)
        sh = 1 - bd / np.where(bs != 0, bs, np.nan)
        off[k] = dict(selfrisk_change=round(float(ds.mean()), 5), selfrisk_plus_dissent_change=round(float(dd.mean()), 5),
                      dissent_effect=round(float((pd_ - ps).mean()), 5),
                      dissent_effect_ci95=[round(float(np.quantile((pd_ - ps)[idx].mean(1), q)), 5) for q in (.025, .975)],
                      share_of_selfrisk_effect_offset=round(float(1 - dd.mean() / ds.mean()), 4) if ds.mean() != 0 else None,
                      share_offset_ci95=[round(float(np.nanquantile(sh, q)), 4) for q in (.025, .975)])
    res["dissent_offset_of_selfrisk"] = off
    res["runtime_s"] = round(time.time() - t0, 1)
    with open(outp, "w") as f:
        json.dump(res, f, indent=1, default=float)
    log(json.dumps(res["results"], indent=1)); log(json.dumps(off, indent=1)); log(json.dumps(diags, indent=1))


if __name__ == "__main__":
    log("torch", torch.__version__, "cuda available:", torch.cuda.is_available(),
        "device:", M8.pick_device(), torch.cuda.get_device_name(0) if torch.cuda.is_available() else "")
    assert torch.cuda.is_available() and os.environ.get("M8_CPU") != "1", "GPU required"
    for st in sys.argv[1:]:
        {"variants": stage_variants, "main": stage_main, "variants2": stage_variants2}[st]()
