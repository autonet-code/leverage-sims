"""Bit-identity check: m8_v4.py (with brakes, all OFF) vs m8_v4_pre_brakes.py, same seed and size.
Also checks that the brake variants change only what they should (new draws on a separate stream)."""
import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m8_v4 as NEW  # noqa: E402
import m8_v4_pre_brakes as OLD  # noqa: E402
import torch  # noqa: E402

print("cuda available:", torch.cuda.is_available(), "device:", NEW.pick_device())
N = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
for M in (NEW, OLD):
    M.T_END = 2076.0; M.NSTEP = int(round((M.T_END - M.T0) / M.DT)); M.YEARS = np.arange(2027, 2077)
ok = True
for variant in ["baseline", "rev_B2_fixed_consolidation", "v3_like"]:
    pn = NEW.sample_params(N, np.random.default_rng(123), None, variant)
    po = OLD.sample_params(N, np.random.default_rng(123), None, variant)
    for k in po:
        if not np.array_equal(np.asarray(po[k]), np.asarray(pn[k])):
            print("PARAM DIFF", variant, k); ok = False
    extra = sorted(set(pn) - set(po))
    on = NEW.simulate(pn, N, variant, records=True)
    oo = OLD.simulate(po, N, variant, records=True)
    nd = 0
    for k, v in oo.items():
        if isinstance(v, dict):
            for kk in v:
                if not np.array_equal(v[kk], on[k][kk], equal_nan=True):
                    print("OUT DIFF", variant, k, kk); nd += 1
        elif not np.array_equal(v, on[k], equal_nan=(v.dtype.kind == "f")):
            print("OUT DIFF", variant, k); nd += 1
    ok &= nd == 0
    print(variant, "params identical, outputs differing:", nd, "| new keys:", extra)
# brake variants: existing draws must be identical to baseline draws
pb = NEW.sample_params(N, np.random.default_rng(123), None, "baseline")
for variant in ["brake_pid", "brake_selfrisk", "brake_selfrisk_dis", "brake_mort", "brakes_all", "brakes_final"]:
    pv = NEW.sample_params(N, np.random.default_rng(123), None, variant)
    diff = [k for k in pb if not np.array_equal(np.asarray(pb[k]), np.asarray(pv[k]))]
    print(variant, "params differing from baseline:", diff)
print("BIT-IDENTICAL" if ok else "NOT IDENTICAL")
# follow-up round: Brake 1 (doctrine) must be unchanged from round 1 (m8_v4_brakes_r1.py)
if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "m8_v4_brakes_r1.py")):
    import m8_v4_brakes_r1 as R1
    R1.T_END = 2076.0; R1.NSTEP = int(round((R1.T_END - R1.T0) / R1.DT)); R1.YEARS = np.arange(2027, 2077)
    pn = NEW.sample_params(N, np.random.default_rng(123), None, "brake_pid")
    pr = R1.sample_params(N, np.random.default_rng(123), None, "brake_pid")
    on = NEW.simulate(pn, N, "brake_pid", records=False); orr = R1.simulate(pr, N, "brake_pid", records=False)
    nd = [k for k in orr if not isinstance(orr[k], dict) and not np.array_equal(orr[k], on[k], equal_nan=(orr[k].dtype.kind == "f"))]
    print("brake_pid vs round-1 code: outputs differing:", nd)
