"""Jev elicitation of the depopulation-ideology baseline for v7 (pre-registered 2026-10-16 before any call).
Reuses the v6 grid wording (grid_def.py) for the setting, the coalition, the resistance and the absent ideology."""
import itertools
from grid_def import SETTING, TXT

FACTORS = {
    "closure": ["closed", "control"],
    "coalition": ["single", "junta", "oligarchy", "democracy_eroding"],
    "war": ["none", "war"],
    "unrest": ["none", "insurgency"],
    "ecology": ["normal", "severe"],
}
WAR = {
    "none": ["The bloc is at peace with its neighbours and rivals.",
             "There is no war; relations with other powers are tense but peaceful.",
             "The bloc is not fighting any war."],
    "war": ["The bloc has been at war with a rival power for two years.",
            "For the past two years the bloc has fought an open war against another major power.",
            "A war with a rival power began two years ago and is still going on."]}
ECO = {
    "normal": ["Climate and ecological conditions are roughly as in the 2020s.",
               "The environment is under the usual pressures of the 2020s, no worse.",
               "Ecological stress is at the level seen in the 2020s."],
    "severe": ["Severe heat, drought and crop failures strain the bloc's land and water every year.",
               "Ecological stress is severe: recurring droughts, heatwaves and harvest failures.",
               "The bloc suffers repeated climate disasters, with failing harvests and water shortages."]}
RES = {"none": TXT["resistance"]["none"], "insurgency": TXT["resistance"]["insurgency"]}
ORDER = [["coalition", "ideology", "war", "unrest", "ecology"],
         ["coalition", "war", "ecology", "ideology", "unrest"],
         ["ecology", "coalition", "unrest", "ideology", "war"]]
QUESTIONS = {
    "id9": "Within the next 9 years, a doctrine that the human population should be greatly reduced, justified by ecological limits or by making way for AI successors, takes hold among the ruling group.",
}


def cells():
    return [dict(zip(FACTORS, v)) for v in itertools.product(*FACTORS.values())]


def state(c, k):
    part = {"coalition": TXT["coalition"][c["coalition"]][k], "ideology": TXT["ideology"]["absent"][k],
            "war": WAR[c["war"]][k], "unrest": RES[c["unrest"]][k], "ecology": ECO[c["ecology"]][k]}
    return " ".join([SETTING[c["closure"]][k]] + [part[f] for f in ORDER[k]])


PROTOCOL = {
    "registered": "2026-10-16, written before any call; analysis plan fixed here",
    "tool": "Jev (TypeSafe System One, model jev-latest) via its HTTPS API, one yes/no (noul) question per state",
    "design": "full factorial closure 2 x coalition 4 x war 2 x unrest 2 x ecology 2 = 64 cells, 3 paraphrases each (reworded sentences, permuted order) = 192 calls. Setting, coalition, resistance and the absent ideology reuse the v6 grid sentences. The ideology is absent at the start of every state",
    "questions": QUESTIONS,
    "analysis": [
        "cell value = mean over 3 paraphrases; report paraphrase spread (median and 90th percentile of max-min)",
        "baseline p_id (model: P(uptake within 9 y) after closure, no war, calm, normal ecology) = mean over coalitions of the closed, no-war, calm, normal-ecology cells",
        "ratios against that baseline, averaged over the other factors: war (model x2.5), insurgency (model m_unrest U(1.5, 3)), severe ecology (model up to x1.5), no closure (model x0.1)",
        "logistic least squares on the logit of cell means with one-hot factors; report coefficients",
        "v7 prior: if the Jev baseline lies outside the v6 prior's 80% interval (lognormal median 0.045, sigma 0.6: 0.021-0.098), replace the prior by an evidence mixture (as for pr_red): weight 0.5 on v6, 0.5 on a lognormal at the Jev baseline with sigma 0.6. Ratios are reported against the model's multipliers, not substituted",
        "no cells dropped; no re-wording after seeing results",
    ],
}

if __name__ == "__main__":
    c = cells(); print(len(c)); print(state(c[0], 0)); print(state(c[-1], 2))
