# v7 design: actors, alliances, institutions and drives

Status: working design on branch `v7-actors` (not pushed). Approved scope 2026-10-16. Every new judgment parameter is labeled J and listed in the sign-off section at the end. The published v6 files (`m8_v4.py`, `integrate_v4.py`, `m9_lever.py`) stay untouched so the paper's numbers keep reproducing; v7 lives in `m8_v7.py`, `integrate_v7.py`, `m9_lever_v7.py`.

## A. Seventeen actors

Order (the integrator keeps US = 0 and China = 1):
0 US, 1 China, 2 Japan, 3 South Korea, 4 Taiwan, 5 Western EU, 6 Eastern EU and neighbours, 7 UK, 8 Canada, Australia, NZ, 9 Russia and Central Asia, 10 Gulf monarchies, 11 Rest of MENA and the Caucasus, 12 India, 13 Rest of South Asia, 14 Southeast and other East Asia, 15 Latin America, 16 Sub-Saharan Africa.

Country membership is fixed in `research/v7_actor_inputs.md`. Each actor gets its own economy, workforce, industrial base, robot, chip and rare-earth shares, military spending, democracy score, provision level, nuclear status and capability lags, from the same sources the six-bloc model used (UN WPP, ILOSTAT, SIPRI, V-Dem, IFR, UNIDO, FAS). Where the six-bloc value was a judgment, the actor value is derived from it with the reason written next to it.

Hard-coded six-bloc logic that becomes actor-specific:
- pursuit priority (A2 keeps US and China at maximum; others get a multiplier per actor);
- the rich-democracy breakdown hazard flag;
- the ongoing Russia-Ukraine war (Russia actor; Eastern EU hosts Ukraine, so it is also at war while it lasts);
- personalist starting regimes (China, Russia, Gulf monarchies);
- wars: dyads instead of one US-China pair plus anonymous regional wars (see B).

## B. Alliances

State: an alliance matrix `Al[a, b]` in [0, 1] per pair, the strength of a security commitment in 2026 (from the alliance research), and whether each tie is intact. Ties are symmetric in existence but not in value (a patron's guarantee matters more to the client).

What alliances do:
1. **Defense and deterrence (B5).** A target's resistance to a cross-border campaign counts its own automated force plus each intact ally's force times the tie strength, unless that ally is itself executing a depopulation programme. A nuclear ally can extend deterrence: the aggressor faces retaliation from the ally with probability tie strength x p_ret.
2. **Joining wars.** When a dyad war starts, each ally of either side joins with probability equal to the tie strength (times a join factor). Allies at war share the war effects (emergency powers, ideology acceleration, war deaths).
3. **Enforcement of outside pressure (B3).** Pressure needs an enforcer. An outsider's enforcement capacity counts its own force plus its willing allies' force (a coalition can enforce what no member can alone). Allies also shield each other: an actor's pressure on its own ally is scaled down by the tie strength.
4. **Trade in robot inputs (B6).** Export restrictions under racing apply less to allies: openness toward an ally is `1 - 0.7 psi (1 - Al)`. This is friend-shoring (US chips to Japan, Chinese magnets to Russia).
5. **No attacks on allies.** A tie that is intact rules out a cross-border campaign between the two.

How ties break (yearly hazard per intact tie), anchored on Leeds and Savun (2007): alliances are abrogated more often after domestic regime change in a member and after shifts in relative power. Base hazard `h_al0` (J, from the base-rate research), multiplied by:
- `m_al_reg` when either member's regime changes (democratic breakdown, seizure, insurgent victory);
- `m_al_close` once the stronger member reaches closure (an automated power no longer needs allies' bases, workers or industry);
- `m_al_atroc` when either member starts executing depopulation (democracies distance themselves; an executing regime is a threat to everyone);
- a 2026 US-specific erosion term (A7: withdrawal from 66 international organizations in January 2026).
A broken tie stays broken for the rest of the run.

This is where Europe's coordination problem enters: whether Western EU, Eastern EU, the UK and CANZ act together is now an outcome of tie strengths and breakages, not an assumption.

## C. Who the rulers are

### Institutions
Each coalition member belongs to one of three institutions:
- **State**: politicians, party and civil administration;
- **Military**: military and security services;
- **Owners**: owners and operators of AI and automated industry.

The institutional mix of a coalition depends on the actor (J, documented per actor): owners are a large part of the US elite, the party-state dominates China, security services dominate Russia, the royal family (state) dominates the Gulf monarchies.

Control of force (A6) depends on institution:
- human coercive networks (hw): state and military members hold them; owners hold little;
- automated force (aw): military members command it; owners hold a share equal to the actor's private-provision share of automated force (`own_auto[a]`, J: high in the US, where firms build and operate AI and autonomous systems; low in China and Russia).
So as security automates, control can drift from generals and party bosses to the owners of the machines, and back if the state nationalizes them. Nationalization is not modeled.

### Seven drives
Each member has an allocation over the seven drives of the World Model (Survival, Status, Meaning, Connection, Autonomy, Comfort, Curiosity), drawn from a Dirichlet with institution-specific tilts (J: military members lean to Survival and Status, owners to Status, Autonomy and Curiosity, politicians to Status and Connection).

Drives do not replace the existing trait priors. They correlate them. Each existing per-member trait is still drawn from its published marginal distribution, but its standard-normal draw is mixed with a drive score:
`z_trait = sqrt(1 - r^2) z_own + r * s_trait(drives)`, where `s_trait` is a standardized weighted sum of drives and `r` is the drive coupling (J, U(0.3, 0.7)). Marginals stay as published; only the correlations are new.

Trait mapping (sign of each drive's weight):
- moral cost of ordering killing: + Connection, + Meaning, - Status;
- concern for the public: + Connection, + Comfort, - Status;
- hostility to the public: + Status, - Connection;
- absolute refusal to order killing: + Connection, + Autonomy;
- threat sensitivity (weight on revolt and latent threat): + Survival;
- cost of own purge risk (Brake 2): + Survival;
- uptake of a depopulation ideology (member level): + Meaning, + Curiosity;
- human-network strength (who becomes leader): + Status;
- willingness to dissent or veto: + Autonomy, - Survival.

## D. Changes carried from the earlier sign-off list

1. **Land.** The material land term (`v0`, scarcity rent `v1`, `eco_land`) is removed. What remains is a preference for an emptier planet that exists only while the depopulation ideology is held: `v_pref x id_lev`, with `v_pref` drawn like the old `v0` (J). Old setting kept as variant `land_old`.
2. **Latent threat.** A yearly cost of keeping any population, independent of current hostility and not reduced by automated security: `tau_lat x alive share x (1 + k_lr x rival)`, with option weights 1 for serve, rents, status quo and warehouse, 0.7 for neglect, and the execution-period weight for depopulation (J; Fearon 1995; Valentino 2004). `tau_lat` ~ lognormal, median 0.01 of output a year, sigma 1.0. Variant `latent_off`.
3. **Unrest accelerates the depopulation ideology.** Uptake hazard x `m_unrest` (U(1.5, 3), C: Harff 2003) during an active insurgency, as war already does.
4. **Ideology baseline.** Re-elicited from Jev with fixed wording and three paraphrases (needs the Jev server at 127.0.0.1:9117).
5. **Variants.** `rudolf_best` (provision costs x 0.1, no revolt or sabotage threat once security is automated), `rudolf_best_latent_off`, `latent_off`, `land_old`, `alliances_off`, `drives_off`, `institutions_off`, `six_blocs` (v6 actors for comparison).

## Sign-off list (plain language)

Everything below is in the code on branch `v7-actors` and has passed small test runs. Nothing has been run at full size.

**1. Who the actors are.** 17 actors in place of 6 blocs, with the membership you approved. Three groupings are rough and stay a limitation: Rest of MENA puts Israel, Iran and Turkey in one actor (security cohesion close to zero), Eastern EU includes Ukraine and the Western Balkans, and Russia includes Central Asia. Thirteen European microstates (0.7 million people) are left out.

**2. Sourced inputs replace several v6 judgment values.** Population, workforce, military spending, democracy scores, social spending, power capacity, manufacturing and industrial output, robots, chips, rare earths and nuclear arsenals now come from the cited sources. Some differ a lot from v6, so v7 results will move for reasons beyond the split:
- China's share of world manufacturing is 0.28 today; v6 used 0.45, a 2030 projection. Europe's is higher than v6 had.
- China makes 97% of general-purpose robots; v6 used 83%.
- China's robot density was revised down (IFR 2026); I set China's starting automated share of manufacturing to 0.06 rather than the 0.04 the density alone gives.
- The UK and the US start inside an autocratization episode (V-Dem 2026); India and much of South and Southeast Asia too.

**3. Alliances.** Each pair has a commitment strength, read as "how strongly A would defend B" in 2026 (research judgment, adjusted down where a commitment covers only a small member of a mixed actor). Allies count toward defense against cross-border campaigns, extend nuclear deterrence, join wars, help enforce outside pressure, shield each other from it, and trade robot inputs more freely. A commitment is honoured with probability 0.4 to 0.75 when triggered (Berkemeier and Fuhrmann 2018; Leeds et al. 2000). Ties break at a base rate of 0.3 to 1.5% a year, faster after the stronger member has closed its loop, with a 10 to 40% chance at each regime change in either member, a 50 to 90% chance when one member starts killing its own people, and an extra yearly hazard of up to 3% for ties with the US (A7).

**4. Wars.** Named dyads with base rates per year: US-China 0.3%, China-Taiwan 0.6%, Russia-Eastern EU 1%, India-Pakistan region 2%, India-China 0.4%, Korea-North Korea 0.3%, China-Japan 0.2%, China-Southeast Asia 0.4%, Gulf-Rest of MENA 0.8%. Each scales with the sampled war priors and the conflict trend. Allies may join. The Russia-Ukraine war runs on as in v6.

**5. Institutions.** Ruling elites mix politicians, the military and owners of AI and automated industry in actor-specific shares (for example US 45/20/35, China 70/20/10, Russia 40/45/15). Owners hold the actor's private share of automated force (US 35%, China 5%). As security automates, control can shift from generals and party networks to whoever owns the machines.

**6. Seven drives.** Each member's drive profile correlates their traits: moral restraint, concern for the public, hostility, refusal, threat sensitivity, fear of purges, network strength (who leads) and susceptibility to a depopulation ideology. The published distribution of each trait is unchanged; only the correlations are new, with a coupling of 0.3 to 0.7.

**7. Land.** No material land motive. A preference for an emptier planet remains, held only while the depopulation ideology is held.

**8. Latent threat.** A yearly cost of keeping any population, median 1% of output, not reduced by automated security, larger when a comparable rival exists.

**9. Unrest speeds up the ideology.** By 1.5 to 3 times during an active insurgency (Harff 2003), and the uptake rate scales with the ruling group's average susceptibility.

**10. Ideology baseline.** Pending: the Jev elicitation needs the Jev server running at 127.0.0.1:9117. Until then the v6 rate stays (about 4.5% per nine years after closure).

**11. Variants reported alongside the main result.** v6 mechanics on 17 actors, alliances off, latent threat off, old land term, unrest effect off, drives off, institutions off, Rudolf's best case with and without the latent threat.

**First small-sample readings (256 draws, not results):** the US-or-China near-total figure stays close to v6, about 0.39. Smaller actors are now often lost to another actor's campaign, mostly China's; alliances cut that noticeably (Taiwan 0.61 to 0.50, CANZ 0.50 to 0.39). About 80% of 2026 ties break by 2075.
