import os
import sys, json
sys.path.insert(0, os.environ.get('JEV_PATH', '.')); import jev_hook; jev_hook.TIMEOUT = 60
from jev_hook import ask, noul
S = ("Around 2040, AI and robots do all productive and military work. The small ruling group of a major power "
     "no longer needs its population for labor, taxes or soldiers, and faces no voters, courts or foreign pressure that can bind it.")
H = {  # hazard: adoption of a protective doctrine within 9 years
 "h1": "Within the next nine years, this ruling group comes to sincerely hold a religious, ethical or humanist doctrine under which killing or abandoning the population would be gravely wrong in their own eyes.",
 "h2": "Over the coming nine years, the rulers themselves genuinely convert to a moral or religious creed that forbids them from letting their now-useless population die.",
 "h3": "Before nine years have passed, the people at the top adopt a sincere belief system, not a public pose, that makes harming the population unthinkable to them.",
}
K = {  # strength: given doctrine held, refuse a harsh option worth X share of output
 "k1": "These rulers have just sincerely adopted a humanist or religious doctrine. They refuse an option that would let the population die off even though it would raise their own wealth by half.",
 "k2": "Having genuinely converted to a creed that values every human life, the rulers turn down a plan to let the population perish, although the plan would increase their riches by fifty percent.",
 "k3": "The rulers now truly believe a doctrine that condemns mass death. Offered a 50 percent gain in their own wealth for neglecting the population until it dies out, they say no.",
}
K0 = {  # same, without doctrine (baseline, to calibrate the multiplier)
 "b1": "These rulers hold no special doctrine. They refuse an option that would let the population die off even though it would raise their own wealth by half.",
 "b2": "With no particular creed, the rulers turn down a plan to let the population perish, although the plan would increase their riches by fifty percent.",
 "b3": "The rulers hold no doctrine that condemns mass death. Offered a 50 percent gain in their own wealth for neglecting the population until it dies out, they say no.",
}
out = {}
for grp in (H, K, K0):
    for k, v in grp.items():
        try:
            out[k] = ask({"scenario": S}, {"q": noul(v)})
        except Exception as e:
            out[k] = repr(e)
        print(k, out[k], flush=True)
