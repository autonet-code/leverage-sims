# S3 Provider Concentration: research priors

Stage claim (scenario text): once everyone depends on a few AI providers, providers raise prices and keep the margin that automating firms briefly enjoyed.

Research date: 2026-09-30. Confidence tags: H = primary/strong source, M = reputable secondary or triangulated, L = weak/secondary blog or my judgement.

## 1. Where things stand (2026)

| Layer | Concentration | Source |
|---|---|---|
| Frontier model APIs (enterprise spend) | Anthropic ~40%, OpenAI ~27%, Google ~21% (end 2025). Top-3 ~88%. HHI ~2,800 | Menlo Ventures State of GenAI 2025 |
| Cloud infrastructure | AWS ~28-31%, Azure ~20-24%, Google ~12-15%; top-3 ~67%. HHI ~1,500-1,700 | Synergy Research Q2 2026 (via Statista and press) |
| AI accelerators | Nvidia ~80-85% (AMD ~6%, rest custom ASICs: TPU, Trainium). HHI ~6,500+ | SiliconAnalysts; Nvidia FY26 DC revenue ~$194B |
| Foundry | TSMC 72.5% of all foundry revenue (Q2 2026), >90% of leading-edge AI logic; Samsung 5.9% | TrendForce Q2 2026 |
| Advanced packaging | Nvidia booked ~60% of TSMC CoWoS 2026 | ClusterBid / industry reports (M) |

Key nuance: concentration increases as you go down the stack. The model layer is an oligopoly with a strong open-weight fringe; the chip and fab layers are near-monopolies. If rent extraction happens, the compute layer is at least as likely a beneficiary as the model labs (Nvidia gross margin ~73-75%).

## 2. Counterforces already visible

- **Open-weight lag is short.** Epoch AI: open models trailed closed frontier by ~3 months (2023-Oct 2025) and ~4 months (2026, ~8 ECI points). On FrontierMath, Chinese open models lag ~7 months.
- **Open models win volume, closed win revenue.** OpenRouter: Chinese open-weight models went from ~1% of tokens (late 2024) to ~50-60% (mid/late 2026), yet closed models capture ~96% of revenue (TechTimes, Sept 2026). OpenRouter skews price-sensitive developers; in enterprise production Menlo put open-source at ~11-13% of workloads (2025).
- **Price at fixed capability collapses.** Epoch: 9x-900x/yr depending on task, median ~40-50x/yr; GPT-4-class went from ~$30/M tokens (2023) to <$1 (2026). Frontier-tier prices, however, are roughly flat to rising (some reports of 1.5-2x price step-ups on newest tiers in 2026, L).
- **Low switching costs so far.** 55% of CIOs switched provider at least once; 81% of large enterprises use 3+ model families (a16z); but most upgrades stay within a provider (66% vs 11% switched vendor).
- **Lab margins improving, not monopoly-level.** Frontier lab gross margins ~40-60% in 2026 (Anthropic from -94% in 2024), API margins reported higher; OpenAI still deeply operating-negative. These are margins from falling inference cost, not visible price hikes.
- **Regulation against lock-in.** EU Data Act bans cloud switching/egress fees from 12 Jan 2027; DMA forced Apple steering changes (EUR 500M fine, 2025); US Epic v Apple contempt ruling upheld Dec 2025.

## 3. Parameters

| # | Parameter | Central | Low | High | Unit | Conf. | Sources |
|---|---|---|---|---|---|---|---|
| 1 | Frontier model market HHI, 2026 | 2800 | 2200 | 3500 | HHI | M | Menlo Ventures 2025 |
| 2 | Frontier model market HHI, 2032 (projection) | 2600 | 1500 | 5000 | HHI | L | judgement; training cost trend (Epoch) vs open-weight pressure |
| 3 | Top-3 cloud share | 0.67 | 0.63 | 0.70 | frac | H | Synergy Q2 2026 |
| 4 | Nvidia AI accelerator share, 2026 | 0.82 | 0.70 | 0.90 | frac | M | SiliconAnalysts; custom-ASIC inclusion drives range |
| 5 | Nvidia AI accelerator share, 2030 | 0.62 | 0.40 | 0.80 | frac | L | judgement; TPU/Trainium/AMD ramp |
| 6 | TSMC share of leading-edge AI logic | 0.92 | 0.85 | 0.97 | frac | M | TrendForce, industry |
| 7 | Open-weight capability lag, 2026 | 4 | 3 | 7 | months | H | Epoch AI data insights |
| 8 | Open-weight lag, 2030 (projection) | 6 | 2 | 24 | months | L | widens if labs stop releasing, compute gap, or regulation; narrows via distillation |
| 9 | P(open-weight lag > 12 months by 2030) | 0.2 | 0.08 | 0.4 | prob | L | judgement |
| 10 | Price decline at fixed capability | 40 | 9 | 200 | x per year | H | Epoch "LLM inference price trends" |
| 11 | Frontier-tier nominal price change | -0.15 | -0.6 | +0.5 | frac/yr | L | observed list prices 2023-2026 |
| 12 | Frontier lab gross margin, 2026 | 0.50 | 0.40 | 0.80 | frac | M | press on Anthropic/OpenAI financials |
| 13 | Nvidia gross margin | 0.74 | 0.60 | 0.78 | frac | H | Nvidia filings |
| 14 | Share of enterprise production workloads on open models | 0.13 | 0.08 | 0.30 | frac | M | Menlo 2025; OpenRouter as upper bound |
| 15 | LLM switching cost (fraction of annual spend) | 0.10 | 0.02 | 0.40 | frac | L | CIO surveys; rises with agent/memory/fine-tune lock-in |
| 16 | Fraction of provider cost declines retained as margin (not passed through) | 0.5 | 0.2 | 0.8 | frac | L | analogs: cloud, Nvidia, app stores |
| 17 | Share of automation surplus captured by AI/compute providers (steady state) | 0.25 | 0.05 | 0.60 | frac | L | analogs: SaaS/cloud take, platform take rates 15-30% |
| 18 | Platform take-rate ceiling observed historically (app stores) | 0.30 | 0.15 | 0.30 | frac | H | Apple/Google stores 2008-2020 |
| 19 | Cloud egress markup over wholesale transit | 20 | 10 | 80 | x | M | Cloudflare 2021 analysis; being regulated away |
| 20 | Lag from antitrust suit to remedy (US) | 8 | 3 | 12 | years | H | cases below |
| 21 | P(structural breakup given US monopolization liability), post-1980 | 0.1 | 0.02 | 0.3 | prob | M | AT&T yes (1982 consent); Microsoft reversed; Google behavioral |
| 22 | Number of labs within 6 months of frontier, 2026 | 7 | 5 | 10 | count | M | Epoch ECI; OpenAI, Anthropic, Google, xAI, DeepSeek, Alibaba, Moonshot |
| 23 | Frontier training compute cost growth | 2.4 | 2.0 | 3.0 | x per year | H | Cottier et al. 2024 (Epoch) |
| 24 | P(tight model oligopoly, HHI>2500, persists to 2032) | 0.5 | 0.3 | 0.7 | prob | L | judgement |
| 25 | P(providers raise real prices and capture majority of automation surplus by 2035, i.e. S3 as stated) | 0.2 | 0.08 | 0.4 | prob | L | judgement from all above |

## 4. Historical analogs

| Case | What happened | Lesson for S3 |
|---|---|---|
| Standard Oil (1870-1911) | ~90% of US refining by ~1880; kerosene prices fell over the period (debate over predation, McGee 1958); 1906 suit, 1911 breakup into 34 firms | Dominance did not show up mainly as higher prices; remedy took ~30 years from dominance |
| AT&T / Bell System (1913-1984) | Regulated monopoly; high long-distance rates cross-subsidized local; 1974 suit, 1984 divestiture; prices fell after | Rents can persist decades under state tolerance; breakup possible but slow |
| IBM (1969-1982) | 13-year case dropped; market shifted to minicomputers/PCs anyway | Technology shifts often beat antitrust |
| Microsoft (1990s-2001) | ~90%+ desktop OS; 2000 breakup order reversed, 2001 behavioral settlement; dominance eroded by web/mobile, not courts | Behavioral remedies weak; platform shift is the real check |
| Intel (x86) | ~80% share for decades; EU fine 2009 (later annulled in part); lost ground to TSMC/AMD/ARM in 2018+ | Manufacturing lead can flip within ~5 years |
| Google Search (2004-) | ~90% share; liability 2024; remedies Sept/Dec 2025 were behavioral (no Chrome divestiture), both sides appealing | Modern US remedies rarely structural; genAI is the bigger competitive threat |
| Apple/Google app stores (2008-) | 30% fee stable ~12 years; 15% small-dev tier 2021; DMA, Epic contempt ruling forced steering | Take rates of 15-30% are sustainable for years until regulation bites |
| Cloud egress (2006-) | Egress priced far above cost as lock-in; free-on-exit waivers 2024-25; EU ban Jan 2027 | Lock-in fees get regulated once salient, with ~15-year lag |
| Nvidia (2016-) | CUDA lock-in, ~75% gross margins, share ~80-90%; hyperscalers respond with custom chips | Compute layer is where rent is currently being captured |
| OPEC (1973-) | Cartel quadrupled prices 1973-74; demand response and new supply eroded power by mid-1980s | Coordinated price hikes on an essential input work short term, invite substitution |
| DeepSeek shock (Jan 2025) | Cheap open model near frontier knocked ~17% off Nvidia in a day, forced price cuts | Open-weight fringe disciplines pricing at the model layer |

## 5. Assessment

The scenario text's mechanism (few providers, then price hikes) has real support at the compute layer (Nvidia, TSMC) and partial support at the frontier model layer (HHI ~2,800, rising frontier-tier prices). Against it: a 3-7 month open-weight lag, 40x/yr price collapse at fixed capability, low switching costs today, multiple competing jurisdictions (US vs China labs), and regulators who do act, although with a 5-15 year lag. Historically, dominant platforms extracted rent mostly by keeping cost declines as margin and charging 15-30% take rates, not by dramatic price hikes. The most plausible S3 variant is "providers capture a sizeable minority of automation surplus" rather than "providers capture all of it".

## 6. Key uncertainties

- Whether open-weight releases continue (lab policy, US/China regulation, export controls, safety-driven restrictions).
- Whether frontier (not commodity) capability is what matters for automating high-value professional work; if yes, the 4-month lag matters more.
- Whether agentic workflows, memory and proprietary data create lock-in that current low switching costs do not reflect.
- Compute supply: a Taiwan disruption would spike prices regardless of market structure.
- Whether states would act against their biggest taxpayers (link to S4 rentier logic); antitrust has historically moved slowly but did move.
- Interaction with S2: if aggregate demand collapses, providers lose their customers' revenue too, which limits rent extraction.
- Many 2026 figures come from secondary press summaries of Menlo, Synergy, OpenRouter, and lab financials; verify before relying on precise values.

## Sources

- Epoch AI, Open models lag closed by 4 months: https://epoch.ai/data-insights/open-closed-eci-gap
- Epoch AI, Open-weight models lag ~3 months: https://epoch.ai/data-insights/open-weights-vs-closed-weights-models
- Epoch AI, LLM inference price trends: https://epoch.ai/data-insights/llm-inference-price-trends
- Menlo Ventures, 2025 mid-year LLM market update: https://menlovc.com/perspective/2025-mid-year-llm-market-update/
- Menlo 2025 report coverage: https://finance.yahoo.com/news/menlo-ventures-2025-state-generative-123000623.html
- Statista / Synergy cloud share: https://www.statista.com/chart/18819/worldwide-market-share-of-leading-cloud-infrastructure-service-providers/
- TrendForce foundry Q2 2026: https://www.trendforce.com/presscenter/news/20260909-13225.html
- SiliconAnalysts Nvidia share: https://siliconanalysts.com/analysis/nvidia-ai-accelerator-market-share-2024-2026
- ClusterBid CoWoS: https://clusterbid.com/blog/gpu-supply-chain-2026-tsmc-cowos-nvidia-allocation-lead-times
- OpenRouter State of AI: https://openrouter.ai/state-of-ai
- TechTimes on open tokens vs closed revenue: https://www.techtimes.com/articles/327646/20260917/chinese-open-weight-ai-handles-most-developer-tokens-closed-models-capture-96-revenue.htm
- Dataiku CIO survey (switching): https://www.dataiku.com/blog/ai-switching-problem
- Anthropic margins coverage: https://finance.yahoo.com/markets/stocks/articles/anthropics-gross-margin-most-important-070500338.html
- Alphabet 10-Q (search remedies): https://www.sec.gov/Archives/edgar/data/0001652044/000165204426000071/goog-20260630.htm
- Google appeal status: https://www.litigationlogic.io/legal-news/google-and-doj-both-challenge-judge-mehta-s-antitrust-remedies-order-at-dc-circuit-2026/
- Apple 10-Q (DMA fine, Epic): https://www.sec.gov/Archives/edgar/data/0000320193/000032019326000020/aapl-20260627.htm
- EU Data Act switching: https://kempitlaw.com/insights/the-end-of-switching-charges-commercial-impact-and-compliance-priorities/
- Cottier et al. 2024, rising costs of training frontier models (Epoch): https://arxiv.org/abs/2405.21015
- McGee 1958, Predatory Price Cutting: The Standard Oil (N.J.) Case, J. Law & Econ.
