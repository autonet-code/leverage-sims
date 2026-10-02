# S2 research: the "no customers" domino

Stage: m2_no_customers_domino. As of 2026-09-30.

**Claim under test:** as more job categories are automated, broad economic participation ends. B2C firms lose customers first. B2B firms hold out a bit longer, but their clients depend on end users too. Demand collapses in waves up the supply chain.

**Verification key:** [V] = checked against a source in this session. [M] = the standard figure from the literature, recalled from memory and not re-fetched. Treat [M] numbers as roughly right to about ±10%.

---

## 1. Core linkages: how much of the economy rests on wage-funded consumption?

- **Consumer spending (PCE) is about 68% of US GDP [M]** (BEA NIPA, stable at 66-70% since 2008). It is the largest part of final demand. The rest is government (~17%), investment (~18%) and net exports (about -3%).
- **Personal income by source [M]** (BEA, 2024-25): wages and benefits ~62%, government transfers ~17-18% (they peaked around 25% in 2021), asset income (interest and dividends) ~16%, business owners' income ~8%, rent ~4%. Social-insurance contributions are then subtracted. Labor is the main source of household purchasing power, but it is not the only one. Transfers are already about a sixth.
- **Labor's share of GDP is ~53-56% [M]** (BEA compensation/GDI; BLS nonfarm labor share ~56-58%). It has been drifting down since about 2000.
- **Spending is concentrated at the top, and measurements disagree [V]:**
  - Top 10%: about 20% of spending in the BLS Consumer Expenditure survey, versus 49.2% in Moody's (Q2 2025).
  - Top 20%: 35% (BLS CE) versus 57% (Dallas Fed, 2020-25 average), up from 53% in the 1990s.
  - One 2026 paper puts the top-quintile share at 47-65% and notes that this group is also the most exposed to AI (arXiv 2603.09209).
  - Why it matters: if the top quintile is both the biggest spender and the most exposed, the domino starts from a larger base than a "low-wage automation" story would suggest.
- **Poorer households spend a larger share of extra income [V]:** MPC is 0.15 for the bottom quintile versus 0.06 for the top (annual, PSID; Fisher, Johnson, Smeeding and Thompson 2020). The one-off MPC out of stimulus checks is much higher, about 0.25-0.5 within a quarter for low-liquidity households [M] (Parker et al. 2013). If income shifts from wage earners to capital owners, demand falls by roughly ΔY × (MPC_labor − MPC_capital), unless the income is recycled through investment, taxes or transfers.
- **B2B depends on consumers indirectly [M]:** intermediate inputs are about 45% of US gross output (BEA input-output use tables). Measured through the total-requirements matrix, about two-thirds of B2B output ultimately serves household consumption. The rest serves government, investment and exports. B2B firms selling to government or defense (and to AI capex, which is booming) get extra runway beyond the scenario's framing. B2B firms selling to consumer-facing businesses (retail inputs, ad-tech, SaaS for SMBs) do not.

## 2. How cascades have spread in the past

- **Bullwhip amplification in 2008-09 [M]:** world trade volume fell ~12% in 2009 while world GDP was roughly flat (-0.1%). US industrial production fell ~17% from peak to trough, while real PCE fell only ~2-3%. Inventory and order cycles amplified the final-demand shock about 3-6x for upstream goods producers, with a lag of 1-3 quarters (Alessandria, Kaboski and Midrigan 2010; Altomonte et al. 2012). For goods, then, B2B gets worse swings but only slightly more time: the scenario's "more runway but not much more" matches the data.
- **Input-output propagation [V]:** after the 2011 Japan earthquake, shocks travelled both up and down supply chains. The disaster cut 0.47 pp from Japan's real GDP growth, and input-output links alone accounted for a 1.2 pp fall in gross output (Carvalho, Nirei, Saito and Tahbaz-Salehi, QJE 2021). Network amplification is real but moderate: roughly 1.5-2.5x the direct effect.
- **Great Depression, 1929-33 [M]:** real GDP fell ~27%, industrial production ~47%, the price level ~25%, and unemployment peaked at ~25%. Real GDP took until about 1936-37 to regain 1929 levels, and full employment returned only in WWII. That fall was driven by money, banks and debt deflation, not by technology, but it is the clearest case of self-reinforcing demand collapse.

## 3. Buffers: what slows or stops the domino

- **Automatic stabilizers [V]:** they absorb 34% of an unemployment-driven income shock in the US and 47% in the EU, which stabilizes demand by up to about 20% (US) and 30% (EU) (Dolls, Fuest and Peichl 2012).
- **Emergency fiscal response can be fast [M]:** in 2020 the CARES Act passed about 3 weeks after the emergency declaration. Personal income rose in 2020 even though about 22M jobs were lost. Transfers jumped from about 17% to over 25% of personal income. Visible, sudden shocks get large responses.
- **Gradual shocks get little response [M]:** in the China shock, about 1-2.4M manufacturing jobs were lost over 1999-2011 once supply links are counted. Transfers offset only a small share (roughly 10-15%) of lost local wage income, the effects lasted more than 10 years, and politics polarized (Autor, Dorn and Hanson 2013 and 2016; Autor et al. 2020). This matters most for S2: AI displacement looks more like a slow, sector-by-sector erosion than a COVID-style shock, unless it speeds up sharply.
- **Monetary offset [M]:** central banks can counter a lack of demand, through direct cash transfers if needed. The limit is the zero lower bound plus political constraints, not physical impossibility.
- **Falling prices [M]:** automation lowers costs, so the real value of a fixed transfer or pension goes up. This partly works against the domino, but only for people who still have some income.
- **Demand can be redirected rather than lost [M]:** AI owners' income can flow into investment (data centers, energy), luxury goods, or government via taxes. Aggregate demand can hold up while broad participation collapses, which is the scenario's "Ghost GDP" (arXiv 2603.09209). In that version the dominoes fall for mass-market firms, while firms serving the top of the market or AI capex do well. The "no customers" story therefore describes distribution (who is served) more robustly than it describes total GDP.

## 4. Reinstatement: does new work appear?

- **New work has been the norm so far [V]:** most US employment in 2018 was in job types introduced after 1940 (the widely quoted figure is ~60%). Since 1980, new work has clustered in high-paid professional roles and, secondarily, in low-paid services (Autor, Chin, Salomons and Seegmiller, QJE 2024).
- **Displacement vs reinstatement rates [M]:** Acemoglu and Restrepo (JEP 2019) estimate task displacement of ~0.48%/yr and reinstatement of ~0.47%/yr over 1947-87, roughly in balance. Over 1987-2017 displacement was ~0.70%/yr and reinstatement ~0.35%/yr, so the balance turned negative for labor. [V] for the qualitative findings: faster displacement and weaker reinstatement.
- **Past transitions were fast by historical standards but slow compared with AI timelines [M]:**
  - US farm employment fell from 41% (1900) to 16% (1945) to about 2% (2000): at most about 0.5-1 pp of employment per year.
  - Manufacturing fell from about 32% (1953) to about 8% (2024).
  - Engels' pause, about 1790-1840: output per worker rose ~46% while real wages rose ~12% (Allen 2009). Labor lost out for about 50 years before wages caught up.
- **Baumol effect [M]:** sectors that are hard to automate (in-person care, education, trades, hospitality) take a growing share of spending as automated goods get cheaper. Services are about 69% of PCE. This keeps human labor in demand and caps growth (Aghion, Jones and Jones 2017). The counterweight comes from Korinek and Suh (2024) [V]: if the complexity of tasks humans can do is bounded and full automation arrives, wages collapse. Wages can also fall before full automation if automation outpaces capital accumulation.
- **Exposure [M]:** about 80% of US workers have at least 10% of their tasks exposed to LLMs, and about 19% have at least 50% exposed (Eloundou et al. 2023).
- **Early evidence, through June 2026 [V]:** employment of 22-25-year-olds in AI-exposed occupations is 16% lower relative to peers (controlling for firm shocks), and 19% below its counterfactual path. There is no widespread displacement across the economy yet. The effect runs mainly through reduced hiring, not layoffs (Brynjolfsson, Chandar and Chen, Stanford Digital Economy Lab, Aug 2026).
- **Expert forecasts [V]** (Karger et al., NBER w35046, surveyed Oct 2025-Feb 2026):
  - The average economist puts 61.4% on moderate or rapid AI progress by 2030.
  - Unconditional forecasts: labor force participation falls from 62.6% to 61% by 2030 and 58.3% by 2050, mostly for demographic reasons.
  - Conditional on "rapid" progress: participation falls to 55% by 2050, about half of that due to AI (about 10M jobs); GDP growth is about 3.5-4%; the top 10%'s wealth share reaches 80%.
  - In other words, experts see even the rapid case as large but not a collapse. Their forecasts spread out widely under the rapid scenario.

## 5. UBI and redistribution: is it feasible?

- **Pilot evidence [V]:** in the OpenResearch study ($1,000/month for 3 years, n=3,000), recipients' earned income fell, by about $0.2-0.3 per dollar transferred going to extra leisure. Financial resilience improved; health effects were minimal. [M] Alaska's Permanent Fund Dividend shows no net employment loss (Jones and Marinescu 2022). Finland 2017-18 showed small positive employment and wellbeing effects.
- **Public support [V]:** 48% of Americans backed UBI for workers displaced by AI (Gallup/Northeastern 2018), with a strong partisan split (68% of Democrats vs 28% of Republicans). 80% of supporters want company taxes to pay for it. Economists: 37.4% back UBI, 71.8% back retraining, 13.7% back a job guarantee (Karger et al. 2026). About 70% of US adults expect AI to cause net job loss within 20 years (Pew, Sept 2026). [M] Swiss UBI referendum (2016): 23% yes.
- **Cost [M]:** $12k per US adult (about 260M adults) is about $3.1T, roughly 10-11% of GDP. Federal revenue is about 17% of GDP and corporate profits about 11-13% of GDP. It is fiscally possible if AI profits become large and taxable, but that takes political will. That links directly to S4's rentier-state argument: if AI firms are the tax base, the state can afford transfers, and whether it pays them is a political question.

---

## 6. Parameter priors

| # | Parameter | Central | Low | High | Unit | Conf. | Source |
|---|---|---|---|---|---|---|---|
| 1 | PCE share of GDP | 0.68 | 0.65 | 0.70 | frac | high | BEA NIPA [M] |
| 2 | Wage/benefit share of personal income | 0.62 | 0.58 | 0.65 | frac | high | BEA [M] |
| 3 | Transfer share of personal income (baseline) | 0.18 | 0.16 | 0.26 | frac | high | BEA [M]; 0.26 is the 2021 peak |
| 4 | Top-20% share of consumption | 0.50 | 0.35 | 0.65 | frac | med | BLS CE; Dallas Fed 2025; arXiv 2603.09209 [V] |
| 5 | MPC, bottom quintile (annual) | 0.15 | 0.10 | 0.50 | frac | med | Fisher et al. 2020 [V]; Parker et al. 2013 for high [M] |
| 6 | MPC, top quintile (annual) | 0.06 | 0.03 | 0.15 | frac | med | Fisher et al. 2020 [V] |
| 7 | Share of B2B output ultimately serving household consumption | 0.65 | 0.55 | 0.72 | frac | med | BEA IO total requirements [M] |
| 8 | Upstream amplification factor (goods, bullwhip) | 3 | 1.5 | 6 | x | med | 2008-09 trade collapse [M]; Carvalho et al. 2021 [V] |
| 9 | B2B lag behind B2C demand drop | 2 | 0.5 | 6 | quarters | low-med | 2008-09 order cycles [M]; services B2B (SaaS contracts) at upper end |
| 10 | Share of unemployment shock absorbed by automatic stabilizers (US) | 0.34 | 0.25 | 0.47 | frac | high | Dolls, Fuest and Peichl 2012 [V]; EU = 0.47 |
| 11 | Probability of large discretionary fiscal response to a sudden visible demand shock | 0.85 | 0.6 | 0.95 | prob | med | 2008 ARRA, 2020 CARES [M] |
| 12 | Probability of large response to a gradual, sector-by-sector displacement | 0.35 | 0.15 | 0.6 | prob | low | China shock, TAA under-reach [M] |
| 13 | Policy response lag once displacement is visible in aggregates | 1.5 | 0.1 | 5 | years | low | CARES (weeks) vs China shock (never at scale) [M] |
| 14 | Task displacement rate, pre-AI | 0.7 | 0.48 | 1.0 | %/yr of tasks | med | Acemoglu and Restrepo 2019 [M] |
| 15 | Task reinstatement (new work) rate | 0.35 | 0.2 | 0.5 | %/yr | med | Acemoglu and Restrepo 2019 [M]; Autor et al. 2024 [V] |
| 16 | Fastest historical sectoral employment shift | 0.8 | 0.5 | 1.2 | pp of total employment/yr | med | US agriculture 1900-45, manufacturing [M] |
| 17 | Workers with ≥50% of tasks LLM-exposed | 0.19 | 0.10 | 0.30 | frac | med | Eloundou et al. 2023 [M] |
| 18 | Observed early-career employment gap in exposed occupations (2026) | 0.16 | 0.13 | 0.19 | frac | high | Brynjolfsson, Chandar and Chen 2026 [V] |
| 19 | Expert P(moderate or rapid AI progress by 2030) | 0.61 | 0.4 | 0.8 | prob | med | Karger et al. 2026 [V] |
| 20 | Labor force participation in 2050, rapid scenario (expert median) | 0.55 | 0.45 | 0.60 | frac | low | Karger et al. 2026 [V]; baseline 0.583 |
| 21 | Share of UBI transfer offset by reduced earnings | 0.25 | 0.0 | 0.35 | frac | med | OpenResearch 2024 [V]; Alaska PFD ~0 [M] |
| 22 | US public support for AI-displacement UBI | 0.48 | 0.35 | 0.65 | frac | med | Gallup/Northeastern 2018 [V]; would likely rise with visible displacement |
| 23 | Cost of a $12k/adult UBI | 0.105 | 0.08 | 0.13 | frac of GDP | high | arithmetic [M] |
| 24 | Services share of PCE (Baumol buffer) | 0.69 | 0.65 | 0.75 | frac | high | BEA [M] |
| 25 | GDP peak-to-trough in worst demand collapse (Great Depression) | 0.27 | 0.10 | 0.40 | frac | high | US 1929-33 [M]; 0.40 ~ post-Soviet 1990s |

## 7. Historical analogs

| Case | What happened | Outcome | Relevance to S2 |
|---|---|---|---|
| Great Depression, 1929-33 | Demand cascade through banks and debt deflation; GDP -27%, unemployment 25% | US/UK recovered through the New Deal, abandoning gold, then WWII; Germany turned to fascism | Demand cascades can be severe. The political result depends on the regime (feeds S4). |
| 2008-09 GFC and trade collapse | 2-3% fall in final demand became 12-17% upstream falls | Recovered in 2-4 years with fiscal and monetary support | Measures the bullwhip. B2B lag is quarters, not years. |
| Japan 2011 earthquake | Supply-chain shock spread through the input-output network | Temporary; -0.47 pp GDP growth | Network amplification is about 1.5-2.5x, not unlimited |
| China shock, 1999-2011 | Slow regional job loss | Persistent local depression, weak compensation, political polarization | Best analog for gradual AI displacement: the domino is regional and partial, and the political response is weak |
| COVID 2020 | 22M jobs lost within weeks | Transfers made personal income rise; fast recovery | Shows the state can replace wage income quickly when the shock is visible and politically shared |
| US farm mechanization, 1900-70 | Farm employment 41% to about 4% | Absorbed by manufacturing and services over decades | Reinstatement worked because the transition was slow and new sectors existed |
| Engels' pause, UK 1790-1840 | Output up, wages flat for about 50 years; handloom weavers' wages collapsed | Wages eventually rose; reforms (Factory Acts, franchise) | A partial "no customers" period can last decades without total collapse |
| Post-Soviet collapse, 1990s | Supply chains and demand broke together; GDP fell ~40% | Mortality spike, oligarchic capture | Upper-bound analog for a disorderly cascade combined with elite capture |
| Rust Belt / Appalachia coal | Main industry disappeared | Long local decline; demand survived via transfers (disability, Medicaid) | Transfers put a floor under "customers" even without jobs |

## 8. Key uncertainties

1. **Aggregate vs broad demand.** AI-owner spending and AI capex may keep GDP up while mass-market firms fail. The domino may play out as a split of the economy into a top-end and a mass market, not a total collapse. The choice of S2 outcome variable (GDP vs median household income vs employment) drives the conclusion.
2. **Speed of displacement relative to political response.** Sudden, visible displacement historically triggers big transfers (COVID). Slow erosion historically does not (China shock). How fast AI diffuses is the swing variable.
3. **Tax capacity is not the bottleneck; political will is.** A UBI of about 10% of GDP is affordable if AI profits are taxable. Whether states choose to pay it connects directly to S4.
4. **Reinstatement under near-full automation** has no historical precedent. Autor-style "new work" may not apply if AI does the new tasks too (Korinek and Suh's bounded-complexity case).
5. **Consumption-concentration data disagree** (the top 10% share is 20% in BLS CE and 49% in Moody's). This decides whether white-collar automation hits a small or a large share of spending.
6. **B2B runway varies by sector:** goods suppliers see amplified swings with short lags; government and defense suppliers and AI-capex suppliers can grow while consumer demand shrinks.
7. **Deflation and monetary offsets** could keep real living standards up for people on transfers, weakening the "mouths to feed" framing in later stages.

## 9. Model v2 changes (post-review, 2026-09-30)

- **Timeline prior now a mixture** of forecaster families. Fast (median 7 yrs, weight 0.45): Metaculus community median for "first general AI" is Jan 2033 as of mid-2026, with weakly general AI around 2028 [V] (metaculus.com/questions/3479; aitoolsreview.co.uk summary, Sept 2026). Medium (median 20, weight 0.35): ESPAI 2023 HLMI 50% year 2047 [M]. Slow (median 45, weight 0.20): ESPAI full automation of occupations is much later; Karger et al. 2026 economists expect modest labour effects [V]. Validation: median jobs lost in 2050 is 7% (Karger's "rapid" case implies about 6% AI-driven), but the p90 is 40%.
- **Households use disposable income.** Bottom-80 APC is about 0.95, with a proportional permanent-income rule. Top-20 consume 55-75% of their disposable income plus 3-5%/yr out of wealth. That wealth term reconciles high top consumption shares with high top saving rates.
- **Other changes:** retained profits go to wealth (no leak); B2B per-seat channel added; household debt with default-driven credit crunch; monetary helicopter money that is blocked in 30-70% of draws; policy as a hazard re-evaluated every election cycle; transfers financed by a tax on automation rents; labour supply capped.
- **Two outcomes.** S2a (participation) is about 0.30. S2b (consumption cascade) is about 0.0003 in the base model and 0.15 only when every pessimistic option is combined. Average bottom-80 real consumption is hard to cut by 25%, for four reasons:
  - Wages are only about 55-60% of bottom-80 disposable income.
  - Transfers are already about 35% of it.
  - Some automation profits come back as capital income.
  - Automation-driven price falls raise real consumption.

  Consumption collapse is concentrated among displaced households, and a bottom-80 average does not capture it.
