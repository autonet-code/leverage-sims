# r8d: Acceleration, takeoff, decision speed, single-actor decisive lead (as of 2026-09-30)

## 2026 state of frontier AI
- METR 50% time horizon: Claude Mythos Preview (May 2026) >=16 h (suite saturates ~16 h; unreliable above). 80% horizon ~3 h.
- Doubling time: ~7 mo (2019-2025 full), ~4 mo (2024-2025), 131 days post-2023 under TH1.1. Evidence: good (measured), but software-task-specific.
- AI Futures Project Q2.5 2026: Automated Coder medians Nov 2027 (Kokotajlo), Jan 2029 (Brendan), Jan 2030 (Lifland); p90s 2030 / 2050 / 2070. AC->ASI p50 1 yr (DK), 2 yr (EL). Reality running ~70-90% of AI 2027 pace. Current coding uplift ~2x (DK median; note METR 2025 RCT found a 19% slowdown for experienced devs, so uplift is contested).
- US-China frontier gap: ~7 months avg since 2023 (range 4-14; Epoch ECI). Narrowing on some benchmarks (Stanford AI Index 2026).
- Compute concentration: 5 hyperscalers ~71% of global AI compute (Q4 2025, up from 63% Q1 2024); Google ~25% alone.
- Military: Maven Smart System processed ~1,000 targets on day 1 of the 2026 Iran war; detection-to-strike compressed hours -> minutes. Ukraine/Russia racing to autonomy; "partially implemented" autonomy. Pentagon 2026 "AI-first" strategy.

## Explosive growth literature
- Roodman 2020: stochastic hyperbolic fit to 10,000 yrs of GWP implies finite-time explosion ~mid-century (median ~2047) if the pattern held; Roodman himself flags it as a fit, not a forecast; demographic transition broke the pattern after ~1960.
- Davidson 2021 (Open Phil): >=30% annual GWP growth this century is plausible (roughly 10-30%+, not the most likely outcome) conditional on AI substituting for labor in R&D.
- Epoch GATE (2025): automation raises growth 2-20x vs ~3%; ~30% growth, full automation "in decades"; authors: qualitative, not a forecast.
- Aghion-Jones-Jones 2017: singularity possible only if AI automates idea production fully; Baumol bottlenecks (tasks that stay non-automated) can cap growth.
- Forethought Industrial Explosion (Davidson & Hadshar 2025): fully automated physical economy could double ~yearly with current methods; later days/weeks. Robot tech efficiency doubling 1-4 years (slower than chips/algorithms).
- Davidson & Houlden 2025 (software intelligence explosion): roughly even odds that AI R&D automation yields accelerating software-only progress (from memory; verify).

## Power concentration
- Forethought "AI-Enabled Coups" (Davidson, Finnveden, Hadshar, Apr 2025): three risk factors (singular loyalties, secret loyalties, exclusive access). Removes need for human cooperation, the historical check. Can happen in democracies; a coup in the frontier country could extend to world control. No numeric probabilities.
- Forethought "Could one country outgrow the rest of the world?": needs >50% world GDP (US could reach it given AI lead), willingness to sacrifice short-term GDP, strong internal coordination, and a large deliberate effort to block tech diffusion. Verdict: US "likely could", but "unclear" whether it will try.
- Forethought/Aschenbrenner: at ~100x speed-up, a 6-month lead ~ 50-year military lead. This assumes fast takeoff; lead is only decisive if the leader acts on it before diffusion/espionage closes it.
- Christiano/Kokotajlo: soft takeoff can still yield DSA (Kokotajlo ~30%+ even at industrial-revolution-x10-100 speeds; one author's judgment).

## Verdict on user claim 5
Partly holds. Relative power/security is a top priority for states (realist IR, well supported) and for many powerful individuals, and AI already compresses tactical military decision cycles by 10-100x (well evidenced, 2026). Not supported: "the main game" (states also pursue prosperity, legitimacy; nuclear deterrence and alliances constrain), and "decision speed rises at the same exponential rate as AI" (strategic/political decisions remain bottlenecked by humans, law, and coalitions; no evidence of exponential compression there yet). The strongest legitimate version: AI removes the need for human cooperation in the chain of command, which is the mechanism v2 lacked.

## Implications for model
- v2 Ppg_med = 0.025 (unconditional-ish) is low given Forethought mechanisms; suggest P(narrow-group AI power grab in leading country by 2045 | AGI by 2035) ~0.10 (0.03-0.25).
- pg_s5_mult = 0.5 based on "public stays economically useful" assumes the conclusion; replace with a function of whether the grabbing actor has closed the industrial loop.
- Add explicit parameters: leader's lead (months), takeoff speed, diffusion-blocking effort, DSA conversion probability.
- Timewave Zero novelty chart: excluded, not evidence. Roodman's hyperbolic fit is the legitimate analog and points to ~2047 at most, with big caveats.

Sources: metr.org/time-horizons; metr.org/blog/2026-1-29-time-horizon-1-1; blog.aifutures.org/p/q25-2026-timelines-update-uplift; forethought.org/research/ai-enabled-coups-how-a-small-group-could-use-ai-to-seize-power; forethought.org/research/could-one-country-outgrow-the-rest-of-the-world; forethought.org/research/the-industrial-explosion; epoch.ai/blog/announcing-gate; epoch.ai/data-insights/us-vs-china-eci; epoch.ai/data-insights/hyperscalers-control-most-compute; militarytimes.com 2026-09-16 AI targeting; aljazeera.com 2026-09-14 Russia-Ukraine autonomy.

## Addendum (pass 2, 2026-09-30)
- Verified: Davidson & Houlden 2025 ("How quick and big would a software intelligence explosion be?"): ~60% that SIE compresses >3 yrs of progress into <1 yr; ~20% that it compresses >10 yrs into <1 yr. Returns r ~1.2 (range 0.4-3.6) output doublings per input doubling; r>1 means accelerating. Chip-tech loop alone ~65% enough to accelerate; software+chips jointly ~75%. Evidence: moderate (model + judgment, one group).
- Anthropic Economic Index (user suggestion; more relevant to S1/S2 than to power concentration): Claude.ai automation share 41% (Jan 2025) -> >50% (Aug 2025) -> 45% (Nov 2025); enterprise API traffic ~75% automated (directive). June 2026 "Cadences" report: >35% of surveyed users expect AI to handle most/nearly all of their tasks within 12 months; Claude Code sessions markedly more autonomous than chat. Evidence: good for usage, weak as a proxy for labor displacement (usage share != jobs removed). Implication: firm-side (API) deployment is already mostly automation-mode, which supports faster S1 than v2 historical-diffusion anchors, but does not measure closure of the physical loop.

## Suggested priors (central, 90% range)
- P(SIE compresses >=3 yrs into 1 yr | automated AI researcher): 0.55 (0.3-0.8)
- Automated coder/AI researcher median: 2029-2030 (p10 2027, p90 2040+)
- Frontier lead of #1 lab over #2 (months): 3 (1-9); US over China: 7 (3-14)
- Lead amplification factor during SIE (lead in years of progress per month of calendar lead): 1-10x
- P(some single actor (lab, state, or lab-state bloc) holds decisive economic-military lead >= 1 yr of AI-progress equivalent at some point | automated AI R&D by 2035): 0.35 (0.15-0.6)
- P(that lead converts to durable DSA, i.e. rivals cannot catch up or deter, | lead): 0.3 (0.1-0.5) (nuclear deterrence, espionage, diffusion, internal coalitions)
- Net P(single-actor DSA by 2045 | AGI by 2035): ~0.10 (0.03-0.3); unconditional by 2045: ~0.06 (0.015-0.2)
- P(narrow-group seizure within the leading actor | DSA): 0.3 (0.1-0.6) (Forethought coup mechanisms; judgment)
- Strategic decision-cycle compression by 2035: tactical 10-100x (observed), strategic/political 1-3x (little evidence)
