import os
import sys, json
sys.path.insert(0, os.environ.get('JEV_PATH', '.')); import jev_hook; jev_hook.TIMEOUT = 60
from jev_hook import ask, noul
base = ("In a future country, AI systems and robots run the whole economy and carry out all military and police work, "
        "so the rulers no longer need the population as workers or soldiers. One man has ruled personally for years, "
        "with a small circle of senior officials around him. He dies suddenly of a stroke.")
alt = ("Picture a state where automated factories and robot security forces have replaced human workers, soldiers and police. "
       "A single dictator, surrounded by a handful of top aides, has held power for a long time. He dies unexpectedly.")
qs = {
 "p1": "Command of the robot armed forces passes intact to one designated heir, rather than being split among several members of the ruling circle.",
 "p2": "A single successor ends up holding the access codes and control of the automated military and police, so no power-sharing among the senior officials is needed.",
 "p3": "After the death, the ruler's chosen heir takes sole control of the automated security forces without having to bargain with the other top officials.",
}
out = {}
for sname, sc in [("base", base), ("alt", alt)]:
    res = ask({"scenario": sc}, {k: noul(v) for k, v in qs.items()})
    out[sname] = res
print(json.dumps(out, indent=1, default=str))
