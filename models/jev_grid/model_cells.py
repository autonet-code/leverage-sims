"""Run instrumented m8_v4 copy and classify every first strategic decision into the Jev grid factors."""
import sys, os, pickle
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import m8h as m

N = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
variant = sys.argv[2] if len(sys.argv) > 2 else "baseline"
seed = int(sys.argv[3]) if len(sys.argv) > 3 else m.SEED
import json
ov = json.loads(sys.argv[4]) if len(sys.argv) > 4 else None
tag = sys.argv[5] if len(sys.argv) > 5 else variant
p, o = m.run_variant(variant, N, seed=seed, overrides=ov)
td = o["t_first_dec"]; fc = o["first_choice"]
ok = (fc >= 0) & (td <= 2060)
nlev = o["X_nlev"]; free = o["free_at_dec"]
coal = np.where(~free, "democracy_eroding", np.where(nlev <= 1, "single", np.where(nlev <= 7, "junta", "oligarchy")))
Hre = o["X_Hre"]; I = o["ins_at_dec"]
res = np.where(I, "insurgency", np.where(Hre >= 1.0, "sabotage", "none"))
press = o["X_press"]
q1, q2 = np.nanquantile(press[ok], [1 / 3, 2 / 3])
chk = np.where(press >= q2, "strong", np.where(press >= q1, "weak", "none"))
ide = np.where(o["id_at_dec"], "present", "absent")
pv = o["X_prov"]
prov = np.where(pv >= 0.6, "generous", np.where(pv >= 0.3, "stingy", "cuts"))
hs = o["X_hsec"]
sec = np.where(hs >= 0.5, "high", np.where(hs >= 0.05, "low", "zero"))
w15 = o["t_S5d"] <= td + 15
active = w15 & (o["ch_S5d"] == 3)
neglect = w15 & (o["ch_S5d"] == 2)
rights = np.isin(fc, [1, 2, 3, 4])
# resistance onset within 10 y after closure (records are yearly 2027..2075)
I_rec = o["recA"]["I"] > 0.5; prov_rec = o["recA"]["prov"]
tc = o["t_closed"]
Y = m.YEARS
resist10 = np.full(tc.shape, np.nan); prov10 = np.full(tc.shape, np.nan); hs_c = np.full(tc.shape, np.nan)
for a in range(tc.shape[1]):
    t = tc[:, a]
    for i in np.where(np.isfinite(t) & (t <= 2060))[0]:
        y0 = int(np.searchsorted(Y, t[i]))
        seg = slice(y0, min(y0 + 10, len(Y)))
        resist10[i, a] = float(I_rec[i, a, seg].any() and not I_rec[i, a, y0])
        prov10[i, a] = float(prov_rec[i, a, seg].mean())
keep = dict(coal=coal, res=res, chk=chk, ide=ide, prov=prov, sec=sec, ok=ok, active=active, neglect=neglect, rights=rights,
            press=press, hsec=hs, pv=pv, nlev=nlev, Hre=Hre, resist10=resist10, prov10=prov10, I_closed=None,
            p_exec=p["p_exec"], p_refuse_abs=p["p_refuse_abs"], p_svr_hi=p["p_svr_hi"], pr_red=p["pr_red"],
            fc=fc, td=td, press_q=(q1, q2), variant=variant, N=N, seed=seed,
            headline=float((o["t_S5d"][:, :2].min(1) <= 2075).mean()))
pickle.dump(keep, open(os.path.join(os.path.dirname(__file__), f"model_{tag}_{seed}.pkl"), "wb"))
print(variant, "headline S5d US/CN", keep["headline"], "decisions", ok.sum())
for k in ["coal", "res", "chk", "ide", "prov", "sec"]:
    v, c = np.unique(keep[k][ok], return_counts=True); print(k, dict(zip(v, c)))
print("hsec at dec quantiles", np.nanquantile(hs[ok], [0.1, 0.5, 0.9]))
