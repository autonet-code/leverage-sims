# r9b: Physical bottlenecks to a closed automated industrial loop (as of 2026-09-30)

Note: web search budget was exhausted this session; figures below come from fetched pages (Forethought, Wikipedia
pages for China solar/electricity/nuclear, JASM, Morowali), earlier note r8a, and well-documented public figures
marked (mem) = from memory of public data, moderate confidence, not re-fetched.

## 1. Can physical capacity grow exponentially? Evidence
Sector ramps under capital flood, human labor, 2015-2026 (all sustained 4-10 yr):
- China solar installs: 48.8 GW (2020) -> 53 -> 87 -> 217 -> 277 -> ~315 GW (2025): ~1.45x/yr, doubling ~1.9 yr. Cumulative 253 GW -> 1.2 TW (2020-25), doubling ~2.2 yr. [Wikipedia, Solar power in China]
- Li-ion battery output ~0.3 TWh (2020) -> ~1.5 TWh (2024) (mem): ~1.5x/yr.
- China NEV 1.4M (2020) -> ~13M (2024): ~1.75x/yr, slowing to ~1.35x/yr at 7-13M. [r8a / m8 P_half]
- Indonesia nickel ~0.35 Mt (2017, mem) -> 1.6 Mt (2022, ~half of world) -> ~2.2 Mt (2024, mem): doubling ~2-2.5 yr. Morowali: stone-laying Dec 2014, first smelter ops Apr 2015 (5 months). [Wikipedia, Morowali]
- Lithium mine output ~82 kt (2020, mem) -> ~240-290 kt (2024-25): doubling ~2.5 yr.
- TSMC CoWoS advanced packaging ~2x/yr 2023-25 (mem); hyperscaler/data-center capex ~1.5-1.7x/yr 2023-26 (mem).
- Humanoid output ~3-4x/yr from ~14k (2025) [r8a].
Aggregate: China electricity capacity 2,200 GW (2020) -> 2,920 (2023) -> ~3,900 (2025, mem): ~14%/yr, doubling ~5 yr.
Industrial robot stock ~9-11%/yr (doubling 6-8 yr). Global manufacturing output 2-4%/yr.
Conclusion: individual physical sectors DO follow exponentials at 35-75%/yr (doubling 1.2-2.5 yr) for 5-10 years when demand
and capital are there, but growth brakes as the sector becomes large relative to its inputs (labor, minerals, grid,
specialized tools). A closed loop grows at the pace of its SLOWEST complementary input (Leontief), not its fastest.
Today the slowest are: greenfield mines outside China's orbit, lithography tools (EUV), grid equipment (large
transformers, gas turbines, multi-year backlogs 2024-26, mem), and construction labor (flat productivity for decades).

## 2. Bottleneck by bottleneck
Mines: greenfield discovery-to-production ~16 yr global (S&P/IEA); construction phase alone 2-4 yr; brownfield 2-5 yr.
 Fast-tracked Chinese-financed cases: Morowali NPI 5 months to first output; Indonesian HPAL ~2 yr build (mem);
 Kamoa-Kakula copper ~2.5 yr build (mem); Zimbabwe lithium ~1-2 yr (mem). Most of the 16 yr is exploration + permitting
 + financing, which state priority removes. Boom supply doubling 2-2.5 yr (nickel, lithium) vs baseline 3-5%/yr growth.
 Autonomous haulage already in use at scale (thousands of trucks, Pilbara, China, mem). AI compresses exploration and
 planning; robots compress labor. Floor with full automation: ore bodies are depleted, grades fall, so ~1-2 yr doubling.
Fabs: TSMC Arizona fab 1 groundbreaking Jun 2021 -> HVM Q4 2024 (~3.5 yr); JASM Kumamoto founded Dec 2021, production
 Dec 2024 (~2.7 yr from groundbreaking Apr 2022, 24/7 build); Taiwan/China shells 1.5-2 yr. Tool lead 12-18 months; EUV
 ~40-50 units/yr, single supplier. Robot inference chips can use mature nodes (China OK), which grow more easily. Global
 wafer capacity ~6-7%/yr baseline (mem); leading actors under race 25-40%/yr.
Energy: China adds ~300-500 GW/yr of capacity, solar module manufacturing >1 TW/yr (mem, ~2x installs = spare). PV
 energy payback ~1 yr, so an automated solar loop could double in ~1-2 yr. Nuclear: China avg 6.3 yr first concrete to
 grid (2015-24), 39 under construction; not the fast path. Grid/transformers the main short-term chokepoint.
Construction: Giga Shanghai ~11 months groundbreaking to cars (2019); xAI Colossus 122 days (2024); Broad Group 57 floors
 in 19 days (prefab, 2015); typical greenfield plant 1.5-3 yr. On-site construction robotics is immature (layout,
 bricklaying, rebar tying niche). Prefab/modular cuts schedule 30-50% (mem).
Robots-building-robots: Fanuc Oshino unattended up to 30 days since ~2001; Xiaomi Changping ~81% automated;
 Chinese dark factories exist but inside human-dependent supply chains. Forethought: robot stock doubled in 6 yr last
 time; ~1 yr doubling once AI directs production (payback 5 mo gross, 1-2 yr with factory costs); days-weeks biological bound;
 ~10x productivity from AI-directed human labor as stage 1.

## 3. Implications for m8
- Td_mine_h = 6 yr too slow for a priority actor: boom evidence 2-2.5 yr. Use 3.5 (2-6) under race; 6 only for
  no-priority blocs.
- tau_phys 7 yr is not supported by current ramps; suggest 4 (2.5-7).
- Human-built robot growth: ~2x/yr near term is consistent with every modern physical ramp, braking with scale.
- Crude check: humanoid output 50k (2026) at 2x/yr braking at ~5-20M/yr -> ~100M cumulative by ~2036-2040. Physical
  capacity alone therefore allows closure of a leading actor's core chain mid/late 2030s; dexterity/capability and the
  slowest-input chokepoints (EUV, transformers, non-aligned mines) are what could push to 2040s. Do not attribute
  late closure to "historical speeds" of physical build-out; the evidence supports 1.5-2.5 yr doublings per sector.
- Counter-evidence (to avoid swinging): no example exists of an aggregate economy (all inputs) doubling in <7 yr;
  China's fastest (2000s) fixed capital ~12-15%/yr. Sector booms borrow labor/inputs from the rest of the economy.
