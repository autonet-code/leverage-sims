# r14a: Soft power, tolerance of parallel communities, and crackdown hazard

Date: 2026-10-01. Scope: inputs for the decentralized-AI lever test (black box; effects only through approved channels). Web search budget was exhausted during this pass, so several figures come from direct page fetches (marked F) and the rest from the established literature recalled without re-checking (marked M). Treat M figures as medium confidence at best.

## Key findings

1. **States repress what can act collectively, not what criticizes them.** King, Pan and Roberts (2013, APSR; F): Chinese censorship leaves even harsh criticism up but removes posts with collective-action potential. Davenport (2007): the "law of coercive responsiveness" says perceived threats are almost always repressed. So the crackdown hazard depends on organisational capacity, visibility and any claim to sovereignty, more than on ideology.
2. **Size thresholds are relative to the regime.** Falun Gong (founded 1992, about 70M practitioners by 1999, more than the CCP's roughly 63M members; F) was banned on 20 July 1999, about 3 months after a visible 10,000-person sit-in at Zhongnanhai. The 610 Office went from creation to nationwide campaign within weeks. Rajneeshpuram (about 7,000 people; F) was tolerated in legal limbo until it tried to capture local government (voter importation, the 1984 salmonella attack). It collapsed within about a year of that.
3. **Explicit sovereignty claims inside a state's reach get suppressed in weeks to months.** Rose Island: independence declared 1 May 1968, seized 55 days later (F). Republic of Minerva: declared in Jan 1972, Tonga annexed it by mid-1972 (M). The Thai seastead (2019) was raided within weeks of publicity, with charges that carried the death penalty (M). Iraqi Kurdistan: the referendum was 25 Sep 2017, Kirkuk was taken on 16 Oct (21 days), and the KRG lost about 40% of its territory (F). Catalonia: police action on referendum day in 2017 and leaders jailed for 9-13 years in 2019, followed by pardons in 2021 and amnesty in 2024 (M). The surviving exceptions are trivial in size (Sealand).
4. **Small, legal, taxed, low-visibility communities are tolerated for decades.** Christiania (1971; 850-1,000 residents; 500k visitors a year): tolerated, legalized in 1989, land bought in 2012, and the drug market was closed jointly with police in 2024 (F). WIR Bank has lasted about 90 years at about 0.2% of Swiss GDP (m7). The Soviet second economy (10-30% of urban income) was tolerated because the state depended on it (m7).
5. **Crypto shows the hazard rising with size.** Countries with bans grew from about 8 absolute and 15 implicit (LoC 2018) to 9 absolute and 42 implicit (LoC 2021) as market cap grew about 5-10x (M; the LoC page returned 403). China tightened in steps as size grew: 2013 bank ban, 2017 exchange/ICO ban, then the 2021 mining and trading ban, which took China's share of hash rate from about 46% to 0, before it recovered underground to about 15-20% (m7). The Tornado Cash and Samourai prosecutions show that developers get criminalized.
6. **Foreign public sympathy does not protect against a great power acting on a core interest.** Hong Kong 2019-20: protests of up to about 2M people, near-unanimous US legislation in support, and the National Security Law anyway (M). Tibet and Xinjiang: sustained Western public sympathy and no protection. Kurdistan 2017: strong Western goodwill toward the Peshmerga, and the US only "urged" restraint (F). Foreign support helps where the repressor depends on the supporters. Levitsky and Way (2010, "linkage and leverage"; M): high-linkage regimes mostly democratized, while low-leverage targets (Russia, China) were unaffected. Examples where it worked: South Africa (decades), East Timor 1999, Solidarity surviving martial law.
7. **Foreign attention moderates severity more than incidence.** Catalonia (legal rather than lethal repression), Christiania, Solidarity. Krain (2012; M): shaming lowers the severity of mass killing. Hafner-Burton (2008; M): shaming alone often comes with more terror. Murdie and Davis (2012; M): shaming works when local and third-party pressure are combined.
8. **Foreign publics protect a network only through their own governments, so the protection inherits those publics' leverage.** Goldsmith and Horiuchi (2012, World Politics; M): foreign public opinion moved government support for US policy only on high-salience issues. Gilens and Page (2014; M): average citizens' independent effect on US policy is near zero, against a large effect for economic elites, even before automation removes their economic leverage. In the model, this protection should scale with foreign publics' leverage L_pub(t), so it shrinks as the "no customers" domino proceeds. It has a deadline, as the handoff anticipated.
9. **Soft power builds slowly, reverses fast, and states can cut its channel.** Hallyu took about 15-20 years (1997 to the 2010s) to go global (F). Japanese affinity toward Korea fell from about 63% (2009) to about 39% (2012) after one political dispute (Cabinet Office; M). Global confidence in the US president fell from 64% to 22% in one year (2016 to 2017; Pew; M). China imposed a Hallyu ban within months of THAAD in 2016-17 (F), and North Korea's 2020 law punishes K-drama distribution severely. China spends roughly $10B a year on external outreach and its favourability still falls (Shambaugh 2015; M), so attraction cannot be bought without credibility (Nye).
10. **Mobilization can spread in weeks, attitudes take years.** Occupy went from 17 Sep 2011 to 951 cities in 82 countries by 9 Oct (22 days), and the camps were mostly cleared by Nov 2011 to Feb 2012 (F). That is fast diffusion with fast clearance. Bass meta-analysis (Sultan, Farley and Lehmann 1990; M): p about 0.03 and q about 0.38, so time to peak adoption is ln(q/p)/(p+q), about 6 years. Durable change in foreign public attitudes runs at 5-15 years.
11. **The AI-specific change is that backfire needs defection.** Repression backfires when it is visible and security forces might defect (r9c, m4). With automated security (an existing assumption), the backfire and defection protection disappears. Foreign-public protection is then the only soft channel left, and it lasts only while foreign publics have leverage.

## Parameters (for the lever test)

| # | Parameter | Central | Low | High | Quality | Source |
|---|---|---|---|---|---|---|
| 1 | Annual crackdown hazard, small (<0.1% of the economy), legal, low-visibility network, democracy | 0.01 | 0.002 | 0.03 | medium | Christiania, WIR, intentional communities |
| 2 | Same, in an autocracy (US-or-China framing: China) | 0.05 | 0.02 | 0.10 | low-medium | Falun Gong pre-1999, crypto steps, house churches |
| 3 | Elasticity of hazard to network size (hazard ∝ share^k) | 0.7 | 0.4 | 1.2 | low | LoC ban counts vs market cap; China escalation |
| 4 | Threat threshold (share of population or economy) where an autocracy treats a network as existential | 0.02 | 0.005 | 0.10 | low-medium | Falun Gong (about 5% of the population, rivalling party size); m7 macro-relevance |
| 5 | Same threshold, democracy (monetary or tax sovereignty) | 0.05 | 0.01 | 0.15 | low | m7 (Wörgl, Liberty Dollar); Gilens and Page context |
| 6 | P(active suppression \| above threshold and eroding tax or monetary control) | 0.6 | 0.5 | 0.8 | medium | m7; crypto bans; Falun Gong |
| 7 | P(suppression \| explicit sovereignty claim within the state's reach) | 0.85 | 0.7 | 0.95 | medium | Rose Island, Minerva, Thai seastead, Kurdistan, Catalonia |
| 8 | Lag from sovereignty claim or visible mass challenge to suppression (years) | 0.15 | 0.05 | 1.0 | medium | 21 days (Kirkuk) to about 5 months (Minerva); Falun Gong about 3 months |
| 9 | Hazard multiplier for high visibility or overt collective action vs low profile | 5 | 2 | 20 | low-medium | King, Pan and Roberts; Davenport; Rajneeshpuram |
| 10 | Hazard multiplier if armed (for reference; user excluded kinetic) | 2.5 | 1.5 | 4 | low-medium | Chenoweth and Stephan; Waco, MOVE |
| 11 | Hazard reduction from foreign public support, target = great power with core interest (US or China) | 0.10 | 0.0 | 0.25 | medium | Hong Kong, Tibet, Xinjiang, Kurdistan |
| 12 | Hazard reduction from foreign public support, target dependent on supporters (high linkage or leverage) | 0.40 | 0.2 | 0.6 | low-medium | Levitsky and Way; South Africa, East Timor, Solidarity |
| 13 | Reduction in crackdown lethality or severity from foreign attention (vs incidence) | 0.35 | 0.15 | 0.5 | low | Krain 2012; Catalonia; Hafner-Burton caveat |
| 14 | Pass-through of foreign public opinion to its government's policy, salient issue, democracy | 0.3 | 0.1 | 0.5 | low-medium | Goldsmith and Horiuchi 2012; Gilens and Page 2014 |
| 15 | Dependence of protection on foreign publics' leverage: protection = P_max x L_pub(t)^e | e = 1 | 0.5 | 2 | low (structural) | Inference from 8, 11-14 |
| 16 | Years to shift foreign public attitudes to majority favourability via cultural propagation | 8 | 4 | 15 | low-medium | Hallyu 1997-2010s; Cold War cultural diplomacy |
| 17 | Goodwill reversal after a hostile political event (percentage points within 1-3 years) | 25 | 10 | 40 | medium | Japan on Korea 63 to 39 (2009-12); US confidence 64 to 22 (2016-17) |
| 18 | Time for a state to cut a foreign cultural channel (years) and effectiveness | 0.3 yr, 70% | 0.1 yr, 50% | 1 yr, 90% | medium | China Hallyu ban 2016-17; Great Firewall; North Korea 2020 |
| 19 | Mobilization diffusion speed: time to reach about 1,000 sites (days) | 22 | 7 | 90 | medium | Occupy 2011; Arab Spring |
| 20 | Bass diffusion coefficients for adoption (p, q) | 0.03, 0.38 | 0.01, 0.2 | 0.05, 0.6 | medium | Sultan, Farley and Lehmann 1990 meta-analysis |

## Modelling suggestions (black box preserved)

- Crackdown hazard: h(t) = h0[regime] x (share/threshold)^k x visibility multiplier x (1 - R_soft(t)), with a step to P7 if a sovereignty-like claim is made, for example by visible enclaves.
- R_soft(t) = R_max[target type] x pass-through x L_pub_foreign(t)^e x favourability(t). For US or China, R_max is about 0.1, so the soft-power channel is small for the headline. It matters more for mid-sized states that host nodes.
- The deadline appears when L_pub_foreign falls with the domino: soft power gained after foreign publics lose leverage buys almost nothing.
- Physical enclaves trade resilience against parameters 7-9. A cruise ship or enclave that looks like a sovereignty claim moves the hazard into the weeks-to-months regime.

## Sources

- King, Pan, Roberts 2013, https://gking.harvard.edu/publications/how-censorship-china-allows-government-criticism-silences-collective-expression (F)
- Persecution of Falun Gong, https://en.wikipedia.org/wiki/Persecution_of_Falun_Gong (F)
- Rajneeshpuram, https://en.wikipedia.org/wiki/Rajneeshpuram (F)
- Freetown Christiania, https://en.wikipedia.org/wiki/Freetown_Christiania (F)
- Republic of Rose Island, https://en.wikipedia.org/wiki/Republic_of_Rose_Island (F)
- 2017 Iraqi-Kurdish conflict, https://en.wikipedia.org/wiki/2017_Iraqi%E2%80%93Kurdish_conflict (F)
- Occupy movement, https://en.wikipedia.org/wiki/Occupy_movement (F)
- Korean wave, https://en.wikipedia.org/wiki/Korean_wave (F)
- Recalled, not re-fetched (M): LoC "Regulation of Cryptocurrency Around the World" 2018 and 2021; Goldsmith and Horiuchi 2012 World Politics 64(3); Gilens and Page 2014 Perspectives on Politics; Levitsky and Way 2010; Krain 2012 ISQ; Hafner-Burton 2008 IO; Murdie and Davis 2012 ISQ; Davenport 2007 ARPS; Sultan, Farley and Lehmann 1990 JMR; Shambaugh 2015 Foreign Affairs; Japan Cabinet Office diplomacy surveys; Pew Global Attitudes 2017; Nye 2004.
