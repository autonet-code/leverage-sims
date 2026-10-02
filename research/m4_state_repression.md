# S4 research: unrest, repression, and the rentier state

Stage claim (from the scenario text): displaced people protest, protests turn violent and target data centers, but this is no real threat because coercion is automated (no soldiers left to defect), and the state has no incentive to side with the people because its biggest taxpayers are AI companies.

The claim has two parts, and they need separate evidence:
1. **Unrest fails.** Will mass unrest fail to force concessions?
2. **The state switches sides.** Does the state's fiscal base move from citizens to AI firms (the rentier logic), so that it stops responding to them?

Researched 2026-09-30. Scope: feeds the quantitative model up to and including S5 (depopulation). S6/S7 are not modeled here.

## 1. Base rates: how often protest movements succeed

| Quantity | Value | Source |
|---|---|---|
| Nonviolent maximalist campaign success, 1900-2006 | 53% | Chenoweth & Stephan, *Why Civil Resistance Works* (2008/2011) |
| Violent campaign success, 1900-2006 | 26% | same |
| Nonviolent success at its peak (1990s) | ~65% | Chenoweth, *Journal of Democracy* 2020 |
| Nonviolent success, 2010-2019 | ~34% | Chenoweth 2020; CNCR |
| Average peak participation since 2010 | 1.3% of population (vs the 3.5% "rule" threshold) | Chenoweth 2020; Commons Library summary |
| Effect of security force defection | raises the probability of success by ~60% (relative); defections occurred in 52% of successful nonviolent campaigns vs 32% of successful violent ones | Chenoweth & Stephan (NAVCO) |
| Updated NAVCO disloyalty data | disloyalty correlates with success, significant only once participation exceeds ~1,000 | Journal of Peace Research 2025 dataset |

Reading: protest success rates were already falling before any AI-enabled coercion, because regimes adapted (information control, provoking violence, criminalizing protest). Violent campaigns, which the scenario text predicts, historically succeed about half as often as nonviolent ones. They also help regimes justify repression.

## 2. Security force defection is still the hinge (recent cases)

| Case | Outcome | Mechanism |
|---|---|---|
| Tunisia 2011 | Ben Ali fled. Democracy until the 2021 self-coup | Army refused to fire |
| Egypt 2011 | Mubarak removed by the army. Military coup in 2013 | Army sided against the leader, then took power |
| Bahrain 2011 | Suppressed | Loyal forces plus GCC troops |
| Syria 2011 | Civil war. Assad survived until Dec 2024 | Core units stayed loyal (sectarian recruitment) |
| Hong Kong 2019-20 | Movement crushed. 10,279 arrests, 2,961 prosecuted. National Security Law 2020 | Police fully loyal, backed by the PRC |
| Sri Lanka 2022 | Rajapaksa ousted | Economic collapse, security forces restrained |
| Bangladesh 2024 | Hasina ousted | Army declined to keep firing |
| Nepal Sep 2025 | Government fell (Gen Z protests) | Army stood aside |
| Madagascar Oct 2025 | Rajoelina fled. Military (CAPSAT) took power. Protesters say they were "betrayed" (Sep 2026) | Elite unit defected |
| Iran Dec 2025-Jan 2026 | Suppressed within about a week of the Jan 8-9 massacres. Official toll 3,117. Activists count 6,126+. Other estimates run 16,500-36,500 | Loyal IRGC/Basij willing to kill at mass scale |

Pattern: when armed forces defect or stand aside, regimes fall (and the result is often military rule, not democracy). When they stay loyal and are willing to kill at scale, regimes survive. Iran 2026 shows this works today without automation. The scenario text's point is that automation removes the defection channel. That is directionally supported. But loyal human forces already achieve the same result in many cases, so automation changes the odds only where defection was the binding constraint (mostly conscript militaries and democracies).

## 3. Historical anti-machine unrest

- **Luddites (1811-16):** about 12,000 troops were deployed. The Frame Breaking Act of 1812 made machine-breaking a capital crime. Executions followed (York 1813). Mechanization went ahead anyway.
- **Swing Riots (1830-32):** over 3,000 riots, the largest English unrest since 1700. About 2,000 tried: 252 sentenced to death, 19 hanged, 481 transported, 644 imprisoned. Caprettini & Voth (AER: Insights 2020): riots were much likelier in parishes where threshing machines had spread. Locally, adoption of threshing machines slowed, and the 1830s saw Poor Law reform and franchise politics (the Reform Act 1832). So there was repression plus a partial policy response, not pure suppression.
- **Modern analogs:** UK 5G mast arson in 2020 (dozens of masts). Waymo vehicles burned in LA in 2025. In 2026: a Molotov attack on Sam Altman's home and an attempted attack on OpenAI HQ. The Soufan Center (May 2026) warned of a new violent strand of anti-data-center extremism. Philadelphia police acknowledged tracking anti-AI protest activity (The Intercept, Jun 2026).
- **Data center opposition today (mostly nonviolent and effective locally):** 142 protests in 42 US states in July 2026. Local opposition blocked or delayed 75 projects worth about $130B in Q1 2026. Only 14% of Americans would support a local AI data center (Jun 2026 poll). Gallup (May 2026) found a majority opposed.

## 4. Rentier state / resource curse

- **Ross (2001, 2012):** oil-rich states are about 50% more likely to be autocratic, and democratic transitions are about 50% more likely in oil-poor states. The proposed mechanism is revenue without taxation, which means less accountability. The effect is strongest after 1980.
- **Haber & Menaldo (APSR 2011):** within-country long-run time series find *no* causal effect of resource reliance on authoritarianism. This is a serious counterweight. Treat the rentier effect as real but contested in size.
- **Norway, Canada, Australia:** large resource rents with democracy intact. Existing institutions moderate the curse.
- **Acemoglu & Robinson (2000, 2006):** elites extend the franchise and redistribute when the threat of revolution is credible. If automation makes the threat of revolution incredible, this model predicts less redistribution. This is the strongest theoretical support for S4.
- **Ross (2004), "Does taxation lead to representation?":** the tax burden *relative to government services* predicts democratization, not taxes alone.
- **Drago & Laine, "The Intelligence Curse" (2025):** applies rentier logic directly to AGI. States and firms lose their incentive to invest in people once people are no longer the source of revenue.

### Where the state's money comes from today (US)

| Item | FY2025 |
|---|---|
| Total federal receipts | $5.2T |
| Individual income tax | $2,656B (50.7%) |
| Payroll taxes | $1,748B (33.4%) |
| Taxes on individuals, combined | 84.1% |
| Corporate income tax | 8.6%, projected to fall toward 7% (CBO) |
| Big Tech/AI firms' income tax (Apple, Microsoft, Alphabet, Meta, Amazon, Nvidia), rough estimate from 10-K provisions | about $90B globally, so the US federal share is roughly 1% of federal revenue (my estimate, medium confidence) |

OECD: corporate income tax is about 10-16% of total tax revenue on average (OECD Corporate Tax Statistics).

Reading: today the scenario text's premise is false. AI firms are small taxpayers and individuals fund about 84% of federal revenue. The premise can only become true *after* S2. If labor income collapses, the tax base mechanically moves to whoever receives income (capital and AI firms). So S4's rentier logic is conditional on S2 and not independent of it. In petrostates the resource curse bites at resource revenue of roughly 40%+ of government revenue (Gulf states 60-90%). Norway is at about 20-30% and stays democratic.

## 5. Automated surveillance and coercion

- **Xinjiang:** domestic security spending rose 92.8% in one year (RMB 30.05B in 2016 to 57.95B in 2017), about 10x over 2007-2017. Detention-center spending rose 239%. About 100,000 security personnel were recruited in the 12 months to mid-2017. Estimated detainees are about 1M (range 0.5-1.8M; Zenz) out of about 12M Uyghurs. Note: this was *labor-intensive* surveillance amplified by technology, not full automation.
- **Drone warfare (Ukraine):** millions of FPV drones are produced per year, and autonomy features are spreading. This shows cheap robotic force is feasible. Fully automated domestic policing does not exist anywhere yet.
- **Democratic backsliding (V-Dem):**
  - Democracy Report 2026: 74% of the world population (about 6B) lives in autocracies, up from 72% in 2025. Only 7% live in liberal democracies. 44 countries are autocratizing. The global level of democracy is back to about 1978.
  - Democracy Report 2025: autocracies outnumber democracies for the first time in 20 years.

## 6. Parameters (central / low / high)

| # | Parameter | Central | Low | High | Confidence | Source |
|---|---|---|---|---|---|---|
| 1 | Nonviolent campaign success, historical | 0.53 | 0.50 | 0.65 | high | Chenoweth & Stephan |
| 2 | Nonviolent campaign success, 2010s-present | 0.34 | 0.25 | 0.40 | medium | Chenoweth 2020 |
| 3 | Violent campaign success, historical | 0.26 | 0.20 | 0.30 | high | Chenoweth & Stephan |
| 4 | Violent campaign success, modern era | 0.12 | 0.05 | 0.26 | low | Chenoweth 2020 (trend); judgment |
| 5 | Relative uplift in success from security force defection | 1.6x | 1.3x | 2.5x | medium | NAVCO |
| 6 | P(regime survives mass uprising given loyal forces willing to kill) | 0.85 | 0.65 | 0.95 | medium | Iran 2026, Syria, Bahrain, HK, Belarus 2020 |
| 7 | Mean peak participation of recent campaigns (% of population) | 1.3 | 0.5 | 3.5 | medium | Chenoweth |
| 8 | Rentier multiplier on the probability of democratic transition | 0.67 | 0.5 | 1.0 | low | Ross (0.5-0.67); Haber-Menaldo (1.0) |
| 9 | US federal revenue share from corporate income tax | 0.086 | 0.07 | 0.10 | high | CBO FY2025 |
| 10 | US federal revenue share from individuals (income plus payroll) | 0.841 | 0.82 | 0.85 | high | CBO FY2025 |
| 11 | Big Tech/AI firms' share of US federal revenue, 2025 | 0.01 | 0.005 | 0.02 | medium | 10-K estimate |
| 12 | Resource/AI share of state revenue at which rentier dynamics dominate | 0.40 | 0.25 | 0.60 | low | Petrostate comparisons; judgment |
| 13 | Share of world population in autocracies | 0.74 | 0.72 | 0.74 | high | V-Dem 2026 |
| 14 | Autocratizing countries | 44 | 42 | 44 | high | V-Dem 2025/2026 |
| 15 | Surveillance-state detention share of the targeted population (Xinjiang) | 0.08 | 0.04 | 0.15 | medium | Zenz |
| 16 | One-year security budget surge feasible for a determined state | 1.93x | 1.5x | 2.4x | high | Xinjiang budgets |
| 17 | Share of coercive capacity (policing/crowd control) automatable by 2035 in leading states | 0.2 | 0.05 | 0.5 | low | judgment; Ukraine drones, Xinjiang |
| 18 | P(democracy responds with major redistribution before unrest escalates, given S2-scale displacement) | 0.5 | 0.25 | 0.75 | low | Acemoglu-Robinson; New Deal / post-war welfare state; polls |
| 19 | Share of the public favoring a guaranteed income | 0.5 | 0.4 | 0.61 | low | Gallup/Northeastern 2018 (61%); "mixed" in 2025-26 polls |
| 20 | Local anti-data-center opposition: projects blocked or delayed per quarter (US) | 75 | 40 | 100 | medium | Q1 2026 reports |
| 21 | P(uprising with defection yields democracy rather than military/new autocracy) | 0.35 | 0.15 | 0.5 | low | Arab Spring (1 of 6), Madagascar, Egypt, Bangladesh, Sri Lanka |

## 7. Implications for the model (honest caveats)

- **Where S4 is supported:** protest success has fallen, repression works when forces stay loyal (Iran 2026), automation plausibly removes the defection channel, Acemoglu-Robinson predicts less redistribution without a revolutionary threat, and democracy has eroded globally (V-Dem).
- **Where S4 is weaker:**
  - The rentier premise is false today and only becomes true conditional on S2.
  - In democracies the main channel is elections, not street protest. 84% of revenue still comes from individuals until their income collapses, and voters can tax AI rents. That is the redistribution/UBI branch.
  - The resource curse effect is contested (Haber-Menaldo), and strong institutions blunt it (Norway).
  - Anti-AI protest is currently *winning locally* through permitting fights rather than violence.
  - Full automation of domestic coercion does not exist yet. The timing race between S2 displacement and coercion automation is the key uncertainty.
- **Violence cuts against the protesters:** the scenario text assumes a turn to violence, and history says violent campaigns succeed less often and legitimize crackdowns (Luddites, Swing).

## 8. v2 model revisions (after review, 2026-09-30)

- Redistribution counts only if adequate (transfers >= 50% of lost labor income; 0.3/0.7 as sensitivity). A token transfer no longer blocks S4.
- Coverage per concession round: 0.1 + 0.9*Beta(2.4,3.77), mean 0.45. Low end is the China shock (transfers offset about a tenth of lost wages, Autor, Dorn & Hanson 2013). High end is CARES Act 2020. Rounds add up (a ratchet). Temporary vs permanent is a separate parameter.
- Actions: concede, mix (partial transfer plus repression), repress, and populist redirection (Autor et al. 2020).
- Concessions now have a budget cost, paid from the AI-rent tax and then from other sources. Transfer spending that flows back to AI firms as revenue reduces the cost (weight c_mass, the "no customers" counterforce). AI rents fall as mass demand falls.
- The pre-emption hazard is calibrated per path to its prior. Autocracies get their own prior, p_perf.
- Added: deterrence lookahead, participation that responds to perceived efficacy, surveillance deterrence before any repression, sabotage costs for AI capital, and AI lobbying that rises continuously with rents. Lock-in rule: 3 of the last 4 mass-unrest years.
- T2 is aligned with the S2 model's S2a onset (median 2046).
