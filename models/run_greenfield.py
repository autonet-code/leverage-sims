"""Matched comparison, brakes on in every arm: brakes only; + greenfield core loop (gf_on); + own-industry compute
feedback (cf_on); + wide automated doubling floors (wfl_on) = the final configuration.
Design as run_brakes.stage_variants / integrate_v4's structural-variants block: 1000 outer draws x 8 m8 replicates x
200 inner paths; m8 seed SEED+900, integrator seed SEED+11. All arms share every existing draw and inner random number.
Changes are paired (bootstrap over outer draws, 95% CI). Run with M8_BRAKES=final; arms are m8 variants baseline,
greenfield, greenfield_cf and greenfield_cf_wfl (the final configuration: + wide automated doubling floors).
Output: results/greenfield_v6_matched.json (refuses to overwrite).
"""
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import integrate_v4 as I  # noqa: E402
import run_brakes as RB  # noqa: E402
M8 = I.M8
import torch  # noqa: E402


def log(*a):
    print(*a); sys.stdout.flush()


def metrics(sv):
    m = RB.metrics(sv)
    R = sv["R"]
    m["P(closure: some bloc core chain <20% human) by 2035"] = R["closure_any_bloc"] < 2036
    m["P(closure: some bloc core chain <20% human) by 2040"] = R["closure_any_bloc"] < 2041
    m["P(S5 deliberate >=10%) any bloc, 2075"] = I.headline(sv)["s5d_any"]
    return m


def main():
    outp = os.path.join(I.RES, "greenfield_v6_matched.json")
    assert not os.path.exists(outp), outp + " exists; not overwriting"
    assert os.environ.get("M8_BRAKES", "") == "final" and all(os.environ.get(k, "") in ("", "0") for k in ("M8_FINAL", "M8_GF", "M8_CF", "M8_WFL")),         "run with M8_BRAKES=final only (greenfield and compute feedback are switched by variant)"
    assert torch.cuda.is_available() and os.environ.get("M8_CPU") != "1", "GPU required"
    log("torch", torch.__version__, "device", M8.pick_device(), torch.cuda.get_device_name(0))
    t0 = time.time()
    NO, R8, NI = 1000, 8, 200
    arms = {"brakes_only": "baseline", "brakes_greenfield": "greenfield", "brakes_greenfield_computefb": "greenfield_cf",
            "final_brakes_greenfield_computefb_widefloors": "greenfield_cf_wfl"}
    sims, mets, diag, ldiag, tcl = {}, {}, {}, {}, {}
    for arm, v in arms.items():
        D = I.run_m8(NO, R8, v, seed=I.SEED + 900)
        diag[arm] = D["gf_diag"]; ldiag[arm] = D["leader_diag"]
        tcl[arm] = D["tc"]                     # per-bloc closure clock (D_core < 0.2) of the m8 main world, NO*R8 rows
        sv = I.simulate(I.BASE_CFG, D, NI, I.SEED + 11)
        sims[arm] = sv; mets[arm] = metrics(sv)
        log("arm", arm, {k: round(float(np.mean(x)), 4) for k, x in mets[arm].items()}, round(time.time() - t0, 1), "s")
        del D
    res = {"design": f"{NO} outer draws x {R8} m8 replicates x {NI} inner paths; m8 seed SEED+900, integrator seed SEED+11; "
                     "brakes on in every arm (M8_BRAKES=final). Arms: brakes only (m8 variant baseline), brakes + greenfield "
                     "(variant greenfield, gf_on), + own-industry compute feedback (variant greenfield_cf), + wide automated doubling "
                     "floors = final configuration (variant greenfield_cf_wfl). "
                     "gf_on adds no draws; the compute-feedback priors come from their own stream, so all arms share every "
                     "existing draw. Changes are paired over outer draws (bootstrap, 2000 resamples).",
           "seed": I.SEED, "device": str(M8.pick_device()), "spec_greenfield": M8.GF_NOTE, "spec_compute_feedback": M8.CF_NOTE,
           "spec_wide_floors": M8.wfl_table()}
    res["headline_by_arm"] = {arm: {k: I.stats(sims[arm], x)[0] for k, x in mets[arm].items()} for arm in arms}
    res["paired_change"] = {
        "greenfield_vs_brakes_only": RB.paired(sims["brakes_only"], sims["brakes_greenfield"], mets["brakes_only"], mets["brakes_greenfield"]),
        "greenfield_computefb_vs_brakes_only": RB.paired(sims["brakes_only"], sims["brakes_greenfield_computefb"], mets["brakes_only"], mets["brakes_greenfield_computefb"]),
        "computefb_increment_vs_greenfield": RB.paired(sims["brakes_greenfield"], sims["brakes_greenfield_computefb"], mets["brakes_greenfield"], mets["brakes_greenfield_computefb"]),
        "final_vs_brakes_only": RB.paired(sims["brakes_only"], sims["final_brakes_greenfield_computefb_widefloors"], mets["brakes_only"], mets["final_brakes_greenfield_computefb_widefloors"]),
        "widefloors_increment_vs_greenfield_computefb": RB.paired(sims["brakes_greenfield_computefb"], sims["final_brakes_greenfield_computefb_widefloors"], mets["brakes_greenfield_computefb"], mets["final_brakes_greenfield_computefb_widefloors"])}
    ct = {}
    a = tcl["brakes_only"]
    for arm in arms:
        b = tcl[arm]; ct[arm] = {}
        for tag, cols in [("first_closer_any_bloc", list(range(a.shape[1]))), ("US_or_China", [0, 1]), ("US_bloc", [0]), ("China_bloc", [1])]:
            ta, tb = a[:, cols].min(1), b[:, cols].min(1)
            both = np.isfinite(ta) & np.isfinite(tb)
            d = tb[both] - ta[both]
            fin = tb[np.isfinite(tb)]
            ct[arm][tag] = dict(median_year=round(float(np.median(fin)), 2), p10_p90=[round(float(np.percentile(fin, q)), 2) for q in (10, 90)],
                                P_by={str(y): round(float((tb < y + 1).mean()), 4) for y in (2030, 2035, 2040, 2050)},
                                paired_shift_vs_brakes_only_years=dict(median=round(float(np.median(d)), 2), mean=round(float(d.mean()), 3),
                                                                       p10=round(float(np.percentile(d, 10)), 2), p90=round(float(np.percentile(d, 90)), 2)))
    res["closure_timing_m8_world"] = ct
    res["greenfield_diagnostics_m8_world"] = diag
    res["leaders_and_compute_feedback_diagnostics_m8_world"] = ldiag
    res["runtime_s"] = round(time.time() - t0, 1)
    with open(outp, "w") as f:
        json.dump(res, f, indent=1, default=float)
    log(json.dumps(res["paired_change"], indent=1)); log(json.dumps(ct, indent=1))


if __name__ == "__main__":
    main()
