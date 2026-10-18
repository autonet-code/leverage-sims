"""v7 variance breakdown: which uncertain inputs drive the spread of the headline.

Draws N0 parameter sets from the baseline priors and runs each one K times with independent
in-simulation randomness, so every draw gets its own probability estimate p_i. The spread of p_i
across draws (corrected for the K-path sampling noise) is the parameter spread; the rest is path
randomness that no input explains. For each input we report the first-order share of the parameter
spread (variance of the binned conditional mean), and a shallow tree gives conditional statements.

Env: M8_FINAL=1 (as the main run), VAR_N0 (default 4000), VAR_K (default 10).
Output: results/v7_variance.json
"""
import os, sys, json, time
import numpy as np
import m8_v7 as m

US, CN = 0, 1
YEAR = 2075.0


def features(p, N0):
    X, names = [], []
    for k, v in p.items():
        a = np.asarray(v)
        if not a.ndim or a.shape[0] != N0 or not (np.issubdtype(a.dtype, np.number) or a.dtype == bool):
            continue
        a = a.astype(float)
        if a.ndim == 1:
            cols = {k: a}
        elif a.ndim == 2 and a.shape[1] == 17:
            cols = {f"{k}[US]": a[:, US], f"{k}[CN]": a[:, CN]}
        elif a.ndim == 3 and a.shape[1] == 17:
            cols = {f"{k}[US,mean]": a[:, US].mean(1), f"{k}[CN,mean]": a[:, CN].mean(1),
                    f"{k}[US,min]": a[:, US].min(1), f"{k}[CN,min]": a[:, CN].min(1)}
        else:
            continue
        for n, c in cols.items():
            if np.isfinite(c).all() and c.std() > 0:
                X.append(c); names.append(n)
    return np.stack(X, 1), names


def first_order(x, y, noise_var_mean, bins=20):
    """Var over quantile bins of the bin mean of y, minus the expected sampling variance of a bin mean."""
    q = np.quantile(x, np.linspace(0, 1, bins + 1)[1:-1])
    b = np.searchsorted(q, x, side="right")
    vals, mu, n = [], [], []
    for j in np.unique(b):
        s = b == j
        mu.append(y[s].mean()); n.append(s.sum())
    mu, n = np.array(mu), np.array(n)
    w = n / n.sum()
    between = (w * (mu - y.mean()) ** 2).sum()
    corr = (w * (y.var() / n)).sum()          # sampling noise of each bin mean
    lo_hi = (float(mu[0]), float(mu[-1]))
    return max(between - corr, 0.0), lo_hi


def main():
    t0 = time.time()
    N0 = int(os.environ.get("VAR_N0", 4000)); K = int(os.environ.get("VAR_K", 10))
    dev = m.pick_device()
    p = m.sample_params(N0, np.random.default_rng(m.SEED), None, "baseline")
    Xf, names = features(p, N0)
    pt = {k: (np.concatenate([v] * K, 0) if isinstance(v, np.ndarray) and v.ndim and v.shape[0] == N0 else v) for k, v in p.items()}
    o = m.simulate(pt, N0 * K, "baseline", dev=dev, chunk=N0, records=False)   # one chunk per replicate, each its own seed
    print("sim done", round(time.time() - t0), "s"); sys.stdout.flush()
    outs = dict(S5d_UC=(o["t_S5d"][:, :2].min(1) <= YEAR), NT_UC=(o["tL_del"][:, :2, 3].min(1) <= YEAR))
    res = dict(N0=N0, K=K, note=__doc__, outcomes={})
    for on, yv in outs.items():
        P = yv.reshape(K, N0).astype(float).mean(0)            # per-draw probability over K paths
        pbar = P.mean()
        tot = pbar * (1 - pbar)                                # total variance of a single-path outcome
        noise = (P * (1 - P)).mean() / (K - 1)                 # sampling noise in P from K paths
        epi = max(P.var() - noise, 1e-12)                      # variance of the true per-draw probability
        fo = []
        for j, n in enumerate(names):
            v, (lo, hi) = first_order(Xf[:, j], P, noise)
            fo.append((v / epi, n, lo, hi))
        fo.sort(reverse=True)
        # shallow tree on P for conditional statements, and a boosted model for the total explained share
        from sklearn.tree import DecisionTreeRegressor, export_text
        from sklearn.ensemble import HistGradientBoostingRegressor
        from sklearn.model_selection import cross_val_predict
        gb = HistGradientBoostingRegressor(max_iter=300, learning_rate=0.05, max_leaf_nodes=15, min_samples_leaf=40)
        pred = cross_val_predict(gb, Xf, P, cv=5)
        expl = 1 - ((P - pred) ** 2).mean() - noise
        tree = DecisionTreeRegressor(max_depth=3, min_samples_leaf=200).fit(Xf, P)
        res["outcomes"][on] = dict(
            mean=round(float(pbar), 4),
            share_of_total_variance_from_inputs=round(float(epi / tot), 3),
            per_draw_probability_95pct_range=[round(float(x), 3) for x in np.quantile(P, [0.025, 0.975])],
            note_range="raw K-path estimates; includes some sampling noise",
            boosted_model_share_of_input_variance_explained=round(float(1 - max(((P - pred) ** 2).mean() - noise, 0) / epi), 3),
            first_order_top=[dict(input=n, share=round(float(s), 3), risk_low_bin=round(lo, 3), risk_high_bin=round(hi, 3)) for s, n, lo, hi in fo[:25]],
            first_order_sum_all=round(float(sum(s for s, *_ in fo)), 3),
            tree=export_text(tree, feature_names=names, decimals=3))
        print(on, json.dumps({k: v for k, v in res["outcomes"][on].items() if k != "tree"}, indent=1)[:3000])
        print(res["outcomes"][on]["tree"]); sys.stdout.flush()
    res["runtime_s"] = round(time.time() - t0, 1)
    out = os.path.join(os.path.dirname(__file__), "..", "results", f"v7_variance{os.environ.get('VAR_TAG', '')}.json")
    json.dump(res, open(out, "w"), indent=1)
    print("done", res["runtime_s"], "s")


if __name__ == "__main__":
    main()
