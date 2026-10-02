# Supplement S1: Full parameter list

Generated from the prior dictionaries in `models/m8_v4.py` (PRIORS, and PRIORS_B for the behavioral changes B1 to B6) and `models/m9_lever.py` (LEVER_PRIORS to LEVER_PRIORS4). The "Basis" column is the source note from the code, shortened. Evidence labels follow the code: A/measured, B/strong analog, C/weak analog, J/judgment, plus older verbal labels (high, medium, low, very low). [M] marks a figure from memory or a secondary compilation that was not re-fetched.

**PRIORS** (198 parameters)

| Parameter | Distribution | Evidence | Basis |
|---|---|---|---|
| h50_0 | lognormal (median 16, sd 0.15) | medium-high | METR 50% horizon, best model mid-2026: 12-20 h (METR May 2026) |
| h80_ratio | lognormal (median 4.5, sd 0.3) | medium-high | 50%/80% horizon ratio: 16 h vs 3.5 h (METR May 2026) |
| metr_doubling_months | lognormal (median 4.3, sd 0.28) | medium-high | horizon doubling 2023+ window 4.3 mo; 2024-25 3-3.5 mo; long-run 7 mo (METR TH1.1). F5: sets only the SPEED of the trend; the task-difficulty spread uses the fixed observed doubling METR_OBS=4.3 mo, so faster doubling can never ... |
| compute_slowdown | U(0.35, 1) | moderate | Epoch: 4-5x/yr compute growth hard to sustain past ~2030. A1: OFF in the baseline (capability follows the trend); used only in the 'trend_breaks' variant |
| mess | lognormal (median 3, sd 0.6) | low-medium | benchmark-to-real-work horizon discount; affects only M6 (the share milestones are re-anchored to measured 2026 shares, so it cancels there) |
| z_rate | U(0.5, 1.1) | medium | speed of AI code-share growth in probit units/yr (Google 25%->50%->75% Oct24-Apr26). Used as the task-difficulty spread for CAPABILITY shares: the share of tasks AI can do well rises with the horizon at this slope |
| k_rnd | U(1, 2) | low | AI-research tasks' difficulty spread relative to software tasks |
| k_ec | U(1.5, 3) | low | economy-wide desk tasks' difficulty spread relative to software |
| sw_cap0 | lognormal (median 0.15, sd 0.5) | low | CAPABILITY 2026: share of software tasks AI can do end to end at mergeable quality with no review. Lower bound: Uber merges >10% with no human in the loop (practice <= capability); upper side limited by METR's finding that many ... |
| sw_prac0 | lognormal (median 0.04, sd 0.5) | low | PRACTICE 2026, economy-wide: share of software work actually merged with no human review (Uber >10% is a leader; most firms review all AI code) |
| g_swad | U(0.4, 1.2) | low-medium | practice adoption speed, log-odds per yr. AI-written, human-reviewed code rose ~1.5 log-odds/yr at Google; removing review is slower (liability, SOC2/ISO review norms, regulated sectors ~30% of software work). Practice never ... |
| rnd0 | U(0.15, 0.35) | medium (single self-report) | share of frontier-lab R&D tasks where AI does the work and humans assign/check (Anthropic Sep 2026: 26% 'leads') |
| Fcog0 | U(0.1, 0.25) | moderate | reliably automatable desk-task share 2026 (AEI, GDPval 48%, API success 49%) |
| p_cog_wall | 0.12 | weak | no-AGI-this-century mass ~10-15% |
| p_capex_correction | 0.35 | moderate | capex ~7x lab revenue; Abilene expansion abandoned 2026 |
| fb_zero_mass | 0.1 | moderate-weak | A1: P(no further shrinking of the doubling time from AI-accelerated AI research); round 2 used 0.25 (Davidson & Houlden 2025: r<1 plausible) |
| fb_strength | lognormal (median 0.7, sd 0.6) | low-medium | A1: elasticity of the horizon growth rate to AI-R&D automation, mult = ((1-rnd0)/(1-s_rnd))^fb. Anchor: the doubling time fell 7 -> ~4.3 mo while AI-led R&D rose from ~0 to ~0.26, which implies fb <= ln(1.63)/ln(1/0.74) = 1.6 if ... |
| a_cog0 | lognormal (median 0.03, sd 0.4) | medium-low | share of desk-task value actually automated 2026 (genAI in 6.3% of work hours, about half automation) |
| g_cog0 | lognormal (median 0.25, sd 0.25) | medium-high | current growth of automated desk-work share (genAI hours +28%/yr) |
| g_cog_max | lognormal (median 0.7, sd 0.4) | low-medium | adoption rate once AI reliably does most desk tasks |
| dx0 | lognormal (median 0.04, sd 0.5) | low | 2026: share of O*NET physical work tasks a general-purpose robot does in production at >=50% of human speed (picking >99% in production, palletizing, machine tending, tote handling; most manipulation 3-10x slower: Epoch 2026, r8a) |
| rp0 | lognormal (median 0.35, sd 0.5) | low | current growth of logit(dx) per yr: 2023-26 production-ready task set went from picking-only to picking + machine tending + tote/parts handling pilots (~1.5-2% -> ~3-5%, logit +0.25-0.45/yr) |
| kc | lognormal (median 0.5, sd 0.8) | low | AI -> robotics coupling per horizon doubling beyond M3 (robot foundation models, sim-to-real) |
| rp_max | lognormal (median 1.5, sd 0.4) | low | cap on logit(dx) growth per yr (hardware generation cadence 1-2 y per actuator generation) |
| p_phys_wall | 0.1 | low | hands/actuator wall before general dexterity |
| s0 | U(0.1, 0.35) | moderate | 2026 manipulation speed vs human (Epoch: 3-10x slower) |
| shifts | U(1.5, 3) | moderate | robot operating hours vs one worker FTE |
| Fp_scale | U(0.6, 1.4) | low | uncertainty on 2026 feasible shares per segment |
| g0_mult_sd | 0.35 | high (observed volatility) | per-segment volatility of current growth rates (China 2025: textiles -92%, auto +38%) |
| g_ramp | lognormal (median 0.5, sd 0.3) | good | sustained sector ramp a priority actor reaches with human labor: solar 49->315 GW/yr, NEV 1.4->13M, Indonesian nickel, CoWoS (r9b) |
| i_K | U(0.08, 0.15) | good | gross fixed investment / capital stock per yr: the flow of new capacity that can be automated from day one (OECD ~0.08-0.10, China peak ~0.15) |
| i_boost | U(1.3, 2) | moderate | investment boost under priority/profitability (China 2000s investment ~45% of GDP vs ~22% typical) |
| k_int | lognormal (median 1, sd 0.3) | low | capital intensity of automated capacity relative to average (robots cheaper than labor but capex-heavy) |
| r_retro0 | U(0.02, 0.06) | moderate | retrofit/scrapping rate of human-operated capacity, no priority |
| r_retro_p | U(0.1, 0.3) | low | retrofit/scrapping rate under full priority (deliberate replacement) |
| kit_brake | U(0.1, 0.5) | moderate-low | automation-kit growth halves once new kit equals this share of the physical workforce |
| humanoid_mult | lognormal (median 2, sd 0.3) | moderate | general-purpose robot output multiple per yr before AI-directed production (Goldman 1.9x/yr; SAG +272% 1H2026 from tiny base) |
| P_half | lognormal (median 5, sd 0.6) | moderate | M robots/yr per bloc at which the human-built ramp halves (NEV 2.2x -> 1.35x at 7-13M) |
| Pmax_h | lognormal (median 50, sd 0.6) | low | M robots/yr reachable with 2026-level human labor (auto industry ~90M vehicles/yr) |
| prod_use | U(0.4, 1) | low | productive-use share of shipped humanoids |
| M0 | lognormal (median 30, sd 0.7) | moderate | M robots/yr supportable by divertible NdPr |
| C0 | lognormal (median 20, sd 0.9) | low | M robots/yr of inference chips at ~20% diversion |
| Td_mine_base | lognormal (median 15, sd 0.3) | good | mineral supply doubling without priority (copper etc. 3-5%/yr) |
| Td_mine_race | lognormal (median 3.5, sd 0.3) | moderate | mineral doubling for a priority actor (Indonesia nickel, lithium 2020-24: 2-2.5 y) |
| Td_mine_auto | lognormal (median 1.5, sd 0.45) | low | mineral doubling floor once mining/processing robotic (ore grades) |
| Td_fab_base | lognormal (median 11, sd 0.2) | moderate | wafer capacity doubling at 6-7%/yr (SEMI) |
| Td_fab_race | lognormal (median 2.5, sd 0.3) | moderate | chip capacity doubling for a race actor (JASM 2.7 y, TSMC AZ 3.5 y build) |
| fab_build | lognormal (median 2.5, sd 0.25) | good | groundbreaking to volume production |
| fact_build_h | lognormal (median 1.2, sd 0.5) | moderate | greenfield factory build, human (Giga Shanghai 11 mo, Colossus 122 days) |
| fact_build_a | lognormal (median 0.5, sd 0.45) | low | same with prefab/robotic construction |
| Td_en_base | lognormal (median 20, sd 0.3) | moderate | electricity capacity doubling without priority |
| Td_en_race | lognormal (median 3, sd 0.3) | good for China | electricity doubling with priority (China solar ~2.2 y, total ~5 y) |
| Td_en_auto | lognormal (median 1.5, sd 0.45) | low-moderate | energy doubling floor in an automated loop (PV payback ~1 y) |
| Td_auto | lognormal (median 1, sd 0.6) | low (theory) | robot-stock doubling once AI directs production (Forethought, theory) |
| Td_mat | lognormal (median 0.25, sd 1) | very low | mature fully automated industrial doubling |
| ai_lc | lognormal (median 1.3, sd 0.2) | very low | AI compression of design/permitting/planning lead times, phased in by M3 (bounded 1.05-2x) |
| adl | lognormal (median 3, sd 0.5) | low | one-time productivity multiple of AI-directed human build labor (Forethought claims 10x; upper bound) |
| reinvest | U(0.3, 1) | low | share of automated output reinvested in expansion |
| G_max | lognormal (median 300, sd 1) | very low | terrestrial ceiling on robot worker-equivalents per 2026 worker |
| robot_life | U(6, 12) | moderate | robot service life |
| q_core | lognormal (median 0.15, sd 0.6) | very low | scale of minimal self-sufficient core loop vs full chain |
| psi0_US | Beta(3.5, 6.5) | weak | US bloc pursuit intensity (Genesis, DoD all-lawful-use) |
| psi0_CN | Beta(4.5, 5.5) | weak | China pursuit (MIC2025, +20%/yr robot installs, 'intelligent military') |
| psi0_RW | Beta(1.5, 8.5) | weak | rest-of-world pursuit (x1.5 Europe, x1.0 Russia_MENA, x0.8 South Asia, x0.6 Global South) |
| race_gamma | U(0.5, 2) | weak | pursuit response to rival lead |
| t_leth_rate | 0.115 | weak | per-bloc rate of routine lethal targeting with no per-strike human approval (r8c) |
| k_pg | lognormal (median 0.012, sd 0.8) | weak | narrow-group power grab hazard at full security/admin automation (Forethought AI coups) |
| alpha_med | lognormal (median 0.02, sd 1) | C | F4: elite willingness to pay for the welfare of a population with no leverage, share of output. Analog: OECD ODA ~0.3% of donor GNI (falling 2025) plus an in-group premium for co-nationals; US private giving ~2% GDP is the upper ... |
| alpha_sig | U(0.6, 1.4) | low | within-coalition heterogeneity |
| p_hostile | Beta(1.5, 40) | C | F4: baseline share of coalition members hostile to the public (welfare inverted), mean 3.6%. Psychopathy ~1% general population, 3-4% in senior corporate roles (Babiak, Neumann & Hare 2010, verified); callousness (indifference) ... |
| moral_med | lognormal (median 0.3, sd 1.2) | J | moral cost of ordering mass killing, output-share equivalent (Sagan & Valentino 2017 wartime polls; Bandura 1999). No direct measurement |
| m_pow | U(0.7, 1) | C- | F4: moral-cost multiplier in autocratic coalitions (power reduces perspective-taking: Galinsky 2006, Hogeveen et al. 2014, Keltner 2016; mixed replication) |
| k_mor | U(0, 0.02) | J | A7: yearly decline of the moral cost (partisan dehumanization, AI targeting compressing human review; r9d, r11a) |
| p_ref_dem | mixture: 0.7 x Beta(7, 3) + 0.3 x Beta(8, 2) | C | F2: share of a DEMOCRATIC ruling elite that absolutely refuses to order killing of the population. Not filtered for obedience; refused far smaller illegal acts (Esper/Milley 2020, Pence 2021, 1973); no democide by democracies ... |
| p_ref_olig | mixture: 0.7 x Beta(2, 10) + 0.3 x Beta(2, 4) | C | F2: same, party/oligarchic elite. Rwanda 1994: ~10-20% of the senior layer resisted (Butare prefect dismissed in ~12 days); Soviet Politburo 1932-33 no recorded refusal. Lit Beta(2,10) mean 0.17; Jev ~0.33 (single veto holder, ... |
| p_ref_pers | mixture: 0.7 x Beta(1.2, 12) + 0.3 x Beta(1, 19) | C | F2: same, personalist inner circle, selected for loyalty after purges. Wannsee 0 of 15 moral objections (verified); Stalin CC 70% arrested 1934-39; Saddam 1979. Lit Beta(1.2,12) mean 0.09; Jev ~0.05 |
| h_purge | U(2, 8) | B/C | F2: half-life (y) of the convergence of a new autocracy's refusal share toward the autocratic value (Stalin 1934-39, Saddam 1979, Turkey post-2016) |
| r_neg | U(0.2, 0.6) | C | F2 bug fix: absolute refusal of LETHAL NEGLECT relative to refusal of killing. Officials who would not order killings enforced lethal neglect (Holodomor, Great Leap, Irish famine, Bengal 1943; Bandura 1999). Round 2 made every ... |
| kappa_N | U(0.05, 0.3) | low | neglect moral cost relative to killing |
| q_ol | U(0.5, 0.67) | C | F1 OLIG: weighted share of the collective leadership needed to move to a HARSHER option (bargaining; Svolik 2012 power-sharing). Milder moves need a simple majority |
| s_tilt | U(0, 1) | J | F1 PERS: selection tilt of the leader toward the harsh end of the coalition's preference distribution (leader at quantile u^(1/(1+s))) |
| v_eff | U(0.05, 0.3) | C | F1 PERS: P(inner-circle veto succeeds) at fully human security/admin; scales with h_sa. Holodomor, T4, Khmer Rouge: no inner-circle veto; Great Leap veto ~3 y late (1962) |
| k_pz | U(0.02, 0.1) | C | F1: hazard/yr of an oligarchy turning personalist at fully automated security/admin (x(1-h_sa)); personalist share of autocracies rose to 40-52% (GWF, Kendall-Taylor et al. 2016) |
| conc_k | U(0.5, 1.5) | J | A6: log-normal dispersion of members' control over automated kinetic force (faction weight = control share as security/admin automate; money and labor-based resources count for nothing) |
| q_I | mixture: 0.7 x Beta(2, 8) + 0.3 x Beta(4.5, 5.5) | B/C | F3: P(systematic defection) under counterinsurgency orders. Armed challengers make forces close ranks (Stephan & Chenoweth 2008, verified). Lit Beta(2,8); Jev ~0.45 |
| q_C | Beta(2.5, 7.5) | C | F3: P(systematic defection) under collective-punishment orders (Mau Mau, Herero, Guatemala: mostly out-group or stacked units) |
| q_X | Beta(5, 3.5) | J/C | F3: P(systematic defection) under orders to kill or starve the general majority population (forces' own kin among the targets; Khmer Rouge peak ~22-25% via class split). Lit and Jev (~0.55) agree |
| m_stack_pers | U(0.4, 0.8) | B | F3: defection multiplier for personalist regimes (coup-proofing, ethnic stacking: Makara 2013, Lee 2015; Syria 2011-13) |
| m_stack_olig | U(0.7, 1) | B | F3: same, oligarchic/party regimes (Egypt 2011 army as institution) |
| d_def | U(0.3, 0.7) | C | F3: share of HUMAN coercive units lost in a systematic breakdown |
| c_req | U(0.4, 0.7) | C | F3: share of coercive capacity an order needs; it fails if d_def x human share > 1 - c_req. A4: once automated systems carry the order the executor check is gone (a threshold, not a slow fade) |
| p_oust | U(0.5, 0.8) | C | F3: P(leader/faction ousted after a failed X or C order; policy resets to status quo) |
| OR_def | lognormal (median 4, sd 0.4) | B | F3: insurgent success odds multiplier from systematic defection (Stephan & Chenoweth 2008: defections more than quadruple success, verified). Replaces def_mult |
| C_oust | lognormal (median 0.3, sd 0.8) | J | F3: members' anticipated cost of ouster, output-share equivalent, weighted by P(order fails) |
| m0 | U(0.3, 0.6) | moderate | cost of decent provision / output in 2026 terms |
| c_W | U(0.15, 0.4) | low | warehouse cost relative to serve |
| c_R | U(0.7, 1) | low | rentier cost relative to serve (full provision, no political rights) |
| w_R | U(0.45, 0.7) | low | public welfare under rentier rule relative to serve (Gulf citizens: rich, no vote) |
| thk_R | U(0.5, 0.9) | B-/C | residual revolt threat under rentier rule relative to warehouse (Saudi 2011 buy-off worked; Bahrain excluded group revolted) |
| tau0 | lognormal (median 0.03, sd 0.9) | low | expected loss from an aggrieved population / output per yr with human security |
| E0 | lognormal (median 0.1, sd 0.8) | low | legitimacy + international pressure / output at full rival leverage |
| intl | U(0, 1.5) | very low | extra international response (sanctions, war risk) to executing depopulation, multiple of E0 term |
| v0 | lognormal (median 0.01, sd 1.1) | J/C | F4: land/resource value freed by removing population, share of output (urban land value depends on population; settler-colonial land: Wolfe 2006, Natives Land Acts 1913/1936, US Indian removal) |
| v1 | lognormal (median 0.03, sd 1) | very low | Ricardian scarcity rent as the terrestrial ceiling binds (50% mass at zero) |
| r_disc | U(0.03, 0.1) | moderate | discount rate for one-time acts |
| phi_stigma | Beta(1.5, 3.5) | very low | recurring share of killing's moral/legitimacy cost |
| s_sw | lognormal (median 0.25, sd 0.8) | low | one-time cost of switching provisioning regime, output-years (0.07-0.9; round 1 used 0.1, which with no confirmation step let blocs ratchet into harsh options) |
| p_exec | U(0.75, 0.95) | J | P(an ordered depopulation is carried out, operationally), EXCLUDING security-force defection, which is now explicit (F3). Round 2 U(0.7,0.95); Jev grid refusal at zero human security 0.08-0.15 -> 0.85-0.92; mixture. Failure ... |
| x_thr | U(1, 3) | C | threat multiplier during execution (a population facing extermination resists harder than a warehoused one, but targeted populations historically rarely mounted effective resistance) |
| p_small | U(0.1, 0.3) | C/very low | P(once security and admin are automated, the deciding circle shrinks to 1-7 people) per consolidated autocracy; otherwise >=21 (selectorate data; Jev assumes ~500) |
| lag_dec0 | U(1, 5) | low | years from closure to strategic decision at 2026 decision speed |
| spd_max | lognormal (median 2, sd 0.5) | weak | strategic decision-speed compression at full AI R&D automation (r8d) |
| Tn | lognormal (median 7, sd 0.5) | low-moderate | years of neglect to 10% population loss (Irish famine 12% in ~5 y) |
| lagX | U(0.5, 3) | low | years from executed depopulation decision to 10% loss |
| a_vote | U(0.15, 0.45) | low-moderate | welfare weight added per unit of D_dem |
| k_inst | U(1, 4) | low | moral/legitimacy cost multiplier per unit of D_dem |
| griev_trend | U(0.03, 0.1) | A polls, C extrapolation | initial yearly rise of anti-AI grievance attitudes (Pew 31%->39% 'more harm' in one year). F7: logistic toward g_max instead of a hard cap at 0.55 |
| g_max | U(0.8, 0.95) | C | F7: ceiling of the grievance-attitude share. Public-opinion saturation: Gallup US Congress disapproval peaked ~85-90% (approval 9%, Nov 2013) [M] |
| att_max | U(0.5, 0.7) | C | F7: ceiling of attitudinal support for political violence (replaces the 0.5 cap). Upper range in populations in open conflict: PCPSR polls, support for armed struggle ~50-60% [M] |
| cr_hl | U(1, 3) | C | F8: half-life (y) of a crisis provision response once grievance stops rising (CARES Act 2020 large but temporary) |
| s_nino | U(0.2, 0.5) | B | A7: ecological-stress index during the record 2026-27 El Nino, until mid-2028 (NOAA CPC 10 Sep 2026: Nino-3.4 +1.8 C, 75% chance of a historic event) |
| k_intl | U(0, 0.04) | B sign, J size | A7: yearly decay of international pressure E0 (US withdrawal from 66 international organizations, Jan 2026; UNGA-81 walkouts; 'breakdown' not verified) |
| r_ab | U(0.3, 0.7) | low | share of displaced labor reabsorbed into new human work at 2026 breadth |
| k_ineq | U(0, 1) | low | grievance amplification from visible inequality |
| pg_red | lognormal (median 0.3, sd 0.45) | C | fraction of grievance removed by full provision (status loss persists): 0.1-0.6 |
| pr_red | mixture: 0.6 x U(0.3, 0.7) + 0.4 x U(0.05, 0.4) | B-/Jev | fraction of revolt hazard removed by full provision. r9c (Saudi 2011 buy-off) U(0.3,0.7), weight 0.6; Jev grid U(0.05,0.4) (almost no provision effect), weight 0.4. Reported as a disagreement |
| k_resp | U(0.2, 0.8) | A- direction, C size | democratic provision response to grievance |
| k_buy | U(0.1, 0.5) | B- | autocratic buy-off of grievance while coercion still needs humans (Saudi 2011) |
| h_beh0 | lognormal (median 0.005, sd 0.6) | low | behavioral hostile faction share (would join sabotage/violence), 2026 |
| att_trend | U(0, 0.04) | medium | yearly rise of attitudinal support for political violence (PRRI 15%->23% 2021-23) |
| e_att | U(0.3, 0.7) | C | elasticity of behavioral hostility to attitudinal support (attitudes rose without proportional organized violence) |
| e_g | U(0.5, 1) | C | elasticity of hostility to the grievance state Gv |
| mdisp | lognormal (median 1.5, sd 0.25) | low | hostile-share multiplier per 10 pp displaced (Swing riots; GTI) |
| Hmax | U(5, 10) | C | round-2 saturation of relative hostility; used only in the caps_v4 variant |
| Habs | U(0.05, 0.2) | C | F7: saturation of the BEHAVIORAL hostile share (would join sabotage/violence), absolute share of adults. Replaces the relative Hmax 5-10 and the 50%-displacement cap. Active participation in the largest revolutions/insurgencies ... |
| p_svr_hi | mixture: 0.6 x U(0.15, 0.5) + 0.4 x U(0.12, 0.35) | C/Jev | P(sustained violent resistance over ~10 y / 30% displaced, provision 0.2, high-capacity state). r9c U(0.15,0.5) weight 0.6; Jev grid U(0.12,0.35) weight 0.4 |
| p_svr_weak | U(0.35, 0.7) | B-/C | same, low-capacity state |
| lam0_hi | lognormal (median 0.003, sd 0.5) | B | 2026 hazard of a NEW sustained insurgency at zero displacement, high-capacity bloc (UCDP onset 0.1-0.5%/yr for high-capacity states; none in US/China for decades) |
| lam0_weak | lognormal (median 0.012, sd 0.5) | B- | same, low-capacity bloc of 2-3B people (new campaigns beyond the 2026 baseline) |
| elec | U(0.3, 0.7) | B | revolt risk diverted to elections per unit D_dem |
| aU | U(0.3, 1) | B- | anocracy excess onset risk (inverted U, Hegre et al. 2001) |
| d_surv | U(0.2, 0.6) | C | onset hazard factor at fully automated security/surveillance (Xu 2021 digital repression; Xinjiang) |
| rd | U(0.4, 0.8) | B- | P(consistent high-capacity repression suppresses sustained resistance within 5 y) |
| k_auto | U(0.3, 0.9) | C | extra suppression effectiveness of automated security |
| coin_win | U(0.25, 0.75) | B/C | incumbent win rate vs insurgency |
| ins_dur | lognormal (median 8, sd 0.4) | B | mean insurgency duration, years |
| def_mult | U(0.15, 0.6) | C | insurgent success odds multiplier when security fully automated |
| p_dem_suc | U(0.2, 0.35) | B | P(a successful violent campaign leads to democracy; otherwise a new narrow autocracy) (Chenoweth-Stephan) |
| k_bf | U(0.2, 1) | C | backfire from repression that fails to deter; also added after collective punishment |
| dfd | U(0.3, 0.7) | C | hostility damping after a defeated revolt (decays over 5 y) |
| ins_mort | lognormal (median 0.0003, sd 1) | C | crackdown/insurgency deaths per year of active insurgency, fraction of population |
| p_lcp | U(0.15, 0.6) | C | P(lethal collective punishment during an insurgency / labor unneeded, weak external check) |
| f_lcp | lognormal (median 0.03, sd 0.9) | C | share of the aggrieved regional population killed per episode (Mau Mau ~1-2% of Kikuyu, Gaza ~3%, Herero 65-80%) |
| m_d | lognormal (median 0.002, sd 0.5) | B- | excess mortality/yr of status-stripped, welfare-dependent displaced adults (deaths of despair ~0.2-0.3%/yr in the affected group; Native American life-expectancy gap ~0.3-0.5%/yr) |
| hgain | U(0, 0.5) | low | offset of despair mortality by AI-era health gains at full automation |
| tau_sab | lognormal (median 0.005, sd 1) | low | sabotage cost to automated infrastructure / output per yr at reference hostility |
| ins_thr | U(1, 3) | C | threat multiplier during active insurgency |
| host_ins | U(0.05, 0.25) | C | F4: coalition hostility added by active insurgency (insurgent threat radicalizes elites toward eliminationist policy: Valentino, Huth & Balch-Lindsay 2004; Harff 2003; Straus 2006; Kteily et al. 2016) |
| host_H | U(0, 0.15) | C | coalition hostility added by public hostility; F7: smooth saturation host_H*(1-exp(-(Hr-1)/3)) instead of a cap at 4x |
| h_on | U(0.04, 0.07) | M | autocratization onset hazard per democracy-year, all countries (V-Dem: 10 new of 179) |
| h_bd | lognormal (median 0.005, sd 0.6) | M | breakdown hazard of a rich democracy at intact leverage (Przeworski et al. 2000) |
| M_lev | lognormal (median 5, sd 0.6) | L | erosion hazard multiplier as leverage goes 1 -> 0 |
| e_rate | U(0.04, 0.12) | M | LDI decline per year during an episode (US -0.218 since 2023) |
| p_uturn | U(0.5, 0.8) | M | P(episode reverses before breakdown / leverage intact) |
| conc | U(0.3, 0.9) | low | concentration of AI/robot ownership |
| em_jump | U(0.02, 0.1) | low | D_dem drop from emergency powers at war/insurgency onset |
| c_trend | U(0.05, 0.12) | M | log trend of armed-conflict intensity (GPI 2008-2025) |
| c_max | U(1.5, 4) | judgment | cap on conflict-intensity index relative to 2026 |
| w_pair | lognormal (median 0.007, sd 0.6) | low (judgment) | US-China war hazard per year at 2026 intensity |
| w_row | lognormal (median 0.015, sd 0.6) | low (judgment) | major-war hazard per year for a non-US/China bloc at 2026 intensity (x0.5 Europe, x1 Russia_MENA, x0.8 South Asia, x0.6 Global South) |
| war_len | U(2, 6) | low | war duration, years |
| ukr_rem | U(0.5, 4) | low | remaining years of the Russia-Ukraine war from Oct 2026 |
| w_mort | lognormal (median 0.0008, sd 0.8) | low | war deaths per war-year as a fraction of a whole bloc's population (Ukraine ~1%/yr for the belligerent; blocs are larger) |
| p_nuc | lognormal (median 0.02, sd 0.6) | very low | P(nuclear use / a major war of a nuclear-armed bloc) |
| f_nuc | U(0.02, 0.3) | very low | bloc population share killed if nuclear weapons are used |
| m_war | U(0.2, 0.7) | L/M | moral cost of killing in war/insurgency vs peacetime |
| mc_ai | U(0.5, 0.9) | L | moral-cost factor at fully AI-mediated targeting |
| eco_year | U(2045, 2100) | low | year ecological stress reaches 'severe' (ETR 2025) |
| eco_mult | lognormal (median 1.5, sd 0.35) | M | conflict multiplier at severe ecological stress (1.2-4) |
| eco_land | U(0, 2) | very low | rise in land/resource value share at severe ecological stress (50% mass at zero) |
| p_id | lognormal (median 0.045, sd 0.6) | L | P(depopulation/successionist ideology taken up by a closed bloc's rulers within 9 y, no war; war x2.5). Calibrated so P(US or China bloc by 2045) ~0.08 (r9d) |
| id_hl | U(10, 20) | L | half-life of a ruling ideology (regime turnover, generational change), years |
| id_share | U(0.1, 0.3) | L | coalition hostility share added when that ideology is fully held (builds over ~4 y) |
| T_full | U(2, 15) | J | A8: years for an executed depopulation carried by automated force plus economic strangulation to reach >=99.9% loss if unconstrained (hazard ramps linearly from the lagX rate); no precedent at this scale, so wide (A10) |
| dL_means | U(-2, 6) | J | A8: horizon doublings beyond M3 (90% software capability) at which a means of rapid mass killing is available to a closed bloc's coalition (abstract availability; probit width 1 doubling) |
| h_use | U(0.2, 1) | J | A8/A9: yearly hazard that a coalition executing depopulation uses such a means once available |
| f_eng | U(0.5, 0.99) | J | A8: share of the remaining targeted population killed by one use (abstract) |
| p_tot0 | U(0.2, 0.6) | J | A11: P(the designation targets near-total removal from the start); otherwise an initial partial target f0 |
| f0 | U(0.3, 0.9) | J | A11: initial partial target (share of population) when the designation is partial |
| k_esc | U(0.1, 1) | J | A11: yearly hazard of escalating a partial designation to near-total, per unit of perceived revenge threat (grievance/0.5 x (1 + active insurgency)): any free surviving community is a seed that can organize and take revenge ... |
| rem | U(0.0003, 0.001) | scenario | A11: captive remnant kept without rights (scenario: ~8 million of 8 billion = 0.1%) |
| k_col | U(0.2, 1) | J | A9: yearly hazard of tacit collusion (economic or hot war on each other's populations) between two coalitions that both execute depopulation, when incentives favor it |
| b_col | lognormal (median 1, sd 1) | J | A9: rulers' value of collusion (cover, elimination of the other bloc's human seed), relative units |
| c_self | lognormal (median 20, sd 1) | J | A9: rulers' value of their own survival in the same units; collude iff b_col > (1 - s_bunk) x p_nx x c_self |
| s_bunk | U(0.5, 0.95) | J | A9: rulers' own survival probability in a nuclear exchange given bunker preparations |
| p_nx | U(0.05, 0.3) | J | A9: P(a collusive war goes nuclear) |
| f_nx | U(0.2, 0.7) | J | A9: share of each colluding bloc's remaining population killed by a nuclear exchange |
| w_col | U(0.02, 0.1) | J | A9: yearly deaths of the remaining population from collusive economic/hot war (on top of the executing bloc's own means) |

**PRIORS_B** (15 parameters)

| Parameter | Distribution | Evidence | Basis |
|---|---|---|---|
| sel_top | U(0.1, 0.6) | J (C anchors) | B1: moral-cost AND refusal multiplier for the person at the top of an autocratic coalition (selection: those who fight their way to that much power have less of the brake). Members of an autocratic coalition get sel_top^0.5. ... |
| id_mor | U(0.3, 0.8) | C/J | B1: share of the remaining moral cost removed when a depopulation ideology is fully held (reframing as kindness / ecological reset: moral justification and euphemistic labelling, Bandura 1999) |
| k_prg | U(0.05, 0.3) | C | B2: yearly purge hazard per coalition member at full incentive (leader holds all force, needs no human staff). Anchors: 70% of the 1934 CC arrested by 1939 (~0.24/yr); Great Purge removed 3 of 5 marshals and ~13 of 15 army ... |
| prg_c0 | U(0.1, 0.4) | C/J | B2: share of the purge incentive present even while the leader still needs competent human staff (loyalty-competence trade-off, Egorov & Sonin 2011; purges happened in fully human regimes). The rest scales with (1 - human share ... |
| c_cc | U(0.1, 0.5) | C | B2: P(counter-coup) per purge event, times the rest of the coalition's share of force (1 - S_L). Svolik 2012: insiders remove ~2/3 of ousted autocrats; Sudduth 2017: dictators purge when elites' capacity to oust them is ... |
| k_par | U(0.5, 3) | J | B2/B4: purge-incentive multiplier per 10% of the population already killed deliberately (scenario: 'guilt turns to paranoia'; fear of retribution after atrocities) |
| k_extp | U(0, 0.8) | C/J | B2: reduction of purge incentive when a rival of comparable automated force exists (Goldring: purges more likely when foreign and revolutionary threats are low) |
| k_am | lognormal (median 10, sd 0.8) | J | B3/B5: force multiplier of automated over human-staffed forces at equal output (Ukraine: drones cause ~60-80% of front-line casualties, r9a [K]; colonial tech asymmetry, e.g. Omdurman 1898 [M]). Kinetic power M = output x (1 + ... |
| k_ret | U(0.5, 3) | J/C | B4: multiplier on the rulers' perceived threat from survivors per 10% of population already killed deliberately (also scales A11 escalation). Archigos: most leaders removed irregularly are exiled, jailed or killed (research/m5) |
| k_xb | U(0.1, 1) | J | B5: yearly hazard that an executing closed coalition extends depopulation to a bloc it can overpower, when its payoff test passes |
| dom_thr | U(0.7, 0.95) | J | B5: share of combined kinetic power (aggressor / (aggressor + target)) the aggressor needs before attacking |
| p_ret0 | U(0.3, 0.9) | J | B5: P(a nuclear-armed target retaliates) at parity; falls as (1 - dominance) since an overwhelmingly dominant automated force can suppress a deterrent (counterforce, defence). Arsenals: FAS 2026 (US 3,700, Russia 4,400, China ... |
| k_rep | U(0.5, 2) | J | B5: yearly hazard of repelling a cross-bloc campaign, times the target's share of combined kinetic power |
| cn_ppp | U(1, 2) | C | B3/B5: multiplier on China's military-expenditure share for purchasing-power parity (market-rate SIPRI figure understates Chinese military output) |
| k_kit | lognormal (median 0.3, sd 0.7) | J | B6/F6: draw of fixed automation kit on the shared robot-input budget (magnets, chips, actuators) per worker-equivalent, relative to a general-purpose robot |

**LEVER_PRIORS** (36 parameters)

| Parameter | Distribution | Evidence | Basis |
|---|---|---|---|
| lv_s_max | ('logu', 0.01, 0.1) | C | network share of world compute at full mobilisation (a = 50%): incentives plus ideology; consumer/edge usable 0.3-2M H100e of ~29M DC stock plus joined DC capacity (r13a) |
| lv_E | lognormal (median 1, sd 0.45) | low | governance wildcard: innovation efficiency per unit compute vs centralized, central 1 (0.5-3): OSS/open-weight record, no evidence of higher frontier R&D efficiency (r14b) |
| lv_spd | ('logu', 0.2, 1.0) | low-medium | governance wildcard: decision speed vs a centralized/autocratic actor, 0.5 (0.2-1): DAO 7-day minimum cycle (Compound docs) vs executive decisions (r14b) |
| lv_M | ('tri', 1.0, 1.3, 2.0) | low | relative amortization advantage on covered tasks vs centralized providers (who also cache/distil/reuse) (r14b) |
| lv_cmax | ('tri', 0.5, 0.7, 0.85) | low | coverable ceiling of task volume (AEI bottom 80% of categories = 10.5-12.7% of use; 31% repeat queries; 44% routine jobs) (r14b) |
| lv_tau | ('tri', 1.0, 2.0, 4.0) | low | coverage growth time constant, use-years (modelling assumption; Zipf task distribution) (r14b) |
| lv_lag_pre | ('tri', 1.1, 3.5, 9.0) | medium | network's own novel-task lag before any cut, months: open-weight lag 3.5 (1.1-5.3), consumer-GPU lag 6-12 (Epoch) (r14b) |
| lv_L27 | ('tri', 17.0, 27.0, 46.0) | low-medium | lag per 10x compute gap under closure, months (derived from 8-month algorithmic halving, Ho et al. 2024) (r14b) |
| lv_p_oc | U(0.2, 0.6) | J | P(some open-weight releases continue after centralized providers cut frontier access) (strategic choice of a few firms/one state, m7) |
| lv_dlag_oc | U(3, 9) | J | extra lag (months) when only lower-tier open releases continue |
| lv_h_net | U(0.3, 0.9) | J | share of network activity that stops if participants withdraw (their hardware, review, keys): labour-like leverage under A6 |
| lv_y_h | U(0.5, 1) | J | share of network value reaching human participants as income (rest: energy, chips) |
| lv_s_acc | U(0, 0.5) | J | share of network livelihoods that survive a state's deliberate strangulation of land/energy/food (m7: parallel economies depend on access) |
| lv_h0_dem | ('tri', 0.002, 0.01, 0.03) | medium | crackdown hazard/yr, small low-visibility network in a democracy (Christiania since 1971; WIR 90 years) |
| lv_h0_aut | ('tri', 0.02, 0.05, 0.1) | low-medium | crackdown hazard/yr, small network in an autocracy (Falun Gong pre-1999; China crypto escalation 2013/2017/2021) |
| lv_k | ('tri', 0.4, 0.7, 1.2) | low | size elasticity of the hazard (crypto bans 23 -> 51 countries as market cap grew 5-10x, 2018-2021) |
| lv_thr_aut | ('tri', 0.005, 0.02, 0.1) | low-medium | autocracy threat threshold, share of activity (Falun Gong ~70M > CCP, banned July 1999) |
| lv_thr_dem | ('tri', 0.01, 0.05, 0.15) | low | democracy threshold where the network erodes tax/monetary control (Worgl, Liberty Dollar, Tornado Cash) |
| lv_p_thr | ('tri', 0.5, 0.6, 0.8) | medium | P(suppression) once above the threshold (m7; crypto bans; Falun Gong) |
| lv_T_thr | U(1, 5) | J | years over which p_thr is realised above the threshold (Falun Gong ~3 months after Zhongnanhai; Worgl ~1 y; crypto bans years) |
| lv_eff | U(0.3, 0.8) | low | share of realised adoption removed by one crackdown (China mining 34% -> 0% -> 14-20% underground; Tornado Cash usage fell but did not stop) (m7 #26) |
| lv_rho0 | U(0.3, 0.7) | C/J | recovery rate/yr after a crackdown at median governance speed (China Bitcoin mining back to ~half within ~1-2 y) |
| lv_R_gp | ('tri', 0.0, 0.1, 0.25) | medium | max hazard reduction from foreign public support, great power acting on a core interest (Hong Kong 2020, Tibet, Xinjiang, Kurdistan 2017) |
| lv_R_dep | ('tri', 0.2, 0.4, 0.6) | low-medium | same, repressor dependent on the supporters (Levitsky-Way linkage/leverage; South Africa, East Timor, Solidarity) |
| lv_sev | ('tri', 0.15, 0.35, 0.5) | low | reduction of crackdown severity by foreign attention (Krain 2012; Hafner-Burton 2008 caveat) |
| lv_e | ('logu', 0.5, 2.0) | low | exponent on foreign publics' remaining leverage (structural inference) |
| lv_Ty | ('tri', 4.0, 8.0, 15.0) | low-medium | years to majority foreign favourability via culture (Hallyu 1997-2010s; Cold War cultural diplomacy) |
| lv_rev | ('tri', 0.1, 0.25, 0.4) | medium | favourability reversal after a hostile event, own public of the cracking-down state (Japan affinity to Korea 63% -> 39%; Pew US 64 -> 22) |
| lv_cut | ('tri', 0.5, 0.7, 0.9) | medium | effectiveness of an autocratic state cutting the cultural channel (China Hallyu ban after THAAD; Great Firewall) |
| lv_V | ('tri', 2.0, 5.0, 20.0) | low-medium | visibility/collective-action hazard multiplier (King-Pan-Roberts 2013; Davenport 2007; Rajneeshpuram) |
| lv_p_sc | U(0.3, 0.8) | J | P(self-governing enclaves are read as a sovereignty claim by the host state) |
| lv_p_ss | ('tri', 0.7, 0.85, 0.95) | medium | P(suppression / sovereignty claim within reach) (Rose Island 55 days; Kirkuk 21 days; Minerva; Catalonia) |
| lv_lag_ss | ('tri', 0.05, 0.15, 1.0) | medium | years from claim to suppression (Kirkuk 21 d, Rose Island 55 d, Falun Gong ~3 months) |
| lv_k_seed | U(0, 0.3) | J | A11 no-witness logic: rise of perceived revenge threat per 1% of the population living in self-sufficient enclaves (cap 10%) |
| lv_claw | U(0.3, 1) | C | benefit-reduction (claw-back) rate of state provision against network income: means-tested programmes withdraw 0.3 (SNAP) to 0.55 (UK Universal Credit) to 1.0 (SSI, unearned income) per unit of other income |
| lv_rho_cl | U(0, 0.1) | J | recovery rate/yr after a crackdown in a CLOSED autocratic bloc (regime controls energy, compute, land): Falun Gong inside China has not recovered since 1999; China's mining recovery relied on globally mobile hardware and capital |

**LEVER_PRIORS2** (24 parameters)

| Parameter | Distribution | Evidence | Basis |
|---|---|---|---|
| lv_kc | U(0.5, 1) | J | L1: network compute per unit of activity relative to the centralized economy (inference-heavy; the centralized side also spends 30-50% of compute on frontier training/R&D) |
| lv_eps_lab | ('logtri', 0.5, 1.0, 2.0) | low-medium | L2: elasticity of frontier-lab capex to expected revenue (capex ~5-10x AI revenue, debt/growth-contingent finance: OpenAI ~$13B 2025 revenue vs ~$1.4T commitments; telecom capex -50-60% 2000-02) |
| lv_eps_hyp | ('tri', 0.2, 0.4, 0.7) | medium-low | L2: elasticity of cash-flow-funded capex (hyperscalers, industrial automation) to revenue relative to capital (Fazzari-Hubbard-Petersen 0.3-0.6; Meta 2022) |
| lv_lag_cx | ('tri', 0.5, 1.0, 1.5) | low | L2: capex response lag, years (telecom bust, 2022 tech) |
| lv_g_eff | U(1.4, 2.6) | low-medium | L2: log growth/yr of the input whose level capex sets: training compute 4-5x/yr (ln 1.4-1.6) if algorithmic progress scales with experiment compute, up to compute x algorithms ~13x/yr (ln 2.6) if it does not (Epoch; Ho et al. ... |
| lv_l4 | ('tri', 0.5, 0.8, 1.2) | medium/low | L4: centralized revenue lost per unit withdrawing customer share when a substitute exists (Bud Light -25-30% peak, ~-40% persisting, AB InBev US revenue -13.5%; Montgomery; BDS ~0 without substitute) |
| lv_pers | ('tri', 0.3, 0.6, 0.9) | low-medium | L4: persistence of a withdrawal after 2 years (Bud Light; Chinese boycotts of Lotte/Hyundai) |
| lv_kpol | U(0.2, 0.6) | J | L4: political weight of customer leverage relative to labour leverage (revenue loss alone did not win Montgomery or apartheid: courts and elite defection were needed) |
| lv_xs | U(0.2, 0.3) | C | L7: export share of a bloc's revenue exposed to cross-bloc withdrawal (world exports ~29% of GDP) |
| lv_mv | ('tri', 0.1, 0.2, 0.3) | low | L5: share of frontier talent willing to move (about half of OpenAI's safety team left in 2024; 97% letter as the solidarity ceiling) |
| lv_el5 | ('tri', 0.1, 0.3, 0.5) | low | L5: elasticity of the centralized capability rate to its top-talent share before R&D automation (OpenAI letter; Anthropic at the frontier ~2 years after the split; $1-100M packages) |
| lv_pcm | ('tri', 0.6, 0.7, 0.8) | low-medium | L6: P(crackdown takes the capture/regulate form / network share > 15%) (China 2020-23 subordinated platforms, ~$1T value lost; India demonetisation 86% of currency, government re-elected) |
| lv_kap | U(0.3, 0.8) | J | L6: depth of capture, share of the network's control/refusal capacity subordinated to the state |
| lv_eff_cap | U(0, 0.2) | J | L6: share of realised adoption lost in a capture (platforms kept operating in China after 2021) |
| lv_rcap_dem | U(0.05, 0.2) | J | L6: capture reversal rate/yr in a democracy (Prohibition repealed after 13 years; courts) |
| lv_rcap_aut | U(0, 0.1) | J | L6: capture reversal rate/yr in an autocracy (China eased in 2023 but kept golden shares) |
| lv_dm | U(1, 2) | low | L6: supply-chain multiplier of a full ban's direct cost (demonetisation PMI 54.5 -> 46.7) |
| lv_spd8 | ('logtri', 2.0, 3.0, 10.0) | medium/low | L8: speed multiplier on the organising part of a collective response (Egypt 18 days, Tunisia 28; OpenAI letter 3 days; IT Army 2 days; DAO fork 33 days; rulemaking 1-2 years) |
| lv_dur | U(0.7, 1) | low | L8: durability of digitally organised action (Tufekci 2017; Chenoweth 2020 post-2010 decline) |
| lv_forg | U(0.3, 0.7) | J | L8: organising share of a collective response's duration (the rest is courts, elections, institutions) |
| lv_rec9 | ('logtri', 1.0, 1.5, 4.0) | medium-low | L9: recruitment multiplier from legitimacy on recovery after a crackdown (nonviolent campaigns ~4x participants) |
| lv_bf | ('tri', -0.1, 0.0, 0.2) | medium | L9: net repression backfire on ban effectiveness, mean ~0 (Stephan & Chenoweth 2008 Table 3: regime violence no significant effect within nonviolent campaigns) |
| lv_defup | ('tri', 2.0, 3.0, 4.4) | medium | L9: defection uplift (RRR) on success, human-staffed share only (Stephan & Chenoweth 2008: 4.44 overall; nonviolence does not raise defection probability) |
| lv_pdoc | U(0.32, 0.52) | medium | L9: P(defections occur) in a campaign (32% of successful violent, 52% of successful nonviolent campaigns) |

**LEVER_PRIORS3** (16 parameters)

| Parameter | Distribution | Evidence | Basis |
|---|---|---|---|
| lv_dnet | U(0.05, 0.3) | J | R3/C3: share of a repression order's execution that depends on capability the network supplies and the state cannot route around before the order runs (civilian logistics, energy, comms; the Reichsbahn and Rwanda's radio show ... |
| lv_tax | U(0.5, 1) | J | R3/C4: share of network activity inside the state's tax base (informal economy ~0, card/platform income ~0.8-1, crypto reporting rules phasing in) |
| lv_ccs | U(0.1, 0.3) | J | R3/C4-L1: compute and energy cost share of activity in an AI-heavy economy (today DC capex ~0.5% of world GDP; capex runs 5-10x AI revenue during the build-out); the network pays kc x ccs of its value for hardware, so y_h <= 1 - ... |
| lv_psic | U(0.5, 0.9) | J | R3/L2: share of the network's hardware/energy spending that goes to centralized suppliers (TSMC, Nvidia, utilities) |
| lv_sub | U(0.2, 0.45) | C/J | R3/L4: share of participants' remaining spending on centralized goods that has a substitute or can be deferred (US CEX: housing 33%, transport 17%, food 13%, health 8% are hard to withdraw) |
| lv_avote | U(0.2, 0.4) | J | R3/L6: network share above which a democracy no longer bans it outright (participants as a voter bloc); P(ban / crackdown, democracy) x max(0, 1 - a / a_vote) |
| lv_kcost | U(0, 3) | J | R3/L6: weight of the anticipated self-inflicted output loss (eff x a x dm) on choosing capture/regulation over a ban: P(ban) x exp(-k_cost x loss) (China 2021 chose capture of platforms worth ~$1T; India's demonetisation shows ... |
| lv_kphys | U(0.2, 0.7) | J | R3/closure: network share of the core physical chain relative to its overall share (fabs and mines are capital-concentrated; distributed solar and owner-operator logistics are not; security sector 0 under A3) |
| lv_gc | U(0.2, 0.6) | low | R3/L1: log growth/yr of the centralized compute stock over the period (2-3x/yr today, slowing) |
| lv_dep | U(0.15, 0.25) | C | R3/L1: depreciation of compute hardware/yr (4-6 year accounting lives) |
| lv_wlab | U(0.3, 0.5) | J | R3/L1: frontier-lab share of centralized compute (global sales, eps_lab); the rest is hyperscaler/enterprise compute funded from bloc revenue (eps_hyp) |
| lv_st | U(0.05, 0.2) | J | R3/L1: state-owned compute (A3 security automation, national labs) as a share of baseline centralized compute; exempt from revenue starvation |
| lv_mig | U(0.3, 0.7) | J | R3/L6: share of banned network activity that migrates back to centralized firms (the rest is lost output for a while) |
| lv_Tre | U(0.5, 2) | low | R3/L6: years for lost output after a ban to be re-absorbed (India demonetisation: ~1 year) |
| lv_dur3 | U(0.5, 0.9) | low | R3/L8: success/durability factor of digitally organised action (nonviolent campaign success ~65% in the 1990s vs ~34% in the 2010s, Chenoweth 2020; Tufekci 2017): faster onset, less success, so the recovery multiplier is centred ... |
| lv_pdoc3 | U(0.15, 0.35) | low | R3/L9: unconditional P(security defections) across campaigns, derived from 52%/32% among successful campaigns, a 0.34-0.53 success base and fewer defections among failures (J-derived) |

**LEVER_PRIORS4** (5 parameters)

| Parameter | Distribution | Evidence | Basis |
|---|---|---|---|
| lv_fnode | U(0.5, 0.9) | J | U1: share of a ban's calibrated adoption loss that is physical removal of hardware or node connections (stops activity 1:1); the rest (P2P partition, user exit) is survivable for an autonomous network. China mining 2021 (hardware ... |
| lv_y_h4 | U(0.9, 1) | J | U2: payout to households, all output except service fees that fund the treasury (network premise) |
| lv_s_acc4 | U(0.2, 0.7) | J | U3: share of displaced people's needs still covered when a regime tries to cut them off; contracts cannot be altered, only conversion and access (exchanges, goods, token value) can be attacked (network premise) |
| lv_g4 | U(0.02, 0.06) | J | U4: growth of the log relative amortization advantage per coverage-weighted use-year (doubling every 12-35 years; Zipf: library value grows ~log of size; AWM/Voyager reuse gains) |
| lv_amort | U(0.1, 0.3) | C | U4: cost per covered task relative to solving from scratch (r14b: reusable workflows 10-30%); 1/amort caps the relative advantage |