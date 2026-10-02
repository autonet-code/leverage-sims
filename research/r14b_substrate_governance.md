# r14b: Substrate capability amortization and decentralized governance speed (2026-10-01)

Scope: evidence for two lever-test channels of the black-box decentralized AI: (1) "beaten paths" (small local model + accumulated skill/tool library), (2) governance decision speed and innovation efficiency. Web search budget was exhausted; sources are direct fetches unless marked "memory" (verify before publishing).

## Bottom line
1. Amortization is real and large on covered, repeat tasks: reusable workflows/tools cut cost per task to about 10-30% of solving from scratch and lift small-model success 25-50% relative. A small model plus library can match a ~10x larger model on structured tasks. Narrow-domain distillation keeps ~90% of teacher scores.
2. AI usage and work are concentrated: the bottom 80% of task categories carry only 10.5-12.7% of Claude usage (Gini 0.84-0.86); ~31% of LLM queries are repeats; ~44% of US jobs are routine (memory). A plausible coverable ceiling is 50-85% of task volume. The novel residual (15-50%) still needs frontier-class capability.
3. Honesty caveat: amortization is not unique to decentralized networks. Centralized providers also cache, distil and reuse workflows. The relative advantage comes only from a shared, open library pooling more users' paths: central 1.3x (1.0-2.0), low evidence.
4. Under closure (frontier access cut), the follower's lag reverts toward the compute-implied lag: about 27 months per 10x compute gap (8-month algorithmic halving). Today's observed open lag (3.5 months; 6-12 months on a consumer GPU) depends on leaders publishing and on distillation.
5. DAO governance is faster than democratic legislatures (7-day minimum cycle vs months to years) but slower than a CEO or autocrat (hours to days). In practice DAOs are oligarchic (17/21 have Nakamoto coefficient <10, half <=3; turnout 5-20%). Liquid democracy (Pirate Party LiquidFeedback, 13,836 users) produced stable super-voters, not measurably better or faster outcomes, and the party collapsed.
6. Innovation: open/commons production has huge reuse value (OSS demand-side value $8.8T vs $4.15B to recreate, ~2000x; 96% of value from 5% of developers) and wins in infrastructure. But no evidence shows higher frontier R&D efficiency per unit of compute. The large historical speedups (5-10x: Warp Speed, Liberty ships, penicillin) came from centralized, well-resourced mission programs.
7. Efficiency bar: to out-innovate a centralized actor holding S of world compute with share s, the network needs efficiency of about S/s. For s = 1-10% and S = 30-60%, that is 3-60x (central ~10x). The evidence supports at most 1-3x. Out-innovating centrally at the frontier before closure is not supported. Niche wins (narrow defensive tools that central actors underinvest in) remain plausible but unquantified.

## Parameters
| # | Parameter | Central | Low | High | Evidence | Source |
|---|---|---|---|---|---|---|
| 1 | Distilled 7-32B model score retention vs teacher, narrow verifiable (math/code) | 0.90 | 0.80 | 0.97 | medium-high | DeepSeek-R1 paper/model card (Distill-Qwen-32B AIME 72.6 vs R1 79.8; MATH-500 94.3 vs 97.3; memory of table) |
| 2 | Same, broad knowledge/science (GPQA) | 0.85 | 0.65 | 0.92 | medium | R1 card: GPQA 62.1 vs 71.5 (32B), 49.1 (7B) |
| 3 | Lag of best consumer-GPU model behind frontier | 9 mo | 6 | 18 | medium-high (benchmark; real-world lag longer) | Epoch AI consumer-GPU gap: 6.3-12.4 mo |
| 4 | Open-weight lag behind closed frontier | 3.5 mo | 1.1 | 5.3 | medium-high | Epoch AI open vs closed (ECI) |
| 5 | Algorithmic compute-halving time | 8 mo | 5 | 14 | medium | Ho et al. / Epoch 2024 |
| 6 | Lag per 10x compute gap if frontier access is cut | 27 mo | 17 | 46 | low-medium (derived from #5, ignores data/talent) | derived |
| 7 | Relative success gain from workflow/skill reuse on covered task families | +35% | +10% | +60% | medium | AWM (Wang et al. 2024): +24.6% Mind2Web, +51.1% WebArena; Voyager 15.3x faster milestones |
| 8 | Cost per covered task vs from-scratch reasoning | 0.15 | 0.05 | 0.4 | medium-low | Buffer of Thoughts 12% of ToT cost; LATM (GPT-3.5 user of GPT-4 tools ~ GPT-4 accuracy) |
| 9 | Effective model-size multiplier from library on structured tasks | 5x | 2x | 10x | low-medium | BoT: Llama3-8B+BoT can surpass 70B; LATM |
| 10 | Share of AI task volume in top 20% of task categories | 0.88 | 0.85 | 0.90 | high (Claude only) | Anthropic Economic Index Sep 2025 |
| 11 | Repeat/near-duplicate query share | 0.31 | 0.20 | 0.45 | medium-low | MeanCache arXiv 2403.02694 |
| 12 | Routine-occupation share of US employment | 0.44 | 0.40 | 0.50 | medium (memory) | Jaimovich-Siu; St Louis Fed (Dvorkin 2016) |
| 13 | Coverable ceiling c_max (share of economic task volume servable by beaten paths) | 0.70 | 0.50 | 0.85 | low | synthesis of #10-12 |
| 14 | Coverage growth time constant once in wide use (c = c_max(1-e^(-t/tau))) | 2 yr | 1 | 4 | low (Zipf makes coverage ~log of library size) | modelling assumption |
| 15 | Relative amortization advantage of open shared library vs centralized provider caching | 1.3x | 1.0x | 2.0x | low | reasoning; centralized prompt caching/distillation exist |
| 16 | OSS reuse amplification (demand-side / supply-side value) | 2100x | 600x | 3200x | medium-high | Hoffmann, Nagle, Zhou 2024 (HBS 24-038) |
| 17 | DAO minimum proposal-to-execution time | 7 d | 3 | 14 | high | Compound governance docs (2d review + 3d vote + 2d timelock) |
| 18 | Decision-speed multiplier, DAO/liquid vs centralized AI-enabled actor | 0.5x | 0.2x | 1.0x | low-medium | #17 vs executive decisions; r8d |
| 19 | Decision-speed multiplier vs democratic legislature/rulemaking | 20x | 5x | 50x | low-medium | #17 vs months-years |
| 20 | DAO turnout (token holders) | 10% | 5% | 20% | medium | Feichtinger et al. 2023 (21 DAOs) |
| 21 | Innovation efficiency per unit compute, decentralized vs centralized frontier R&D | 1.0x | 0.5x | 3.0x | low | OSS/Wikipedia/open-weight record; Covenant 1000x compute gap (m7) |
| 22 | Efficiency bar to out-innovate (S/s) | 10x | 3x | 60x | derived | s = 1-10% (r13a), S = 30-60% |
| 23 | Centralized emergency mission-program speedup | 7x | 5x | 10x | medium (memory) | Warp Speed ~11 mo vs 5-10 yr; Liberty ships 230 -> ~40 d |

## Other facts
- LiquidFeedback (German Pirate Party, about 4 years): 13,836 users, 499,009 votes, 6,517 initiatives, 14,964 delegations. 38 users held >100 delegations; 1,156 members voted >100 times. Super-voters mostly voted with the majority, which had a stabilizing effect (Kling et al. 2015, arXiv 1503.07723).
- DAO pathologies: >10% "pointless" votes in most DAOs. Governance gas costs: ENS ~$7.7M, Uniswap ~$3.2M. Beanstalk 2022 flash-loan governance attack ($182M, memory) shows why timelocks exist: speed trades off against security.
- Linux kernel: most commits come from paid corporate developers (memory). Successful "open" production is usually hybrid with firms.

## Modelling suggestion (black box, effects only)
Effective network capability share on task volume = s_compute x [c x M_amort + (1-c) x f_novel], where M_amort is the network's amortization advantage relative to centralized providers (not the absolute 3-10x cost saving, which both sides get). Use M = 1.3 (1-2) (#15). f_novel = 1 with frontier/open-weight access, or decays by lag #6 under closure. Governance: decision-speed multiplier 0.5x (0.2-1.0) vs the centralized adversary; innovation efficiency 1.0x (0.5-3). The efficiency bar #22 sits above the evidence range, so report frontier out-innovation as unsupported.
