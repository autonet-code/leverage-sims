"""v7 extra analyses for the paper (Section 5.1 and 5.8).

rights: when the US or China public loses its rights, by year, in the actor simulation run on its own (main seed,
        20,000 draws). Rights stripped = a first decision to live off rents, warehouse, neglect or depopulate, captivity,
        or deliberate mass death. Output: results/v7_rights_timeline.json
ideology: the ideology base rate scaled down until the 2045 US-or-China uptake meets the six-bloc calibration target
        (about 0.08), and its effect on the headline (10,000 draws per factor). Output: results/v7_ideology_sensitivity.json

Run: M8_FINAL=1 python models/v7_extras.py [rights|ideology|all]
"""
import os, sys, json
import numpy as np
import m8_v7 as m

RES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")


def rights(N=20000):
    p, o = m.run_variant("baseline", N)
    yrs = [2030, 2032, 2035, 2038, 2040, 2045, 2050, 2060, 2075]
    fc, td = o["first_choice"], o["t_first_dec"]

    def tr(a):
        tw = np.where(np.isin(fc[:, a], [1, 3, 4, 5]), td[:, a], np.inf)     # rentier, warehouse, neglect, depopulate
        return np.minimum.reduce([tw, o["t_first_harsh"][:, a], o["t_captive"][:, a], o["t_S5d"][:, a]])
    uc = np.minimum(tr(0), tr(1))
    r = dict(years=yrs, rights_stripped_US_or_China=[round(float((uc <= y).mean()), 3) for y in yrs],
             rights_stripped_US=[round(float((tr(0) <= y).mean()), 3) for y in yrs],
             rights_stripped_China=[round(float((tr(1) <= y).mean()), 3) for y in yrs],
             median_year_if_reached_US_or_China=float(np.median(uc[np.isfinite(uc)])),
             note="m8 layer only (no integrator S4 path); rights stripped = first rentier/warehouse/neglect/depopulate decision, captivity or deliberate S5")
    json.dump(r, open(os.path.join(RES, "v7_rights_timeline.json"), "w"), indent=1)
    print(json.dumps(r))


def ideology(N=10000):
    out = {}
    for f in [1.0, 0.5, 0.3, 0.2, 0.12]:
        p = m.sample_params(N, np.random.default_rng(m.SEED), None, "baseline")
        p["p_id"] = p["p_id"] * f
        o = m.simulate(p, N, "baseline", records=False)
        out[f] = dict(ideology_US_or_China_by={y: round(float((o["t_id"][:, :2].min(1) <= y).mean()), 3) for y in [2035, 2045, 2060, 2075]},
                      S5d_UC_2075=round(float((o["t_S5d"][:, :2].min(1) <= 2075).mean()), 4),
                      NT_UC_2075=round(float((o["tL_del"][:, :2, 3].min(1) <= 2075).mean()), 4))
        print(f, json.dumps(out[f]), flush=True)
    json.dump(out, open(os.path.join(RES, "v7_ideology_sensitivity.json"), "w"), indent=1)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    if mode in ("rights", "all"):
        rights()
    if mode in ("ideology", "all"):
        ideology()
