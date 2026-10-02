#!/bin/bash
# v6 final runs (GPU, sequential). Final configuration = M8_FINAL=1 (four final brakes + greenfield core loop + own-industry compute feedback + wide automated doubling floors).
set -e
cd "$(dirname "$0")"
R=../results
echo "== 1 m8 standalone"; date
M8_FINAL=1 M8_NVERIFY=0 M8_OUT=m8_v6_final.json M8_FIG="figures/m8v6_final" python m8_v4.py > $R/m8_v6_final_run_log.txt 2>&1
echo "== 2 integrated"; date
M8_FINAL=1 INT_OUT=integrated_v6_final.json INT_FIG="figures/v6_final" python integrate_v4.py > $R/integrated_v6_final_run_log.txt 2>&1
echo "== 3 matched greenfield on vs off (brakes on)"; date
M8_BRAKES=final python run_greenfield.py > $R/greenfield_v6_matched_run_log.txt 2>&1
[ "$SKIP_LEVER" = 1 ] && { echo "== lever skipped (run separately)"; exit 0; }
echo "== 4 lever grid"; date
M8_FINAL=1 LV_TAG=_v6_final python m9_lever.py all > $R/lever_v6_final_run_log.txt 2>&1
echo "== done"; date
