"""Identity checks for the greenfield core-loop change (gf_on).
1. m8_v4.py (greenfield code, gf off) vs m8_v4_pre_greenfield.py: same parameters and bit-identical simulation outputs,
   with brakes off (env unset) and with brakes on (M8_BRAKES=final), for several variants.
2. variant 'greenfield' / M8_FINAL=1 change only the gf_on flag (and the brake flags for M8_FINAL), no other draw.
3. the lever model's text anchors still match the new m8_v4.py (m9_lever.build_patched).
4. integrated headline at the main-run size and seeds (3000 x 8 x 200): brakes off -> 0.44656 / 0.13853,
   brakes on (M8_BRAKES=final), greenfield off -> 0.36744 / 0.08784.
GPU only. Usage: python models/check_greenfield_identity.py [N]   (writes results/greenfield_identity_check.json)
"""
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
for k in ("M8_BRAKES", "M8_FINAL", "M8_GF", "M8_CF", "M8_WFL"):
    os.environ.pop(k, None)
import torch  # noqa: E402
import m8_v4 as NEW  # noqa: E402
import m8_v4_pre_greenfield as OLD  # noqa: E402
import m8_v4_pre_computefb as GFV  # noqa: E402   (greenfield version, before the compute feedback)
import m8_v4_pre_widefloors as CFV  # noqa: E402   (greenfield + compute feedback version, before the wide floors)

assert torch.cuda.is_available() and os.environ.get("M8_CPU") != "1", "GPU required"
OUT = os.path.join(NEW.ROOT, "results", "greenfield_cf_wfl_identity_check.json")   # v3: greenfield + compute feedback + wide floors
assert not os.path.exists(OUT), OUT + " exists"
N = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
for M in (NEW, OLD, GFV, CFV):
    M.T_END = 2076.0; M.NSTEP = int(round((M.T_END - M.T0) / M.DT)); M.YEARS = np.arange(2027, 2077)
res = {"device": torch.cuda.get_device_name(0), "N": N, "m8_vs_pre_greenfield": {}}
ok = True
for env in ["", "final"]:
    if env:
        os.environ["M8_BRAKES"] = env
    else:
        os.environ.pop("M8_BRAKES", None)
    for variant in ["baseline", "rev_B2_fixed_consolidation", "v3_like", "brakes_final", "f6_caps_forced_x100_qcore4"]:
        pn = NEW.sample_params(N, np.random.default_rng(123), None, variant)
        po = OLD.sample_params(N, np.random.default_rng(123), None, variant)
        pdiff = [k for k in po if not np.array_equal(np.asarray(po[k]), np.asarray(pn[k]))]
        extra = sorted(set(pn) - set(po))
        on = NEW.simulate(pn, N, variant, records=True)
        oo = OLD.simulate(po, N, variant, records=True)
        nd = []
        for k, v in oo.items():
            if isinstance(v, dict):
                for kk in v:
                    if not np.array_equal(v[kk], on[k][kk], equal_nan=True):
                        nd.append(k + "." + kk)
            elif not np.array_equal(v, on[k], equal_nan=(v.dtype.kind == "f")):
                nd.append(k)
        ok &= (not nd) and (not pdiff)
        res["m8_vs_pre_greenfield"][f"M8_BRAKES={env or 'unset'}|{variant}"] = dict(param_diffs=pdiff, output_diffs=nd, new_param_keys=extra)
        print(env or "unset", variant, "param diffs", pdiff, "output diffs", nd, "new keys", extra); sys.stdout.flush()
os.environ.pop("M8_BRAKES", None)
# 2. greenfield switches change only flags
pb = NEW.sample_params(N, np.random.default_rng(123), None, "baseline")
sw = {}
for tag, env, var in [("variant greenfield", {}, "greenfield"), ("M8_GF=1", {"M8_GF": "1"}, "baseline"),
                      ("variant computefb", {}, "computefb"), ("variant greenfield_cf", {}, "greenfield_cf"), ("M8_CF=1", {"M8_CF": "1"}, "baseline"),
                      ("variant widefloors", {}, "widefloors"), ("variant greenfield_cf_wfl", {}, "greenfield_cf_wfl"), ("M8_WFL=1", {"M8_WFL": "1"}, "baseline"),
                      ("M8_FINAL=1", {"M8_FINAL": "1"}, "baseline"), ("M8_BRAKES=final", {"M8_BRAKES": "final"}, "baseline")]:
    os.environ.update(env)
    pv = NEW.sample_params(N, np.random.default_rng(123), None, var)
    for k in env:
        os.environ.pop(k)
    sw[tag] = [k for k in pb if not np.array_equal(np.asarray(pb[k]), np.asarray(pv[k]))]
    print(tag, "params differing from baseline:", sw[tag])
res["switches_params_differing_from_baseline"] = sw
# 2b. greenfield on, compute feedback off: identical to the greenfield-only code (m8_v4_pre_computefb.py)
res["gf_on_cf_off_vs_greenfield_code"] = {}
for env in ["", "final"]:
    if env:
        os.environ["M8_BRAKES"] = env
    else:
        os.environ.pop("M8_BRAKES", None)
    pn = NEW.sample_params(N, np.random.default_rng(123), None, "greenfield")
    po = GFV.sample_params(N, np.random.default_rng(123), None, "greenfield")
    pdiff = [k for k in po if not np.array_equal(np.asarray(po[k]), np.asarray(pn[k]))]
    on = NEW.simulate(pn, N, "greenfield", records=True); oo = GFV.simulate(po, N, "greenfield", records=True)
    nd = []
    for k, v in oo.items():
        if isinstance(v, dict):
            nd += [k + "." + kk for kk in v if not np.array_equal(v[kk], on[k][kk], equal_nan=True)]
        elif not np.array_equal(v, on[k], equal_nan=(v.dtype.kind == "f")):
            nd.append(k)
    ok &= (not nd) and (not pdiff)
    res["gf_on_cf_off_vs_greenfield_code"][f"M8_BRAKES={env or 'unset'}"] = dict(param_diffs=pdiff, output_diffs=nd)
    print("greenfield-only vs greenfield code", env or "unset", pdiff, nd)
os.environ.pop("M8_BRAKES", None)
# 2c. greenfield + compute feedback on, wide floors off: identical to the pre-wide-floors code (m8_v4_pre_widefloors.py)
res["gf_cf_on_wfl_off_vs_previous_code"] = {}
for env in ["", "final"]:
    if env:
        os.environ["M8_BRAKES"] = env
    else:
        os.environ.pop("M8_BRAKES", None)
    pn = NEW.sample_params(N, np.random.default_rng(123), None, "greenfield_cf")
    po = CFV.sample_params(N, np.random.default_rng(123), None, "greenfield_cf")
    pdiff = [k for k in po if not np.array_equal(np.asarray(po[k]), np.asarray(pn[k]))]
    on = NEW.simulate(pn, N, "greenfield_cf", records=True); oo = CFV.simulate(po, N, "greenfield_cf", records=True)
    nd = []
    for k, v in oo.items():
        if isinstance(v, dict):
            nd += [k + "." + kk for kk in v if not np.array_equal(v[kk], on[k][kk], equal_nan=True)]
        elif not np.array_equal(v, on[k], equal_nan=(v.dtype.kind == "f")):
            nd.append(k)
    ok &= (not nd) and (not pdiff)
    res["gf_cf_on_wfl_off_vs_previous_code"][f"M8_BRAKES={env or 'unset'}"] = dict(param_diffs=pdiff, output_diffs=nd)
    print("greenfield+cf vs pre-wide-floors code", env or "unset", pdiff, nd)
os.environ.pop("M8_BRAKES", None)
res["wide_floors_table"] = NEW.wfl_table()
# 3. lever anchors
import m9_lever as LVR  # noqa: E402
try:
    LVR.build_patched()
    res["lever_anchors_match"] = True
except AssertionError as e:
    res["lever_anchors_match"] = False; res["lever_anchor_error"] = str(e); ok = False
print("lever anchors match:", res["lever_anchors_match"])
# 4. integrated headline reproduction (fresh import so T_END etc. are the module defaults)
for M in (NEW,):
    M.T_END = 2075.0; M.NSTEP = int(round((M.T_END - M.T0) / M.DT)); M.YEARS = np.arange(2027, 2076)
import integrate_v4 as I  # noqa: E402
assert I.M8 is NEW
rep = {}
for tag, env, exp in [("brakes off, greenfield off", {}, (0.44656, 0.13853)),
                      ("brakes on (M8_BRAKES=final), greenfield off", {"M8_BRAKES": "final"}, (0.36744, 0.08784))]:
    t0 = time.time()
    os.environ.update(env)
    D = I.run_m8(3000, 8, "baseline")
    sv = I.simulate(I.BASE_CFG, D, 200, I.SEED)
    for k in env:
        os.environ.pop(k)
    H = I.headline(sv)
    a = I.stats(sv, H["nt_UC"])[0]["mean"]; b = I.stats(sv, H["nt_world"])[0]["mean"]
    rep[tag] = dict(expected=list(exp), got=[a, b], identical=bool(a == exp[0] and b == exp[1]), runtime_s=round(time.time() - t0, 1))
    ok &= rep[tag]["identical"]
    print(tag, rep[tag]); sys.stdout.flush()
    del D, sv
res["integrated_headline_reproduction"] = rep
res["ALL_OK"] = bool(ok)
with open(OUT, "w") as f:
    json.dump(res, f, indent=1)
print("ALL OK" if ok else "NOT OK")
