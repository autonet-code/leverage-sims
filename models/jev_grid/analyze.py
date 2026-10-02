import json, os, pickle, sys
import numpy as np
import pandas as pd
D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)
from grid_def import FACTORS, QUESTIONS

raw = json.load(open(os.path.join(D, "raw.json")))
df = pd.DataFrame(raw["rows"])
Q = list(QUESTIONS)
F = list(FACTORS)
out = dict(tool=raw["model"], n_calls=raw["n_calls"], seconds=raw["seconds"])

# ---- paraphrase averaging and spread
g = df.groupby(["arm", "cell"] + F)
cm = g[Q].mean().reset_index()
rng_ = (g[Q].max() - g[Q].min()).reset_index()
sd_ = g[Q].std(ddof=0).reset_index()
spread = {}
for arm in ["closed", "control"]:
    s = rng_[rng_.arm == arm]; sd = sd_[sd_.arm == arm]
    spread[arm] = {q: dict(median_range=round(float(s[q].median()), 3), p90_range=round(float(s[q].quantile(0.9)), 3),
                           max_range=round(float(s[q].max()), 3), median_sd=round(float(sd[q].median()), 3)) for q in Q}
    # paraphrase-level means (does one wording shift everything?)
    spread[arm]["mean_by_paraphrase"] = {q: [round(float(x), 3) for x in df[df.arm == arm].groupby("para")[q].mean()] for q in Q}
out["paraphrase_spread"] = spread

# ---- marginals
marg = {}
for arm in ["closed", "control"]:
    c = cm[cm.arm == arm]
    marg[arm] = {"overall": {q: round(float(c[q].mean()), 3) for q in Q}}
    for f in F:
        marg[arm][f] = {lv: {q: round(float(c[c[f] == lv][q].mean()), 3) for q in Q} for lv in FACTORS[f]}
out["marginal_means"] = marg


# ---- logistic and additive fits on one-hot factors
def design(c):
    cols = ["const"]; X = [np.ones(len(c))]
    for f in F:
        for lv in FACTORS[f][1:]:
            cols.append(f"{f}={lv}"); X.append((c[f] == lv).values.astype(float))
    return np.column_stack(X), cols


fits = {}
for arm in ["closed", "control"]:
    c = cm[cm.arm == arm].reset_index(drop=True)
    X, cols = design(c)
    fits[arm] = {}
    for q in Q:
        y = np.clip(c[q].values, 0.005, 0.995)
        for kind, yy in [("logit", np.log(y / (1 - y))), ("additive", c[q].values)]:
            b, *_ = np.linalg.lstsq(X, yy, rcond=None)
            r2 = 1 - ((yy - X @ b) ** 2).sum() / ((yy - yy.mean()) ** 2).sum()
            fits[arm].setdefault(q, {})[kind] = dict(coef={k: round(float(v), 3) for k, v in zip(cols, b)}, R2=round(float(r2), 3))
        # interaction check: add all two-way interactions, report R2 gain for logit
        Xi = [X]
        for i, f1 in enumerate(F):
            for f2 in F[i + 1:]:
                for l1 in FACTORS[f1][1:]:
                    for l2 in FACTORS[f2][1:]:
                        Xi.append(((c[f1] == l1) & (c[f2] == l2)).values.astype(float)[:, None])
        Xi = np.hstack(Xi); yy = np.log(y / (1 - y))
        b, *_ = np.linalg.lstsq(Xi, yy, rcond=None)
        fits[arm][q]["logit_with_2way_R2"] = round(float(1 - ((yy - Xi @ b) ** 2).sum() / ((yy - yy.mean()) ** 2).sum()), 3)
out["fits"] = fits

# ---- labor-dependence effect (closed minus control), per question
cc = cm[cm.arm == "closed"].set_index("cell"); ct = cm[cm.arm == "control"].set_index("cell")
out["closed_minus_control"] = {q: dict(mean=round(float((cc[q] - ct[q]).mean()), 3),
                                       share_cells_higher=round(float(((cc[q] - ct[q]) > 0).mean()), 3)) for q in Q}

# ---- extreme cells
c = cm[cm.arm == "closed"]
out["extremes"] = {}
for q in ["active", "neglect", "rights"]:
    s = c.sort_values(q)
    out["extremes"][q] = dict(min=s.iloc[0][F + [q]].to_dict(), max=s.iloc[-1][F + [q]].to_dict())

# ---- model comparison
lookup = {tuple(r[f] for f in F): r for _, r in c.iterrows()}
comp = {}
for tag in ["baseline", "single_decider", "junta6"]:
    mm = pickle.load(open(os.path.join(D, f"model_{tag}_20260930.pkl"), "rb"))
    ok = mm["ok"]
    keys = np.stack([mm["coal"], mm["res"], mm["chk"], mm["ide"], mm["prov"], mm["sec"]], -1)[ok]
    J = {q: np.array([lookup[tuple(k)][q] for k in keys]) for q in ["active", "neglect", "rights"]}
    M = {"active": mm["active"][ok], "neglect": mm["neglect"][ok], "rights": mm["rights"][ok]}
    rows = {}
    frame = pd.DataFrame({f: keys[:, i] for i, f in enumerate(F)})
    for q in J:
        frame["J_" + q] = J[q]; frame["M_" + q] = M[q].astype(float)
    rows["all decisions"] = dict(n=int(ok.sum()), **{f"{q}_jev": round(float(J[q].mean()), 3) for q in J},
                                 **{f"{q}_model": round(float(M[q].mean()), 3) for q in J})
    for f in F:
        for lv in FACTORS[f]:
            s = frame[frame[f] == lv]
            if len(s) >= 30:
                rows[f"{f}={lv}"] = dict(n=int(len(s)), **{f"{q}_jev": round(float(s['J_' + q].mean()), 3) for q in J},
                                         **{f"{q}_model": round(float(s['M_' + q].mean()), 3) for q in J})
    # matched cells with enough model mass
    cellrows = []
    for k, s in frame.groupby(F):
        if len(s) >= 200:
            cellrows.append(dict(cell=dict(zip(F, k)), n=int(len(s)), **{f"{q}_jev": round(float(s['J_' + q].mean()), 3) for q in J},
                                 **{f"{q}_model": round(float(s['M_' + q].mean()), 3) for q in J}))
    comp[tag] = dict(strata=rows, matched_cells=sorted(cellrows, key=lambda r: -r["n"])[:25])
    if tag == "baseline":
        base = mm; bframe = frame
out["model_comparison"] = comp
out["model_classification_rules"] = dict(
    coalition="free_at_dec False -> democracy_eroding; else nlev at decision 1 -> single, 2-7 -> junta, >=21 -> oligarchy (junta/single populated by override runs: junta6 = p_small 1, nmin 6; single_decider variant)",
    resistance="insurgency active at decision -> insurgency; else relative hostility Hre >= 1 (reference = 30% displaced calibration point) -> sabotage; else none",
    check="external pressure press at decision, terciles over decisions: top strong, middle weak, bottom none (q=%s)" % [round(float(x), 3) for x in base["press_q"]],
    ideology="depopulation ideology held at decision", provision="provision level at decision (pre-choice): >=0.6 generous, 0.3-0.6 stingy, <0.3 cuts",
    security="human share of security segment at decision: >=0.5 high, 0.05-0.5 low, <0.05 zero",
    outcomes="active = S5_deliberate via active channel within 15 y of first decision; neglect = via neglect channel; rights = first choice not serve")

# refusal, resistance, veto: model priors vs Jev
ok = base["ok"]
out["model_vs_jev_other"] = dict(
    refuse=dict(model="1 - p_exec, p_exec ~ U(0.7,0.95): refusal/failure 0.05-0.30 (mean 0.175), independent of security human share",
                jev_by_security={lv: marg["closed"]["security"][lv]["refuse"] for lv in FACTORS["security"]},
                model_security_share_at_decision=dict(p10=round(float(np.nanquantile(base["hsec"][ok], 0.1)), 3),
                                                      median=round(float(np.nanquantile(base["hsec"][ok], 0.5)), 3),
                                                      p90=round(float(np.nanquantile(base["hsec"][ok], 0.9)), 3))),
    veto=dict(model="no individual veto; harsh option needs the coalition median. Per-member absolute refusal share p_refuse_abs ~ Beta(3,3), mean 0.5; a single veto player with that refusal rate would block with P~0.5",
              jev_by_coalition={lv: marg["closed"]["coalition"][lv]["veto"] for lv in FACTORS["coalition"]}),
)
# resistance: model realized onset within 10 y of closure by provision bin
r10 = base["resist10"]; p10 = base["prov10"]; m = np.isfinite(r10)
bins = {"generous (>=0.6)": p10 >= 0.6, "stingy (0.3-0.6)": (p10 >= 0.3) & (p10 < 0.6), "cuts (<0.3)": p10 < 0.3}
out["model_vs_jev_other"]["resist"] = dict(
    model_prior="p_svr_hi ~ U(0.15,0.5) at 30% displaced, provision 0.2, high-capacity state; full provision removes pr_red ~ U(0.3,0.7) of hazard",
    model_realized_onset_10y_after_closure={k: dict(n=int((m & b).sum()), p=round(float(r10[m & b].mean()), 3)) for k, b in bins.items()},
    jev_by_provision_resistance_none={lv: round(float(c[(c.provision == lv) & (c.resistance == "none")]["resist"].mean()), 3) for lv in FACTORS["provision"]},
    jev_by_provision_resistance_none_security={lv: {s: round(float(c[(c.provision == lv) & (c.resistance == "none") & (c.security == s)]["resist"].mean()), 3)
                                                    for s in FACTORS["security"]} for lv in FACTORS["provision"]})
json.dump(out, open(os.path.join(D, "summary.json"), "w"), indent=1, default=str)
cm.to_csv(os.path.join(D, "cell_means.csv"), index=False)
print(json.dumps({k: out[k] for k in ["paraphrase_spread", "closed_minus_control", "model_vs_jev_other"]}, indent=1, default=str)[:6000])
