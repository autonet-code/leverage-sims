# r8e: Anthropic Economic Index and 2025-2026 adoption measures (as of 2026-09-30)

## AEI releases (HF: Anthropic/EconomicIndex)
2025-02-10 (v1, Dec24-Jan25), 2025-03-27 (3.7 Sonnet), 2025-09-15 (Aug 2025, geo + 1P API), 2026-01-15 (Nov 13-20 2025, "economic primitives"), 2026-03-24 (Feb 5-12 2026, "learning curves"), 2026-06-26 (Apr 10-Jun 10 2026, "cadences" + AEI Survey n~9,700), plus "Labor market impacts" (Mar 2026). Sep 2026: Anthropic Institute econ-scenarios explorer (WP 2026-02).

## Automation (directive + feedback loop) vs augmentation
| Sample | Claude.ai automation | Claude.ai directive | 1P API automation |
|---|---|---|---|
| Dec24-Jan25 | ~43% (57% aug) | 27% | n/a |
| Aug 2025 | ~49% (first time > aug) | 39% | 77% (aug ~12%); 97% of API tasks automation-dominant |
| Nov 2025 | 45% (aug 52%) | 32% | ~75% (directive ~64%) |
| Feb 2026 | aug up slightly | - | "decreased sharply" (no number published) |
Trend: consumer automation share oscillates 43-49%, no monotone rise. Enterprise API is ~3/4 automation. Coding migrates from chat to API/Claude Code (more autonomous: +0.37 on 1-5 autonomy scale).

## Occupations / coverage
- Computer & Math: 40% (Mar25 peak) -> 36% (Aug25) -> 34% (Nov25) -> 35% (Feb26) of Claude.ai; API 44% -> 46%; Office/Admin API 10% -> 13%.
- Occupations with AI use on >=25% of tasks: 36% (Feb25) -> 49% (Nov25).
- Top-10 task concentration: Claude.ai 24% -> 19% (Nov25->Feb26), broadening; API 28% -> 33%, deepening.
- Labor-market-impacts: Computer & Math 94% theoretically feasible vs 33% observed; programmers 75% coverage, data entry 67%; ~30% of workers zero coverage; no unemployment rise for exposed workers; 22-25 job-finding in exposed occs -14% (marginal significance); +10pp coverage -> -0.6pp BLS projected growth to 2034.

## Primitives (Nov 2025)
Success: Claude.ai 67%, API 49%; API <1h tasks ~60%, 5h+ ~45%. 50% horizon: API 3.5h, Claude.ai ~19h (multi-turn). Human-alone 3.1h vs ~15 min with AI (9-12x on covered tasks). Implied labor productivity: 1.8pp/yr naive, 1.0-1.2pp success-adjusted, 0.7-0.9pp at sigma=0.5, 2.2-2.6 at sigma=1.5.
Enterprise price elasticity: -0.29 (capability/value-limited, not cost-limited).

## Survey (May-Jun 2026, heavy-user selected: 30% comp/math)
35%+ expect AI to do most/nearly all their tasks within 12 months; 10% rate own job loss likely; highest-automation users most optimistic.

## Other measures
- St. Louis Fed RPS: workers using genAI at work 28.2% (Q3-24) -> 39.2% (Q2-26); share of all work hours with genAI 4.1% -> 6.3% (~28%/yr growth, doubling ~2.7y); time saved 1.6% -> 2.2% of all hours (~20%/yr).
- Census BTOS: firms using AI ~18% Dec25, flat 17-20% through May26 (37% of 250+ employee firms); +3.9pp y/y to Dec25.
- Fed SBU: 78% of workers at AI-adopting firms, 54% at LLM-using firms (Nov25).
- Microsoft global: 16.3% (end-25) -> 17.8% (Q1-26) -> 18.8% (Q2-26) of working-age pop; Global North 28.8%.
- OpenAI/NBER w34255: non-work share 53% -> >70% (to Jun25); "Doing" ~40% of messages (from memory, verify).
- Anthropic scenarios 2030: labor share 59.4 / 56.1 / 45.2% (modest/substantial/extreme); GDP +1.6/+8.3/+32%.

## Calibration implications
- 2026 baseline: AI assists ~6% of US work hours and saves ~2% of hours; genuinely automated (human-out-of-loop) cognitive work is likely 1-3% of US hours. Enterprise automation is where substitution happens and is concentrated in coding, customer service, back office.
- Growth: intensity measures ~20-35%/yr; firm adoption 20-70%/yr but plateaued H1 2026. Naive exponential of hours-share (doubling ~2.7-3.5y) hits ~30-50% by 2035; logistic with lags gives 15-30%. v2's S1 <1% by 2035 looks too low if S1 is defined by an automation race among leading firms (API data already show firm-level automation-first deployment); but data show no labor displacement yet, which argues against pulling S2 into the 2020s.
- Evidence gaps: AEI is one vendor (Claude skews coders), Clio classifier noise, 1-week samples, API automation drop Feb26 unquantified.

## User claim 2 ("if automation is profitable it will be done")
Partly supported. Supported: weak price elasticity, enterprise API ~75% automation, fast diffusion vs past tech. Not supported as stated: timing. BTOS flat for 6 months, API success 49%, observed use is ~1/3 of feasible in comp/math, most usage augmentative, zero unemployment effect yet. Better: "profitable, reliable automation diffuses with 3-10y lags; competition compresses lags in tradable, digital sectors first".
