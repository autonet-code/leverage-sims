# r10a: Grounding the elite-decision, refusal, defection and provision priors (F1-F4, F8)

Date: 2026-09-30. Target: models/m8_v4.py (elite game lines ~940-1030, PRIORS lines 259-287, grievance/provision lines 822-833).
Evidence grades: A = measured data, B = quantitative study or strong case pattern, C = case analogy with judgment, J = judgment.

Verification status. Web search budget was exhausted in this session. Items marked [V] were checked against a fetched source today. Items marked [M] are standard literature figures stated from memory and should be spot-checked before publication. Jev cross-checks are calibrated judgment, not data, and are labeled [Jev].

## 0. What the code does now (read before the proposals)

- Decision rule: 51 member draws per bloc. The deciding set is nlev (51 while democratic, 21 or the small-circle size nmin after breakdown, 51/21 by human share of security/admin h_sa). Each member picks the option maximizing U. The bloc takes the first option on the harshness order (serve, rentier, warehouse, neglect, depopulate) at which the cumulative count reaches a simple majority, i.e. the median member. No regime-type difference except the member count and a_vote/k_inst.
- p_refuse_abs: a member with refusal gets mX = 1e6. Because the neglect moral weight is kappa_N x mX, refusers also refuse neglect absolutely. This is a semantic defect: the historical record (section 2.4) shows elites who would not order killing routinely accepted lethal neglect. Hostile members override refusal (mX = 0).
- Security forces: only implicit, through h_sec in tau (threat cost), in the leverage index Lev (0.25 h_sec + 0.15 rv h_sec) and in insurgent success (def_mult). No event where humans refuse an order.
- Unconfirmed harsh choice: `keep_c = choice if choice >= 0 else 2` (warehouse). So the first recorded decision of an autocracy is warehouse whenever the harsh preference is not yet confirmed, which is why first_choice shows ~85% warehouse and 0% neglect/depopulate.

## 1. F1: evidence-grounded, regime-dependent decision rule

### 1.1 Evidence

| Finding | Value | Source | Grade |
|---|---|---|---|
| Personalist share of autocracies | 23% (1988) to 40% (2010) in Kendall-Taylor, Frantz & Wright 2016; Wikipedia's summary of GWF cites 28% to 52% [V]. Either way the modal modern autocracy is personalist | Geddes, Wright & Frantz 2014/2018 (GWF); Kendall-Taylor et al., Foreign Affairs 2016 | A |
| Personalist regimes: fewer internal checks, more repression, more radical policy shifts and war initiation | qualitative plus Weeks' estimates: personalist "bosses" and military "strongmen" initiate conflict markedly more than democracies; civilian "machine" (party) regimes are about as restrained as democracies [M] | Weeks 2012 APSR "Strongmen and Straw Men", Weeks 2014 *Dictators at War and Peace*; Frantz & Ezrow 2011 | B |
| Party/oligarchic regimes: power-sharing institutions (politburos, collective leadership) let elites monitor and constrain the leader | institutional constraint real but can be eroded by personalization (Stalin 1930s, Mao after 1959, Xi after 2018) | Svolik 2012 *Politics of Authoritarian Rule*; Magaloni 2008; Shirk on CCP collective leadership [M] | B |
| Who removes autocrats | 205 of 316 non-constitutional exits (about 65%) by regime insiders | Svolik 2012 (already in research/m5) | A |
| Selectorate logic | small W: private goods, loyalty via fear of exclusion; W shrinks as coercion is automated | Bueno de Mesquita et al. 2003 [V summary]; Davidson et al. 2025 AI coups | B (theory) |
| Democracies: policy change away from the status quo requires every veto player; 1-D result: the status quo is stable if it lies between the most and least extreme veto players' ideals | | Tsebelis 2002 *Veto Players*; Henisz POLCON | B (theory, strong empirics on policy stability) |
| Democracies essentially never committed democide against their own enfranchised citizens; democratic mass killing targets colonial or wartime out-groups | | Rummel; Harff 2003 (autocracy + exclusionary ideology is a risk factor) | B |

How the atrocity decisions were actually taken:

| Case | Regime type at decision | Who decided | Did others object; what happened | Grade |
|---|---|---|---|---|
| Final Solution / Wannsee (Jan 1942) | personalist (Hitler) with a bureaucratic implementing layer | decision already taken above the conference (Hitler, Himmler, Heydrich); Wannsee coordinated 15 officials [V] | no moral objection recorded; objections were administrative (Stuckart on Mischlinge/mixed marriages, Neumann on war-critical workers) [V] | A |
| Aktion T4 | personalist | Hitler's authorization letter, small circle (Bouhler, Brandt) | publicly halted Aug 1941 after church protest (Galen), not by an inner-circle veto; killing continued decentralized | B |
| Holodomor 1932-33 | personalizing party regime (Stalin dominant) | Stalin, Molotov, Kaganovich; Politburo decrees | objections from Ukrainian officials (Terekhov, Skrypnyk) were overruled; Skrypnyk suicide 1933 [M] | B |
| Great Leap famine 1959-61 | party regime personalized by Mao | Mao; Lushan 1959 | Peng Dehuai objected and was purged; the collective retreated only in 1960-62 (7000 Cadres Conference), i.e. a delayed partial veto after ~3 years [M] | B |
| Khmer Rouge 1975-79 | personalist-oligarchic Standing Committee, Pol Pot dominant | CPK Standing Committee (~7-9 members) | dissenters and whole zones (Eastern Zone 1978) purged; S-21 mostly cadres (research/m5) | B |
| Rwanda 1994 | oligarchic faction capture | Bagosora's crisis committee became de facto ruler; interim government a front [V] | moderates killed first (PM Uwilingiyimana); Butare prefect Habyalimana refused and was dismissed within ~12 days [V]; Gatsinzi tried to keep the army out, had limited control [V] | A/B |

Pattern: every large atrocity decision was taken by a dominant leader or a hardline faction that had captured the coercive apparatus. Inner-circle vetoes were rare and, when they happened (Great Leap), came years late. Collective bodies mostly acquiesced once the leader or faction controlled coercion. Where a collective leadership with real power-sharing existed (post-Stalin Politburo, post-Mao CCP), no comparable atrocity decision was taken. That is the core of the mixture below: the median-member rule is too cautious for personalist regimes and too permissive for democracies and institutionalized oligarchies.

### 1.2 Proposed rule (replaces lines ~985-987)

Regime type R(n, a, t) in {DEM, OLIG, PERS}:
- DEM while not `free`.
- On breakdown or grab: PERS with probability `p_pers_bd[a]`, else OLIG. Consolidated autocracies (ENTRENCHED) start in PERS with probability `p_pers0[a]`.
- Personalization hazard OLIG -> PERS: `k_pz * (1 - h_sa)` per year (the leader needs fewer allies once security/admin are automated; W shrinks). No reverse transition except via regime change (success, redemocratization).

| Param | Proposal | Evidence | Grade |
|---|---|---|---|
| p_pers0 | China_bloc Beta(5,5) (party regime personalized since 2018); Russia_MENA Beta(7.5,2.5) | GWF codings; Xi term-limit removal 2018, 2022 PSC of loyalists; Putin | B/C |
| p_pers_bd | US_bloc Beta(7,3) (mean 0.7); Europe_plus, South_Asia, Global_South Beta(5.5,4.5) | modern breakdowns via executive aggrandizement (Hungary, Turkey, Venezuela, Nicaragua) all produced personalist regimes; personalist share of autocracies 40-52% | B/C |
| k_pz | U(0.02, 0.10)/yr at h_sa = 0 | observed within-regime personalization over ~5-12 y (Russia 2000-12, China 2012-22) | C |

Aggregation by type (ideal = each member's argmax as now; order serve < rentier < status quo < warehouse < neglect < depopulate, see F8):
- DEM (veto players): split the 51 members into V groups; each group's median is a veto player's ideal. Status quo SQ is the current regime (initially the status-quo trajectory). New policy = SQ clamped to [min_g med_g, max_g med_g] (the 1-D unanimity core). V = 1 + round((V_max - 1) x clip((Ddem - 0.3)/0.3, 0, 1)), V_max ~ U{3,4,5} (executive, two chambers, court, federal units). Erosion removes veto players before formal breakdown (courts captured, legislature subordinated), which is the observed backsliding sequence. Grade B (theory with strong policy-stability evidence), V_max C.
- OLIG (collective leadership, bargaining): a move harsher than SQ to option k needs a share >= q_ol of members whose ideal is >= k; a move to milder options needs only a simple majority (hardliners must build a coalition; relief is the default of bargaining failure plus provision already in place). q_ol ~ U(0.5, 0.67). Evidence: consensus norms in collective leaderships; Weeks' machine regimes behave like democracies; Svolik's power-sharing. Grade C.
- PERS (leader with veto players): the leader is one member, drawn with a selection tilt toward harshness: leader = member at harshness quantile u^(1/(1+s)), s ~ U(0, 1) (s = 0 is a random member; J, since the evidence that crisis-era personalists are more ruthless than their circles is anecdotal). The inner circle (nmin or 5-9 members) can veto: if a majority of it prefers a milder option, the veto succeeds with probability v_eff x h_sa, and policy becomes the inner-circle median. v_eff ~ U(0.05, 0.30) per decision. Evidence: no inner-circle veto stopped Holodomor, Final Solution, T4 or Khmer Rouge; the Great Leap retreat came after ~3 years; insiders do remove leaders (65% of irregular exits) but rarely over atrocity policy. Grade C.

Expected direction versus the current median rule: lower harsh-choice probability in DEM (unanimity core) and OLIG (q_ol > 0.5), higher in PERS (leader tail). The net effect on the headline depends on the PERS share, which rises with automation through k_pz. This is the honest version of the "2/3 vs 1/3" lever: the data do not pick one threshold; they pick different ones by regime type, and the modern trend is toward the type with the weakest constraint.

Jev cross-check (research/jev_elite_calculus.json, earlier): single ruler after purges raised P(lethal) 0.19 -> 0.23; strong democratic institutions cut it to 0.11. Same direction as this mixture.

## 2. F2: p_refuse_abs, by layer and regime

### 2.1 Evidence: executors (not the decision layer)

| Finding | Value | Source | Grade |
|---|---|---|---|
| Milgram baseline obedience to 450 V | 65% [V] | Milgram 1963 | A |
| Across variations | 21% (phone orders), 40% (same room), 47.5% (Bridgeport office), 15% (friend as learner) [V]; mean about 44% across ~20 conditions [M] (Haslam, Loughnan & Perry 2014) | Milgram 1974 | A |
| Burger 2009 partial replication (stop at 150 V) | obedience "virtually identical" [V]; 70% continued past 150 V vs 82.5% in Milgram [M] | Burger 2009 | A |
| Belief caveat | only about half fully believed the shocks were real; of those 66% disobeyed [V] | Perry 2012 | B |
| Reserve Police Battalion 101, Józefów July 1942 | 12 of ~500 stepped out when offered [V] (2.4%); more asked to stop during the shooting; Browning's overall estimate of refusers/evaders 10-20% [M] | Browning 1992 | A/B |
| Punishment of refusers | no documented case of a German executed for refusing to kill civilians; ~100 documented refusals [M] | Kitterman 1988 | B |
| Rwanda | villagers refusing to kill were often branded Tutsi sympathizers and murdered [V]; perpetrators ~175-210k, roughly 14-17% of adult Hutu men [M] | Straus 2006; Fujii 2009 | B |
| Mechanisms | conformity and fear of appearing weak (Browning [V]), moral disengagement (Bandura 1999), displaced/diffused responsibility, dehumanization (Haslam 2006; Kteily et al. 2015), gradual escalation (Mann 2005; Waller 2002) | | B |

Reading: when the harm is real and the order is framed as legitimate, 10-35% of individual executors refuse or evade (Browning upper range, Milgram belief-adjusted). Collective breakdown did not happen in minority-targeted genocides, because perpetrators were recruited from a non-targeted group. These figures belong in p_exec and the F3 defection mechanism, not in p_refuse_abs.

### 2.2 Evidence: top decision layer

| Case | Refusal among the decision/implementation elite | Grade |
|---|---|---|
| Wannsee, 15 senior officials | 0 moral objections recorded [V] (a selected, ideologized group; decision already taken) | A |
| Soviet Politburo 1932-33 | no recorded refusal among members; objections came from republic-level officials, overruled [M] | B |
| Rwanda 1994 | moderates in government killed at onset; 1 of ~11 prefects refused outright (Butare) and a few resisted briefly; a group of FAR officers (Gatsinzi and others) sought a truce [V/M]. Roughly 10-20% of the senior layer | B |
| Khmer Rouge, Stalin 1937-38, Saddam 1979 | refusers purged before or during; 70% of the 1934 CC arrested by 1939 (research/m5) | A |
| Democratic elites, far smaller acts | Esper and Milley refused to deploy active troops against protesters in 2020 (Esper memoir, [M]); Pence refused to overturn the 2020 count; Richardson and Ruckelshaus resigned rather than fire Cox (1973) | B (direction) |
| Public, killing enemy civilians in war | ~60% of Americans approved a nuclear strike killing ~2M Iranian civilians to save 20k US troops [M] (Sagan & Valentino 2017): ~40% refuse even for an enemy out-group in war; refusal for one's own co-nationals in peace should be far higher | B |

Selection is the central fact: regimes that go on to commit atrocities have already filtered refusers out of the decision layer (purges, killings, dismissals); democracies have not. So a single Beta(3,3) for all regimes averages two very different populations.

### 2.3 Proposed priors (replace p_refuse_abs)

| Param | Proposal | Mean (90% interval) | Evidence | Grade |
|---|---|---|---|---|
| p_ref_dem (DEM coalition while not free) | Beta(7, 3) | 0.70 (0.45-0.90) | no democratic democide against citizens; elite refusals of far smaller acts; Jev 0.75-0.85 [Jev] | C |
| p_ref_olig (OLIG) | Beta(2, 10) | 0.17 (0.03-0.37) | Rwanda senior layer ~10-20%; Politburo 1932 ~0; Jev mean ~0.15 [Jev] | C |
| p_ref_pers (PERS inner circle) | Beta(1.2, 12) | 0.09 (0.01-0.25) | purge selection; Wannsee 0/15; Jev mean ~0.05 [Jev] | C |
| h_purge (half-life of convergence from p_ref_dem to the autocratic value after breakdown) | U(2, 8) y | | Stalin 1934-39 (~5 y), Saddam 1979 (instant), Turkey post-2016 (~150k officials purged within ~2 y [M]), Hungary gradual (8+ y) | B/C |
| r_neg (neglect refusal as a share of killing refusal) | U(0.2, 0.6); non-refusers of neglect keep finite kappa_N x moral_base | | Holodomor, Great Leap, Irish famine, Bengal: officials who would not order shootings enforced lethal requisition/neglect; Bandura's "distortion of consequences". Jev put neglect refusal in the party layer at ~0.25 of the population vs ~0.15 for killing, but with confidence 0.08 (uninformative) [Jev] | C |

Code: `refuse = mem_u_ref < p_ref(R, t)`; `refuse_neg = mem_u_ref < r_neg x p_ref(R, t)`; mX for neglect uses refuse_neg only. Keep "hostile overrides refusal".

Executors (for p_exec and F3): individual refusal of real killing q_ind ~ U(0.10, 0.35) against an out-group; a majority own-population target breaks the perpetrator/victim separation and belongs in the F3 collective-breakdown probability.

## 3. F3: explicit security-force defection

### 3.1 Evidence

| Finding | Value | Source | Grade |
|---|---|---|---|
| Effect of defection on campaign success | "defections more than quadruple the chances of campaign success" [V]; defections coded only as "large-scale, systematic breakdowns in the execution of a regime's orders" [V] | Stephan & Chenoweth 2008, IS 33:1 | A |
| Frequency | defections in ~52% of successful nonviolent vs ~32% of successful violent campaigns (research/m4, [M]); nonviolent methods themselves did not significantly raise defection probability in their logit [V] | Chenoweth & Stephan 2011 | A/B |
| Mechanism | forces are more willing to kill armed insurgents than unarmed demonstrators; armed challengers make forces close ranks [V] | Stephan & Chenoweth 2008 | B |
| Coup-proofing and communal stacking predict loyalty | Syria, Bahrain (loyal core) vs Tunisia, Egypt (institutional armies stood aside) [M] | Makara 2013; Lee 2015 *Defect or Defend* (military institutional interest vs personalized regime); Barany 2016; Nepstad 2011 | B |
| Cases, defected/stood aside | Iran 1979, East Germany 1989 (Leipzig 9 Oct), Serbia 2000, Tunisia 2011, Egypt 2011, Bangladesh 2024, Madagascar 2025 (research/m4) | | A |
| Cases, loyal and fired | China 1989 (Xu Qinxian refused and was court-martialed, others fired), Syria 2011 (tens of thousands defected, core held), Iran 2009/2019/2022/2026, Belarus 2020, Myanmar 2021 (a few thousand defected, regime held) | | A |
| Outcome of defection | regimes usually fall; result is often military rule (1 of 6 Arab Spring cases democratic; research/m4 row 21) | | B |

### 3.2 Proposed mechanism

Order types o in {P: repress mass protest/strikes, I: counterinsurgency, C: collective punishment, X: execute depopulation (also enforce lethal neglect)}.

1. Systematic breakdown event, given an order of type o while humans do part of coercion: probability q_o x m_stack(R).
2. Size and bite: a breakdown takes a share d ~ U(0.3, 0.7) of the human coercive units. The order fails if d x h_sec_f > 1 - c_req, with c_req ~ U(0.4, 0.7) (the capacity the regime needs to carry the order through; Syria survived losing roughly half of its army with a loyal core plus foreign help). The protection therefore vanishes smoothly as coercion is automated: below h_sec_f = (1 - c_req)/d (typically 0.4-1.0), defection can no longer stop an order. This is the scenario's mechanism made explicit, and it also dates the end of protection.
3. Consequences: (a) X or C fails: current failX branch (1-5% dead, insurgency) plus regime crisis: with p_oust ~ U(0.5, 0.8) the leader/faction is removed (Svolik insiders; Tunisia, Egypt, Iran 1979, Bangladesh 2024), choice resets to SQ, and p_dem_suc applies. (b) During insurgency, a breakdown multiplies insurgent success odds by OR_def ~ lognormal(median 4, sd 0.4) (Stephan & Chenoweth 2008 "more than quadruple"); replace the ad hoc def_mult term with this. (c) Anticipation: in U, harsh options carry P_fail_o x C_oust, where C_oust is the coalition's loss if ousted (Archigos: ~80% of leaders removed irregularly were punished; research/m5). (d) Remove the double count: drop 0.25 h_sec_f and 0.15 rv h_sec_f from Lev, or halve them, since defection now carries that channel explicitly.

| Param | Proposal | Mean (90%) | Evidence | Grade |
|---|---|---|---|---|
| q_P (mass nonviolent protest, fully human forces) | Beta(4, 6) | 0.40 (0.17-0.65) | NAVCO frequencies (implies roughly a third of major nonviolent campaigns saw systematic defection); Arab Spring 2 of 6 stood aside, 2 split; Jev ~0.45 [Jev] | B/C |
| q_I (armed insurgency) | Beta(2, 8) | 0.20 (0.04-0.45) | closing ranks against armed challengers; lower defection share in violent campaigns. Jev gave ~0.45; I weight the NAVCO pattern over Jev here | B/C |
| q_C (collective punishment of a region) | Beta(2.5, 7.5) | 0.25 | between I and X; colonial and counterinsurgency cases were carried out (Mau Mau, Herero, Guatemala) mostly with out-group or stacked units | C |
| q_X (kill the general majority population) | Beta(5, 3.5) | 0.59 (0.31-0.84) | no precedent at majority scale; minority genocides saw no collective breakdown because perpetrators came from a non-targeted group; a majority target includes the forces' own kin; the maximum own-population share ever killed (~22-25%, Khmer Rouge) used a class split. Jev ~0.55 [Jev] | J/C |
| m_stack | PERS x U(0.4, 0.8); OLIG x U(0.7, 1.0); DEM 1 | | coup-proofing and communal stacking (Makara; Syria, Bahrain); institutional armies stand aside (Lee; Tunisia, Egypt) | B |
| d, c_req | U(0.3, 0.7), U(0.4, 0.7) | | Syria 2011-13, Myanmar 2021, Iran 1979 desertion scale | C |
| p_oust | U(0.5, 0.8) | | Arab Spring, Iran 1979, Bangladesh 2024 | B |

Interaction with p_exec: p_exec now reads as the technical/organizational success probability with automated forces; effective success = p_exec x (1 - P_fail_X(h_sec_f)).

## 4. F4: other elite dispositions

| Param (code) | Current | Proposal | Evidence | Grade |
|---|---|---|---|---|
| p_hostile (welfare inverted, zero moral cost) | Beta(1.2, 14), mean 0.08 | Beta(1.5, 40), mean 0.036 (0.005-0.09) as baseline; growth via host_ins, host_H, id_share unchanged in form | psychopathy ~1% of the general population, ~3-4% in senior business roles [V: Hare; Babiak, Neumann & Hare 2010]. Psychopathy is callousness (indifference), not hostility; true hostility (gain from others' suffering) is rarer. Callous indifference is already covered by the lower tail of moral_med (sd 1.2) and alpha. Page, Bartels & Seawright 2013: wealthy far less supportive of job guarantees and income floors (research/r8b): that is low alpha, not hostility | C |
| host_ins (hostility added by insurgency) | U(0.03, 0.15) | U(0.05, 0.25) | threat radicalizes elites: counterguerrilla mass killing (Valentino, Huth & Balch-Lindsay 2004); political upheaval raises genocide odds (Harff 2003, 28% of state failures became geno/politicide); war and the assassination radicalized Rwandan moderates (Straus 2006); perceived dehumanization breeds reciprocal dehumanization (Kteily et al. 2016) | C |
| host_H | U(0, 0.15) | keep; note evidence is the same threat literature | C |
| moral_med | lognormal(0.3, 1.2) | keep the form; state "J, no direct measurement". Scale anchor: publics accept very large enemy civilian tolls for small own-side gains (Sagan & Valentino), so moral cost is finite and outcome-dependent, but for co-nationals it is higher | J |
| power effect on moral cost/alpha | none | optional multiplier U(0.7, 1.0) on moral_med and alpha for autocratic coalitions | power reduces perspective taking and empathic resonance (Galinsky et al. 2006; Hogeveen, Inzlicht & Obhi 2014; Keltner 2016); upper-class unethical behavior (Piff et al. 2012) has mixed replications, so the size is small and uncertain | C- |
| mc_ai (moral-cost factor at AI-mediated targeting) | U(0.5, 0.9) | keep; now grounded | Milgram proximity gradient: 65% remote vs 40% same room vs 30% touch-proximity [V/M], so distance roughly halves the moral brake; Bandura displacement and diffusion of responsibility; drone operators still show moral injury, so the discount is partial | B |
| alpha_med (willingness to pay for public welfare, share of output) | lognormal(0.03, 0.9) | lognormal(0.02, 1.0) (p10 0.006, p90 0.07) | the cleanest analog of spending on a population that has no leverage: ODA ~0.3% of donor GNI and falling in 2025 [M] (USAID dismantled, UK to 0.3%); co-nationals get an in-group premium over foreigners (several-fold in value-of-life surveys [M]); US private giving ~2% of GDP [M]. Welfare-state spending (~21% of GDP OECD) is leverage-driven (research/r8b) and must not be used | C |
| alpha_sig | U(0.6, 1.4) | keep | heterogeneity in giving is large (lognormal-like); no better data | C |
| v0 (land/resource value freed) | lognormal(0.01, 0.9) | keep median, widen sd to 1.1; note urban land value is endogenous to population (removing people destroys most of it), so freed value is mainly rural land, minerals and siting for energy/data centers | settler-colonial "logic of elimination" (Wolfe 2006) is the historical motive, but in labor-free AI economies the land need is small (solar and data-center land is a small share of territory) | J |
| LANDK [serve, rentier, warehouse, neglect, depop] | [0, 0, 0.6, 0.8, 1.0] | [0, 0, 0.6, 0.6 + 0.4 x f_dead, 1.0], f_dead ~ the neglect loss share (~0.1-0.3), so neglect ~0.65-0.7 | warehousing = concentration: apartheid reserved ~13% of land for the majority (Natives Land Acts 1913/1936 [M]), US Indian removal; neglect frees only the extra land of those who die | C/J |

Unchanged but flagged: kappa_N (neglect moral cost vs killing) should be read together with the r_neg split in F2.

## 5. F8: status-quo provision trajectory (replace the warehouse default)

### 5.1 Evidence on the 2026 direction

| Bloc | Direction | Evidence | Grade |
|---|---|---|---|
| US | cuts to the means-tested floor, no displacement program | OBBBA (Jul 2025): >$1.2T spending cuts over 10 y, mainly Medicaid and SNAP; SNAP -$186B 2025-34; CBO: 10.9M more uninsured; bottom decile income -3.1% and top decile +2.7% by 2034; Medicaid work requirement 80 h/month ages 19-64, SNAP work rules extended to 18-64 [V]. UI replaces ~40-50% of wages for ≤26 weeks and reaches roughly a quarter to a third of the unemployed [M]; Trade Adjustment Assistance, the only displacement-specific program, lapsed in 2022 [M] | A |
| US, crisis response | large but temporary | CARES Act 2020 (~$2.2T, +$600/week UI), Great Recession UI extensions to 99 weeks; both expired within ~1-2 years [M] | A |
| Europe_plus | flat to slightly down; resistance to cuts | NATO 2025 commitment to 5% of GDP (3.5% core) pressures social budgets; UK 2025 welfare cuts partly withdrawn after backbench revolt; German Bürgergeld tightening [M] | B |
| China | slight expansion from a low base, "anti-welfarism" doctrine | childcare subsidy 3,600 yuan/yr per child under 3 (2025), small rural pension increases; dibao coverage shrank over the 2010s; Xi's 2021 warning against "welfarism" [M] | B |
| Others | mixed, fiscal constraints | IMF programs, low-capacity states | C |

### 5.2 Proposal

- Add a sixth internal option "status quo" (SQ) between rentier and warehouse on the harshness order (political rights intact while democratic, provision meager, no concentration). SQ is also the value of `choice` before any confirmed decision: set `keep_c = choice if choice >= 0 else SQ`, not warehouse. first_choice then reports "status quo (no confirmed decision)" separately; warehouse must win the decision rule to be recorded.
- SQ provision: P_sq(a, t) = BASE_PROV[a] x exp(d_a x (t - 2026.75)) for the displaced long-term, plus the existing crisis response (k_resp in democracies, k_buy in autocracies with human security) that already appears in P_pre. Add a decay so each crisis expansion fades with half-life U(1, 3) y unless grievance stays high (CARES, 99-week UI).
- Drift priors d_a per year: US_bloc U(-0.020, 0.000) (OBBBA: bottom-decile income -3.1% by 2034, federal Medicaid cuts on the order of 10-15% by 2034 [M]); Europe_plus U(-0.010, 0.005); China_bloc U(-0.005, 0.015); others U(-0.010, 0.010). Grade B for the sign in the US, C for sizes.
- Long-term displaced vs BASE_PROV: BASE_PROV US 0.45 is an average of today's system; for the long-term displaced (UI exhausted, TAA gone, work requirements binding on Medicaid/SNAP) the effective floor is lower. Suggest a displaced-specific multiplier U(0.6, 0.9) on BASE_PROV for US_bloc (C).
- SQ in U: welfare = P_sq; cost = P_sq x costS; threat = 1 - pr_red x P_sq; land 0; moral 0; no switching cost for staying.

Note: warehouse provision (0.6) is above US status quo (0.45), so the current default both inflates "warehouse" as a first choice and slightly overstates provision for undecided blocs. With SQ, disempowerment and first-choice statistics should fall and attrition could rise a little.

## 6. Documentation items requested (keep as is, document)
- Executed depopulation books S5 at t + lagX without simulated deaths (94% of S5_deliberate). It is a definitional shortcut: p_exec (now x (1 - P_fail_X)) is the probability that the order reaches >=10% loss.
- Rentier is never chosen: with c_R 0.7-1.0 of serve cost and w_R < 1, it is dominated by serve for low-hostility members and by warehouse/SQ for others. Gulf rentierism is driven by the leverage of a citizen minority and oil rents that labor does not produce; the model has no minority-citizen structure.
- "Serving is cheap when output explodes": costS = m0/G, so provision cost falls as output G rises. Legitimate (research/m5 rentier analog; Jev) and it is the strongest force against S5 in the model.

## 7. Evidence-quality summary
Best grounded: regime-type differences in constraint (GWF, Weeks, Tsebelis), historical decision structure (Wannsee, Rwanda, Holodomor, Great Leap), defection effect size (Stephan & Chenoweth) and its dependence on coup-proofing, US provision direction (OBBBA/CBO). Moderate: executor refusal rates (Browning, Milgram), selection of refusers out of autocratic elites, mc_ai. Weak/judgment: q_X for a majority target, leader selection tilt s, v_eff, moral_med, v0, LANDK, the power-empathy multiplier.
