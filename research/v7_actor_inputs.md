# v7 actor inputs: 17 actors replacing m8_v4's 6 blocs

Date: 2026-10-16. Data only; no model code changed. Machine-readable values, per-country raw data, sources and per-field confidence and verified flags are in `v7_actor_inputs.json`. Every value there has the form {value, unit, year, source, confidence, verified, note}. "verified" means the figure was seen in a source fetched this session. "judgment" in a note marks an estimate.

## Sources used

- Population: UN WPP 2024 medium variant, 2026 (official CSV). World 8.30 bn; the 17 actors sum to 8.30 bn.
- Labor force and core workforce: ILOSTAT modelled estimates 2025 (labor force; employment by ISIC section). Taiwan is included in ILO.
- Military expenditure: SIPRI Military Expenditure Database, April 2026 release (2025 data, current USD). World total $2,887 bn (SIPRI fact sheet https://www.sipri.org/sites/default/files/2026-04/2604_milex_2025.pdf).
- Nuclear: FAS Status of World Nuclear Forces 2026 (https://fas.org/initiative/status-world-nuclear-forces/).
- Democracy: V-Dem v16 LDI for 2025 (via Our World in Data) and the V-Dem Democracy Report 2026 list of 44 autocratizers.
- Manufacturing and industry value added: World Bank NV.IND.MANF.CD and NV.IND.TOTL.CD, 2024. US from BEA via FRED (WB stops at 2021); Taiwan from DGBAS.
- Generating capacity: Ember yearly data, end-2025; China NEA 3,901 GW; national data for gaps.
- Rare earths: USGS Mineral Commodity Summaries 2026 (2025 mine output, world 390 kt). Refining and magnet shares from IEA (via secondary reports) plus company capacities.
- Robots: IFR World Robotics 2026 press releases (2025 installs 603,307; stock 5,079,078) and the IFR robot density release of 8 Apr 2026 (2024 data).
- Chips: SIA/BCG 2024 and TrendForce 2024 regional fab capacity, extrapolated to 2025. AI compute: Epoch AI GPU-cluster data (ends mid-2025), plus judgment for 2026.
- Social expenditure: OECD SOCX for OECD members, ILO World Social Protection Report 2024-26 Annex 6 (including health) for the rest. Population-weighted within actor; the JSON also has GDP-weighted values.
- State capacity: World Bank WGI Government Effectiveness, 2026 release (2025 data). Percentile ranks were computed from the scores over 213 economies, because the API no longer serves ranks. Class thresholds are judgment: high at the 70th percentile or above, medium 45 to 70, low below 45.

## Per-actor summary

Column notes:
- Pop: billions, 2026.
- LF and core: millions, 2025.
- Mil: SIPRI 2025, USD bn and share of world.
- LDI: population-weighted.
- Aut: share of the actor's population living in countries in an ongoing autocratization episode.
- MVA: share of world manufacturing value added, 2024.
- Ind: share of world industry value added, 2024.
- GW: installed generating capacity, end-2025.
- Fab: share of world fab capacity.
- Adv: share of advanced-node (7nm and below) capacity.
- AI: share of AI compute.
- Rob: robot density per 10k manufacturing employees, 2024.
- Soc: social expenditure, % of GDP.
- GE: Government Effectiveness percentile.

| Actor | Pop | LF | Core | Mil $bn (share) | LDI | Aut | Nuc | MVA | Ind | GW | Fab | Adv | AI | Rob | Soc | GE |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| US | 0.349 | 178 | 50.0 | 954 (33.1%) | 0.571 | 1.00 | 3,700 | 17.3% | 17.9% | 1,333 | 10% | 8% | 72% | 307 | 19.8 | 84 |
| JP | 0.122 | 69 | 21.8 | 62.2 (2.2%) | 0.734 | 0 | no (US umbrella) | 4.7% | 4.0% | 323 | 14% | 0 | 1.5% | 446 | 24.7 | 99.5 |
| KR | 0.052 | 30 | 9.7 | 47.8 (1.7%) | 0.739 | 0 | no (US umbrella) | 3.0% | 2.2% | 159 | 17% | 15% | 1% | 1,220 | 15.3 | 91 |
| TW | 0.023 | 12 | 5.1 | 18.2 (0.6%) | 0.704 | 0 | no | 1.7% | 1.1% | 63 | 18% | 70% | 0.3% | 302 | 11.0* | 91.5 |
| CN | 1.421 | 777 | 294.3 | 335.5 (11.6%) | 0.040 | 0.005 | 620 | 28.0% | 24.1% | 3,901 | 27% | 6% | 12% | 166 | 10.8 | 70 |
| WEU | 0.362 | 180 | 52.1 | 401.4 (13.9%) | 0.755 | 0.19 | 290 (FR) + US B61 hosts | 15.8% | 14.6% | 1,087 | 7% | 0.3% | 5% | 267 | 26.9 | 86 |
| EEU | 0.160 | 77 | 29.6 | 172.5 (6.0%) | 0.473 | 0.55 | no | 2.5% | 2.5% | 268 | 0.2% | 0 | 0.2% | 130 | 20.6 | 58 |
| UK | 0.070 | 35 | 8.3 | 89.0 (3.1%) | 0.689 | 1.00 | 225 | 1.8% | 2.2% | 111 | 0.4% | 0 | 1% | 110 | 23.0 | 86 |
| CANZ | 0.073 | 40 | 10.7 | 75.7 (2.6%) | 0.761 | 0 | no | 1.9% | 3.9% | 282 | 0.1% | 0 | 1% | 180 | 18.9 | 96 |
| RUS | 0.237 | 110 | 39.6 | 197.3 (6.8%) | 0.068 | 0.07 | 4,400 | 2.2% | 3.1% | 319 | 0.3% | 0 | 0.2% | ~10 | 15.6 | 31 |
| GULF | 0.062 | 34 | 11.9 | ~143 (5.0%) | 0.070 | 0.08 | no | 1.8% | 3.9% | 218 | 0 | 0 | 1.5% | ~10 | 8.7 | 72 |
| MENA | 0.576 | 184 | 63.5 | 143.3 (5.0%) | 0.140 | 0.03 | 90 (Israel) + US B61 host (Turkey) | 3.2% | 4.0% | 455 | 1.2% | 0.5% | 0.3% | ~30 | 9.6 | 32 |
| IN | 1.477 | 618 | 204.4 | 92.1 (3.2%) | 0.260 | 1.00 | 190 | 3.0% | 3.3% | 555 | 0.1% | 0 | 0.5% | ~9 | 5.1 | 67.5 |
| SAS | 0.537 | 187 | 59.1 | 17.9 (0.6%) | 0.182 | 0.56 | 170 (Pakistan) | 1.0% | 0.9% | 95 | 0 | 0 | 0 | ~1 | 2.1 | 26 |
| SEA | 0.750 | 382 | 120.4 | 71.0 (2.5%) | 0.238 | 0.64 | 60 (DPRK) | 4.9% | 4.9% | 369 | 4.5% | 0 | 4% | ~40 | 4.7 | 51 |
| LAC | 0.672 | 326 | 92.9 | 76.9 (2.7%) | 0.479 | 0.36 | no | 6.1% | 6.3% | 623 | 0.1% | 0 | 0.2% | ~25 | 14.3 | 42 |
| SSA | 1.358 | 545 | 101.7 | 25.8 (0.9%) | 0.243 | 0.18 | no | 1.2% | 1.8% | 153 | 0 | 0 | 0.1% | ~2 | 2.5 | 22 |

Values with "~" are judgment. Taiwan social expenditure (*) excludes health; the true figure is probably 14-15 (judgment). The UK's US B61s at Lakenheath are probable but not officially confirmed.

Other per-actor fields in the JSON:
- Robots: installs and stock.
- Humanoids: China above 97% of 1H2026 shipments of about 19.1k; US about 2%.
- Rare earths: mining, refining and NdFeB magnet shares.
- V-Dem regime types.
- Military spending at purchasing-power parity (PPP).
- Automation notes.

## Rare earths (USGS 2026; IEA via secondary sources)

- Mining shares: China 69%, US 13%, Australia (CANZ) 7.4%, SEA 6.9% (mostly Myanmar ore refined in China), SSA 1.1%, India and Russia 0.7% each.
- Refining: China about 91%, SEA about 3.5% (Lynas Malaysia), US about 2.5%.
- NdFeB magnets: China about 94%, Japan about 4%.
- The old RE_SHARE0 of 0.90 for China matches refining, not mining.
- China's April 2025 export controls still apply; the October 2025 expansion was suspended for a year in November 2025.
- US DoD-MP Materials deal (July 2025): a stake of about 15%, a $110/kg NdPr price floor, and a 10 kt/yr magnet plant due in 2028.

## Core workforce method (judgment parts labelled)

Core workforce is built from four pieces:
- ILO 2025 modelled employment in ISIC B, C, D-E and F.
- Transport H. ILO 2025 publishes H together with J, so H was split out using each country's latest labor force survey. A default H share of 0.70 was used where no survey split exists (China, Canada and others).
- An add-on of 4% of employment for repair and maintenance, security services and core admin. This is judgment; a 3-5% range is given in the JSON.

Results:
- Core workforce is 25-38% of labor force (China 38%, India 33%, SSA 19% because of agriculture).
- The old WORKFORCE values were 21-26% of the new labor force. About 4 points of the gap is the add-on.

## Reconciliation with the old 6 blocs

Population, new vs old (billions):
- US_bloc 0.546 vs 0.53.
- China_bloc 1.421 vs 1.42.
- Europe_plus 0.606 vs 0.62 counting only EU members of EEU; 0.665 counting all of EEU.
- Russia_MENA 0.876 vs 0.99 (-12%). The old figure probably included extra countries; Central Asia, 85M, is already inside RUS.
- South_Asia 2.013 vs 1.97.
- Global_South 2.779 vs 2.67. Sudan is assigned to SSA.

Leftovers not assigned in the old blocs:
- Ukraine, Moldova, Western Balkans and Kosovo: 59M people, 27.6M labor force, 9.8M core.
- Central Asia: 85M people, 10.1M core.
- 13 microstates (0.7M) are unassigned in v7: Andorra, Monaco, Liechtenstein, San Marino, Vatican, Faroes, Greenland, Gibraltar, Channel Islands, Isle of Man, Bermuda, St Pierre.

Old arrays that conflict with the new data by more than 25% (new vs old; Europe_plus here includes all EEU):
- WORKFORCE: Europe_plus 101 vs 77, Russia_MENA 115 vs 85, South_Asia 264 vs 200 (mostly the definition and add-on). US_bloc +15%, Global_South +20%, China matches.
- MFG_SHARE: China 0.28 vs 0.45; the old 0.45 matches a UNIDO 2030 projection, not current data. Europe_plus 0.22 vs 0.10, Russia_MENA 0.073 vs 0.03, South_Asia 0.040 vs 0.03, Global_South 0.121 vs 0.04. US_bloc 0.27 vs 0.35 (-23%).
- WORLD_W (industry VA): China 0.24 vs 0.35, Europe_plus 0.23 vs 0.15, Russia_MENA 0.11 vs 0.07, Global_South 0.13 vs 0.08.
- E_GW0: Europe_plus 1,748 vs 1,300, Russia_MENA 992 vs 700. The others match within 20%.
- CHIP_SHARE0, read as total fab capacity: Europe_plus 0.08 vs 0.03, Russia_MENA 0.015 vs 0.005, Global_South 0.046 vs 0.01. US_bloc 0.59 vs 0.70 and China 0.27 vs 0.35 are within 25%.
  - The old values sum to 1.09, so they may mix total and advanced capacity.
  - On advanced nodes the US_bloc holds 0.93 and China 0.06.
- ROBOT_SHARE0, read as humanoid shipments: US_bloc 0.025 vs 0.10, China 0.97 vs 0.83.
  - Industrial robot installs: China 0.59, US_bloc 0.19, Europe_plus 0.11 (vs 0.04), Global_South 0.05 (vs 0.01).
- RE_SHARE0 vs refining: US_bloc 0.03 vs 0.08. Small blocs differ, but all of them are tiny.
- P_EP0 (autocratization episode share): South_Asia 0.89 vs 0 (India and Pakistan are both in episodes), US_bloc 0.63 vs 1.0 (Japan, Korea and Taiwan are not autocratizing), Europe_plus 0.30 vs 0.40.
- X0 manufacturing column and G_IND:
  - IFR's revised China density (166, after a change in China's labor statistics, IFR 8 Apr 2026) puts China below the US bloc's employment-weighted density of about 380. The old X0 comment's 470 is outdated.
  - US robot stock is growing about 3-5%/yr, below G_IND 0.08. India's is growing about 15-17%, above 0.10.

Arrays within 25%: POP, MIL0, and D0 (pop-weighted LDI).
- MIL0 new: US_bloc 0.375, China 0.116, Europe_plus 0.256, Russia_MENA 0.167, South_Asia 0.038, Global_South 0.060.
- D0 new: US_bloc 0.63, China 0.04, Europe_plus 0.68, Russia_MENA 0.115, South_Asia 0.24, Global_South 0.30.

BASE_PROV analog: social spending as % of GDP relative to Western EU (26.9) gives:
- US about 0.45 to 0.55 of the Western EU level, China 0.40, RUS 0.58, GULF/MENA about 0.35, India 0.19, SAS/SSA about 0.08, SEA 0.17, LAC 0.53.
- Mapping this to provision levels is a modelling choice.

## Military PPP

SIPRI uses market exchange rates (MER).
- China: about $474 bn for 2024 at World Bank PPP (Fravel, Gilboy and Heginbotham 2024). Higher figures of about $700 bn exist, but they are not standard PPP.
- Russia: about $462 bn PPP for 2024 (IISS Military Balance 2025), about 3x MER. No 2025 PPP figure was found.
- India: no sourced PPP figure. A judgment multiplier of 1.5-2.5x applies, because imported equipment does not get the PPP discount.

## Alliances (full detail in JSON `alliances`)

All strength ratings are judgment on a 0-1 scale (1 = treaty with credible automatic defence).

| Arrangement | Actors | Mutual defence | Ext. nuclear | 2026 |
|---|---|---|---|---|
| Russia-Belarus Union State + security guarantees treaty (in force Mar 2025), Oreshnik on duty in Belarus Dec 2025 | RUS | yes | yes | 0.85 |
| US-Israel (no treaty; de facto, joint war on Iran 2026) | US, MENA | no formal | no | 0.80 |
| US-Japan 1960 | US, JP | yes (asymmetric) | yes | 0.70 |
| Russia-DPRK 2024 (Art. 4; DPRK troops in Kursk) | RUS, SEA | yes | no explicit | 0.70 |
| US-ROK 1953 + Washington Declaration | US, KR | yes | yes | 0.68 |
| NATO Art. 5 | US, WEU (most), EEU (EU + AL, ME, MK), UK, Canada, Turkey | yes ("such action as it deems necessary") | yes | 0.60 (US to WEU 0.55, US to EEU 0.50) |
| US-Philippines MDT 1951 | US, SEA | yes | declaratory | 0.55 |
| ANZUS | US, Australia (NZ suspended) | yes, weak wording | Australia only | 0.55 |
| Saudi-Pakistan SMDA (Sep 2025), extended as Mecca Joint Defence Agreement with Turkey (7 Aug 2026) | GULF, SAS, MENA | yes | ambiguous | 0.50 |
| China-DPRK 1961 | CN, SEA | yes (automatic) | no | 0.50 |
| EU Art. 42.7 | EU parts of WEU, EEU | yes | no | 0.45 |
| France-Poland Treaty of Nancy 2025 | WEU, EEU | yes | no | 0.45 |
| GCC Joint Defence 2000 | GULF | yes | no | 0.40 |
| US-Qatar executive order guarantee (Oct 2025) | US, GULF | unilateral | no | 0.40 |
| Northwood Declaration (UK-FR, Jul 2025); French "dissuasion avancée" (2 Mar 2026) | UK, WEU, EEU | political | emerging | 0.40 |
| CSTO (Armenia effectively suspended Apr 2026) | RUS, Armenia | yes | declaratory | 0.35 |
| US-Saudi Strategic Defense Agreement (Nov 2025) | US, GULF | no clause published | no | 0.35 |
| AUKUS, JEF, Sahel AES | various | no / no / yes | no | 0.35 |
| Taiwan Relations Act | US, TW | no (arms only) | no | 0.30 |
| Pakistan-China | CN, SAS | no | no | 0.30 |
| China-Russia 2001 + "no limits" | CN, RUS | no (consultation) | no | 0.20 |
| US-Thailand; Five Eyes | US, SEA / US, UK, CANZ | weak / intelligence only | no | 0.20 |
| Rio Treaty | US, LAC | yes on paper | no | 0.15 |
| India-Russia; Quad | | no | no | 0.10; 0.05 |

Reliability evidence from 2025-26 (spot-checked: the Germany troop cut and the Mecca agreement were confirmed by independent searches):
- US withdrawal from 66 international organizations (7 Jan 2026 memorandum).
- NATO 5% Hague commitment (June 2025); the Ankara summit (July 2026) reaffirmed Art. 5.
- Greenland: US tariffs on 8 NATO allies in January 2026, then reversed after a framework deal.
- US cut about 5,000 troops from Germany (announced 1 May 2026, after a Trump-Merz feud over the Iran war). Trump called NATO a "paper tiger."
- US/Israel war on Iran from 28 Feb 2026: Iran struck Gulf states, and Gulf officials complained of insufficient US defence. Saudi Arabia reportedly invoked the Pakistan pact in May 2026 (about 8,000 Pakistani troops; seen via Wikipedia citing Reuters).
- US capture of Maduro (3 Jan 2026).
- Trump discussed Taiwan arms sales with Xi in May and September 2026, contrary to the Six Assurances.
- Within-actor cohesion (judgment): WEU 0.65, RUS 0.45, GULF 0.45, EEU 0.40, SSA 0.15, SEA 0.10, LAC 0.10, MENA 0.05.

Historical base rates:
- Leeds, Long and Mitchell 2000 (JCR 44(5)): commitments honoured 74.5% of the time, 1816-1944 (verified from the abstract).
- Berkemeier and Fuhrmann 2018 (Research and Politics 5(2)): fulfilment 50% overall for 1816-2003; 66% before 1945 and 22% for 1945-2003 (few cases); defence pacts 41% (verified from the abstract).
- Leeds 2003 (AJPS 47(3)): defensive pacts reduce challenges to the protected state. This is contested post-1945 by Kenwick, Vasquez and Powers 2015.
- Fuhrmann and Sechser 2014 (AJPS 58(4)): pacts with nuclear states deter, but forward-deployed weapons add nothing.
- Leeds and Savun 2007 (JOP 69(4)): abrogation is likelier when power, threat or domestic institutions change. No numeric rate was retrieved, so this is unverified.

## Most uncertain inputs

1. AI compute shares for 2026 and fab and advanced-node shares for 2025. These are extrapolated from 2022-2024 data; the Epoch data ends mid-2025.
2. Non-China rare-earth refining and magnet shares. These are company-capacity judgment; the IEA China figures (91%, 94%) were seen only in secondary sources.
3. Core workforce. Two parts are judgment: the 4% add-on and the transport split where no survey exists.
4. Robot stock in 2025 and installs for Taiwan, Eastern Europe and the residual actors. Korea's 30k and India's 10.5k come from secondary reports of IFR WR2026.
5. GULF military spending. The UAE ($20-24 bn) is from secondary sources; Qatar (about $21 bn as a SIPRI regional residual vs Global Firepower's $12 bn) is uncertain by about $10 bn. Actor sums exceed SIPRI's world total by 1.3%.
6. Alliance strengths. All are judgment. Mecca pact text is unpublished, and the status of the Iran war from August to October 2026 is unverified.
7. Social expenditure. SOCX and ILO are not comparable (US 19.8 SOCX vs 26.4 ILO), and some ILO years are old.
8. Military spending at purchasing-power parity (PPP) for 2025. Only 2024 PPP figures exist (China, Russia); India has none.
