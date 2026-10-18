"""Model structure diagram (v7: seventeen actors, alliances, institutions and drives).
Output: figures/structure/model_structure_v7.{png,svg,pdf}"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = os.path.join(os.path.dirname(__file__), "..", "figures", "structure")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"; MUTED = "#57606a"; RED = "#b42318"
C_PHYS = "#dbe9f6"; C_PUB = "#fbe5d0"; C_DEC = "#e4dcf3"; C_OUT = "#f6d6d6"; C_FRAME = "#f4f5f7"; C_STOP = "#d9efdc"
C_BETW = "#e3eee0"

fig, ax = plt.subplots(figsize=(16, 12.6))
ax.set_xlim(0, 160); ax.set_ylim(-22, 104); ax.axis("off")

# columns: x0, width (gutters of 8 units between them)
C1, C2, C3, C4 = (2, 34), (44, 32), (84, 36), (128, 30)
TOP, MID, BOT = (55, 21), (30, 21.5), (4, 22)          # y0, height


def box(col, row, title, body, fc, fs=8.9, lw=1.0, ec=INK):
    (x, w), (y, h) = col, row
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.2", fc=fc, ec=ec, lw=lw))
    ax.text(x + 1.2, y + h - 1.4, title, fontsize=10.3, fontweight="bold", color=INK, va="top")
    ax.text(x + 1.2, y + h - 4.6, body, fontsize=fs, color=INK, va="top", linespacing=1.35)


def arrow(p, q, color=INK, lw=1.5, label=None, lx=0, ly=0):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=15, color=color, lw=lw, shrinkA=1, shrinkB=1))
    if label:
        ax.text((p[0] + q[0]) / 2 + lx, (p[1] + q[1]) / 2 + ly, label, fontsize=8.4, color=color, ha="center",
                va="center", style="italic")


def right(col, y): return (col[0] + col[1] + 0.4, y)
def left(col, y): return (col[0] - 0.4, y)


# ---------------- title and scenario frame ----------------
ax.text(1, 102.6, "Structure of the model (v7)", fontsize=15, fontweight="bold", color=INK, va="top")
ax.text(1, 99.4, "Seventeen actors, simulated year by year, 2026 to 2075, as a Monte Carlo over all uncertain parameters. "
        "Labels in brackets refer to the assumptions in Section 4 of the paper.", fontsize=9.4, color=MUTED, va="top")
ax.add_patch(FancyBboxPatch((0.5, 84.5), 159, 11.5, boxstyle="round,pad=0.3,rounding_size=1.2", fc=C_FRAME, ec=MUTED, lw=0.9))
ax.text(1.6, 94.8, "Scenario tree around the actor simulation", fontsize=10.3, fontweight="bold", color=INK, va="top")
ax.text(1.6, 91.4, "Earlier stages (US and China, regimes still staffed by humans):  automation race  →  collapse of broad "
        "economic participation  →  broad repression.\nCompeting end points: AI takeover not directed by rulers, non-AI global "
        "catastrophe (a run that hits one first is not counted).\nCounterfactual: if the US becomes broadly repressive first, "
        "all seventeen actors continue from a world where the US is autocratic at closure.",
        fontsize=8.9, color=INK, va="top", linespacing=1.4)

# ---------------- actor frame ----------------
ax.add_patch(FancyBboxPatch((0.5, 0.8), 159, 81.5, boxstyle="round,pad=0.3,rounding_size=1.2", fc="none", ec=MUTED, lw=1.0, ls="--"))
ax.text(1.6, 81.4, "Inside each actor: US, China, Japan, South Korea, Taiwan, Western EU, Eastern EU, UK, Canada-Australia-NZ, "
        "Russia and Central Asia, Gulf, rest of MENA,\nIndia, rest of South Asia, Southeast Asia, Latin America, sub-Saharan Africa. "
        "Each actor is modeled as one state with one ruling coalition.",
        fontsize=8.9, color=MUTED, va="top", style="italic", linespacing=1.3)

# column 1: physical world
box(C1, TOP, "1  AI and robots",
    "AI capability follows the measured\ntask-horizon trend and can speed up\n(A1). An actor's own chips and energy\n"
    "add capability; others lag and catch\nup. Robots build robots, limited by\nenergy, chips, mining and world\ninputs (A2, B6).", C_PHYS)
box(C1, MID, "2  Automation and closure",
    "Nine economic segments automate. A\ndedicated automated core loop can be\nbuilt beside the old economy.\n"
    "Human-dependence index: share\nof 2026 labor still needed.\nCLOSURE when it falls below 20%.", C_PHYS)
box(C1, BOT, "3  Force",
    "Security automates first (A3). Once\nfielded at scale, refusal by soldiers\nand police stops mattering (A4).\n"
    "Military power = spending x output x\nautomated share. Power inside the\nruling group = control of that force (A6).", C_PHYS)

# column 2: the public
box(C2, TOP, "4  Democracy",
    "V-Dem liberal democracy score.\nFalls as labor and revolt leverage\nfall. Below 0.30 = breakdown.\n"
    "Sets the decision rule in box 7.", C_PUB)
box(C2, MID, "5  The public's leverage",
    "Labor: people can stop working.\nRevolt: people can fight.\nEnforcers: soldiers can refuse.\n"
    "All three fall with closure (box 2)\nand automated force (box 3).", C_PUB)
box(C2, BOT, "6  Grievance and unrest",
    "Displacement and provision cuts\n(no safety net by default, A5)\n→ grievance → hostility → yearly\n"
    "insurgency hazard → repression.\nProvision only partly buys peace.\n"
    "Allied autocracies may send forces\nto put down an uprising (box 10).", C_PUB, fs=8.6)

# column 3: decision
x3, w3 = C3
ax.add_patch(FancyBboxPatch((x3, 4), w3, 72, boxstyle="round,pad=0.4,rounding_size=1.2", fc=C_DEC, ec=INK, lw=1.6))
ax.text(x3 + 1.2, 74.6, "7  The ruling coalition decides", fontsize=10.8, fontweight="bold", color=INK, va="top")
sections = [
    (71.0, None, "Every year once the actor reaches closure.\nUp to 21 members (autocracy) or a\n"
                 "51-person elite (democracy), drawn from\nthe state, the military and the owners\nof AI and industry. "
                 "Each has, correlated\nthrough seven drives:\n  moral cost of ordering killing (lower at\n"
                 "  the top in autocracies, B1)\n  concern for the public, discount rate\n  share of automated force (box 3)"),
    (49.9, "Each member scores six options:",
     "+ public's welfare x concern\n− cost of provision (falls with growth)\n− threat of revolt and sabotage\n"
     "− latent threat: what survivors could\n   later become, even when quiet\n− outside pressure if enforceable (B3)\n"
     "+ preference for an emptier planet,\n   only under a depopulation ideology\n− own moral cost of killing or neglect"),
    (27.1, "Decision rule depends on regime:",
     "democracy: 3 to 5 veto players\noligarchy: force-weighted supermajority\npersonalist: leader decides, inner circle\nmay veto"),
    (14.9, "Inside the group:",
     "purges and counter-coups (B2). A\ndepopulation ideology can spread, faster\n"
     "in war and unrest. Brakes: fear of being\nnext, leader mortality, protective doctrine."),
]
for y, head, body in sections:
    if head:
        ax.text(x3 + 1.2, y, head, fontsize=9.2, fontweight="bold", color=INK, va="top")
        y -= 3.0
    ax.text(x3 + 1.2, y, body, fontsize=8.6, color=INK, va="top", linespacing=1.3)

# column 4: options and outcomes
box(C4, TOP, "8  Options (mild → harsh)",
    "1  serve the public\n2  live off rents\n3  keep the status quo\n4  warehouse (minimal provision)\n"
    "5  neglect\n6  depopulate", C_DEC)
box(C4, (25, 26), "9  How deaths happen",
    "Ordered depopulation: automated\n  force, economic strangulation,\n  abstract means of mass killing (A8)\n"
    "Chosen, with no order to kill:\n  lethal neglect, partly through a\n  deniable passive channel\nWar, up to nuclear exchange (A9);\n"
    "  attacks on weaker actors (B5)\nTotal loss only: despair, crackdowns", C_OUT, fs=8.2)
box(C4, (4, 16.5), "What stops a campaign",
    "a successful revolt, a repelled\nattack, or nuclear retaliation", C_STOP, fs=8.6)

# ---------------- between actors (new in v7) ----------------
ax.add_patch(FancyBboxPatch((2, -20.5), 156, 18.0, boxstyle="round,pad=0.4,rounding_size=1.2", fc=C_BETW, ec=INK, lw=1.0))
ax.text(3.2, -3.9, "10  Between actors", fontsize=10.3, fontweight="bold", color=INK, va="top")
ax.text(3.2, -7.1, "Alliances: defense commitments that deter attacks and\nextend nuclear deterrence (B5), draw allies into wars,\n"
        "enforce outside pressure (B3) and ease trade in robot\ninputs (B6). Allies never attack each other. Atrocities\nbreak ties; autocracies form new ones.",
        fontsize=8.9, color=INK, va="top", linespacing=1.35)
ax.text(57, -7.1, "Allied autocracies send forces to help put down uprisings.\nForeign troops do not defect, so revolts succeed less\n"
        "often. Democracies do not send forces. The helper's cost\nto its own defenses is not modeled.",
        fontsize=8.9, color=INK, va="top", linespacing=1.35)
ax.text(108, -7.1, "The US as of October 2026: weak commitments to\nEurope, Canada and Oceania, middling to Japan\n"
        "and Korea, partial alignment with Russia (no\ndefense). Ties do not recover after a US return\nto democracy. Small US-Europe war hazards.",
        fontsize=8.9, color=INK, va="top", linespacing=1.35)

# arrows: only between neighbours
xc1, xc2, xc4 = C1[0] + C1[1] / 2, C2[0] + C2[1] / 2, C4[0] + C4[1] / 2
arrow((xc1, TOP[0] - 0.4), (xc1, MID[0] + MID[1] + 0.4))                  # 1 -> 2
arrow((xc1, MID[0] - 0.4), (xc1, BOT[0] + BOT[1] + 0.4))                  # 2 -> 3
arrow(right(C1, 44), left(C2, 44))                                        # 2 -> 5
arrow(right(C1, 34), left(C2, 20))                                         # 2 -> 6
arrow((xc2, MID[0] + MID[1] + 0.4), (xc2, TOP[0] - 0.4))                  # 5 -> 4
arrow(right(C2, 66), left(C3, 66))                                        # 4 -> 7
arrow(right(C2, 15), left(C3, 15), label="threat", ly=1.8)                # 6 -> 7
arrow(right(C3, 66), left(C4, 66))                                        # 7 -> 8
arrow((xc4, TOP[0] - 0.4), (xc4, 51.4))                                   # 8 -> 9
arrow((xc4, 24.6), (xc4, 20.9))                                           # 9 -> stops
arrow(left(C4, 38), right(C3, 38), color=RED, lw=1.8)                     # 9 -> 7 feedback
ax.text(124, 39.5, "fear of\nsurvivors\n(A11, B4)", fontsize=7.4, color=RED, ha="center", va="bottom",
        style="italic", linespacing=1.2)
arrow((xc2, -2.0), (xc2, 3.3), color=MUTED)                               # 10 -> 6 (help against uprisings)
arrow((x3 + w3 / 2, -2.0), (x3 + w3 / 2, 3.3), color=MUTED)               # 10 -> 7 (pressure, deterrence)
arrow((xc4, -2.0), (xc4, 3.3), color=MUTED)                               # 10 -> stops (repelled attacks)

for ext in ("png", "svg", "pdf"):
    fig.savefig(os.path.join(OUT, f"model_structure_v7.{ext}"), dpi=200, bbox_inches="tight", facecolor="white")
print("ok")
