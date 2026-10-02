# R13a: World AI compute inventory, October 2026

Prepared 2026-10-01 for the dystopia simulation paper. Units: **H100e** = H100-equivalents (1 H100 SXM = 989 TFLOP/s dense FP16/BF16, about 1,979 TOP/s dense INT8/FP8). Conversions to FLOP/s: 1M H100e is about 1.0e21 FLOP/s FP16 or 2.0e21 OP/s INT8.

Evidence grades: **A** = primary data or filing, fetched today; **B** = reputable estimate (Epoch, SemiAnalysis, company statements) with stated method; **C** = my derivation from A/B inputs with explicit assumptions; **D** = rough recollection or low-quality claim, use only as an order of magnitude.

Method note: the web search budget for this session was exhausted, so figures come from direct fetches of primary datasets (Epoch AI CSVs downloaded today, live network APIs, mempool.space, Steam survey), from earlier project files (m7, which cites Pine Analytics, FalconX, Messari, Covenant-72B) and from recollection where flagged D.

---

## 0. Headline numbers

| Quantity | Value (central, range) | Date | Grade | Source |
|---|---|---|---|---|
| Cumulative AI accelerators sold, 2022 to Q3 2026 | 32.6M H100e (26-40M, 90% CI); 25.5M chips | data through 2026-09-30 (Q3 partial) | B | Epoch AI, Data on AI chip sales (CSV, estimates generated 2026-08-27) |
| Of which Nvidia / Google TPU / AMD / Amazon / Huawei / Cambricon | 22.2M / 7.0M / 1.7M / 1.0M / 0.71M / 0.03M | same | B | same (Amazon, Huawei, Cambricon series stop at end-2025, so 2026 is undercounted by perhaps 1-2M H100e) |
| Sold in 2025 / in 2026 Q1-Q3 | 13.6M / 12.3M H100e | same | B | same |
| Chip TDP of all accelerators sold | 19.2 GW (chip only; facility power roughly 1.5-2x, so 30-38 GW) | same | B/C | same |
| Operational datacenter AI compute today (assuming 1-2 quarter install lag, small retirements) | **~29M H100e (25-33M)** = ~2.9e22 FLOP/s FP16, ~5.8e22 OP/s INT8 dense | 2026-10 | C | derived from Epoch |
| World deployed compute end-2025 | 12-16M H100e deployed, ~20M sold | end-2025 | B | Epoch, "Frontier labs don't use most AI compute" |
| Growth of installed compute | ~3.3x/yr since 2022 (2.7-4.1x), doubling ~7 months | 2022-2026 | B | Epoch, AI chip production insight |
| Theoretical consumer/edge peak (gaming GPUs + phones + PC NPUs + Macs) | ~40M H100e-equivalent peak OPs (15-80M), mostly INT8 | 2026 | C/D | Section 3 |
| Effective consumer/edge compute usable by a network | ~0.3-2M H100e for inference; ~0 for frontier training | 2026 | C | Section 3 |
| Active decentralized AI compute networks (all, real usage) | ~10-50k H100e (0.03-0.2% of datacenter stock) | 2026-10 | C | Section 5 |
| Bitcoin network power | ~20 GW (990 EH/s at ~20 J/TH) | 2026-10-01 | A/C | mempool.space hashrate; efficiency assumption |

---

## 1. Central compute: hyperscalers, frontier labs, neoclouds, China, governments

### 1.1 Ownership in Epoch's frontier data center database (tracked sites only)

Epoch's Frontier Data Centers dataset (downloaded 2026-10-01) sums to **14.2M H100e and 13.6 GW** across ~400 tracked sites. It covers roughly half the world stock; the rest sits in many smaller sites. Grade B, with Epoch's own confidence tags.

| Owner (tag) | Current H100e in tracked sites | Notes |
|---|---|---|
| Google | 3.67M | TPU-heavy; users tagged mostly "Google DeepMind (speculative)" |
| Meta | 2.55M | Prometheus (0.60M, 496 MW), Rosemount, Jeffersonville, Temple, Montgomery |
| Microsoft | 1.69M | Fairwater Atlanta (0.77M), Fairwater Wisconsin (0.45M), Goodyear; users OpenAI (likely) |
| SpaceXAI (xAI, as labelled by Epoch) | 1.40M | Colossus 2 (1.11M, 946 MW, B200/B300, users Anthropic, Cursor, SpaceXAI), Colossus 1 (0.28M, user Anthropic) |
| Amazon | 1.35M | New Carlisle (0.69M, Trainium2, Anthropic), Madison |
| CoreWeave | 0.76M | Denton TX (0.25M, OpenAI likely) etc. |
| Oracle | 0.59M | Stargate Abilene (0.51M, OpenAI confident) |
| Huawei | 0.17M | China |
| VNET (China) | 0.12M | user ByteDance (speculative) |
| Nebius | 0.11M | |
| Core42/G42 (UAE) | 0.07M | |
| Unattributed Malaysia (DayOne Kempas 0.48M, Nusajaya 0.28M) | 0.76M | owner not tagged; press has linked DayOne Johor to ByteDance (D) |
| By country | US 12.7M (90%), Malaysia 0.76M, China 0.32M, UK 0.12M | China is badly undercovered here |

### 1.2 Frontier labs as users (Epoch, end-2025)

Source: Epoch Gradient Update "Frontier labs don't use most AI compute (yet)". Grade B.

| Lab | H100e (end-2025) | Basis |
|---|---|---|
| OpenAI | ~1.7M | 1.9 GW disclosed capacity; ~3x/yr growth; target "low double-digit GW" by 2027 |
| Anthropic | 1M+ | ~1.4 GW; projected 5-6 GW by end-2026; quarterly compute spend ~$3B to $6B |
| xAI | 0.6-0.7M | Colossus 1+2 (by 2026 Epoch tags Anthropic as a Colossus user) |
| Google total | ~4M (~25% of world) | split across Cloud, DeepMind, internal products |
| Meta total | ~2.3M (~10%+ of world) | |
| OpenAI+Anthropic+xAI | under 4M = 20-30% of world (up to ~35% incl. hyperscaler inference for them) | |
| Top 5 developers incl. GDM and Meta | "probably still under half" | |

Key structural point: frontier labs are mostly **tenants**. Ownership of the physical compute sits with ~5 hyperscalers plus a handful of neoclouds; labs control the workloads.

### 1.3 Estimated ownership shares of ~29M H100e operational (Oct 2026)

Grade C (synthesis of Epoch chip sales, Epoch DC database, and the fact that TPUs and Trainium are captive to Google and Amazon).

| Category | Share | H100e | Notes |
|---|---|---|---|
| Big hyperscalers (Google, Microsoft, Amazon, Meta, Oracle) | 58-65% | 17-19M | Google alone ~25% (all TPUs plus Nvidia fleet) |
| xAI/SpaceXAI (owned) | ~5% | ~1.5M | |
| Neoclouds (CoreWeave, Nebius, Lambda, Crusoe, Nscale, Fluidstack, Together, Firmus, etc.) | 8-12% | 2.5-3.5M | CoreWeave alone ~1M; 250k GPUs in 2025 per Wikipedia, ~$100B backlog Q1 2026 |
| China (all owners) | 5-9% | 1.5-2.5M | see 1.4 |
| Governments, national labs, sovereign AI | 2-4% | 0.6-1.2M | see 1.5 |
| Enterprise and university on-prem | 6-12% | 2-3.5M | see section 2 |
| Other (Gulf, Malaysia hosts, smaller clouds, Tesla, etc.) | 3-6% | 1-2M | Tesla Cortex, Saudi Humain, UAE Stargate |

### 1.4 China

| Item | Value | Date | Grade | Source |
|---|---|---|---|---|
| China-market chips sold 2022-2025 (H20 1.49M units, H800, A800, Ascend 910B/C 1.25M units, Cambricon 590) | 1.12M H100e | to end-2025 | B | Epoch chip sales CSV |
| Huawei Ascend | 0.71M H100e (910B 0.21M, 910C 0.50M) | 2024-2025 | B | same; 2026 output not yet in data |
| Smuggled via Malaysia | ~150k H100e ($3.75B of servers) | Apr 2024-Jun 2025 | B | Epoch, Malaysia-China chip smuggling insight |
| Alibaba T-Head Zhenwu accelerators | 560k units shipped to 400+ external customers; $53B 3-year AI and cloud capex; target 20 GW by 2032 | Sep 2026 | B | Jon Peddie Research, "Alibaba builds its own AI stack" (2026-09) |
| Pre-control A100 imports and offshore leasing (ByteDance in Malaysia etc.) | 0.3-1M H100e | 2022-2026 | D | |
| **China total accessible** | **~1.5-2.5M H100e (5-9% of world)**; per-chip quality lower, interconnect and HBM constrained | 2026 | C | |

### 1.5 Governments, national labs, sovereign AI

| Item | Value | Grade | Source |
|---|---|---|---|
| Public-sector share of Epoch's cluster database (482 existing clusters, 1.57M H100e, mostly pre-2026) | 0.17M public + 0.05M public/private = ~14% of tracked clusters, but far less of total stock | B | Epoch GPU clusters CSV |
| El Capitan (LLNL) | 44k H100e, 35 MW | B | same |
| JUPITER (EuroHPC, Julich) | 23.5k H100e | B | same |
| Alps (CSCS) | 10.8k H100e | B | same |
| Isambard-AI (UK), ABCI 3.0 (Japan), India AI Mission (~35-40k subsidized GPUs), Saudi Humain, UAE Stargate (first 200 MW in 2026), DOE-Nvidia/Oracle Solstice (100k Blackwell planned) | each 5k-100k H100e; much of the sovereign buildout is still pipeline | D | announcements, recollection |
| **Total government/national lab/sovereign** | **~0.6-1.2M H100e (2-4%)** | C | |

---

## 2. Enterprises and universities (on-prem)

| Item | Value | Grade | Notes |
|---|---|---|---|
| Epoch "Other (ex-Big 4 hyperscalers)" bucket of Nvidia sales | includes neoclouds, sovereigns, enterprises, Chinese buyers; roughly 35-45% of Nvidia volume | B/C | Epoch chip sales organizations table |
| Enterprise on-prem (banks, pharma, auto, telcos, Tesla, quant funds, via Dell/HPE/Supermicro/Lenovo) | ~2-3M H100e (7-10%) | C/D | OEM AI server revenue runs tens of $B/yr, but a large part goes to neoclouds and xAI |
| Universities and academic HPC | ~0.1-0.3M H100e (under 1%) | D | Largest single university clusters are typically 1-5k GPUs; national academic resources (NAIRR pilot, EuroHPC, Isambard) counted under governments |
| Utilization | enterprise GPU clusters often run at 30-60% average utilization | D | widely reported in industry surveys; this idle share is the most plausible "donatable" datacenter-class pool |

---

## 3. Consumer and small-business hardware

### 3.1 Inventory (theoretical peak)

| Device class | Installed base (est.) | Per-device peak | Aggregate peak | Grade |
|---|---|---|---|---|
| Discrete gaming GPUs with tensor cores (RTX 20-50 series, RX 7000/9000) | ~250M in use (150-350M) | median ~60-80 TFLOP/s FP16 tensor dense (RTX 3060 ~51, 4060 ~60, 4090 ~330, 5090 ~420 with FP16 accumulate) | **~15M H100e** (8-30M) FP16 | C/D |
| Smartphone NPUs | ~4.5B smartphones; ~2-3B with usable NPUs | ~5-50 TOPS INT8 (flagships 35-60) | **~20M H100e** INT8 (10-40M) | C/D |
| Copilot+/AI PC NPUs (40+ TOPS) | ~100-150M | ~45-50 TOPS INT8 | ~2-3M H100e INT8 | D |
| Apple silicon Macs (M1-M5) | ~120M | GPU ~3-20 TFLOP/s FP16, NPU ~11-38 TOPS, unified memory 8-128 GB | ~0.6-1M H100e | D |
| **Total consumer/edge peak** | | | **~40M H100e-equivalent (15-80M)**, comparable to the whole datacenter fleet on paper | C |

Steam Hardware Survey (August 2026, A): top GPUs are RTX 3060 (3.92%), RTX 4060 Laptop (3.84%), RTX 5070 (3.77%), RTX 4060 (3.60%), RTX 3050 (3.21%). VRAM: 8 GB 25.7%, 12 GB 13.0%, 16 GB 26.9%. System RAM: 16 GB 41.2%, 32 GB 37.5%. So the typical gaming GPU is a mid-range card with 8-16 GB VRAM. JPR (2026-09-15): memory capacity, not FLOP/s, is the binding difference between consumer and pro cards (RTX 5090: 32 GB, 1.79 TB/s; RTX Pro 6000: 96 GB).

### 3.2 Practical derating

| Constraint | Consumer reality | Datacenter reference | Effect |
|---|---|---|---|
| Memory per device | 8-16 GB VRAM typical (32 GB top end); phones 8-16 GB shared | 80-288 GB HBM per GPU, 13+ TB per NVL72 rack | Single card runs a ~7-14B model at 4-bit, ~30B on 24-32 GB cards. Frontier models (hundreds of B to trillions of params) need pipelining across dozens of homes |
| Memory bandwidth | 0.3-1.8 TB/s (GPUs); 50-100 GB/s (phones) | 3.35-8 TB/s per GPU | Decode throughput is bandwidth-bound; phones are ~50x slower per device |
| Interconnect | 10-1,000 Mb/s residential, high latency | NVLink 1.8 TB/s per GPU, InfiniBand 400-800 Gb/s | 4-5 orders of magnitude gap; tensor/pipeline parallel over the internet is impractical; only DiLoCo-style data parallel with large local nodes or embarrassingly parallel inference works |
| Uptime and availability | gaming PCs idle most of the day but owner-controlled; phones thermally and battery limited (sustained NPU load maybe 10-20% of peak) | 95%+ | Effective hours perhaps 30-50% for PCs, near 0-10% for phones |
| Precision/software | INT8/FP16 inference fine; FP8/FP4 training support limited on older cards; heterogeneity | homogeneous | verification and scheduling overhead, 10-50% |
| Power cost | paid by owner at retail rates | wholesale | needs payment above $0.10-0.40/kWh |

**Workload feasibility.** Inference of distilled/open models up to ~30B: feasible on gaming GPUs and Macs, the main real use. RL rollouts (generation for post-training): feasible, proven by INTELLECT-2. Fine-tuning small models (LoRA up to ~14B): feasible. Pretraining frontier models: infeasible on consumer devices; even decentralized pretraining today (Covenant-72B) uses 8x B200 datacenter nodes, not home GPUs. Phones: useful only for on-device personal inference, not as network contributors.

**Effective consumer contribution (C):** if 10-20% of gaming GPUs joined, at 30-50% availability and 50-70% efficiency, that is ~0.3-1.5M H100e of inference-only capacity. Phones add almost nothing to a shared network.

---

## 4. Crypto mining

| Item | Value | Date | Grade | Source |
|---|---|---|---|---|
| Bitcoin network hashrate | 990 EH/s (peak ~1,133 EH/s in Oct 2025; 921 EH/s Sep 2026 monthly avg) | 2026-10-01 | A | mempool.space API |
| Bitcoin network power | ~20 GW at ~20 J/TH fleet average (15-25 GW) | 2026 | C | derived |
| Convertibility of BTC ASICs to AI | **zero** (SHA-256 fixed function) | | A | |
| Convertible asset | sites, grid interconnects, substations, cooling, operating teams; conversion to AI hosting takes ~12-24 months and needs new GPUs and usually liquid cooling | | B | |
| Ethereum GPU mining at peak | ~1.0-1.1 PH/s Ethash, i.e. ~10-20M GPU-equivalents (at 50-100 MH/s each), ~$15-20B/yr miner revenue at peak 2021-22 | May 2022 | D | widely reported; recollection |
| After the Merge (2022-09-15) | most mining GPUs were sold into the gaming market or idled; ETC and others absorbed a minority briefly; a few operators became AI clouds | | D | |
| CoreWeave | founded 2017 as Atlantic Crypto, an Ethereum GPU miner; renamed 2019; now ~$5.1B 2025 revenue, ~$100B backlog | Q1 2026 | B | Wikipedia (CoreWeave) |
| Core Scientific | $10B of hosting contracts in 2025 (mostly CoreWeave); CoreWeave's $9B acquisition rejected by shareholders Oct 2025; exited bitcoin mining Mar 2026, 10 data centers | Mar 2026 | B | Wikipedia (Core Scientific) |
| IREN | 5 GW secured power; 810 MW operational (BC sites plus Childress); Sweetwater 2 GW under construction; Oklahoma 1.6 GW in development; large Microsoft GPU cloud contract (2025) | 2026-10 | A/B | iren.com |
| Others (Hut 8, Cipher, TeraWulf, Galaxy Helios, Bitfarms, CleanSpark) | multi-hundred-MW AI hosting leases each, often backstopped by Google or with CoreWeave/Fluidstack/AWS tenants | 2025-26 | D | recollection |
| **Total miner power pivoting to AI** | ~3-6 GW contracted, ~10-15 GW in pipeline | 2026 | D | |

Implication: miners are the clearest example of incentive-driven reallocation, but they are moving **into** centralized hyperscaler and lab supply chains (long-term leases to CoreWeave, Microsoft, Google, AWS), not into decentralized networks. The hashrate dip since October 2025 partly reflects this power reallocation.

---

## 5. Decentralized compute networks

### 5.1 Network scale and utilization

| Network | Claimed capacity | Actual active usage | Date | Grade | Source |
|---|---|---|---|---|---|
| io.net | 1.06M "total" GPUs, 327k "verified" | **1,446 active GPUs** | 2026-10-01 | A | io.net explorer API (api.io.solutions network/info) |
| Akash | 421-442 GPUs (232 A100, 68 H100, 40 H200, 16 B300, misc.), 62 providers | 316-354 allocated (~80%); ~$7.8k/day spend (~$2.9M/yr) | 2026-10-01 | A | Akash console API |
| Aethir | 440k "GPU containers", 94 countries | revenue $128M (2025), ~$166M annualized Q3; largely enterprise H100 resale via partners | 2026 | B/D | BlockEden (2026-03), company claims |
| Bittensor (Chutes, Targon, Templar/Covenant etc.) | ~128 subnets | external revenue ~$3-45M/yr; emissions ~20x revenue | 2026 | B/C | m7: Pine Analytics, FalconX |
| Render | thousands of node GPUs, mostly rendering | usage +87% in 2025 | 2025 | D | BlockEden |
| Vast.ai, Salad, others (non-token or partly token marketplaces) | ~10-60k listed consumer and datacenter GPUs | unknown utilization | | D | |
| **All decentralized AI networks, real active compute** | | **~10-50k H100e (0.03-0.2% of world datacenter AI compute)**; total DePIN compute revenue well under 0.1% of AI infrastructure spend | 2026 | C | |

The claimed-versus-active gap (io.net: 1.06M registered vs 1,446 active) is the norm, not an exception: token rewards pull registrations, but demand-side revenue determines what runs.

### 5.2 Decentralized training results

| Run | Date | Scale | Hardware | Compute (6ND) | Ratio to 2026 frontier (~1e26-1e27) | Grade |
|---|---|---|---|---|---|---|
| INTELLECT-1 (Prime Intellect) | Nov 2024 | 10B params, 1T tokens, 42 days | up to 112 H100 across 5 countries, 4-14 nodes; 83-96% compute utilization; 400x bandwidth reduction (DiLoCo) | ~6e22 | ~1/2,000-1/20,000 | A (blog) |
| INTELLECT-2 | May 2025 | 32B, decentralized RL (permissionless rollout workers) | heterogeneous | small (post-training) | n/a | A (arXiv 2505.07291) |
| INTELLECT-3 | Nov 2025 | 106B MoE on GLM-4.5-Air base, SFT plus RL | **centralized**: 512 H200 for 2 months | | | A (blog) |
| Nous Psyche (Consilience 40B) | 2025 | 40B pretraining over the internet | distributed datacenter nodes | ~1e24 order | ~1/100-1/1,000 | D |
| Covenant-72B (Templar, Bittensor) | Mar 2026 | 72B, ~1.1T tokens, SparseLoCo, 146x compression, 94.5% utilization, 500/110 Mb/s links | ~20 peers per round (avg 16.9), 70+ unique peers, each at least 8x B200 (~160+ B200, ~400 H100e) | ~4.8e23 | **~1/200-1/2,000** (central ~1/1,000) | A (arXiv 2603.08163) |

Takeaways: (1) the algorithms (DiLoCo, SparseLoCo, compressed pseudo-gradients) now work at 70B scale over commodity internet with >90% utilization; (2) every successful run uses **datacenter-class 8-GPU nodes**, not consumer devices; (3) the best permissionless run is about 3 orders of magnitude below frontier, roughly where centralized frontier was in 2020-2022.

Theoretical ceiling: if a network assembled 1M H100e of datacenter-class nodes at 30% MFU for 100 days, it could do ~2.6e27 FLOP, i.e. frontier scale. The binding constraint is access to datacenter-class hardware, not the protocol.

---

## 6. Incentive and mobilization analogs

### 6.1 Token incentives

| Case | Mobilization speed | Collapse / quality | Grade | Source |
|---|---|---|---|---|
| Bitcoin hashrate | 0.31 EH/s (Jan 2015) to 15 (Jan 2018) to 153 (Jan 2021) to 703 (Jan 2025) to peak 1,133 (Oct 2025); ~2-3x/yr in growth phases | China ban: 172 EH/s (May 2021) to 91 (Jul 2021), -47% in 2 months; recovered to 179 by Jan 2022 (~7 months) via relocation to US/Kazakhstan; 2025-26 dip ~15-20% as miners shift power to AI | A | mempool.space |
| Ethereum GPU mining | ~150 TH/s (early 2020) to ~1 PH/s (2022), ~6x in ~2 years, pulling in ~10-20M GPUs including a visible share of retail gaming cards (2021 GPU shortage) | ended overnight at the Merge (Sep 2022); hardware dispersed to resale | D | recollection |
| Filecoin | mainnet Oct 2020; crossed baseline target Apr 2021; raw capacity peaked ~17 EiB (2022) | fell below baseline by Feb 2023; capacity later declined several-fold; most early capacity was empty "committed capacity" with few paying deals | B (Wikipedia for baseline dates) / D (EiB figures) | Wikipedia |
| Helium | ~20-30k hotspots (early 2021) to ~900k-1M (mid 2022), ~30-45x in 18 months | data revenue was trivial (on the order of $6.5k per month in 2022 vs tens of millions in token rewards); online hotspot count later fell by more than half | D | recollection |
| Bittensor | ~128 subnets, $B-scale market cap | emissions ~20x external revenue; a leading subnet team (Covenant) later left | B/C | m7 sources |
| io.net | 1M+ registered GPUs in about 2 years | ~1,400 active | A | live API |

Pattern: when token rewards exceed operating cost, **registrations and cheap hardware** arrive within months (10-50x in 1-2 years). Useful, demand-backed capacity grows far more slowly and collapses when emissions fall. Hardware that can be repurposed (GPUs) is pulled more easily than special-purpose hardware, but the hardware attracted tends to be the cheapest that qualifies for rewards.

### 6.2 Mobilization under existential threat

| Case | Speed | Grade | Source |
|---|---|---|---|
| US aircraft production | <3,000 planes in 1939 to ~300,000 total by 1945; roughly 6k (1939), 13k (1940), 26k (1941), 48k (1942), 86k (1943), 96k (1944): ~2x/yr for 4 years | B (totals) / D (annual series) | Wikipedia, Military production during WWII |
| US tanks and SPGs | 108,410 in the war | B | same |
| US auto industry | civilian car production halted Feb 1942; conversion of plants to military output within ~6-12 months | D | |
| Willow Run (Ford B-24) | construction 1940-41; first B-24 Sep 1942; one bomber every 63 minutes by 1944 (428 in April 1944); 6,972 built; ~2.5-3 years from groundbreaking to peak rate | A | Wikipedia, Willow Run |
| USSR 1941 evacuation | ~2,500 factories and 17M people moved east, mostly within ~6 months; many back in production within ~1 year | B | Wikipedia, Military production during WWII |
| War production share | ~40% of US GDP at peak (1943-44) | D | |

Implication for AI compute: even total war roughly doubled output of a strategic sector per year, with new greenfield plants taking 2-3 years to reach peak. Today, leading-edge logic, CoWoS packaging and HBM have 2-3 year lead times, and AI compute is *already* growing ~3x/yr. So mobilization can redirect existing chips quickly (months, as with Bitcoin relocation) but cannot quickly add chips outside the TSMC/SK Hynix/Samsung/Nvidia chain. Historically, mobilization was also **state-directed and centralizing**, not decentralized.

---

## 7. Summary

### 7.1 Shares of world AI compute (October 2026)

| Category | Datacenter-equivalent effective compute | Share of effective total | Theoretical peak |
|---|---|---|---|
| Central: hyperscalers, labs, neoclouds, China, governments | ~26M H100e | ~85-90% | same |
| Enterprise and university on-prem | ~2-3.5M H100e | ~7-11% | same |
| Consumer/edge (usable for networked inference) | ~0.3-2M H100e | ~1-5% | ~40M H100e peak, mostly unusable |
| Decentralized networks today (actual) | ~10-50k H100e | ~0.03-0.2% | registrations ~1M+ GPUs claimed |

Concentration: about 5 hyperscalers own ~60%, the top 10 owners ~80%. About 90% of tracked frontier data center capacity is in the US.

### 7.2 Plausible decentralized share under strong economic and ideological incentives

Scenario reasoning (grade C):

| Pool | Plausible joining fraction | H100e | Usable for |
|---|---|---|---|
| Gaming GPUs (Ethereum-era precedent: millions of retail cards joined within ~2 years when payback was under a year) | 10-20% | 0.3-1.5M effective | inference, RL rollouts, small fine-tunes |
| Macs and AI PCs | 5-10% | 0.05-0.2M | small-model inference |
| Enterprise/university idle GPUs | 5-15% of on-prem | 0.1-0.5M | inference, DiLoCo training nodes |
| Neoclouds and miner-hosted capacity rented by a network (if the network can pay market rates) | 1-5% of central | 0.3-1.5M | any workload incl. DiLoCo pretraining |
| Hyperscalers / frontier labs | ~0 unless forced or broken up | ~0 | |
| Phones | ~0 for shared work | ~0 | personal on-device inference only |
| **Total** | | **~1-4M H100e, i.e. ~3-10% of world effective AI compute within ~1-2 years**; 1-3% is the more realistic central case | |

Frontier-scale decentralized training would require ~0.3-1M H100e of **datacenter-class nodes** coordinated for months. That is plausible only if neoclouds, miners-turned-hosts, or sovereigns join; consumer hardware cannot close the gap.

### 7.3 Key constraints

1. **Chip supply is centralized.** New compute comes from TSMC/Nvidia/Google/AMD/HBM makers on 2-3 year lead times; export controls and allocation deals decide who gets it. A decentralized network can only bid for it, and governments can cut it off.
2. **Memory and interconnect, not FLOP/s.** Consumer devices match datacenters in peak OPs on paper but have 10-30x less memory per device and 4-5 orders of magnitude less interconnect bandwidth.
3. **Demand-side revenue.** Every token network to date has had emissions far above real revenue (Bittensor ~20x, Helium far more); capacity collapses when emissions fall.
4. **Verification and trust.** Proving work was done correctly costs 10-50% overhead and invites gaming of rewards.
5. **Power and sites.** About 20 GW of Bitcoin mining power exists, comparable to the ~19 GW chip TDP of all AI accelerators ever sold, but it is being contracted to centralized buyers, and hosting new GPUs needs capital and chips.
6. **Speed asymmetry.** Central compute grows ~3x/yr; even WWII-style mobilization manages ~2x/yr from new plants. A decentralized network starting at ~0.1% share needs sustained >10x/yr growth to reach ~10% within two years.

---

## Sources

- Epoch AI, Data on AI chip sales (CSV and ZIP, retrieved 2026-10-01; estimates generated 2026-08-27): https://epoch.ai/data/ai-chip-sales
- Epoch AI, Frontier Data Centers dataset (retrieved 2026-10-01): https://epoch.ai/data/data-centers
- Epoch AI, GPU clusters dataset: https://epoch.ai/data/gpu-clusters
- Epoch AI, Frontier labs don't use most AI compute (yet): https://epoch.ai/gradient-updates/frontier-labs-dont-use-most-ai-compute
- Epoch AI, AI chip production insight: https://epoch.ai/data-insights/ai-chip-production
- Epoch AI, Is a compute crunch coming?: https://epoch.ai/gradient-updates/is-a-compute-crunch-coming
- Epoch AI, Malaysia-China chip smuggling: https://epoch.ai/data-insights/malaysia-china-chip-smuggling
- Epoch AI, global computing capacity (2024 owner estimates): https://epoch.ai/data-insights/computing-capacity
- Jon Peddie Research, Gaming GPUs find new AI workloads (2026-09-15): https://www.jonpeddie.com/news/gaming-gpus-find-new-ai-workloads/
- Jon Peddie Research, Alibaba builds its own AI stack (2026-09): https://www.jonpeddie.com/news/alibaba-builds-its-own-ai-stack/
- Steam Hardware and Software Survey, August 2026: https://store.steampowered.com/hwsurvey/
- mempool.space hashrate API (retrieved 2026-10-01): https://mempool.space/api/v1/mining/hashrate/all
- io.net explorer API (retrieved 2026-10-01): https://api.io.solutions/v1/io-explorer/network/info
- Akash console API (retrieved 2026-10-01): https://console-api.akash.network/v1/dashboard-data and /v1/gpu
- BlockEden, DePIN compute revenue (2026-03-12): https://blockeden.xyz/blog/2026/03/12/depin-compute-revenue-pivot-akash-ionet-aethir/
- Covenant-72B: https://arxiv.org/abs/2603.08163
- INTELLECT-1: https://www.primeintellect.ai/blog/intellect-1-release
- INTELLECT-2: https://arxiv.org/abs/2505.07291
- INTELLECT-3: https://www.primeintellect.ai/blog/intellect-3
- IREN: https://iren.com/
- Wikipedia: CoreWeave, Core Scientific, Nebius Group, Filecoin, Willow Run, Military production during World War II
- Project file m7_decentralized_alternative.md (Pine Analytics, FalconX, Messari citations for Bittensor and DePIN revenue)
