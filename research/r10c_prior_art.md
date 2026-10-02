# r10c Prior-art comparison (2026-09-30)

Purpose: place the m8_v4 standalone numbers against published forecasts and models.
Tags: [web] fetched this session; [notes] from earlier research notes (m1, m5, m6, r8d); [lit] from memory of the published source, NOT re-fetched (web search budget exhausted); verify before citing in the paper.

Our quantities (m8_v4, N=20000):
- S5_deliberate: >=10% of a bloc's 2026 population lost to an executed depopulation decision, collective punishment or deliberate lethal neglect. US or China bloc by 2075: 13.0% (by 2050: 8.4%). Any of 6 blocs: 28.6%.
- S5_total (adds attrition and war): any bloc 37.4%, US/China 16.3%. Expected world population share in S5_total blocs by 2075: 14.9%.
- Public disempowered, US/China by 2075: 70.8%. US democratic breakdown (LDI<0.3) by 2040: 52.6%.
- Closure (leading bloc core chain <20% human-dependent): median 2038, p10 2035; P(by 2040) 60.8%.
- Model average incl. skeptic/pessimist parameter sets: 24.4% (range 0.6% to 71.2%).

## 1. Qualitative frameworks (no probabilities)

| Work | Method | Claims | Comparability |
|---|---|---|---|
| Drago & Laine, The Intelligence Curse (2025) [web] | Essay; rentier-state / resource-curse analogy; "pyramid replacement" | When labor stops mattering, states and firms stop investing in people. Remedy: avert, diffuse, democratize (explicitly decentralizing). No dates or probabilities. | Same mechanism as our S4 to public-disempowered chain. Our model is in effect a quantified Intelligence Curse with a lethal tail. |
| Kulveit, Douglas, Ammann, Turan, Krueger, Duvenaud, Gradual Disempowerment (arXiv 2501.16946, Jan 2025; ICML 2025) [web] | Conceptual systems analysis | Incremental AI erodes human influence over economy, culture and state; mutually reinforcing; possibly irreversible. No numbers. | Maps to "public disempowered" and closure. They argue it happens even without a malicious actor; our model needs an elite decision for S5_deliberate, so it is narrower. |
| Davidson, Finnveden, Hadshar, AI-Enabled Coups (Forethought, 15 Apr 2025) [web] | Mechanism analysis | Singular loyalties, secret loyalties, exclusive access; frontier projects could shrink to one; superhuman AI plausibly "within 5 or 10 years". No probability. | Same actor class as our single-ruler / elite branch. Supports concentration priors, gives no number to check against. |
| Davidson & Hadshar, The Industrial Explosion (Forethought, 21 May 2025) [web] | Growth/biology analogies | Robot doubling ~1 to 2 years once AI directs production; much faster later. Industrial explosion follows, and is slower than, the intelligence explosion. | Supports our physical build-out speed. Our capped build-out (gross investment 8-15%/yr plus retrofit) is SLOWER than their central case, so closure 2038 is not aggressive by their standard. |
| Kokotajlo, Alexander, Larsen, Lifland, Dean, AI 2027 (3 Apr 2025) [web + lit] | Scenario from ~25 tabletop exercises | Superhuman coder Mar 2027, ASI Dec 2027 (modal, not median). Race ending [lit]: misaligned AI kills most humans with bioweapons ~mid-2030. Slowdown ending [lit]: a small oversight committee controls superintelligence (power concentration). No stated probability for either ending. | Race ending is misalignment, not our channel. Slowdown ending is our precondition (small human group controls automated economy). Our M3 (90% software tasks) median 2029.5 is about 2 years behind their modal path and close to their later medians. |

## 2. Quantitative forecasts of catastrophe

| Source | Method | Numbers | vs our S5 |
|---|---|---|---|
| XPT, Karger et al. (FRI; tournament 2022, paper 10 Jul 2023) [lit; ACX summary web] | Structured tournament, 89 superforecasters and 80 experts | AI catastrophe (>10% of humanity dies within 5 yrs) by 2100: superforecasters ~2.1%, AI experts ~12% (paper) [lit]; ACX's summary gives 1.6% vs 5% for all experts [web]. AI extinction by 2100: 0.38% vs 3%. All-cause catastrophe by 2100: 9% vs ~20%. | Closest event definition (>=10% dead). Ours is bloc-level not world, deliberate-human not misalignment, 2075 not 2100. A bloc-level event is less stringent, so ours should exceed theirs. Our 13% (US/China) is ~6x superforecasters and about equal to AI experts. Relative to superforecasters: outlier. Relative to experts: consistent. |
| Grace et al., Thousands of AI Authors (ESPAI, surveyed Oct 2023, N=2,778) [web + notes] | Researcher survey | HLMI 10% by 2027, 50% by 2047. Full automation of occupations 10% by 2037, 50% by 2116. P(extinction or severe disempowerment): median 5%, mean ~9-16% depending on framing; 38-51% give >=10%. [lit] ~73% report substantial/extreme concern about authoritarian population control via AI; ~71% about AI-worsened inequality. | "Severe disempowerment" is close to our public-disempowered, but they give 5% median and we give 70.8%. Their disempowerment question means permanent loss for all humanity; ours means the public loses political leverage while elites stay in control. Different quantity, so they should not be compared directly. Our S5 13% lies between their median and mean. |
| Ord, The Precipice (2020) [lit] | Author judgment | Existential catastrophe within 100 yrs: unaligned AI 1 in 10; all risks 1 in 6. His definition includes unrecoverable dystopia. | Our S5 is a smaller event on a shorter horizon at about the same magnitude. Consistent in order of magnitude. |
| Carlsmith, Is Power-Seeking AI an Existential Risk? (2021, updated 2022) [lit] | Six-premise probability chain | Existential catastrophe from power-seeking AI by 2070: ~5%, later revised to >10%. | Method is closest to ours (a chained conditional decomposition). Magnitude matches, channel differs. |
| Metaculus q5121 general AI [notes] | Crowd forecast | Median ~Jan 2033, 25% by 2029 (Jul 2026). | Timing input only. |
| AI Futures Project, Q2.5 2026 update [notes] | Timelines model | Automated coder medians: Nov 2027 (Kokotajlo), Jan 2029, Jan 2030 (Lifland); AC to ASI in 1 to 2 years. | Our M3 2029.5 falls inside this range. |

## 3. Economic models of automation

| Source | Method | Numbers | vs closure |
|---|---|---|---|
| Acemoglu, The Simple Macroeconomics of AI (2024) [notes/lit] | Hulten task-share calculation | ~4.6% of tasks profitably automated in 10 years; TFP +~0.5-0.7% and GDP about +1% over a decade. | Our model is far outside this (closure 2038). It is the key skeptical anchor; the paper must say we assume capabilities Acemoglu's exposure data do not price in. |
| Korinek & Suh, Scenarios for the Transition to AGI (NBER w32255, Mar 2024) [web] | Task-complexity growth model | Wages rise if capital accumulation outruns automation, and collapse under full automation within 5 to 20 years. [lit] | Supports our displacement to wage collapse chain under fast scenarios. No probabilities. |
| Epoch GATE, Erdil, Besiroglu et al. (arXiv 2503.04941, 2025) [notes] | Integrated assessment model (compute to automation to growth) | Growth 2-20x the current ~3%; full automation "in decades"; the authors say it is not a forecast. | Our closure (core chain only, leading bloc) is narrower than full automation, so it is compatible with GATE's fast settings. |
| Davidson, Could Advanced AI Drive Explosive Growth? (Open Phil 2021) and compute-centric takeoff (2023) [lit] | Growth-model review; takeoff model | Explosive (>30%/yr) growth this century is plausible and should not be dismissed. Takeoff model: ~3 years median from 20% to 100% automation of cognitive tasks. | Closure 2035-2040 fits a 2029-2033 AGI date plus a few-year takeoff plus physical lag. |
| Agent-based macro models, e.g. Dosi, Roventini et al. Keynes+Schumpeter family (2010s-2022) [lit] | ABM of firms, workers, policy | Automation can raise unemployment and inequality; the result depends on policy and demand regime. | They model no political or lethal outcomes. We found no ABM that links automation to regime change or population loss. |

## 4. Empirical AI-authoritarianism work

- Beraja, Kao, Yang, Yuchtman, AI-tocracy (QJE 2023) [lit]: in China, local unrest leads to more police procurement of facial-recognition AI, and that procurement is followed by less unrest. It is the only causal evidence we found that AI surveillance suppresses dissent. It supports our "automated surveillance deters onset" term, but it measures protest suppression, not mortality.
- V-Dem democracy trends: see r9d.
- We found no published quantitative model that gives a probability of AI-enabled authoritarian consolidation or deliberate depopulation.

## 5. Verdict

1. Novelty: no published model estimates deliberate human-directed depopulation made possible by aligned automation. Prior quantitative work covers misalignment catastrophe (XPT, ESPAI, Ord, Carlsmith) or economics (Acemoglu, Korinek, GATE). The mechanism has only qualitative treatments (Intelligence Curse, Gradual Disempowerment, AI-Enabled Coups). The paper should present m8 as the first quantification of that literature, not as a replication.
2. S5_deliberate 13% (US/China, 2075): consistent with expert and researcher estimates (XPT experts ~12%, ESPAI mean ~9-16%, Ord 10%, Carlsmith >10%) and about 6x superforecasters (~2%). Say so explicitly. Superforecasters are the best-calibrated group on track record, and our number is an outlier against them. Our event is less stringent (one bloc, 10%), which explains part of the gap, not all of it.
3. S5_total any bloc 37.4%: higher than any published catastrophe figure, but it is a union over 6 blocs of regional >=10% losses, including war and attrition. Do not put it next to world-level numbers. Report the world-population-share figure (14.9%) instead, and consider adding P(world loss >=10%) to integrate_v4 so it can be compared with XPT directly.
4. Public disempowered 70.8%: no probabilistic comparator exists. ESPAI's 5% "severe disempowerment" measures something different (all humanity, permanent). The direction is supported by researcher concern (~73% substantially concerned about AI authoritarian control [lit]) and by the qualitative literature.
5. Closure median 2038: fast against researchers (FAOL 50% 2116) and against economists (Acemoglu); in line with forecasters and AI-safety-adjacent models (Metaculus AGI 2033, AI Futures AC 2027-2030, Davidson takeoff ~3 yr, Industrial Explosion doubling 1-2 yr). Closure applies to the leading bloc's core chain, not the whole economy, which narrows the gap with the survey.
6. The model average of 24.4% and its 0.6-71.2% range span the whole published spread, from superforecasters to AI 2027-style pessimism. Present the range as the honest result.

## Sources
- https://intelligence-curse.ai/
- https://arxiv.org/abs/2501.16946
- https://www.forethought.org/research/ai-enabled-coups-how-a-small-group-could-use-ai-to-seize-power
- https://www.forethought.org/research/the-industrial-explosion
- https://ai-2027.com/
- https://forecastingresearch.org/xpt ; https://forecastingresearch.org/pdf/existential-risk-persuasion-tournament.pdf
- https://www.astralcodexten.com/p/the-extinction-tournament
- https://arxiv.org/abs/2401.02843
- https://www.nber.org/papers/w32255
- https://epoch.ai/gate ; https://arxiv.org/abs/2503.04941
- Not fetched [lit]: Ord 2020; Carlsmith 2022 (arXiv 2206.13353); Acemoglu 2024 (NBER w32487); Davidson 2021 (Open Phil); Beraja et al. QJE 2023; Dosi et al. ABMs.
