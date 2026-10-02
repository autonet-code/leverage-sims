"""
M9: decentralized-AI lever test (black box), plugged into m8_v4 + integrate_v4 without changing the baseline.

The lever is "adoption level X of economic activity reached by year Y" (grid X in {5, 10, 25, 50}%, Y in {2028, 2030,
2032, 2035, 2040}). How adoption is achieved is NOT modelled. Decentralized AI is a black box: only its effects enter,
through the channels approved by the scenario (HANDOFF.md):

 C1 leverage   participants stay economically relevant: the A6 labour-leverage term 0.5*D_full gets the network's share
               of activity that stops if participants withdraw: Lev += 0.5 * (1 - D_full) * a * h_net.
 C2 control    the share n of the bloc's automated capability (compute and robots) coordinated by the network is outside
               any ruler's control: every coalition member's control share of coercive force is scaled by (1 - n)
               (leader share S_L, purge hazard, counter-coup odds, personalist threshold, inner veto), and the narrow
               power-grab hazard by (1 - n). n = network compute share s_b.
 C3 refusal    aligned capability refuses repression in proportion to the network's share phi of effective frontier
               capability: each depopulation order, collective-punishment order and cross-bloc launch is blocked with
               P = phi (blocked orders cause no deaths; the coalition can retry after the usual 5-year cool-down), and the
               death hazard of a programme already running is scaled by (1 - phi). Sensitivity: F3-style threshold
               (blocked only if phi > 1 - c_req).
 C4 livelihood livelihoods independent of the state (review round 1: income, not work). Network income a*y_h covers a share
               cov of the displaced public's need. Audit fix: network income reaches the displaced at average-share
               (population-proportional) breadth, so a displaced person receives a*y_h of average income: cov = a*y_h
               (the pre-audit form cov = a*y_h / displaced put ALL network income on the displaced; kept as an upper
               sensitivity, cf. m7 reward_breadth U(0.1, 0.5)). Means-tested state provision is clawed back at rate claw,
               so provision Pv -> min(1, max(Pv - claw*cov, 0) + cov) (grievance, hostility, despair mortality all follow Pv),
               and a regime that keeps people (serve, rentier, status quo, warehouse) pays only the top-up: those options'
               costs x (1 - claw*cov/target). Under a lethal choice (neglect, depopulation) the state strangles land/energy/
               food and only s_acc survives (cov x s_acc; lethal-neglect mortality x (1 - a*y_h*s_acc)). The pre-review form
               (fewer displaced people) is kept as an upper sensitivity.
 C5 soft power NO defensive or kinetic capability. Foreign publics' favourability toward the network grows with its presence
               (years to majority Ty) and reduces the crackdown hazard in a bloc by R_b * sum_c w_c fav_c L_c^e, where L_c
               is foreign public c's remaining leverage over its own government (A6 leverage x democracy index, relative to
               the 2026 US/Europe level). It decays as foreign publics lose leverage: a deadline.
 C6 enclaves   optional share e of participants in self-sufficient physical enclaves: resilience (despair and neglect
               deaths x (1 - E_b)) vs visibility (crackdown hazard x (1 + (V - 1) e), sovereignty-claim suppression, and the
               A11 no-witness logic: perceived revenge threat x (1 + k_seed * E_b / 1%)).
 C7 governance wildcard: innovation efficiency E multiplies the network's effective capability; decision speed scales its
               recovery after a crackdown. The efficiency bar to out-innovate centralized actors before closure is reported.
 Compute       network share of a bloc's compute s_b = s_max * min(1, a_b / 0.5), s_max ~ log-U(1%, 10%) (r13a).
               Effective capability = E * s_b * [c * M_rel + (1 - c) * f_novel]; coverage c = c_max (1 - exp(-U / tau)),
               U = use-years at >=10% world adoption; f_novel = 10^(-lag / L27) (compute-equivalent lag). Centralized
               providers cut frontier access at the first US/China closure or US crackdown; the lag then moves to the
               compute-implied lag L27 * log10(central/network compute) unless open weights continue (p_oc).
 Crackdown     state crackdown risk stays in. p_thr is a ONE-TIME P(suppression) realised over T_thr years after the regime's
               threat threshold is crossed (window re-opens on a new crossing or a regime change, closes at the crackdown).
               Otherwise the hazard is h0[regime] (a/a_ref)^k with a clamped to [a_ref, 10 a_ref] (the measured elasticity
               range); x enclave visibility, x (1 - soft-power protection). A crackdown cuts realised adoption by eff (reduced
               by foreign attention); it recovers at rho0 * speed / median(speed), except in a closed autocratic bloc, where
               it recovers at rho_cl ~ U(0, 0.1)/yr. Frontier cut: US or China closure, or a US crackdown.
 Spread rule   adoption reaches X in the US bloc by Y. Other blocs: X * r_b by Y + d_b, with r = access factor (Europe 1;
               China U(0.3, 0.7): firewall, capital controls; Russia/MENA U(0.3, 0.7); South Asia and Global South
               U(0.5, 1.0)) and delay d_b (Europe U(0, 1), China U(0, 2), others U(0, 3)). Variant: uniform (r = 1, d = 0).
               Crackdowns come on top (new suppression events, not standing access barriers).

ROUND 2 (HANDOFF 'Lever round 2 fixes' L1-L9, approved 2026-10-01; research/r15a_lever_round2.md). Principle: a network
carrying X% of economic activity carries the economic, political and organisational weight of X% of the economy. Still a
black box, still no kinetic or defensive capability, crackdown risk stays in. Every fix has a switch (ch_L*); all L
switches off reproduces the round-1 model draw for draw (round-2 parameters come from their own numpy stream, and new
torch draws are made only when the switch that needs them is on). The round-1 module is kept as m9_lever_round1.py.
 L1 compute     network compute share scales with adoption: s_b = kc a_b / (kc a_b + cfC_b), kc = compute per unit
               activity relative to the centralized economy (inference-heavy, no frontier training) and cfC_b the
               centralized compute factor after revenue starvation (L2); the round-1 mobilisation ceiling is kept as a
               floor. C2 (n) and C3 (phi) inherit it.
 L2 revenue     centralized revenue factor R_b = (1 - a_b)(1 - withdrawal - ban shock). Frontier labs (global sales):
               capex factor cf = R_world^eps_lab with a first-order lag; a fall in log capex becomes a capability lag
               (debt) of dln(cf)/g_eff years at the current progress rate, paid out of later progress (no regression).
               Physical build-out: the investment rate of centralized firms x (R_b/K_b)^eps_hyp, where the capital
               base K_b follows R_b at the investment rate i_K (a transient: once capital has adjusted, a smaller
               centralized economy automates its share at the old speed). Security automation (state, A3) exempt.
 L3 weight      leverage, control and refusal are not gated only by frontier-capability share: C1/C4 use a, and C2/C3
               scale with a through L1. The round-1 capphi lower bound stays as a sensitivity.
 L4 customers   withdrawal episodes: a crackdown on the network, a slide into autocracy or a harsh elite choice in a bloc
               trigger organised withdrawal of participants' remaining demand from centralized firms (loss l4 x a of
               centralized revenue, decaying with persistence pers x durability per 2 years). Political weight before
               closure: Lev += 0.5 k_pol l4 a Dc (customer leverage fades as the elite economy closes; revenue alone did
               not win Montgomery or apartheid, hence k_pol < 1).
 L5 talent      a share mv x min(1, a_US/0.5) of frontier talent moves; the centralized capability rate x
               (1 - moved)^(el5 (1 - s_rnd)) (fades as R&D automates).
 L6 crackdown   form shifts with size: P(capture/regulate | crackdown) = pcm x ramp(a; 5% -> 15%); a capture cuts adoption
               little (eff_cap) but subordinates the network (C2/C3 x (1 - cap)); the crackdown hazard is x (1 - cap/kap)
               (no re-crackdown while captured, back as the capture decays: courts, repeal; slower in autocracies). A full ban removes eff of adoption and hits centralized
               revenue through the supply chain ((dm - 1) x removed share, 1-year decay). Incidence is not reduced.
 L7 geo actor   the cross-bloc network responds as one actor: a crackdown/slide/harsh choice in bloc b also triggers
               withdrawal by participants elsewhere from b's exports (export share xs), and the network's weight in each
               outside economy adds to the outside pressure in the elite calculus (willing_c -> willing_c + (1 -
               willing_c) a_c l4, still scaled by the outsider's enforceability, B3).
 L8 speed       collective response rate x m8r = dur / (f_org/spd + 1 - f_org) (only the organising share of a response
               speeds up; digitally organised action is less durable). Applies to recovery after crackdowns (normalised
               to the calibration case, which was already a fast decentralized network), to the public's democratic
               recovery and redemocratisation hazards (x (1 + a (m8r - 1))), to capture reversal, and to withdrawal
               persistence.
 L9 legitimacy  recruitment x rec9 on crackdown recovery; backfire bf (mean ~0, Stephan-Chenoweth 2008 Table 3) on ban
               effectiveness; defection uplift (RRR def_up on odds of success, base 0.34) on the human-staffed share only:
               ban effectiveness and the public's democratic recovery (weighted by a).

ROUND 3 (two reviews of round 2, 2026-10-01). Each fix has a switch r3_* (or ch_core); all off reproduces round 2 draw for
draw, and the round-2 module is kept as m9_lever_round2.py. Round-3 priors come from a third numpy stream (LEVER_PRIORS3).
 C3 refusal     P(block) = phi x d_net: the coercive apparatus is state-owned security automation (A3) and the network has
               no kinetic role, so refusal binds only on the network-supplied, non-substitutable part of execution.
 C2 control     only on the economic power-grab hazard; no longer on the coalition's control of coercive force.
 L1 compute     centralized compute is a stock: dK/dt = (g + delta)(I/I0 - K); labs invest from world revenue (eps_lab),
               the rest from bloc revenue (eps_hyp); state compute (A3) is a floor exempt from starvation.
 C4 cost link   every option is paid from the elite fiscal base 1 - a (1 - tax) - dm L_lost (untaxed network activity and
               output destroyed by bans are outside it). Income share y_h capped at 1 - kc ccs (the network pays for its
               own hardware and energy out of the same revenue).
 L2 revenue     R_b = (1 - a - dm L_lost)(1 - wd) + a (1 - y_h) psi_c: the network buys chips/energy from centralized
               firms; a ban destroys the part of the banned activity that does not migrate back (re-absorbed over T_re).
               Investment and robot production slow only on the centralized share: x ((1 - a) fI + a).
 Closure        the closure test uses D_c,eff = D_c (1 - ac) + ac h_net, ac = a kphys (1 - cap) minus the replacement the
               elite builds at its investment rate i_K fI (ch_core). Also used in the L4 fade term.
 L4/L7          withdrawal limited to substitutable household spending (0.6 x sub; exports x sub); the standing political
               term uses the same capacity; capture subordinates C1, the L4 term and withdrawal, and does not trigger one.
               L7 outside pressure weighted by the outside public's remaining leverage (Lr^e, as C5).
 L6 form        P(ban | crackdown) = (1 - pc) exp(-k_cost eff a dm), and in a democracy x max(0, 1 - a / a_vote).
 L8/L9          durability dur3 0.5-0.9 (success factor centred ~1); unconditional defection rate; ban-effectiveness uplift
               weighted by min(1, a / 3.5%). L5: moved talent >= the network's share of world compute.

LEVER ROUND 3 UPDATES (HANDOFF 'Lever round 3 updates' U1-U4, approved 2026-10-01; the code's earlier "round 2/3/4" labels
are internal review rounds, and everything up to r4_* is the reported lever round-2 specification, archived as
m9_lever_round4audit.py). Each update has a switch u*_*; all off reproduces the lever round-2 grid draw for draw. New priors
come from a fourth numpy stream (LEVER_PRIORS4); no new torch draws.
 U1 autonomy    the network runs without humans; human withdrawal does not stop it. (a) u1_lev: C1 is reinterpreted as
               participants directing the network's whole activity through its governance (vote, delegation), not as labour
               they can withhold: the C1 term and the closure test count the network's share at weight 1 instead of h_net
               (X% of activity carries X% of the weight). (b) u1_crack: a ban stops activity only 1:1 with the hardware and
               node connections it removes; P2P segmentation is survivable (pieces keep running and merge back), so the share
               removed by a ban is eff x f_node, where f_node is the part of the calibrated ban effect (China mining, Tornado
               Cash) that is physical node removal rather than partition or user exit. The state's anticipated ban loss
               (L6 k_cost) uses the same reduced removal.
 U2 payout      y_h ~ U(0.9, 1.0): all output goes to households except service fees (treasury). The round-3 cap y_h <= 1 - kc ccs
               is replaced: hardware and energy are inputs paid before payout, so households get y_h of output net of the bill,
               a y_h (1 - kc ccs), and the network's purchases from centralized suppliers (L2) are
               a (kc ccs + (1 - y_h)(1 - kc ccs)) psi_c (bill plus treasury spending); the two sum to a (no double counting).
 U3 access      s_acc ~ U(0.2, 0.7): the contracts cannot be altered; a regime cutting people off can only attack conversion and
               access (exchanges, goods, token value).
 U4 substrate   the relative amortization advantage on covered tasks grows with coverage-weighted use (reuse of beaten paths):
               M_t = min(M exp(g4 Uc), max(M, 1/amort)), dUc = min(1, aw/0.1) (c/c_max) dt; the cap is the absolute saving
               (cost per covered task 10-30% of solving from scratch, r14b). The general efficiency trend is shared by both
               sides and cancels. Acts on effective capability (phi: C3, efficiency bar); compute intensity kc unchanged.

Baseline protection: m8_v4.py is NOT edited. Its source is patched at fixed anchors (each must match exactly once) into
models/_m8_v4_lever_gen.py; every hook is inside `if LV is not None:`, lever randomness uses its own torch generator, and
lever parameters are drawn from their own numpy stream after the baseline draws. With the lever off the pipeline must
reproduce the baseline headline bit for bit (verify()).

Run: python models/m9_lever.py [verify|grid|all]   (GPU; one job at a time)
Outputs: results/lever_grid.json, figures/lever_*.png
"""
import json
import os
import sys
import time
import types

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOD = os.path.join(ROOT, "models")
RES = os.path.join(ROOT, "results")
FIG = os.path.join(ROOT, "figures")
sys.path.insert(0, MOD)
LV_SEED = 20261001
A0 = 1e-4            # adoption today (share of economic activity): r13a active networks 0.03-0.2% of DC compute, revenue far lower
A_REF = 0.002        # 'small community' reference scale for crackdown base hazards (WIR ~0.2% of Swiss GDP, m7)

# ============================================================================================
# 1. patch m8_v4 source at fixed anchors
# ============================================================================================
PATCHES = [
    ("    rent_ok = P[\"rentier_on\"]\n",
     "    rent_ok = P[\"rentier_on\"]\n"
     "    LV = None\n"
     "    if \"lv_on\" in P and bool(P[\"lv_on\"].any()):\n"
     "        LV = LEVER_STATE_CLS(P, N, A, dev, seed, nb, reps)\n"),
    ("        cw = h_sa[..., None] * hn + (1 - h_sa[..., None]) * an          # A6: control share of coercive force\n",
     "        cw = h_sa[..., None] * hn + (1 - h_sa[..., None]) * an          # A6: control share of coercive force\n"
     "        if LV is not None:\n"
     "            cw = LV.ctl(cw)\n"),
    ("        Dc_prev = Dc\n",
     "        Dc_prev = Dc\n"
     "        if LV is not None:\n"
     "            LV.step(t, free, Ddem, t_closed, omega, Dc, choice)\n"),
    # ---- round 2 anchors
    ("        L = torch.minimum(L + torch.clamp(r0 * slow * corr * mult, max=15.0) * DT, Lcap)\n",
     "        L = torch.minimum(L + torch.clamp(r0 * slow * corr * mult, max=15.0) * DT, Lcap)\n"
     "        if LV is not None:\n"
     "            L = LV.capL(L, torch.clamp(r0 * slow * corr * mult, max=15.0), s_rnd, Lcap)\n"),
    ("        dxf = torch.clamp(torch.minimum(g_full * xf * (1 - xf / F_tot), cap_f * (F_tot - xf)), min=0) * DT\n",
     "        if LV is not None:\n"
     "            g_full, g_core, cap_f, cap_c = LV.inv(g_full, g_core, cap_f, cap_c)\n"
     "        dxf = torch.clamp(torch.minimum(g_full * xf * (1 - xf / F_tot), cap_f * (F_tot - xf)), min=0) * DT\n"),
    ("        kit_new = torch.minimum(kit * torch.exp(g_kit * DT), 1e4 * need_tot)\n",
     "        if LV is not None:\n"
     "            g_kit = LV.inv1(g_kit)\n"
     "        kit_new = torch.minimum(kit * torch.exp(g_kit * DT), 1e4 * need_tot)\n"),
    ("        prod = torch.minimum(prod * torch.exp(g_pot * dfac * DT), torch.clamp(cap, min=1e-6))\n",
     "        if LV is not None:\n"
     "            g_pot = LV.inv1(g_pot)\n"
     "        prod = torch.minimum(prod * torch.exp(g_pot * dfac * DT), torch.clamp(cap, min=1e-6))\n"),
    ("        rec_ep = demo & in_ep & (u2[:, :, 1] < 1 - torch.exp(-lam_r0[:, None] * Lev / torch.sqrt(shock) * DT))\n",
     "        if LV is not None:\n"
     "            rec_ep = demo & in_ep & (u2[:, :, 1] < 1 - torch.exp(-lam_r0[:, None] * Lev * LV.dmult() / torch.sqrt(shock) * DT))\n"
     "        else:\n"
     "            rec_ep = demo & in_ep & (u2[:, :, 1] < 1 - torch.exp(-lam_r0[:, None] * Lev / torch.sqrt(shock) * DT))\n"),
    ("        lam_red = 0.02 * Lev * T(RED_W)[None] * (1 + 3 * sdem.float())\n",
     "        lam_red = 0.02 * Lev * T(RED_W)[None] * (1 + 3 * sdem.float())\n"
     "        if LV is not None:\n"
     "            lam_red = lam_red * LV.dmult()\n"),
    ("            pi = E0t[:, None] * torch.where(b3, enf, press) * (0.3 + 0.7 * torch.clamp(imp_dep / 0.2, 0, 1))\n",
     "            pi = E0t[:, None] * torch.where(b3, enf, press) * (0.3 + 0.7 * torch.clamp(imp_dep / 0.2, 0, 1))\n"
     "            if LV is not None:\n"
     "                pi = LV.press(pi, E0t, fac_e, omega, willing, imp_dep, b3)\n"),
    ("        disp = (1 - Dfd) * (1 - P[\"r_ab\"][:, None] * Dfd)\n",
     "        disp = (1 - Dfd) * (1 - P[\"r_ab\"][:, None] * Dfd)\n"
     "        if LV is not None:\n"
     "            disp = LV.disp(disp)\n"),
    ("        dep = torch.where(chW, torch.maximum(disp, 1 - Dfd), disp)\n",
     "        dep = torch.where(chW, torch.maximum(disp, 1 - Dfd), disp)\n"
     "        if LV is not None:\n"
     "            dep = LV.dep(dep, chW, disp, Dfd)\n"),
    ("        r_neg = torch.where(decided & (choice == I_NEG), -float(np.log(0.9)) / P[\"Tn\"][:, None], 0.0)\n",
     "        r_neg = torch.where(decided & (choice == I_NEG), -float(np.log(0.9)) / P[\"Tn\"][:, None], 0.0)\n"
     "        if LV is not None:\n"
     "            r_neg = LV.neg(r_neg)\n"),
    ("        thr_rev = thr_rev * torch.where(b4, 1 + P[\"k_ret\"][:, None] * w_atroc, 1.0)\n",
     "        thr_rev = thr_rev * torch.where(b4, 1 + P[\"k_ret\"][:, None] * w_atroc, 1.0)\n"
     "        if LV is not None:\n"
     "            thr_rev = LV.seed(thr_rev)\n"),
    ("        lcp = lcp & ~lcp_def\n",
     "        lcp = lcp & ~lcp_def\n"
     "        if LV is not None:\n"
     "            lcp = LV.block_c(lcp, P[\"c_req\"])\n"),
    ("        hx = h0x + (h1x - h0x) * torch.clamp(tau_x / P[\"T_full\"][:, None], 0, 1)\n",
     "        hx = h0x + (h1x - h0x) * torch.clamp(tau_x / P[\"T_full\"][:, None], 0, 1)\n"
     "        if LV is not None:\n"
     "            hx = LV.slow(hx)\n"),
    ("& (dom >= P[\"dom_thr\"][:, None, None]) & ok_pay\n",
     "& (dom >= P[\"dom_thr\"][:, None, None]) & ok_pay\n"
     "            if LV is not None:\n"
     "                elig = LV.block_xb(elig, P[\"c_req\"])\n"),
    ("            hxb = h0x + (h1x - h0x) * torch.clamp(tau_b / P[\"T_full\"][:, None], 0, 1)\n",
     "            hxb = h0x + (h1x - h0x) * torch.clamp(tau_b / P[\"T_full\"][:, None], 0, 1)\n"
     "            if LV is not None:\n"
     "                hxb = LV.slow_xb(hxb, byc)\n"),
    ("        Lev = torch.where(P[\"a6_lev\"][:, None], 0.5 * Dfd + 0.25 * h_sec_f + 0.25 * rv * h_sec_f, Lev)\n",
     "        Lev = torch.where(P[\"a6_lev\"][:, None], 0.5 * Dfd + 0.25 * h_sec_f + 0.25 * rv * h_sec_f, Lev)\n"
     "        if LV is not None:\n"
     "            Lev = LV.lev(Lev, Dfd, Ddem)\n"),
    ("        grab_cum = grab_cum + P[\"k_pg\"][:, None] * (1 - h_sa) ** 2 * T(GRAB_W)[None] * DT\n",
     "        g_inc = P[\"k_pg\"][:, None] * (1 - h_sa) ** 2 * T(GRAB_W)[None] * DT\n"
     "        if LV is not None:\n"
     "            g_inc = LV.grab(g_inc, h_sa)\n"
     "        grab_cum = grab_cum + g_inc\n"),
    ("            okX = wantX & ~dfX & (ux[:, :, 0] < P[\"p_exec\"][:, None])\n"
     "            failX = wantX & ~okX\n",
     "            nfX = (LV.refuse(P[\"c_req\"]) & wantX & ~dfX) if LV is not None else torch.zeros_like(wantX)\n"
     "            okX = wantX & ~dfX & ~nfX & (ux[:, :, 0] < P[\"p_exec\"][:, None])\n"
     "            failX = wantX & ~okX & ~nfX\n"),
    ("            cool_until = torch.where(failX, t + 5.0, cool_until)\n",
     "            cool_until = torch.where(failX, t + 5.0, cool_until)\n"
     "            if LV is not None:\n"
     "                choice = torch.where(nfX, dflt, choice); cool_until = torch.where(nfX, t + 5.0, cool_until)\n"
     "                LV.note_block_x(nfX)\n"),
    ("        Pv = torch.where(t < prov_floor_until, torch.clamp(Pv, min=0.8), Pv)\n",
     "        Pv = torch.where(t < prov_floor_until, torch.clamp(Pv, min=0.8), Pv)\n"
     "        if LV is not None:\n"
     "            LV.G = G\n"
     "            Pv = LV.prov(Pv, disp, choice, decided, t, t_closed)\n"),
    # audit (round 4): the closure clock handed to the integrator (t_core, D_core < 0.2) must use the same D_c,eff as
    # the m8 closure test (ch_core); it used the raw D_c
    ("            t_core[:, :, j] = torch.where(torch.isinf(t_core[:, :, j]) & (Dc < th), t, t_core[:, :, j])\n",
     "            t_core[:, :, j] = torch.where(torch.isinf(t_core[:, :, j]) & ((LV.tcore_D(Dc) if LV is not None else Dc) < th), t, t_core[:, :, j])\n"),
    ("                                0.005 / G], -1)\n",
     "                                0.005 / G], -1)\n"
     "            if LV is not None:\n"
     "                cost = LV.cost(cost, Psq)\n"),
    # round 3: closure test counts the network's participant-controlled share of the core chain (ch_core)
    ("        closed_now = Dc < P[\"trig\"][:, None]\n",
     "        if LV is not None:\n"
     "            closed_now = LV.dcfix(Dc) < P[\"trig\"][:, None]\n"
     "        else:\n"
     "            closed_now = Dc < P[\"trig\"][:, None]\n"),
    ("    out = {k: v.cpu().numpy() for k, v in out.items()}\n",
     "    if LV is not None:\n"
     "        out.update(LV.outputs())\n"
     "    out = {k: v.cpu().numpy() for k, v in out.items()}\n"),
]
TAIL = '''

# ===================== appended by m9_lever.py (lever hooks) =====================
LEVER_CFG = None
LEVER_STATE_CLS = None
LEVER_SAMPLER = None
_sample_params_base = sample_params


def sample_params(N, rng, overrides=None, variant="baseline"):
    p = _sample_params_base(N, rng, overrides, variant)
    if LEVER_CFG is not None:
        p.update(LEVER_SAMPLER(N, p, LEVER_CFG))
    return p
'''
GEN_PATH = os.path.join(MOD, "_m8_v4_lever_gen.py")


def build_patched():
    src = open(os.path.join(MOD, "m8_v4.py"), encoding="utf-8").read()
    for old, new in PATCHES:
        c = src.count(old)
        assert c == 1, f"anchor matched {c} times: {old[:70]!r}"
        src = src.replace(old, new)
    src = "# GENERATED by m9_lever.py from m8_v4.py (do not edit). Lever hooks only; all inside `if LV is not None`.\n" + src + TAIL
    with open(GEN_PATH, "w", encoding="utf-8") as f:
        f.write(src)
    import importlib
    if "_m8_v4_lever_gen" in sys.modules:
        del sys.modules["_m8_v4_lever_gen"]
    gen = importlib.import_module("_m8_v4_lever_gen")
    return gen


# ============================================================================================
# 2. lever priors (epistemic, per draw). (spec, source, evidence grade)
# ============================================================================================
LEVER_PRIORS = {
    # compute and substrate (r13a, r14b)
    "lv_s_max": (("logu", 0.01, 0.10), "network share of world compute at full mobilisation (a = 50%): incentives plus ideology; consumer/edge usable 0.3-2M H100e of ~29M DC stock plus joined DC capacity (r13a)", "C"),
    "lv_E": (("lognormal", 1.0, 0.45, 0.5, 3.0), "governance wildcard: innovation efficiency per unit compute vs centralized, central 1 (0.5-3): OSS/open-weight record, no evidence of higher frontier R&D efficiency (r14b)", "low"),
    "lv_spd": (("logu", 0.2, 1.0), "governance wildcard: decision speed vs a centralized/autocratic actor, 0.5 (0.2-1): DAO 7-day minimum cycle (Compound docs) vs executive decisions (r14b)", "low-medium"),
    "lv_M": (("tri", 1.0, 1.3, 2.0), "relative amortization advantage on covered tasks vs centralized providers (who also cache/distil/reuse) (r14b)", "low"),
    "lv_cmax": (("tri", 0.5, 0.7, 0.85), "coverable ceiling of task volume (AEI bottom 80% of categories = 10.5-12.7% of use; 31% repeat queries; 44% routine jobs) (r14b)", "low"),
    "lv_tau": (("tri", 1.0, 2.0, 4.0), "coverage growth time constant, use-years (modelling assumption; Zipf task distribution) (r14b)", "low"),
    "lv_lag_pre": (("tri", 1.1, 3.5, 9.0), "network's own novel-task lag before any cut, months: open-weight lag 3.5 (1.1-5.3), consumer-GPU lag 6-12 (Epoch) (r14b)", "medium"),
    "lv_L27": (("tri", 17.0, 27.0, 46.0), "lag per 10x compute gap under closure, months (derived from 8-month algorithmic halving, Ho et al. 2024) (r14b)", "low-medium"),
    "lv_p_oc": (("uniform", 0.2, 0.6), "P(some open-weight releases continue after centralized providers cut frontier access) (strategic choice of a few firms/one state, m7)", "J"),
    "lv_dlag_oc": (("uniform", 3.0, 9.0), "extra lag (months) when only lower-tier open releases continue", "J"),
    # leverage and livelihoods
    "lv_h_net": (("uniform", 0.3, 0.9), "share of network activity that stops if participants withdraw (their hardware, review, keys): labour-like leverage under A6", "J"),
    "lv_y_h": (("uniform", 0.5, 1.0), "share of network value reaching human participants as income (rest: energy, chips)", "J"),
    "lv_s_acc": (("uniform", 0.0, 0.5), "share of network livelihoods that survive a state's deliberate strangulation of land/energy/food (m7: parallel economies depend on access)", "J"),
    # crackdown (r14a)
    "lv_h0_dem": (("tri", 0.002, 0.01, 0.03), "crackdown hazard/yr, small low-visibility network in a democracy (Christiania since 1971; WIR 90 years)", "medium"),
    "lv_h0_aut": (("tri", 0.02, 0.05, 0.10), "crackdown hazard/yr, small network in an autocracy (Falun Gong pre-1999; China crypto escalation 2013/2017/2021)", "low-medium"),
    "lv_k": (("tri", 0.4, 0.7, 1.2), "size elasticity of the hazard (crypto bans 23 -> 51 countries as market cap grew 5-10x, 2018-2021)", "low"),
    "lv_thr_aut": (("tri", 0.005, 0.02, 0.10), "autocracy threat threshold, share of activity (Falun Gong ~70M > CCP, banned July 1999)", "low-medium"),
    "lv_thr_dem": (("tri", 0.01, 0.05, 0.15), "democracy threshold where the network erodes tax/monetary control (Worgl, Liberty Dollar, Tornado Cash)", "low"),
    "lv_p_thr": (("tri", 0.5, 0.6, 0.8), "P(suppression) once above the threshold (m7; crypto bans; Falun Gong)", "medium"),
    "lv_T_thr": (("uniform", 1.0, 5.0), "years over which p_thr is realised above the threshold (Falun Gong ~3 months after Zhongnanhai; Worgl ~1 y; crypto bans years)", "J"),
    "lv_eff": (("uniform", 0.3, 0.8), "share of realised adoption removed by one crackdown (China mining 34% -> 0% -> 14-20% underground; Tornado Cash usage fell but did not stop) (m7 #26)", "low"),
    "lv_rho0": (("uniform", 0.3, 0.7), "recovery rate/yr after a crackdown at median governance speed (China Bitcoin mining back to ~half within ~1-2 y)", "C/J"),
    # soft power (r14a)
    "lv_R_gp": (("tri", 0.0, 0.10, 0.25), "max hazard reduction from foreign public support, great power acting on a core interest (Hong Kong 2020, Tibet, Xinjiang, Kurdistan 2017)", "medium"),
    "lv_R_dep": (("tri", 0.2, 0.40, 0.60), "same, repressor dependent on the supporters (Levitsky-Way linkage/leverage; South Africa, East Timor, Solidarity)", "low-medium"),
    "lv_sev": (("tri", 0.15, 0.35, 0.50), "reduction of crackdown severity by foreign attention (Krain 2012; Hafner-Burton 2008 caveat)", "low"),
    "lv_e": (("logu", 0.5, 2.0), "exponent on foreign publics' remaining leverage (structural inference)", "low"),
    "lv_Ty": (("tri", 4.0, 8.0, 15.0), "years to majority foreign favourability via culture (Hallyu 1997-2010s; Cold War cultural diplomacy)", "low-medium"),
    "lv_rev": (("tri", 0.10, 0.25, 0.40), "favourability reversal after a hostile event, own public of the cracking-down state (Japan affinity to Korea 63% -> 39%; Pew US 64 -> 22)", "medium"),
    "lv_cut": (("tri", 0.5, 0.7, 0.9), "effectiveness of an autocratic state cutting the cultural channel (China Hallyu ban after THAAD; Great Firewall)", "medium"),
    # enclaves (r14a; J)
    "lv_V": (("tri", 2.0, 5.0, 20.0), "visibility/collective-action hazard multiplier (King-Pan-Roberts 2013; Davenport 2007; Rajneeshpuram)", "low-medium"),
    "lv_p_sc": (("uniform", 0.3, 0.8), "P(self-governing enclaves are read as a sovereignty claim by the host state)", "J"),
    "lv_p_ss": (("tri", 0.7, 0.85, 0.95), "P(suppression | sovereignty claim within reach) (Rose Island 55 days; Kirkuk 21 days; Minerva; Catalonia)", "medium"),
    "lv_lag_ss": (("tri", 0.05, 0.15, 1.0), "years from claim to suppression (Kirkuk 21 d, Rose Island 55 d, Falun Gong ~3 months)", "medium"),
    "lv_k_seed": (("uniform", 0.0, 0.3), "A11 no-witness logic: rise of perceived revenge threat per 1% of the population living in self-sufficient enclaves (cap 10%)", "J"),
    # review round 1 (appended so earlier draws are unchanged)
    "lv_claw": (("uniform", 0.3, 1.0), "benefit-reduction (claw-back) rate of state provision against network income: means-tested programmes withdraw 0.3 (SNAP) to 0.55 (UK Universal Credit) to 1.0 (SSI, unearned income) per unit of other income", "C"),
    "lv_rho_cl": (("uniform", 0.0, 0.1), "recovery rate/yr after a crackdown in a CLOSED autocratic bloc (regime controls energy, compute, land): Falun Gong inside China has not recovered since 1999; China's mining recovery relied on globally mobile hardware and capital", "J"),
}
# round 2 (L1-L9), drawn from their own numpy stream so the round-1 draws are unchanged (r15a; J = judgment)
LEVER_PRIORS2 = {
    "lv_kc": (("uniform", 0.5, 1.0), "L1: network compute per unit of activity relative to the centralized economy (inference-heavy; the centralized side also spends 30-50% of compute on frontier training/R&D)", "J"),
    "lv_eps_lab": (("logtri", 0.5, 1.0, 2.0), "L2: elasticity of frontier-lab capex to expected revenue (capex ~5-10x AI revenue, debt/growth-contingent finance: OpenAI ~$13B 2025 revenue vs ~$1.4T commitments; telecom capex -50-60% 2000-02)", "low-medium"),
    "lv_eps_hyp": (("tri", 0.2, 0.4, 0.7), "L2: elasticity of cash-flow-funded capex (hyperscalers, industrial automation) to revenue relative to capital (Fazzari-Hubbard-Petersen 0.3-0.6; Meta 2022)", "medium-low"),
    "lv_lag_cx": (("tri", 0.5, 1.0, 1.5), "L2: capex response lag, years (telecom bust, 2022 tech)", "low"),
    "lv_g_eff": (("uniform", 1.4, 2.6), "L2: log growth/yr of the input whose level capex sets: training compute 4-5x/yr (ln 1.4-1.6) if algorithmic progress scales with experiment compute, up to compute x algorithms ~13x/yr (ln 2.6) if it does not (Epoch; Ho et al. 2024)", "low-medium"),
    "lv_l4": (("tri", 0.5, 0.8, 1.2), "L4: centralized revenue lost per unit withdrawing customer share when a substitute exists (Bud Light -25-30% peak, ~-40% persisting, AB InBev US revenue -13.5%; Montgomery; BDS ~0 without substitute)", "medium/low"),
    "lv_pers": (("tri", 0.3, 0.6, 0.9), "L4: persistence of a withdrawal after 2 years (Bud Light; Chinese boycotts of Lotte/Hyundai)", "low-medium"),
    "lv_kpol": (("uniform", 0.2, 0.6), "L4: political weight of customer leverage relative to labour leverage (revenue loss alone did not win Montgomery or apartheid: courts and elite defection were needed)", "J"),
    "lv_xs": (("uniform", 0.2, 0.3), "L7: export share of a bloc's revenue exposed to cross-bloc withdrawal (world exports ~29% of GDP)", "C"),
    "lv_mv": (("tri", 0.1, 0.2, 0.3), "L5: share of frontier talent willing to move (about half of OpenAI's safety team left in 2024; 97% letter as the solidarity ceiling)", "low"),
    "lv_el5": (("tri", 0.1, 0.3, 0.5), "L5: elasticity of the centralized capability rate to its top-talent share before R&D automation (OpenAI letter; Anthropic at the frontier ~2 years after the split; $1-100M packages)", "low"),
    "lv_pcm": (("tri", 0.6, 0.7, 0.8), "L6: P(crackdown takes the capture/regulate form | network share > 15%) (China 2020-23 subordinated platforms, ~$1T value lost; India demonetisation 86% of currency, government re-elected)", "low-medium"),
    "lv_kap": (("uniform", 0.3, 0.8), "L6: depth of capture, share of the network's control/refusal capacity subordinated to the state", "J"),
    "lv_eff_cap": (("uniform", 0.0, 0.2), "L6: share of realised adoption lost in a capture (platforms kept operating in China after 2021)", "J"),
    "lv_rcap_dem": (("uniform", 0.05, 0.2), "L6: capture reversal rate/yr in a democracy (Prohibition repealed after 13 years; courts)", "J"),
    "lv_rcap_aut": (("uniform", 0.0, 0.1), "L6: capture reversal rate/yr in an autocracy (China eased in 2023 but kept golden shares)", "J"),
    "lv_dm": (("uniform", 1.0, 2.0), "L6: supply-chain multiplier of a full ban's direct cost (demonetisation PMI 54.5 -> 46.7)", "low"),
    "lv_spd8": (("logtri", 2.0, 3.0, 10.0), "L8: speed multiplier on the organising part of a collective response (Egypt 18 days, Tunisia 28; OpenAI letter 3 days; IT Army 2 days; DAO fork 33 days; rulemaking 1-2 years)", "medium/low"),
    "lv_dur": (("uniform", 0.7, 1.0), "L8: durability of digitally organised action (Tufekci 2017; Chenoweth 2020 post-2010 decline)", "low"),
    "lv_forg": (("uniform", 0.3, 0.7), "L8: organising share of a collective response's duration (the rest is courts, elections, institutions)", "J"),
    "lv_rec9": (("logtri", 1.0, 1.5, 4.0), "L9: recruitment multiplier from legitimacy on recovery after a crackdown (nonviolent campaigns ~4x participants)", "medium-low"),
    "lv_bf": (("tri", -0.1, 0.0, 0.2), "L9: net repression backfire on ban effectiveness, mean ~0 (Stephan & Chenoweth 2008 Table 3: regime violence no significant effect within nonviolent campaigns)", "medium"),
    "lv_defup": (("tri", 2.0, 3.0, 4.4), "L9: defection uplift (RRR) on success, human-staffed share only (Stephan & Chenoweth 2008: 4.44 overall; nonviolence does not raise defection probability)", "medium"),
    "lv_pdoc": (("uniform", 0.32, 0.52), "L9: P(defections occur) in a campaign (32% of successful violent, 52% of successful nonviolent campaigns)", "medium"),
}
# round 3 (review of round 2), own numpy stream so round-1/round-2 draws are unchanged (J = judgment)
LEVER_PRIORS3 = {
    "lv_dnet": (("uniform", 0.05, 0.30), "R3/C3: share of a repression order's execution that depends on capability the network supplies and the state cannot route around before the order runs (civilian logistics, energy, comms; the Reichsbahn and Rwanda's radio show civilian chains mattered; under A3 the coercive apparatus itself is state-owned automation and the state can requisition)", "J"),
    "lv_tax": (("uniform", 0.5, 1.0), "R3/C4: share of network activity inside the state's tax base (informal economy ~0, card/platform income ~0.8-1, crypto reporting rules phasing in)", "J"),
    "lv_ccs": (("uniform", 0.10, 0.30), "R3/C4-L1: compute and energy cost share of activity in an AI-heavy economy (today DC capex ~0.5% of world GDP; capex runs 5-10x AI revenue during the build-out); the network pays kc x ccs of its value for hardware, so y_h <= 1 - kc ccs", "J"),
    "lv_psic": (("uniform", 0.5, 0.9), "R3/L2: share of the network's hardware/energy spending that goes to centralized suppliers (TSMC, Nvidia, utilities)", "J"),
    "lv_sub": (("uniform", 0.20, 0.45), "R3/L4: share of participants' remaining spending on centralized goods that has a substitute or can be deferred (US CEX: housing 33%, transport 17%, food 13%, health 8% are hard to withdraw)", "C/J"),
    "lv_avote": (("uniform", 0.2, 0.4), "R3/L6: network share above which a democracy no longer bans it outright (participants as a voter bloc); P(ban | crackdown, democracy) x max(0, 1 - a / a_vote)", "J"),
    "lv_kcost": (("uniform", 0.0, 3.0), "R3/L6: weight of the anticipated self-inflicted output loss (eff x a x dm) on choosing capture/regulation over a ban: P(ban) x exp(-k_cost x loss) (China 2021 chose capture of platforms worth ~$1T; India's demonetisation shows large self-harm does happen)", "J"),
    "lv_kphys": (("uniform", 0.2, 0.7), "R3/closure: network share of the core physical chain relative to its overall share (fabs and mines are capital-concentrated; distributed solar and owner-operator logistics are not; security sector 0 under A3)", "J"),
    "lv_gc": (("uniform", 0.2, 0.6), "R3/L1: log growth/yr of the centralized compute stock over the period (2-3x/yr today, slowing)", "low"),
    "lv_dep": (("uniform", 0.15, 0.25), "R3/L1: depreciation of compute hardware/yr (4-6 year accounting lives)", "C"),
    "lv_wlab": (("uniform", 0.3, 0.5), "R3/L1: frontier-lab share of centralized compute (global sales, eps_lab); the rest is hyperscaler/enterprise compute funded from bloc revenue (eps_hyp)", "J"),
    "lv_st": (("uniform", 0.05, 0.20), "R3/L1: state-owned compute (A3 security automation, national labs) as a share of baseline centralized compute; exempt from revenue starvation", "J"),
    "lv_mig": (("uniform", 0.3, 0.7), "R3/L6: share of banned network activity that migrates back to centralized firms (the rest is lost output for a while)", "J"),
    "lv_Tre": (("uniform", 0.5, 2.0), "R3/L6: years for lost output after a ban to be re-absorbed (India demonetisation: ~1 year)", "low"),
    "lv_dur3": (("uniform", 0.5, 0.9), "R3/L8: success/durability factor of digitally organised action (nonviolent campaign success ~65% in the 1990s vs ~34% in the 2010s, Chenoweth 2020; Tufekci 2017): faster onset, less success, so the recovery multiplier is centred near 1", "low"),
    "lv_pdoc3": (("uniform", 0.15, 0.35), "R3/L9: unconditional P(security defections) across campaigns, derived from 52%/32% among successful campaigns, a 0.34-0.53 success base and fewer defections among failures (J-derived)", "low"),
}
# lever round 3 updates (U1-U4), own numpy stream so all earlier draws are unchanged
LEVER_PRIORS4 = {
    "lv_fnode": (("uniform", 0.5, 0.9), "U1: share of a ban's calibrated adoption loss that is physical removal of hardware or node connections (stops activity 1:1); the rest (P2P partition, user exit) is survivable for an autonomous network. China mining 2021 (hardware moved out, ~1) vs Tornado Cash (contracts kept running, usage fell, ~0); hosts who unplug out of fear still count", "J"),
    "lv_y_h4": (("uniform", 0.9, 1.0), "U2: payout to households, all output except service fees that fund the treasury (network premise)", "J"),
    "lv_s_acc4": (("uniform", 0.2, 0.7), "U3: share of displaced people's needs still covered when a regime tries to cut them off; contracts cannot be altered, only conversion and access (exchanges, goods, token value) can be attacked (network premise)", "J"),
    "lv_g4": (("uniform", 0.02, 0.06), "U4: growth of the log relative amortization advantage per coverage-weighted use-year (doubling every 12-35 years; Zipf: library value grows ~log of size; AWM/Voyager reuse gains)", "J"),
    "lv_amort": (("uniform", 0.1, 0.3), "U4: cost per covered task relative to solving from scratch (r14b: reusable workflows 10-30%); 1/amort caps the relative advantage", "C"),
}
P_SUC9 = 0.34      # L9: nonviolent campaign success baseline, 2010s (Chenoweth 2020; 53% 1900-2006 not used)
LEV_ARMED_NOTE ="armed-hazard multiplier (2.5, Chenoweth & Stephan) NOT applied: the network has no defensive or kinetic capability"
UNUSED_RESEARCH = {
    "foreign_opinion_policy_passthrough_salient_democracy": "not multiplied in: R_gp/R_dep are realised reductions observed at today's passthrough; multiplying again would double count",
    "mobilization_days_to_1000_sites": "adoption path is the lever (black box); mobilization speed not modelled",
    "bass_q_imitation": "adoption path is the lever (black box); Bass diffusion only as a plausibility check on fast Y",
    "distilled_small_model_retention_*": "subsumed in lv_lag_pre / coverage",
    "decision_speed_multiplier_vs_democratic_legislature": "not used: the relevant contest is with executives and autocrats",
}


def _draw(rng, spec, N):
    k = spec[0]
    if k == "uniform":
        return rng.uniform(spec[1], spec[2], N)
    if k == "tri":
        return rng.triangular(spec[1], spec[2], spec[3], N)
    if k == "logu":
        return np.exp(rng.uniform(np.log(spec[1]), np.log(spec[2]), N))
    if k == "lognormal":
        return np.clip(spec[1] * np.exp(spec[2] * rng.standard_normal(N)), spec[3], spec[4])
    if k == "logtri":
        return np.exp(rng.triangular(np.log(spec[1]), np.log(spec[2]), np.log(spec[3]), N))
    return np.full(N, float(spec[1]))


DEFAULT_CFG = dict(X=0.25, Y=2030.0, enc=0.0, ch_lev=True, ch_ctl=True, ch_ref=True, ch_liv=True, ch_soft=True,
                   crack=True, uniform=False, ref_thr=False,
                   # review round 1 switches (main spec values here; alternatives are reported as sensitivities)
                   liv_disp=False,      # True: C4 as fewer displaced people (pre-review form; upper sensitivity)
                   cost_link=True,      # C4 lowers the state's cost of keeping people (means-tested top-up)
                   gate_closure=False,  # True: C4 x s_acc in every closed bloc (skeptic reading); main: only under lethal choices
                   crack_perm=False,    # True: above-threshold hazard permanent and re-firing (pre-review form)
                   rho_cl=True,         # closed autocracies: recovery rate lv_rho_cl instead of the calibrated rho
                   s_mult=1.0,          # multiplier on the network compute ceiling s_max (sensitivity)
                   capphi=False,        # True: C1/C4 use min(a, effective capability share) (lower-bound sensitivity)
                   cov_conc=False,      # audit: True = all network income reaches the displaced (cov = a*y_h/disp, pre-audit main; upper)
                   # round 2 switches (L3 has none: it is carried by L1 and by C1/C4 using a)
                   ch_L1=True, ch_L2=True, ch_L4=True, ch_L5=True, ch_L6=True, ch_L7=True, ch_L8=True, ch_L9=True,
                   ch_core=True,        # round 3: network's participant-controlled share of the core chain in the closure test
                   L7_wd=True, L7_press=True,   # the two parts of L7 (only active with ch_L7)
                   # round 3 fixes (review of round 2); all False + ch_core False reproduces round 2 draw for draw
                   r3_ref=True,         # C3: P(block) = phi x d_net (False: P = phi, round-2 form)
                   r3_ctl=True,         # C2 only on the power-grab hazard, not on control of coercive force
                   r3_kstock=True,      # L1: centralized compute is a stock (capex flow, depreciation), state floor, eps by owner
                   r3_base=True,        # C4: the elite's fiscal base shrinks with untaxed network activity (gated by L2)
                   r3_yh=True,          # C4/L1: income share capped by the network's own hardware/energy bill (gated by L1)
                   r3_rb=True,          # L2: network buys chips/energy from centralized firms; a ban destroys output (gated by L2)
                   r3_wd=True,          # L4/L7: withdrawal limited to substitutable household spending; standing term same scale
                   r3_cap=True,         # L6: capture also subordinates C1, the L4 term and withdrawal; captures do not trigger boycotts
                   r3_gate7=True,       # L7 press: weighted by the outside public's remaining leverage (as C5)
                   r3_inv=True,         # L2: only the centralized share of investment/robot production slows
                   r3_ban=True,         # L6: democracies stop banning large networks; anticipated cost tilts toward capture
                   r3_l8=True,          # L8: success factor dur3 (centred ~1 on recovery hazards)
                   r3_l9=True,          # L9: unconditional defection rate; uplift weighted by participation as in dmult
                   r3_l5=True,          # L5: talent moved >= the network's share of world compute (payroll follows compute)
                   # audit round 4 fixes; all False reproduces the round-3 (pre-audit) model draw for draw
                   r4_need=True,        # C4: network income per person measured against the cost of decent provision
                                        # (m0/G of output per person, the m8 'serve' cost), not against average income
                   r4_ref=True,         # C3 under L3: the network's share of the capability a repression order needs is
                                        # max(phi, a) (economic weight counts directly), times d_net (non-routable share)
                   need_G=True,         # r4_need: True = network income grows with output (it carries X% of activity);
                                        # False = network income fixed at the 2026 output scale (sensitivity)
                   r4_tcore=True,       # closure clock passed to the integrator uses D_c,eff (consistent with m8's test)
                   # lever round 3 updates (U1-U4); all False reproduces the lever round-2 grid draw for draw
                   u1_lev=True,         # U1: C1 and the closure test count the network's share at weight 1 (governance), not h_net
                   u1_crack=True,       # U1: a ban removes eff x f_node (hardware/connection removal only; partition survivable)
                   u2_yh=True,          # U2: y_h ~ U(0.9, 1.0) of output net of the kc ccs bill; L2 purchases a (kc ccs + (1 - y_h)(1 - kc ccs)) psi_c
                   u3_sacc=True,        # U3: s_acc ~ U(0.2, 0.7)
                   u4_sub=True,         # U4: relative amortization advantage grows with coverage-weighted use
                   ov=None)             # dict: fix round-2 parameters at a value (sensitivities)
L_SW = ["ch_L1", "ch_L2", "ch_L4", "ch_L5", "ch_L6", "ch_L7", "ch_L8", "ch_L9", "ch_core"]
R3_SW = ["r3_ref", "r3_ctl", "r3_kstock", "r3_base", "r3_yh", "r3_rb", "r3_wd", "r3_cap", "r3_gate7", "r3_inv", "r3_ban",
         "r3_l8", "r3_l9", "r3_l5"]
R4_SW = ["r4_need", "r4_ref", "r4_tcore"]
U_SW = ["u1_lev", "u1_crack", "u2_yh", "u3_sacc", "u4_sub"]


def sample_lever(N, p, cfg):
    """lever parameters from a separate numpy stream (depends only on N, so every grid cell sees the same draws)"""
    c = dict(DEFAULT_CFG); c.update(cfg)
    rng = np.random.default_rng([LV_SEED, N])
    q = {k: _draw(rng, spec, N) for k, (spec, _, _) in LEVER_PRIORS.items()}
    A = 6
    r = np.ones((N, A)); d = np.zeros((N, A))
    r[:, 1] = rng.uniform(0.3, 0.7, N); r[:, 3] = rng.uniform(0.3, 0.7, N)
    r[:, 4] = rng.uniform(0.5, 1.0, N); r[:, 5] = rng.uniform(0.5, 1.0, N)
    d[:, 2] = rng.uniform(0, 1, N); d[:, 1] = rng.uniform(0, 2, N)
    for a in (3, 4, 5):
        d[:, a] = rng.uniform(0, 3, N)
    q["lv_oc"] = rng.random(N) < q["lv_p_oc"]
    if c["uniform"]:
        r[:] = 1.0; d[:] = 0.0
    q["lv_r"] = r; q["lv_dly"] = d
    q["lv_on"] = np.ones(N, bool)
    q["lv_X"] = np.full(N, float(c["X"])); q["lv_Y"] = np.full(N, float(c["Y"])); q["lv_enc"] = np.full(N, float(c["enc"]))
    for k in ["ch_lev", "ch_ctl", "ch_ref", "ch_liv", "ch_soft", "crack", "ref_thr", "liv_disp", "cost_link", "gate_closure",
              "crack_perm", "rho_cl", "capphi", "cov_conc", "L7_wd", "L7_press", "need_G"] + L_SW + R3_SW + R4_SW + U_SW:
        q["lv_" + k] = np.full(N, bool(c[k]))
    q["lv_s_mult"] = np.full(N, float(c["s_mult"]))
    rng2 = np.random.default_rng([LV_SEED, N, 2])
    for k, (spec, _, _) in LEVER_PRIORS2.items():
        q[k] = _draw(rng2, spec, N)
    rng3 = np.random.default_rng([LV_SEED, N, 3])
    for k, (spec, _, _) in LEVER_PRIORS3.items():
        q[k] = _draw(rng3, spec, N)
    rng4 = np.random.default_rng([LV_SEED, N, 4])
    for k, (spec, _, _) in LEVER_PRIORS4.items():
        q[k] = _draw(rng4, spec, N)
    for k, v in (c.get("ov") or {}).items():     # fixed values for sensitivities (round-1 keys also allowed)
        q[k] = np.full(N, float(v))
    return q


# ============================================================================================
# 3. lever state inside the m8 time loop (torch)
# ============================================================================================
class LeverState:
    def __init__(self, P, N, A, dev, seed, nb, reps):
        import torch
        self.t_ = torch; self.P = P; self.N = N; self.A = A; self.dev = dev; self.nb = nb; self.reps = reps
        self.g = torch.Generator(device=dev); self.g.manual_seed(int(seed) + 15485863)
        f = lambda k: P[k].float()
        self.sw = {k: f("lv_" + k)[:, None] for k in ["ch_lev", "ch_ctl", "ch_ref", "ch_liv", "ch_soft", "crack"]}
        self.thr_mode = P["lv_ref_thr"].bool()[:, None]
        self.T0 = GEN.T0; self.DT = GEN.DT
        Xb = torch.clamp(f("lv_X")[:, None] * P["lv_r"].float(), min=3 * A0)
        self.Yb = f("lv_Y")[:, None] + P["lv_dly"].float()
        self.lg0 = float(np.log(A0 / (1 - A0))); self.lgX = torch.logit(Xb)
        z = torch.zeros(N, A, device=dev)
        self.sup = torch.ones(N, A, device=dev); self.a = z.clone(); self.E = z.clone(); self.ay = z.clone()
        self.n = z.clone(); self.phi = z.clone(); self.fav = z.clone(); self.prot = z.clone(); self.sevr = z.clone()
        self.U = torch.zeros(N, device=dev); self.c = torch.zeros(N, device=dev)
        self.lag = f("lv_lag_pre").clone(); self.t_cut = torch.full((N,), float("inf"), device=dev)
        self.levD = None; self.lref = None
        inf = float("inf")
        self.ncr = z.clone(); self.tcr1 = torch.full((N, A), inf, device=dev)
        self.nbx = z.clone(); self.nbc = z.clone(); self.nbxb = z.clone()
        self.enc_alive = (f("lv_enc")[:, None] > 0).float().expand(N, A).clone()
        self.vis_done = torch.zeros(N, A, dtype=torch.bool, device=dev)
        self.t_sup = torch.full((N, A), inf, device=dev); self.t_encsup = torch.full((N, A), inf, device=dev)
        self.eye = torch.eye(A, device=dev)[None]
        self.rho = f("lv_rho0") * f("lv_spd") / float(np.sqrt(0.2 * 1.0))     # median of log-U(0.2, 1) = sqrt(0.2)
        self.h_thr = -torch.log(1 - f("lv_p_thr")) / f("lv_T_thr")
        b = lambda k: bool(P["lv_" + k][0].item())
        self.liv_disp, self.cost_link, self.gate_closure = b("liv_disp"), b("cost_link"), b("gate_closure")
        self.crack_perm, self.rho_cl_on, self.capphi = b("crack_perm"), b("rho_cl"), b("capphi")
        self.cov_conc = b("cov_conc")
        self.s_mult = float(P["lv_s_mult"][0].item())
        self.above_prev = torch.zeros(N, A, dtype=torch.bool, device=dev); self.free_prev = None
        self.win_until = torch.full((N, A), -inf, device=dev)
        self.cov = z.clone(); self.phi_raw = z.clone(); self.a_c = z.clone()
        self.R = torch.cat([f("lv_R_gp")[:, None].expand(N, 2), f("lv_R_dep")[:, None].expand(N, A - 2)], 1)
        # ---- round 2 state
        self.L1, self.L2, self.L4, self.L5 = b("ch_L1"), b("ch_L2"), b("ch_L4"), b("ch_L5")
        self.L6, self.L7, self.L8, self.L9 = b("ch_L6"), b("ch_L7"), b("ch_L8"), b("ch_L9")
        self.core = b("ch_core"); self.L7w = self.L7 and b("L7_wd"); self.L7p = self.L7 and b("L7_press")
        r3 = {k: b(k) for k in R3_SW}
        self.r3_ref, self.r3_ctl = r3["r3_ref"], r3["r3_ctl"]
        self.r3_kstock = r3["r3_kstock"] and self.L1 and self.L2
        self.r3_base = r3["r3_base"] and self.L2
        self.r3_yh = r3["r3_yh"] and self.L1
        self.r3_rb = r3["r3_rb"] and self.L2
        self.r3_wd, self.r3_cap, self.r3_gate7, self.r3_inv = r3["r3_wd"], r3["r3_cap"] and self.L6, r3["r3_gate7"], r3["r3_inv"]
        self.r3_ban, self.r3_l8, self.r3_l9, self.r3_l5 = r3["r3_ban"], r3["r3_l8"], r3["r3_l9"], r3["r3_l5"]
        self.r4_need, self.r4_ref, self.r4_tcore = b("r4_need"), b("r4_ref"), b("r4_tcore") and self.core
        self.G = None; self.need_G = b("need_G")
        # L8: response-rate multiplier; only the organising share of a response speeds up, durability below 1
        self.dur = f("lv_dur3") if self.r3_l8 else f("lv_dur")
        self.m8r = self.dur / (f("lv_forg") / f("lv_spd8") + 1 - f("lv_forg"))
        # central values (f_org 0.5, spd 3; dur 0.85 round 2, 0.7 round 3): the calibration case for crackdown recovery
        self.m8c = (0.7 if self.r3_l8 else 0.85) / (0.5 / 3.0 + 0.5)
        self.pdoc = f("lv_pdoc3") if self.r3_l9 else f("lv_pdoc")
        # round 3: income share net of the network's own hardware/energy bill (the same revenue is not spent twice)
        self.u1_lev, self.u1_crack, self.u2, self.u3, self.u4 = b("u1_lev"), b("u1_crack"), b("u2_yh"), b("u3_sacc"), b("u4_sub")
        yh = f("lv_y_h")
        if self.u2:      # U2: all output to households except service fees; hardware/energy are inputs paid before payout,
            # so y_h is a share of output net of the kc ccs input bill (audit: paying y_h of gross output AND the bill spent
            # 1 + kc ccs per unit of activity)
            self.yh = (f("lv_y_h4") * (1 - f("lv_kc") * f("lv_ccs")))[:, None]
        else:
            self.yh = (torch.minimum(yh, 1 - f("lv_kc") * f("lv_ccs")) if self.r3_yh else yh)[:, None]
        self.sacc = f("lv_s_acc4" if self.u3 else "lv_s_acc")[:, None]
        self.hw = torch.ones(N, 1, device=dev) if self.u1_lev else f("lv_h_net")[:, None]   # U1: weight of the network's share
        self.Uc = torch.zeros(N, device=dev); self.Mt = f("lv_M").clone()
        self.fnode = f("lv_fnode")[:, None] if self.u1_crack else 1.0
        self.Kc = torch.ones(N, A, device=dev)        # centralized compute stock relative to the no-lever path
        self.Llost = z.clone()                        # output destroyed by bans, not yet re-absorbed (share of bloc output)
        self.base = torch.ones(N, A, device=dev)      # elite fiscal base relative to the no-lever path
        self.rep = z.clone()                          # elite-built replacement of the network's core-chain share
        self.Dce = torch.ones(N, A, device=dev); self.ac = z.clone(); self.phie = z.clone(); self.wdv = z.clone()
        self.nbd = z.clone(); self.nbd10 = z.clone()
        if self.L8:
            self.rho = f("lv_rho0") * self.m8r / self.m8c
        if self.L9:
            self.rho = self.rho * f("lv_rec9")
        self.cap = z.clone()                          # L6 capture depth
        self.mob = z.clone()                          # L4/L7 withdrawal intensity
        self.shock = z.clone()                        # L6 ban supply-chain shock to centralized revenue
        self.Rb = torch.ones(N, A, device=dev); self.Kb = torch.ones(N, A, device=dev); self.fI = torch.ones(N, A, device=dev)
        self.cfb = torch.ones(N, A, device=dev); self.cfw = torch.ones(N, device=dev); self.dln = torch.zeros(N, device=dev)
        self.debt = torch.zeros(N, device=dev); self.Lprev = torch.zeros(N, device=dev); self.Ldef = torch.zeros(N, device=dev)
        self.tl = torch.zeros(N, device=dev); self.Dc = torch.ones(N, A, device=dev); self.hsa = torch.ones(N, A, device=dev)
        self.s_b = z.clone()
        self.nban = z.clone(); self.ncap = z.clone(); self.free4 = None; self.ch4 = torch.full((N, A), -1, dtype=torch.long, device=dev)
        self.rec = {k: [] for k in ["a", "phi", "prot", "sup", "E", "cov", "s", "R", "fI", "cap", "mob", "phie", "wd", "base",
                                    "ac", "Dce", "Kc"]}
        self.rec_c = []; self.rec_t = []; self.rec_Ldef = []; self.rec_cfw = []; self.rec_Mt = []

    def rnd(self, *shape):
        x = self.t_.rand((self.nb,) + shape, generator=self.g, device=self.dev)
        return x if self.reps == 1 else x.repeat((self.reps,) + (1,) * len(shape))

    def _p_odds(self, p, rrr):
        o = p / (1 - p) * rrr
        return o / (1 + o)

    def step(self, t, free, Ddem, t_closed, omega, Dc, choice):
        torch = self.t_; P = self.P; DT = self.DT; f = lambda k: P[k].float()
        self.Dc = Dc
        frac = torch.clamp((t - self.T0) / (self.Yb - self.T0), 0, 1)
        a_t = torch.sigmoid(self.lg0 + (self.lgX - self.lg0) * frac)
        rho = self.rho[:, None].expand(self.N, self.A)
        if self.rho_cl_on:
            # closed autocratic bloc: the regime controls energy, compute and land; no Falun-Gong-style recovery
            rho = torch.where(free & (t >= t_closed), f("lv_rho_cl")[:, None], rho)
        self.sup = self.sup + rho * (1 - self.sup) * DT
        if self.L6:      # capture reversal (courts, repeal); faster with fast collective response (L8)
            rcap = torch.where(free, f("lv_rcap_aut")[:, None], f("lv_rcap_dem")[:, None])
            if self.L8:
                rcap = rcap * (1 + self.a * (self.m8r[:, None] - 1))
            self.cap = self.cap * torch.exp(-rcap * DT)
        a = a_t * self.sup
        enc = f("lv_enc")[:, None]
        E = enc * a * self.enc_alive
        crack = self.sw["crack"] > 0
        ev_enc = torch.zeros_like(crack.expand_as(a))
        if bool((enc > 0).any()):
            newvis = (E > 1e-3) & ~self.vis_done
            u = self.rnd(self.A)
            claim = newvis & (u < (f("lv_p_sc") * f("lv_p_ss"))[:, None]) & crack
            self.t_sup = torch.where(claim, t + f("lv_lag_ss")[:, None], self.t_sup)
            self.vis_done = self.vis_done | newvis
            ev_enc = (self.enc_alive > 0) & (t >= self.t_sup)
            self.enc_alive = torch.where(ev_enc, 0.0, self.enc_alive)
            self.t_encsup = torch.where(ev_enc & torch.isinf(self.t_encsup), t, self.t_encsup)
            self.t_sup = torch.where(ev_enc, float("inf"), self.t_sup)
            E = enc * a * self.enc_alive
        aw = (a * omega).sum(1)
        self.U = self.U + torch.clamp(aw / 0.1, max=1.0) * DT
        self.c = f("lv_cmax") * (1 - torch.exp(-self.U / f("lv_tau")))
        if self.u4:      # U4: reuse of beaten paths compounds the relative advantage on covered tasks
            self.Uc = self.Uc + torch.clamp(aw / 0.1, max=1.0) * (self.c / f("lv_cmax")) * DT
            self.Mt = torch.minimum(f("lv_M") * torch.exp(f("lv_g4") * self.Uc), torch.maximum(f("lv_M"), 1 / f("lv_amort")))
        smax = torch.clamp(f("lv_s_max") * self.s_mult, max=0.9)
        s_b = smax[:, None] * torch.clamp(a / 0.5, max=1.0)
        s_w = smax * torch.clamp(aw / 0.5, max=1.0)
        if self.L1:
            # L1: the token economy pulls hardware in proportion to activity; centralized compute shrinks with its capex (L2)
            kc = f("lv_kc")
            if self.r3_kstock:
                # round 3: centralized compute is a STOCK (existing GPUs keep running); state-owned compute (A3) exempt
                st = f("lv_st")
                cfb = st[:, None] + (1 - st[:, None]) * self.Kc
                cfw = st + (1 - st) * (self.Kc * omega).sum(1)
            else:
                cfb = self.cfb if self.L2 else torch.ones_like(self.cfb)
                cfw = self.cfw if self.L2 else torch.ones_like(self.cfw)
            s_b = torch.clamp(torch.maximum(s_b, kc[:, None] * a / (kc[:, None] * a + cfb)), max=0.9)
            s_w = torch.clamp(torch.maximum(s_w, kc * aw / (kc * aw + cfw)), max=0.9)
        self.s_b = s_b; self.s_w = s_w
        # providers are ~90% US-based: cut on US or China closure or a US crackdown (review: not on a Chinese crackdown)
        cutnow = (t >= t_closed[:, 0]) | (t >= t_closed[:, 1]) | (self.ncr[:, 0] > 0)
        self.t_cut = torch.where(torch.isinf(self.t_cut) & cutnow, t, self.t_cut)
        cut = torch.isfinite(self.t_cut)
        lag_c = torch.where(P["lv_oc"], f("lv_lag_pre") + f("lv_dlag_oc"),
                            torch.maximum(f("lv_lag_pre"), f("lv_L27") * torch.log10((1 - s_w) / torch.clamp(s_w, min=1e-9))))
        lag_tgt = torch.where(cut, lag_c, f("lv_lag_pre"))
        self.lag = self.lag + (lag_tgt - self.lag) * min(DT / 1.0, 1.0)
        fn = 10 ** (-self.lag / f("lv_L27"))
        effc = f("lv_E")[:, None] * s_b * (self.c * self.Mt + (1 - self.c) * fn)[:, None]
        phi = torch.where(s_b > 0, effc / (effc + 1 - s_b), 0.0)
        # audit round 4 (L3): the network's share of the civilian capability a repression order runs on (logistics,
        # energy, comms) is at least its share of economic activity, not only its frontier-capability share
        phir = torch.maximum(phi, a) if self.r4_ref else phi
        if self.L6:      # a captured network's refusal and control capacity is subordinated to the state
            self.phi = phir * (1 - self.cap) * self.sw["ch_ref"]; self.n = s_b * (1 - self.cap) * self.sw["ch_ctl"]
        else:
            self.phi = phir * self.sw["ch_ref"]; self.n = s_b * self.sw["ch_ctl"]
        if self.r3_ref:  # round 3: refusal binds only on the part of the order's execution the network supplies (A3 exempt)
            self.phi = self.phi * f("lv_dnet")[:, None]
        self.phie = self.phi
        self.phi_raw = phi
        # soft power (foreign publics' favourability x their remaining leverage over their own governments)
        if self.levD is not None:
            Lr = torch.clamp(self.levD / self.lref, 0, 1)
            grow = (float(np.log(2.0)) / f("lv_Ty"))[:, None] * (1 - self.fav) * torch.clamp(a / 0.01, max=1.0) \
                * torch.where(free, 1 - f("lv_cut")[:, None], 1.0) * DT
            self.fav = torch.clamp(self.fav + grow, 0, 1)
            W = omega[:, None, :] * (1 - self.eye)
            S = (W * (self.fav * Lr ** f("lv_e")[:, None])[:, None, :]).sum(-1) / torch.clamp(W.sum(-1), min=1e-9)
            self.prot = self.R * S * self.sw["ch_soft"]; self.sevr = f("lv_sev")[:, None] * S * self.sw["ch_soft"]
        # crackdown
        h0 = torch.where(free, f("lv_h0_aut")[:, None], f("lv_h0_dem")[:, None])
        thr = torch.where(free, f("lv_thr_aut")[:, None], f("lv_thr_dem")[:, None])
        above = a > thr
        if self.crack_perm:      # pre-review form: permanent, re-firing above-threshold hazard; size scaling extrapolated
            h = torch.minimum(h0 * (torch.clamp(a, min=A_REF) / A_REF) ** f("lv_k")[:, None], self.h_thr[:, None])
            h = torch.where(above, self.h_thr[:, None].expand_as(h), h)
        else:
            if self.free_prev is None:
                self.free_prev = free.clone()
            newc = above & (~self.above_prev | (free != self.free_prev))
            self.win_until = torch.where(newc, t + f("lv_T_thr")[:, None], self.win_until)
            hb = torch.minimum(h0 * (torch.clamp(a, min=A_REF, max=10 * A_REF) / A_REF) ** f("lv_k")[:, None], self.h_thr[:, None])
            h = torch.where(above & (t < self.win_until), self.h_thr[:, None].expand_as(hb), hb)
        h = h * (1 + (f("lv_V")[:, None] - 1) * enc * (self.enc_alive > 0).float())
        h = h * (1 - self.prot)
        if self.L6:      # a subordinated network is not cracked down on again while it stays captured (returns as it decays)
            h = h * torch.clamp(1 - self.cap / f("lv_kap")[:, None], 0, 1)
        ev = (self.rnd(self.A) < 1 - torch.exp(-h * DT)) & crack
        if self.L6:
            # L6: crackdown FORM shifts with size (ban -> capture/regulate); incidence is not reduced
            pc = f("lv_pcm")[:, None] * torch.clamp((a - 0.05) / 0.10, 0, 1)
            if self.r3_ban:
                # round 3: a ban's anticipated self-inflicted loss tilts the form toward capture/regulation, and a
                # democracy does not ban a network its voters carry (a >= a_vote)
                loss = f("lv_eff")[:, None] * self.fnode * a * f("lv_dm")[:, None]
                pban = (1 - pc) * torch.exp(-f("lv_kcost")[:, None] * loss)
                pban = torch.where(free, pban, pban * torch.clamp(1 - a / f("lv_avote")[:, None], 0, 1))
                pc = 1 - pban
            capt = ev & (self.rnd(self.A) < pc)
            ban = (ev & ~capt) | ev_enc
        else:
            capt = torch.zeros_like(ev); ban = ev | ev_enc
        ev = ev | ev_enc
        eff = f("lv_eff")[:, None] * (1 - self.sevr) * self.fnode     # U1: only hardware/connection removal stops activity
        if self.L9:
            # L9: backfire (mean ~0) and defections of the human-staffed share of enforcement (odds of resisting x RRR)
            wpart = torch.clamp(a / 0.035, max=1.0) if self.r3_l9 else 1.0       # 3.5% participation rule
            rrr = 1 + (f("lv_defup")[:, None] - 1) * self.pdoc[:, None] * self.hsa * wpart
            p_res = self._p_odds(P_SUC9, rrr)
            eff = eff * (1 - f("lv_bf")[:, None]) * (1 - p_res) / (1 - P_SUC9)
        sup_old = self.sup
        self.sup = torch.where(ban, self.sup * (1 - eff), self.sup)
        if self.L6:
            self.sup = torch.where(capt, self.sup * (1 - f("lv_eff_cap")[:, None]), self.sup)
            self.cap = torch.where(capt, torch.maximum(self.cap, f("lv_kap")[:, None]), self.cap)
            da = a_t * (sup_old - self.sup)
            if self.r3_rb:   # round 3: the part that does not migrate back is lost output (re-absorbed over T_re)
                self.Llost = self.Llost * torch.exp(-DT / f("lv_Tre"))[:, None] + torch.where(
                    ban, (1 - f("lv_mig")[:, None]) * da, 0.0)
            else:
                self.shock = self.shock * float(np.exp(-DT)) + torch.where(
                    ban, (f("lv_dm")[:, None] - 1) * da / torch.clamp(1 - a, min=0.05), 0.0)
        self.ncr = self.ncr + ev.float(); self.tcr1 = torch.where(ev & torch.isinf(self.tcr1), t, self.tcr1)
        self.nban = self.nban + ban.float(); self.ncap = self.ncap + capt.float()
        self.nbd = self.nbd + (ban & ~free).float(); self.nbd10 = self.nbd10 + (ban & ~free & (a > 0.1)).float()
        self.fav = torch.where(ev, torch.clamp(self.fav - f("lv_rev")[:, None], min=0), self.fav)
        a = a_t * self.sup
        if not self.crack_perm:
            self.win_until = torch.where(ev, -float("inf"), self.win_until)
            self.above_prev = a > thr; self.free_prev = free.clone()
        self.a = a; self.E = enc * a * self.enc_alive
        self.a_c = torch.minimum(a, phi) if self.capphi else a
        # ---- L4/L7 withdrawal episodes, L2 revenue and capex, L5 talent
        if self.free4 is None:
            self.free4 = free.clone()
        # round 3: a capture (the network subordinated) does not trigger a boycott organised by that network
        evw = ban if self.r3_cap else ev
        trig = evw | (free & ~self.free4) | ((choice >= GEN.I_WH) & (choice != self.ch4))
        self.free4 = free.clone(); self.ch4 = choice.clone()
        if self.L4 or self.L7:
            pers = f("lv_pers") * (self.dur if self.L8 else 1.0)
            self.mob = torch.where(trig, 1.0, self.mob * (pers ** (DT / 2.0))[:, None])
        ka = (1 - self.cap) if self.r3_cap else 1.0          # captured share cannot be mobilised
        # round 3: participants can only withdraw substitutable household spending (consumption ~0.6 of output x sub)
        self.wcap = f("lv_l4")[:, None] * ((0.6 * f("lv_sub"))[:, None] if self.r3_wd else 1.0)
        wd = torch.zeros_like(a)
        if self.L4:
            wd = wd + self.wcap * a * ka * self.mob
        if self.L7w:
            Wo = omega[:, None, :] * (1 - self.eye)
            Sout = (Wo * (a * ka)[:, None, :]).sum(-1) / torch.clamp(Wo.sum(-1), min=1e-9)
            wd = wd + f("lv_l4")[:, None] * f("lv_xs")[:, None] * Sout * self.mob * (f("lv_sub")[:, None] if self.r3_wd else 1.0)
        self.wdv = wd
        if self.r3_rb:
            # round 3: the network buys hardware/energy from centralized suppliers; banned output that did not migrate back
            # is lost (x dm through the supply chain)
            dm = f("lv_dm")[:, None]
            self.Rb = torch.clamp((1 - a - dm * self.Llost) * (1 - torch.clamp(wd, 0, 0.95))
                                  + a * self._buy() * f("lv_psic")[:, None], min=0.02)
        else:
            self.Rb = (1 - a) * (1 - torch.clamp(wd + self.shock, 0, 0.95))
        if self.r3_base:     # elite fiscal base: untaxed network activity and lost output are outside it
            self.base = torch.clamp(1 - a * (1 - f("lv_tax")[:, None]) - f("lv_dm")[:, None] * self.Llost, min=0.05)
        if self.L2:
            lagc = f("lv_lag_cx")
            Rw = (self.Rb * omega).sum(1)
            cfw_new = self.cfw + (Rw ** f("lv_eps_lab") - self.cfw) * torch.clamp(DT / lagc, max=1.0)
            self.dln = torch.log(cfw_new) - torch.log(self.cfw); self.cfw = cfw_new
            self.cfb = self.cfb + (self.Rb ** f("lv_eps_lab")[:, None] - self.cfb) * torch.clamp(DT / lagc, max=1.0)[:, None]
            self.Kb = self.Kb + (self.Rb - self.Kb) * P["i_K"].float()[:, None] * DT
            self.fI = torch.clamp((self.Rb / self.Kb) ** f("lv_eps_hyp")[:, None], 0.2, 1.5)
            if self.r3_kstock:
                # compute stock: dK/dt = (g + delta) (I/I0 - K); labs fund from world revenue, the rest from bloc revenue
                Rw = (self.Rb * omega).sum(1)
                wl = f("lv_wlab")[:, None]
                Irel = wl * (Rw ** f("lv_eps_lab"))[:, None] + (1 - wl) * self.Rb ** f("lv_eps_hyp")[:, None]
                self.Kc = self.Kc + (f("lv_gc") + f("lv_dep"))[:, None] * (Irel - self.Kc) * DT
        if self.L5:
            mvd = f("lv_mv") * torch.clamp(a[:, 0] / 0.5, 0, 1)
            self.tl = torch.maximum(mvd, self.s_w) if self.r3_l5 else mvd
        # round 3: participant-controlled share of the core chain in the closure test; the elite duplicates it at its
        # (revenue-limited) investment rate, and capture or a ban removes it
        if self.core:
            ac_raw = a * f("lv_kphys")[:, None] * ((1 - self.cap) if self.L6 else 1.0)
            self.rep = self.rep + P["i_K"].float()[:, None] * self.fI * torch.clamp(ac_raw - self.rep, min=0) * DT
            self.ac = torch.clamp(ac_raw - self.rep, min=0)
            self.Dce = Dc * (1 - self.ac) + self.ac * self.hw
        else:
            self.Dce = Dc
        if abs(t % 1.0) < 1e-9:
            for k, v in [("a", a), ("phi", phi), ("prot", self.prot), ("sup", self.sup), ("E", self.E), ("cov", self.cov),
                         ("s", s_b), ("R", self.Rb), ("fI", self.fI), ("cap", self.cap), ("mob", self.mob), ("phie", self.phie),
                         ("wd", self.wdv), ("base", self.base), ("ac", self.ac), ("Dce", self.Dce), ("Kc", self.Kc)]:
                self.rec[k].append(v.clone())
            self.rec_c.append(self.c.clone()); self.rec_Ldef.append(self.Ldef.clone()); self.rec_cfw.append(self.cfw.clone())
            if self.u4:
                self.rec_Mt.append(self.Mt.clone())

    def _buy(self):
        """network spending on centralized suppliers per unit of activity (before the psi_c split)"""
        # U2: the hardware/energy bill kc ccs plus treasury spending of the service fees (1 - y_h)(1 - kc ccs) = 1 - yh_gross
        return 1 - self.yh

    # ---- round 2 hooks
    def capL(self, L, rate, s_rnd, Lcap):
        """L2 capex debt and L5 talent drain on the centralized capability (doublings of the task horizon). Capability
        never regresses: the shortfall is taken out of this step's progress; catch-up at most 1x the rate."""
        torch = self.t_; DT = self.DT; f = lambda k: self.P[k].float()
        if not (self.L2 or self.L5):
            self.Lprev = L
            return L
        inc = L - self.Lprev
        tal = (1 - self.tl) ** (f("lv_el5") * (1 - s_rnd)) if self.L5 else torch.ones_like(L)
        ti = inc * tal
        if self.L2:
            self.debt = self.debt - self.dln * rate / f("lv_g_eff")
            self.dln = torch.zeros_like(self.dln)
            pay = torch.minimum(torch.maximum(self.debt, -rate * DT), ti)
            self.debt = self.debt - pay
        else:
            pay = torch.zeros_like(L)
        Ln = torch.minimum(self.Lprev + ti - pay, Lcap)
        Ln = torch.maximum(Ln, torch.minimum(self.Lprev, Lcap))
        self.Ldef = self.Ldef + (L - Ln)
        self.Lprev = Ln
        return Ln

    def inv(self, g_full, g_core, cap_f, cap_c):
        """L2: investment rate of centralized firms x (R/K)^eps_hyp; security automation (state, A3) exempt"""
        if not self.L2:
            return g_full, g_core, cap_f, cap_c
        fI = self._fIsh()
        m = fI[..., None].expand_as(cap_f).clone(); m[:, :, 7] = 1.0
        return g_full * m, g_core * m, cap_f * m, cap_c * m

    def _fIsh(self):
        """round 3: only the centralized share (1 - a) of investment demand slows; the network's own demand for
        automation (it uses robots too) continues at the bloc's pace"""
        return (1 - self.a) * self.fI + self.a if self.r3_inv else self.fI

    def inv1(self, g):
        return g * self._fIsh() if self.L2 else g

    def dcfix(self, Dc):
        return self.Dce if self.core else Dc

    def tcore_D(self, Dc):
        return self.Dce if self.r4_tcore else Dc

    def dmult(self):
        """L8/L9 multiplier on the public's democratic recovery and redemocratisation hazards"""
        m = self.t_.ones_like(self.a)
        if self.L8:
            m = m * (1 + self.a * (self.m8r[:, None] - 1))
        if self.L9:
            f = lambda k: self.P[k].float()
            rrr = 1 + (f("lv_defup")[:, None] - 1) * self.pdoc[:, None] * self.hsa * self.a
            m = m * self._p_odds(P_SUC9, rrr) / P_SUC9
        return m

    def press(self, pi, E0t, fac_e, omega, willing, imp_dep, b3):
        """L7: the network's weight in each outside economy joins that economy's outside pressure (still scaled by the
        outsider's enforceability, B3)"""
        if not self.L7p:
            return pi
        torch = self.t_
        add = torch.clamp(self.a * self.P["lv_l4"].float()[:, None], 0, 1)
        if self.L6:
            add = add * (1 - self.cap)
        if self.r3_gate7:
            # round 3: economic weight in an outside bloc moves that bloc's policy only through its public's remaining
            # leverage over its own government (as C5); an autocratic, automated outsider is not steered by its customers
            if self.levD is None:
                return pi
            Lr = torch.clamp(self.levD / self.lref, 0, 1)
            add = add * Lr ** self.P["lv_e"].float()[:, None]
        w2 = willing + (1 - willing) * add
        enf2 = (fac_e * (omega * w2)[:, None, :]).sum(-1)
        pi2 = E0t[:, None] * enf2 * (0.3 + 0.7 * torch.clamp(imp_dep / 0.2, 0, 1))
        return torch.where(b3, pi2, pi)

    # ---- round 1 hooks (L4 leverage added)
    def lev(self, Lev, Dfd, Ddem):
        ka = (1 - self.cap) if self.r3_cap else 1.0
        Lev = Lev + self.sw["ch_lev"] * 0.5 * (1 - Dfd) * self.a_c * ka * self.hw
        if self.L4:      # customer leverage before closure (fades with core-chain closure, incl. the network's share)
            Lev = Lev + 0.5 * self.P["lv_kpol"].float()[:, None] * self.wcap * self.a * ka * torch_clamp01(self.Dce)
        self.levD = Lev * Ddem
        if self.lref is None:
            self.lref = self.t_.clamp(self.levD[:, [0, 2]].mean(1, keepdim=True), min=1e-6)
        return Lev

    def disp(self, d):
        self.ay = self.sw["ch_liv"] * self.a_c * self.yh
        if self.liv_disp:        # pre-review form: network income counted as new human work (upper sensitivity)
            return self.t_.clamp(d - self.ay, min=0)
        return d

    def dep(self, dep, chW, disp_eff, Dfd):
        torch = self.t_
        if self.liv_disp:
            dep = torch.where(chW, torch.maximum(disp_eff, torch.clamp(1 - Dfd - self.ay, min=0)), dep)
        return dep * (1 - self.E)

    def prov(self, Pv, disp, choice, decided, t, t_closed):
        """C4 main form: network income is income, not work. It covers a share cov = a*y_h of the displaced public's need
        (average-share breadth); means-tested state provision is clawed back at rate claw; the total is capped at full
        provision. Under a lethal choice (neglect, depopulation) the state strangles land/energy/food, so only s_acc survives."""
        torch = self.t_
        if self.liv_disp:
            self.cov = torch.zeros_like(Pv)
            return Pv
        if self.cov_conc:        # pre-audit form: all network income reaches the displaced (upper sensitivity)
            cov = torch.clamp(self.ay / torch.clamp(disp, min=1e-6), 0, 1)
        elif self.r4_need and self.G is not None:
            # audit round 4: a displaced person gets a*y_h of average income per person; full (decent) provision costs
            # m0/G of output per person (the m8 'serve' cost), so the share of need covered is a*y_h*G/m0
            cov = torch.clamp(self.ay * (self.G if self.need_G else 1.0) / self.P["m0"].float()[:, None], 0, 1)
        else:                    # round-3 form: need taken as average income (cov = a*y_h)
            cov = torch.clamp(self.ay, 0, 1)
        self.cov = cov
        hostile = (t >= t_closed) if self.gate_closure else (decided & (choice >= GEN.I_NEG))
        cg = cov * torch.where(hostile, self.sacc, 1.0)
        claw = self.P["lv_claw"].float()[:, None]
        return torch.clamp(torch.clamp(Pv - claw * cg, min=0) + cg, max=1.0)

    def cost(self, cost, Psq):
        """C4 cost link: a regime that keeps people (serve, rentier, status quo, warehouse) tops up network income to the
        option's provision target, so its bill falls by claw*cov/target. Neglect and depopulation costs unchanged."""
        torch = self.t_
        if not (self.liv_disp or not self.cost_link):
            tgt = torch.stack([torch.ones_like(Psq), torch.ones_like(Psq), torch.clamp(Psq, min=0.02), 0.6 * torch.ones_like(Psq)], -1)
            fac = torch.clamp(1 - (self.P["lv_claw"].float()[:, None] * self.cov)[..., None] / tgt, 0, 1)
            cost = torch.cat([cost[..., :4] * fac, cost[..., 4:]], -1)
        if self.r3_base:
            # round 3: every option is paid out of the elite's fiscal base, which untaxed network activity shrinks
            cost = cost / self.base[..., None]
        return cost

    def neg(self, r):
        c = self.cov if (self.r4_need and not self.liv_disp) else self.ay
        return r * (1 - c * self.sacc) * (1 - self.E)

    def seed(self, th):
        return th * (1 + self.P["lv_k_seed"].float()[:, None] * self.t_.clamp(self.E, max=0.1) / 0.01)

    def ctl(self, cw):
        # round 3: the network holds no coercive force (no kinetic role; security automation is state-owned, A3), so C2
        # acts only on the economic power-grab hazard
        return cw if self.r3_ctl else cw * (1 - self.n)[..., None]

    def grab(self, inc, h_sa):
        self.hsa = h_sa
        return inc * (1 - self.n)

    def refuse(self, c_req):
        u = self.rnd(self.A)
        return self.t_.where(self.thr_mode, self.phi > (1 - c_req.float())[:, None], u < self.phi)

    def block_c(self, lcp, c_req):
        b = lcp & self.refuse(c_req)
        self.nbc = self.nbc + b.float()
        return lcp & ~b

    def block_xb(self, elig, c_req):
        r = self.refuse(c_req)
        self.nbxb = self.nbxb + (elig.any(2) & r).float()
        return elig & ~r[:, :, None]

    def note_block_x(self, nfX):
        self.nbx = self.nbx + nfX.float()

    def slow(self, hx):
        return self.t_.where(self.thr_mode, hx, hx * (1 - self.phi))

    def slow_xb(self, hxb, byc):
        return self.t_.where(self.thr_mode, hxb, hxb * (1 - self.phi.gather(1, byc)))

    def outputs(self):
        torch = self.t_
        o = {"lv_" + k: torch.stack(v, -1) for k, v in self.rec.items()}
        if self.rec_Mt:
            o["lv_Mt"] = torch.stack(self.rec_Mt, -1)
        o["lv_c"] = torch.stack(self.rec_c, -1); o["lv_Ldef"] = torch.stack(self.rec_Ldef, -1); o["lv_cfw"] = torch.stack(self.rec_cfw, -1)
        o.update(lv_ncr=self.ncr, lv_tcr1=self.tcr1, lv_tcut=self.t_cut, lv_nbx=self.nbx, lv_nbc=self.nbc, lv_nbxb=self.nbxb,
                 lv_tencsup=self.t_encsup, lv_nban=self.nban, lv_ncap=self.ncap, lv_nbd=self.nbd, lv_nbd10=self.nbd10)
        return o


def torch_clamp01(x):
    return x.clamp(0, 1)


# ============================================================================================
# 4. pipeline: patched m8 inside the unchanged integrator
# ============================================================================================
GEN = None
IV = None
STASH = []
KEEP = ["t_closed", "t_first_dec", "free_at_dec", "first_choice", "t_X"]


def setup():
    global GEN, IV
    GEN = build_patched()
    import integrate_v4 as iv
    IV = iv
    GEN.T_END = 2076.0
    GEN.NSTEP = int(round((GEN.T_END - GEN.T0) / GEN.DT))
    GEN.YEARS = np.arange(2027, 2077)
    GEN.LEVER_STATE_CLS = LeverState
    GEN.LEVER_SAMPLER = sample_lever
    base_sim = GEN.simulate

    def sim_stash(*a, **k):
        o = base_sim(*a, **k)
        STASH.append({kk: v for kk, v in o.items() if kk.startswith("lv_") or kk in KEEP})
        return o
    GEN.simulate = sim_stash
    IV.M8 = GEN
    return GEN, IV


def run_cell(cfg, NO, R8=8, NI=200):
    """cfg None = lever off (baseline). Returns metrics, per-draw arrays and the m8 lever stash (baseline world)."""
    GEN.LEVER_CFG = None if cfg is None else dict(DEFAULT_CFG, **cfg)
    STASH.clear()
    D8 = IV.run_m8(NO, R8, "baseline")
    st = STASH[0]
    pe_lv = sample_lever(NO, None, GEN.LEVER_CFG) if cfg is not None else None
    sim = IV.simulate(IV.BASE_CFG, D8, NI, IV.SEED)
    H = IV.headline(sim); X = sim["extras"]; R = sim["R"]
    cls = IV.outcome_class(sim, H); cls_UC = cls[:, [0, 1]].min(1)
    inds = dict(nt_UC=H["nt_UC"], nt_world=H["nt_world"], nt_any=H["nt_any"], keep_UC=cls_UC == 6, s5d_UC=H["s5d_UC"],
                keep_US=cls[:, 0] == 6, keep_EU=cls[:, 2] == 6,
                nt_US=np.isfinite(X["TLd"][:, 0, 3]), nt_CN=np.isfinite(X["TLd"][:, 1, 3]),
                disemp_UC=H["disemp_UC"])
    m = {}; pdd = {}
    for k, ind in inds.items():
        s, pd_ = IV.stats(sim, ind)
        m[k] = dict(mean=s["mean"], mc_ci95=s["mc_ci95_bootstrap"], epistemic_ci95_denoised=s["epistemic_ci95_denoised"])
        pdd[k] = pd_
    m["nt_UC_by_year"] = {str(y): round(float(np.mean(R["loss>=0.999 deliberate US_or_China"] < y + 1)), 5)
                          for y in [2035, 2040, 2045, 2050, 2060, 2075]}
    m["world_loss_mean"] = round(float(X["world_loss"].mean()), 5)
    return m, pdd, st, pe_lv, D8


def paired_delta(pd_a, pd_b, B=2000, seed=11):
    rng = np.random.default_rng(seed)
    d = pd_a - pd_b; n = len(d)
    bs = d[rng.integers(0, n, (B, n))].mean(1)
    return dict(delta=round(float(d.mean()), 5), ci95=[round(float(np.quantile(bs, .025)), 5), round(float(np.quantile(bs, .975)), 5)])


def closure_delay(st, st_b):
    """paired (common random numbers) change in the first closure time t_closed per bloc vs the baseline world"""
    out = {}
    if st_b is None or "t_closed" not in st_b:
        return out
    for b, nm in [(0, "US"), (1, "China"), (2, "Europe")]:
        tl = np.minimum(st["t_closed"][:, b], 2076.0); tb = np.minimum(st_b["t_closed"][:, b], 2076.0)
        both = (tl < 2076) & (tb < 2076)
        out[nm] = dict(mean_shift_years_capped2076=round(float((tl - tb).mean()), 3),
                       median_shift_years_if_closed_in_both=round(float(np.median((tl - tb)[both])), 3) if both.any() else None,
                       mean_shift_years_if_closed_in_both=round(float((tl - tb)[both].mean()), 3) if both.any() else None,
                       P_closed_by={str(y): [round(float(np.mean(tb < y + 1)), 4), round(float(np.mean(tl < y + 1)), 4)]
                                    for y in [2030, 2035, 2040, 2050]},
                       note="P_closed_by: [baseline, lever]")
    return out


def lever_diag(st, pe, cfg, st_b=None):
    """diagnostics from the m8 baseline-world stash (NO*R8 runs)"""
    yrs = np.arange(2027, 2027 + st["lv_a"].shape[-1])
    a = st["lv_a"]; tcr = st["lv_tcr1"]; ncr = st["lv_ncr"]
    NR = a.shape[0]; R8 = NR // len(pe["lv_X"])
    rep = lambda x: np.repeat(x, R8, axis=0)
    Y = cfg["Y"]
    iy = lambda y: int(np.clip(y - 2027, 0, len(yrs) - 1))
    out = {}
    for b, nm in [(0, "US"), (1, "China"), (2, "Europe")]:
        out[nm] = dict(
            target_adoption_at_Y=round(float(cfg["X"] * (1.0 if (b in (0, 2) or cfg.get("uniform")) else rep(pe["lv_r"])[:, b].mean())), 4),
            realised_adoption_mean_at_Y=round(float(a[:, b, iy(Y)].mean()), 4),
            realised_adoption_mean_2050=round(float(a[:, b, iy(2050)].mean()), 4),
            P_first_crackdown_by={str(y): round(float(np.mean(tcr[:, b] < y + 1)), 4) for y in [2030, 2035, 2040, 2050, 2075]},
            mean_crackdowns_by_2076=round(float(ncr[:, b].mean()), 3),
            mean_bans_by_2076=round(float(st["lv_nban"][:, b].mean()), 3),
            mean_captures_by_2076=round(float(st["lv_ncap"][:, b].mean()), 3),
            capture_depth_mean_2040=round(float(st["lv_cap"][:, b, iy(2040)].mean()), 4),
            compute_share_mean_at_Y=round(float(st["lv_s"][:, b, iy(Y)].mean()), 4),
            centralized_revenue_factor_mean_at_Y=round(float(st["lv_R"][:, b, iy(Y)].mean()), 4),
            investment_factor_fI_mean_at_Y=round(float(st["lv_fI"][:, b, iy(Y)].mean()), 4),
            investment_factor_fI_min_mean=round(float(st["lv_fI"][:, b].min(-1).mean()), 4),
            withdrawal_active_share_2040=round(float((st["lv_mob"][:, b, iy(2040)] > 0.5).mean()), 4),
            phi_mean_at_Y=round(float(st["lv_phi"][:, b, iy(Y)].mean()), 4),
            phi_effective_mean_at_Y=round(float(st["lv_phie"][:, b, iy(Y)].mean()), 4),
            withdrawal_revenue_loss_mean_at_Y=round(float(st["lv_wd"][:, b, iy(Y)].mean()), 4),
            withdrawal_revenue_loss_mean_2040=round(float(st["lv_wd"][:, b, iy(2040)].mean()), 4),
            elite_fiscal_base_mean_at_Y=round(float(st["lv_base"][:, b, iy(Y)].mean()), 4),
            core_chain_network_share_mean={str(y): round(float(st["lv_ac"][:, b, iy(y)].mean()), 4) for y in [2035, 2040, 2050]},
            centralized_compute_stock_mean_at_Y=round(float(st["lv_Kc"][:, b, iy(Y)].mean()), 4),
            mean_bans_while_democratic=round(float(st["lv_nbd"][:, b].mean()), 3),
            mean_bans_while_democratic_a_gt_10pct=round(float(st["lv_nbd10"][:, b].mean()), 3),
            phi_p90_at_Y=round(float(np.quantile(st["lv_phi"][:, b, iy(Y)], .9)), 4),
            soft_protection_mean_at_Y=round(float(st["lv_prot"][:, b, iy(Y)].mean()), 4),
            soft_protection_mean_2040=round(float(st["lv_prot"][:, b, iy(2040)].mean()), 4),
            P_refusal_blocked_depop_order=round(float(np.mean(st["lv_nbx"][:, b] > 0)), 4),
            P_refusal_blocked_coll_punishment=round(float(np.mean(st["lv_nbc"][:, b] > 0)), 4),
            P_enclaves_suppressed=round(float(np.mean(np.isfinite(st["lv_tencsup"][:, b]))), 4),
            C4_cover_of_displaced_need_mean_at_Y=round(float(st["lv_cov"][:, b, iy(Y)].mean()), 4),
            C4_cover_mean_2050=round(float(st["lv_cov"][:, b, iy(2050)].mean()), 4))
    out["P_frontier_cut_by"] = {str(y): round(float(np.mean(st["lv_tcut"] < y + 1)), 4) for y in [2030, 2035, 2040, 2050]}
    out["coverage_mean_2035"] = round(float(st["lv_c"][:, iy(2035)].mean()), 4)
    if "lv_Mt" in st:
        out["U4_amortization_advantage_mean"] = {str(y): round(float(st["lv_Mt"][:, iy(y)].mean()), 4) for y in [2030, 2035, 2040, 2050, 2075]}
    out["capability_deficit_doublings"] = {str(y): round(float(st["lv_Ldef"][:, iy(y)].mean()), 4) for y in [2030, 2035, 2040, 2050]}
    out["frontier_capex_factor_mean"] = {str(y): round(float(st["lv_cfw"][:, iy(y)].mean()), 4) for y in [2030, 2035, 2040, 2050]}
    out["closure_delay"] = closure_delay(st, st_b)
    out["curves"] = dict(years=yrs.tolist(),
                         a_mean={nm: a[:, b].mean(0).round(5).tolist() for b, nm in [(0, "US"), (1, "China"), (2, "Europe")]},
                         P_crackdown_cum={nm: [round(float(np.mean(tcr[:, b] < y + 1)), 4) for y in yrs] for b, nm in [(0, "US"), (1, "China"), (2, "Europe")]})
    return out


def efficiency_bar(st, pe):
    """E needed (innovation efficiency per unit compute vs centralized) for the network's effective capability share to reach
    a bar at the first US/China closure, before frontier access is cut. phi = E s q / (E s q + 1 - s), q = c M + (1 - c) f_pre,
    s = the network's simulated compute share in that bloc at closure (round 2: scales with adoption, L1)."""
    NR = st["lv_a"].shape[0]; R8 = NR // len(pe["lv_X"]); rep = lambda x: np.repeat(x, R8, axis=0)
    tcl = st["t_closed"][:, :2]; first = np.argmin(np.where(np.isfinite(tcl), tcl, 1e9), 1)
    tc = tcl[np.arange(NR), first]; ok = np.isfinite(tc) & (tc < 2076)
    iy = np.clip(np.floor(np.where(ok, tc, 2027)).astype(int) - 2027, 0, st["lv_a"].shape[-1] - 1)
    s = np.minimum(st["lv_s"][np.arange(NR), first, iy], 0.9); c = st["lv_c"][np.arange(NR), iy]
    fpre = 10 ** (-rep(pe["lv_lag_pre"]) / rep(pe["lv_L27"]))
    Mq = st["lv_Mt"][np.arange(NR), iy] if "lv_Mt" in st else rep(pe["lv_M"])     # U4: advantage at closure
    q = c * Mq + (1 - c) * fpre
    E = rep(pe["lv_E"])
    out = {"n_draws_with_closure": int(ok.sum()), "compute_share_at_closure_median": round(float(np.median(s[ok])), 4) if ok.any() else None}
    base = (1 - s) / np.maximum(s * q, 1e-12)
    for nm, phi in [("out_innovate_phi_0.5", 0.5), ("defense_dominant_3x_phi_0.25", 0.25), ("defense_dominant_10x_phi_0.091", 1 / 11)]:
        Es = base * phi / (1 - phi)
        if ok.any():
            out[nm] = dict(E_needed_median=round(float(np.median(Es[ok])), 2), E_needed_p10=round(float(np.quantile(Es[ok], .1)), 2),
                           E_needed_p90=round(float(np.quantile(Es[ok], .9)), 2),
                           P_sampled_E_meets_bar=round(float(np.mean(E[ok] >= Es[ok])), 4))
    return out


# ============================================================================================
# 5. runs
# ============================================================================================
GRID_X = [0.05, 0.10, 0.20, 0.25, 0.50]
GRID_Y = [2028, 2030, 2032, 2035, 2040]
DECOMP_CELLS = [(0.25, 2030), (0.50, 2035)]
L_OFF = {k: False for k in L_SW}
C_OFF = dict(ch_lev=False, ch_ctl=False, ch_ref=False, ch_liv=False, ch_soft=False)
R3_OFF = {k: False for k in R3_SW}
R4_OFF = {k: False for k in R4_SW}
U_OFF = {k: False for k in U_SW}
DECOMP = [
    ("all channels", {}),
    ("all channels, no crackdown risk", dict(crack=False)),
    ("lever round-2 spec (U1-U4 off)", dict(U_OFF)),
    ("all minus U1 autonomy (both parts)", dict(u1_lev=False, u1_crack=False)),
    ("all minus U1 C1/closure weight (h_net back)", dict(u1_lev=False)),
    ("all minus U1 crackdown damage (f_node 1)", dict(u1_crack=False)),
    ("all minus U2 payout (y_h U(0.5,1) capped)", dict(u2_yh=False)),
    ("all minus U3 access (s_acc U(0,0.5))", dict(u3_sacc=False)),
    ("all minus U4 substrate advantage growth", dict(u4_sub=False)),
    ("only U2+U3 (U1, U4 off)", dict(u1_lev=False, u1_crack=False, u4_sub=False)),
    ("S: U1 f_node 0.5 (low end)", dict(ov=dict(lv_fnode=0.5))),
    ("S: U3 s_acc 0.2 (low end)", dict(ov=dict(lv_s_acc4=0.2))),
    ("S: U3 s_acc 0.7 (high end)", dict(ov=dict(lv_s_acc4=0.7))),
    ("S: U4 strong (g4 0.06, cap 10x)", dict(ov=dict(lv_g4=0.06, lv_amort=0.1))),
    ("round-3 pre-audit spec (round-4 fixes off)", dict(R4_OFF, **U_OFF)),
    ("all minus r4 C4 need units (need = average income)", dict(r4_need=False)),
    ("all minus r4 C3 economic-weight share", dict(r4_ref=False)),
    ("all minus r4 closure clock fix", dict(r4_tcore=False)),
    ("S: network income fixed at 2026 output scale (cov = a y_h / m0)", dict(need_G=False)),
    ("S: C4 coverage need = average income and no cost link", dict(r4_need=False, cost_link=False)),
    ("round-2 spec (round-3 fixes off)", dict(R3_OFF, **R4_OFF, **U_OFF, ch_core=False)),
    ("round-1 spec (L1-L9 off)", dict(L_OFF, **R3_OFF, **R4_OFF, **U_OFF)),
    ("all minus core-chain dependence in closure", dict(ch_core=False)),
    ("all minus L1 compute scaling", dict(ch_L1=False)),
    ("all minus L2 revenue/capex", dict(ch_L2=False)),
    ("all minus L4 customer withdrawal", dict(ch_L4=False)),
    ("all minus L5 talent", dict(ch_L5=False)),
    ("all minus L6 crackdown form/cost", dict(ch_L6=False)),
    ("all minus L7 cross-bloc actor", dict(ch_L7=False)),
    ("all minus L7 withdrawal part", dict(L7_wd=False)),
    ("all minus L7 outside-pressure part", dict(L7_press=False)),
    ("all minus L8 organising speed", dict(ch_L8=False)),
    ("all minus L9 legitimacy", dict(ch_L9=False)),
    ("all minus C1 leverage", dict(ch_lev=False)),
    ("all minus C2 control", dict(ch_ctl=False)),
    ("all minus C3 refusal", dict(ch_ref=False)),
    ("all minus C4 livelihoods", dict(ch_liv=False)),
    ("all minus C5 soft power", dict(ch_soft=False)),
    ("closure channels only (L2+L4+L5+core, C1-C5 off)", dict(C_OFF, ch_L1=False, ch_L6=False, ch_L7=False, ch_L8=False, ch_L9=False)),
    ("all minus closure channels (L2, L4, L5, core)", dict(ch_L2=False, ch_L4=False, ch_L5=False, ch_core=False)),
    ("all + enclaves (20% of participants)", dict(enc=0.2)),
    ("all, uniform cross-bloc spread", dict(uniform=True)),
    ("S: refusal as F3 threshold (phi_eff > 1 - c_req)", dict(ref_thr=True)),
    ("S: C3 blocks with P = phi (round-2 form, upper)", dict(r3_ref=False)),
    ("S: C2 also on coercive force (round-2 form, upper)", dict(r3_ctl=False)),
    ("S: C4 welfare only, no provision-cost link", dict(cost_link=False)),
    ("S: network untaxed (tax 0)", dict(ov=dict(lv_tax=0.0))),
    ("S: network fully taxed (tax 1)", dict(ov=dict(lv_tax=1.0))),
    ("S: core-chain share kphys 0.5", dict(ov=dict(lv_kphys=0.5))),
    ("S: core-chain share kphys 1.0 (upper)", dict(ov=dict(lv_kphys=1.0))),
    ("S: centralized compute as a flow (round-2 form)", dict(r3_kstock=False)),
    ("S: withdrawal at brand elasticity (round-2 form)", dict(r3_wd=False)),
    ("S: democracies may ban large networks (round-2 form)", dict(r3_ban=False)),
    ("S: capex elasticities low (eps_lab 0.5, eps_hyp 0.2)", dict(ov=dict(lv_eps_lab=0.5, lv_eps_hyp=0.2))),
    ("S: capex elasticities high (eps_lab 2, eps_hyp 0.7)", dict(ov=dict(lv_eps_lab=2.0, lv_eps_hyp=0.7))),
    ("S: network compute intensity kc 0.5", dict(ov=dict(lv_kc=0.5))),
    ("S: organising speed 10x, durability 1", dict(ov=dict(lv_spd8=10.0, lv_dur3=1.0))),
    ("S: repression backfire +0.2", dict(ov=dict(lv_bf=0.2))),
    ("S: no capture form (every crackdown a ban)", dict(r3_ban=False, ov=dict(lv_pcm=0.0))),
    ("S: low reading (F3 refusal, no cost link, untaxed, eps low, kphys 0.2, every crackdown a ban)",
     dict(ref_thr=True, cost_link=False, r3_ban=False, ov=dict(lv_tax=0.0, lv_eps_lab=0.5, lv_eps_hyp=0.2, lv_kphys=0.2, lv_pcm=0.0))),
    ("S: high reading (kphys 1, fully taxed, eps high)", dict(ov=dict(lv_kphys=1.0, lv_tax=1.0, lv_eps_lab=2.0, lv_eps_hyp=0.7))),
]


def verify(NO_full=3000):
    """lever off must reproduce the baseline headline exactly; lever on with every channel and crackdown off must equal it too"""
    t0 = time.time()
    m0, pd0, _, _, _ = run_cell(None, NO_full)
    ref = json.load(open(os.path.join(RES, "integrated_v4.json")))
    out = dict(lever_off_nt_UC=m0["nt_UC"]["mean"], lever_off_nt_world=m0["nt_world"]["mean"], lever_off_keep_UC=m0["keep_UC"]["mean"],
               runtime_s=round(time.time() - t0, 1))
    out["reference_integrated_v4"] = _ref_vals(ref)
    print("verify lever off:", out); sys.stdout.flush()
    return out, m0, pd0


def _ref_vals(ref):
    def find(d, key):
        if isinstance(d, dict):
            for k, v in d.items():
                if k == key:
                    return v
                r = find(v, key)
                if r is not None:
                    return r
        return None
    v1 = find(ref, "HEADLINE P(>=99.9% deliberate depopulation of the US or China bloc by 2075)")
    v2 = find(ref, "HEADLINE P(world population loss >=99.9% by 2075, all blocs)")
    g = lambda v: v["mean"] if isinstance(v, dict) else v
    return dict(nt_UC=g(v1), nt_world=g(v2))


def null_check(NO, m_base, pd_base):
    """lever on, all channels (C1-C5, L1-L9) and crackdown off, enclaves 0: lever randomness must not disturb the baseline"""
    m, pdd, _, _, _ = run_cell(dict(C_OFF, crack=False, **L_OFF), NO)
    same = all(np.array_equal(pdd[k], pd_base[k]) for k in pd_base)
    return dict(identical_per_draw=bool(same), nt_UC=m["nt_UC"]["mean"], base_nt_UC=m_base["nt_UC"]["mean"])


def main(mode="all"):
    setup()
    tag = os.environ.get("LV_TAG", "")           # brake runs: e.g. LV_TAG=_brakes -> results/lever_grid_brakes.json
    out_path = os.path.join(RES, f"lever_grid{tag}.json")
    part = os.path.join(RES, f"lever_grid_partial{tag}.json")
    # M8_FINAL=1 (final configuration: brakes + greenfield core loop + compute feedback + wide floors) counts as a brake run too; m8_v4.sample_params
    # reads M8_BRAKES / M8_FINAL itself, so the patched generator picks the configuration up unchanged
    final = os.environ.get("M8_FINAL", "") == "1"
    brakes = os.environ.get("M8_BRAKES", "") == "final" or final
    if brakes:
        assert tag, "set LV_TAG with M8_BRAKES=final or M8_FINAL=1 so the published lever grid is not touched"
    res = json.load(open(part)) if os.path.exists(part) else {}
    NO = int(os.environ.get("LV_NO", 1500))
    if mode in ("verify", "all") and "verify" not in res:
        v, _, _ = verify(3000)
        res["verify"] = v
        json.dump(res, open(part, "w"), indent=1)
    if mode == "verify":
        return
    t0 = time.time()
    m_b, pd_b, st_b, _, _ = run_cell(None, NO)
    res["baseline_NO"] = dict(NO=NO, metrics=m_b)
    if "null_check" not in res:
        res["null_check"] = null_check(NO, m_b, pd_b)
        print("null check", res["null_check"]); sys.stdout.flush()
    json.dump(res, open(part, "w"), indent=1)
    res.setdefault("grid", {}); res.setdefault("decomp", {})

    def do(key, cfg, store):
        if key in store:
            return
        t1 = time.time()
        m, pdd, st, pe, _ = run_cell(cfg, NO)
        c = dict(DEFAULT_CFG, **cfg)
        rec = dict(cfg=c, metrics=m, delta_vs_baseline={k: paired_delta(pdd[k], pd_b[k]) for k in ["nt_UC", "nt_world", "keep_UC", "keep_US", "keep_EU", "s5d_UC", "nt_US", "nt_CN"]},
                   diag=lever_diag(st, pe, c, st_b), efficiency_bar=efficiency_bar(st, pe), runtime_s=round(time.time() - t1, 1))
        store[key] = rec
        json.dump(res, open(part, "w"), indent=1)
        print(key, "nt_UC", m["nt_UC"]["mean"], rec["delta_vs_baseline"]["nt_UC"], round(time.time() - t0), "s"); sys.stdout.flush()
    if mode in ("uoff", "all") and not brakes:     # the U-off check compares with the stored brake-free round-2 grid
        # U1-U4 off must reproduce the stored lever round-2 grid (results/lever_grid_round4audit.json) exactly
        ref = json.load(open(os.path.join(RES, "lever_grid_round4audit.json")))
        res.setdefault("uoff_grid", {})
        for X in GRID_X:
            for Y in GRID_Y:
                do(f"X={X:g}|Y={Y}|enc=0", dict(X=X, Y=float(Y), enc=0.0, **U_OFF), res["uoff_grid"])
        chk = {}
        for k, r in res["uoff_grid"].items():
            o = ref["grid"][k]
            chk[k] = dict(nt_UC=r["metrics"]["nt_UC"]["mean"], ref=o["metrics"]["nt_UC"]["mean"],
                          delta=r["delta_vs_baseline"]["nt_UC"]["delta"], ref_delta=o["delta_vs_baseline"]["nt_UC"]["delta"],
                          identical=all(r["delta_vs_baseline"][m] == o["delta_vs_baseline"][m] for m in o["delta_vs_baseline"])
                          and r["metrics"]["nt_UC"] == o["metrics"]["nt_UC"] and r["metrics"]["nt_world"] == o["metrics"]["nt_world"])
        res["uoff_check"] = dict(all_identical=all(v["identical"] for v in chk.values()), cells=chk)
        print("U-off reproduces lever round-2 grid:", res["uoff_check"]["all_identical"]); sys.stdout.flush()
        json.dump(res, open(part, "w"), indent=1)
        if mode == "uoff":
            return
    if mode == "test":
        for X, Y, nm, cc in [(0.5, 2035, "round-3 pre-audit spec (round-4 fixes off)", dict(R4_OFF)),
                             (0.5, 2035, "round-2 spec (round-3 fixes off)", dict(R3_OFF, **R4_OFF, ch_core=False)),
                             (0.5, 2035, "all channels", {})]:
            do(f"X={X:g}|Y={Y}|{nm}", dict(X=X, Y=float(Y), **cc), res["decomp"])
        return
    for enc in [0.0]:
        for X in GRID_X:
            for Y in GRID_Y:
                do(f"X={X:g}|Y={Y}|enc={enc:g}", dict(X=X, Y=float(Y), enc=enc), res["grid"])
    for (X, Y) in DECOMP_CELLS:
        for nm, c in DECOMP:
            do(f"X={X:g}|Y={Y}|{nm}", dict(X=X, Y=float(Y), **c), res["decomp"])
    res["priors"] = {k: dict(spec=list(v[0]), source=v[1], evidence=v[2]) for k, v in LEVER_PRIORS.items()}
    res["priors_round2"] = {k: dict(spec=list(v[0]), source=v[1], evidence=v[2]) for k, v in LEVER_PRIORS2.items()}
    res["priors_round3"] = {k: dict(spec=list(v[0]), source=v[1], evidence=v[2]) for k, v in LEVER_PRIORS3.items()}
    res["priors_U"] = {k: dict(spec=list(v[0]), source=v[1], evidence=v[2]) for k, v in LEVER_PRIORS4.items()}
    res["notes_U"] = dict(lever_round2_results="results/lever_grid_round4audit.json", lever_round2_code="models/m9_lever_round4audit.py",
                          reproduction="uoff_check: every grid cell with U1-U4 off equals the stored lever round-2 cell")
    res["notes_round2"] = dict(P_SUC9=P_SUC9, round1_results="results/lever_grid_round1.json", round1_code="models/m9_lever_round1.py")
    res["notes_round3"] = dict(round2_results="results/lever_grid_round2.json", round2_code="models/m9_lever_round2.py",
                               reproduction="round-2 spec (round-3 fixes off) and round-1 spec decomp rows must equal the stored values")
    res["brakes"] = dict(M8_BRAKES=os.environ.get("M8_BRAKES", ""), M8_FINAL=os.environ.get("M8_FINAL", ""), note="final brake configuration (pid_on, sr_on, dis_on, brk_mort) on in every cell incl. the lever-off baseline; U-off reproduction check skipped (it compares with the brake-free grid)") if brakes else None
    res["greenfield"] = dict(M8_FINAL="1", note="final configuration: greenfield core loop (gf_on) and own-industry compute feedback (cf_on) and wide automated doubling floors (wfl_on) on in every cell incl. the lever-off baseline; see m8_v4.GF_NOTE and m8_v4.CF_NOTE") if final else None
    res["notes"] = dict(armed=LEV_ARMED_NOTE, unused_research=UNUSED_RESEARCH, A0=A0, A_REF=A_REF, NO=NO, R8=8, NI=200,
                        trajectories_per_cell=NO * 200)
    json.dump(res, open(out_path, "w"), indent=1)
    print("done", round(time.time() - t0), "s")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "all")
