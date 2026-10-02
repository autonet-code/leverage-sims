# m7: Decentralized alternatives (Alt A: parallel economy, Alt B: decentralized AI)

Research date: 2026-09-30. Priors for the simulation stage covering Alternative A (people decouple into a parallel economy/currency) and Alternative B (decentralized AI out-competes centralized providers on price before automation completes).

## Bottom line

1. **"Open" is not "decentralized".** Open-weight models are doing well: about a third of OpenRouter tokens, roughly 4 months behind the closed frontier. But almost all of them come from a few centralized labs (Qwen/Alibaba, DeepSeek, Meta, Mistral). Qwen alone accounts for about 69% of new fine-tunes. Alt B as described (a consensus network rewarding aligned work, a shared substrate) is a different thing. Its real traction is orders of magnitude smaller: Bittensor's verified external revenue is about $3-15M/yr against roughly $700B of 2026 hyperscaler capex.
2. **Truly decentralized training is about 1000x behind in compute.** Covenant-72B (March 2026, the largest permissionless run) used about 4.8e23 FLOP. 2026 frontier runs use about 1e26 to 1e27. That puts decentralized training roughly 3-5 years behind in compute, and the gap is not closing.
3. **Decentralized inference does not currently win on price.** Pine Analytics estimates that unsubsidized Bittensor inference (Chutes) would cost 1.6-3.5x centralized providers. The price edge comes from token emissions, which pay out about 20x the revenue.
4. **The historical pattern splits by layer.** Open or decentralized tech wins in the *infrastructure* layer: Linux holds about 45-60% of servers and cloud. It loses in the *consumer/convenience* layer: Linux desktop about 5% after 30 years, Mastodon under 0.2% of X, BitTorrent fell from 35% of traffic to under 3%, and crypto is used for payments by only about 2% of US adults. Where the open layer wins, centralized firms usually capture it (Android, AWS on Linux).
5. **Parallel economies are normal and large, but low productivity.** The informal sector averages about 31% of GDP worldwide (under 20% in the OECD) and covers 58% of the global workforce. Crisis-driven parallel currencies grow fast but collapse fast. Argentina's trueque reached about 2.5M members (about 7% of the population, around 27% counting families) in 2002, then lost 80-90% within about a year to counterfeiting and loss of trust. Durable examples (WIR, 90 years) stay small, at about 0.2% of Swiss GDP.
6. **States tolerate small parallel economies and suppress ones that threaten monetary sovereignty or tax collection.** Examples: Wörgl banned in 1933 along with about 200 copycats; the Liberty Dollar prosecuted in 2011; China's crypto ban in 2021; convictions of the Tornado Cash and Samourai developers in 2025. Suppression is only partly effective. China's share of Bitcoin mining went from 34% to 0%, then climbed back to 14-20% underground.
7. **The "no customers" domino interacts with Alt A in two directions.** Mass exclusion from the formal economy is exactly the condition under which parallel economies have grown historically (Argentina 2001, Greece 2015, the Soviet second economy). But those cases relied on human labour producing real goods, with land and energy still accessible. If the formal sector controls energy, land and compute, a parallel economy's output depends on what it is allowed to access (the scenario text's "tolerated" point).

## Parameters

| # | Parameter | Central | Low | High | Unit | Confidence | Source |
|---|---|---|---|---|---|---|---|
| 1 | Open-weight share of LLM tokens (OpenRouter, late 2025) | 33 | 20 | 40 | % | medium (OpenRouter skews to developers) | OpenRouter/a16z State of AI 100T token study |
| 2 | Open-weight share of enterprise LLM API usage (2025) | 11 | 8 | 19 | % | medium | Menlo Ventures 2025 (fell from 19% in 2024) |
| 3 | Capability lag, best open vs best closed model | 4 | 3 | 12 | months | medium-high (high end counts unreleased internal models) | Epoch AI ECI gap insight 2026 |
| 4 | Compute gap, largest permissionless decentralized training run vs frontier (2026) | 1000 | 200 | 3000 | x | medium (6ND estimate) | Covenant-72B arXiv 2603.08163 (72B params, 1.1T tokens gives about 4.8e23 FLOP); frontier 1e26 to 1e27 |
| 5 | Bittensor verified external (demand-side) revenue | 15 | 3 | 45 | $M/yr | low | Pine Analytics bear case ($3-15M); ecosystem claims $28-35M/yr, or $43M in Q1 2026 (unaudited) |
| 6 | Bittensor revenue / token emissions ratio | 0.05 | 0.02 | 0.2 | ratio | low-medium | Pine Analytics (largest subnet: $2.4M revenue vs $52M emissions) |
| 7 | Unsubsidized decentralized inference cost vs centralized | 2.3 | 1.6 | 3.5 | x | low-medium | Pine Analytics (Chutes vs DeepSeek/Together) |
| 8 | Decentralized compute (DePIN) revenue as share of AI infrastructure spend | 0.05 | 0.02 | 0.2 | % | low | Aethir about $128M in 2025, io.net about $20M ARR, Akash about $20M/yr, vs about $450B AI capex in 2026 (Futurum/CNBC) |
| 9 | 2026 hyperscaler capex (4 largest firms) | 700 | 600 | 725 | $B | high | CNBC Feb 2026, Futurum |
| 10 | Frontier labs' share of global AI compute (end 2025) | 40 | 25 | 50 | % | medium | Epoch AI "Frontier labs don't use most AI compute (yet)" (OpenAI 10-15%, top labs combined under 50%, rising) |
| 11 | Concentration within open-weight ecosystem: top family share of new fine-tunes | 69 | 44 | 69 | % | medium-high | ATOM Report arXiv 2604.07190 (Qwen 69% Feb 2026; Llama peaked at 44% in 2024) |
| 12 | Linux desktop share after about 30 years (consumer layer) | 4.7 | 4 | 5 | % | high | StatCounter 2025 |
| 13 | Linux server/cloud share (infrastructure layer) | 50 | 45 | 60 | % | medium | Industry estimates (44.8% server OS 2024; 49% cloud workloads) |
| 14 | Decentralized social vs incumbent (Mastodon MAU / X MAU) | 0.15 | 0.1 | 0.2 | % | medium | Mastodon 0.7-1M MAU 2025-26 vs X about 600M |
| 15 | Retention of a decentralized alternative after a protest-driven migration spike | 30 | 25 | 40 | % of peak MAU after about 3 years | medium | Mastodon 2.6M (Nov 2022) to about 0.7-1M (2025-26); Bluesky MAU about halved from peak |
| 16 | Peak-to-trough share loss of a decentralized protocol when convenient centralized pricing arrives | 90 | 80 | 95 | % | medium | BitTorrent 35% of traffic (2004) to under 3% (2022), displaced by Netflix/Spotify (Sandvine) |
| 17 | Share of US adults using crypto for payments | 2 | 1.5 | 3 | % | high | Fed SHED 2024/2025, KC Fed |
| 18 | Use of a decentralized currency despite a legal mandate (El Salvador BTC) | 8 | 7.5 | 20 | % of population, 2024 (20%+ in 2021) | high | UCA/UFG surveys, NBER |
| 19 | Real-economy stablecoin payments vs Visa | 3 | 2 | 4 | % of Visa volume (about $400B, growing about 100%/yr) | medium | Artemis/BVP, Spark 2025 analysis |
| 20 | Shadow economy, world average | 31 | 20 | 38 | % of GDP (OECD under 20; CH 7, AT 9) | medium | Medina & Schneider, IMF WP 18/17 and 2019 |
| 21 | Informal employment share of global workforce | 58 | 55 | 61 | % | high | ILO 2023, ILO WESO Trends 2026 |
| 22 | Peak crisis parallel-currency participation (Argentina 2002) | 7 | 5 | 27 | % of population (27% counting families) | medium | IPS 2002; about 2-3M prosumers out of 37M |
| 23 | Collapse of crisis parallel currency within about 1 year of peak | 85 | 70 | 90 | % decline in participants | medium | IPS 2002 (to 250k habitual prosumers), counterfeiting and hyperinflation of créditos |
| 24 | Soviet second economy share of urban household income (late 1970s) | 20 | 10 | 33 | % | medium | Grossman; Treml (Berkeley-Duke survey) |
| 25 | Long-lived complementary currency scale (WIR) | 0.2 | 0.1 | 0.5 | % of national GDP | medium | WIR turnover about CHF 1.4B in 2013, declining since 1992 peak; Bristol £ about £1M peak, closed 2021; Sardex about €51M |
| 26 | Long-run effectiveness of state suppression of a decentralized economic activity | 50 | 30 | 80 | % reduction vs counterfactual | low | China mining 34% to 0% to 14-20%; Wörgl fully stopped; Tornado Cash usage fell but did not stop |

### Suggested derived priors (my judgement, not sourced)

- P(permissionless/consensus-network AI above 10% of global AI inference spend by 2030): about 3% (1-8%). Growth would need to be roughly 100x in 4 years, *without* emission subsidies.
- P(open-weight models of any origin above 30% of global AI tokens in 2030): about 50% (30-70%). But this mostly reflects rivalry between centralized providers (US vs China), not Alt B.
- P(Alt B condition met: decentralized AI adoption outpaces automation): the base rate that a decentralized challenger overtakes a convenience-driven, network-effect incumbent in the consumer/enterprise layer within 10 years is close to 0 in the cases listed. The infrastructure-layer path (Linux-like) took 15-25 years, and the value was then captured by centralized firms. A reasonable prior is 2-10%, higher if states subsidize public/open AI (the EU, India and Switzerland have public-model efforts).
- P(parallel economy above 10% of GDP in a large advanced economy by 2035, conditional on severe AI job displacement): 15-35%. Informal sectors already exceed 10% in most countries, so the growth would come from people pushed out of formal work.
- P(state tolerates a parallel economy, given it stays small and pays some tax): about 0.8. P(active suppression, given it reaches macro relevance and erodes the tax base or monetary control): 0.5-0.7.

## Historical analogs

| Case | Outcome | Relevance |
|---|---|---|
| Linux vs Windows/Unix (1991 to now) | Won servers, cloud, supercomputers and phones (via Android) over 15-25 years. Desktop about 5%. | The infrastructure layer can go open, but centralized firms captured the value (AWS, Google). |
| BitTorrent vs Netflix/Spotify | 35% of traffic in 2004, under 3% by 2022 | Decentralized tech loses when centralized services get cheap and convenient. Reverse risk for Alt B: price is exactly the weapon. |
| Mastodon/Bluesky vs X (2022 to 2026) | Protest-driven spikes, then about 30-50% retention. Now 0.1-7% of the incumbent. | Anger at a "rigged" incumbent produces migration spikes, not a transition. |
| Bitcoin as money / El Salvador | Held mainly as an investment. Payment use 2% in the US, 8% in El Salvador even with a legal mandate. Legal tender status dropped for IMF deal 2025. | Even state backing did not make decentralized currency the medium of exchange. |
| Stablecoins in Venezuela/Argentina | Widely used as a dollar substitute in high-inflation economies | Parallel money does get adopted when the official one fails. But the stablecoins are centralized (Tether), not decentralized. |
| Bittensor (2021 to 2026) | About $2.6B market cap, revenue about $3-45M/yr, emissions about 20x revenue. Covenant-72B was a real technical milestone, but a leading subnet team later left. | Closest real-world version of Alt B. The price edge is currently subsidized. |
| Prime Intellect INTELLECT-1/2, Nous Psyche | Permissionless training up to 32B params (RL) and 72B (pretraining) | Proof it works, about 3 orders of magnitude behind the frontier. |
| Argentina trueque 2001-2002 | About 2.5M members at peak. Collapsed about 85% in a year (counterfeit créditos, no central governance). | The best "no customers" analog: mass exclusion leads to rapid parallel-economy growth, then collapse from trust and scaling failure. |
| Greece 2015 (capital controls, TEM Volos, barter sites) | Local currencies and barter grew but stayed marginal. The euro remained dominant. | Crisis boosts parallel economies only modestly in a rich economy with a welfare state. |
| Soviet second economy | About 10-30% of urban household income for decades. Tolerated in practice, periodically punished. | A long-lived parallel economy under an authoritarian state that relied on it; tolerance served the state's interest. |
| WIR Bank (1934 to now) | Survived 90 years at about 0.2% of Swiss GDP. Counter-cyclical (Stodder). | Durable, legal, tolerated because it is small, B2B and taxed. |
| Wörgl stamp scrip 1932-33 | Worked locally. Banned by the Austrian central bank, which also blocked about 200 copycat towns. | The state suppresses local currency once it spreads. |
| Liberty Dollar 1998-2011 | Founder convicted of counterfeiting; about $7M of silver seized | US enforcement against private currencies that resemble legal tender |
| China crypto ban 2021 | Mining fell from 34% to 0%, then 14-20% came back underground | Suppression works partly. Decentralized activity persists at reduced scale. |
| Tornado Cash / Samourai (2022-2025) | Sanctions, then Storm convicted on one count and Samourai developers took 5-year pleas | States will criminalize the developers of decentralized tools that route around control. Relevant to Alt A/B being "tolerated". |

## Key uncertainties

- Whether AI capability keeps scaling with centralized compute (which favours incumbents) or plateaus so that distillation lets small or decentralized players reach "good enough" cheaply. Epoch's 4-month open-weight lag suggests diffusion is fast. The 1000x decentralized compute gap says production stays centralized.
- Whether Chinese and other open-weight releases continue. They are the main thing putting price pressure on centralized providers today, and they are a strategic choice by a few firms and one state, not a decentralized movement.
- The accuracy of crypto-ecosystem revenue figures. They are unaudited and sources differ by about 10x.
- Whether a parallel economy of excluded people can get land, energy and compute. Historical cases always had human labour as the productive core. In an automated economy, excluded humans may have little that insiders want to trade for.
- The state's response. The rentier-state logic (S4) implies low tolerance if a parallel economy cuts into the AI tax base. Democratic states may instead back public or open AI.
- Measurement: OpenRouter token share overstates developer and hobbyist open-model use. Menlo's survey is small, and "usage" is defined differently across sources.

## Sources

- OpenRouter/a16z State of AI: https://openrouter.ai/state-of-ai ; https://arxiv.org/abs/2601.10088
- Menlo Ventures 2025 State of GenAI in the Enterprise: https://menlovc.com/perspective/2025-the-state-of-generative-ai-in-the-enterprise/
- Epoch AI open-closed gap: https://epoch.ai/data-insights/open-closed-eci-gap ; https://epoch.ai/data-insights/open-weights-vs-closed-weights-models
- Epoch AI frontier labs compute share: https://epoch.ai/gradient-updates/frontier-labs-dont-use-most-ai-compute
- ATOM Report: https://arxiv.org/abs/2604.07190
- Covenant-72B: https://arxiv.org/abs/2603.08163 ; https://huggingface.co/1Covenant/Covenant-72B
- INTELLECT-2: https://arxiv.org/abs/2505.07291
- Pine Analytics, Bear case for Bittensor: https://pineanalytics.substack.com/p/the-bear-case-for-bittensor-tao
- FalconX State of Bittensor: https://www.falconx.io/newsroom/state-of-bittensor-subnet-adoption-trends-network-mechanics-and-covenants-departure
- DePIN revenue: https://blockeden.xyz/blog/2026/03/12/depin-compute-revenue-pivot-akash-ionet-aethir/ ; https://messari.io/report/state-of-akash-q3-2025
- Hyperscaler capex: https://www.cnbc.com/2026/02/06/google-microsoft-meta-amazon-ai-cash.html ; https://futurumgroup.com/insights/ai-capex-2026-the-690b-infrastructure-sprint/
- StatCounter desktop OS: https://gs.statcounter.com/os-market-share/desktop/worldwide
- Mastodon MAU: https://techcrunch.com/2023/10/02/amid-twitter-chaos-mastodon-grew-donations-488-in-2022-reached-1-8m-monthly-active-users ; https://marketful.com/mastodon-statistics
- BitTorrent traffic: https://torrentfreak.com/bittorrent-is-no-longer-the-king-of-upstream-internet-traffic-240315/ ; https://en.wikipedia.org/wiki/BitTorrent
- Fed/KC Fed crypto payments: https://www.kansascityfed.org/research/payments-system-research-briefings/us-consumers-use-of-cryptocurrency-for-payments/
- El Salvador: https://www.nber.org/digest/202207/el-salvadors-experiment-bitcoin-legal-tender ; https://www.elsalvadornow.org/2025/01/17/92-of-salvadorans-did-not-use-bitcoin-in-2024-el-92-de-salvadorenos-no-uso-bitcoin-en-2024/
- Stablecoin volumes: https://www.bvp.com/atlas/stablecoins-from-defi-primitive-to-global-financial-infrastructure ; https://www.spark.money/research/stablecoin-transfer-volume-eleven-trillion
- Medina & Schneider (IMF): https://www.imf.org/en/publications/wp/issues/2018/01/25/shadow-economies-around-the-world-what-did-we-learn-over-the-last-20-years-45583
- ILO informal employment: https://www.wiego.org/informal-economy/statistical-picture/
- Argentina trueque: https://www.ipsnews.net/2002/11/argentina-the-rise-and-fall-of-the-great-bartering-network/
- Soviet second economy: https://public.econ.duke.edu/Papers/Other/Treml/2ndecon.pdf ; https://en.wikipedia.org/wiki/Second_economy_of_the_Soviet_Union
- WIR: https://en.wikipedia.org/wiki/WIR_Bank ; http://www.jimstodder.com/WIR_Panel_CES.pdf
- Bristol pound: https://en.wikipedia.org/wiki/Bristol_pound
- Wörgl/Sardex/Chiemgauer: https://en.wikipedia.org/wiki/W%C3%B6rgl ; https://wiki.p2pfoundation.net/History_of_Stamp_Scrip
- Liberty Dollar: https://en.wikipedia.org/wiki/Bernard_von_NotHaus
- China mining ban: https://www.cnbc.com/2021/12/10/bitcoin-network-hashrate-hits-all-time-high-after-china-crypto-ban.html ; https://finance.yahoo.com/news/china-underground-bitcoin-mining-rebounds-120146540.html
- Tornado Cash / Samourai: https://www.mayerbrown.com/en/insights/publications/2025/08/the-tornado-cash-trials-mixed-verdict-implications-for-developer-liability ; https://www.dlnews.com/articles/regulation/samurai-wallet-devs-plead-guilty-to-money-transmitting/
- Greece dual currency: https://www.weforum.org/stories/2016/01/how-greece-became-a-dual-currency-economy/
- Venezuela stablecoins: https://en.cryptonomist.ch/2025/09/30/venezuela-turning-point-in-payments-usdt-becomes-the-operational-dollar/
