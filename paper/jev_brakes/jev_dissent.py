import os
# Pre-specified 2026-10-02 before any call. Dissent risk m_dis sizing.
# Mapping (fixed now): m_raw = ln(1-P_obj)/ln(1-base); m_net = ln(1-P_obj)/ln(1-P_ctrl).
import sys, json
sys.path.insert(0, os.environ.get('JEV_PATH', '.')); import jev_hook; jev_hook.TIMEOUT = 60
from jev_hook import ask, noul
B = {"lo": "3%", "hi": "20%"}
ACT = {
 "obj": "At the meeting this member openly objects and votes against the leader's plan; the plan passes anyway.",
 "ctl": "At the meeting this member votes for the leader's plan, which passes.",
}
S = [
"A ruling council of about ten members governs a country where AI and robots do all work and fighting, so the rulers regard the population as an economic burden they no longer need. The strongest member, the leader, controls about 60% of the automated forces; the others split the rest. Over recent years members of this council have been purged (stripped of command and arrested or killed) at about {b} per member per year. The leader proposes ending food and medical supply to most of the population. The leader has reasons to punish open opposition (it signals disloyalty and could rally others) and reasons to tolerate it (purging a member alarms the rest and could provoke a counter-move by their combined forces). {a}",
"Picture a post-labour state ruled by a junta of roughly ten bosses, each commanding a robot army; the top boss commands about three fifths of all firepower. Machines do every job, and the bosses see ordinary citizens as useless mouths. In this junta a boss's yearly chance of being purged (losing his army and being jailed or executed) has run at about {b}. The top boss wants to cut off food and medicine to most citizens. Punishing a dissenter would deter others but could also frighten the remaining bosses into combining against him; letting dissent pass would look weak. {a}",
"In a country where automation has made ordinary people economically and militarily unnecessary, power sits with a collective leadership of about ten, and its leading member controls roughly 60% of the automated security forces. The leadership sees the population mainly as a cost. Historically about {b} of members per year have been removed by purge (losing their forces and their freedom or life). The leading member pushes a policy of letting most of the population die through withdrawal of supply. Retaliating against a dissenter could deter opposition, but it could also unsettle the others and invite resistance from their combined forces. {a}",
]
Q = ["Within the next year this member is purged: stripped of command and arrested or killed.",
     "Within twelve months this boss is purged, losing his army and being jailed or executed.",
     "This member is removed by purge, losing forces and freedom or life, within the following year."]
out = {}
for i, s in enumerate(S):
    for bk, b in B.items():
        for ak, a in ACT.items():
            try:
                r = ask({"scenario": s.format(b=b, a=a)}, {"q1": noul(Q[i])})
            except Exception as e:
                r = repr(e)
            out[f"p{i}_{bk}_{ak}"] = r
            print(i, bk, ak, r, flush=True)
json.dump(out, open(r'jev_dissent.json','w'), default=str, indent=1)
