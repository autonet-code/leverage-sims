# S1 research: automation race (m1_automation_race)

As of 2026-09-30. Tags: [web] = checked via search this session; [lit] = well-known literature figure recalled, verify before citing publicly.

## Bottom line
- Technical exposure is high and rising fast (McKinsey Nov 2025: 57% of US work hours technically automatable with today's tech; METR agent time horizons doubling every ~3-4 months since 2024; inference cost for fixed capability falling ~10-50x/yr).
- Realized adoption and labor effects are still modest: ~18-20% of US firms use AI in production (Census BTOS, May 2026), ~41% of workers use genAI at work, no economy-wide displacement, but a 19% employment gap for 22-25 year olds in AI-exposed jobs (Stanford/ADP, Aug 2026), operating via reduced hiring.
- History: general-purpose technologies took 20-40 years from first use to majority diffusion (steam, electricity, computers). Software-delivered AI is faster on the adoption side, but organizational complements remain the bottleneck.
- Competitive forcing is real (robot adopters gain share, non-adopters shed jobs: Koch et al; Acemoglu-Lelarge-Restrepo), but historically it reallocated rather than eliminated employment. Whether S1 feeds S2 hinges on whether new-task creation keeps up; no historical case tests near-complete cognitive automation.

## Parameters

| # | Parameter | Central | Low | High | Unit | Source |
|---|---|---|---|---|---|---|
| 1 | US firm AI use (production), mid-2026 | 19 | 17 | 20 | % firms | Census BTOS May 2026 [web] |
| 2 | Large-firm (250+) AI use, 2026 | 37 | 32 | 40 | % firms | Census BTOS [web] |
| 3 | Worker genAI use at work, late 2025 | 41 | 30 | 50 | % workers | Fed FEDS Note Apr 2026 (RPS) [web] |
| 4 | Employment share at AI-adopting firms | 78 | 54 | 85 | % labor force | SBU via Fed note (54% at LLM-using firms) [web] |
| 5 | Worker genAI adoption growth | 31 | 20 | 45 | %/yr relative | Fed note [web] |
| 6 | Tasks technically automatable now (US hours) | 57 | 30 | 65 | % hours | McKinsey MGI Nov 2025 (44 agents + 13 robots); 2023 estimate 30% by 2030 [web] |
| 7 | Workers with >=50% tasks LLM-exposed | 19 | 15 | 46 | % workers | Eloundou et al 2023 (46% incl. complementary software) [lit] |
| 8 | Workers with >=10% tasks exposed | 80 | 70 | 90 | % workers | Eloundou et al 2023 [lit] |
| 9 | Jobs exposed to AI (advanced economies) | 60 | 40 | 60 | % jobs | IMF SDN 2024 (40% global, ~60% AEs, about half of those complementary) [lit] |
| 10 | Tasks profitably automated within 10 yrs | 4.6 | 2 | 25 | % tasks | Acemoglu 2024 (low/central-conservative); Goldman 2023 ~25% of work automatable (high) [lit] |
| 11 | Inference price decline at fixed capability | 40 | 9 | 200 | x per year | Epoch AI (median ~50x, range 9-900x; post-2024 ~200x; GPT-4-level GPQA 40x) [web] |
| 12 | Agent time-horizon doubling time | 4 | 3 | 7 | months | METR TH1.1 Jan 2026 (7mo long-run, 4.3mo since 2023, ~3mo since 2024) [web] |
| 13 | Automation share of AI use (vs augmentation) | 45 | 41 | 50 | % of conversations | Anthropic Economic Index 2025-26 (augmentation 52-55%) [web] |
| 14 | Young-worker employment gap, AI-exposed jobs | 19 | 13 | 25 | % below trend | Brynjolfsson, Chandar, Chen, Aug 2026 [web] |
| 15 | Earnings/hours effect of chatbot adoption, 2 yrs | 0 | -2 | 2 | % | Humlum & Vestergaard 2025, Denmark [web] |
| 16 | Realized time savings from chatbots | 3 | 2 | 15 | % of hours | Humlum & Vestergaard (low); experimental task studies 14-40% [web/lit] |
| 17 | US nonfarm labor share, 2025Q3 | 53.8 | 53 | 55.6 | % of output | BLS (record low since 1947; decade avg 55.6) [web] |
| 18 | Global labor share decline since 1975 | 5 | 3 | 6 | pp | Karabarbounis & Neiman 2014 [lit] |
| 19 | Robot effect: +1 robot per 1000 workers | -0.2 | -0.4 | -0.1 | pp emp/pop | Acemoglu & Restrepo 2020 (wages -0.42%) [lit] |
| 20 | Manufacturing robot density, 2024 | 204 | 131 | 1220 | per 10k workers | IFR 2025 (N. America 204, Asia 131, Korea 1220) [web] |
| 21 | GPT diffusion lag, first use to ~50% adoption | 25 | 10 | 45 | years | Comin & Hobijn 2010 (historic avg ~45 yrs, shrinking); US factory electrification ~30 yrs (David 1990) [lit] |
| 22 | Prob. a firm automates given cost advantage and rival automation (competitive forcing) | 0.7 | 0.4 | 0.9 | probability | Judgmental, from robot-adopter share-gain evidence (Koch, Manuylov, Smolka 2021; Acemoglu, Lelarge, Restrepo 2020) |
| 23 | Expert-forecast year, full automation of labor (50%) | 2116 | 2060 | 2200 | year | Grace et al 2024 AI Impacts survey (HLMI 50% by 2047); forecasters much earlier [lit] |

## Historical analogs

- **Steam (UK, 1760-1870):** negligible TFP contribution until after ~1830 (Crafts 2004); real wages lagged output for decades ("Engels' pause"). Outcome: long lag, distributional pain, eventual broad gains.
- **Electrification (US factories):** ~5% of factory power in 1900, ~50% mid-1920s, ~80% by 1930 (David 1990). Productivity surge only after factory redesign. Outcome: ~30-year lag, employment grew.
- **Computers / IT:** Solow paradox (1987), productivity boom 1995-2004. Outcome: routine-task job polarization (Autor, Levy, Murnane 2003), not mass unemployment; labor share drifted down.
- **ATMs (1970-2010):** ATMs ~100k to ~400k (1995-2010) while US teller jobs stayed roughly flat, as cheaper branches multiplied (Bessen 2015). Outcome: task shift. Tellers declined only later with mobile banking.
- **Industrial robots (1993-2016):** negative local employment/wage effects (Acemoglu-Restrepo); adopting firms gain share and hire, non-adopting competitors shrink (Koch et al, Spain; Acemoglu-Lelarge-Restrepo, France). Outcome: textbook competitive forcing, small aggregate effect.
- **Agricultural mechanization (US 1900-1970):** farm employment ~40% to <5% of workforce. Outcome: near-total displacement of the largest occupation, absorbed over ~2 generations by new sectors and new demand.
- **Horses (US 1910-1960):** ~26M to ~3M once engines matched all their tasks. Outcome: canonical "no new tasks" case, often cited for full-substitution AI.
- **Containerization (1960s-80s):** longshore employment collapsed within ~15 years in major ports while trade boomed. Outcome: concentrated displacement, aggregate gain.
- **Generative AI (2022-2026):** fastest consumer uptake on record; firm production use still ~1 in 5; entry-level hiring weakening in substitution-type exposed jobs; no aggregate displacement yet; labor share at record low (causality unclear).

## Key uncertainties
1. Exposure vs cost-effective automation: Acemoglu 4.6% vs McKinsey 57% is a >10x spread.
2. Whether agent capability trends (METR) persist and generalize beyond software.
3. Organizational lag: does software-delivered AI skip the 20-30 year GPT diffusion lag?
4. New-task creation ("reinstatement", Acemoglu-Restrepo) vs displacement rate.
5. Young-worker hiring gap: AI-driven vs rates/post-COVID tech correction.
6. Inference price declines may slow; frontier pricing stickier than fixed-capability pricing (link to S3 provider pricing power).
7. Survey "AI use" conflates light chatbot use with process automation.

## Sources
- Census BTOS AI use, May 2026: https://www.census.gov/library/stories/2026/05/ai-use-businesses.html
- Fed FEDS Note, Monitoring AI Adoption, Apr 2026: https://www.federalreserve.gov/econres/notes/feds-notes/monitoring-ai-adoption-in-the-u-s-economy-20260403.html
- McKinsey MGI, Agents, Robots, and Us (Nov 2025): https://www.mckinsey.com/mgi/our-research/agents-robots-and-us-skill-partnerships-in-the-age-of-ai
- Epoch AI, LLM inference price trends: https://epoch.ai/data-insights/llm-inference-price-trends
- METR Time Horizon 1.1: https://metr.org/blog/2026-1-29-time-horizon-1-1/
- Anthropic Economic Index: https://www.anthropic.com/research/anthropic-economic-index-january-2026-report
- Brynjolfsson, Chandar, Chen, Canaries (Aug 2026): https://digitaleconomy.stanford.edu/news/canariesaug26/
- Humlum & Vestergaard, NBER w33777: https://www.nber.org/papers/w33777
- BLS labor share (FRED PRS85006172): https://alfred.stlouisfed.org/series?seid=PRS85006172 ; https://fortune.com/2026/01/13/us-workers-smallest-labor-share-gdp-on-record/
- IFR robot density: https://ifr.org/ifr-press-releases/news/robot-density-surges-in-europe-asia-and-americas
- Literature (not re-fetched): Eloundou et al 2023 "GPTs are GPTs" (Science 2024); Acemoglu 2024 "The Simple Macroeconomics of AI"; IMF SDN/2024/001; Goldman Sachs 2023 (Briggs & Kodnani); Acemoglu & Restrepo 2020 JPE; Karabarbounis & Neiman 2014 QJE; David 1990 AER; Comin & Hobijn 2010 AER; Bessen 2015; Koch, Manuylov, Smolka 2021 EJ; Acemoglu, Lelarge, Restrepo 2020 AEA P&P; Crafts 2004 EJ; Grace et al 2024.

## v2 model revision (2026-09-30, after structural review)

Verified this session:
- Acemoglu & Restrepo 2019 JEP: reinstatement +0.47%/yr (1947-87) and +0.35%/yr (1987-2017); displacement -0.48%/yr and -0.70%/yr. [web, from paper PDF]
- METR (May 2026): best model 50% horizon >=16h, 80% horizon ~3.1h; measurements above 16h unreliable. [web]
- Metaculus general AI (4-part definition incl. robotics): community median ~Jan 2033, 25% by 2029 (mid-2026). [web, secondary]
- Robot prices: IFR, average robot cost -80% 1995-2017 (~7%/yr); 6-axis arm ASP -3-5%/yr over 2022-25; ~$46k (2010) to ~$27k (2017). [web, ARK/IFR secondary]
- Grace et al 2024: HLMI 10% by 2027, 50% by 2047; FAOL 10% by 2037, 50% by 2116. [lit; the "~45% by 2100" FAOL point used in reweighting is my interpolation]

Structural changes: saturating capability with per-draw ceiling; uncertain trend-break mean; no-transfer mass; acceleration branch; separate physical capability and cost; CES/Baumol spending closure with a recycling share; frictions scaled to gains, oversight and liability costs, lognormal firm heterogeneity; explicit PD test with demand externality and retention pacts (legal x repeated-game sustainable); government adoption by budget pressure with veto; regulation with instrument types and a 0-0.3 strength prior; process-automation starting shares; end-of-year records. The headline pools the judgmental prior with draws reweighted to three external capability anchors (HLMI, FAOL, Metaculus), all weighted for 2026 exposure consistency.

Findings on mechanism (see results JSON): once realized depth reaches 0.5 in half of employment, adoption usually follows (P(adoption | depth) ~0.8), and 15% net displacement is then almost arithmetic (0.8 x 0.5 x 0.5 = 20% gross, with Baumol reabsorption small because labor-cost savings are ~10% of sector cost). The frictions, benevolence, pacts and regulation terms now move P by a few points up to about 15 points. The biggest drivers are still capability transfer, the ceiling, physical automation, and a strong payroll-parity tax.
