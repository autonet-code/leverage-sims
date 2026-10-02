# r12a: Evidence for round-3 changes B1, B2, B5, B6 (m8_v4 round 3)

Date: 2026-09-30. Target: models/m8_v4.py (PRIORS_B, MIL0, IB, LAGC/LAGP; sim blocks marked "B1".."B6"), models/integrate_v4.py (B8).
Tags: [V] fetched from the source today; [K] from earlier project notes (r8a-r11a), not re-fetched; [M] standard literature figure from memory, check before publication.
Note: the WebSearch budget of this session was exhausted before this round, so only direct page fetches were possible. Items that could not be fetched are marked [M].

## B1: moral cost of those at the top

| Evidence | Figure | Source | Tag |
|---|---|---|---|
| Psychopathy prevalence, general population vs senior business roles | ~1% vs ~3-4% | Hare 1994; Babiak & Hare 2007 (Wikipedia "Psychopathy in the workplace"); Babiak, Neumann & Hare 2010, Behav. Sci. Law | [V] |
| Fearless dominance (boldness facet of psychopathy) among US presidents, historian-rated | elevated vs population; associated with rated performance and crisis leadership | Lilienfeld, Waldman, Landfield, Watts, Rubenzer & Faschingbauer 2012, JPSP 103(3):489-505 (bibliographic record [V], findings [M]) | [V]/[M] |
| Tyrants: "narcissist with severe superego deficiencies"; reality testing declines after power is secured, exaggerated paranoid responses | qualitative case synthesis | Glad 2002, "Why Tyrants Go Too Far: Malignant Narcissism and Absolute Power", Political Psychology (abstract [V]) | [V] |
| Russia's casualty tolerance in the Ukraine war | ~1.118M total casualties (UK DI, Oct 2025); >1.25M, losing ~40k/month while recruiting ~35k (Telegraph, Feb 2026); nearly 500,000 killed (BBC citing GCHQ, 27 May 2026; BBC confirmed 223,539 names) | Wikipedia "Casualties of the Russo-Ukrainian war", fetched | [V] |
| North Korea's camp system | 80,000-120,000 political prisoners; "hundreds of thousands" perished over five decades; crimes against humanity incl. extermination | UN Commission of Inquiry on Human Rights in the DPRK, 2014 (Wikipedia page on the COI) | [V] |
| Stalin's Great Purge | 681,692 executions (official) 1937-38; 3 of 5 marshals and ~13 of 15 army commanders eliminated | Wikipedia "Great Purge" | [V] |
| Famines under personalist rule | Great Leap 1959-61 continued ~3 years after Lushan; Holodomor | research/r10a | [K] |
| Distance: Milgram proximity gradient | obedience 65% remote vs ~30-40% proximity | research/r10a (mc_ai) | [V earlier] |
| Ideology as moral disengagement | moral justification, euphemistic labelling, distortion of consequences | Bandura 1999 | [M] |

Mapping (judgment, J): the model had one moral-cost distribution for all coalition members anchored on general-population wartime polls (moral_med ~ lognormal(0.3, 1.2)). B1 multiplies the moral cost of the person at the top of an autocratic coalition by sel_top ~ U(0.1, 0.6) and of the other members by sel_top^0.5; the leader's probability of absolute refusal is also multiplied by sel_top. A depopulation ideology removes a share id_mor ~ U(0.3, 0.8) of the remaining moral cost. Automation distance was already in the model (mc_ai). The evidence above is qualitative or concerns smaller acts (own-soldier casualties, political prisoners, purges, famine tolerance); there is no measurement of a leader's moral cost of killing a whole population, so the size of sel_top is judgment. The direction (lower brake at the top) is supported; the size is not measured.

Democratic leaders are left unchanged: Lilienfeld's result is on boldness (fearless dominance), not on callousness (meanness), and democratic decisions run through veto players.

## B2: consolidation from incentives

| Evidence | Figure | Source | Tag |
|---|---|---|---|
| Who removes dictators | ~2/3 of non-constitutional exits by regime insiders (205 of 316) | Svolik 2012 (research/m5) | [K] |
| Commitment problem of authoritarian power-sharing; contested vs established (personal) autocracy | theory | Svolik 2012 | [M] |
| When dictators purge | "dictators are more likely to eliminate rivals when elites' capabilities to oust dictators are temporarily low" | Sudduth 2017, Comparative Political Studies, doi 10.1177/0010414016688004 (abstract via Crossref) | [V] |
| Purges and outside threat | "dictators are more likely to purge elites when there are reduced threats from foreign adversaries or of a revolution occurring" (North Korea under Kim Jong Un; South Korea under Park) | Goldring, "Elite purges in dictatorships", doi 10.32469/10355/78075 | [V] |
| Coup-proofing | family/ethnic stacking, parallel forces, overlapping agencies; reduces coup risk, reduces military effectiveness (loyalty over competence) | Quinlivan 1999 (Wikipedia "Coup-proofing") | [V] |
| Loyalty-competence trade-off | purging competent staff has a cost; AI replaces that competence | Egorov & Sonin 2011 | [M] |
| Purge scale | 70% of the 1934 CC arrested by 1939; Great Purge above | research/m5; Wikipedia | [K]/[V] |

Implementation: each autocratic bloc has an actual coalition (21 members at start or after a breakdown; 5-9 after a narrow grab). Control of coercive force is a mix of human-network control (weight = human share of security/admin) and automated-force control (the rest), A6. The member with the largest control share leads (so the leader can change as control shifts to whoever holds the machines). Yearly purge hazard per member = k_prg x [prg_c0 + (1 - prg_c0)(1 - h_sa)] x S_L x (1 + k_par x atrocity weight) x (1 - k_extp x rival). A purge can trigger a counter-coup (P = c_cc (1 - S_L)) that removes the leader instead. The leader absorbs purged members' control. Personalist = S_L >= 0.5. The personalist decision is the leader's own ideal, with an inner-circle veto whose chance scales with the force the others still hold. No endpoint is set.

## B3: outside cost only if enforceable

Pressure from each outside bloc is multiplied by min(1, 2 M_c/(M_c + M_b)) with M = kinetic power (below). This leaves round-2 pressure unchanged when rivals are at parity or stronger, and removes it when the bloc dominates. What remains is internal conscience, carried by B1.

## B5: cross-bloc depopulation

| Evidence | Figure | Source | Tag |
|---|---|---|---|
| Military expenditure 2025 (SIPRI, USD bn) | US 954, China 336, Russia 190, Germany 114, India 92.1, UK 89, Ukraine 84.1, Saudi Arabia 83.2, France 68, Japan 62.2, Israel 48.3, Italy 48.1, S. Korea 47.8, Poland 46.8, Spain 40.2, Canada 37.5, Australia 35.3, Turkey 30, Netherlands 28.9, Algeria 25.4, Brazil 23.9, Taiwan 18.2, Singapore 17.4, Norway 17, Sweden 16.5, Indonesia 15, Colombia 14.5, Mexico 13.6, Pakistan 11.9, Iran 7.4 | Wikipedia "List of countries by military expenditures" (SIPRI 2025) | [V] |
| World total 2024 | $2,718 bn (+9.4%) | SIPRI fact sheet 2025 | [V] |
| Nuclear arsenals (FAS 2026) | US 3,700; Russia 4,400; China 620; France 290; UK 225; India 190; Pakistan 170; Israel 90; DPRK 60 | Wikipedia "List of states with nuclear weapons" | [V] |
| Automated vs human forces | drones cause ~60-80% of front-line casualties in Ukraine | research/r9a | [K] |

Bloc military shares used (MIL0): US bloc 0.39, China 0.12 (x cn_ppp U(1,2) for PPP), Europe+ 0.23, Russia/MENA 0.17, South Asia 0.04, Global South 0.05 (sums from the SIPRI figures above plus rough residuals for unlisted members, marked in code). Kinetic power M = MIL0 x output growth G x (1 + k_am x automated share of security), k_am ~ lognormal(10, 0.8) (J). Cross-bloc logic: an executing coalition with a near-total designation (pooled with colluders) attacks a bloc when its share of combined power >= dom_thr ~ U(0.7, 0.95) and b_col > (1 - s_bunk) x p_ret x c_self, with p_ret = p_ret0 x nuclear-armed x min(1, 2(1 - dominance)). Nuclear retaliation at launch kills f_nx of the remaining population in both blocs and kills the aggressor's rulers with P = 1 - s_bunk. A campaign is repelled at a yearly hazard k_rep x (target's power share). All endgame parameters are J.

## B6: physical bottlenecks and bloc heterogeneity

| Evidence | Figure | Source | Tag |
|---|---|---|---|
| Industrial robot installations 2024 | 542,000 world; China 295,000 (54%); Japan 44,500; US 34,200; Korea 30,600; Germany 26,982; stock 4.664M | IFR press release | [V] |
| Installations 2025 | 603k world, China 354k (59%) | research/r9a (IFR WR2026) | [K] |
| GPU-cluster performance | US ~3/4, China 15% (May 2025) | Epoch AI data insight | [V] |
| Humanoid shipments | 97% Chinese (1H2026) | research/r9a | [K] |
| Rare-earth processing ~90% China; advanced chips concentrated in the US bloc (Taiwan, Korea, Japan) | RE_SHARE0, CHIP_SHARE0 in code | research/r9a, r9b | [K] |

Wiring fixes (the round-2 bypasses): (1) fixed automation kit had no physical input constraint; it now draws on the same robot-input budget (k_kit ~ lognormal(0.3, 0.7) per worker-equivalent relative to a general-purpose robot); (2) M0 and C0 were applied as the full world pool to EVERY bloc; they are now world pools allocated by domestic production plus imports by purchasing power, with exporters restricting sales as they race (openness 1 - 0.7 psi); (3) security automation ignored supply under A3; it is now served first from supply. Heterogeneity: reshoring speed x industrial base IB (sqrt of manufacturing share relative to the US bloc); unsecured imports count as dependence (on the leaders), not closure; deployable capability lags the frontier by bloc (cognitive: US 0, China 0-1 y, Europe 0-1, Russia/MENA 0.5-3, South Asia 0.25-2, Global South 0.5-3; physical: China 0, US 0-1, Europe 0.5-2, others 1-4). Lag ranges are judgment anchored on the compute, robot and humanoid shares above.
